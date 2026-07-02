from rfp_eval import swarm


def test_workers_cover_the_diagram_roles():
    assert set(swarm.WORKERS) == {
        "pricing",
        "legal",
        "technical-fit",
        "competitive",
        "risk-assessment",
    }


def test_each_worker_binds_a_skill():
    assert swarm.WORKERS["pricing"].skills == ["pricing-playbook"]
    assert swarm.WORKERS["legal"].skills == ["legal-checklist"]
    assert swarm.WORKERS["competitive"].skills == ["competitive-intel"]
    assert swarm.WORKERS["risk-assessment"].skills == ["risk-assessment"]
    # risk worker must be able to write its HTML dashboard
    assert "Write" in (swarm.WORKERS["risk-assessment"].tools or [])


def test_build_swarm_call_shapes_options():
    prompt, options = swarm.build_swarm_call(
        task_dir="/task", rfp_path="synthetic-data/rfp-acme-corp.md", out_dir="/task/outputs/runs/swarm"
    )
    assert "synthetic-data/rfp-acme-corp.md" in prompt
    assert "/task/outputs/runs/swarm" in prompt
    assert options.agents is swarm.WORKERS
    assert options.setting_sources == ["project"]
    assert str(options.cwd) == "/task"
    assert options.permission_mode == "bypassPermissions"
    assert "coordinator" in (options.system_prompt or "").lower()
