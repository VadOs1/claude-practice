import unittest

from claude_agent_sdk import ResultMessage

from sdk_eval.runner import _collect_result


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


if __name__ == "__main__":
    unittest.main()
