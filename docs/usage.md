<h1>Age Decision AntiSpoof Usage</h1>

This document describes how to run and use the AntiSpoof service.

<hr>

<h2>Contributor usage</h2>

Start the development environment:

```bash
./scripts/docker/dev.sh
```

Download models:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-antispoof python scripts/models/download_models.py
```

Stop the environment:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml down
```

<hr>

<h2>Health checks</h2>

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
  "version": "2.3.0",
  "contract_version": "2.3"
}
```
<!-- END:HEALTH_RESPONSE -->

Expected version response:

<!-- BEGIN:VERSION_RESPONSE -->
```json
{
  "service_name": "age-decision-antispoof",
  "app_name": "Age Decision AntiSpoof",
  "version": "2.3.0",
  "contract_version": "2.3",
  "repository": "https://github.com/credona/age-decision-antispoof",
  "image": "ghcr.io/credona/age-decision-antispoof"
}
```
<!-- END:VERSION_RESPONSE -->

<hr>

<h2>Run an anti-spoof check</h2>

```bash
curl -X POST http://localhost:8001/check \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

<hr>

<h2>Runtime configuration</h2>

Default runtime values are declared in `project.json`.

Generated runtime files are written to:

```text
.generated/runtime/
```

Generated Compose files are written to:

```text
.generated/compose/
```

Do not edit generated files manually.

Regenerate them with:

```bash
./scripts/config/generate_env.sh dev
```

<hr>

<h2>External Docker usage</h2>

Run from the published image:

```bash
docker run --rm \
  -p 8001:8001 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-antispoof:latest
```

Override runtime values:

```bash
docker run --rm \
  -p 8001:8001 \
  -e SPOOF_THRESHOLD=0.8 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-antispoof:latest
```

<hr>

<h2>Public privacy contract</h2>

The public `/check` response does not expose:

- raw image content
- raw model scores
- raw logits
- heuristic details
- calibration details
- internal threshold value
- legacy `cred_score` alias

<hr>

<h2>Error response shape</h2>

Error responses follow a stable JSON format.

Request validation failures use the same shape and do not echo internal validation details.

The API does not expose internal exception details.

```json
{
  "request_id": "test-request-001",
  "correlation_id": "test-correlation-001",
  "error": {
    "code": "invalid_image",
    "message": "Invalid request."
  }
}
```

Known error codes:

```text
missing_file
empty_file
invalid_image
antispoof_processing_error
benchmark_dataset_unavailable
benchmark_runtime_error
internal_error
```

<hr>

<h2>Python usage</h2>

```python
from antispoof import AntiSpoof

pipeline = AntiSpoof()
result = pipeline.predict_from_path("test-face.jpg")

print(result.is_real)
print(result.cred_antispoof_score)
print(result.to_dict())
```

<hr>

<h2>Validation</h2>

Run the full auto-fix and validation pipeline:

```bash
./scripts/ci/fix_all_docker.sh
```

Run validation only:

```bash
./scripts/ci/check_all_docker.sh
```

<hr>

<h2>Compatibility metadata</h2>

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-antispoof",
  "version": "2.3.0",
  "contract_version": "2.3",
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

<h2>Scope</h2>

This service works on still images.

It does not perform:

- identity verification
- face recognition
- document verification
- age estimation
- gender prediction
- emotion prediction
- active liveness challenge
- video liveness analysis
