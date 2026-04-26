<h1>Age Decision AntiSpoof Roadmap</h1>

This document tracks the public roadmap of Age Decision AntiSpoof.

<h2>Versioning Strategy</h2>

Age Decision AntiSpoof follows semantic versioning:

```text
vX.Y.Z
```

Meaning:

- `X` changes for major architectural or detection paradigm changes
- `Y` changes for feature releases
- `Z` changes for patches, automation, documentation, CI, distribution, and maintenance

Examples:

```text
v1.0.1 -> automation and distribution patch
v1.1.0 -> improved spoof detection features
v2.0.0 -> video and active liveness milestone
```

<h2>Roadmap</h2>

<h3>v1.0.0 - Credona Initial Public Release</h3>

- [x] Migrate repository to Credona
- [x] Provide clean open source snapshot
- [x] Add Apache License 2.0
- [x] Add FastAPI service
- [x] Add ONNX anti-spoofing model integration
- [x] Add MiniFASNetV2 inference
- [x] Add 3-class output handling
- [x] Add binary real / spoof decision
- [x] Add texture heuristic
- [x] Add screen pattern heuristic
- [x] Add blur detection
- [x] Add multi-signal fusion
- [x] Add configurable threshold
- [x] Add configurable weights
- [x] Add structured responses
- [x] Add structured JSON logs
- [x] Add request_id support
- [x] Add correlation_id support
- [x] Add privacy-first metadata
- [x] Add spoof_score exposure
- [x] Add cred_antispoof_score
- [x] Add confidence calibration
- [x] Add benchmark dataset structure
- [x] Add benchmark dataset downloader
- [x] Add APCER / BPCER / ACER metrics
- [x] Add threshold tuning
- [x] Add /benchmark endpoint
- [x] Add integration tests with real images
- [x] Add README documentation

<h3>v1.0.1 - Automation and Distribution</h3>

- [x] Add GitHub Actions CI
- [x] Add automated tests on pull requests
- [x] Add Docker image build
- [x] Add automated release workflow
- [x] Add automated tag-based release notes
- [x] Publish Docker image (GHCR)
- [x] Add CodeQL scanning
- [x] Add Dependabot configuration
- [x] Add production Dockerfile
- [x] Embed model files in Docker image
- [x] Add `.dockerignore`
- [x] Add `.env.example.dev`
- [x] Remove APP_NAME and APP_VERSION from runtime environment
- [x] Add single source of truth for application version
- [x] Add README badges
- [x] Align repository structure with core

<h3>v1.x - Benchmark and Detection Improvements</h3>

- [ ] Add larger benchmark validation datasets
- [ ] Separate calibration and validation datasets
- [ ] Improve threshold tuning strategy
- [ ] Add safety-oriented threshold recommendation
- [ ] Export benchmark reports (JSON / Markdown)
- [ ] Add CI benchmark job
- [ ] Add stricter MIME type validation
- [ ] Add image size constraints
- [ ] Add spoof score distribution analysis
- [ ] Improve heuristic weighting strategy

<h3>v2 - Video and Active Liveness</h3>

- [ ] Add video-based liveness detection
- [ ] Add temporal consistency checks
- [ ] Add blink detection
- [ ] Add head movement detection
- [ ] Add replay attack detection
- [ ] Add challenge-response liveness

<h3>v3 - Trust, Privacy and Proof</h3>

- [ ] Add stronger privacy-first guarantees
- [ ] Add signed verification result prototype
- [ ] Add reusable Credona score envelope
- [ ] Add ZK-ready result structure
- [ ] Add proof-friendly metadata
- [ ] Add verifiable anti-spoof claim format
- [ ] Add external verification example