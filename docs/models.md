<h1>Age Decision AntiSpoof Models</h1>

This document lists the model and signals currently used by Age Decision AntiSpoof.

<hr>

<h2>Model lifecycle policy</h2>

Runtime configuration uses model identifiers as the public operational reference.

Low-level model paths are internal implementation details.

A model entry must define:

<pre>
model_id
model_version
task
runtime
scoring_policy_id
reproducibility metadata
</pre>

<hr>

<h2>Configured model identifier</h2>

<pre>
model_id: credona.antispoof.minifasnet-v2.v1
model_version: 1.0.0
task: presentation_attack_detection
runtime: onnx
scoring_policy_id: credona.antispoof.fusion-threshold.v1
</pre>

<hr>

<h2>Model binary policy</h2>

Model binaries are not intended to be committed to Git.

Model binaries are not intended to be embedded in the public Docker image.

Download explicitly:

<pre>
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/models/download_models.py
</pre>

<hr>

<h2>Anti-spoofing model</h2>

<h3>Model</h3>

<pre>
MiniFASNetV2.onnx
</pre>

<h3>Source</h3>

<pre>
https://github.com/yakhyo/face-anti-spoofing
</pre>

<h3>License note</h3>

The upstream project is distributed under Apache 2.0.

Verify license and dataset provenance before redistribution.

<hr>

<h2>Output handling</h2>

The model output is treated as a 3-class output.

<pre>
real_probability = probability[1]
spoof_probability = probability[0] + probability[2]
</pre>

Raw probabilities are internal and must not be exposed publicly.

<hr>

<h2>Heuristic signals</h2>

- texture heuristic
- screen pattern heuristic
- blur heuristic

Heuristic details remain internal.

<hr>

<h2>Model transparency</h2>

Before redistribution or commercial use, verify:

- upstream license
- dataset provenance
- intended use
- redistribution terms
