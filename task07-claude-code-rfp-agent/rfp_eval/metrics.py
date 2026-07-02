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
    usage = raw.get("usage") or {}
    inp = int(usage.get("input_tokens", 0) or 0)
    out = int(usage.get("output_tokens", 0) or 0)
    cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
    cache_creation = int(usage.get("cache_creation_input_tokens", 0) or 0)
    return RunMetrics(
        strategy_key=strategy_key,
        cost_usd=float(raw.get("total_cost_usd", 0.0) or 0.0),
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
