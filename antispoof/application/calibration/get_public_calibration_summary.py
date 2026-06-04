from antispoof.domain.calibration.public_summary import PublicCalibrationSummary


class GetPublicCalibrationSummaryUseCase:
    def __init__(
        self,
        *,
        lifecycle_store,
        active_policy_store,
        service: str,
        contract_version: str,
        model_identifier: str,
    ) -> None:
        self.lifecycle_store = lifecycle_store
        self.active_policy_store = active_policy_store
        self.service = service
        self.contract_version = contract_version
        self.model_identifier = model_identifier

    def execute(self) -> PublicCalibrationSummary:
        state = self.lifecycle_store.load()
        active_policy = self.active_policy_store.load_active_policy()

        benchmark_attestation_id = None

        if active_policy is not None:
            benchmark_attestation_id = active_policy.metadata.benchmark_attestation_id

        return PublicCalibrationSummary(
            active_policy_id=state.active_policy_id,
            service=self.service,
            contract_version=self.contract_version,
            model_identifier=self.model_identifier,
            benchmark_attestation_id=benchmark_attestation_id,
        )
