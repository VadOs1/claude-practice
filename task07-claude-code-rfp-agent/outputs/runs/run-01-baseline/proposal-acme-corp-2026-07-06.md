# Proposal for Acme Corp Enterprise Data Platform

**Prepared for:** Sarah Chen, VP Procurement / Marcus Webb, Chief Data Officer — Acme Corp
**Prepared by:** BTS-Synthetic
**Date:** 2026-07-06
**In response to:** RFP issued 2026-05-12, response due 2026-05-26

---

## 1. Executive Summary

Acme Corp is replacing a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics with a single enterprise data platform that can carry real-time IoT ingest, batch ETL, BI for 600 analysts, self-service prep for 150 data engineers, and a future predictive-maintenance ML program — all on a Microsoft/Azure-centric stack with EU/US data residency.

BTS-Synthetic proposes our Enterprise-tier Lakehouse platform, deployed multi-region (EU primary, US East secondary), built on open formats (Delta, Iceberg, Parquet) so Acme is never locked into a proprietary table format. We are the only bidder that combines a purpose-built, DirectQuery-certified Power BI integration with real-time streaming ingest tested well beyond Acme's peak load, and a governance model that enforces EU data residency at the table level.

We can meet Acme's functional and technical requirements in full. On commercial terms, we are close on most points and are transparent about the two or three places — most notably the 35% discount floor and uncapped liability — where we need to negotiate rather than simply accept, and we explain why. Section 6 (Risks & Mitigations) lays these out plainly.

**Headline commercial offer:** $720,000 effective annual fee (28% off a $1,000,000 list price), fixed with no escalators across the full 5-year horizon (3-year initial term + 2-year renewal), annual in advance, Net 60.

We believe BTS-Synthetic is the lowest-execution-risk path off Teradata for a company of Acme's profile, and we would welcome the chance to validate that with a scoped proof-of-concept ahead of contract signature.

---

## 2. Our Understanding of Acme's Needs

Acme is a $1.4B industrial IoT and sensor manufacturer running 18 countries' worth of operations on a Microsoft/Azure stack, currently constrained by an aging on-premises Teradata estate being decommissioned through 2027. The RFP describes five concurrent workloads that the new platform must support without compromise:

- **Real-time ingest** from ~40,000 field IoT devices, peaking at 80,000 events/second.
- **Batch ETL** from 30+ internal systems.
- **BI and reporting** for ~600 analysts and executives, with Power BI as a non-negotiable, native integration.
- **Self-service data preparation** for ~150 data engineers.
- **Machine learning pipelines** for predictive maintenance — planned, not yet active, but architecturally important to plan for now.

Scale requirements are significant but well inside modern lakehouse norms: ~280TB current volume, ~12TB/month growth, and multi-region deployment (EU primary, US East secondary) with a hard requirement that EU customer data never leaves the EU. Acme has also been explicit that it wants open file formats (Parquet, Delta, Iceberg) specifically to avoid the kind of vendor lock-in that made the Teradata migration necessary in the first place.

Commercially, Acme is running a disciplined, procurement-led process: a 14-day RFP window, evaluation weighted 30% functional fit / 25% commercial terms / 20% five-year TCO / 15% implementation risk / 10% vendor stability and references, and a named field of competitors (Databricks, Snowflake, Microsoft Fabric, and one unnamed regional vendor). The commercial and contractual asks — 35%+ discount, 5-year price certainty, Net 90 payment, MFN pricing, uncapped breach liability, and unrestricted audit rights — read as an aggressive, well-informed procurement position, not an oversight. We've treated them as such rather than assuming they're negotiable by default.

---

## 3. Why BTS-Synthetic Is the Right Fit

### 3.1 Functional and technical fit

| Requirement | Our capability | Fit |
|---|---|---|
| Real-time ingest, 80K events/sec peak | Native Kafka/Kinesis streaming, tested to 250K events/sec single-region | Strong — 3x headroom over peak |
| Batch ETL, 30+ sources | 80+ out-of-the-box connectors (Salesforce, SAP, NetSuite, common DBs) | Strong |
| Native Power BI, 600 users | Dedicated DirectQuery adapter — our most mature BI integration | Strong — a genuine differentiator |
| Self-service prep, 150 engineers | Low-code data prep UI for analyst/engineer personas | Strong |
| ML pipelines for predictive maintenance | Model registry, feature store (offline + online), autoscaling model serving, bring-your-own-model | Strong — ready when the program activates |
| Lakehouse, open formats | Delta, Iceberg, Parquet natively; compute decoupled from storage | Strong |
| Multi-region EU + US East, EU residency | Multi-cloud, multi-region; per-table residency pinning | Strong |
| 280TB volume, 12TB/month growth | Well within platform limits; SQL is sub-second on warmed caches up to 10TB — typical hot-data BI queries stay in this range, with cooler historical data served at standard lakehouse query latency | Good fit, with one honest caveat below |
| 99.99% uptime | Available as a custom multi-region active-active add-on (our Enterprise base is 99.95%) | Achievable, priced as an add-on (see Section 4) |

