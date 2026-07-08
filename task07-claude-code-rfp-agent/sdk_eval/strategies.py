"""Strategy definitions ported from .claude/commands/rfp-0{1,2,3}-*.md.

Prompt text is copied verbatim from each command's body (everything after
the frontmatter), with one deliberate substitution: every occurrence of
the CLI reference runs' output path `outputs/runs/run-0N-...` is rewritten
to `outputs/runs-sdk/run-0N-...` so an SDK-run agent (which has real
Write/Bash tool access) never overwrites the already-committed CLI-based
reference outputs.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Strategy:
    key: str
    label: str
    dir_name: str
    prompt: str


_BASELINE_PROMPT = """Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

Produce:
1. A customer-facing proposal response covering: executive summary, our
   understanding of the customer's need, why we're the right fit, commercial
   proposal, contract approach, and risks/mitigations. Provide this as both a
   Markdown source file and a converted .docx.
2. An internal risk assessment (.html) — a self-contained interactive risk vs.
   revenue dashboard, for internal use only.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

## Expected artifacts

Save all outputs under `outputs/runs-sdk/run-01-baseline/`, producing exactly
these three files (`<customer>` and `<date>` reflect the customer name and
today's date):

- `outputs/runs-sdk/run-01-baseline/proposal-<customer>-<date>.docx`
- `outputs/runs-sdk/run-01-baseline/proposal-<customer>-<date>.md`
- `outputs/runs-sdk/run-01-baseline/risk-assessment-<customer>-<date>.html`
"""

_AGENT_TEAMS_PROMPT = """Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

Produce:
1. A customer-facing proposal response covering: executive summary, our
   understanding of the customer's need, why we're the right fit, commercial
   proposal, contract approach, and risks/mitigations. Provide this as both a
   Markdown source file and a converted .docx.
2. An internal risk assessment (.html) — a self-contained interactive risk vs.
   revenue dashboard, for internal use only.

Use the `deal-desk-orchestrator` agent to run this deal via agent team. The
orchestrator spawns five specialist teammates (Pricing Specialist, Legal
Reviewer, Technical Fit Specialist, Competitive Intel Analyst, Risk Assessment
Specialist), assigns each their scope, and synthesizes their findings. The
orchestrator must NOT perform the pricing, legal, technical-fit, competitive,
or risk-assessment analysis itself — delegate each to its specialist and
integrate their responses into the proposal and dashboard.

When the orchestrator delegates to the first four specialists (and later to
Risk Assessment), it must get two independent settings right:

- CONCURRENCY comes from batching: issue all four `Agent` calls as separate
  tool-use blocks in the SAME message. The harness runs them at the same
  time regardless of `run_in_background`.
- RETURN PATH comes from foreground vs. background: omit `run_in_background`
  (or set it to `false`) on every specialist call. Never set
  `run_in_background: true`. Foreground means each specialist's result lands
  back directly in the orchestrator's own conversation once ready.
  Background detaches the call — the orchestrator's turn ends immediately,
  and since the orchestrator is itself a spawned subagent, the completion
  notification does not come back to it directly; it surfaces to whatever
  session invoked the orchestrator, which then has to relay it second-hand.
  That relay is exactly what stalls the workflow (a dropped or delayed
  relay leaves the orchestrator waiting on a specialist that already
  finished).

So: same message (parallel), foreground (direct result, no relay). The
orchestrator must not end its turn while a specialist call is still
pending.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

## Expected artifacts

Save all outputs under `outputs/runs-sdk/run-02-agent-teams/`, producing exactly
these three files (`<customer>` and `<date>` reflect the customer name and
today's date):

- `outputs/runs-sdk/run-02-agent-teams/proposal-<customer>-<date>.docx`
- `outputs/runs-sdk/run-02-agent-teams/proposal-<customer>-<date>.md`
- `outputs/runs-sdk/run-02-agent-teams/risk-assessment-<customer>-<date>.html`
"""

_DYNAMIC_WORKFLOW_PROMPT = """Use a workflow to process the RFP at `synthetic-data/rfp-acme-corp.md`.

Orchestrate specialists to produce:
1. A customer-facing proposal response (.docx): executive summary, our
   understanding of need, fit, commercial proposal, contract approach,
   risks/mitigations.
2. An internal risk assessment (.html): interactive risk vs. revenue
   dashboard.

The workflow should dynamically decide which verification phases and agents
are needed based on RFP content. Reference `synthetic-data/past-wins.json`
and `synthetic-data/product-overview.md` as needed.

## Expected artifacts

Save all outputs under `outputs/runs-sdk/run-03-dynamic-workflow/`, producing
exactly these three files (`<customer>` and `<date>` reflect the customer
name and today's date):

- `outputs/runs-sdk/run-03-dynamic-workflow/proposal-<customer>-<date>.docx`
- `outputs/runs-sdk/run-03-dynamic-workflow/proposal-<customer>-<date>.md`
- `outputs/runs-sdk/run-03-dynamic-workflow/risk-assessment-<customer>-<date>.html`

Use ultracode.
"""

STRATEGIES = [
    Strategy(key="rfp-01-baseline", label="Baseline",
             dir_name="run-01-baseline", prompt=_BASELINE_PROMPT),
    Strategy(key="rfp-02-agent-teams", label="Agent Teams",
             dir_name="run-02-agent-teams", prompt=_AGENT_TEAMS_PROMPT),
    Strategy(key="rfp-03-dynamic-workflow", label="Dynamic Workflow",
             dir_name="run-03-dynamic-workflow", prompt=_DYNAMIC_WORKFLOW_PROMPT),
]


def get_strategy(key: str) -> Strategy:
    for s in STRATEGIES:
        if s.key == key:
            return s
    raise ValueError(
        f"unknown strategy key: {key!r} (expected one of {[s.key for s in STRATEGIES]})"
    )
