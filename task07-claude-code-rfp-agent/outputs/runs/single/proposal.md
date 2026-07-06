% BTS-Synthetic Enterprise Data Platform — Proposal for Acme Corp
% Prepared for Sarah Chen (VP Procurement) and Marcus Webb (CDO), Acme Corp
% 2026-05-23

# Executive Summary

Acme Corp is retiring a patchwork of on-premises Teradata warehouses and ad-hoc
cloud analytics in favour of a single enterprise data platform that can carry
real-time IoT ingest, batch ETL, BI/reporting, self-service data engineering,
and future ML workloads — at 280 TB and growing ~12 TB/month, across EU and US
regions, inside a Microsoft/Azure-centric estate.

BTS-Synthetic proposes our **Enterprise tier lakehouse platform** as that
single system of record. In summary:

- **Functional fit is high.** Native Delta/Iceberg/Parquet lakehouse, a
  dedicated Power BI DirectQuery adapter (our most mature BI integration),
  real-time streaming ingest tested to 250K events/second (Acme's peak is
  80K/second), 80+ batch connectors, and per-table EU data residency pinning
  all map directly to the workloads and capabilities in Section 2 of your RFP.
- **One flagged gap, transparently priced:** our Enterprise SLA is 99.95%
  monthly uptime. 99.99% is available as a bespoke, multi-region active-active
  add-on. We have priced it explicitly rather than silently over-promising —
  see Commercial Proposal.
- **Commercial terms:** we are proposing a 30% strategic discount off list
  (our board-approved ceiling for a deal of this size and strategic value),
  fixed for the full 5-year horizon with no price escalator — a concession we
  are able to make specifically because Acme is willing to commit to a 3-year
  initial term with a 2-year renewal option.
- **We have won this exact profile before.** Initech Sensors (industrial IoT,
  real-time ingest, evaluating Microsoft Fabric) and Globex Manufacturing
  (industrial, evaluating Snowflake/Databricks) both chose BTS-Synthetic on a
  3-year total-cost-of-ownership basis. We expect the same dynamic here against
  Databricks, Snowflake, and Microsoft Fabric.
- **A small number of contractual terms in your draft (uncapped liability, an
  MFN clause, subprocessor veto rights, and an immediate-termination-on-any-SLA-miss
  right) fall outside terms our insurers and legal team can support as
  written.** We propose specific, workable counter-positions for each below
  rather than simply declining — see Commercial Proposal §3 and the attached
  internal risk memo is available on request.

We are confident this is a winnable, referenceable, multi-year strategic
account for both sides, and we look forward to a working session with Marcus
Webb's team to validate the technical fit against your live workload profile.

---

# Technical Proposal

## Architecture fit to Acme's requirements

| Acme requirement (RFP §2) | BTS-Synthetic capability | Fit |
| --- | --- | --- |
| Real-time ingest, ~40,000 IoT devices, peak 80,000 events/sec | Native Kafka/Kinesis streaming consumers, tested to 250K events/sec single-region | **Strong** |
| Batch ETL from 30+ internal sources | 80+ out-of-the-box connectors (SAP, Salesforce, NetSuite, common DBs); Debezium-compatible CDC | **Strong** |
| BI/reporting for ~600 analysts and executives | Certified Power BI integration with a dedicated DirectQuery adapter — our most mature BI integration | **Strong (non-negotiable requirement met directly)** |
| Self-service data prep for ~150 data engineers | Low-code self-service prep UI for analyst/engineer personas | **Strong** |
| ML pipelines for predictive maintenance (planned) | Model registry with versioning, offline/online feature store, native autoscaling model serving, bring-your-own-model (HF/Anthropic/OpenAI) | **Strong — ready when Acme is** |
| ~280 TB current volume, ~12 TB/month growth | Well within platform scale envelope; decoupled compute/storage scales independently | **Strong** |
| Multi-region: primary EU, secondary US East | Multi-region deployment on Azure (and multi-cloud if ever needed) | **Strong** |
| EU data residency | Per-table residency enforcement — EU tables pinned to EU regions | **Strong** |
| Lakehouse architecture preferred | Core architecture — not bolted on | **Strong** |
| Open formats: Parquet, Delta, Iceberg | Native support for all three, portable, no proprietary lock-in | **Strong** |
| 99.99% monthly uptime (RFP §4.3) | Enterprise tier ships at 99.95%. 99.99% is available as a custom multi-region active-active add-on. | **Partial — priced gap, see Commercial Proposal** |

