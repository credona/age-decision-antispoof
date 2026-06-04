import pytest

from antispoof.domain.calibration.manifest import CalibrationDistributionManifest


def test_manifest_accepts_matching_policy_reference() -> None:
    manifest = CalibrationDistributionManifest(
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
        allowed_policy_ids=("policy-1",),
        revoked_policy_ids=(),
    )

    manifest.assert_policy_allowed(
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
        policy_id="policy-1",
    )


def test_manifest_rejects_wrong_service() -> None:
    manifest = CalibrationDistributionManifest(
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
        allowed_policy_ids=("policy-1",),
        revoked_policy_ids=(),
    )

    with pytest.raises(ValueError, match="CALIBRATION_MANIFEST_WRONG_SERVICE"):
        manifest.assert_policy_allowed(
            service="core",
            contract_version="2.6",
            model_identifier="credona.antispoof.minifasnet-v2.v1",
            policy_id="policy-1",
        )


def test_manifest_rejects_unknown_policy() -> None:
    manifest = CalibrationDistributionManifest(
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
        allowed_policy_ids=("policy-1",),
        revoked_policy_ids=(),
    )

    with pytest.raises(ValueError, match="CALIBRATION_POLICY_NOT_IN_MANIFEST"):
        manifest.assert_policy_allowed(
            service="antispoof",
            contract_version="2.6",
            model_identifier="credona.antispoof.minifasnet-v2.v1",
            policy_id="policy-2",
        )


def test_manifest_rejects_revoked_policy() -> None:
    manifest = CalibrationDistributionManifest(
        service="antispoof",
        contract_version="2.6",
        model_identifier="credona.antispoof.minifasnet-v2.v1",
        allowed_policy_ids=("policy-1",),
        revoked_policy_ids=("policy-1",),
    )

    with pytest.raises(ValueError, match="CALIBRATION_POLICY_REVOKED"):
        manifest.assert_policy_allowed(
            service="antispoof",
            contract_version="2.6",
            model_identifier="credona.antispoof.minifasnet-v2.v1",
            policy_id="policy-1",
        )
