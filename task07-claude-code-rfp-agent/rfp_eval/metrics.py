"""Normalize a run's raw dict into comparable metrics."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class RunMetrics:
    strategy_key: str
    cost_usd: float
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_creation_tokens: int
    total_tokens: int
    num_turns: int
    duration_ms: int
    is_error: bool


def extract_metrics(strategy_key: str, raw: dict) -> RunMetrics:
    model_usage = raw.get("model_usage") or {}
    if model_usage:
        # `usage` (tokens) and `total_cost_usd` both only reflect the
        # top-level query's own turns; `model_usage` breaks down every model
        # invoked during the call, including subagents dispatched via the
        # Task tool. Sum across models so multi-agent strategies don't look
        # artificially cheap on tokens or cost.
        inp = sum(int(m.get("inputTokens", 0) or 0) for m in model_usage.values())
        out = sum(int(m.get("outputTokens", 0) or 0) for m in model_usage.values())
        cache_read = sum(
            int(m.get("cacheReadInputTokens", 0) or 0) for m in model_usage.values()
        )
        cache_creation = sum(
            int(m.get("cacheCreationInputTokens", 0) or 0)
            for m in model_usage.values()
        )
        cost = sum(float(m.get("costUSD", 0.0) or 0.0) for m in model_usage.values())
    else:
        usage = raw.get("usage") or {}
        inp = int(usage.get("input_tokens", 0) or 0)
        out = int(usage.get("output_tokens", 0) or 0)
        cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
        cache_creation = int(usage.get("cache_creation_input_tokens", 0) or 0)
        cost = float(raw.get("total_cost_usd", 0.0) or 0.0)
    return RunMetrics(
        strategy_key=strategy_key,
        cost_usd=cost,
        input_tokens=inp,
        output_tokens=out,
        cache_read_tokens=cache_read,
        cache_creation_tokens=cache_creation,
        total_tokens=inp + out + cache_read + cache_creation,
        num_turns=int(raw.get("num_turns", 0) or 0),
        duration_ms=int(raw.get("duration_ms", 0) or 0),
        is_error=bool(raw.get("is_error", False)),
    )


def metrics_as_dict(m: RunMetrics) -> dict:
    return asdict(m)
