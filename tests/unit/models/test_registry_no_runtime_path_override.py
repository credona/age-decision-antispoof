import os

from antispoof.infrastructure.models.registry import (
    DEFAULT_ANTISPOOF_MODEL_ID,
    DEFAULT_ANTISPOOF_MODEL_PATH,
    build_default_model_registry,
)


def test_default_registry_ignores_runtime_model_path_override(monkeypatch):
    monkeypatch.setenv("ANTISPOOF_MODEL_PATH", "unsafe/runtime/path.onnx")

    registry = build_default_model_registry()
    model = registry.get(DEFAULT_ANTISPOOF_MODEL_ID)

    assert model.path == DEFAULT_ANTISPOOF_MODEL_PATH


def test_default_registry_does_not_depend_on_runtime_model_identifier_override(monkeypatch):
    monkeypatch.setenv("ANTISPOOF_MODEL_ID", "unsafe.runtime.model")

    registry = build_default_model_registry()
    model = registry.get(DEFAULT_ANTISPOOF_MODEL_ID)

    assert model.model_id == DEFAULT_ANTISPOOF_MODEL_ID
    assert os.getenv("ANTISPOOF_MODEL_ID") == "unsafe.runtime.model"
