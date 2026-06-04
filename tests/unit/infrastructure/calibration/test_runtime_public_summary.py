import json
from pathlib import Path

from antispoof.infrastructure.calibration.runtime_activation import (
    get_antispoof_public_calibration_summary,
)
from antispoof.infrastructure.models.registry import DEFAULT_ANTISPOOF_MODEL_ID
from antispoof.project import project_metadata


def test_runtime_public_summary_returns_empty_summary_without_active_state(
    tmp_path: Path,
    monkeypatch,
) -> None:
    lifecycle_path = tmp_path / "lifecycle.json"

    monkeypatch.setenv("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH", str(lifecycle_path))

    summary = get_antispoof_public_calibration_summary().to_dict()

    assert summary["active_policy_id"] is None
    assert summary["benchmark_attestation_id"] is None
    assert summary["service"] == "antispoof"
    assert summary["contract_version"] == project_metadata.contract_version
    assert summary["model_identifier"] == DEFAULT_ANTISPOOF_MODEL_ID


def test_runtime_public_summary_uses_active_policy_metadata(
    tmp_path: Path,
    monkeypatch,
) -> None:
    lifecycle_path = tmp_path / "lifecycle.json"
    active_policy_metadata_path = tmp_path / "active-policy-metadata.json"

    lifecycle_path.write_text(
        json.dumps(
            {
                "active_policy_id": "policy-1",
                "previous_policy_id": "policy-0",
                "activated_at": "2026-06-04T00:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    active_policy_metadata_path.write_text(
        json.dumps(
            {
                "policy_id": "policy-1",
                "benchmark_attestation_id": "benchmark-attestation-1",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH", str(lifecycle_path))
    monkeypatch.setenv(
        "ANTISPOOF_CALIBRATION_ACTIVE_METADATA_PATH",
        str(active_policy_metadata_path),
    )

    summary = get_antispoof_public_calibration_summary().to_dict()
    serialized = str(summary)

    assert summary["active_policy_id"] == "policy-1"
    assert summary["benchmark_attestation_id"] == "benchmark-attestation-1"

    assert "private_payload" not in serialized
    assert "calibration_parameters" not in serialized
    assert "signature" not in serialized
    assert "payload_hash" not in serialized
    assert "threshold" not in serialized
    assert "weight" not in serialized
    assert "margin" not in serialized