**Honest assessment of the one gap:** BTS-Synthetic's standard Enterprise SLA
is 99.95% monthly uptime. Reaching 99.99% requires a bespoke active-active
multi-region architecture, which we can deliver, but which is priced as an
add-on rather than baked silently into the base price — every vendor bidding
this RFP faces the same physics here, and we would rather be transparent about
it now than have it surface as a change order later.

## Governance & compliance

- Unity-style catalog across tables, models, and dashboards.
- Row- and column-level security with attribute-based access control.
- Full audit logging of every read/write, exportable to Acme's SIEM.
- Built-in PII detection and masking.
- SOC 2 Type II, ISO 27001, GDPR-aligned (DPA available), HIPAA-eligible.

## Implementation plan and milestones

Given Acme's scale (280 TB, 30+ sources, legacy Teradata decommission through
2027) and multi-region footprint, we scope this as a **large, multi-region,
multi-source migration**:

| Phase | Duration | Milestone |
| --- | --- | --- |
| 1. Discovery & architecture validation | Weeks 1–4 | Source system inventory, EU/US region design, security/residency sign-off |
| 2. Foundation build | Weeks 5–10 | Lakehouse provisioned (EU primary, US East secondary), governance/catalog live, Power BI DirectQuery connectivity validated |
| 3. First production workload | Weeks 8–12 (parallel) | First batch ETL source(s) and a subset of IoT ingest live in production — our typical "first production workload" milestone |
| 4. Phased source & workload migration | Weeks 12–20 | Remaining 30+ batch sources migrated; full 80K events/sec real-time ingest validated at peak |
| 5. Full cutover from Teradata | Weeks 20–24 | Legacy Teradata warehouses fully decommissioned per Acme's 2027 timeline; 600 analysts/executives and 150 data engineers fully onboarded |
| 6. ML enablement (optional, phase 2) | Post go-live | Feature store and model registry stood up ahead of predictive-maintenance pipelines |

This is consistent with our typical **24-week timeline for very large,
multi-region, multi-source customers**, well ahead of Acme's 2026-06-30 award
target allowing implementation to begin promptly, and comfortably inside the
2027 Teradata decommission deadline.

## Customer references (similar scale, Power BI, Azure)

1. **Initech Sensors** (Industrial / IoT) — real-time ingest performance and
   governance maturity were the deciding factors against Microsoft Fabric;
   comparable IoT/industrial profile to Acme.
2. **Globex Manufacturing** (Industrial / Manufacturing) — won on a 3-year TCO
   comparison against Snowflake and Databricks at a heavy, real workload
   profile; directly comparable industry.
3. **Wayne Manufacturing** (Industrial) — started via a 90-day PoC and signed
   a reference-customer agreement; a template we would propose for Acme's own
   validation phase if helpful ahead of full commitment.

*(Formal reference calls to be arranged directly between Acme and named
customer contacts, subject to those customers' standard reference process.)*

## Capability Matrix attachment

Per RFP §7, the completed Capability Matrix attachment accompanies this
proposal as a separate document.

---

# Commercial Proposal

## 1. Pricing — full 5-year transparency

Acme's scale (unlimited ingest/users required, 280 TB, 80K events/sec peak,
600+ analysts, 150 engineers) places this at our **Enterprise tier**, the only
tier we recommend for deals of this size.

| Component | Annual list price |
| --- | --- |
| Enterprise base (unlimited ingest, unlimited users, 24/7 support, 99.95% SLA, dedicated CSM) | $720,000 |
| Optional: 99.99% SLA add-on (bespoke multi-region active-active architecture) | +$100,000 (indicative; $80K–$120K band) |
| **Total annual list (with 99.99% SLA add-on)** | **$820,000** |

