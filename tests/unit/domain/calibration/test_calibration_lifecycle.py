from antispoof.domain.calibration.lifecycle import CalibrationLifecycleState


def test_lifecycle_state_tracks_active_and_previous_policy() -> None:
    state = CalibrationLifecycleState(
        active_policy_id="policy-2",
        previous_policy_id="policy-1",
        activated_at="2026-06-04T00:00:00+00:00",
    )

    assert state.active_policy_id == "policy-2"
    assert state.previous_policy_id == "policy-1"


def test_lifecycle_state_can_represent_empty_runtime() -> None:
    state = CalibrationLifecycleState.empty()

    assert state.active_policy_id is None
    assert state.previous_policy_id is None
    assert state.activated_at is None
