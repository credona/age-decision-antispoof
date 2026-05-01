"""Helpers for deterministic changelog version sections."""

from __future__ import annotations

import re
from pathlib import Path

VERSION_SECTION_HEADING_RE = re.compile(r"<h2>\d+\.\d+\.\d+</h2>")
INSERT_ANCHOR_AFTER = (
    "Global project direction is tracked in the central Age Decision repository.\n\n"
)


def build_version_heading(version: str) -> str:
    return f"<h2>{version}</h2>"


def build_changelog_block(version: str, items: tuple[str, ...]) -> str:
    lines = [build_version_heading(version), "", "<ul>"]
    for item in items:
        lines.append(f"  <li>{item}</li>")
    lines.extend(["</ul>", "", "<hr>", "", ""])
    return "\n".join(lines)


def replace_or_prepend_version_section(text: str, version: str, block: str) -> str:
    """Replace only the managed version block, or insert it before the first semver section.

    Idempotent for a fixed ``block``: repeated application yields the same result when
    ``block`` is unchanged. Older release sections are never removed.
    """
    heading = build_version_heading(version)
    pattern = re.compile(
        re.escape(heading) + r"\s*\n\s*<ul>.*?</ul>\s*\n\s*<hr>\s*\n*",
        re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(block, text, count=1)

    m = VERSION_SECTION_HEADING_RE.search(text)
    if m:
        return text[: m.start()] + block + text[m.start() :]

    if INSERT_ANCHOR_AFTER in text:
        return text.replace(INSERT_ANCHOR_AFTER, INSERT_ANCHOR_AFTER + block, 1)

    raise ValueError(
        "CHANGELOG.md has no semver <h2> section and lacks the insert anchor paragraph"
    )


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | Path, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")
