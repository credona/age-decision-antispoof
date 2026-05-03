"""Deterministically maintain the v2.5.0 release section in CHANGELOG.md."""

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
MANAGED_VERSION = "2.5.0"

CHANGELOG_SECTION_ITEMS: tuple[str, ...] = (
    "Introduced model metadata and registry abstractions for presentation attack detection models.",
    "Replaced low-level runtime model paths with stable model identifiers.",
    "Simplified runtime configuration with shared common values and empty dev/prod overrides.",
    "Moved spoof threshold and fusion weights into a versioned scoring policy.",
    "Added deterministic scoring policy tests covering score bounds, "
    "monotonicity, stability, and privacy.",
    "Documented the public scoring methodology for cred_antispoof_score.",
    "Documented calibration methodology, model reproducibility metadata, "
    "benchmark methodology, and dataset transparency.",
    "Removed threshold logic from runtime configuration.",
    "Preserved the privacy-first public contract and response filtering guarantees.",
    "Validated the release through Docker CI-equivalent checks.",
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
