#!/usr/bin/env bash
set -euo pipefail

ruff check . --fix
ruff format .

python scripts/metadata/sync_compatibility_metadata.py

python scripts/docs/update_readme_examples.py
python scripts/docs/update_docs_usage.py
python scripts/docs/update_docs_compatibility.py
python scripts/docs/update_changelog_release_section.py

python scripts/metadata/check_project_metadata.py
python scripts/metadata/check_compatibility_metadata.py
python scripts/metadata/check_docker_metadata.py

echo "Auto-fix passed."
