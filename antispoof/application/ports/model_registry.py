from typing import Protocol

from antispoof.domain.models.metadata import ModelMetadata


class ModelRegistryPort(Protocol):
    def get(self, model_id: str) -> ModelMetadata: ...

    def validate(self) -> None: ...
