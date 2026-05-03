from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class AntiSpoofMetrics:
    """Represents standard presentation attack detection metrics.

    APCER: Attack Presentation Classification Error Rate.
    BPCER: Bona Fide Presentation Classification Error Rate.
    ACER: Average Classification Error Rate.
    """

    apcer: float
    bpcer: float
    acer: float
    attack_count: int
    bona_fide_count: int


def _safe_divide(numerator: int, denominator: int) -> float:
    """Divide safely and return 0.0 when the denominator is zero."""
    if denominator == 0:
        return 0.0

    return numerator / denominator


def compute_error_rates(
    ground_truth_labels: Sequence[str],
    predicted_labels: Sequence[str],
) -> AntiSpoofMetrics:
    """Compute APCER, BPCER and ACER from benchmark labels.

    Expected labels:
    - "spoof" for attack presentations.
    - "real" for bona fide presentations.
    """
    if len(ground_truth_labels) != len(predicted_labels):
        raise ValueError("Ground truth and prediction lists must have the same length.")

    attack_count = 0
    bona_fide_count = 0
    attack_misclassified_as_real = 0
    bona_fide_misclassified_as_attack = 0

    for ground_truth, prediction in zip(ground_truth_labels, predicted_labels, strict=True):
        if ground_truth not in {"real", "spoof"}:
            raise ValueError(f"Unsupported ground truth label: {ground_truth}")

        if prediction not in {"real", "spoof"}:
            raise ValueError(f"Unsupported prediction label: {prediction}")

        if ground_truth == "spoof":
            attack_count += 1
            if prediction == "real":
                attack_misclassified_as_real += 1

        if ground_truth == "real":
            bona_fide_count += 1
            if prediction == "spoof":
                bona_fide_misclassified_as_attack += 1

    apcer = _safe_divide(attack_misclassified_as_real, attack_count)
    bpcer = _safe_divide(bona_fide_misclassified_as_attack, bona_fide_count)
    acer = (apcer + bpcer) / 2.0

    return AntiSpoofMetrics(
        apcer=apcer,
        bpcer=bpcer,
        acer=acer,
        attack_count=attack_count,
        bona_fide_count=bona_fide_count,
    )
