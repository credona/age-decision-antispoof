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

<h2>Quickstart</h2>

```bash
cp .env.example.dev .env
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_models.py
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
  "version": "2.1.0",
  "contract_version": "2.0"
}
```
<!-- END:HEALTH_RESPONSE -->

Expected version response:

<!-- BEGIN:VERSION_RESPONSE -->
```json
{
  "service_name": "age-decision-antispoof",
  "app_name": "Age Decision AntiSpoof",
  "version": "2.1.0",
  "contract_version": "2.0",
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

Compatibility metadata is declared in `compatibility.json` and checked by CI.

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-antispoof",
  "version": "2.1.0",
  "contract_version": "2.0",
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
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_models.py
```

Expected path:

```text
antispoof/models/MiniFASNetV2.onnx
```

See docs/models.md for model origin, license notes, and redistribution checks.

<hr>

<h2>Docker image</h2>

```text
ghcr.io/credona/age-decision-antispoof
```

Run with mounted models:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_models.py

docker run --rm \
  -p 8001:8001 \
  -v "$PWD/antispoof/models:/app/antispoof/models" \
  ghcr.io/credona/age-decision-antispoof:latest
```

<hr>

<h2>Quality and compatibility checks</h2>

Run tests:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof pytest
```

Run contract tests:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof pytest tests/unit/contract
```

Run quality checks:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof ruff check .
docker compose -f docker-compose.dev.yml exec age-decision-antispoof ruff format --check .
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/check_project_metadata.py
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/check_compatibility_metadata.py
```

Update generated documentation blocks:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/update_readme_examples.py
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/update_docs_usage.py
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/update_docs_compatibility.py
```

<hr>

<h2>Testing</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_models.py
docker compose -f docker-compose.dev.yml exec age-decision-antispoof pytest
```

<hr>

<h2>License</h2>

This repository is released under the Apache License 2.0.

Third-party models may have their own upstream license and constraints.

See docs/models.md for details.
