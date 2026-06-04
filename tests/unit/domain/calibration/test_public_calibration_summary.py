from antispoof.domain.calibration.public_summary import PublicCalibrationSummary


def test_public_summary_exposes_no_private_calibration_payload() -> None:
    summary = PublicCalibrationSummary(
        active_policy_id="policy-1",
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
        benchmark_attestation_id="benchmark-attestation-1",
    )

    payload = summary.to_dict()
    serialized = str(payload)

    assert payload["active_policy_id"] == "policy-1"
    assert payload["service"] == "antispoof"

    assert "private_payload" not in serialized
    assert "calibration_parameters" not in serialized
    assert "signature" not in serialized
    assert "payload_hash" not in serialized
    assert "threshold" not in serialized
    assert "weight" not in serialized
    assert "margin" not in serialized
