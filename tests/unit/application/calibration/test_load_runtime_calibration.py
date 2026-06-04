import base64
import hashlib
import json

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from antispoof.application.calibration.load_runtime_calibration import (
    LoadRuntimeCalibrationUseCase,
)
from antispoof.domain.calibration import (
    CalibrationActivationError,
    CalibrationIntegrityError,
    CalibrationSignatureError,
)
from antispoof.infrastructure.calibration.ed25519_signature_verifier import (
    Ed25519CalibrationSignatureVerifier,
)
from antispoof.infrastructure.calibration.sha256_integrity_verifier import (
    Sha256CalibrationIntegrityVerifier,
)


class MemoryPolicyReader:
    def __init__(self, payload: bytes):
        self.payload = payload

    def read_policy_bytes(self) -> bytes:
        return self.payload


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def signed_policy_document(
    *,
    service: str = "antispoof",
    contract_version: str = "2.6",
    model_identifier: str = "credona.antispoof.minifasnet-v2.v1",
    private_payload: dict | None = None,
) -> tuple[bytes, str]:
    payload = private_payload or {
        "calibration_parameters": {
            "final_score_offset": 0.0,
            "final_score_floor": 0.0,
        }
    }

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    payload_bytes = canonical_payload(payload)
    signature = base64.b64encode(private_key.sign(payload_bytes)).decode("ascii")
    public_key_b64 = base64.b64encode(public_key.public_bytes_raw()).decode("ascii")

    document = {
        "metadata": {
            "policy_id": "antispoof-runtime-policy-test",
            "service": service,
            "contract_version": contract_version,
            "policy_version": "1.0.0",
            "benchmark_attestation_id": "benchmark-attestation-test",
            "model_identifier": model_identifier,
            "payload_hash": f"sha256:{hashlib.sha256(payload_bytes).hexdigest()}",
            "signature": signature,
        },
        "private_payload": payload,
    }

    return json.dumps(document).encode("utf-8"), public_key_b64


def build_use_case(document: bytes, public_key_b64: str) -> LoadRuntimeCalibrationUseCase:
    return LoadRuntimeCalibrationUseCase(
        reader=MemoryPolicyReader(document),
        integrity_verifier=Sha256CalibrationIntegrityVerifier(),
        signature_verifier=Ed25519CalibrationSignatureVerifier(public_key_b64),
    )


def test_load_runtime_calibration_accepts_valid_signed_policy() -> None:
    document, public_key_b64 = signed_policy_document()
    use_case = build_use_case(document, public_key_b64)

    policy = use_case.execute(
        expected_service="antispoof",
        expected_contract_version="2.6",
        expected_model_identifier="credona.antispoof.minifasnet-v2.v1",
    )

    assert policy.metadata.policy_id == "antispoof-runtime-policy-test"
    assert policy.metadata.service == "antispoof"


def test_load_runtime_calibration_rejects_invalid_json() -> None:
    use_case = build_use_case(b"{invalid-json", "unused")

    with pytest.raises(CalibrationActivationError, match="CALIBRATION_INVALID_JSON"):
        use_case.execute(
            expected_service="antispoof",
            expected_contract_version="2.6",
            expected_model_identifier="credona.antispoof.minifasnet-v2.v1",
        )


def test_load_runtime_calibration_rejects_wrong_hash() -> None:
    document, public_key_b64 = signed_policy_document()
    parsed = json.loads(document.decode("utf-8"))
    parsed["metadata"]["payload_hash"] = "sha256:invalid"

    use_case = build_use_case(json.dumps(parsed).encode("utf-8"), public_key_b64)

    with pytest.raises(CalibrationIntegrityError, match="CALIBRATION_HASH_INVALID"):
        use_case.execute(
            expected_service="antispoof",
            expected_contract_version="2.6",
            expected_model_identifier="credona.antispoof.minifasnet-v2.v1",
        )


def test_load_runtime_calibration_rejects_wrong_signature() -> None:
    document, public_key_b64 = signed_policy_document()
    parsed = json.loads(document.decode("utf-8"))
    parsed["metadata"]["signature"] = base64.b64encode(b"invalid-signature").decode("ascii")

    use_case = build_use_case(json.dumps(parsed).encode("utf-8"), public_key_b64)

    with pytest.raises(CalibrationSignatureError, match="CALIBRATION_SIGNATURE_INVALID"):
        use_case.execute(
            expected_service="antispoof",
            expected_contract_version="2.6",
            expected_model_identifier="credona.antispoof.minifasnet-v2.v1",
        )


def test_load_runtime_calibration_rejects_wrong_service() -> None:
    document, public_key_b64 = signed_policy_document(service="core")
    use_case = build_use_case(document, public_key_b64)

    with pytest.raises(Exception, match="CALIBRATION_WRONG_SERVICE"):
        use_case.execute(
            expected_service="antispoof",
            expected_contract_version="2.6",
            expected_model_identifier="credona.antispoof.minifasnet-v2.v1",
        )
