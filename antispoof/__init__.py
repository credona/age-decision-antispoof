from antispoof.domain.result.antispoof_result import AntiSpoofResult
from antispoof.exceptions import (
    AntiSpoofError,
    FaceDetectionUnavailableError,
    ModelNotFoundError,
    NoFaceDetectedError,
)
from antispoof.pipeline import AntiSpoofPipeline

AntiSpoof = AntiSpoofPipeline

__all__ = [
    "AntiSpoof",
    "AntiSpoofPipeline",
    "AntiSpoofResult",
    "AntiSpoofError",
    "ModelNotFoundError",
    "FaceDetectionUnavailableError",
    "NoFaceDetectedError",
]
