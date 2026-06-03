import hashlib
from pathlib import Path

import pytest

from antispoof.domain.calibration import CalibrationActivationError
from antispoof.infrastructure.calibration.file_policy_reader import FileCalibrationPolicyReader
from antispoof.infrastructure.calibration.sha256_integrity_verifier import (
    Sha256CalibrationIntegrityVerifier,
)


def test_file_policy_reader_reads_runtime_policy_file(tmp_path: Path) -> None:
    policy_file = tmp_path / "antispoof-policy.private.json"
    policy_file.write_bytes(b'{"metadata":{}}')

    reader = FileCalibrationPolicyReader(str(policy_file))

    assert reader.read_policy_bytes() == b'{"metadata":{}}'


def test_file_policy_reader_rejects_missing_path() -> None:
    reader = FileCalibrationPolicyReader(None)

    with pytest.raises(CalibrationActivationError, match="CALIBRATION_POLICY_PATH_MISSING"):
        reader.read_policy_bytes()


def test_file_policy_reader_rejects_missing_file(tmp_path: Path) -> None:
    reader = FileCalibrationPolicyReader(str(tmp_path / "missing.private.json"))

    with pytest.raises(CalibrationActivationError, match="CALIBRATION_POLICY_FILE_MISSING"):
        reader.read_policy_bytes()


def test_sha256_integrity_verifier_accepts_matching_hash() -> None:
    payload = b'{"private":true}'
    expected_hash = f"sha256:{hashlib.sha256(payload).hexdigest()}"

    verifier = Sha256CalibrationIntegrityVerifier()

    assert verifier.verify(payload=payload, expected_hash=expected_hash) is True


def test_sha256_integrity_verifier_rejects_wrong_hash() -> None:
    verifier = Sha256CalibrationIntegrityVerifier()

    assert verifier.verify(payload=b"payload", expected_hash="sha256:invalid") is False
