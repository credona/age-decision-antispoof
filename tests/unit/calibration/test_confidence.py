from antispoof.domain.calibration import (
    calibrate_signal_quality,
    compute_cred_antispoof_score,
)


def test_calibrate_signal_quality_clamps_low_values():
    assert calibrate_signal_quality(-0.5) == 0.0


def test_calibrate_signal_quality_clamps_high_values():
    assert calibrate_signal_quality(1.5) == 1.0


def test_calibrate_signal_quality_keeps_valid_values():
    assert calibrate_signal_quality(0.73) == 0.73


def test_compute_cred_antispoof_score():
    assert compute_cred_antispoof_score(0.82) == 0.82


def test_cred_antispoof_score_is_stable_for_same_input():
    assert compute_cred_antispoof_score(0.64) == compute_cred_antispoof_score(0.64)


def test_cred_antispoof_score_is_monotonic():
    assert compute_cred_antispoof_score(0.9) >= compute_cred_antispoof_score(0.4)


def test_cred_antispoof_score_is_bounded():
    assert 0.0 <= compute_cred_antispoof_score(2.0) <= 1.0
    assert 0.0 <= compute_cred_antispoof_score(-1.0) <= 1.0
