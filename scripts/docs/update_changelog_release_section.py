"""Deterministically maintain the v2.4.0 release section in CHANGELOG.md."""

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
MANAGED_VERSION = "2.4.0"

CHANGELOG_SECTION_ITEMS: tuple[str, ...] = (
    "Introduced pipeline-oriented application, domain, and infrastructure boundaries.",
    "Added privacy-safe logging tests covering image, base64, raw payload, "
    "internal scores, thresholds, and downstream data leakage.",
    "Added deterministic rejection for unsupported v3 input types: image_sequence and video.",
    "Renamed liveness use case and pipeline port to neutral spoof check terminology.",
    "Renamed public status metadata from model info to engine info.",
    "Renamed internal confidence terminology to signal quality.",
    "Centralized public decisions, model metadata, privacy metadata, and log levels as constants.",
    "Updated documentation from model status terminology to engine status terminology.",
    "Preserved the existing public API contract and privacy-first forbidden field checks.",
    "Validated the refactor through Docker CI-equivalent checks.",
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
