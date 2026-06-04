import json
from pathlib import Path

from antispoof.domain.calibration.manifest import CalibrationDistributionManifest


class FileCalibrationManifestReader:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def read(self) -> CalibrationDistributionManifest:
        payload = json.loads(self.path.read_text(encoding="utf-8"))

        return CalibrationDistributionManifest(
            service=payload["service"],
            contract_version=payload["contract_version"],
            model_identifier=payload["model_identifier"],
            allowed_policy_ids=tuple(payload.get("allowed_policy_ids", ())),
            revoked_policy_ids=tuple(payload.get("revoked_policy_ids", ())),
        )
