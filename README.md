<h1>Age Decision AntiSpoof</h1>

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/ci.yml?branch=main&label=CI" alt="CI">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/docker.yml?branch=main&label=Docker" alt="Docker">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/codeql.yml?branch=main&label=CodeQL" alt="CodeQL">
  <img src="https://img.shields.io/github/v/release/credona/age-decision-antispoof" alt="Release">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License">
</p>

Age Decision AntiSpoof is the presentation attack detection service of the Age Decision ecosystem.

It estimates whether a face image appears to be a real human capture or a spoof attempt.

It does not expose raw model scores, heuristic details, or internal calibration details through the public API.

It does not perform identity verification, face recognition, document verification, age estimation, or active liveness challenge.

<hr>

<h2>Documentation</h2>

- Repository: https://github.com/credona/age-decision-antispoof
- Usage: docs/usage.md
- Models and third-party notes: docs/models.md
- Benchmarks: docs/benchmarks.md
- Compatibility: docs/compatibility.md
- Changelog: CHANGELOG.md
- Contributing: CONTRIBUTING.md
- Global project: https://github.com/credona/age-decision

<hr>

<h2>Quickstart for contributors</h2>

Start the development environment:

```bash
./scripts/docker/dev.sh
```

Download local model files:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-antispoof python scripts/models/download_models.py
```

Check the service:

```bash
curl -i http://localhost:8001/health
curl -i http://localhost:8001/version
curl -i http://localhost:8001/model/status
```

Expected health response:

<!-- BEGIN:HEALTH_RESPONSE -->
```json
{
  "status": "ok",
  "service": "age-decision-antispoof",
  "version": "2.2.1",
  "contract_version": "2.2"
}
```
<!-- END:HEALTH_RESPONSE -->

Expected version response:

<!-- BEGIN:VERSION_RESPONSE -->
```json
{
  "service_name": "age-decision-antispoof",
  "app_name": "Age Decision AntiSpoof",
  "version": "2.2.1",
  "contract_version": "2.2",
  "repository": "https://github.com/credona/age-decision-antispoof",
  "image": "ghcr.io/credona/age-decision-antispoof"
}
```
<!-- END:VERSION_RESPONSE -->

Run an anti-spoof check:

```bash
curl -X POST http://localhost:8001/check \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

<hr>

<h2>One-command workflow</h2>

Auto-fix, regenerate metadata and documentation, then validate everything:

```bash
./scripts/ci/fix_all_docker.sh
```

Run strict validation only:

```bash
./scripts/ci/check_all_docker.sh
```

Start the development container:

```bash
./scripts/docker/dev.sh
```

Build an image with metadata from `project.json`:

```bash
./scripts/docker/build.sh prod
./scripts/docker/build.sh dev
```

<hr>

<h2>Configuration model</h2>

Project metadata is declared once in:

```text
project.json
```

Generated environment files are created under:

```text
.generated/
```

Do not edit generated files manually.

Runtime defaults are generated from `project.json`.

External users may still override runtime values with Docker environment variables.

Example:

```bash
docker run --rm \
  -p 8001:8001 \
  -e SPOOF_THRESHOLD=0.8 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-antispoof:latest
```

<hr>

<h2>Public contract</h2>

The main response exposes:

- `decision`
- `is_real`
- `spoof_detected`
- `cred_antispoof_score`
- `request_id`
- `correlation_id`
- `privacy`
- `model_info`
- `rejection_reason`

The public response does not expose:

- raw model scores
- raw logits
- heuristic details
- calibration details
- internal threshold value
- legacy `cred_score` alias

<hr>

<h2>Compatibility metadata</h2>

Compatibility metadata is declared in `compatibility.json` and synchronized from `project.json`.

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-antispoof",
  "version": "2.2.1",
  "contract_version": "2.2",
  "compatible_with": {
    "age-decision-api": ">=2.0.0 <3.0.0",
    "age-decision-js": ">=2.0.0 <3.0.0"
  },
  "public_contract": {
    "decision_values": [
      "real",
      "spoof"
    ],
    "score_field": "cred_antispoof_score",
    "raw_model_scores_exposed": false,
    "heuristic_details_exposed": false,
    "calibration_details_exposed": false,
    "legacy_cred_score_exposed": false
  }
}
```
<!-- END:COMPATIBILITY_METADATA -->

<hr>

<h2>Model files</h2>

The service relies on external ONNX model files.

Model binaries are not intended to be committed to Git.

Model binaries are not intended to be embedded in the public Docker image.

Download them explicitly:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-antispoof python scripts/models/download_models.py
```

Expected path:

```text
models/MiniFASNetV2.onnx
```

See docs/models.md for model origin, license notes, and redistribution checks.

<hr>

<h2>Docker image</h2>

```text
ghcr.io/credona/age-decision-antispoof
```

Run with mounted models:

```bash
docker run --rm \
  -p 8001:8001 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-antispoof:latest
```

<hr>

<h2>License</h2>

This repository is released under the Apache License 2.0.

Third-party models may have their own upstream license and constraints.

See docs/models.md for details.
