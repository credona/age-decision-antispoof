from antispoof.domain.calibration.provenance import CalibrationProvenanceRecord


def test_provenance_record_contains_public_safe_fields_only() -> None:
    record = CalibrationProvenanceRecord(
        event="activated",
        policy_id="policy-1",
        previous_policy_id=None,
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
        created_at="2026-06-04T00:00:00+00:00",
    )

    payload = record.to_dict()
    serialized = str(payload)

    assert payload["event"] == "activated"
    assert payload["policy_id"] == "policy-1"

    assert "private_payload" not in serialized
    assert "calibration_parameters" not in serialized
    assert "signature" not in serialized
    assert "payload_hash" not in serialized
    assert "threshold" not in serialized
    assert "weight" not in serialized
    assert "margin" not in serialized
