from antispoof.exceptions import (
    AntiSpoofError,
    FaceDetectionUnavailableError,
    ModelNotFoundError,
    NoFaceDetectedError,
)
from antispoof.pipeline import AntiSpoofPipeline
from antispoof.result import AntiSpoofResult

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
