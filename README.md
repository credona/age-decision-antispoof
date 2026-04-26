<h1>Age Decision AntiSpoof</h1>

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/ci.yml?branch=main&label=CI" alt="CI">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/docker.yml?branch=main&label=Docker" alt="Docker">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/codeql.yml?branch=main&label=CodeQL" alt="CodeQL">
  <img src="https://img.shields.io/github/v/release/credona/age-decision-antispoof" alt="Release">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License">
</p>

Age Decision AntiSpoof is the anti-spoofing service of the Age Decision project.

It estimates whether a face image looks like a real human capture or a spoof attempt.

<hr>

<h2>Purpose</h2>

This service focuses on presentation attack detection for still images.

It combines an ONNX anti-spoofing model with image heuristics and exposes a structured API.

- real / spoof decision
- spoof score
- Credona anti-spoof trust score
- privacy-first response metadata
- request_id and correlation_id traceability
- structured JSON logs
- benchmark metrics and threshold tuning
- automated CI, Docker build, CodeQL and release workflow

<hr>

<h2>Status</h2>

Current version: <b>v1.1.1</b>

Validated status:

```text
45 passed
```

<hr>

<h2>Repository structure</h2>

```text
age-decision-antispoof/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── codeql.yml
│   │   ├── docker.yml
│   │   └── release.yml
│   └── dependabot.yml
├── antispoof/
│   ├── api/
│   ├── benchmark/
│   ├── calibration/
│   ├── core/
│   ├── heuristics/
│   ├── integrations/
│   ├── metrics/
│   ├── models/
│   ├── preprocessing/
│   ├── privacy/
│   ├── utils/
│   ├── pipeline.py
│   ├── result.py
│   └── version.py
├── benchmarks/
│   └── datasets/
├── scripts/
├── tests/
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.dev.yml
├── requirements.txt
├── pyproject.toml
├── ROADMAP.md
├── LICENSE
└── README.md
```

<hr>

<h2>Model</h2>

The current anti-spoofing model is:

```text
MiniFASNetV2.onnx
```

Expected path:

```text
antispoof/models/MiniFASNetV2.onnx
```

The model output is treated as a 3-class output.

```text
real_score = probability[1]
spoof_score = probability[0] + probability[2]
```

<h3>Download model</h3>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_models.py
```

<hr>

<h2>Environment variables</h2>

Example `.env` for local development:

```env
ANTISPOOF_PORT=8001

ANTISPOOF_THRESHOLD=0.5
ANTISPOOF_MODEL_PATH=antispoof/models/MiniFASNetV2.onnx

MODEL_WEIGHT=0.7
TEXTURE_WEIGHT=0.15
SCREEN_WEIGHT=0.15

