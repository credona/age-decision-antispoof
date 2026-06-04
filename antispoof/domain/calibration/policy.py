from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from antispoof.domain.calibration.errors import CalibrationCompatibilityError


@dataclass(frozen=True)
class CalibrationPolicyMetadata:
    policy_id: str
    service: str
    contract_version: str
    policy_version: str
    benchmark_attestation_id: str
    model_identifier: str
    payload_hash: str
    signature: str


@dataclass(frozen=True)
class RuntimeCalibrationPolicy:
    metadata: CalibrationPolicyMetadata
    private_payload: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "private_payload",
            MappingProxyType(dict(self.private_payload)),
        )

    def assert_compatible(
        self,
        *,
        expected_service: str,
        expected_contract_version: str,
        expected_model_identifier: str,
    ) -> None:
        if self.metadata.service != expected_service:
            raise CalibrationCompatibilityError("CALIBRATION_WRONG_SERVICE")

        if self.metadata.contract_version != expected_contract_version:
            raise CalibrationCompatibilityError("CALIBRATION_WRONG_CONTRACT_VERSION")

        if self.metadata.model_identifier != expected_model_identifier:
            raise CalibrationCompatibilityError("CALIBRATION_WRONG_MODEL_IDENTIFIER")
