from dataclasses import dataclass


@dataclass(frozen=True)
class CalibrationLifecycleState:
    active_policy_id: str | None
    previous_policy_id: str | None
    activated_at: str | None

    @classmethod
    def empty(cls) -> "CalibrationLifecycleState":
        return cls(
            active_policy_id=None,
            previous_policy_id=None,
            activated_at=None,
        )
