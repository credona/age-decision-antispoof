import pytest

from antispoof.domain.calibration import (
    CalibrationCompatibilityError,
    CalibrationPolicyMetadata,
    RuntimeCalibrationPolicy,
)


def make_policy() -> RuntimeCalibrationPolicy:
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
        private_payload={"calibration_parameters": {"final_score_offset": 0.1}},
    )


def test_runtime_calibration_policy_accepts_compatible_metadata() -> None:
    policy = make_policy()

    policy.assert_compatible(
        expected_service="antispoof",
        expected_contract_version="2.6",
        expected_model_identifier="credona.antispoof.minifasnet-v2.v1",
    )


def test_runtime_calibration_policy_rejects_wrong_service() -> None:
    policy = make_policy()

    with pytest.raises(CalibrationCompatibilityError, match="CALIBRATION_WRONG_SERVICE"):
        policy.assert_compatible(
            expected_service="core",
            expected_contract_version="2.6",
            expected_model_identifier="credona.antispoof.minifasnet-v2.v1",
        )


def test_runtime_calibration_policy_rejects_wrong_contract_version() -> None:
    policy = make_policy()

    with pytest.raises(
        CalibrationCompatibilityError,
        match="CALIBRATION_WRONG_CONTRACT_VERSION",
    ):
        policy.assert_compatible(
            expected_service="antispoof",
            expected_contract_version="2.5",
            expected_model_identifier="credona.antispoof.minifasnet-v2.v1",
        )


def test_runtime_calibration_policy_rejects_wrong_model_identifier() -> None:
    policy = make_policy()

    with pytest.raises(
        CalibrationCompatibilityError,
        match="CALIBRATION_WRONG_MODEL_IDENTIFIER",
    ):
        policy.assert_compatible(
            expected_service="antispoof",
            expected_contract_version="2.6",
            expected_model_identifier="another-model",
        )


def test_runtime_calibration_private_payload_is_immutable() -> None:
    policy = make_policy()

    with pytest.raises(TypeError):
        policy.private_payload["calibration_parameters"] = {}
