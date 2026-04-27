<h1>Age Decision AntiSpoof Benchmarks</h1>

This document describes benchmark expectations for Age Decision AntiSpoof.

Benchmark results should be reproducible and separated from product claims.

<hr>

<h2>Benchmark endpoint</h2>

```bash
curl -i http://localhost:8001/benchmark
```

The endpoint evaluates the local benchmark dataset when available.

<hr>

<h2>Benchmark dataset</h2>

The repository includes a local dataset structure under:

```text
benchmarks/datasets/
```

Real benchmark images should not be treated as product assets.

Dataset licenses and usage rights must be verified before redistribution or commercial use.

<hr>

<h2>Download benchmark dataset</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-antispoof python scripts/download_benchmark_dataset.py --limit 200
```

Expected local structure:

```text
benchmarks/datasets/celeba_spoof/
├── README.md
├── labels.csv
└── images/
```

<hr>

<h2>Metrics</h2>

<h3>APCER</h3>

Attack Presentation Classification Error Rate.

It measures spoof attacks incorrectly classified as real.

<h3>BPCER</h3>

Bona Fide Presentation Classification Error Rate.

It measures real captures incorrectly classified as spoof.

<h3>ACER</h3>

Average Classification Error Rate.

```text
ACER = (APCER + BPCER) / 2
```

<hr>

<h2>Threshold tuning</h2>

The benchmark service can compute a threshold recommendation.

A threshold optimized for ACER is not always the safest threshold.

For safety-oriented deployments, APCER must be reviewed separately.

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

Benchmark reports should include:

```text
date
runtime
model path
dataset name
dataset size
threshold
APCER
BPCER
ACER
recommended threshold
known limitations
```
