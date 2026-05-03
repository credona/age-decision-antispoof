def _clamp_score(value: float) -> float:
    """Clamp a score into the [0.0, 1.0] interval."""
    return max(0.0, min(float(value), 1.0))


def calibrate_signal_quality(raw_score: float) -> float:
    """Calibrate the anti-spoofing signal_quality score.

    The current version calibration is intentionally conservative:
    it only guarantees a valid probability-like interval.

    This function is isolated so future versions can replace it with
    dataset-based calibration such as Platt scaling, isotonic regression,
    or temperature scaling without changing the public API contract.
    """
    return _clamp_score(raw_score)


def compute_cred_antispoof_score(real_score: float) -> float:
    """Compute the Credona anti-spoof trust score.

    The score represents the credibility of the liveness evidence.
    A higher score means the image is more likely to be genuine.
    """
    return calibrate_signal_quality(real_score)
