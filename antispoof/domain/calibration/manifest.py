from dataclasses import dataclass


@dataclass(frozen=True)
class CalibrationDistributionManifest:
    service: str
    contract_version: str
    model_identifier: str
    allowed_policy_ids: tuple[str, ...]
    revoked_policy_ids: tuple[str, ...]

    def assert_policy_allowed(
        self,
        *,
        service: str,
        contract_version: str,
        model_identifier: str,
        policy_id: str,
    ) -> None:
        if service != self.service:
            raise ValueError("CALIBRATION_MANIFEST_WRONG_SERVICE")

        if contract_version != self.contract_version:
            raise ValueError("CALIBRATION_MANIFEST_WRONG_CONTRACT_VERSION")

        if model_identifier != self.model_identifier:
            raise ValueError("CALIBRATION_MANIFEST_WRONG_MODEL_IDENTIFIER")

        if policy_id in self.revoked_policy_ids:
            raise ValueError("CALIBRATION_POLICY_REVOKED")

        if policy_id not in self.allowed_policy_ids:
            raise ValueError("CALIBRATION_POLICY_NOT_IN_MANIFEST")
