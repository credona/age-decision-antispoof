import pytest

from antispoof.domain.calibration.trusted_registry import TrustedCalibrationRegistry


def test_trusted_registry_accepts_trusted_policy() -> None:
    registry = TrustedCalibrationRegistry(
        trusted_policy_ids=("policy-1",),
        revoked_policy_ids=(),
    )

    registry.assert_policy_trusted("policy-1")


def test_trusted_registry_rejects_unknown_policy() -> None:
    registry = TrustedCalibrationRegistry(
        trusted_policy_ids=("policy-1",),
        revoked_policy_ids=(),
    )

    with pytest.raises(ValueError, match="CALIBRATION_POLICY_NOT_TRUSTED"):
        registry.assert_policy_trusted("policy-2")


def test_trusted_registry_rejects_revoked_policy() -> None:
    registry = TrustedCalibrationRegistry(
        trusted_policy_ids=("policy-1",),
        revoked_policy_ids=("policy-1",),
    )

    with pytest.raises(ValueError, match="CALIBRATION_POLICY_REVOKED"):
        registry.assert_policy_trusted("policy-1")
