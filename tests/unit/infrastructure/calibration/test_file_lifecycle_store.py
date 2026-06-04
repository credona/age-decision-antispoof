from pathlib import Path

from antispoof.domain.calibration.lifecycle import CalibrationLifecycleState
from antispoof.infrastructure.calibration.file_lifecycle_store import FileCalibrationLifecycleStore


def test_file_lifecycle_store_returns_empty_state_when_missing(tmp_path: Path) -> None:
    store = FileCalibrationLifecycleStore(tmp_path / "lifecycle.json")

    state = store.load()

    assert state == CalibrationLifecycleState.empty()


def test_file_lifecycle_store_persists_active_and_previous_state(tmp_path: Path) -> None:
    path = tmp_path / "lifecycle.json"
    store = FileCalibrationLifecycleStore(path)

    state = CalibrationLifecycleState(
        active_policy_id="policy-2",
        previous_policy_id="policy-1",
        activated_at="2026-06-04T00:00:00+00:00",
    )

    store.save(state)

    assert FileCalibrationLifecycleStore(path).load() == state
