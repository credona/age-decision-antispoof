import json
from pathlib import Path

from antispoof.domain.calibration.attestation import CalibrationAttestation


class FileCalibrationAttestationWriter:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def write(self, attestation: CalibrationAttestation) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(attestation.to_dict(), sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
