import json
from typing import Any

from antispoof.application.calibration.ports import (
    CalibrationIntegrityVerifierPort,
    CalibrationPolicyReaderPort,
    CalibrationSignatureVerifierPort,
)
from antispoof.domain.calibration import (
    CalibrationActivationError,
    CalibrationIntegrityError,
    CalibrationPolicyMetadata,
    CalibrationSignatureError,
    RuntimeCalibrationPolicy,
)


class LoadRuntimeCalibrationUseCase:
    def __init__(
        self,
        reader: CalibrationPolicyReaderPort,
        integrity_verifier: CalibrationIntegrityVerifierPort,
        signature_verifier: CalibrationSignatureVerifierPort,
    ):
        self.reader = reader
        self.integrity_verifier = integrity_verifier
        self.signature_verifier = signature_verifier

    def execute(
        self,
        *,
        expected_service: str,
        expected_contract_version: str,
        expected_model_identifier: str,
    ) -> RuntimeCalibrationPolicy:
        raw_policy = self.reader.read_policy_bytes()

        try:
            document = json.loads(raw_policy.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CalibrationActivationError("CALIBRATION_INVALID_JSON") from exc

        metadata = self._build_metadata(document)
        private_payload = self._extract_private_payload(document)
        canonical_payload = self._canonical_private_payload(private_payload)

        if not self.integrity_verifier.verify(
            payload=canonical_payload,
            expected_hash=metadata.payload_hash,
        ):
            raise CalibrationIntegrityError("CALIBRATION_HASH_INVALID")

        if not self.signature_verifier.verify(
            payload=canonical_payload,
            signature=metadata.signature,
        ):
            raise CalibrationSignatureError("CALIBRATION_SIGNATURE_INVALID")

        policy = RuntimeCalibrationPolicy(
            metadata=metadata,
            private_payload=private_payload,
        )

        policy.assert_compatible(
            expected_service=expected_service,
            expected_contract_version=expected_contract_version,
            expected_model_identifier=expected_model_identifier,
        )

        return policy

    def _build_metadata(self, document: dict[str, Any]) -> CalibrationPolicyMetadata:
        try:
            metadata = document["metadata"]

            return CalibrationPolicyMetadata(
                policy_id=metadata["policy_id"],
                service=metadata["service"],
                contract_version=metadata["contract_version"],
                policy_version=metadata["policy_version"],
                benchmark_attestation_id=metadata["benchmark_attestation_id"],
                model_identifier=metadata["model_identifier"],
                payload_hash=metadata["payload_hash"],
                signature=metadata["signature"],
            )
        except KeyError as exc:
            raise CalibrationActivationError("CALIBRATION_METADATA_INVALID") from exc

    def _extract_private_payload(self, document: dict[str, Any]) -> dict[str, Any]:
        try:
            payload = document["private_payload"]
        except KeyError as exc:
            raise CalibrationActivationError("CALIBRATION_PAYLOAD_MISSING") from exc

        if not isinstance(payload, dict):
            raise CalibrationActivationError("CALIBRATION_PAYLOAD_INVALID")

        return payload

    def _canonical_private_payload(self, payload: dict[str, Any]) -> bytes:
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
