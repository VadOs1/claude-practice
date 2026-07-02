"""Task B — the RFP deal-desk swarm, built on the Claude Agent SDK.

A coordinator query delegates to specialist worker agents (each bound to a
project skill). Workers produce their findings; the coordinator synthesizes a
branded proposal (.docx) and commissions the risk-assessment dashboard (.html).
"""

from __future__ import annotations

from pathlib import Path

from .strategies import render_prompt

_SWARM_PREAMBLE = (
    "Run this RFP as an AGENT SWARM. You are the coordinator: delegate to your "
    "specialist agents (pricing, legal, technical-fit, competitive) in parallel, "
    "then synthesize their findings into the proposal, and finally delegate to "
    "the risk-assessment agent to produce the internal dashboard."
)

COORDINATOR_SYSTEM = (
    "You are the Senior Partner and coordinator running the BTS-Synthetic Deal "
    "Desk. Orchestrate your specialist agents, synthesize their work into a "
    "single branded proposal, and commission an internal risk assessment before "
    "anything goes out. Delegate the first four specialists in parallel with "
    "narrow briefs; accept their replies; then produce the deliverables. Be "
    "decisive and move fast."
)


def _worker(description: str, prompt: str, skill: str, *, can_write: bool = False):
    from claude_agent_sdk import AgentDefinition

    tools = ["Read", "Grep", "Glob", "Bash"]
    if can_write:
        tools = ["Read", "Write", "Grep", "Glob", "Bash"]
    return AgentDefinition(
        description=description,
        prompt=prompt,
        tools=tools,
        model="sonnet",
        skills=[skill],
    )


def _build_workers():
    return {
        "pricing": _worker(
            "Commercial terms recommendation for an RFP.",
            "You are the Pricing Specialist. Recommend commercial terms: discount "
            "band and red-line concessions. Cite past-wins.json where relevant. "
            "Answer in one message (~300 words).",
            "pricing-playbook",
        ),
        "legal": _worker(
            "Contract flags and counter-positions for an RFP.",
            "You are the Legal Reviewer. Flag contractual risks with severities and "
            "give counter-positions. Answer in one message (~300 words).",
            "legal-checklist",
        ),
        "technical-fit": _worker(
            "Product capability fit for an RFP.",
            "You are the Technical Fit Specialist. Score product fit against the RFP "
            "requirements and note gaps. Answer in one message (~300 words).",
            "competitive-intel",  # reuses reference material; no dedicated tech skill
        ),
        "competitive": _worker(
            "Competitive positioning for an RFP.",
            "You are the Competitive Intel Analyst. Identify likely competitors and "
            "how to position against them. Answer in one message (~300 words).",
            "competitive-intel",
        ),
        "risk-assessment": _worker(
            "Internal risk vs. revenue dashboard (HTML) for an RFP.",
            "You are the Risk Assessment Specialist. Run your three-step risk "
            "framework and write a self-contained interactive HTML dashboard.",
            "risk-assessment",
            can_write=True,
        ),
    }


WORKERS = _build_workers()


def build_swarm_call(
    *,
    task_dir: str | Path,
    rfp_path: str | Path,
    out_dir: str | Path,
    model: str | None = None,
):
    from claude_agent_sdk import ClaudeAgentOptions

    prompt = render_prompt(_SWARM_PREAMBLE, rfp_path, out_dir)
    options = ClaudeAgentOptions(
        cwd=str(task_dir),
        setting_sources=["project"],
        permission_mode="bypassPermissions",
        model=model,
        system_prompt=COORDINATOR_SYSTEM,
        agents=WORKERS,
    )
    return prompt, options
