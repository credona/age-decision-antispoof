from antispoof.domain.models.metadata import ModelMetadata

DEFAULT_ANTISPOOF_MODEL_ID = "credona.antispoof.minifasnet-v2.v1"
DEFAULT_ANTISPOOF_MODEL_VERSION = "1.0.0"
DEFAULT_ANTISPOOF_MODEL_PATH = "antispoof/models/MiniFASNetV2.onnx"
DEFAULT_ANTISPOOF_SCORING_POLICY_ID = "credona.antispoof.fusion-threshold.v1"


class StaticModelRegistry:
    def __init__(self, models: dict[str, ModelMetadata]):
        self.models = models
        self.validate()

    def get(self, model_id: str) -> ModelMetadata:
        try:
            return self.models[model_id]
        except KeyError as exc:
            raise ValueError("Unknown model identifier") from exc

    def validate(self) -> None:
        if not self.models:
            raise ValueError("Model registry must not be empty")

        for model in self.models.values():
            model.validate()


def build_default_model_registry() -> StaticModelRegistry:
    return StaticModelRegistry(
        models={
            DEFAULT_ANTISPOOF_MODEL_ID: ModelMetadata(
                model_id=DEFAULT_ANTISPOOF_MODEL_ID,
                model_version=DEFAULT_ANTISPOOF_MODEL_VERSION,
                task="presentation_attack_detection",
                runtime="onnx",
                path=DEFAULT_ANTISPOOF_MODEL_PATH,
                scoring_policy_id=DEFAULT_ANTISPOOF_SCORING_POLICY_ID,
                reproducibility={
                    "format": "onnx",
                    "execution_provider": "CPUExecutionProvider",
                },
            )
        }
    )
