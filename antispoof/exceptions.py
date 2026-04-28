class AntiSpoofError(Exception):
    """Base exception for all anti-spoofing errors."""


class ModelNotFoundError(AntiSpoofError):
    """Raised when the anti-spoofing model file cannot be found."""


class FaceDetectionUnavailableError(AntiSpoofError):
    """Raised when the optional face detection dependency is unavailable."""


class NoFaceDetectedError(AntiSpoofError):
    """Raised when no face can be detected in the provided image."""
