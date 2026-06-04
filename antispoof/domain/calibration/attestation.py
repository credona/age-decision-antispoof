from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CalibrationAttestation:
    attestation_type: str
    policy_id: str
    service: str
    contract_version: str
    model_identifier: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "attestation_type": self.attestation_type,
            "policy_id": self.policy_id,
            "service": self.service,
            "contract_version": self.contract_version,
            "model_identifier": self.model_identifier,
            "created_at": self.created_at,
        }
