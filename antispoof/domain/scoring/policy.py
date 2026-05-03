from dataclasses import dataclass

DEFAULT_ANTISPOOF_SCORING_POLICY_ID = "credona.antispoof.fusion-threshold.v1"


@dataclass(frozen=True)
class AntispoofScoringPolicy:
    policy_id: str
    threshold: float
    model_weight: float
    texture_weight: float
    screen_weight: float
    calibration_method: str

    def validate(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id is required")

        if not 0.0 <= self.threshold <= 1.0:
            raise ValueError("threshold must be between 0.0 and 1.0")

        for name, value in {
            "model_weight": self.model_weight,
            "texture_weight": self.texture_weight,
            "screen_weight": self.screen_weight,
        }.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0.0 and 1.0")

        if abs((self.model_weight + self.texture_weight + self.screen_weight) - 1.0) >= 1e-6:
            raise ValueError("weights must sum to 1.0")

        if not self.calibration_method:
            raise ValueError("calibration_method is required")


def default_antispoof_scoring_policy() -> AntispoofScoringPolicy:
    policy = AntispoofScoringPolicy(
        policy_id=DEFAULT_ANTISPOOF_SCORING_POLICY_ID,
        threshold=0.5,
        model_weight=0.7,
        texture_weight=0.15,
        screen_weight=0.15,
        calibration_method="clamp_v1",
    )
    policy.validate()
    return policy
