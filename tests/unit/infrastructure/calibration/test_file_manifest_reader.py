import json
from pathlib import Path

from antispoof.infrastructure.calibration.file_manifest_reader import (
    FileCalibrationManifestReader,
)


def test_file_manifest_reader_reads_distribution_manifest(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps(
            {
                "service": "antispoof",
                "contract_version": "2.6",
                "model_identifier": "credona.antispoof.minifasnet-v2.v1",
                "allowed_policy_ids": ["policy-1"],
                "revoked_policy_ids": ["policy-0"],
            }
        ),
        encoding="utf-8",
    )

    manifest = FileCalibrationManifestReader(path).read()

    assert manifest.service == "antispoof"
    assert manifest.allowed_policy_ids == ("policy-1",)
    assert manifest.revoked_policy_ids == ("policy-0",)
