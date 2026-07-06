# BTS-Synthetic Enterprise Data Platform
## Proposal for Acme Corp

**Prepared for:** Sarah Chen, VP Procurement / Marcus Webb, Chief Data Officer
**Prepared by:** BTS-Synthetic Deal Desk
**Date:** 2026-05-24
**In response to:** RFP issued 2026-05-12, response due 2026-05-26

---

## 1. Executive Summary

Acme Corp is replacing a patchwork of on-premises Teradata warehouses and ad-hoc
cloud analytics with a single enterprise data platform that can serve 40,000
field IoT devices, 30+ batch sources, 600 BI users, and 150 data engineers —
today on Azure, with predictable growth toward machine-learning-driven
predictive maintenance.

BTS-Synthetic proposes our **Enterprise tier Lakehouse platform** as the
platform of record for this program. We are an especially strong fit for
Acme's profile for three reasons:

1. **Power BI is our most mature BI integration** — we ship a dedicated
   DirectQuery adapter, directly satisfying your non-negotiable requirement
   for 600 analysts and executives.
2. **We have already run this exact profile.** Initech Sensors — an
   industrial IoT manufacturer of comparable scale — is a live BTS-Synthetic
   customer today, selected over Microsoft Fabric specifically for real-time
   ingest performance and governance maturity.
3. **Open, portable, and residency-aware by design.** Native Delta/Iceberg/
   Parquet support and per-table EU data residency enforcement directly meet
   your lakehouse and EU-data-stays-in-EU requirements without custom
   engineering.

We are also transparent about the one area where our fit is "strong with an
add-on" rather than "native": our standard Enterprise SLA is 99.95% monthly
uptime. We can commit to your requested 99.99% as a paid, architected add-on
(multi-region active-active) — details in Section 4.

On commercial terms, we want to be direct with you now rather than at
contract redline: the RFP's ≥35% discount, Net 90 payment, and zero-escalator
5-year fixed pricing sit outside our standard and strategic discount bands.
Section 4 sets out where we can move, how far, and why — anchored in
comparable industrial/IoT deals we've closed at your scale.

---

## 2. Technical Proposal

### 2.1 Requirements fit summary

| Requirement | BTS-Synthetic capability | Fit |
| --- | --- | --- |
| Real-time ingest, ~40,000 IoT devices, peak 80,000 events/sec | Native Kafka/Kinesis streaming consumers, tested to 250,000 events/sec single-region | **Strong** |
| Batch ETL from 30+ internal sources | 80+ out-of-the-box connectors (Salesforce, SAP, NetSuite, common databases) + Debezium-compatible CDC | **Strong** |
| BI/reporting for ~600 analysts and executives | Certified Power BI integration with dedicated DirectQuery adapter (our most mature BI integration) | **Strong — meets non-negotiable requirement** |
| Self-service data prep for ~150 data engineers | Low-code data prep UI for analyst/engineer personas | **Strong** |
| ML pipelines for predictive maintenance (planned) | Model registry with versioning, offline/online feature store, native autoscaling model serving | **Strong, future-ready** |
| ~280 TB current volume, ~12 TB/month growth | Decoupled compute/storage lakehouse; sub-second SQL on warmed caches up to 10TB, scales horizontally beyond that | **Strong** |
| Multi-region (primary EU, secondary US East) | Multi-cloud, multi-region within cloud; deployable on Azure | **Strong** |
| EU data residency | Per-table residency enforcement; EU tables pinned to EU regions | **Strong — meets non-negotiable requirement** |
| Lakehouse architecture, open formats (Parquet, Delta, Iceberg) | Native support for all three, no proprietary lock-in format | **Strong** |
| 99.99% monthly uptime | 99.95% standard on Enterprise tier; 99.99% available as a bespoke multi-region active-active add-on | **Add-on required — see Section 4** |

**Overall technical fit: HIGH**, with one clearly-scoped add-on (SLA tier) and
no functional gaps against your stated workloads.

### 2.2 Architecture approach for Acme

- **Primary region: EU** (hosting EU manufacturing/customer data under
  residency pinning). **Secondary region: US East**, active for US-sourced
  workloads and DR.
