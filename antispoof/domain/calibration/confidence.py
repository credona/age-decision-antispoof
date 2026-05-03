def _clamp_score(value: float) -> float:
    return max(0.0, min(float(value), 1.0))


def calibrate_signal_quality(raw_score: float) -> float:
    return _clamp_score(raw_score)


def compute_cred_antispoof_score(real_score: float) -> float:
    return calibrate_signal_quality(real_score)
