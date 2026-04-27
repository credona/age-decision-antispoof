<h1>Age Decision AntiSpoof Models</h1>

This document lists the model and signals currently used by Age Decision AntiSpoof.

It is intentionally separated from the main README to keep model transparency visible without overloading the repository entry page.

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

<h3>Reference implementation family</h3>

```text
Silent-Face-Anti-Spoofing / MiniFASNet-style models
https://github.com/minivision-ai/Silent-Face-Anti-Spoofing
```

The local model file must be reviewed for its own origin, license, redistribution terms, and commercial usage constraints.

<hr>

<h2>Output handling</h2>

The model output is treated as a 3-class output.

```text
real_score = probability[1]
spoof_score = probability[0] + probability[2]
```

The current implementation fuses the model score with heuristic signals.

<hr>

<h2>Heuristic signals</h2>

The service currently includes:

- texture heuristic
- screen pattern heuristic
- blur heuristic

These signals are not standalone proof of spoofing.

They are used as additional evidence in the final anti-spoof score.

<hr>

<h2>Score fields</h2>

<h3>confidence</h3>

Calibrated final score used to decide whether the image is real.

<h3>spoof_score</h3>

Model-derived probability-like score representing spoof likelihood.

<h3>cred_antispoof_score</h3>

Credona trust score for anti-spoofing evidence.

A higher value means the capture is more likely to be real.

<hr>

<h2>Limitations</h2>

Anti-spoofing is probabilistic.

The result should not be interpreted as:

- identity proof
- legal verification
- certified PAD compliance
- biometric authentication
- active liveness proof

Model behavior may vary depending on:

- screen quality
- print quality
- lighting
- camera sensor
- compression
- face pose
- motion absence
- dataset shift
- attack type

<hr>

<h2>Model transparency</h2>

Before redistribution or commercial use, verify:

- upstream model license
- model source
- dataset provenance
- intended use
- redistribution terms
- biometric and privacy obligations