**One caveat we'd rather flag than gloss over:** our sub-second SQL guarantee applies to warmed caches up to 10TB. Acme's 280TB estate is comfortably supported by the platform overall, but if the majority of analyst queries routinely scan the full historical volume rather than recent/hot data, we'd want to validate query patterns during a PoC and potentially tune caching or partitioning strategy. This is a solvable design question, not a capability gap.

### 3.2 Competitive positioning

Acme is also evaluating Databricks, Snowflake, and Microsoft Fabric — all three signals are present in this RFP (lakehouse/open-format language, heavy analyst/SQL emphasis, and a Microsoft-shop/Power BI-first stance), so we assume all three are genuinely in contention alongside the unnamed regional vendor.

- **vs. Databricks** — Databricks will pitch ML/AI breadth and Spark-native lakehouse performance, and we won't out-engineer them there. Our angle is total cost of ownership: Databricks compute spend typically ramps faster than customers expect at Acme's scale, and our BI/analyst tooling — the workload serving 600 of Acme's users — is more mature than theirs. We've won this matchup before (Globex Manufacturing) on a 3-year TCO comparison run against the customer's actual workload profile; we'd propose the same exercise here.
- **vs. Snowflake** — Snowflake's analyst experience is excellent and we won't claim to beat it on day one. Our angle is workload breadth: Snowflake's story is comparatively thin for real-time, semi-structured, and ML-native workloads, all of which are explicitly in Acme's scope. We displaced Snowflake at Globex on exactly this basis.
- **vs. Microsoft Fabric** — This is the matchup that matters most given Acme's Azure-first posture. Fabric will look "free" bundled into an E5 license, and Fabric owns the Power BI relationship — we won't contest that. Our angle is honest TCO (bundled licensing rarely stays free once implementation and consulting hours are counted) and platform maturity: we've been running lakehouse workloads in production for 8 years, Fabric for under 2. We won Initech Sensors — a very similar industrial IoT profile to Acme — directly against a Microsoft Fabric "free with E5" pitch, on real-time ingest performance and governance maturity Fabric couldn't match.

**Bottom line:** our best opening move is a head-to-head 3-year TCO model built on Acme's actual workload numbers (280TB, 80K events/sec, 600 BI seats), not a list-price comparison — that is where we have beaten this exact field of competitors before.

### 3.3 Relevant track record

Three reference-quality deals map closely to Acme's profile:

- **Initech Sensors** (Industrial/IoT, $420K/year, Net 60, 15% discount) — closest analog to Acme. Won against Microsoft Fabric on real-time ingest and governance.
- **Globex Manufacturing** (Industrial, $580K/year, 18% discount) — won a Snowflake/Databricks bake-off on 3-year TCO with a heavy unstructured-data profile.
- **Stark Industries** (regulated/defence, $1.1M/year, 28% discount, 5-year term) — closest analog on deal size and IP posture; Stark also demanded full IP assignment and we resolved it with a license-back model, described in Section 5 below.

---

## 4. Commercial Proposal

### 4.1 Pricing (5-year transparency, as requested)

| Component | Annual list |
|---|---|
| Enterprise tier (unlimited ingest/users, 24/7 support, dedicated CSM) | $720,000 |
| 99.99% uptime add-on (multi-region active-active architecture) | $100,000 |
| Scale & governance premium (40K-device ingest fleet, 600 BI seats, 150 engineer seats, EU/US per-table residency enforcement) | $180,000 |
| **Total annual list price** | **$1,000,000** |

| Term | Discount | Effective annual fee | Total for period |
|---|---|---|---|
| Years 1–3 (initial term) | 28% | $720,000 | $2,160,000 |
| Years 4–5 (renewal option) | 28% (same rate, fixed at signature) | $720,000 | $1,440,000 |
| **Full 5-year horizon** | | | **$3,600,000** |

This pricing is fixed at signature for the full five-year horizon with **no escalators**, as requested, and includes a 10% volume true-up buffer at year-end so Acme is not exposed to overage charges for normal growth within that band.

**On the 35% discount floor:** we cannot get to 35% off list. Our standard discount ceiling for a deal this size (>$1M list, multi-year committed term) is 25%, and we are proposing 28% as a strategic exception that requires VP Sales approval — already in motion given Acme's scale and reference potential. Getting further than 28-30% would mean cutting into margin in a way we don't believe is sustainable, and pricing history suggests customers who forced us below that band (e.g., Pied Piper Data) were also the ones we ultimately lost or should have walked away from. We'd rather be direct about this now and win the deal on 5-year TCO — which is 20% of the evaluation weighting — than overpromise on the discount line and underdeliver on service quality later.

### 4.2 Payment terms

We propose **annual in advance, Net 60** — a concession from our Net 30 standard reflecting Acme's scale and credit profile, but short of the requested Net 90. Net 90 on annual invoices creates a working-capital gap we're not able to absorb at this contract size; Net 60 is the maximum extension we can offer without additional pricing adjustment.

