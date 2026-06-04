import json
from pathlib import Path

from antispoof.domain.calibration.attestation import CalibrationAttestation
from antispoof.infrastructure.calibration.file_attestation_writer import (
    FileCalibrationAttestationWriter,
)


def test_file_attestation_writer_writes_json_document(tmp_path: Path) -> None:
    path = tmp_path / "attestations" / "activation.json"
    writer = FileCalibrationAttestationWriter(path)

    writer.write(
        CalibrationAttestation(
            attestation_type="activation",
            policy_id="policy-1",
            service="antispoof",
            contract_version="2.6",
            model_identifier="credona.antispoof.minifasnet-v2.v1",
            created_at="2026-06-04T00:00:00+00:00",
        )
    )

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["attestation_type"] == "activation"
    assert payload["policy_id"] == "policy-1"
    assert "private_payload" not in str(payload)
    assert "calibration_parameters" not in str(payload)
