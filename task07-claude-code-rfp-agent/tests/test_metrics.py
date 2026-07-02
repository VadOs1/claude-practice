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


def test_metrics_as_dict_is_json_serializable():
    d = metrics.metrics_as_dict(metrics.extract_metrics("single", RAW))
    assert d["total_tokens"] == 189200
    assert json.dumps(d)
