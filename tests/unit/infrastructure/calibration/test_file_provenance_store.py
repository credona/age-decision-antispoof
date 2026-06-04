import json
from pathlib import Path

from antispoof.domain.calibration.provenance import CalibrationProvenanceRecord
from antispoof.infrastructure.calibration.file_provenance_store import (
    FileCalibrationProvenanceStore,
)


def test_file_provenance_store_appends_jsonl_records(tmp_path: Path) -> None:
    path = tmp_path / "provenance.jsonl"
    store = FileCalibrationProvenanceStore(path)

    store.append(
        CalibrationProvenanceRecord(
            event="activated",
            policy_id="policy-1",
            previous_policy_id=None,
            service="antispoof",
            contract_version="2.6",
            model_identifier="credona.antispoof.minifasnet-v2.v1",
            created_at="2026-06-04T00:00:00+00:00",
        )
    )
    store.append(
        CalibrationProvenanceRecord(
            event="rollback",
            policy_id="policy-0",
            previous_policy_id="policy-1",
            service="antispoof",
            contract_version="2.6",
            model_identifier="credona.antispoof.minifasnet-v2.v1",
            created_at="2026-06-04T01:00:00+00:00",
        )
    )

    lines = path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2
    assert json.loads(lines[0])["event"] == "activated"
    assert json.loads(lines[1])["event"] == "rollback"
