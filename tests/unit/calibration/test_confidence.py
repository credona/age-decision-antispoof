from antispoof.domain.calibration import (
    calibrate_signal_quality,
    compute_cred_antispoof_score,
)


def test_calibrate_signal_quality_clamps_low_values():
    """Test that calibration clamps values below zero."""
    assert calibrate_signal_quality(-0.5) == 0.0


def test_calibrate_signal_quality_clamps_high_values():
    """Test that calibration clamps values above one."""
    assert calibrate_signal_quality(1.5) == 1.0


def test_calibrate_signal_quality_keeps_valid_values():
    """Test that calibration keeps valid probability-like values."""
    assert calibrate_signal_quality(0.73) == 0.73


def test_compute_cred_antispoof_score():
    """Test Credona anti-spoof trust score computation."""
    assert compute_cred_antispoof_score(0.82) == 0.82
