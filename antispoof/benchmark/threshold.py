from collections.abc import Sequence
from dataclasses import dataclass

from antispoof.metrics import AntiSpoofMetrics, compute_error_rates


@dataclass(frozen=True)
class ThresholdTuningResult:
    """Represents the best threshold found during benchmark tuning."""

    threshold: float
    metrics: AntiSpoofMetrics


def _build_candidate_thresholds(step: float) -> list[float]:
    """Build threshold candidates from 0.0 to 1.0 included."""
    if not 0.0 < step <= 1.0:
        raise ValueError("Threshold step must be greater than 0.0 and lower or equal to 1.0.")

    values: list[float] = []
    current = 0.0

    while current <= 1.0:
        values.append(round(current, 10))
        current += step

    if values[-1] != 1.0:
        values.append(1.0)

    return values


def _score_to_label(score: float, threshold: float) -> str:
    """Convert a realness score into a binary anti-spoof label."""
    return "real" if score >= threshold else "spoof"


def tune_threshold(
    ground_truth_labels: Sequence[str],
    real_scores: Sequence[float],
    step: float = 0.01,
) -> ThresholdTuningResult:
    """Find the threshold with the lowest ACER.

    real_scores must represent the calibrated probability-like score where:
    - high score means likely real
    - low score means likely spoof
    """
    if len(ground_truth_labels) != len(real_scores):
        raise ValueError("Ground truth and score lists must have the same length.")

    if not ground_truth_labels:
        raise ValueError("At least one benchmark sample is required.")

    best_result: ThresholdTuningResult | None = None

    for threshold in _build_candidate_thresholds(step):
        predicted_labels = [_score_to_label(score, threshold) for score in real_scores]

        metrics = compute_error_rates(ground_truth_labels, predicted_labels)
        current_result = ThresholdTuningResult(
            threshold=threshold,
            metrics=metrics,
        )

        if best_result is None or metrics.acer < best_result.metrics.acer:
            best_result = current_result

    if best_result is None:
        raise RuntimeError("Unable to tune threshold.")

    return best_result
