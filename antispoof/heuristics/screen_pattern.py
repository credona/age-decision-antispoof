from dataclasses import dataclass
from typing import Dict, Any

import cv2
import numpy as np


@dataclass(frozen=True)
class ScreenPatternHeuristicResult:
    """Represents the result of a screen pattern (moire) heuristic."""

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


class ScreenPatternHeuristicAnalyzer:
    """Detects periodic patterns typical of screens using frequency analysis.

    Rationale:
    - Screens introduce periodic structures (pixel grid, refresh artifacts)
    - These patterns appear as peaks in the frequency domain (FFT)
    """

    def __init__(self, threshold: float = 0.2):
        """
        Args:
            threshold: Energy ratio threshold indicating suspicious periodic patterns.
        """
        if threshold < 0:
            raise ValueError("Threshold must be non-negative.")

        self.threshold = threshold

    def analyze(self, face_image: np.ndarray) -> ScreenPatternHeuristicResult:
        """Analyze frequency domain to detect screen-like patterns."""
        if face_image is None or face_image.size == 0:
            raise ValueError("Face image is empty.")

        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

        # FFT
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude = np.abs(fshift)

        # Normalize
        magnitude = magnitude / (np.max(magnitude) + 1e-8)

        # Compute energy outside low-frequency center
        h, w = magnitude.shape
        center_h, center_w = h // 2, w // 2

        radius = min(h, w) // 8

        mask = np.ones_like(magnitude, dtype=np.uint8)
        mask[
            center_h - radius:center_h + radius,
            center_w - radius:center_w + radius,
        ] = 0

        high_freq_energy = float(np.mean(magnitude[mask == 1]))

        label = "spoof" if high_freq_energy >= self.threshold else "real"

        return ScreenPatternHeuristicResult(
            score=high_freq_energy,
            threshold=self.threshold,
            label=label,
        )