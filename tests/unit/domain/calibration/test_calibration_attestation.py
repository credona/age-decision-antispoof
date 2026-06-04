from antispoof.domain.calibration.attestation import CalibrationAttestation


def test_activation_attestation_is_public_safe() -> None:
    attestation = CalibrationAttestation(
        attestation_type="activation",
        policy_id="policy-1",
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
        created_at="2026-06-04T00:00:00+00:00",
    )

    payload = attestation.to_dict()
    serialized = str(payload)

    assert payload["attestation_type"] == "activation"
    assert payload["policy_id"] == "policy-1"

    assert "private_payload" not in serialized
    assert "calibration_parameters" not in serialized
    assert "signature" not in serialized
    assert "payload_hash" not in serialized
    assert "threshold" not in serialized
    assert "weight" not in serialized
    assert "margin" not in serialized
