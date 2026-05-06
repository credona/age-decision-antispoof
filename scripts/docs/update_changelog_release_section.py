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
    "Added privacy-safe benchmark report schema for API end-to-end benchmarks.",
    "Added API end-to-end benchmark execution script for the public verification flow.",
    "Added aggregate latency, decision distribution, and spoof-check presence metrics.",
    "Added machine, runtime, dataset, and hosting provider metadata in benchmark reports.",
    "Added benchmark privacy tests preventing raw payloads and downstream response exposure.",
    "Added benchmark output schema tests for reproducible reporting.",
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
