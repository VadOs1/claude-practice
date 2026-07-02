"""Non-swarm strategy definitions (single agent, dynamic workflow)."""

from __future__ import annotations

from pathlib import Path

STRATEGY_KEYS: list[str] = ["single", "swarm", "dynamic"]

LABELS: dict[str, str] = {
    "single": "Single Agent",
    "swarm": "Agent Swarm",
    "dynamic": "Dynamic Workflow",
}

COMMON_TASK = """\
You are processing an inbound RFP for the BTS-Synthetic Deal Desk.

RFP file: {rfp_path}
Reference data (read as needed): synthetic-data/past-wins.json, \
synthetic-data/product-overview.md

Produce BOTH deliverables and save them into the directory {out_dir}:
1. A customer-facing branded proposal at {out_dir}/proposal.docx (use the docx skill).
2. An internal risk-assessment dashboard at {out_dir}/risk-assessment.html \
(use the risk-assessment skill).

Use the available project skills: pricing-playbook, legal-checklist, \
competitive-intel, risk-assessment, docx. When finished, print a one-line \
confirmation naming the two files you wrote.
"""

_PREAMBLES = {
    "single": (
        "Handle this RFP entirely yourself as a single agent. Do NOT spawn "
        "sub-agents, agent teams, or workflows — rely only on skills and your "
        "own reasoning."
    ),
    "dynamic": (
        "Use a DYNAMIC WORKFLOW: first draft an explicit multi-step plan for "
        "handling this RFP end to end, then execute that workflow step by step, "
        "adapting the plan as results come in."
    ),
}


def render_prompt(preamble: str, rfp_path: str | Path, out_dir: str | Path) -> str:
    task = COMMON_TASK.format(rfp_path=rfp_path, out_dir=out_dir)
    return f"{preamble}\n\n{task}"


def build_call(
    key: str,
    *,
    task_dir: str | Path,
    rfp_path: str | Path,
    out_dir: str | Path,
    model: str | None = None,
):
    """Return (prompt, ClaudeAgentOptions) for a non-swarm strategy."""
    if key not in _PREAMBLES:
        raise ValueError(f"build_call handles single/dynamic only, not {key!r}")
    from claude_agent_sdk import ClaudeAgentOptions

    prompt = render_prompt(_PREAMBLES[key], rfp_path, out_dir)
    options = ClaudeAgentOptions(
        cwd=str(task_dir),
        setting_sources=["project"],
        permission_mode="bypassPermissions",
        model=model,
    )
    return prompt, options
