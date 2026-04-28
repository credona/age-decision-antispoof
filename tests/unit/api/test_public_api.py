from antispoof import (
    AntiSpoof,
    AntiSpoofError,
    AntiSpoofPipeline,
    AntiSpoofResult,
    FaceDetectionUnavailableError,
    ModelNotFoundError,
    NoFaceDetectedError,
)


def test_public_api_exports():
    """Ensure public Python API exports remain stable."""
    assert AntiSpoof is AntiSpoofPipeline
    assert AntiSpoofResult is not None
    assert AntiSpoofError is not None
    assert ModelNotFoundError is not None
    assert FaceDetectionUnavailableError is not None
    assert NoFaceDetectedError is not None
