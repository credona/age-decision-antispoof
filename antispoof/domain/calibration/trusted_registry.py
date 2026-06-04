from dataclasses import dataclass


@dataclass(frozen=True)
class TrustedCalibrationRegistry:
    trusted_policy_ids: tuple[str, ...]
    revoked_policy_ids: tuple[str, ...]

    def assert_policy_trusted(self, policy_id: str) -> None:
        if policy_id in self.revoked_policy_ids:
            raise ValueError("CALIBRATION_POLICY_REVOKED")

        if policy_id not in self.trusted_policy_ids:
            raise ValueError("CALIBRATION_POLICY_NOT_TRUSTED")
