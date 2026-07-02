import pytest

from rfp_eval import strategies as s


def test_strategy_keys_and_labels():
    assert s.STRATEGY_KEYS == ["single", "swarm", "dynamic"]
    assert s.LABELS["swarm"] == "Agent Swarm"
    assert set(s.LABELS) == set(s.STRATEGY_KEYS)


def test_render_prompt_embeds_paths():
    prompt = s.render_prompt("PREAMBLE-X", "synthetic-data/rfp-acme-corp.md", "outputs/runs/single")
    assert "PREAMBLE-X" in prompt
    assert "synthetic-data/rfp-acme-corp.md" in prompt
    assert "outputs/runs/single" in prompt
    assert "proposal.docx" in prompt
    assert "risk-assessment.html" in prompt


def test_build_call_single_no_delegation():
    prompt, options = s.build_call(
        "single", task_dir="/task", rfp_path="rfp.md", out_dir="/task/outputs/runs/single"
    )
    assert "single agent" in prompt.lower()
    assert "do not" in prompt.lower()  # forbids delegation
    assert str(options.cwd) == "/task"
    assert options.setting_sources == ["project"]
    assert options.permission_mode == "bypassPermissions"


def test_build_call_dynamic_prompt():
    prompt, _ = s.build_call("dynamic", task_dir="/task", rfp_path="rfp.md", out_dir="/o")
    assert "dynamic workflow" in prompt.lower()


def test_build_call_swarm_rejected_here():
    with pytest.raises(ValueError):
        s.build_call("swarm", task_dir="/task", rfp_path="rfp.md", out_dir="/o")
