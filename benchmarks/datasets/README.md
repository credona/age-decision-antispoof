<h1>AntiSpoof Benchmark Datasets</h1>

<p>
This directory documents the expected local benchmark dataset format.
Real benchmark images are not committed to this repository.
</p>

<h2>Expected dataset structure</h2>

<pre>
benchmarks/datasets/&lt;dataset-name&gt;/
├── manifest.json
└── images/
    └── *.jpg
</pre>

<h2>manifest.json format</h2>

<pre>
[
  {
    "image_path": "images/example-real.jpg",
    "label": "real"
  },
  {
    "image_path": "images/example-spoof.jpg",
    "label": "spoof"
  }
]
</pre>

<h2>Supported labels</h2>

<ul>
  <li><b>real</b>: bona fide presentation.</li>
  <li><b>spoof</b>: attack presentation.</li>
</ul>

<h2>Privacy rules</h2>

<ul>
  <li>Do not commit images.</li>
  <li>Do not commit private calibration datasets.</li>
  <li>Do not commit raw benchmark payloads.</li>
  <li>Use external artifacts or the benchmark repository for reproducible manifests.</li>
</ul>
