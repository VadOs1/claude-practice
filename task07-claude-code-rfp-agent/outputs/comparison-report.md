# RFP Processing — Three-Approach Comparison

**Deal:** Acme Corp — Enterprise Data Platform RFP
**Date:** 2026-07-01
**Approaches compared:** (1) Agent Team, (2) Single Agent (no delegation), (3) Dynamic Workflow (approximated)

All three runs processed the identical `synthetic-data/rfp-acme-corp.md` input and were expected to produce the same two deliverables: a customer-facing proposal (`.docx`) and an internal risk-assessment HTML dashboard, per `.claude/skills/risk-assessment/SKILL.md`.

> **Note on approach 3:** Claude Code's real "Dynamic Workflow" feature (where Claude writes a JS orchestration script to fan out subagents, invoked via `ultracode`/`/effort ultracode`) is not callable as a tool from within a session — there is no exposed tool for it. This run **approximates** the spirit of that architecture: a single coordinator agent that decides its own decomposition and wave structure at runtime, rather than following a fixed pre-scripted roster. Treat its numbers as directional, not a literal measurement of the built-in feature.

---

## 1. Architecture per approach

| | Agent Team | Single Agent | Dynamic Workflow (approx.) |
|---|---|---|---|
| Output folder | `outputs/` | `outputs-single-agent/` | `outputs-dynamic-workflow/` |
| Delegation | Fixed roster of 5 specialists (pricing, legal, technical-fit, competitive, risk-assessment), 4 run in parallel wave 1, risk-assessment run after synthesis | None — one agent does everything itself, sequentially | Coordinator dynamically chose 5 subagents across 2 waves: wave 1 = pricing/legal/technical-fit/competitive in parallel, wave 2 = risk-assessment (run after reviewing wave 1 and synthesizing the proposal itself) |
| Who writes the proposal | Top-level orchestrator, from the 4 specialist outputs | The single agent itself | The coordinator agent itself, from its 4 subagents' outputs |
| Adaptive re-planning | No — roster and waves were fixed in advance | N/A — no delegation to re-plan | Yes in principle — coordinator explicitly reviewed wave 1 before deciding wave 2, and judged no extra "wave 1.5" deep-dive was needed |
| Reliability during this session | Completed cleanly | Hit two transient `529 Overloaded` API errors, needed 2 manual retries | Hit two transient `529 Overloaded` API errors, needed 2 manual retries (unrelated to architecture — server-side outage window affected both concurrently) |

---

## 2. Token / cost comparison

Exact per-call token usage was only captured for the Agent Team run (from each subagent's returned usage metadata):

| Specialist | Tokens |
|---|---|
| Pricing | 30,300 |
| Legal | 25,959 |
| Technical Fit | 23,941 |
| Competitive | 20,004 |
| Risk Assessment | 51,431 |
| **Total (5 subagent calls)** | **151,635** |

The Single Agent and Dynamic Workflow runs did not surface per-call usage metadata in their returned reports, so exact figures aren't available here. Structurally, though, the ordering is predictable:

- **Single Agent is almost certainly the cheapest in raw tokens.** It reads the RFP and every skill/data file exactly once into one context. Agent Team and Dynamic Workflow each re-read the RFP (and several skills) independently inside 4–5 separate subagent contexts — that duplication is the single biggest cost driver in both multi-agent approaches. The tradeoff is that Single Agent's one context grows very large and is entirely serial, so wall-clock latency is higher per step even though total tokens are lower.
- **Dynamic Workflow ≥ Agent Team in raw tokens.** Same 5-way specialist split as Agent Team, but with an added full coordinator context on top (reads the RFP itself, reviews wave 1 outputs, authors the synthesis) — that's extra overhead the Agent Team's orchestrator also pays, but Dynamic Workflow's coordinator additionally reasons about *how* to decompose the work, which agent-team's fixed roster doesn't spend tokens on.
- **Parallelism:** Agent Team (4-way parallel wave) and Dynamic Workflow (4-way parallel wave 1, then 1 sequential wave 2) both finish faster in wall-clock than Single Agent's fully serial pass, at the cost of the token duplication above.

**Bottom line:** if raw token/dollar cost is the priority, Single Agent wins by a clear margin. If wall-clock latency and separation-of-concerns are the priority, both multi-agent approaches win, at a real token premium — with Agent Team's fixed roster being the leaner of the two multi-agent options since it skips the coordinator's own decomposition reasoning.

---

## 3. Risk assessment report — quality comparison (the key ask)

All three dashboards agree on the two numbers that matter most:

| | Agent Team | Single Agent | Dynamic Workflow |
|---|---|---|---|
| Gross risk (worst case) | 18.0% | 18.0% | 18.0% |
| Net risk (proposed position) | 8.0% | 8.0% | 8.0% |
| Decision | Escalate to VP | Escalate to VP | Escalate to VP |
| Revenue opportunity score | **85 / 100** | **100 / 100** | **100 / 100** |
| Clause cards in risk register | **10** | **12** | **12** |

Two real quality differences surfaced, both favoring the Single Agent and Dynamic Workflow outputs:

### a) Revenue score discrepancy — Agent Team under-scored by 15 points
The Agent Team's risk-assessment specialist withheld the "target vertical" +15 points, annotating the card: *"Target vertical (industrial/IoT) — not an official 2026 target vertical."* That reasoning conflates two different lists from two different skills:
- `pricing-playbook/SKILL.md` defines "target verticals" (financial services, life sciences, government) as a qualifier for the **strategic discount band**.
- `risk-assessment/SKILL.md`'s own revenue-signal table separately lists **"Target vertical (manufacturing, IoT, industrial)" → +15** — a different, risk-assessment-specific definition that Acme Corp (an "industrial IoT manufacturer") matches exactly.

Single Agent and Dynamic Workflow — working independently of each other — both read the risk-assessment skill correctly and awarded the full +15, landing on 100/100. This didn't change the final decision (revenue was ≥70 in all three cases, so the Escalate-to-VP threshold is unaffected either way), but it's a genuine reasoning error unique to the team run, and the kind of subtle skill-file cross-reference mistake that's easier to make when a subagent only has one skill file in context and has to reason about an adjacent skill's definitions from memory of the RFP alone.

### b) Clause granularity — Agent Team merged 4 distinct risk line items into 2
`risk-assessment/SKILL.md` defines 8 distinct legal-risk patterns as separate rows (each with its own base risk % and severity). The Agent Team's dashboard collapsed two pairs together:
- Merged "uncapped liability" (3.0%) + "uncapped regulatory-fine indemnity" (2.5%) into one **"Uncapped Liability & Indemnification" card at 5.5%**.
- Merged "immediate termination on any SLA miss" (2.0%) + "SLA > 99.95% demanded" (0.5%) into one **"99.99% Uptime, Immediate Termination on Any Miss" card at 2.5%**.

The aggregate math still nets out to the same 18.0% gross / 8.0% net, so the top-line numbers are unaffected — but the resulting dashboard has 10 toggle cards instead of the 12 the skill's clause taxonomy defines, which reduces per-clause transparency (e.g., a VP reviewing the dashboard can't independently toggle "regulatory fine indemnity" separately from "breach liability" to see its isolated contribution).

