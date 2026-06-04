import json
from pathlib import Path

from antispoof.domain.calibration.lifecycle import CalibrationLifecycleState


class FileCalibrationLifecycleStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> CalibrationLifecycleState:
        if not self.path.exists():
            return CalibrationLifecycleState.empty()

        payload = json.loads(self.path.read_text(encoding="utf-8"))

        return CalibrationLifecycleState(
            active_policy_id=payload.get("active_policy_id"),
            previous_policy_id=payload.get("previous_policy_id"),
            activated_at=payload.get("activated_at"),
        )

    def save(self, state: CalibrationLifecycleState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(
                {
                    "active_policy_id": state.active_policy_id,
                    "previous_policy_id": state.previous_policy_id,
                    "activated_at": state.activated_at,
                },
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
