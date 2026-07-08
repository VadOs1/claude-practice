"""Build the same cost-eval.metrics.json shape cost-eval.sh's jq filter
produces, sourced from a claude_agent_sdk.ResultMessage instead of the
claude CLI's raw JSON output.
"""
import json
from dataclasses import asdict
from pathlib import Path

from claude_agent_sdk import ResultMessage

_TOKEN_FIELDS = {
    "input_tokens": "inputTokens",
    "output_tokens": "outputTokens",
    "cache_creation_input_tokens": "cacheCreationInputTokens",
    "cache_read_input_tokens": "cacheReadInputTokens",
}


def build_metrics(strategy_key: str, result: ResultMessage) -> dict:
    model_usage = result.model_usage or {}
    cost_usd = sum((m.get("costUSD") or 0) for m in model_usage.values())
    tokens = {
        out_key: sum((m.get(sdk_key) or 0) for m in model_usage.values())
        for out_key, sdk_key in _TOKEN_FIELDS.items()
    }
    return {
        "command": strategy_key,
        "cost_usd": cost_usd,
        "orchestrator_cost_usd": result.total_cost_usd,
        "num_turns": result.num_turns,
        "duration_ms": result.duration_ms,
        "tokens": tokens,
        "per_model": model_usage,
    }


def save_metrics(run_dir: Path, strategy_key: str, result: ResultMessage) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "cost-eval.json").write_text(
        json.dumps(asdict(result), indent=2, default=str)
    )
    metrics = build_metrics(strategy_key, result)
    (run_dir / "cost-eval.metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics
