import os

from antispoof.application.calibration.activate_runtime_calibration import (
    ActivateRuntimeCalibrationUseCase,
)
from antispoof.application.calibration.get_public_calibration_summary import (
    GetPublicCalibrationSummaryUseCase,
)
from antispoof.application.calibration.load_runtime_calibration import (
    LoadRuntimeCalibrationUseCase,
)
from antispoof.domain.calibration import RuntimeCalibrationPolicy
from antispoof.infrastructure.calibration.ed25519_signature_verifier import (
    Ed25519CalibrationSignatureVerifier,
)
from antispoof.infrastructure.calibration.file_active_policy_metadata_store import (
    FileActivePolicyMetadataStore,
)
from antispoof.infrastructure.calibration.file_attestation_writer import (
    FileCalibrationAttestationWriter,
)
from antispoof.infrastructure.calibration.file_lifecycle_store import (
    FileCalibrationLifecycleStore,
)
from antispoof.infrastructure.calibration.file_manifest_reader import (
    FileCalibrationManifestReader,
)
from antispoof.infrastructure.calibration.file_policy_reader import FileCalibrationPolicyReader
from antispoof.infrastructure.calibration.file_provenance_store import (
    FileCalibrationProvenanceStore,
)
from antispoof.infrastructure.calibration.file_trusted_registry_reader import (
    FileTrustedCalibrationRegistryReader,
)
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


def _env_required(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"{name}_MISSING")

    return value


def load_antispoof_runtime_calibration() -> RuntimeCalibrationPolicy | None:
    calibration_required = _env_bool("ANTISPOOF_CALIBRATION_REQUIRED", False)
    calibration_policy_path = os.getenv("ANTISPOOF_CALIBRATION_POLICY_PATH")
    calibration_public_key_b64 = os.getenv("ANTISPOOF_CALIBRATION_PUBLIC_KEY_B64")

    if not calibration_required and not calibration_policy_path:
        return None

    load_use_case = LoadRuntimeCalibrationUseCase(
        reader=FileCalibrationPolicyReader(calibration_policy_path),
        integrity_verifier=Sha256CalibrationIntegrityVerifier(),
        signature_verifier=Ed25519CalibrationSignatureVerifier(calibration_public_key_b64),
    )

    policy = load_use_case.execute(
        expected_service="antispoof",
        expected_contract_version=project_metadata.contract_version,
        expected_model_identifier=DEFAULT_ANTISPOOF_MODEL_ID,
    )

    manifest_path = os.getenv("ANTISPOOF_CALIBRATION_MANIFEST_PATH")
    trusted_registry_path = os.getenv("ANTISPOOF_CALIBRATION_TRUSTED_REGISTRY_PATH")

    if manifest_path:
        manifest = FileCalibrationManifestReader(manifest_path).read()
        manifest.assert_policy_allowed(
            service=policy.metadata.service,
            contract_version=policy.metadata.contract_version,
            model_identifier=policy.metadata.model_identifier,
            policy_id=policy.metadata.policy_id,
        )

    if trusted_registry_path:
        trusted_registry = FileTrustedCalibrationRegistryReader(trusted_registry_path).read()
        trusted_registry.assert_policy_trusted(policy.metadata.policy_id)

    lifecycle_path = os.getenv("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH")
    provenance_path = os.getenv("ANTISPOOF_CALIBRATION_PROVENANCE_PATH")
    activation_attestation_path = os.getenv("ANTISPOOF_CALIBRATION_ACTIVATION_ATTESTATION_PATH")

    if lifecycle_path and provenance_path and activation_attestation_path:
        ActivateRuntimeCalibrationUseCase(
            lifecycle_store=FileCalibrationLifecycleStore(lifecycle_path),
            provenance_store=FileCalibrationProvenanceStore(provenance_path),
            attestation_writer=FileCalibrationAttestationWriter(activation_attestation_path),
        ).execute(policy=policy)

        active_metadata_path = os.getenv("ANTISPOOF_CALIBRATION_ACTIVE_METADATA_PATH")
        FileActivePolicyMetadataStore(active_metadata_path).save_from_policy(policy)

    return policy


def rollback_antispoof_runtime_calibration():
    lifecycle_path = _env_required("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH")
    provenance_path = _env_required("ANTISPOOF_CALIBRATION_PROVENANCE_PATH")
    rollback_attestation_path = _env_required("ANTISPOOF_CALIBRATION_ROLLBACK_ATTESTATION_PATH")

    from antispoof.application.calibration.rollback_runtime_calibration import (
        RollbackRuntimeCalibrationUseCase,
    )

    return RollbackRuntimeCalibrationUseCase(
        lifecycle_store=FileCalibrationLifecycleStore(lifecycle_path),
        provenance_store=FileCalibrationProvenanceStore(provenance_path),
        attestation_writer=FileCalibrationAttestationWriter(rollback_attestation_path),
        service="antispoof",
        contract_version=project_metadata.contract_version,
        model_identifier=DEFAULT_ANTISPOOF_MODEL_ID,
    ).execute()


def get_antispoof_public_calibration_summary():
    lifecycle_path = os.getenv("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH")
    active_metadata_path = os.getenv("ANTISPOOF_CALIBRATION_ACTIVE_METADATA_PATH")

    return GetPublicCalibrationSummaryUseCase(
        lifecycle_store=FileCalibrationLifecycleStore(lifecycle_path or ""),
        active_policy_store=FileActivePolicyMetadataStore(active_metadata_path),
        service="antispoof",
        contract_version=project_metadata.contract_version,
        model_identifier=DEFAULT_ANTISPOOF_MODEL_ID,
    ).execute()
