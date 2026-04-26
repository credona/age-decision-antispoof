<h1>Age Decision AntiSpoof Roadmap</h1>

This roadmap tracks the technical evolution of the Age Decision AntiSpoof service.

<hr>

<h2>v1.0.0 - Credona Initial Public Release</h2>

- [x] Migrate repository to Credona
- [x] Provide clean open source snapshot
- [x] Add Apache License 2.0
- [x] Add FastAPI service
- [x] Add local Docker development setup
- [x] Add ONNX model integration
- [x] Add MiniFASNetV2 inference
- [x] Add softmax probability normalization
- [x] Add 3-class model handling
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
- [x] Add X-Request-ID support
- [x] Add X-Correlation-ID support
- [x] Add custom exceptions
- [x] Add PEP 561 typing support
- [x] Add privacy metadata
- [x] Add spoof_score exposure
- [x] Add cred_antispoof_score exposure
- [x] Add confidence calibration layer
- [x] Add benchmark dataset structure
- [x] Add real benchmark dataset downloader
- [x] Add APCER metric
- [x] Add BPCER metric
- [x] Add ACER metric
- [x] Add threshold tuning
- [x] Add /benchmark endpoint
- [x] Add benchmark metrics in structured logs
- [x] Add integration tests with real sample images
- [x] Add model status with file path and existence check
- [x] Add stricter invalid image handling
- [x] Add README documentation

<hr>

<h2>v1.0.1 - Automation and Distribution</h2>

- [ ] Add GitHub Actions CI
- [ ] Add automated tests on pull requests
- [ ] Add Docker image build
- [ ] Add automated release workflow
- [ ] Add automated tag-based release notes
- [ ] Publish Docker image
- [ ] Add CodeQL scanning
- [ ] Add Dependabot configuration

<hr>

<h2>v1.x - Benchmark and Validation Improvements</h2>

- [ ] Add larger benchmark validation
- [ ] Separate calibration and validation datasets
- [ ] Add configurable threshold tuning strategy
- [ ] Add safety-oriented threshold recommendation
- [ ] Export benchmark report as JSON
- [ ] Export benchmark report as Markdown
- [ ] Add CI benchmark job with local or artifact-based datasets
- [ ] Add stricter MIME type validation
- [ ] Add image size limits
- [ ] Add benchmark score distribution report

<hr>

<h2>v2 - Video and Active Liveness</h2>

- [ ] Add video-based liveness detection
- [ ] Add temporal consistency checks
- [ ] Add blink detection
- [ ] Add head movement detection
- [ ] Add replay attack detection on short video
- [ ] Add challenge-response liveness checks

<hr>

<h2>Future evaluation</h2>

- [ ] Add ISO/IEC 30107-3 inspired reporting
- [ ] Add NIST-style evaluation notes
- [ ] Add adversarial robustness testing
- [ ] Add hardware-specific tuning
- [ ] Add dataset bias analysis
- [ ] Add privacy review documentation

<hr>

<h2>Future privacy and trust</h2>

- [ ] Add stronger privacy-first documentation
- [ ] Add signed verification result prototype
- [ ] Add reusable Credona score envelope
- [ ] Add ZK-ready result architecture
- [ ] Add proof-friendly score metadata