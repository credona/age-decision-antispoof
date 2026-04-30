<h1>Compatibility</h1>

This document describes compatibility expectations for Age Decision AntiSpoof.

Age Decision AntiSpoof exposes the presentation attack detection contract used by downstream services such as the public API and SDK integrations.

For ecosystem-wide compatibility policy, see:
https://github.com/credona/age-decision/blob/main/COMPATIBILITY.md

<hr>

<h2>Scope</h2>

This document applies to the public behavior of this repository:

- HTTP endpoints
- request headers
- public response fields
- error response structure
- privacy metadata
- OpenAPI schema
- project metadata
- compatibility metadata

Internal implementation details are not stable unless explicitly documented.

<hr>

<h2>Stable public endpoints</h2>

```text
GET /health
GET /version
GET /model/status
POST /check
GET /benchmark
GET /openapi.json
```

The `/check` endpoint is the main anti-spoof decision endpoint.

The `/version` endpoint exposes project metadata from `project.json`.

The `/benchmark` endpoint is intended for local benchmark visibility and should not be treated as a public production verification endpoint.

<hr>

<h2>Project metadata</h2>

Project metadata is stored in:

```text
project.json
```

Generated view:

<!-- BEGIN:VERSION_RESPONSE -->
```json
{
  "service_name": "age-decision-antispoof",
  "app_name": "Age Decision AntiSpoof",
  "version": "2.2.3",
  "contract_version": "2.2",
  "repository": "https://github.com/credona/age-decision-antispoof",
  "image": "ghcr.io/credona/age-decision-antispoof"
}
```
<!-- END:VERSION_RESPONSE -->

The service name, application name, version and contract version must not be duplicated in environment files.

<hr>

<h2>Compatibility metadata</h2>

Compatibility metadata is stored in:

```text
compatibility.json
```

It is synchronized from `project.json`.

Generated view:

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-antispoof",
  "version": "2.2.3",
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

<h2>Stable public fields</h2>

The main `/check` response exposes:

```text
request_id
correlation_id
provider
decision
is_real
spoof_detected
cred_antispoof_score
rejection_reason
privacy
model_info
```

These fields should remain stable throughout the v2.x release line.

<hr>

<h2>Decision values</h2>

```text
real
spoof
```

These values represent a probabilistic anti-spoofing decision.

They do not represent certified liveness, identity proof, or legal proof.

<hr>

<h2>Score ownership</h2>

Age Decision AntiSpoof owns:

```text
cred_antispoof_score
```

AntiSpoof does not own:

```text
cred_decision_score
cred_global_score
```

Those fields belong to other repositories in the Age Decision ecosystem.

<hr>

<h2>Privacy-first contract</h2>

The public response must not expose:

```text
raw image content
raw model scores
raw logits
heuristic details
calibration details
internal threshold value
biometric embeddings
legacy cred_score alias
```

<hr>

<h2>Backward-compatible changes</h2>

The following changes are considered backward-compatible in v2.x:

- adding optional metadata fields
- adding internal logs without sensitive data
- improving validation messages without changing public error shape
- improving model loading behavior without changing response semantics
- adding tests
- adding documentation
- adding CI checks
- improving developer workflow scripts
- improving release automation

<hr>

<h2>Breaking changes</h2>

The following changes are considered breaking:

- removing a stable public field
- renaming a stable public field
- changing decision values
- exposing raw model scores
- exposing heuristic details
- exposing internal threshold values
- changing score ownership
- changing endpoint paths
- changing the public error response shape
- changing request header names without transition

Breaking changes should be reserved for a new major version.

<hr>

<h2>Deprecated fields</h2>

Age Decision AntiSpoof v2.x does not expose the legacy field:

```text
cred_score
```

New integrations must use:

```text
cred_antispoof_score
```

<hr>

<h2>Compatibility checks</h2>

Compatibility is checked through:

- unit contract tests
- OpenAPI contract tests
- privacy response tests
- project metadata checks
- compatibility metadata checks
- Docker metadata checks
- release tag checks
- generated documentation checks

Run all checks:

```bash
./scripts/ci/check_all_docker.sh
```

Auto-fix generated files and run checks:

```bash
./scripts/ci/fix_all_docker.sh
```

<hr>

<h2>Generated documentation</h2>

The following documentation blocks are generated from `project.json` and `compatibility.json`:

```text
HEALTH_RESPONSE
VERSION_RESPONSE
COMPATIBILITY_METADATA
```

Do not edit generated blocks manually.

Use:

```bash
./scripts/ci/fix_all_docker.sh
```

<hr>

<h2>Release checks</h2>

On tag release, CI verifies that the Git tag matches the version declared in `project.json`.

Example:

```text
project.json version: 2.2.1
expected Git tag: v2.2.1
```

A mismatched tag must fail the release workflow.

<hr>

<h2>Integrator guidance</h2>

Integrators should rely on:

- documented response fields
- documented decision values
- `/version`
- `compatibility.json`
- OpenAPI schema
- changelog entries
- release tags

Integrators should not rely on:

- internal model outputs
- internal logs
- private Python classes
- undocumented metadata
- local development-only behavior
