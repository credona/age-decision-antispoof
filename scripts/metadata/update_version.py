"""Update project-wide version and contract metadata (not CHANGELOG)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
CONTRACT_PATTERN = re.compile(r"^\d+\.\d+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Set semantic version (X.Y.Z) and contract version (X.Y) in "
            "project.json, compatibility.json, and optional npm lockfiles."
        )
    )
    parser.add_argument("version", help="Release version, e.g. 2.3.0")
    parser.add_argument("contract_version", help="Public contract line, e.g. 2.3")
    return parser.parse_args()


def validate_version(version: str) -> None:
    if not VERSION_PATTERN.match(version):
        raise SystemExit(f"version must match X.Y.Z, got {version!r}")


def validate_contract_version(contract_version: str) -> None:
    if not CONTRACT_PATTERN.match(contract_version):
        raise SystemExit(f"contract_version must match X.Y, got {contract_version!r}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def update_project(repo_root: Path, version: str, contract_version: str) -> None:
    path = repo_root / "project.json"
    data = load_json(path)
    data["version"] = version
    data["contract_version"] = contract_version
    dump_json(path, data)


def update_compatibility(repo_root: Path, version: str, contract_version: str) -> None:
    path = repo_root / "compatibility.json"
    data = load_json(path)
    data["version"] = version
    data["contract_version"] = contract_version
    dump_json(path, data)


def update_package_json(repo_root: Path, version: str) -> None:
    path = repo_root / "package.json"
    if not path.is_file():
        return
    data = load_json(path)
    data["version"] = version
    dump_json(path, data)


def update_package_lock(repo_root: Path, version: str) -> None:
    path = repo_root / "package-lock.json"
    if not path.is_file():
        return
    data = load_json(path)
    data["version"] = version
    packages = data.get("packages")
    if isinstance(packages, dict) and isinstance(packages.get(""), dict):
        packages[""]["version"] = version
    dump_json(path, data)


def main() -> None:
    args = parse_args()
    validate_version(args.version)
    validate_contract_version(args.contract_version)

    repo_root = Path.cwd()
    try:
        update_project(repo_root, args.version, args.contract_version)
        update_compatibility(repo_root, args.version, args.contract_version)
        update_package_json(repo_root, args.version)
        update_package_lock(repo_root, args.version)
    except FileNotFoundError as exc:
        raise SystemExit(f"expected file missing: {exc.filename}") from exc


if __name__ == "__main__":
    main()
