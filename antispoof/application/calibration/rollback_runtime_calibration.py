from datetime import UTC, datetime

from antispoof.domain.calibration.attestation import CalibrationAttestation
from antispoof.domain.calibration.lifecycle import CalibrationLifecycleState
from antispoof.domain.calibration.provenance import CalibrationProvenanceRecord


class RollbackRuntimeCalibrationUseCase:
    def __init__(
        self,
        *,
        lifecycle_store,
        provenance_store,
        attestation_writer,
        service: str,
        contract_version: str,
        model_identifier: str,
    ) -> None:
        self.lifecycle_store = lifecycle_store
        self.provenance_store = provenance_store
        self.attestation_writer = attestation_writer
        self.service = service
        self.contract_version = contract_version
        self.model_identifier = model_identifier

    def execute(self) -> CalibrationLifecycleState:
        current_state = self.lifecycle_store.load()

        if current_state.previous_policy_id is None:
            raise ValueError("CALIBRATION_ROLLBACK_UNAVAILABLE")

        created_at = datetime.now(UTC).isoformat()

        next_state = CalibrationLifecycleState(
            active_policy_id=current_state.previous_policy_id,
            previous_policy_id=current_state.active_policy_id,
            activated_at=created_at,
        )

        self.lifecycle_store.save(next_state)

        self.provenance_store.append(
            CalibrationProvenanceRecord(
                event="rollback",
                policy_id=next_state.active_policy_id,
                previous_policy_id=next_state.previous_policy_id,
                service=self.service,
                contract_version=self.contract_version,
                model_identifier=self.model_identifier,
                created_at=created_at,
            )
        )

        self.attestation_writer.write(
            CalibrationAttestation(
                attestation_type="rollback",
                policy_id=next_state.active_policy_id,
                service=self.service,
                contract_version=self.contract_version,
                model_identifier=self.model_identifier,
                created_at=created_at,
            )
        )

        return next_state
