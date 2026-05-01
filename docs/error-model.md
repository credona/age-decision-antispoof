<h1>Error model (Age Decision AntiSpoof)</h1>

Standard failures return one JSON envelope. Success responses on <strong><code>POST /check</code></strong> follow distinct schemas documented in compatibility material; errors never embed extra diagnostics beyond the constrained shape described here.

<hr>

<h2>ErrorResponse shape</h2>

```json
{
  "request_id": "...",
  "correlation_id": "...",
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

Identifiers resolve from inbound <strong>X-Request-ID</strong> / <strong>X-Correlation-ID</strong> headers; generated defaults apply when omitted.

<hr>

<h2>Endpoints using the envelope</h2>

<ul>
  <li><strong>POST /check</strong> — HTTP <strong>400</strong> for validation-domain or processing rejects; HTTP <strong>500</strong> for unexpected failures (OpenAPI advertises standardized models).</li>
  <li><strong>GET /benchmark</strong> — HTTP <strong>404</strong> when curated benchmark assets are unavailable; HTTP <strong>500</strong> for unexpected benchmark runtime faults.</li>
</ul>

Multipart validation misses are routed through the shared FastAPI validation handler documented below.

<hr>

<h2>Known error codes emitted here</h2>

<ul>
  <li><strong>missing_file</strong> — multipart <code>file</code> absent.</li>
  <li><strong>invalid_request</strong> — other validation mapping fallback after normalization.</li>
  <li><strong>empty_file</strong> — upload resolves to zero bytes prior to decoding.</li>
  <li><strong>invalid_image</strong> — bytes present but decoding fails.</li>
  <li><strong>antispoof_processing_error</strong> — pipeline-level <code>AntiSpoofError</code>; HTTP <strong>400</strong>.</li>
  <li><strong>internal_error</strong> — unchecked exception paths on <code>/check</code>; HTTP <strong>500</strong>; external message stays generic (<code>An internal error has occurred.</code>).</li>
  <li><strong>benchmark_dataset_unavailable</strong> — missing benchmark corpus; HTTP <strong>404</strong>.</li>
  <li><strong>benchmark_runtime_error</strong> — benchmark execution fault; HTTP <strong>500</strong>.</li>
</ul>

<hr>

<h2>Message policy</h2>

Most client-visible messages stay fixed short strings (<code>Invalid request.</code> where applicable). They intentionally omit stack traces, OpenCV internals, tensor dumps, heuristic vectors, calibrated thresholds unrelated to advertised fields, downstream bodies, latency breakdowns usable as covert channels.

<hr>

<h2>Forbidden fields</h2>

Top-level entries are limited to <strong>request_id</strong>, <strong>correlation_id</strong>, and <strong>error</strong> with nested <strong>code</strong> plus <strong>message</strong>. Additional keys—even popular framework structures such as chained <code>detail</code> arrays—violate privacy-first assertions enforced by repository contract tests until explicitly adopted and documented elsewhere.
