import base64
import hashlib
import json
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from antispoof.infrastructure.calibration.runtime_activation import (
    load_antispoof_runtime_calibration,
)
from antispoof.infrastructure.models.registry import DEFAULT_ANTISPOOF_MODEL_ID
from antispoof.project import project_metadata


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write_signed_policy(path: Path, policy_id: str) -> str:
    payload = {
        "calibration_parameters": {
            "final_score_offset": 0.05,
            "cred_antispoof_score_offset": 0.05,
        }
    }

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    payload_bytes = canonical_payload(payload)

    document = {
        "metadata": {
            "policy_id": policy_id,
            "service": "antispoof",
            "contract_version": project_metadata.contract_version,
            "policy_version": "1.0.0",
            "benchmark_attestation_id": "benchmark-attestation-test",
            "model_identifier": DEFAULT_ANTISPOOF_MODEL_ID,
            "payload_hash": f"sha256:{hashlib.sha256(payload_bytes).hexdigest()}",
            "signature": base64.b64encode(private_key.sign(payload_bytes)).decode("ascii"),
        },
        "private_payload": payload,
    }

    path.write_text(json.dumps(document), encoding="utf-8")
    return base64.b64encode(public_key.public_bytes_raw()).decode("ascii")


def test_runtime_activation_validates_manifest_registry_and_persists_lifecycle(
    tmp_path: Path,
    monkeypatch,
) -> None:
    policy_path = tmp_path / "policy.private.json"
    public_key_b64 = write_signed_policy(policy_path, "policy-1")

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "service": "antispoof",
                "contract_version": project_metadata.contract_version,
                "model_identifier": DEFAULT_ANTISPOOF_MODEL_ID,
                "allowed_policy_ids": ["policy-1"],
                "revoked_policy_ids": [],
            }
        ),
        encoding="utf-8",
    )

    registry_path = tmp_path / "trusted-registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "trusted_policy_ids": ["policy-1"],
                "revoked_policy_ids": [],
            }
        ),
        encoding="utf-8",
    )

    lifecycle_path = tmp_path / "runtime" / "lifecycle.json"
    provenance_path = tmp_path / "runtime" / "provenance.jsonl"
    attestation_path = tmp_path / "runtime" / "activation-attestation.json"

    monkeypatch.setenv("ANTISPOOF_CALIBRATION_REQUIRED", "true")
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_POLICY_PATH", str(policy_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_PUBLIC_KEY_B64", public_key_b64)
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_MANIFEST_PATH", str(manifest_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_TRUSTED_REGISTRY_PATH", str(registry_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_LIFECYCLE_STATE_PATH", str(lifecycle_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_PROVENANCE_PATH", str(provenance_path))
    monkeypatch.setenv(
        "ANTISPOOF_CALIBRATION_ACTIVATION_ATTESTATION_PATH",
        str(attestation_path),
    )

    policy = load_antispoof_runtime_calibration()

    assert policy is not None
    assert policy.metadata.policy_id == "policy-1"

    lifecycle = json.loads(lifecycle_path.read_text(encoding="utf-8"))
    assert lifecycle["active_policy_id"] == "policy-1"
    assert lifecycle["previous_policy_id"] is None

    provenance_lines = provenance_path.read_text(encoding="utf-8").splitlines()
    assert len(provenance_lines) == 1
    assert json.loads(provenance_lines[0])["event"] == "activated"

    attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
    assert attestation["attestation_type"] == "activation"
    assert attestation["policy_id"] == "policy-1"


def test_runtime_activation_rejects_policy_missing_from_manifest(
    tmp_path: Path,
    monkeypatch,
) -> None:
    policy_path = tmp_path / "policy.private.json"
    public_key_b64 = write_signed_policy(policy_path, "policy-2")

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "service": "antispoof",
                "contract_version": project_metadata.contract_version,
                "model_identifier": DEFAULT_ANTISPOOF_MODEL_ID,
                "allowed_policy_ids": ["policy-1"],
                "revoked_policy_ids": [],
            }
        ),
        encoding="utf-8",
    )

    registry_path = tmp_path / "trusted-registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "trusted_policy_ids": ["policy-2"],
                "revoked_policy_ids": [],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("ANTISPOOF_CALIBRATION_REQUIRED", "true")
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_POLICY_PATH", str(policy_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_PUBLIC_KEY_B64", public_key_b64)
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_MANIFEST_PATH", str(manifest_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_TRUSTED_REGISTRY_PATH", str(registry_path))

    try:
        load_antispoof_runtime_calibration()
    except ValueError as exc:
        assert str(exc) == "CALIBRATION_POLICY_NOT_IN_MANIFEST"
    else:
        raise AssertionError("Expected manifest rejection.")


def test_runtime_activation_rejects_untrusted_policy(tmp_path: Path, monkeypatch) -> None:
    policy_path = tmp_path / "policy.private.json"
    public_key_b64 = write_signed_policy(policy_path, "policy-1")

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "service": "antispoof",
                "contract_version": project_metadata.contract_version,
                "model_identifier": DEFAULT_ANTISPOOF_MODEL_ID,
                "allowed_policy_ids": ["policy-1"],
                "revoked_policy_ids": [],
            }
        ),
        encoding="utf-8",
    )

    registry_path = tmp_path / "trusted-registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "trusted_policy_ids": [],
                "revoked_policy_ids": [],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("ANTISPOOF_CALIBRATION_REQUIRED", "true")
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_POLICY_PATH", str(policy_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_PUBLIC_KEY_B64", public_key_b64)
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_MANIFEST_PATH", str(manifest_path))
    monkeypatch.setenv("ANTISPOOF_CALIBRATION_TRUSTED_REGISTRY_PATH", str(registry_path))

    try:
        load_antispoof_runtime_calibration()
    except ValueError as exc:
        assert str(exc) == "CALIBRATION_POLICY_NOT_TRUSTED"
    else:
        raise AssertionError("Expected trusted registry rejection.")
