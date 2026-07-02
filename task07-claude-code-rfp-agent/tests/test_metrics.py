import json

from rfp_eval import metrics

RAW = {
    "total_cost_usd": 0.42,
    "usage": {
        "input_tokens": 1200,
        "output_tokens": 8000,
        "cache_read_input_tokens": 150000,
        "cache_creation_input_tokens": 30000,
    },
    "num_turns": 6,
    "duration_ms": 42000,
    "is_error": False,
}


def test_extract_metrics():
    m = metrics.extract_metrics("single", RAW)
    assert m.strategy_key == "single"
    assert m.cost_usd == 0.42
    assert m.input_tokens == 1200
    assert m.output_tokens == 8000
    assert m.cache_read_tokens == 150000
    assert m.cache_creation_tokens == 30000
    assert m.total_tokens == 189200
    assert m.num_turns == 6
    assert m.duration_ms == 42000
    assert m.is_error is False


def test_extract_metrics_defaults_on_empty():
    m = metrics.extract_metrics("swarm", {})
    assert m.cost_usd == 0.0
    assert m.total_tokens == 0
    assert m.is_error is False


def test_extract_metrics_sums_model_usage_across_subagents():
    # A coordinator + subagent swarm: the top-level `usage` dict only reflects
    # the coordinator's own turns, but `model_usage` aggregates every model
    # invoked during the query (including subagents dispatched via the Task
    # tool). Token totals must come from model_usage when it's present, or a
    # multi-agent strategy looks artificially cheap on tokens despite driving
    # up total_cost_usd.
    raw = {
        "total_cost_usd": 1.2,
        "usage": {
            "input_tokens": 4,
            "output_tokens": 706,
            "cache_read_input_tokens": 81189,
            "cache_creation_input_tokens": 2258,
        },
        "model_usage": {
            "claude-opus-coordinator": {
                "costUSD": 0.3,
                "inputTokens": 4,
                "outputTokens": 706,
                "cacheReadInputTokens": 81189,
                "cacheCreationInputTokens": 2258,
            },
            "claude-sonnet-subagent": {
                "costUSD": 0.9,
                "inputTokens": 500,
                "outputTokens": 20000,
                "cacheReadInputTokens": 100000,
                "cacheCreationInputTokens": 5000,
            },
        },
        "num_turns": 2,
        "duration_ms": 9000,
        "is_error": False,
    }
    m = metrics.extract_metrics("swarm", raw)
    assert m.input_tokens == 504
    assert m.output_tokens == 20706
    assert m.cache_read_tokens == 181189
    assert m.cache_creation_tokens == 7258
    assert m.total_tokens == 209657
    # cost still comes from the authoritative total_cost_usd field
    assert m.cost_usd == 1.2


def test_extract_metrics_falls_back_to_usage_when_no_model_usage():
    m = metrics.extract_metrics("single", RAW)
    assert m.input_tokens == 1200
    assert m.output_tokens == 8000


def test_metrics_as_dict_is_json_serializable():
    d = metrics.metrics_as_dict(metrics.extract_metrics("single", RAW))
    assert d["total_tokens"] == 189200
    assert json.dumps(d)