### 4.3 Most Favoured Nation

We are not able to offer an MFN warranty. This is a firm position across all our enterprise contracts, not something specific to Acme: our pricing reflects negotiated volume, term, and configuration for each customer, and an MFN clause would require us to track and reconcile pricing across our entire customer base indefinitely, which is operationally unworkable and would raise costs for everyone, Acme included. In place of MFN, we're glad to share the discount-banding logic in Section 4.1 so Acme can see how this offer was constructed relative to deals of comparable size and term.

---

## 5. Contract Approach

Acme's draft terms are, in several places, more aggressive than our standard paper. Rather than silently accept terms we can't actually stand behind operationally, here is where we align and where we propose a counter-position:

| Area | Acme's ask | Our position |
|---|---|---|
| Liability for data breach | Uncapped, full indemnification | Capped at 24 months of fees paid, with carve-outs for gross negligence, willful misconduct, and IP infringement (uncapped for those carve-outs) |
| Regulatory fine indemnification | Uncapped | Same 24-month cap structure as above |
| IP ownership | All work product vests in Acme | Platform IP stays ours; Acme owns its data; custom configurations/integrations/reports built for Acme are licensed to Acme for their internal use — the same license-back model Stark Industries accepted in a comparable negotiation |
| Audit rights | Unannounced, up to 4x/year, vendor pays | 30 days' notice, 2 audits/year included at no cost, additional audits customer-funded; we audit our own subprocessors rather than granting direct access to them |
| Termination for convenience | Any time, 30 days' notice, no fees | We propose 90 days' notice (standard) with a fallback to 60 days if needed to close; no penalty fees either way — full alignment on the "no early termination fee" principle |
| SLA remedy | 99.99% uptime; any SLA miss triggers immediate termination + full refund | We commit to 99.99% (multi-region active-active, priced in Section 4.1); remedy for a miss is service credit up to 30% of that month's fees, not unilateral termination — termination stays available only for a sustained, material pattern of misses |
| Subprocessors | Prior written consent required, may be withheld at will | Public subprocessor list maintained; 30 days' advance notice before adding a new one; Acme may object, triggering substitution or a termination right — the same model we run for every enterprise customer |

Full reasoning and severity ratings for each of these are in the internal risk assessment; we're summarizing our position here so Acme's legal and procurement teams see it early rather than in a redline exchange after signature.

---

## 6. Risks & Mitigations

| Risk | Our mitigation |
|---|---|
| **Discount gap** (Acme wants 35%+, we're offering 28%, ceiling 30%) | Anchor the conversation on 5-year TCO (20% of evaluation weight) rather than headline discount; offer a scoped PoC to build confidence ahead of final pricing conversations |
| **Uncapped liability / indemnification exposure** | Firm 24-month cap with carve-outs — consistent with our insurance coverage; we've closed comparable deals (Stark Industries) with equivalent terms |
| **IP assignment demand** | License-back model in place of full assignment; precedent exists (Stark Industries) |
| **99.99% SLA is outside our standard tier** | Priced explicitly as a multi-region active-active add-on rather than silently over-promised; architecture already required for EU/US residency split, so incremental cost is contained |
| **Query performance on cold/historical data beyond the 10TB warm-cache guarantee** | Recommend validating actual query patterns during a PoC; tune partitioning/caching before go-live if needed |
| **Migration risk off Teradata by 2027 deadline** | Phased plan (Section 3.3/7): 8 weeks to first production workload, 16 weeks for full legacy warehouse migration — comfortably inside Acme's 2027 decommission window |
| **Net 90 payment ask vs. our working-capital constraints** | Net 60 offered as the maximum extension; can revisit if Acme is open to alternative structuring (e.g., quarterly billing at the same effective rate) |
| **Competitive pressure from Fabric's "free with E5" narrative** | Lead with independently-verified TCO model, not list-price comparison; this is the same play that beat Fabric at Initech Sensors |

---

## 7. Implementation Plan (High-Level)

| Milestone | Timeline |
|---|---|
| Contract signature | Target 2026-06-30 (per RFP) |
| Environment provisioning, EU/US multi-region setup, security/compliance sign-off | Weeks 1–4 |
| First production workload live (subset of IoT ingest + initial BI dashboards) | Week 8 |
| Full batch ETL cutover (30+ sources) | Weeks 9–14 |
| Full legacy Teradata migration complete | Week 16 |
| Predictive maintenance ML pipeline enablement (when Acme activates the program) | Post-migration, on request |

This timeline is consistent with our typical delivery pattern for customers of Acme's scale and complexity, and lands well ahead of the 2027 Teradata decommission deadline.

---

## 8. References

Available on request, consistent with the RFP's requirement for three customer references of similar scale with Power BI and Azure in their stack:

- Initech Sensors (Industrial/IoT — closest profile match)
- Globex Manufacturing (Industrial)
- A third reference to be confirmed based on Acme's preferred vertical focus

---

*BTS-Synthetic — prepared in response to Acme Corp RFP, issued 2026-05-12.*
