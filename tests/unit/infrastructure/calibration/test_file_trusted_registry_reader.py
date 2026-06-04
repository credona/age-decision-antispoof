import json
from pathlib import Path

from antispoof.infrastructure.calibration.file_trusted_registry_reader import (
    FileTrustedCalibrationRegistryReader,
)


def test_file_trusted_registry_reader_reads_registry(tmp_path: Path) -> None:
    path = tmp_path / "trusted-registry.json"
    path.write_text(
        json.dumps(
            {
                "trusted_policy_ids": ["policy-1"],
                "revoked_policy_ids": ["policy-0"],
            }
        ),
        encoding="utf-8",
    )

    registry = FileTrustedCalibrationRegistryReader(path).read()

    assert registry.trusted_policy_ids == ("policy-1",)
    assert registry.revoked_policy_ids == ("policy-0",)
