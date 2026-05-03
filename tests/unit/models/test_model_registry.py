import pytest

from antispoof.domain.models.metadata import ModelMetadata
from antispoof.infrastructure.models.registry import StaticModelRegistry


def test_static_model_registry_returns_model_by_identifier():
    model = ModelMetadata(
        model_id="credona.antispoof.test.v1",
        model_version="1.0.0",
        task="presentation_attack_detection",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.antispoof.policy.v1",
    )

    registry = StaticModelRegistry(models={model.model_id: model})

    assert registry.get(model.model_id) == model


def test_static_model_registry_rejects_unknown_identifier():
    model = ModelMetadata(
        model_id="credona.antispoof.test.v1",
        model_version="1.0.0",
        task="presentation_attack_detection",
        runtime="onnx",
        path="models/test.onnx",
        scoring_policy_id="credona.antispoof.policy.v1",
    )

    registry = StaticModelRegistry(models={model.model_id: model})

    with pytest.raises(ValueError, match="Unknown model identifier"):
        registry.get("credona.antispoof.unknown.v1")
