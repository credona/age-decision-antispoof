<h1>CelebA-Spoof Local Benchmark Dataset</h1>

<p>
This directory is reserved for a local CelebA-Spoof-compatible benchmark subset.
</p>

<h2>Purpose</h2>

<p>
The dataset is used by integration tests to run anti-spoofing inference on real images.
The images are not committed to Git.
</p>

<h2>Download</h2>

```bash
python scripts/download_benchmark_dataset.py \
  --dataset celeba-spoof-hf \
  --output-dir benchmarks/datasets/celeba_spoof \
  --limit 20
```

<h2>Expected structure</h2>

```text
celeba_spoof/
├── README.md
├── manifest.json
└── images/
    ├── 000000_real.jpg
    ├── 000001_spoof.jpg
    └── ...
```

<h2>Manifest format</h2>

```json
[
  {
    "image_path": "images/000000_real.jpg",
    "label": "real"
  },
  {
    "image_path": "images/000001_spoof.jpg",
    "label": "spoof"
  }
]
```

<h2>Notes</h2>

<p>
Dataset licensing must be reviewed before commercial use or redistribution.
This repository only provides tooling to create a local benchmark subset.
</p>