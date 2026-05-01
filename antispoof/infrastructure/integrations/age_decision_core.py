import numpy as np

from antispoof.exceptions import FaceDetectionUnavailableError


class AgeDecisionCoreFaceDetector:
    """Wrapper around age-decision-core face detection.

    This wrapper keeps age-decision-core optional. The dependency is imported
    only when full-image prediction is requested.
    """

    def __init__(self):
        try:
            from age_decision_core import FaceDetector  # type: ignore
        except ImportError as exc:
            raise FaceDetectionUnavailableError(
                "age-decision-core is required for face detection. "
                "Install it to use predict_from_full_image()."
            ) from exc

        self.detector = FaceDetector()

    def detect_and_crop(self, image: np.ndarray) -> np.ndarray | None:
        """Detect the primary face and return its cropped image."""
        faces = self.detector.detect(image)

        if not faces:
            return None

        x, y, w, h = faces[0]

        return image[y : y + h, x : x + w]
