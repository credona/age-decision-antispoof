#!/usr/bin/env bash
set -euo pipefail

ruff check .
ruff format --check .

if grep -rIn "[[:blank:]]$" antispoof tests scripts docs README.md CHANGELOG.md CONTRIBUTING.md; then
  echo "Trailing whitespace found"
  exit 1
fi

FAILED=0

for file in $(find antispoof tests scripts docs -type f \( -name "*.py" -o -name "*.md" -o -name "*.sh" \)); do
  if [ -s "$file" ] && [ "$(tail -c1 "$file")" != "" ]; then
    echo "Missing final newline: $file"
    FAILED=1
  fi
done

for file in README.md CHANGELOG.md CONTRIBUTING.md pyproject.toml project.json compatibility.json; do
  if [ -f "$file" ] && [ -s "$file" ] && [ "$(tail -c1 "$file")" != "" ]; then
    echo "Missing final newline: $file"
    FAILED=1
  fi
done

if [ "$FAILED" -ne 0 ]; then
  exit "$FAILED"
fi

python -m compileall antispoof tests scripts
python scripts/metadata/check_project_metadata.py
python scripts/metadata/check_compatibility_metadata.py
python scripts/docs/update_readme_examples.py
./scripts/ci/assert_file_unchanged.sh README.md python scripts/docs/update_readme_examples.py
./scripts/ci/assert_file_unchanged.sh docs/usage.md python scripts/docs/update_docs_usage.py
./scripts/ci/assert_file_unchanged.sh docs/compatibility.md python scripts/docs/update_docs_compatibility.py
pytest

echo "CI-equivalent check passed."