Single Agent and Dynamic Workflow both kept all 12 clauses as separate cards, matching the skill spec's taxonomy exactly. Dynamic Workflow's version additionally cites the specific RFP section for each clause (e.g., `§4.1`, `§4.3`), which neither of the other two dashboards does — a small but genuine traceability improvement.

**Conclusion on risk-assessment quality:** Single Agent and Dynamic Workflow produced more faithful, more granular, and more accurate dashboards than Agent Team on this run. This is likely incidental to this specific execution rather than a general property of the team architecture (the error was a reasoning slip in one subagent, not a structural limitation of delegation) — but it's a useful illustration that splitting a skill's own multi-step logic across a subagent with only partial context can introduce cross-referencing mistakes that a single agent holding the entire skill file in view is less prone to.

---

## 4. Proposal quality comparison

All three proposals cover the same six required sections (executive summary, understanding of need, why we're the right fit, commercial proposal, contract approach, risks/mitigation), but differ sharply in commercial specificity:

- **Agent Team's proposal (40 lines)** stays high-level and defers detail: *"Full pricing detail, discount structure, and payment terms will be presented in the accompanying commercial proposal and 5-year TCO model"* and *"we will bring forward alternative language in the redline"* — no concrete numbers in the document itself.
- **Single Agent's proposal (126 lines)** and **Dynamic Workflow's proposal (125 lines)** both commit to specific, checkable numbers: Enterprise tier at $720K list, 25% strategic discount → $540K/year, a priced ~$100K/year multi-region add-on to cover the 99.99% SLA ask, Net 90 countered to Net 30 (Net 60 as a concession), and a 3-year firm price with a CPI-capped (≤5%) renewal escalator instead of a flat 5-year freeze.

The Agent Team's brevity may be intentional given its stated framing as a "summary submission" with a fuller technical/commercial proposal to follow — but taken at face value, the other two documents are substantially more decision-ready and directly usable by a sales rep in a live negotiation.

---

## 5. Output artifacts

| File | Agent Team | Single Agent | Dynamic Workflow |
|---|---|---|---|
| `proposal-*.md` | 5.4 KB / 40 lines | 11.7 KB / 126 lines | 11.3 KB / 125 lines |
| `proposal-*.docx` | 13.5 KB | 17.2 KB | 16.5 KB |
| `risk-assessment-*.html` | 23.3 KB | 19.3 KB | 17.9 KB |

---

## 6. Overall takeaways

- **All three architectures correctly converged on the same headline decision** (Escalate to VP, net risk 8.0%), which is reassuring — the risk-assessment skill's math is robust to how the work gets divided up.
- **Single Agent produced the best cost-to-quality ratio in this run**: likely the lowest total token cost, and the most detailed/accurate outputs of the three, at the price of being fully serial (slowest wall-clock, and the largest single context to manage).
- **Agent Team is the cheapest way to get parallelism**, but this run shows a real failure mode: dividing the risk-assessment skill's own internal logic across a subagent with partial context led to a cross-skill reasoning error (revenue score) and reduced clause granularity — worth a skill-file tweak (e.g., explicitly disambiguating "target vertical" from "strategic discount vertical") if the team approach is used going forward.
- **Dynamic Workflow (approximated) delivered Single-Agent-level output quality with Agent-Team-level parallelism**, at the cost of an extra coordinator-reasoning pass on top — plausibly the best quality/latency balance of the three, but likely the most expensive in raw tokens since it pays both the multi-agent duplication cost and the coordinator's own decomposition overhead.
- Both delegation-based runs hit transient `529 Overloaded` API errors mid-session and needed manual retries; this was a shared infrastructure blip, not something attributable to either architecture.
