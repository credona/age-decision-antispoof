<h1>Age Decision AntiSpoof</h1>

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/ci.yml?branch=main&label=CI" alt="CI">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/docker.yml?branch=main&label=Docker" alt="Docker">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-antispoof/codeql.yml?branch=main&label=CodeQL" alt="CodeQL">
  <img src="https://img.shields.io/github/v/release/credona/age-decision-antispoof" alt="Release">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License">
</p>

Age Decision AntiSpoof is the presentation attack detection service of the Age Decision ecosystem.

<h2>Responsibility</h2>

This repository owns still-image presentation attack detection and anti-spoof score production.

<h2>Scope</h2>

It estimates whether a face image appears to be a real human capture or a spoof attempt.

It does not expose raw model scores, heuristic details, or internal calibration details through the public API.

It does not perform identity verification, face recognition, document verification, age estimation, or active liveness challenge.

Version 2.3.0 tightens public contract governance: stable status endpoint coverage, standardized error responses, normalized request validation errors including <code>missing_file</code> for missing multipart uploads, and enforced privacy-first forbidden-field rules for anti-spoof outputs.

<hr>

<h2>When to use this repository</h2>

- you need to detect spoof attempts (photo, screen, replay)
- you want to secure an age decision pipeline

<h2>When NOT to use this repository</h2>

- you need age estimation
- you need identity verification
- you need active liveness challenges

<hr>

<h2>Documentation</h2>

- Repository: https://github.com/credona/age-decision-antispoof
- Usage: docs/usage.md
- Models and third-party notes: docs/models.md
- Benchmarks: docs/benchmarks.md
- Compatibility: docs/compatibility.md
- Security: SECURITY.md
- Global architecture and ownership: https://github.com/credona/age-decision/blob/main/docs/architecture.md
- Global scoring model: https://github.com/credona/age-decision/blob/main/docs/scoring.md
- Changelog: CHANGELOG.md
- Contributing: CONTRIBUTING.md
- Global project: https://github.com/credona/age-decision

<hr>

<h2>Usage example</h2>

Run one anti-spoof decision request:

```bash
curl -X POST http://localhost:8001/check \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

<hr>

For setup, configuration, runtime options, Docker workflows, and full response details, see `docs/usage.md`.

<hr>

<h2>License</h2>

This repository is released under the Apache License 2.0.

Third-party models may have their own upstream license and constraints.

See docs/models.md for details.
