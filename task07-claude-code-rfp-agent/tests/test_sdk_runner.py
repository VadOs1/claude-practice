import asyncio
from types import SimpleNamespace

from rfp_eval import sdk_runner


def _fake_result():
    return SimpleNamespace(
        total_cost_usd=0.42,
        usage={
            "input_tokens": 1200,
            "output_tokens": 8000,
            "cache_read_input_tokens": 150000,
            "cache_creation_input_tokens": 30000,
        },
        model_usage={
            "claude-opus": {
                "costUSD": 0.42,
                "inputTokens": 1200,
                "outputTokens": 8000,
                "cacheReadInputTokens": 150000,
                "cacheCreationInputTokens": 30000,
            },
        },
        num_turns=6,
        duration_ms=42000,
        is_error=False,
        result="Wrote proposal.docx and risk-assessment.html",
    )


def _text_msg(text):
    # duck-typed AssistantMessage: has .content list of blocks with .text
    return SimpleNamespace(content=[SimpleNamespace(text=text)])


def test_result_to_dict_normalizes():
    d = sdk_runner.result_to_dict(_fake_result())
    assert d["total_cost_usd"] == 0.42
    assert d["usage"]["output_tokens"] == 8000
    assert d["num_turns"] == 6
    assert d["is_error"] is False


def test_result_to_dict_captures_model_usage():
    d = sdk_runner.result_to_dict(_fake_result())
    assert d["model_usage"]["claude-opus"]["outputTokens"] == 8000


def test_result_to_dict_model_usage_defaults_to_empty_dict():
    fr = _fake_result()
    del fr.model_usage
    d = sdk_runner.result_to_dict(fr)
    assert d["model_usage"] == {}


def test_result_to_dict_none():
    assert sdk_runner.result_to_dict(None) == {}


def test_run_query_collects_result_and_text():
    async def fake_query(prompt, options=None):
        yield _text_msg("working...")
        yield _fake_result()

    result = asyncio.run(
        sdk_runner.run_query("do it", key="single", query_fn=fake_query)
    )
    assert result.key == "single"
    assert result.raw["total_cost_usd"] == 0.42
    # prefers ResultMessage.result text
    assert "proposal.docx" in result.result_text


def test_run_query_falls_back_to_assistant_text_when_no_result_text():
    fr = _fake_result()
    fr.result = None

    async def fake_query(prompt, options=None):
        yield _text_msg("only assistant text")
        yield fr

    result = asyncio.run(sdk_runner.run_query("p", query_fn=fake_query))
    assert result.result_text == "only assistant text"
