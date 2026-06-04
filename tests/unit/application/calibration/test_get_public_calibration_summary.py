from antispoof.application.calibration.get_public_calibration_summary import (
    GetPublicCalibrationSummaryUseCase,
)
from antispoof.domain.calibration import CalibrationPolicyMetadata, RuntimeCalibrationPolicy
from antispoof.domain.calibration.lifecycle import CalibrationLifecycleState


class MemoryLifecycleStore:
    def __init__(self, state: CalibrationLifecycleState) -> None:
        self.state = state

    def load(self) -> CalibrationLifecycleState:
        return self.state


class MemoryActivePolicyStore:
    def __init__(self, policy: RuntimeCalibrationPolicy | None) -> None:
        self.policy = policy

    def load_active_policy(self) -> RuntimeCalibrationPolicy | None:
        return self.policy


def make_policy() -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id="policy-1",
            service="antispoof",
            contract_version="2.6",
            policy_version="1.0.0",
            benchmark_attestation_id="benchmark-attestation-1",
            model_identifier="credona.antispoof.minifasnet-v2.v1",
            payload_hash="sha256:test",
            signature="signature-test",
        ),
        private_payload={"calibration_parameters": {"final_score_offset": 0.1}},
    )


def test_get_public_calibration_summary_uses_active_policy_metadata() -> None:
    use_case = GetPublicCalibrationSummaryUseCase(
        lifecycle_store=MemoryLifecycleStore(
            CalibrationLifecycleState(
                active_policy_id="policy-1",
                previous_policy_id="policy-0",
                activated_at="2026-06-04T00:00:00+00:00",
            )
        ),
        active_policy_store=MemoryActivePolicyStore(make_policy()),
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
    )

    payload = use_case.execute().to_dict()
    serialized = str(payload)

    assert payload["active_policy_id"] == "policy-1"
    assert payload["benchmark_attestation_id"] == "benchmark-attestation-1"

    assert "private_payload" not in serialized
    assert "calibration_parameters" not in serialized
    assert "signature" not in serialized
    assert "payload_hash" not in serialized


def test_get_public_calibration_summary_handles_no_active_policy() -> None:
    use_case = GetPublicCalibrationSummaryUseCase(
        lifecycle_store=MemoryLifecycleStore(CalibrationLifecycleState.empty()),
        active_policy_store=MemoryActivePolicyStore(None),
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
    )

    payload = use_case.execute().to_dict()

    assert payload["active_policy_id"] is None
    assert payload["benchmark_attestation_id"] is None
