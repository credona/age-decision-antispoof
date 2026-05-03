from pathlib import Path

import numpy as np

from antispoof.domain.calibration import (
    calibrate_signal_quality,
    compute_cred_antispoof_score,
)
from antispoof.domain.constants import DECISION_REAL, DECISION_SPOOF
from antispoof.domain.heuristics import (
    BlurHeuristicAnalyzer,
    ScreenPatternHeuristicAnalyzer,
    TextureHeuristicAnalyzer,
)
from antispoof.domain.result.antispoof_result import AntiSpoofResult
from antispoof.domain.scoring.policy import (
    AntispoofScoringPolicy,
    default_antispoof_scoring_policy,
)
from antispoof.exceptions import NoFaceDetectedError
from antispoof.infrastructure.models.loader import AntiSpoofModelLoader
from antispoof.infrastructure.preprocessing.face_crop import resize_face_crop
from antispoof.infrastructure.preprocessing.image import read_image, read_image_from_bytes


class AntiSpoofPipeline:
    """Runs anti-spoofing inference using deterministic policy-based fusion."""

    def __init__(
        self,
        threshold: float | None = None,
        model_weight: float | None = None,
        texture_weight: float | None = None,
        screen_weight: float | None = None,
        scoring_policy: AntispoofScoringPolicy | None = None,
    ):
        base_policy = scoring_policy or default_antispoof_scoring_policy()

        self.scoring_policy = AntispoofScoringPolicy(
            policy_id=base_policy.policy_id,
            threshold=threshold if threshold is not None else base_policy.threshold,
            model_weight=(model_weight if model_weight is not None else base_policy.model_weight),
            texture_weight=(
                texture_weight if texture_weight is not None else base_policy.texture_weight
            ),
            screen_weight=(
                screen_weight if screen_weight is not None else base_policy.screen_weight
            ),
            calibration_method=base_policy.calibration_method,
        )
        self.scoring_policy.validate()

        self.threshold = self.scoring_policy.threshold
        self.model_weight = self.scoring_policy.model_weight
        self.texture_weight = self.scoring_policy.texture_weight
        self.screen_weight = self.scoring_policy.screen_weight

        self.session = AntiSpoofModelLoader().load()
        self.input_name = self.session.get_inputs()[0].name

        self.texture_analyzer = TextureHeuristicAnalyzer()
        self.screen_analyzer = ScreenPatternHeuristicAnalyzer()
        self.blur_analyzer = BlurHeuristicAnalyzer()

    def preprocess(self, face_image: np.ndarray) -> np.ndarray:
        image = resize_face_crop(face_image, size=(80, 80))
        image = image.astype(np.float32)
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, axis=0)

        return image

    def _softmax(self, values: np.ndarray) -> np.ndarray:
        shifted_values = values - np.max(values)
        exp_values = np.exp(shifted_values)

        return exp_values / np.sum(exp_values)

    def _normalize_texture_score(self, texture_score: float) -> float:
        return min(max(texture_score / 255.0, 0.0), 1.0)

    def _normalize_screen_score(self, screen_score: float) -> float:
        return min(max(screen_score, 0.0), 1.0)

    def predict(self, face_image: np.ndarray) -> AntiSpoofResult:
        input_tensor = self.preprocess(face_image)
        outputs = self.session.run(None, {self.input_name: input_tensor})

        raw_scores = outputs[0][0]
        probabilities = self._softmax(raw_scores)

        model_real_score = float(probabilities[1])
        spoof_score = float(probabilities[0] + probabilities[2])

        texture_result = self.texture_analyzer.analyze(face_image)
        screen_result = self.screen_analyzer.analyze(face_image)
        blur_result = self.blur_analyzer.analyze(face_image)

        texture_score = self._normalize_texture_score(texture_result.score)
        screen_score = self._normalize_screen_score(screen_result.score)

        raw_final_score = (
            self.scoring_policy.model_weight * model_real_score
            + self.scoring_policy.texture_weight * texture_score
            + self.scoring_policy.screen_weight * (1.0 - screen_score)
        )

        final_score = calibrate_signal_quality(raw_final_score)
        cred_antispoof_score = compute_cred_antispoof_score(final_score)

        is_real = final_score >= self.scoring_policy.threshold

        return AntiSpoofResult(
            is_real=is_real,
            signal_quality=final_score,
            threshold=self.scoring_policy.threshold,
            label=DECISION_REAL if is_real else DECISION_SPOOF,
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
                    "method": self.scoring_policy.calibration_method,
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
                    "model": self.scoring_policy.model_weight,
                    "texture": self.scoring_policy.texture_weight,
                    "screen": self.scoring_policy.screen_weight,
                },
            },
        )

    def predict_from_bytes(self, image_bytes: bytes) -> AntiSpoofResult:
        image = read_image_from_bytes(image_bytes)
        return self.predict(image)

    def predict_from_path(self, image_path: str | Path) -> AntiSpoofResult:
        image = read_image(image_path)
        return self.predict(image)

    def predict_from_full_image(self, image: np.ndarray) -> AntiSpoofResult:
        from antispoof.infrastructure.integrations.age_decision_core import (
            AgeDecisionCoreFaceDetector,
        )

        detector = AgeDecisionCoreFaceDetector()
        face_crop = detector.detect_and_crop(image)

        if face_crop is None:
            raise NoFaceDetectedError("No face detected in image.")

        return self.predict(face_crop)