**Discount:** RFP §3.3 requests no less than 35% off list. Our published
discount bands cap at **25% standard / 30% strategic** for deals over $1M/year.
We are approving the **30% strategic discount** — our ceiling — on the
strength of: (a) a 3-year committed initial term, (b) Acme's fit as a named
reference account in our target industrial/IoT vertical, and (c) competitive
displacement of Databricks/Snowflake/Microsoft Fabric. We are not able to go
to 35%; see the counter-position below.

| | List | At 30% strategic discount |
| --- | --- | --- |
| Annual (base only, 99.95% SLA) | $720,000 | **$504,000** |
| Annual (with 99.99% SLA add-on) | $820,000 | **$574,000** |

**5-year fixed pricing, no escalators** (per RFP §3.1): we can commit to this
— years 1–3 initial term and the 2-year renewal option — **at the base 99.95%
SLA figure of $504,000/year, fixed, $2,520,000 over 5 years**, or
**$574,000/year fixed, $2,870,000 over 5 years** if the 99.99% SLA add-on is
selected. In exchange for holding price flat across the full horizon with no
CPI escalator, we ask for a standard **year-end volume true-up with a 10%
buffer** above committed volume (no true-up owed unless usage exceeds the
buffer) — this simply protects both sides against a step-change in usage that
neither of us can price today.

> **Counter-position on the 35% discount ask:** 30% is the top of our approved
> band for deals of this size; 35% is below our cost-to-serve at this scale
> once support, infrastructure, and account management are factored in. We
> would rather hold a sustainable 30% and over-deliver on TCO and reference
> value than commit to a number we can't stand behind for five years.

## 2. Payment terms

RFP §3.2 requests annual-in-advance billing, Net 90. We can do annual in
advance; **Net 90 is outside terms our finance team can extend**. We propose
**Net 60**, which we extend to Fortune-500-scale customers with strong credit
— a bracket Acme (~$1.4B revenue) qualifies for.

## 3. Contractual terms — our counter-positions

Acme's draft terms (RFP §4) contain several items that conflict with
positions our legal and insurance teams hold firm on. We flag each with
severity and a specific counter — full detail is in the internal risk
memo (not for customer distribution); the customer-facing summary is below.

| RFP term | Our position |
| --- | --- |
| §3.4 Most-Favoured-Nation pricing warranty | We do not offer MFN terms to any customer, at any deal size — this is a firm no across our entire customer base, not specific to Acme. |
| §4.1 Uncapped liability for data breach, incl. indemnification for regulatory fines | We propose liability capped at **24 months of fees paid**, with mutual carve-outs for gross negligence and IP infringement — our standard structure, and the maximum our cyber policy will support. |
| §4.2 Audit without notice, up to 4x/year, vendor pays | We propose **one audit per year included, with 30 days' notice**; additional audits available at Acme's cost with the same notice period. Unannounced audits are not something any of our customers, including regulated ones, require of us today. |
| §4.3 99.99% uptime with immediate termination on any SLA miss and full monthly refund | We propose our standard **99.95% SLA (99.99% available as the priced add-on above)**, with service credits up to 30% of the affected month's fees as the sole remedy for an SLA miss, and termination rights reserved for repeated or material breach rather than any single miss. |
| §4.4 All work product vests in Acme on creation | We propose our standard model: **Acme's data is always Acme's**; custom configurations/integrations we build are **licensed to Acme, not assigned** — with a broad, perpetual licence-back of any derivative work, the same structure we used successfully with a comparable large industrial customer. |
| §4.5 Prior written consent for any subprocessor, withholdable at Acme's sole discretion | We propose our standard **30-day advance notice with a right to object**; if Acme objects we will substitute the subprocessor or, if we cannot, Acme may terminate the affected service without penalty. |
| §3.5 Termination at any time, with or without cause, on 30 days' notice | We propose **mutual termination for convenience on 90 days' notice** (or we can meet closer to Acme's ask at 60 days as a negotiated midpoint), with fees refunded pro-rata for the unused period. |

None of these counter-positions are unusual asks on our side — they reflect
terms we hold across our customer base, including comparably large accounts,
and we're glad to walk Acme's legal team through the reasoning on a call.

---

*This proposal is commercial-in-confidence between BTS-Synthetic and Acme
Corp. Prepared 2026-05-23 in response to the RFP issued 2026-05-12
(response due 2026-05-26).*
