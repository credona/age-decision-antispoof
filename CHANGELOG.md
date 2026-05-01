<h1>Changelog</h1>

This changelog tracks changes specific to Age Decision AntiSpoof.

Global project direction is tracked in the central Age Decision repository.

<h2>2.3.0</h2>

<ul>
  <li>Added stable public status contract regression coverage for <code>/health</code> and <code>/model/status</code>.</li>
  <li>Standardized the public error response model to expose only <code>request_id</code>, <code>correlation_id</code>, and <code>error</code>.</li>
  <li>Normalized request validation errors to the same public ErrorResponse contract.</li>
  <li>Mapped missing multipart file validation failures to <code>missing_file</code> with HTTP 400 and <code>Invalid request.</code>.</li>
  <li>Preserved privacy-first forbidden field guarantees for anti-spoof public outputs.</li>
</ul>

<hr>

<h2>2.2.3</h2>

<ul>
  <li>Enforced documentation boundaries between global and repository-specific docs.</li>
  <li>Removed cross-repository documentation duplication.</li>
  <li>Normalized repository <code>README.md</code> scope.</li>
  <li>Normalized <code>CONTRIBUTING.md</code> to local workflows.</li>
  <li>Normalized <code>SECURITY.md</code> and <code>COMPATIBILITY.md</code> scope.</li>
  <li>Enforced absolute GitHub links only for cross-repository documentation references.</li>
  <li>Centralized global documentation in <code>age-decision</code>.</li>
</ul>

<hr>

<h2>2.2.2</h2>

<ul>
  <li>Published Docker images from version tags only; pull request workflows no longer publish Docker images.</li>
  <li>Release workflow builds GitHub release description from the matching <code>CHANGELOG.md</code> section.</li>
  <li>Release workflow validates the Git tag matches <code>project.json</code> and that exactly one GHCR package version carries that tag.</li>
  <li>Added manual and scheduled workflow to delete untagged GHCR Docker package versions.</li>
</ul>

<hr>

<h2>2.2.1</h2>

<ul>
  <li>Introduced single source of truth configuration via project.json.</li>
  <li>Added dynamic environment generation for Docker (compose and runtime).</li>
  <li>Removed static .env usage in favor of generated configuration.</li>
  <li>Added Docker image metadata injection using build arguments.</li>
  <li>Added Docker metadata consistency validation.</li>
  <li>Added compatibility metadata auto-synchronization.</li>
  <li>Added automatic documentation synchronization checks.</li>
  <li>Added one-command auto-fix pipeline (fix_all_docker.sh).</li>
  <li>Added one-command CI-equivalent validation (check_all_docker.sh).</li>
  <li>Added pre-push validation hook aligned with CI.</li>
  <li>Added Docker-first local CI execution.</li>
</ul>

<hr>

<h2>2.2.0</h2>

<ul>
  <li>Added one-command local validation.</li>
  <li>Added one-command release preparation.</li>
  <li>Reorganized developer, CI, metadata, documentation, model, benchmark, and release scripts.</li>
  <li>Added automatic release tagging from project metadata after main CI success.</li>
  <li>Aligned release and Docker workflows with tag-triggered automation.</li>
</ul>
<hr>

<h2>2.1.0</h2>

- Added centralized project metadata through `project.json`.
- Added `antispoof/project.py` to load project metadata from a single source of truth.
- Added `/version` endpoint exposing service metadata, version, contract version, repository and image.
- Added `version` and `contract_version` fields to `/health`.
- Added `contract_version` to `/model/status`.
- Updated FastAPI metadata to use `project.json` for application title and version.
- Updated structured logs to use service name, version and contract version from project metadata.
- Kept `antispoof/version.py` as a backward-compatible metadata bridge.
- Added compatibility metadata through `compatibility.json`.
- Added version contract tests for `/health`, `/version`, project metadata and compatibility metadata.
- Added generated documentation blocks for health, version and compatibility examples.
- Added project, compatibility and release metadata validation scripts.
- Added generated documentation synchronization scripts.
- Added `docs/compatibility.md` for contract stability, versioning and compatibility rules.
- Added unified CI graph with quality, metadata, tests, contract compatibility and Docker runtime jobs.
- Added quality checks with Ruff linting, Ruff formatting and Python compilation.
- Added `requirements.dev.txt` for development and quality tooling.
- Added EditorConfig-based whitespace normalization.
- Added VS Code workspace settings for save-time formatting and whitespace cleanup and extension recommendations.
- Updated Docker ignore and Git ignore rules to align with metadata, documentation and model binary policy.
- Updated README, usage and contributing documentation for v2.1.0 metadata and compatibility rules.
- Made optional benchmark image integration test skip when image assets are not available locally.
- Reformatted Python source and tests with Ruff.

<hr>

<h2>2.0.0</h2>

- Clarified model binary policy.
- Removed ONNX model download from Docker build.
- Documented explicit model download requirement.
- Documented that Docker images should not embed model binaries.
- Updated README and usage documentation accordingly.
- Removed raw model scores from the public `/check` response.
- Removed `confidence`, `spoof_score`, `threshold`, and `details` from the public `/check` response.
- Kept internal diagnostic fields available in the Python result object.
- Documented the privacy-first public anti-spoof response contract.

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
