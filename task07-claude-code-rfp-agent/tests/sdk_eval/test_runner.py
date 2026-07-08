import unittest
from pathlib import Path
from unittest.mock import patch

from claude_agent_sdk import ResultMessage

from sdk_eval.runner import _collect_result, run_prompt


async def fake_stream(items):
    for item in items:
        yield item


def make_result(is_error=False, **overrides):
    defaults = dict(
        subtype="success",
        duration_ms=1000,
        duration_api_ms=900,
        is_error=is_error,
        num_turns=1,
        session_id="s1",
        result="done",
        errors=None,
    )
    defaults.update(overrides)
    return ResultMessage(**defaults)


class CollectResultTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_final_result_message(self):
        result = make_result()
        collected = await _collect_result(fake_stream(["not-a-result", result]))
        self.assertIs(collected, result)

    async def test_raises_when_no_result_message_seen(self):
        with self.assertRaisesRegex(RuntimeError, "ended without a ResultMessage"):
            await _collect_result(fake_stream(["not-a-result"]))

    async def test_raises_when_result_is_error(self):
        result = make_result(is_error=True, errors=["boom"], result="failed")
        with self.assertRaisesRegex(RuntimeError, "errored"):
            await _collect_result(fake_stream([result]))


class RunPromptModelTests(unittest.IsolatedAsyncioTestCase):
    async def test_threads_model_through_to_options(self):
        captured_options = {}

        def fake_query(*, prompt, options):
            captured_options["options"] = options
            return fake_stream([make_result()])

        with patch("sdk_eval.runner.query", side_effect=fake_query):
            await run_prompt("hi", Path("."), "default", model="sonnet")

        self.assertEqual(captured_options["options"].model, "sonnet")

    async def test_defaults_to_no_model(self):
        captured_options = {}

        def fake_query(*, prompt, options):
            captured_options["options"] = options
            return fake_stream([make_result()])

        with patch("sdk_eval.runner.query", side_effect=fake_query):
            await run_prompt("hi", Path("."), "default")

        self.assertIsNone(captured_options["options"].model)


if __name__ == "__main__":
    unittest.main()
