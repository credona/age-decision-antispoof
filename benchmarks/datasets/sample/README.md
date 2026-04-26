<h1>Sample Anti-Spoof Benchmark Dataset</h1>

<p>
This directory describes the expected benchmark dataset format for Age Decision AntiSpoof.
</p>

<h2>Purpose</h2>

<p>
This sample dataset folder is documentation-only.
It defines the CSV structure expected by the benchmark loader.
It does not contain real benchmark images.
</p>

<h2>CSV format</h2>

```csv
image_path,label
real/example-real.jpg,real
spoof/example-spoof.jpg,spoof
```

<h2>Expected directory structure</h2>

```text
sample/
├── labels.csv
├── real/
│   └── example-real.jpg
└── spoof/
    └── example-spoof.jpg
```

<h2>Supported labels</h2>

<ul>
  <li><b>real</b>: bona fide presentation.</li>
  <li><b>spoof</b>: attack presentation.</li>
</ul>

<h2>Notes</h2>

<p>
The image paths in labels.csv are examples.
Real images are intentionally not committed to this repository.
Benchmark datasets must be added locally or through CI artifacts according to their license.
</p>