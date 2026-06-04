import json
from pathlib import Path

import pytest

from antispoof.infrastructure.calibration.runtime_activation import (
    rollback_antispoof_runtime_calibration,
)
from antispoof.infrastructure.models.registry import DEFAULT_ANTISPOOF_MODEL_ID
from antispoof.project import project_metadata


def test_runtime_rollback_restores_previous_policy_and_writes_records(
    tmp_path: Path,
    monkeypatch,
) -> None:
    lifecycle_path = tmp_path / "runtime" / "lifecycle.json"
    provenance_path = tmp_path / "runtime" / "provenance.jsonl"
    attestation_path = tmp_path / "runtime" / "rollback-attestation.json"

    lifecycle_path.parent.mkdir(parents=True)
    lifecycle_path.write_text(
        json.dumps(
            {
                "active_policy_id": "policy-2",
                "previous_policy_id": "policy-1",
                "activated_at": "2026-06-04T00:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH", str(lifecycle_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_PROVENANCE_PATH", str(provenance_path))
    monkeypatch.setenv(
        "ANTISPOOF_CALIBRATION_ROLLBACK_ATTESTATION_PATH",
        str(attestation_path),
    )

    state = rollback_antispoof_runtime_calibration()

    assert state.active_policy_id == "policy-1"
    assert state.previous_policy_id == "policy-2"

    persisted = json.loads(lifecycle_path.read_text(encoding="utf-8"))
    assert persisted["active_policy_id"] == "policy-1"
    assert persisted["previous_policy_id"] == "policy-2"

    provenance_lines = provenance_path.read_text(encoding="utf-8").splitlines()
    assert len(provenance_lines) == 1
    assert json.loads(provenance_lines[0])["event"] == "rollback"

    attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
    assert attestation["attestation_type"] == "rollback"
    assert attestation["policy_id"] == "policy-1"


def test_runtime_rollback_requires_lifecycle_provenance_and_attestation_paths(
    monkeypatch,
) -> None:
    monkeypatch.delenv("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH", raising=False)
    monkeypatch.delenv("ANTISPOOF_CALIBRATION_PROVENANCE_PATH", raising=False)
    monkeypatch.delenv("ANTISPOOF_CALIBRATION_ROLLBACK_ATTESTATION_PATH", raising=False)

    with pytest.raises(ValueError, match="ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH_MISSING"):
        rollback_antispoof_runtime_calibration()


def test_runtime_rollback_uses_expected_service_metadata(tmp_path: Path, monkeypatch) -> None:
    lifecycle_path = tmp_path / "lifecycle.json"
    provenance_path = tmp_path / "provenance.jsonl"
    attestation_path = tmp_path / "rollback-attestation.json"

    lifecycle_path.write_text(
        json.dumps(
            {
                "active_policy_id": "policy-2",
                "previous_policy_id": "policy-1",
                "activated_at": "2026-06-04T00:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH", str(lifecycle_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_PROVENANCE_PATH", str(provenance_path))
    monkeypatch.setenv(
        "ANTISPOOF_CALIBRATION_ROLLBACK_ATTESTATION_PATH",
        str(attestation_path),
    )

    rollback_antispoof_runtime_calibration()

    record = json.loads(provenance_path.read_text(encoding="utf-8").splitlines()[0])

    assert record["service"] == "antispoof"
    assert record["contract_version"] == project_metadata.contract_version
    assert record["model_identifier"] == DEFAULT_ANTISPOOF_MODEL_ID
