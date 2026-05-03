import pytest

from antispoof.domain.scoring.policy import (
    AntispoofScoringPolicy,
    default_antispoof_scoring_policy,
)


def test_default_antispoof_scoring_policy_is_valid_and_versioned():
    policy = default_antispoof_scoring_policy()

    assert policy.policy_id == "credona.antispoof.fusion-threshold.v1"
    assert policy.threshold == 0.5
    assert policy.model_weight == 0.7
    assert policy.texture_weight == 0.15
    assert policy.screen_weight == 0.15
    assert policy.calibration_method == "clamp_v1"


def test_antispoof_scoring_policy_rejects_invalid_threshold():
    policy = AntispoofScoringPolicy(
        policy_id="credona.antispoof.invalid.v1",
        threshold=1.2,
        model_weight=0.7,
        texture_weight=0.15,
        screen_weight=0.15,
        calibration_method="clamp_v1",
    )

    with pytest.raises(ValueError, match="threshold"):
        policy.validate()


def test_antispoof_scoring_policy_rejects_invalid_weights():
    policy = AntispoofScoringPolicy(
        policy_id="credona.antispoof.invalid.v1",
        threshold=0.5,
        model_weight=0.8,
        texture_weight=0.2,
        screen_weight=0.2,
        calibration_method="clamp_v1",
    )

    with pytest.raises(ValueError, match="weights"):
        policy.validate()
