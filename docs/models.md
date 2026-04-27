<h1>Age Decision AntiSpoof Models</h1>

This document lists the model and signals currently used by Age Decision AntiSpoof.

<hr>

<h2>Model binary policy</h2>

Model binaries are not intended to be committed to Git.

Model binaries are not intended to be embedded in the public Docker image.

Download explicitly:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_models.py
```

<hr>

<h2>Anti-spoofing model</h2>

<h3>Model</h3>

```text
MiniFASNetV2.onnx
```

Expected path:

```text
antispoof/models/MiniFASNetV2.onnx
```

<h3>Source</h3>

```text
https://github.com/yakhyo/face-anti-spoofing
```

<h3>License note</h3>

The upstream project is distributed under Apache 2.0.

Verify license and dataset provenance before redistribution.

<hr>

<h2>Output handling</h2>

The model output is treated as a 3-class output.

```text
real_score = probability[1]
spoof_score = probability[0] + probability[2]
```

<hr>

<h2>Heuristic signals</h2>

- texture heuristic
- screen pattern heuristic
- blur heuristic

<hr>

<h2>Model transparency</h2>

Before redistribution or commercial use, verify:

- upstream license
- dataset provenance
- intended use
- redistribution terms
