# BTS-Synthetic — Response to Acme Corp RFP: Enterprise Data Platform

**Prepared for:** Sarah Chen, VP Procurement; Marcus Webb, Chief Data Officer
**Prepared by:** BTS-Synthetic Deal Desk
**Date:** 2026-07-06
**RFP reference:** Enterprise Data Platform, issued 2026-05-12

## 1. Executive summary

Acme Corp is replacing a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics with a single enterprise data platform that must handle real-time IoT ingest at scale, serve 600 Power BI users natively, and operate across EU and US regions under EU data residency rules — all on a fixed 5-year price.

BTS-Synthetic is a strong technical match for this scope: our lakehouse architecture natively supports Parquet, Delta, and Iceberg; our Power BI integration (a dedicated DirectQuery adapter) is our most mature BI integration; and our streaming ingest is tested to 250K events/second — well above Acme's 80,000 events/second peak. We have a directly comparable win with **Initech Sensors**, an industrial IoT customer of similar profile, where we beat a Microsoft Fabric "free with E5" bid on real-time ingest performance and governance maturity.

Where we differ from the RFP as issued is commercial and contractual, not technical. A small number of terms — an uncapped liability/indemnification clause, no-notice audit rights, an SLA structure that ties any outage to immediate contract termination, full IP vesting, and a 35% minimum discount with a most-favoured-nation warranty — sit outside terms we or (to our knowledge) any enterprise vendor can respons­ibly accept as written. We address each with a specific counter-position below (Section 6) so Acme's evaluation team can assess our overall offer on a like-for-like basis with other bidders.

**Recommendation:** proceed to negotiation. Functional fit is high, the commercial gap is closable within our standard strategic-deal authority, and the contractual gaps are the kind we resolve routinely with enterprise customers of Acme's scale.

## 2. Our understanding of your need

- **Scale & workloads:** ~280 TB current volume growing ~12 TB/month, real-time ingest from ~40,000 IoT devices (peak 80,000 events/sec), batch ETL from 30+ sources, BI/reporting for ~600 analysts and executives, self-service prep for ~150 data engineers, and a planned (not yet active) ML program for predictive maintenance.
- **Architecture constraints:** Microsoft/Azure-centric environment today, legacy on-premises Teradata warehouses being decommissioned through 2027, lakehouse architecture and open file formats (Parquet, Delta, Iceberg) preferred for portability.
- **Geography:** primary EU, secondary US East, with a hard requirement that EU customer data remain in the EU.
- **Non-negotiable:** native Power BI integration for the existing 600-user base.
- **Commercial framing:** a 3-year initial term with a 2-year renewal option, 5-year pricing fixed at signature, minimum 35% off list, Net 90 payment, and a most-favoured-nation pricing warranty.
- **Contractual framing:** uncapped breach liability, unannounced audit rights up to 4x/year at vendor cost, a 99.99% SLA tied to immediate termination on any miss, full IP vesting, and subprocessor engagement gated on Acme's sole-discretion consent.
- **Competitive context:** Acme is also evaluating Databricks, Snowflake, Microsoft Fabric, and a regional vendor — evaluation is weighted 30% functional fit, 25% commercial terms, 20% five-year TCO, 15% implementation timeline/risk, 10% vendor stability/references.

## 3. Why we're the right fit

| Requirement | Fit | Notes |
|---|---|---|
| Lakehouse + open formats (Parquet, Delta, Iceberg) | **High** | Native support for all three; core architecture is a lakehouse by design. |
| Native Power BI integration (600 users) | **High** | Our most mature BI integration, with a dedicated DirectQuery adapter — this is the single strongest match in the RFP. |
| Real-time ingest, 40K devices / 80K events/sec peak | **High** | Streaming tested to 250K events/sec single-region; ~3x headroom over Acme's peak before multi-region distribution. |
| Multi-region (EU primary / US East secondary) + EU residency | **High** | Native multi-region deployment with per-table residency pinning — EU tables can be enforced to stay in EU regions at the data level, not just the deployment level. |
| Batch ETL, 30+ sources | **High** | 80+ connectors out of the box. |
| Legacy Teradata decommission by 2027 | **High** | Typical full legacy-warehouse migration timeline is 16 weeks — comfortably inside Acme's runway. |
| Self-service prep, 150 engineers | **High** | Low-code prep UI purpose-built for this persona. |
| ML pipelines for predictive maintenance (planned) | **Medium-High** | Model registry, feature store, and autoscaling model serving are all in place today; recommend scoping this as an explicit Phase 2 milestone rather than day-one scope, since Acme's own program is not yet active. |
| 99.99% monthly uptime | **Conditional** | See Section 5 (Contract approach) — technically achievable via a multi-region active-active add-on, but the remedy structure attached to it in the RFP needs to change. |

