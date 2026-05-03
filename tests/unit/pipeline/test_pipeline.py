import numpy as np

from antispoof import AntiSpoofPipeline, AntiSpoofResult


def test_pipeline_predict_returns_expected_structure():
    """Test that pipeline prediction returns the expected V1.1 structure."""
    pipeline = AntiSpoofPipeline()

    fake_face_crop = np.zeros((80, 80, 3), dtype=np.uint8)
    result = pipeline.predict(fake_face_crop)

    assert isinstance(result, AntiSpoofResult)

    assert isinstance(result.is_real, bool)
    assert isinstance(result.signal_quality, float)
    assert isinstance(result.model_score, float)
    assert isinstance(result.spoof_score, float)
    assert isinstance(result.texture_score, float)
    assert isinstance(result.final_score, float)
    assert isinstance(result.cred_antispoof_score, float)

    assert 0.0 <= result.signal_quality <= 1.0
    assert 0.0 <= result.spoof_score <= 1.0
    assert 0.0 <= result.cred_antispoof_score <= 1.0

    assert "screen" in result.details
    assert "texture" in result.details
    assert "blur" in result.details
    assert "model" in result.details
    assert "weights" in result.details
    assert "calibration" in result.details
    assert "cred" in result.details

    assert result.label in ["real", "spoof"]


def test_pipeline_result_to_dict_contains_v1_1_fields():
    """Test that serialized pipeline result exposes V1.1 score fields."""
    pipeline = AntiSpoofPipeline()

    fake_face_crop = np.zeros((80, 80, 3), dtype=np.uint8)
    result = pipeline.predict(fake_face_crop).to_dict()

    assert "spoof_score" in result
    assert "cred_antispoof_score" in result
    assert "final_score" in result
    assert "details" in result


def test_pipeline_uses_configurable_threshold():
    """Test configurable threshold."""
    pipeline = AntiSpoofPipeline(threshold=0.9)

    assert pipeline.threshold == 0.9


def test_pipeline_rejects_invalid_threshold():
    """Test invalid threshold values."""
    for threshold in [-0.1, 1.1]:
        try:
            AntiSpoofPipeline(threshold=threshold)
        except ValueError as exc:
            assert str(exc) == "threshold must be between 0.0 and 1.0"
        else:
            raise AssertionError("Expected ValueError for invalid threshold.")


def test_pipeline_rejects_invalid_weights():
    """Test invalid fusion weights."""
    try:
        AntiSpoofPipeline(model_weight=0.8, texture_weight=0.3, screen_weight=0.3)
    except ValueError as exc:
        assert str(exc) == "weights must sum to 1.0"
    else:
        raise AssertionError("Expected ValueError for invalid weights.")
