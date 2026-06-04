from antispoof.infrastructure.calibration import (
    get_antispoof_public_calibration_summary,
    load_antispoof_runtime_calibration,
    rollback_antispoof_runtime_calibration,
)


def test_runtime_calibration_exports_are_available() -> None:
    assert callable(load_antispoof_runtime_calibration)
    assert callable(rollback_antispoof_runtime_calibration)
    assert callable(get_antispoof_public_calibration_summary)