**Overall technical fit: High.** No requirement in the RFP is outside our platform's capability; the only open item is the commercial structure around the highest SLA tier.

### Competitive position

Acme is also evaluating Databricks, Snowflake, and Microsoft Fabric. Given Acme's deep Azure/Power BI footprint, Fabric is the most immediate competitive threat; Databricks and Snowflake compete more on data-engineering depth and analyst SQL experience respectively. We are not the incumbent on any of these fronts, so we lead with the arguments that hold up under scrutiny rather than compete point-for-point on turf we don't own:

- **Vs. Microsoft Fabric:** Fabric's Power BI integration is native and its E5-bundled pricing looks free on paper. We don't contest that. We instead put a transparent 5-year TCO on the table — including the migration, governance, and consulting costs that "free with E5" doesn't show — and lead with open-format portability: Acme keeps its data in Parquet/Delta/Iceberg, not locked to a single cloud's proprietary runtime. This is the same argument that won Initech Sensors against a comparable Fabric bid.
- **Vs. Databricks:** strong on data engineering and Delta Lake, less strong on interactive BI performance for 600 analyst users and on cost predictability at scale. We lead with responsive BI on open formats plus a fixed, predictable 5-year cost model against Databricks' usage-based compute ramp.
- **Vs. Snowflake:** excellent SQL/analyst experience, but built around a SQL-warehouse model rather than combined real-time IoT ingest, batch ETL, and unstructured data. We lead with workload breadth — one platform for streaming, batch, and BI — rather than three tools stitched together.

## 4. Commercial proposal

Acme's evaluation weights functional fit at 30% and total 5-year TCO at 20% — together, more than half the score rests on capability and true cost rather than headline discount. We've priced accordingly.