LOG_LEVEL=INFO
```

`APP_NAME` and `APP_VERSION` are application constants and are not controlled by environment variables.

The three scoring weights must sum to 1.0.

<hr>

<h2>Local Development with Docker</h2>

The Docker configuration in this repository is intended for local development only.

It does not represent the production deployment configuration of Credona hosted services.

Start the service:

```bash
cp .env.example.dev .env
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
```

Check service:

```bash
curl -i http://localhost:8001/health
```

View logs:

```bash
docker compose -f docker-compose.dev.yml logs -f age-decision-antispoof
```

Stop service:

```bash
docker compose -f docker-compose.dev.yml down -v
```

<hr>

<h2>Docker image</h2>

The production-oriented image is built from `Dockerfile`.

Build locally:

```bash
docker build -t age-decision-antispoof:local .
```

Run locally:

```bash
docker run --rm -p 8001:8001 age-decision-antispoof:local
```

Official GHCR image:

```text
ghcr.io/credona/age-decision-antispoof
```

Available tags after release:

```text
ghcr.io/credona/age-decision-antispoof:v1.0.1
ghcr.io/credona/age-decision-antispoof:v1.0.2
ghcr.io/credona/age-decision-antispoof:v1.1.0
ghcr.io/credona/age-decision-antispoof:v1.1.1
ghcr.io/credona/age-decision-antispoof:latest
```

<hr>

<h2>API endpoints</h2>

<h3>Health</h3>

```bash
curl -i http://localhost:8001/health
```

```json
{
  "status": "ok",
  "service": "age-decision-antispoof",
  "version": "1.1.1"
}
```

<h3>Model status</h3>

```bash
curl -i http://localhost:8001/model/status
```

```json
{
  "service": "age-decision-antispoof",
  "version": "1.1.1",
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

<h3>Check anti-spoof</h3>

```bash
curl -X POST http://localhost:8001/check \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

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
  }
}
```

<h3>Benchmark</h3>

```bash
curl -i http://localhost:8001/benchmark
```

The benchmark endpoint runs evaluation on the local benchmark dataset if available.

It exposes APCER, BPCER, ACER and a threshold recommendation.

<hr>

<h2>Scores</h2>

<h3>confidence</h3>

Calibrated final score used to decide whether the image is real.

<h3>spoof_score</h3>

Model-derived probability-like score representing spoof likelihood.

<h3>cred_antispoof_score</h3>

Credona trust score for anti-spoofing evidence.

A higher value means the capture is more likely to be real.

<hr>

<h2>Metrics</h2>

- <b>APCER</b>: attack presentations incorrectly classified as real.
- <b>BPCER</b>: bona fide presentations incorrectly classified as spoof.
- <b>ACER</b>: average of APCER and BPCER.

The ACER-optimal threshold on the local 200-image subset was 0.37.

However, that threshold increased APCER.

For safety-oriented deployments, 0.5 remains the default until larger validation benchmarks are available.

<hr>

<h2>Benchmark dataset</h2>

Real benchmark images are not committed to Git.

A local CelebA-Spoof-compatible subset can be downloaded for integration tests.

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_benchmark_dataset.py --limit 200
docker compose -f docker-compose.dev.yml exec age-decision-antispoof pytest
```

Expected local structure:

```text
benchmarks/datasets/celeba_spoof/
├── README.md
├── labels.csv
└── images/
```

<hr>

<h2>Privacy</h2>

The API processes uploaded images in memory only.

It does not persist raw images, store biometric templates, or log image content.

<hr>

<h2>Logging</h2>

Logs are structured JSON events.

```json
{
  "timestamp": "2026-04-25T20:07:58+00:00",
  "service": "age-decision-antispoof",
  "version": "1.1.1",
  "event": "antispoof_check_completed",
  "request_id": "test-request-001",
  "correlation_id": "test-correlation-001",
  "decision": "real",
  "confidence": 0.82,
  "spoof_score": 0.18,
  "cred_antispoof_score": 0.82
}
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

<h2>Integration with Age Decision</h2>

`age-decision-core` handles face detection and age estimation.

`age-decision-antispoof` handles real / spoof analysis.

`age-decision-api` orchestrates both services and exposes the final verification API.

```text
image
→ age-decision-api
  → age-decision-core
  → age-decision-antispoof
→ final decision
```

<hr>

<h2>Automation</h2>

This repository includes:

- GitHub Actions CI
- automated tests on pull requests
- Docker image build
- automated GHCR publishing
- automated GitHub release creation
- tag-based release notes
- CodeQL scanning
- Dependabot updates

<hr>

<h2>Testing</h2>

Run all tests:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof pytest
```

Run only integration tests:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof pytest tests/integration
```

Current result:

```text
45 passed
```

<hr>

<h2>Scope</h2>

This service does not perform:

- identity verification
- face recognition
- document verification
- age estimation
- gender prediction
- emotion prediction
- active liveness challenge

Its scope is limited to estimating whether a face image appears to be a real capture or a spoof attempt.

<hr>

<h2>Limitations</h2>

- `v1.1.1` works on still images.
- `v1.1.1` does not perform active liveness checks.
- `v1.1.1` does not analyze video sequences.
- Thresholds require larger validation datasets before production tuning.
- This repository is not certified as an industrial PAD system.
- Model and dataset licenses must be reviewed before redistribution or commercial use.

<hr>

<h2>Roadmap</h2>

See `ROADMAP.md`.

<hr>

<h2>License</h2>

This repository is released under the Apache License 2.0.

See the `LICENSE` file for details.
