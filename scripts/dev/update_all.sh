#!/usr/bin/env bash
set -euo pipefail

python scripts/docs/update_compatibility.py
python scripts/docs/update_readme_examples.py
python scripts/docs/update_docs_usage.py
python scripts/docs/update_docs_compatibility.py

echo "Project generated files updated."
