from antispoof.domain.metrics import compute_error_rates


def test_compute_error_rates():
    """Test APCER, BPCER and ACER computation."""
    ground_truth = ["real", "real", "spoof", "spoof"]
    predictions = ["real", "spoof", "spoof", "real"]

    metrics = compute_error_rates(ground_truth, predictions)

    assert metrics.attack_count == 2
    assert metrics.bona_fide_count == 2
    assert metrics.apcer == 0.5
    assert metrics.bpcer == 0.5
    assert metrics.acer == 0.5


def test_compute_error_rates_with_perfect_predictions():
    """Test metrics with no classification error."""
    ground_truth = ["real", "real", "spoof", "spoof"]
    predictions = ["real", "real", "spoof", "spoof"]

    metrics = compute_error_rates(ground_truth, predictions)

    assert metrics.apcer == 0.0
    assert metrics.bpcer == 0.0
    assert metrics.acer == 0.0


def test_compute_error_rates_rejects_different_lengths():
    """Test metrics reject mismatched input lengths."""
    try:
        compute_error_rates(["real"], ["real", "spoof"])
    except ValueError as exc:
        assert str(exc) == "Ground truth and prediction lists must have the same length."
    else:
        raise AssertionError("Expected ValueError for mismatched input lengths.")


def test_compute_error_rates_rejects_invalid_ground_truth_label():
    """Test metrics reject unsupported ground truth labels."""
    try:
        compute_error_rates(["unknown"], ["real"])
    except ValueError as exc:
        assert str(exc) == "Unsupported ground truth label: unknown"
    else:
        raise AssertionError("Expected ValueError for invalid ground truth label.")


def test_compute_error_rates_rejects_invalid_prediction_label():
    """Test metrics reject unsupported prediction labels."""
    try:
        compute_error_rates(["real"], ["unknown"])
    except ValueError as exc:
        assert str(exc) == "Unsupported prediction label: unknown"
    else:
        raise AssertionError("Expected ValueError for invalid prediction label.")
