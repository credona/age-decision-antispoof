class CalibrationError(Exception):
    """Base error for runtime calibration."""


class CalibrationActivationError(CalibrationError):
    """Raised when runtime calibration cannot be activated."""


class CalibrationCompatibilityError(CalibrationError):
    """Raised when a calibration policy is incompatible with this service."""


class CalibrationIntegrityError(CalibrationError):
    """Raised when calibration policy integrity validation fails."""


class CalibrationSignatureError(CalibrationError):
    """Raised when calibration policy signature validation fails."""
