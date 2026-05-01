# Age Decision AntiSpoof Architecture

## Scope

This document describes the internal architecture of the AntiSpoof service.

The public API contract is frozen for v2.4.0. Internal refactoring must not add, remove or rename public response fields.

## Layers

antispoof/
  api/
  application/
  domain/
  infrastructure/
  models/

## API layer

antispoof/api contains FastAPI routing, request parsing, error mapping and public response filtering.

antispoof/api/response_filter.py is the public contract barrier. Internal scores, heuristic details, raw model values and thresholds must not leak through the public API response.

## Application layer

antispoof/application contains use cases, DTOs and ports.

It receives framework-neutral input data and delegates anti-spoofing execution to the pipeline.

## Domain layer

antispoof/domain contains pure PAD logic:

- calibration
- heuristics
- metrics
- privacy metadata
- result objects

## Infrastructure layer

antispoof/infrastructure contains technical adapters:

- ONNX model loading
- OpenCV image preprocessing
- Age Decision Core integration
- safe logging

## Model artifacts

antispoof/models contains runtime model artifacts.

Model binaries are runtime assets, not domain code.

## Contract rule

Only fields explicitly allowed by the public response filter may be returned by the API.
