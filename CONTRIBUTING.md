<h1>Contributing to Age Decision AntiSpoof</h1>

This repository contains the AntiSpoof service.

For global contribution rules, see:

```text
https://github.com/credona/age-decision/blob/main/CONTRIBUTING.md
```

<hr>

<h2>Local setup</h2>

Start the development environment:

```bash
./scripts/docker/dev.sh
```

Download model files:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-antispoof python scripts/models/download_models.py
```

<hr>

<h2>Developer workflow</h2>

Auto-fix, regenerate generated files, run tests, then run the final check:

```bash
./scripts/ci/fix_all_docker.sh
```

Run validation only:

```bash
./scripts/ci/check_all_docker.sh
```

Prepare a release locally:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-antispoof scripts/ci/release_prepare.sh
```

<hr>

<h2>Configuration policy</h2>

Project metadata is edited in:

```text
project.json
```

Generated files are written under:

```text
.generated/
```

Do not edit generated files manually.

Do not duplicate the service name, application name, version, contract version, Docker image metadata, or default runtime values in environment files.

Compatibility metadata is synchronized from `project.json`.

Release tags must match the version declared in `project.json`.

Example:

```text
project.json version: 2.2.1
Git tag: v2.2.1
```

<hr>

<h2>Generated documentation</h2>

Some documentation blocks are generated from `project.json` and `compatibility.json`.

Generated blocks are delimited by comments such as:

```text
<!-- BEGIN:HEALTH_RESPONSE -->
<!-- END:HEALTH_RESPONSE -->
```

Do not edit generated blocks manually.

Use:

```bash
./scripts/ci/fix_all_docker.sh
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
- developer workflow improvements
- release automation improvements

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

Model files must be downloaded explicitly through:

```text
scripts/models/download_models.py
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
- docs/compatibility.md for compatibility and contract stability rules
- CHANGELOG.md for release history
