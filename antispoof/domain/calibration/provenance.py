from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CalibrationProvenanceRecord:
    event: str
    policy_id: str
    previous_policy_id: str | None
    service: str
    contract_version: str
    model_identifier: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "event": self.event,
            "policy_id": self.policy_id,
            "previous_policy_id": self.previous_policy_id,
            "service": self.service,
            "contract_version": self.contract_version,
            "model_identifier": self.model_identifier,
            "created_at": self.created_at,
        }
