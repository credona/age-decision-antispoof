from dataclasses import dataclass
from typing import Dict, Any

import cv2
import numpy as np


@dataclass(frozen=True)
class BlurHeuristicResult:
    """Represents the result of a blur/focus heuristic.

    This signal is primarily used as an image quality indicator.
    Low sharpness may indicate spoof artifacts or poor acquisition conditions.
    """

    score: float
    threshold: float
    label: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a serializable dictionary."""
        return {
            "score": self.score,
            "threshold": self.threshold,
            "label": self.label,
        }


class BlurHeuristicAnalyzer:
    """Detects blur using the variance of the Laplacian.

    Rationale:
    - Sharp images have high Laplacian variance
    - Blurry images have low Laplacian variance
    """

    def __init__(self, threshold: float = 50.0):
        """
        Args:
            threshold: Minimum sharpness required to consider the image as focused.
        """
        if threshold < 0:
            raise ValueError("Threshold must be non-negative.")

        self.threshold = threshold

    def analyze(self, face_image: np.ndarray) -> BlurHeuristicResult:
        """Compute blur score using Laplacian variance."""
        if face_image is None or face_image.size == 0:
            raise ValueError("Face image is empty.")

        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = float(laplacian.var())

        label = "sharp" if variance >= self.threshold else "blurry"

        return BlurHeuristicResult(
            score=variance,
            threshold=self.threshold,
            label=label,
        )