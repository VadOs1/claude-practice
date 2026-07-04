# Technical Fit Specialist — carry-forward memory

Patterns and reasoning to reuse across RFP evaluations (not deal-specific numbers).

## Recurring gap: uptime SLA tier
- Our standard Enterprise tier is 99.95% monthly uptime. Any RFP demanding
  99.99%+ requires the custom add-on (bespoke multi-region active-active
  architecture, meaningful annual premium). Treat any "four nines or higher"
  requirement as an automatic "partial fit" flag, not a full fit — even
  though it's technically achievable, it changes architecture, cost, and
  timeline, and often collides with aggressive contractual SLA-failure
  remedies (e.g. "any SLA miss = immediate termination + full refund").
  This is usually the single highest-leverage risk to surface to the
  coordinator, since it sits at the intersection of technical fit,
  pricing, and legal — flag it prominently even though the underlying
  capability exists as an add-on.

## Recurring strength: core lakehouse/ingest/BI stack
- Our streaming ingest (tested to 250K events/sec single-region), 80+
  batch connectors, Power BI DirectQuery adapter, and open-format
  lakehouse (Delta/Iceberg/Parquet) comfortably cover typical industrial
  IoT / manufacturing RFP profiles (tens of thousands of devices, tens of
  thousands of events/sec, hundreds of BI users, dozens of source
  systems). Don't over-hedge on these — they're genuinely full fits when
  scale is in this range. Reserve "partial fit" language for cases that
  approach or exceed the 250K events/sec ceiling, need single-region
  capacity near/above it, or need sub-100ms query latency (we run
  ~250ms-1s on streaming queries — flag as partial if RFP specifies
  sub-100ms).

## Migration timeline heuristic
- Use the three published bands (8 wks first workload / 16 wks full legacy
  warehouse migration / 24 wks very large multi-region multi-source) as
  starting anchors, but for combined scenarios (large scale + multi-region
  + legacy warehouse decommission all at once) push toward the upper band
  (24-36 wks for full cutover) rather than picking the single closest
  bucket — these factors compound rather than average out. Always compare
  the resulting timeline against the customer's stated legacy
  decommission deadline and flag if it's tight, not just "feasible."

## ML pipelines for "planned, not active" use cases
- When ML capability is requested for a future/planned use case (e.g.
  predictive maintenance not yet in production), assess against the
  platform's ML primitives (model registry, feature store, model serving)
  as a full fit if those primitives exist — don't downgrade to partial
  just because the customer hasn't operationalized the use case yet. The
  fit assessment is about platform capability, not customer readiness.

## Data residency / multi-region
- Per-table residency pinning + multi-region-per-cloud deployment is a
  full fit for "primary region A, secondary region B, residency enforced
  for region A" requirements as long as both regions are within the same
  supported cloud (e.g. both Azure regions). Don't confuse this with data
  residency across clouds, which we don't cover well — check the RFP's
  cloud provider is singular before calling this a full fit.
