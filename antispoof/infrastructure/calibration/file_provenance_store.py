import json
from pathlib import Path

from antispoof.domain.calibration.provenance import CalibrationProvenanceRecord


class FileCalibrationProvenanceStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(self, record: CalibrationProvenanceRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
