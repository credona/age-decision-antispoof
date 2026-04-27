<h1>Changelog</h1>

This changelog tracks changes specific to Age Decision AntiSpoof.

Global project direction is tracked in the central Age Decision repository.

<hr>

<h2>1.2.1</h2>

- Documentation structure simplified.
- Repository README reduced to a concise entry point.
- Technical usage moved to docs/usage.md.
- Model transparency moved to docs/models.md.
- Benchmark methodology moved to docs/benchmarks.md.

<hr>

<h2>1.2.0</h2>

- Confirmed `cred_antispoof_score` as the public anti-spoof score field.
- Kept the response free from generic `cred_score`.
- Added stable error response schema.
- Added request tracing to error responses.
- Added OpenAPI contract tests.
- Added contract tests for `cred_antispoof_score`.
- Updated response documentation.

<hr>

<h2>1.1.1</h2>

- Updated dependency and CI maintenance items.
- Validated Docker runtime.
- Validated health endpoint.
- Validated model status endpoint.
- Validated check endpoint with a real image.

<hr>

<h2>1.1.0</h2>

- Upgraded Docker runtime to Python 3.14.
- Validated runtime compatibility.
- Validated downstream service compatibility.
- Validated health, readiness and verification flows.

<hr>

<h2>1.0.2</h2>

- Updated Python dependencies.
- Kept runtime compatible with ML dependencies.
- Validated Docker runtime and anti-spoof endpoint.

<hr>

<h2>1.0.1</h2>

- Added CI workflow.
- Added Docker image workflow.
- Added release workflow.
- Added CodeQL scanning.
- Added Dependabot configuration.
- Published Docker image.

<hr>

<h2>1.0.0</h2>

- Initial public release.
- Added FastAPI service.
- Added MiniFASNetV2 ONNX inference.
- Added texture, screen pattern and blur heuristics.
- Added multi-signal fusion.
- Added privacy metadata.
- Added structured logs.
- Added benchmark metrics.
- Added tests.
- Added Docker development setup.