- **Ingest layer:** streaming consumers sized for your 80,000 events/sec peak
  (well within our validated 250,000 events/sec ceiling), plus scheduled
  batch pipelines for your 30+ internal systems and the Teradata sunset.
- **Governance:** row/column-level access control, full read/write audit
  logging exportable to your SIEM, and built-in PII detection — relevant
  given your global footprint across 18 countries.
- **ML readiness:** feature store and model registry provisioned in Phase 2,
  ahead of your predictive-maintenance program, so no re-platforming is
  needed when that workload goes live.

### 2.3 Competitive context

We understand Acme is also evaluating Databricks, Snowflake, and Microsoft
Fabric. Briefly, on why we believe BTS-Synthetic is the stronger fit for your
specific profile:

- **vs. Microsoft Fabric:** Fabric's headline appeal is "free with your E5
  license" and native Azure tenancy. We recommend evaluating the *fully
  loaded* 3-year TCO including Microsoft consulting hours, not just license
  cost — and weighing platform maturity (BTS-Synthetic: 8 years in
  production; Fabric: under 2). We match Fabric's Power BI depth without
  locking you into a single cloud.
- **vs. Databricks:** Databricks' Lakehouse/Delta story is strong for
  engineering-heavy workloads, but total cost of ownership tends to surprise
  customers as compute spend ramps, and analyst-facing BI tooling is less
  mature than ours. We're happy to run a side-by-side 3-year TCO model at
  your projected volumes.
- **vs. Snowflake:** Snowflake's analyst experience is excellent, but its
  architecture is less suited to your real-time, high-volume IoT ingest
  requirement and its ML story is bolted on rather than native.

**Our recommended proof point:** a 3-year TCO comparison run against your
actual projected workload (280TB base, 12TB/month growth, 80K events/sec
peak) — this is exactly how we won the comparable Globex Manufacturing and
Initech Sensors deals against this same competitive set.

---

## 3. Implementation Plan

Based on your scale (multi-region, multi-source, Teradata migration), we
recommend our **large-enterprise implementation track**:

| Milestone | Timeline | Notes |
| --- | --- | --- |
| Contract signature & kickoff | Week 0 | Joint governance model established |
| First production workload live | Week 8 | Typically one high-value batch or streaming source |
| EU region + residency controls validated | Week 12 | Gate before onboarding EU customer data |
| Core batch + streaming ingest at full scale | Week 16 | Matches our typical "full migration from a legacy warehouse" timeline |
| Power BI rollout to analyst population (600 users) | Week 18 | Phased by business unit |
| US East secondary region + DR validated | Week 20 | |
| Full multi-region, multi-source cutover; legacy Teradata sunset support | Week 24 | Aligned to your 2027 Teradata decommission window |
| ML/feature store provisioning (predictive maintenance readiness) | Week 24+ | Ahead of go-live, no re-platforming required |

We propose award by 2026-06-30 as requested, with kickoff the following week.

---

## 4. Commercial Proposal

### 4.1 Pricing structure

At Acme's scale (unlimited ingest/users, 24/7 support, dedicated CSM), the
**Enterprise tier** is the appropriate platform:

| Component | Annual list price |
| --- | --- |
| Enterprise base (unlimited ingest, unlimited users, 24/7 support, 99.95% SLA, dedicated CSM) | $720,000 |
| 99.99% SLA add-on (multi-region active-active architecture) | $100,000 |
| **Total annual list price** | **$820,000** |

**5-year total list value:** $4,100,000 (before discount).

### 4.2 Discount

The RFP requests a minimum 35% discount off list. Our standard discount
bands cap out at 20% (standard) / 25% (strategic sign-off) for deals in the
$500K–$1M annual range, and this deal qualifies for our strategic band on
every count: target vertical (industrial/IoT), a 3+ year committed term, and
strong reference-customer potential.

**We are proposing a 25% strategic discount** — $615,000/year on the base
platform, or **$3,075,000 across the 5-year horizon** including the SLA
add-on years — with VP Sales sign-off already in motion. We recognize this
is short of your 35% target, and we'd rather be candid about that gap now
than discover it at contract redline. Our best path to closing that gap is
the 3-year TCO comparison referenced in Section 2.3: on deals of this profile
(Globex Manufacturing, Initech Sensors), we've closed at 15–18% discount and
still won on projected TCO against Databricks/Snowflake/Fabric list pricing.
We're glad to walk your team through that model.

