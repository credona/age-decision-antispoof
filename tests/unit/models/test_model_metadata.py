import pytest

from antispoof.domain.models.metadata import ModelMetadata


def test_model_metadata_accepts_valid_definition():
    metadata = ModelMetadata(
        model_id="credona.antispoof.test.v1",
        model_version="1.0.0",
        task="presentation_attack_detection",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.antispoof.policy.v1",
    )

    metadata.validate()


def test_model_metadata_rejects_unsupported_task():
    metadata = ModelMetadata(
        model_id="credona.antispoof.test.v1",
        model_version="1.0.0",
        task="age_estimation",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.antispoof.policy.v1",
    )

    with pytest.raises(ValueError, match="unsupported model task"):
        metadata.validate()


def test_model_metadata_rejects_unsupported_runtime():
    metadata = ModelMetadata(
        model_id="credona.antispoof.test.v1",
        model_version="1.0.0",
        task="presentation_attack_detection",
        runtime="pytorch",
        path="models/test.onnx",
        scoring_policy_id="credona.antispoof.policy.v1",
    )

    with pytest.raises(ValueError, match="unsupported model runtime"):
        metadata.validate()
