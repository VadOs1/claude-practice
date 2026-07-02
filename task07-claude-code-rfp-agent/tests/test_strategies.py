from rfp_eval import strategies as s


def test_strategy_keys_and_labels():
    assert s.STRATEGY_KEYS == ["single", "swarm", "dynamic", "agent_teams"]
    assert s.LABELS["swarm"] == "Agent Swarm"
    assert s.LABELS["agent_teams"] == "Agent Teams"
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


def test_build_call_agent_teams_prompt():
    prompt, options = s.build_call(
        "agent_teams", task_dir="/task", rfp_path="rfp.md", out_dir="/task/outputs/runs/agent_teams"
    )
    assert "agent team" in prompt.lower()
    assert "coordinator" in prompt.lower()
    # names the project's specialist roster, per index.md: "be quite
    # specific which agents to include in the team"
    assert "deal-desk-orchestrator" in prompt
    assert "pricing" in prompt.lower()
    assert "risk-assessment" in prompt.lower()
    # same options shape as single/dynamic — no swarm-style `agents=` param
    assert str(options.cwd) == "/task"
    assert options.setting_sources == ["project"]
    assert options.permission_mode == "bypassPermissions"
    assert options.agents is None


def test_build_call_swarm_delegates_to_swarm_module():
    prompt, options = s.build_call(
        "swarm", task_dir="/task", rfp_path="rfp.md", out_dir="/task/outputs/runs/swarm"
    )
    assert "coordinator" in prompt.lower() or "swarm" in prompt.lower()
    assert options.agents is not None
    assert "pricing" in options.agents
