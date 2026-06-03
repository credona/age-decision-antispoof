"""Deterministically maintain the v2.6.0 release section in CHANGELOG.md."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCRIPTS_DIR))

from lib.changelog import (  # noqa: E402
    build_changelog_block,
    read_text,
    replace_or_prepend_version_section,
    write_text,
)

CHANGELOG_PATH = Path("CHANGELOG.md")
MANAGED_VERSION = "2.6.0"

CHANGELOG_SECTION_ITEMS: tuple[str, ...] = (
    "Updated project and compatibility metadata to v2.6.0.",
    "Aligned AntiSpoof with the centralized age-decision-benchmark laboratory.",
    "Removed legacy local benchmark orchestration and sample benchmark datasets "
    "from the service repository.",
    "Kept AntiSpoof focused on spoof analysis, public contract, privacy, "
    "scoring, and dataset manifest parsing.",
    "Added runtime private calibration policy loading for AntiSpoof.",
    "Added SHA-256 integrity verification for private calibration policies.",
    "Added Ed25519 signature verification for private calibration policies.",
    "Added service, contract_version, and model_identifier compatibility checks "
    "before calibration activation.",
    "Added fail-fast runtime activation when AntiSpoof calibration is required "
    "but missing or invalid.",
    "Applied deterministic AntiSpoof calibration before spoof decision computation.",
    "Hardened response filtering and privacy tests to prevent calibration internals "
    "from reaching public responses.",
    "Hardened safe logging to prevent private calibration fields, signatures, hashes, "
    "weights, margins, and thresholds from being logged.",
    "Ensured private runtime calibration policies are excluded from Git tracking.",
    "Preserved Docker CI-equivalent validation after runtime calibration integration.",
)


def main() -> None:
    block = build_changelog_block(MANAGED_VERSION, CHANGELOG_SECTION_ITEMS)
    text = read_text(CHANGELOG_PATH)
    try:
        updated = replace_or_prepend_version_section(text, MANAGED_VERSION, block)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    write_text(CHANGELOG_PATH, updated)


if __name__ == "__main__":
    main()
