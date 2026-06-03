import os

from antispoof.application.calibration.load_runtime_calibration import (
    LoadRuntimeCalibrationUseCase,
)
from antispoof.domain.calibration import RuntimeCalibrationPolicy
from antispoof.infrastructure.calibration.ed25519_signature_verifier import (
    Ed25519CalibrationSignatureVerifier,
)
from antispoof.infrastructure.calibration.file_policy_reader import FileCalibrationPolicyReader
from antispoof.infrastructure.calibration.sha256_integrity_verifier import (
    Sha256CalibrationIntegrityVerifier,
)
from antispoof.infrastructure.models.registry import DEFAULT_ANTISPOOF_MODEL_ID
from antispoof.project import project_metadata


def _env_bool(name: str, default: bool = False) -> bool:
    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def load_antispoof_runtime_calibration() -> RuntimeCalibrationPolicy | None:
    calibration_required = _env_bool("ANTISPOOF_CALIBRATION_REQUIRED", False)
    calibration_policy_path = os.getenv("ANTISPOOF_CALIBRATION_POLICY_PATH")
    calibration_public_key_b64 = os.getenv("ANTISPOOF_CALIBRATION_PUBLIC_KEY_B64")

    if not calibration_required and not calibration_policy_path:
        return None

    use_case = LoadRuntimeCalibrationUseCase(
        reader=FileCalibrationPolicyReader(calibration_policy_path),
        integrity_verifier=Sha256CalibrationIntegrityVerifier(),
        signature_verifier=Ed25519CalibrationSignatureVerifier(calibration_public_key_b64),
    )

    return use_case.execute(
        expected_service="antispoof",
        expected_contract_version=project_metadata.contract_version,
        expected_model_identifier=DEFAULT_ANTISPOOF_MODEL_ID,
    )
