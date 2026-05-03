from pathlib import Path
from typing import Any

import onnxruntime as ort

from antispoof.domain.models.metadata import ModelMetadata
from antispoof.exceptions import ModelNotFoundError
from antispoof.infrastructure.models.registry import (
    DEFAULT_ANTISPOOF_MODEL_ID,
    build_default_model_registry,
)


class AntiSpoofModelLoader:
    """Loads the configured anti-spoofing ONNX model."""

    def __init__(self, model: ModelMetadata | None = None):
        self.registry = build_default_model_registry()
        self.model = model or self.registry.get(DEFAULT_ANTISPOOF_MODEL_ID)
        self.model_path = Path(self.model.path)

    def exists(self) -> bool:
        return self.model_path.exists()

    def status(self) -> dict[str, Any]:
        return {
            "model_id": self.model.model_id,
            "model_version": self.model.model_version,
            "task": self.model.task,
            "runtime": self.model.runtime,
            "scoring_policy_id": self.model.scoring_policy_id,
            "exists": self.exists(),
        }

    def load(self) -> ort.InferenceSession:
        if not self.exists():
            raise ModelNotFoundError(
                "Configured anti-spoof model was not found. "
                "Run scripts/models/download_models.py before inference."
            )

        return ort.InferenceSession(
            str(self.model_path),
            providers=["CPUExecutionProvider"],
        )
