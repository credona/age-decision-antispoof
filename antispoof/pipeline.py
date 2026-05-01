from pathlib import Path

import numpy as np

from antispoof.domain.calibration import (
    calibrate_antispoof_confidence,
    compute_cred_antispoof_score,
)
from antispoof.domain.heuristics import (
    BlurHeuristicAnalyzer,
    ScreenPatternHeuristicAnalyzer,
    TextureHeuristicAnalyzer,
)
from antispoof.domain.result.antispoof_result import AntiSpoofResult
from antispoof.exceptions import NoFaceDetectedError
from antispoof.infrastructure.models.loader import AntiSpoofModelLoader
from antispoof.infrastructure.preprocessing.face_crop import resize_face_crop
from antispoof.infrastructure.preprocessing.image import read_image, read_image_from_bytes


class AntiSpoofPipeline:
    """Runs anti-spoofing inference using model and heuristic fusion."""

    def __init__(
        self,
        threshold: float = 0.5,
        model_weight: float = 0.7,
        texture_weight: float = 0.15,
        screen_weight: float = 0.15,
    ):
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0.")

        for name, value in {
            "model_weight": model_weight,
            "texture_weight": texture_weight,
            "screen_weight": screen_weight,
        }.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0.0 and 1.0.")

        if not abs((model_weight + texture_weight + screen_weight) - 1.0) < 1e-6:
            raise ValueError("Weights must sum to 1.0.")

        self.threshold = threshold
        self.model_weight = model_weight
        self.texture_weight = texture_weight
        self.screen_weight = screen_weight

        self.session = AntiSpoofModelLoader().load()
        self.input_name = self.session.get_inputs()[0].name

        self.texture_analyzer = TextureHeuristicAnalyzer()
        self.screen_analyzer = ScreenPatternHeuristicAnalyzer()
        self.blur_analyzer = BlurHeuristicAnalyzer()

    def preprocess(self, face_image: np.ndarray) -> np.ndarray:
        """Prepare a face crop for ONNX inference."""
        image = resize_face_crop(face_image, size=(80, 80))
        image = image.astype(np.float32)
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, axis=0)

        return image

    def _softmax(self, values: np.ndarray) -> np.ndarray:
        """Convert raw model logits into probabilities."""
        shifted_values = values - np.max(values)
        exp_values = np.exp(shifted_values)

        return exp_values / np.sum(exp_values)

    def _normalize_texture_score(self, texture_score: float) -> float:
        """Normalize texture score into the [0.0, 1.0] interval."""
        return min(texture_score / 255.0, 1.0)

    def _normalize_screen_score(self, screen_score: float) -> float:
        """Normalize screen pattern score into the [0.0, 1.0] interval."""
        return min(screen_score, 1.0)

    def predict(self, face_image: np.ndarray) -> AntiSpoofResult:
        """Predict whether a face crop is real or spoofed."""
        input_tensor = self.preprocess(face_image)
        outputs = self.session.run(None, {self.input_name: input_tensor})

        raw_scores = outputs[0][0]
        probabilities = self._softmax(raw_scores)

        # MiniFASNet-style 3-class handling:
        # index 1 is treated as bona fide / real.
        # index 0 and index 2 are treated as spoof classes.
        model_real_score = float(probabilities[1])
        spoof_score = float(probabilities[0] + probabilities[2])

        texture_result = self.texture_analyzer.analyze(face_image)
        screen_result = self.screen_analyzer.analyze(face_image)
        blur_result = self.blur_analyzer.analyze(face_image)

        texture_score = self._normalize_texture_score(texture_result.score)
        screen_score = self._normalize_screen_score(screen_result.score)

        raw_final_score = (
            self.model_weight * model_real_score
            + self.texture_weight * texture_score
            + self.screen_weight * (1.0 - screen_score)
        )

        final_score = calibrate_antispoof_confidence(raw_final_score)
        cred_antispoof_score = compute_cred_antispoof_score(final_score)

        is_real = final_score >= self.threshold

        return AntiSpoofResult(
            is_real=is_real,
            confidence=final_score,
            threshold=self.threshold,
            label="real" if is_real else "spoof",
            model_score=model_real_score,
            spoof_score=spoof_score,
            texture_score=texture_score,
            final_score=final_score,
            cred_antispoof_score=cred_antispoof_score,
            scores=probabilities.tolist(),
            details={
                "model": {
                    "real_score": model_real_score,
                    "spoof_score": spoof_score,
                    "raw_scores": raw_scores.tolist(),
                },
                "calibration": {
                    "method": "clamp_v1",
                    "raw_final_score": raw_final_score,
                    "calibrated_score": final_score,
                },
                "cred": {
                    "cred_antispoof_score": cred_antispoof_score,
                    "meaning": "higher_score_means_more_likely_real",
                },
                "texture": texture_result.to_dict(),
                "screen": screen_result.to_dict(),
                "blur": blur_result.to_dict(),
                "weights": {
                    "model": self.model_weight,
                    "texture": self.texture_weight,
                    "screen": self.screen_weight,
                },
            },
        )

    def predict_from_bytes(self, image_bytes: bytes) -> AntiSpoofResult:
        """Run anti-spoofing inference from encoded image bytes."""
        image = read_image_from_bytes(image_bytes)
        return self.predict(image)

    def predict_from_path(self, image_path: str | Path) -> AntiSpoofResult:
        """Run anti-spoofing inference from an image file path."""
        image = read_image(image_path)
        return self.predict(image)

    def predict_from_full_image(self, image: np.ndarray) -> AntiSpoofResult:
        """Detect a face from a full image and run anti-spoofing inference."""
        from antispoof.infrastructure.integrations.age_decision_core import (
            AgeDecisionCoreFaceDetector,
        )

        detector = AgeDecisionCoreFaceDetector()
        face_crop = detector.detect_and_crop(image)

        if face_crop is None:
            raise NoFaceDetectedError("No face detected in image.")

        return self.predict(face_crop)
