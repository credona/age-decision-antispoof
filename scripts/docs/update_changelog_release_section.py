"""Deterministically maintain the v2.3.0 release section in CHANGELOG.md."""

from __future__ import annotations

import sys
from pathlib import Path

_DOCS_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_DOCS_SCRIPTS_DIR))

from changelog_utils import (  # noqa: E402
    build_changelog_block,
    read_text,
    replace_or_prepend_version_section,
    write_text,
)

CHANGELOG_PATH = Path("CHANGELOG.md")
MANAGED_VERSION = "2.3.0"

CHANGELOG_SECTION_ITEMS: tuple[str, ...] = (
    "Added stable public status contract regression coverage for "
    "<code>/health</code> and <code>/model/status</code>.",
    "Standardized the public error response model to expose only "
    "<code>request_id</code>, <code>correlation_id</code>, and <code>error</code>.",
    "Normalized request validation errors to the same public ErrorResponse contract.",
    "Mapped missing multipart file validation failures to <code>missing_file</code> "
    "with HTTP 400 and <code>Invalid request.</code>.",
    "Preserved privacy-first forbidden field guarantees for anti-spoof public outputs.",
    "Documented AntiSpoof public contract deprecation rules in "
    "<code>docs/deprecation-policy.md</code>.",
    "Documented the AntiSpoof error model and codes in <code>docs/error-model.md</code>.",
    "Documented stable status endpoints and <code>contract_version</code> behavior in "
    "<code>docs/status-contract.md</code>.",
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
