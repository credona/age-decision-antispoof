from antispoof.application.calibration.activate_runtime_calibration import (
    ActivateRuntimeCalibrationUseCase,
)

from antispoof.domain.calibration import CalibrationPolicyMetadata, RuntimeCalibrationPolicy
from antispoof.domain.calibration.lifecycle import CalibrationLifecycleState


class MemoryLifecycleStore:
    def __init__(self) -> None:
        self.state = CalibrationLifecycleState.empty()
        self.saved_state = None

    def load(self) -> CalibrationLifecycleState:
        return self.state

    def save(self, state: CalibrationLifecycleState) -> None:
        self.saved_state = state
        self.state = state


class MemoryProvenanceStore:
    def __init__(self) -> None:
        self.records = []

    def append(self, record) -> None:
        self.records.append(record)


class MemoryAttestationWriter:
    def __init__(self) -> None:
        self.attestations = []

    def write(self, attestation) -> None:
        self.attestations.append(attestation)


def make_policy(policy_id: str = "policy-1") -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id=policy_id,
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


def test_activate_runtime_calibration_persists_active_and_previous_state() -> None:
    lifecycle_store = MemoryLifecycleStore()
    lifecycle_store.state = CalibrationLifecycleState(
        active_policy_id="policy-0",
        previous_policy_id=None,
        activated_at="2026-06-03T00:00:00+00:00",
    )
    provenance_store = MemoryProvenanceStore()
    attestation_writer = MemoryAttestationWriter()

    use_case = ActivateRuntimeCalibrationUseCase(
        lifecycle_store=lifecycle_store,
        provenance_store=provenance_store,
        attestation_writer=attestation_writer,
    )

    state = use_case.execute(policy=make_policy("policy-1"))

    assert state.active_policy_id == "policy-1"
    assert state.previous_policy_id == "policy-0"
    assert lifecycle_store.saved_state == state
    assert len(provenance_store.records) == 1
    assert provenance_store.records[0].event == "activated"
    assert len(attestation_writer.attestations) == 1
    assert attestation_writer.attestations[0].attestation_type == "activation"
