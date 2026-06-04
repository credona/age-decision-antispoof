import pytest
from antispoof.application.calibration.rollback_runtime_calibration import (
    RollbackRuntimeCalibrationUseCase,
)

from antispoof.domain.calibration.lifecycle import CalibrationLifecycleState


class MemoryLifecycleStore:
    def __init__(self, state: CalibrationLifecycleState) -> None:
        self.state = state
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


def test_rollback_runtime_calibration_restores_previous_policy() -> None:
    lifecycle_store = MemoryLifecycleStore(
        CalibrationLifecycleState(
            active_policy_id="policy-2",
            previous_policy_id="policy-1",
            activated_at="2026-06-04T00:00:00+00:00",
        )
    )
    provenance_store = MemoryProvenanceStore()
    attestation_writer = MemoryAttestationWriter()

    use_case = RollbackRuntimeCalibrationUseCase(
        lifecycle_store=lifecycle_store,
        provenance_store=provenance_store,
        attestation_writer=attestation_writer,
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
    )

    state = use_case.execute()

    assert state.active_policy_id == "policy-1"
    assert state.previous_policy_id == "policy-2"
    assert lifecycle_store.saved_state == state
    assert provenance_store.records[0].event == "rollback"
    assert attestation_writer.attestations[0].attestation_type == "rollback"


def test_rollback_runtime_calibration_rejects_missing_previous_policy() -> None:
    lifecycle_store = MemoryLifecycleStore(CalibrationLifecycleState.empty())

    use_case = RollbackRuntimeCalibrationUseCase(
        lifecycle_store=lifecycle_store,
        provenance_store=MemoryProvenanceStore(),
        attestation_writer=MemoryAttestationWriter(),
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
    )

    with pytest.raises(ValueError, match="CALIBRATION_ROLLBACK_UNAVAILABLE"):
        use_case.execute()
