<h1>Deprecation policy (AntiSpoof public contract)</h1>

This document covers HTTP routes and stable JSON payloads published by the Age Decision AntiSpoof service. Organizational release planning stays in the central project repository.

<hr>

<h2>Versioning semantics</h2>

Documented URLs, multipart expectations, advertised success payloads, and error envelopes align with semver and <code>contract_version</code> metadata released from this repository.

<hr>

<h2>Deprecated artifacts before removal</h2>

If a documented field, endpoint, or error code disappears, changelog and repository docs retain guidance until removal ships alongside updated compatibility assertions.

<hr>

<h2>Majors, minors, and internal-only changes</h2>

Breaking changes observable to gateways and SDKs typically imply coordinated minor or major bumps per ecosystem compatibility rules. Helpers and internals that never appeared under tested public contracts may change when tests and documented surfaces remain stable.

<hr>

<h2>Privacy-first corrections</h2>

Unintended exposure of biometric-grade diagnostics, verbatim internal errors, heuristic vectors, undocumented raw model logits, downstream dumps, timing traces usable for inference fingerprinting, or stack content in responses must be fixed without a deprecation runway when severity demands it.
