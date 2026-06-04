import json
from pathlib import Path

from antispoof.domain.calibration.trusted_registry import TrustedCalibrationRegistry


class FileTrustedCalibrationRegistryReader:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def read(self) -> TrustedCalibrationRegistry:
        payload = json.loads(self.path.read_text(encoding="utf-8"))

        return TrustedCalibrationRegistry(
            trusted_policy_ids=tuple(payload.get("trusted_policy_ids", ())),
            revoked_policy_ids=tuple(payload.get("revoked_policy_ids", ())),
        )
