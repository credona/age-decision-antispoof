import pytest

from antispoof.benchmark import tune_threshold


def test_tune_threshold_finds_lowest_acer():
    """Test threshold tuning with separable benchmark scores."""
    ground_truth = ["spoof", "spoof", "real", "real"]
    real_scores = [0.1, 0.2, 0.8, 0.9]

    result = tune_threshold(
        ground_truth_labels=ground_truth,
        real_scores=real_scores,
        step=0.1,
    )

    assert result.metrics.acer == 0.0
    assert 0.3 <= result.threshold <= 0.8


def test_tune_threshold_rejects_mismatched_lengths():
    """Test threshold tuning rejects mismatched inputs."""
    with pytest.raises(ValueError) as exc:
        tune_threshold(["real"], [0.8, 0.9])

    assert str(exc.value) == "Ground truth and score lists must have the same length."


def test_tune_threshold_rejects_empty_dataset():
    """Test threshold tuning rejects empty benchmark data."""
    with pytest.raises(ValueError) as exc:
        tune_threshold([], [])

    assert str(exc.value) == "At least one benchmark sample is required."


def test_tune_threshold_rejects_invalid_step():
    """Test threshold tuning rejects invalid threshold steps."""
    with pytest.raises(ValueError) as exc:
        tune_threshold(["real"], [0.8], step=0.0)

    assert str(exc.value) == (
        "Threshold step must be greater than 0.0 and lower or equal to 1.0."
    )