### 4.3 Term & pricing horizon

We can commit to **fixed unit pricing for the full 3-year initial term, no
escalator** — meeting your requirement for the initial term. For the 2-year
renewal option, we propose a capped escalator (CPI + 2%, capped at 5%/year)
consistent with our standard 3-year-term pricing policy, disclosed in full
now so there are no surprises at renewal. This gives you cost certainty for
the initial term and a known, bounded ceiling for the renewal — full 5-year
pricing transparency, as requested, without an open-ended commitment on our
side.

### 4.4 Payment terms

We propose **annual payment in advance, Net 60** (rather than the requested
Net 90). Net 60 is a concession we make for Fortune-500-scale customers with
strong credit, which we're glad to extend given Acme's ~$1.4B revenue and
global footprint.

### 4.5 Most-Favoured-Nation clause

We are not able to offer an MFN warranty. Our pricing is tailored to each
customer's specific workload profile, term, and volume commitments, and an
MFN clause would prevent us from offering any customer — including Acme in
future negotiations — deal-specific flexibility. We'd like to discuss
removing this clause; in its place we're happy to offer a volume true-up
mechanism (10% buffer above committed volume) so Acme's pricing stays
aligned to actual usage.

### 4.6 Other commercial terms

- **Termination:** We propose either party may terminate for convenience on
  90 days' written notice (standard), or 60 days if preferred, with fees
  pro-rated to the termination date and no penalty either way.
- **Liability:** We propose an aggregate liability cap of 24 months of fees
  paid, with uncapped carve-outs for gross negligence and IP infringement —
  this is the ceiling our cyber insurance policy supports and is consistent
  with caps we've agreed on comparably-sized programs.
- **Audit rights:** One audit per calendar year with 30 days' notice, at
  Acme's cost for any audits beyond the first — consistent with maintaining
  SOC 2 Type II / ISO 27001 certifications across our customer base.
- **Intellectual property:** Acme's data is Acme's, always. Custom
  configurations and integrations we build for Acme are licensed to Acme
  (not assigned) — mirroring the license-back model we agreed with Stark
  Industries, which let them retain full commercial use of derivative work
  without us losing the underlying IP we reuse across our platform.
- **Subprocessors:** We maintain a public subprocessor list with 30 days'
  advance notice of any change; Acme may object, triggering substitution or
  a termination right — rather than a blanket pre-approval requirement,
  which is more operationally workable for a platform at this scale.
- **Service levels:** 99.95% standard, service credits up to 30% of monthly
  fees as sole remedy; 99.99% available via the add-on in Section 4.1 with
  a mutually workable remedy structure (rather than immediate termination on
  any SLA miss).

We believe every position above is negotiable in good faith and none of them
should be a blocker to award — we'd like to work through them collaboratively
during the evaluation window.

---

## 5. Customer References

Three references matching Acme's profile (industrial/IoT vertical, Microsoft/
Azure-aligned environment, comparable or larger scale):

1. **Initech Sensors** — Industrial/IoT manufacturer, enterprise tier,
   selected BTS-Synthetic over Microsoft Fabric on real-time ingest
   performance and governance maturity. Closed 2025-11-22.
2. **Globex Manufacturing** — Industrial/manufacturing, enterprise tier,
   won against Snowflake and Databricks on a 3-year TCO comparison at a
   heavy-unstructured-data workload profile. Closed 2025-09-14.
3. **Stark Industries** — Large enterprise, 5-year term, sovereign deployment
   with a license-back IP model comparable to what we're proposing for
   Acme's custom work product. Closed 2026-02-10.

Full reference contacts available on request, subject to each customer's
reference agreement terms.

---

## 6. Capability Matrix

The completed BTS-Synthetic Capability Matrix is provided as a separate
attachment per the RFP's requested format.

---

## 7. Next Steps

We would welcome the opportunity to present this proposal to Sarah Chen and
Marcus Webb's teams before the 2026-05-26 response deadline, including a
live walkthrough of the 3-year TCO model referenced in Sections 2.3 and 4.2.

**Contact:** BTS-Synthetic Deal Desk