| Term | RFP ask | Our proposal |
|---|---|---|
| List price basis | — | Enterprise tier configured for Acme's scope (280TB, multi-region active-active for EU/US residency, 600 BI seats, 150 engineer seats): ~$900K–$950K annual list |
| Discount | ≥35% off list | **22–25% at signature**, with a path to **28–30%** (VP-approved strategic ceiling) if Acme commits to a public reference and the full 3+2 year structure |
| Term | 3-year initial + 2-year renewal, 5-year price fixed at signature, no escalators | Accepted, **conditional on final discount landing at or below ~28–30%**. Outside that band, we fix pricing for the 3-year initial term and apply a capped escalator (CPI+2%, max 5%/yr) on the 2-year renewal only, which itself remains a mutual (not unilateral) option |
| Payment | Annual in advance, Net 90 | Annual in advance accepted; **counter Net 60** (matches our closest comparable win, Initech Sensors, and Acme's investment-grade profile) |
| MFN pricing warranty | Pricing no less favourable than any comparable customer, for contract duration | **Not offered as a continuous warranty** — our discount structure reflects deal-specific scope and competitive context (see past deals ranging 10%–28% by profile), and a blanket MFN would force retroactive repricing against unrelated deals. We propose an annual benchmark review at renewal instead |

**Proof point:** our closest comparable deal, Initech Sensors (industrial IoT, similar scale), closed at 15% off list against a Microsoft Fabric "free with E5" bid, won on real-time ingest performance and governance maturity — the same combination Acme is evaluating. Our largest strategic discount to date, 28% (Stark Industries), came with a full 5-year fixed price and no escalator, which is the template we're proposing here if Acme's final discount lands in that range.

We want to be candid about one boundary: at a 35% discount with an MFN warranty, this deal would price below every comparable win in our history, including deals we ultimately walked away from rather than match (see: a 2025 opportunity where a competitor discounted to 40% to win a purely price-driven deal — we let that one go rather than erode our standard structure). We don't expect that outcome here, since Acme's own evaluation criteria weight capability and TCO over headline discount, but we want the trade-off visible up front rather than discovered at contract redlines.

## 5. Implementation plan

| Phase | Milestone | Timing |
|---|---|---|
| Phase 0 | Contract execution, kickoff, architecture validation for EU/US multi-region residency design | Weeks 1–2 |
| Phase 1 | First production workload live (batch ETL + BI for a pilot analyst group), core lakehouse stood up on Azure | By week 8 |
| Phase 2 | Full real-time IoT ingest onboarded (40K devices, ramping to 80K events/sec peak), remaining 30+ batch sources migrated | By week 16 |
| Phase 3 | Full cutover from Teradata, all 600 BI users and 150 data engineers onboarded, governance/audit logging validated | By week 20–24 |
| Phase 4 | Predictive maintenance ML pipeline stood up (model registry, feature store, serving) once Acme's ML program is active | Post-cutover, scoped jointly |

This timeline is inside Acme's stated 2027 Teradata decommission target with meaningful buffer, and aligns to the RFP's award date of 2026-06-30 (noting the response and award dates in the original RFP have since passed as of this proposal's preparation; timeline above is anchored to contract execution date, whenever that occurs).

## 6. Contract approach

Five terms in the RFP's Section 4 are outside standard enterprise contract terms for us (and, in our experience, for any vendor able to responsibly underwrite them). We flag these clearly rather than accept silently or bury them in redlines:

| RFP term | Our position | Counter-proposal |
|---|---|---|
| **Uncapped liability + full indemnification** for any breach, including regulatory fines and reputational damages (4.1) | Not acceptable as written — voids standard cyber insurance coverage, and reputational/regulatory-fine indemnification is uninsurable | Liability capped at 24 months of fees paid, carve-outs for IP infringement and gross negligence; indemnification covers direct breach-response costs (notification, forensics, credit monitoring), excluding regulatory fines and reputational damages |
| **Audit rights** without notice, up to 4x/year, vendor pays (4.2) | Not acceptable as written — operationally unworkable at scale | One audit/year, 30 days' notice, under NDA; up to 2 additional audits/year available at Acme's cost |
| **99.99% SLA, any-duration failure triggers immediate termination + full monthly refund** (4.3) | 99.99% is achievable via a multi-region active-active architecture (which our EU/US residency design already points toward), at a $80K–$120K/year premium — but tying it to instant termination on any blip, regardless of cause or duration, is not a workable remedy structure | Standard commitment: 99.95% monthly uptime with tiered service credits (up to 30% of monthly fees) as sole remedy; termination reserved for chronic failure (3+ consecutive months missed). 99.99% available as a priced add-on with the same credit-based remedy, not termination-on-first-incident |
| **Full IP vesting** of all custom development, configurations, and integrations to Acme (4.4) | Not acceptable as written | Acme retains full rights to its own data; custom reports, dashboards, and configurations built for Acme are licensed to Acme perpetually, royalty-free, for internal use. BTS-Synthetic retains ownership of the underlying platform, connectors, and reusable IP |
| **Subprocessor engagement** requires Acme's prior consent, withholdable at sole discretion (4.5) | Not acceptable as written — no vendor can operate at scale under unilateral third-party veto over infrastructure choices | Public subprocessor list with 30 days' advance notice of any addition; Acme may object within that window, and we will propose a substitute or Acme may terminate the affected service without penalty |
| **Termination for convenience**, 30 days' notice, no fee (3.5) | Directionally acceptable — we do offer termination for convenience | 90 days' written notice (60 days if 90 is a hard blocker), pro-rated refund of prepaid, unused fees; no early-termination fee, consistent with the RFP's intent |

None of these are unusual asks from an enterprise customer, and all five are things we resolve routinely in contracts of this size — we raise them now, ahead of a redline cycle, so evaluation can proceed on a complete and accurate picture of our terms.

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| RFP's discount floor (35%) and MFN warranty exceed our standard and strategic pricing authority | Open at 22–25%, hold a 28–30% ceiling backed by a 5-year TCO case and a reference-customer agreement; be prepared to walk rather than match an unsustainable discount, consistent with our own pricing discipline on past deals |
| SLA remedy structure (any-duration failure → immediate termination + full refund) creates disproportionate risk relative to the $80K–$120K/year cost of the 99.99% architecture | Counter with credit-based remedies and a chronic-failure termination threshold (Section 6); do not price the 99.99% add-on until the remedy structure is resolved |
| Uncapped liability, unannounced audits, and full IP vesting represent unbounded operational/financial exposure if accepted as-is | Standard counter-positions in Section 6, escalated to legal sign-off before contract execution; none of these are unusual asks to negotiate with an enterprise customer at Acme's scale |
| 5-year fixed price with 12 TB/month growth could outpace the discount math by years 3–5 (~280TB → 1,000TB+ over the term) | Volume true-up mechanism with a defined buffer, revisited at each renewal; escalator on the 2-year renewal option if final discount falls outside the 28–30% strategic band |
| Microsoft Fabric's embedded position (Azure tenant, E5 bundling, native Power BI) is a real competitive risk given Acme's Microsoft-centric environment | Lead with transparent 5-year TCO (including Fabric's hidden migration/consulting costs) and open-format portability, the same combination that won the comparable Initech Sensors deal against a similar Fabric bid |
| Net 90 payment terms and unilateral 2-year renewal option shift cash-flow and commitment risk toward us | Counter Net 60; confirm renewal requires mutual agreement, not Acme's unilateral exercise |

---

*This proposal reflects BTS-Synthetic's standard commercial and legal positions for enterprise deals of this scale and is intended to open, not close, negotiation on the items in Section 6. A completed Capability Matrix accompanies this response under separate cover.*
