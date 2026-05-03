from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AntiSpoofResult:
    """Represents the result of an anti-spoofing inference.

    This object combines model prediction, heuristic analysis,
    calibrated signal_quality, and Credona trust scoring into a single,
    immutable structure.
    """

    is_real: bool
    signal_quality: float
    threshold: float
    label: str

    model_score: float
    spoof_score: float
    texture_score: float

    final_score: float
    cred_antispoof_score: float
    scores: list[float]

    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert the result to a serializable dictionary."""
        return {
            "is_real": self.is_real,
            "signal_quality": self.signal_quality,
            "threshold": self.threshold,
            "label": self.label,
            "model_score": self.model_score,
            "spoof_score": self.spoof_score,
            "texture_score": self.texture_score,
            "final_score": self.final_score,
            "cred_antispoof_score": self.cred_antispoof_score,
            "scores": self.scores,
            "details": self.details,
        }
