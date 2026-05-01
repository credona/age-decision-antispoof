<h1>Status contract (Age Decision AntiSpoof)</h1>

Public metadata and subsystem readiness endpoints for AntiSpoof. They intentionally exclude per-request spoof scores (those appear only on authenticated success payloads from <strong><code>POST /check</code></strong>), raw logits, biometric confidence dumps, heuristic vectors, undisclosed internals, profiling streams, downstream captures, stack traces.

<hr>

<h2>GET /health</h2>

Stable keys validated by contracts:

<ul>
  <li><strong>status</strong> (<code>ok</code>),</li>
  <li><strong>service</strong> slug from project metadata,</li>
  <li><strong>version</strong> semver,</li>
  <li><strong>contract_version</strong>.</li>
</ul>

<hr>

<h2>GET /version</h2>

Emits serialized <code>ProjectMetadata</code>:

<ul>
  <li><strong>service_name</strong>, <strong>app_name</strong>, <strong>version</strong>, <strong>contract_version</strong>,</li>
  <li><strong>repository</strong>, <strong>image</strong>.</li>
</ul>

<hr>

<h2>GET /model/status</h2>

Top-level envelope per contract assertions:

<ul>
  <li><strong>service</strong> provider slug,</li>
  <li><strong>version</strong> / <strong>contract_version</strong>,</li>
  <li><strong>antispoof_model</strong> structured metadata describing loader state,</li>
  <li><strong>heuristics</strong> string list,</li>
  <li><strong>threshold</strong> aggregated decision cutoff advertised for deployments,</li>
  <li><strong>weights</strong> coarse blend factors (<code>model</code>, <code>texture</code>, <code>screen</code>).</li>
</ul>

This endpoint answers readiness and coarse configuration transparency—it does **not** return per-upload scores, ONNX tensor dumps for arbitrary inputs, heuristic activation traces, latent embeddings, profiling timestamps, upstream HTTP transcripts, verbose calibration tables beyond the documented keys.

<hr>

<h2><code>contract_version</code> behavior</h2>

The string reflects the contracted JSON schema generation shipped with tagged releases of this artifact. Coordinating services should correlate it via published compatibility matrices rather than inferring unpublished fields beneath the stabilized top-level envelopes.
