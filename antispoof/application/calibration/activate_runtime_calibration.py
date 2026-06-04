from datetime import UTC, datetime

from antispoof.domain.calibration import RuntimeCalibrationPolicy
from antispoof.domain.calibration.attestation import CalibrationAttestation
from antispoof.domain.calibration.lifecycle import CalibrationLifecycleState
from antispoof.domain.calibration.provenance import CalibrationProvenanceRecord


class ActivateRuntimeCalibrationUseCase:
    def __init__(
        self,
        *,
        lifecycle_store,
        provenance_store,
        attestation_writer,
    ) -> None:
        self.lifecycle_store = lifecycle_store
        self.provenance_store = provenance_store
        self.attestation_writer = attestation_writer

    def execute(self, *, policy: RuntimeCalibrationPolicy) -> CalibrationLifecycleState:
        current_state = self.lifecycle_store.load()
        created_at = datetime.now(UTC).isoformat()

        next_state = CalibrationLifecycleState(
            active_policy_id=policy.metadata.policy_id,
            previous_policy_id=current_state.active_policy_id,
            activated_at=created_at,
        )

        self.lifecycle_store.save(next_state)

        self.provenance_store.append(
            CalibrationProvenanceRecord(
                event="activated",
                policy_id=policy.metadata.policy_id,
                previous_policy_id=current_state.active_policy_id,
                service=policy.metadata.service,
                contract_version=policy.metadata.contract_version,
                model_identifier=policy.metadata.model_identifier,
                created_at=created_at,
            )
        )

        self.attestation_writer.write(
            CalibrationAttestation(
                attestation_type="activation",
                policy_id=policy.metadata.policy_id,
                service=policy.metadata.service,
                contract_version=policy.metadata.contract_version,
                model_identifier=policy.metadata.model_identifier,
                created_at=created_at,
            )
        )

        return next_state
