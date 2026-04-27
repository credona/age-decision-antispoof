<h1>Age Decision AntiSpoof Usage</h1>

This document describes how to run and use the AntiSpoof service.

For global project concepts, see:

```text
https://github.com/credona/age-decision
```

<hr>

<h2>Environment</h2>

Create a local environment file:

```bash
cp .env.example.dev .env
```

Example:

```env
ANTISPOOF_PORT=8001

ANTISPOOF_THRESHOLD=0.5
ANTISPOOF_MODEL_PATH=antispoof/models/MiniFASNetV2.onnx

MODEL_WEIGHT=0.7
TEXTURE_WEIGHT=0.15
SCREEN_WEIGHT=0.15

LOG_LEVEL=INFO
```

The three scoring weights must sum to `1.0`.

<hr>

<h2>Model setup</h2>

Download model files locally:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_models.py
```

Expected file:

```text
antispoof/models/MiniFASNetV2.onnx
```

Model binaries are not intended to be committed to Git or embedded in Docker images.

<hr>

<h2>Run with Docker</h2>

```bash
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_models.py
```

View logs:

```bash
docker compose -f docker-compose.dev.yml logs -f age-decision-antispoof
```

Stop the service:

```bash
docker compose -f docker-compose.dev.yml down -v
```

<hr>

<h2>Health</h2>

```bash
curl -i http://localhost:8001/health
```

Example response:

```json
{
  "status": "ok",
  "service": "age-decision-antispoof",
  "version": "1.2.1"
}
```

<hr>

<h2>Model status</h2>

```bash
curl -i http://localhost:8001/model/status
```

Example response:

```json
{
  "service": "age-decision-antispoof",
  "version": "1.2.1",
  "antispoof_model": {
    "type": "onnx",
    "name": "MiniFASNetV2",
    "path": "antispoof/models/MiniFASNetV2.onnx",
    "exists": true,
    "loaded": true
  },
  "heuristics": [
    "texture",
    "screen_pattern",
    "blur"
  ],
  "threshold": 0.5,
  "weights": {
    "model": 0.7,
    "texture": 0.15,
    "screen": 0.15
  }
}
```

<hr>

<h2>Check anti-spoof</h2>

```bash
curl -X POST http://localhost:8001/check \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

Example response:

```json
{
  "request_id": "test-request-001",
  "correlation_id": "test-correlation-001",
  "provider": "age-decision-antispoof",
  "decision": "real",
  "is_real": true,
  "spoof_detected": false,
  "confidence": 0.82,
  "spoof_score": 0.18,
  "cred_antispoof_score": 0.82,
  "threshold": 0.5,
  "rejection_reason": null,
  "privacy": {
    "privacy_first": true,
    "image_persisted": false,
    "biometric_template_stored": false,
    "raw_image_logged": false,
    "processing_scope": "in_memory_inference_only",
    "retention_policy": "no_image_retention"
  },
  "model_info": {
    "antispoof_model": "MiniFASNetV2",
    "model_type": "onnx",
    "heuristics": [
      "texture",
      "screen_pattern",
      "blur"
    ]
  }
}
```

<hr>

<h2>Error response shape</h2>

Error responses follow a stable JSON format.

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
