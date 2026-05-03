<h1>Age Decision AntiSpoof Scoring Methodology</h1>

This document defines the public scoring methodology used by Age Decision AntiSpoof.

<hr>

<h2>Public score</h2>

The public score is:

<pre>
cred_antispoof_score
</pre>

It is a normalized value in the interval:

<pre>
0.0 <= cred_antispoof_score <= 1.0
</pre>

A higher value means stronger evidence that the image is a bona fide presentation.

<hr>

<h2>Internal fusion model</h2>

The internal fusion score is computed from three normalized signals:

<pre>
model_real_score
texture_score
screen_score
</pre>

The deterministic fusion policy is:

<pre>
raw_final_score =
  model_weight * model_real_score
  + texture_weight * texture_score
  + screen_weight * (1.0 - screen_score)
</pre>

Default policy:

<pre>
scoring_policy_id: credona.antispoof.fusion-threshold.v1
model_weight: 0.70
texture_weight: 0.15
screen_weight: 0.15
calibration_method: clamp_v1
</pre>

<hr>

<h2>Calibration methodology</h2>

Current calibration is conservative:

<pre>
calibrated_score = clamp(raw_final_score, 0.0, 1.0)
</pre>

Therefore:

<pre>
cred_antispoof_score = calibrated_score
</pre>

This is intentionally simple and reproducible.

Future versions may replace clamp_v1 with dataset-based calibration such as:

- Platt scaling
- isotonic regression
- temperature scaling

Such changes must be versioned through scoring_policy_id.

<hr>

<h2>Privacy contract</h2>

Public responses must not expose:

- raw model scores
- raw logits
- spoof probability
- heuristic details
- internal threshold
- fusion weights
- calibration internals

Public responses may expose:

- decision
- is_real
- spoof_detected
- cred_antispoof_score
- privacy metadata
- safe engine metadata

<hr>

<h2>Limitations</h2>

cred_antispoof_score is not a certification result.

It does not prove resistance to all presentation attacks.

It must be interpreted as a probabilistic signal.
