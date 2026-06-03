from pathlib import Path

from antispoof.domain.calibration import CalibrationActivationError


class FileCalibrationPolicyReader:
    def __init__(self, path: str | None):
        self.path = path

    def read_policy_bytes(self) -> bytes:
        if not self.path:
            raise CalibrationActivationError("CALIBRATION_POLICY_PATH_MISSING")

        policy_path = Path(self.path)

        if not policy_path.exists() or not policy_path.is_file():
            raise CalibrationActivationError("CALIBRATION_POLICY_FILE_MISSING")

        return policy_path.read_bytes()
