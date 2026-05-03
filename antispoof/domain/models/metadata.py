from dataclasses import dataclass, field
from typing import Any

SUPPORTED_MODEL_RUNTIMES = {"onnx", "mock"}
SUPPORTED_MODEL_TASKS = {"presentation_attack_detection"}


@dataclass(frozen=True)
class ModelMetadata:
    model_id: str
    model_version: str
    task: str
    runtime: str
    path: str
    scoring_policy_id: str
    reproducibility: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.model_id:
            raise ValueError("model_id is required")

        if not self.model_version:
            raise ValueError("model_version is required")

        if self.task not in SUPPORTED_MODEL_TASKS:
            raise ValueError("unsupported model task")

        if self.runtime not in SUPPORTED_MODEL_RUNTIMES:
            raise ValueError("unsupported model runtime")

        if not self.path:
            raise ValueError("model path is required")

        if not self.scoring_policy_id:
            raise ValueError("scoring_policy_id is required")
