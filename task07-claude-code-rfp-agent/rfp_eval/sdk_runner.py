"""Run one Claude Agent SDK query to completion and normalize its result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RunResult:
    key: str
    result_text: str
    raw: dict


def result_to_dict(result_msg) -> dict:
    if result_msg is None:
        return {}
    return {
        "total_cost_usd": getattr(result_msg, "total_cost_usd", 0.0) or 0.0,
        "usage": getattr(result_msg, "usage", None) or {},
        "model_usage": getattr(result_msg, "model_usage", None) or {},
        "num_turns": getattr(result_msg, "num_turns", 0) or 0,
        "duration_ms": getattr(result_msg, "duration_ms", 0) or 0,
        "is_error": bool(getattr(result_msg, "is_error", False)),
        "result": getattr(result_msg, "result", None),
    }


def _default_query_fn():
    from claude_agent_sdk import query

    return query


async def run_query(prompt: str, *, options=None, key: str = "", query_fn=None) -> RunResult:
    if query_fn is None:
        query_fn = _default_query_fn()
    text_parts: list[str] = []
    result_msg = None
    async for msg in query_fn(prompt=prompt, options=options):
        if hasattr(msg, "total_cost_usd"):  # ResultMessage
            result_msg = msg
            continue
        content = getattr(msg, "content", None)
        if isinstance(content, list):
            for block in content:
                text = getattr(block, "text", None)
                if text:
                    text_parts.append(text)
    raw = result_to_dict(result_msg)
    result_text = raw.get("result") or "".join(text_parts)
    return RunResult(key=key, result_text=result_text, raw=raw)
