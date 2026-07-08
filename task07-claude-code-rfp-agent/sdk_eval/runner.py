"""Run a prompt through the Agent SDK and return the terminal ResultMessage.

This replaces cost-eval.sh's `claude -p "..." --output-format json` calls.
"""
from pathlib import Path
from typing import AsyncIterator

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from .strategies import Strategy


async def _collect_result(messages: AsyncIterator) -> ResultMessage:
    result = None
    async for message in messages:
        if isinstance(message, ResultMessage):
            result = message
    if result is None:
        raise RuntimeError("SDK message stream ended without a ResultMessage")
    if result.is_error:
        raise RuntimeError(
            f"strategy run errored (subtype={result.subtype!r}): "
            f"errors={result.errors!r} result={result.result!r}"
        )
    return result


async def run_prompt(prompt: str, repo_root: Path, permission_mode: str) -> ResultMessage:
    # setting_sources is left at its SDK default (None = load user + project +
    # local settings) to match the claude CLI's own default discovery of
    # .claude/agents/*.md and .claude/skills/* when run from repo_root.
    options = ClaudeAgentOptions(cwd=str(repo_root), permission_mode=permission_mode)
    return await _collect_result(query(prompt=prompt, options=options))


async def run_strategy(strategy: Strategy, repo_root: Path, permission_mode: str) -> ResultMessage:
    return await run_prompt(strategy.prompt, repo_root, permission_mode)
