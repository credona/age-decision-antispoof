<h1>Contributing to Age Decision AntiSpoof</h1>

This repository contains the AntiSpoof service.

For global contribution rules, see:

```text
https://github.com/credona/age-decision/blob/main/CONTRIBUTING.md
```

<hr>

<h2>Local setup</h2>

```bash
cp .env.example.dev .env
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/models/download_models.py
```

<hr>

<h2>Run tests</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/models/download_models.py
docker compose -f docker-compose.dev.yml exec age-decision-antispoof pytest
```

<hr>

<h2>Contribution scope</h2>

Good AntiSpoof contributions include:

- presentation attack detection improvements
- score calibration improvements
- benchmark improvements
- safer error handling
- privacy metadata improvements
- model transparency improvements
- tests and documentation

<hr>

<h2>Rules</h2>

Do not commit:

- private images
- biometric templates
- credentials
- generated cache folders
- local secrets
- unlicensed model files
- ONNX model binaries
- benchmark datasets without clear license review

Models must be downloaded using:

```text
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/models/download_models.py
```

<hr>

<h2>Model policy</h2>

When modifying models:

- update docs/models.md
- update scripts/models/download_models.py
- verify upstream license
- document source and usage

<hr>

<h2>Documentation</h2>

Use:

- README.md for the repository entry point
- docs/usage.md for service usage
- docs/models.md for model transparency
- docs/benchmarks.md for benchmark methodology
- CHANGELOG.md for release history
