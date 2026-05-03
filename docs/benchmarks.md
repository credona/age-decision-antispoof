<h1>Age Decision AntiSpoof Benchmarks</h1>

This document describes benchmark expectations for Age Decision AntiSpoof.

Benchmark results must be reproducible and tied to explicit model identifiers.

<hr>

<h2>Benchmark endpoint</h2>

<pre>
curl -i http://localhost:8001/benchmark
</pre>

The endpoint evaluates the local benchmark dataset when available.

<hr>

<h2>Benchmark dataset</h2>

The repository includes a local dataset structure under:

<pre>
benchmarks/datasets/
</pre>

Dataset licenses and usage rights must be verified before redistribution or commercial use.

<hr>

<h2>Metrics</h2>

<h3>APCER</h3>

Attack Presentation Classification Error Rate.

<h3>BPCER</h3>

Bona Fide Presentation Classification Error Rate.

<h3>ACER</h3>

<pre>
ACER = (APCER + BPCER) / 2
</pre>

<hr>

<h2>Model reproducibility requirements</h2>

Every benchmark MUST specify:

<pre>
model_id
model_version
scoring_policy_id
runtime
execution provider
dataset name
dataset size
</pre>

Low-level model paths must not be used as reference identifiers.

<hr>

<h2>What the benchmark does not prove</h2>

The current benchmark does not prove:

- certified PAD compliance
- resistance to all spoof attacks
- production reliability
- demographic fairness
- video liveness quality
- active liveness quality

<hr>

<h2>Reporting format</h2>

<pre>
date
model_id
model_version
scoring_policy_id
dataset name
dataset size
APCER
BPCER
ACER
known limitations
</pre>
