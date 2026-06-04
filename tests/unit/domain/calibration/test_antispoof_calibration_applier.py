from antispoof.domain.calibration import (
    AntispoofCalibrationApplier,
    CalibrationPolicyMetadata,
    RuntimeCalibrationPolicy,
)


def make_policy(private_payload: dict) -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id="antispoof-policy-test",
            service="antispoof",
            contract_version="2.6",
            policy_version="1.0.0",
            benchmark_attestation_id="attestation-test",
            model_identifier="credona.antispoof.minifasnet-v2.v1",
            payload_hash="sha256:test",
            signature="signature-test",
        ),
        private_payload=private_payload,
    )


def test_antispoof_calibration_applier_is_neutral_without_policy() -> None:
    applier = AntispoofCalibrationApplier()

    result = applier.apply(
        final_score=0.8,
        cred_antispoof_score=0.7,
    )

    assert result.final_score == 0.8
    assert result.cred_antispoof_score == 0.7


def test_antispoof_calibration_applier_applies_private_offsets() -> None:
    policy = make_policy(
        {
            "calibration_parameters": {
                "final_score_offset": 0.05,
                "cred_antispoof_score_offset": 0.1,
            }
        }
    )

    applier = AntispoofCalibrationApplier(policy)

    result = applier.apply(
        final_score=0.8,
        cred_antispoof_score=0.7,
    )

    assert result.final_score == 0.85
    assert result.cred_antispoof_score == 0.8


def test_antispoof_calibration_applier_clamps_scores() -> None:
    policy = make_policy(
        {
            "calibration_parameters": {
                "final_score_offset": 2.0,
                "cred_antispoof_score_offset": 2.0,
            }
        }
    )

    applier = AntispoofCalibrationApplier(policy)

    result = applier.apply(
        final_score=0.8,
        cred_antispoof_score=0.7,
    )

    assert result.final_score == 1.0
    assert result.cred_antispoof_score == 1.0


def test_antispoof_calibration_applier_applies_floor_and_ceiling() -> None:
    policy = make_policy(
        {
            "calibration_parameters": {
                "final_score_floor": 0.6,
                "final_score_ceiling": 0.9,
                "cred_antispoof_score_floor": 0.5,
                "cred_antispoof_score_ceiling": 0.85,
            }
        }
    )

    applier = AntispoofCalibrationApplier(policy)

    low = applier.apply(final_score=0.2, cred_antispoof_score=0.2)
    high = applier.apply(final_score=0.95, cred_antispoof_score=0.95)

    assert low.final_score == 0.6
    assert low.cred_antispoof_score == 0.5
    assert high.final_score == 0.9
    assert high.cred_antispoof_score == 0.85


def test_antispoof_calibration_applier_does_not_expose_policy_payload() -> None:
    policy = make_policy(
        {
            "calibration_parameters": {
                "final_score_offset": 0.05,
                "private_weight": 0.4,
                "private_margin": 2.0,
            }
        }
    )

    applier = AntispoofCalibrationApplier(policy)

    result = applier.apply(
        final_score=0.8,
        cred_antispoof_score=0.7,
    )

    assert not hasattr(result, "private_payload")
    assert not hasattr(result, "calibration_parameters")
    assert not hasattr(result, "private_weight")
    assert not hasattr(result, "private_margin")
