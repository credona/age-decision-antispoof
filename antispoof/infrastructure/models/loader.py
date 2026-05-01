import os
from pathlib import Path
from typing import Any

import onnxruntime as ort

from antispoof.exceptions import ModelNotFoundError

DEFAULT_MODEL_PATH = "antispoof/models/MiniFASNetV2.onnx"


class AntiSpoofModelLoader:
    """Loads the ONNX anti-spoofing model."""

    def __init__(self, model_path: str | Path | None = None):
        resolved_path = model_path or os.getenv("ANTISPOOF_MODEL_PATH", DEFAULT_MODEL_PATH)
        self.model_path = Path(resolved_path)

    def exists(self) -> bool:
        """Return whether the configured model file exists."""
        return self.model_path.exists()

    def status(self) -> dict[str, Any]:
        """Return model metadata without loading the model again."""
        return {
            "type": "onnx",
            "name": "MiniFASNetV2",
            "path": str(self.model_path),
            "exists": self.exists(),
        }

    def load(self) -> ort.InferenceSession:
        """Load the ONNX model and return an inference session."""
        if not self.exists():
            raise ModelNotFoundError(
                f"Model not found at {self.model_path}. "
                "Run scripts/download_models.py before inference."
            )

        return ort.InferenceSession(
            str(self.model_path),
            providers=["CPUExecutionProvider"],
        )
