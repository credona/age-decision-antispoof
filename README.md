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

It does not perform identity verification, face recognition, document verification, age estimation, or active liveness challenge.

<hr>

<h2>Documentation</h2>

- Usage: docs/usage.md
- Models and third-party notes: docs/models.md
- Benchmarks: docs/benchmarks.md
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
curl -i http://localhost:8001/model/status
```

Run an anti-spoof check:

```bash
curl -X POST http://localhost:8001/check \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

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
