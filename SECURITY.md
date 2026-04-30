<h1>Security Policy</h1>

This document covers repository-specific security constraints for Age Decision AntiSpoof.

For ecosystem-wide policy and coordinated disclosure guidance, see:
https://github.com/credona/age-decision/blob/main/SECURITY.md

<hr>

<h2>Local security scope</h2>

Security reports in this repository may concern:

- AntiSpoof request validation
- `/check` contract leakage risks
- unsafe logging of image payloads
- model loading and runtime hardening issues
- benchmark route exposure outside intended environments

<hr>

<h2>Local privacy constraints</h2>

AntiSpoof should not:

- persist uploaded images by default
- expose raw model scores or logits publicly
- expose internal calibration or heuristic details publicly
- log raw image bytes or base64 payloads
- commit model binaries or secrets to Git
