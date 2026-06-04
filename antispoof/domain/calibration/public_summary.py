from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PublicCalibrationSummary:
    active_policy_id: str | None
    service: str
    contract_version: str
    model_identifier: str
    benchmark_attestation_id: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "active_policy_id": self.active_policy_id,
            "service": self.service,
            "contract_version": self.contract_version,
            "model_identifier": self.model_identifier,
            "benchmark_attestation_id": self.benchmark_attestation_id,
        }
