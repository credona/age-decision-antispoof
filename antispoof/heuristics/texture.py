from dataclasses import dataclass
from typing import Dict, Any

import cv2
import numpy as np


@dataclass(frozen=True)
class TextureHeuristicResult:
    """Represents the result of a texture-based anti-spoofing heuristic."""

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


class TextureHeuristicAnalyzer:
    """Analyzes image texture using variance as a spoofing indicator.

    Rationale:
    - Real faces typically contain richer texture (skin details, micro-variations)
    - Spoof media (screens, prints) tend to be smoother or exhibit uniform patterns
    """

    def __init__(self, threshold: float = 100.0):
        """
        Args:
            threshold: Variance threshold separating spoof vs real-like texture.
                       This value is empirical and will be refined later.
        """
        if threshold < 0:
            raise ValueError("Threshold must be non-negative.")

        self.threshold = threshold

    def analyze(self, face_image: np.ndarray) -> TextureHeuristicResult:
        """Compute a texture score based on grayscale variance."""
        if face_image is None or face_image.size == 0:
            raise ValueError("Face image is empty.")

        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        variance = float(np.var(gray))

        label = "real" if variance >= self.threshold else "spoof"

        return TextureHeuristicResult(
            score=variance,
            threshold=self.threshold,
            label=label,
        )