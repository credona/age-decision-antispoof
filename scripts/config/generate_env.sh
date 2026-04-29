#!/usr/bin/env bash
set -euo pipefail

PROFILE="${1:-dev}"

mkdir -p .generated/compose .generated/runtime

docker run --rm -i \
  -v "$PWD:/workspace" \
  -w /workspace \
  python:3.14-slim \
  python - "$PROFILE" <<'PY'
import json
import sys
from pathlib import Path

profile = sys.argv[1]
project = json.loads(Path("project.json").read_text(encoding="utf-8"))

for key in ("version", "repository", "license", "docker", "runtime"):
    if key not in project:
        raise SystemExit(f"Missing '{key}' in project.json")

if profile not in project["docker"]:
    raise SystemExit(f"Missing docker.{profile} in project.json")

if profile not in project["runtime"]:
    raise SystemExit(f"Missing runtime.{profile} in project.json")

docker_conf = project["docker"][profile]
runtime_conf = project["runtime"][profile]

compose_env = {
    "AGE_DECISION_ANTISPOOF_VERSION": project["version"],
    "AGE_DECISION_ANTISPOOF_REPOSITORY": project["repository"],
    "AGE_DECISION_ANTISPOOF_LICENSE": project["license"],
    "AGE_DECISION_ANTISPOOF_DOCKERFILE": docker_conf["dockerfile"],
    "AGE_DECISION_ANTISPOOF_IMAGE": docker_conf["image"],
    "AGE_DECISION_ANTISPOOF_TITLE": docker_conf["title"],
    "AGE_DECISION_ANTISPOOF_DESCRIPTION": docker_conf["description"],
    "ANTISPOOF_PORT": runtime_conf["ANTISPOOF_PORT"],
}

Path(f".generated/compose/{profile}.env").write_text(
    "\n".join(f"{key}={value}" for key, value in compose_env.items()) + "\n",
    encoding="utf-8",
)

Path(f".generated/runtime/{profile}.env").write_text(
    "\n".join(f"{key}={value}" for key, value in runtime_conf.items()) + "\n",
    encoding="utf-8",
)

print("Env generation OK")
PY

for file in ".generated/compose/$PROFILE.env" ".generated/runtime/$PROFILE.env"; do
  if [ ! -s "$file" ]; then
    echo "ERROR: $file is empty"
    exit 1
  fi
done

echo "Generated .generated/compose/$PROFILE.env"
echo "Generated .generated/runtime/$PROFILE.env"
