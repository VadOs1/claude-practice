#!/usr/bin/env python3
"""Run RFP strategies via the Agent SDK and build a cost/quality comparison
report — equivalent pipeline to scripts/cost-eval.sh, but every invocation
of Claude goes through claude_agent_sdk instead of shelling out to the
claude CLI directly.

Usage:
  python3 scripts/cost-eval-sdk.py                     # run all 3 strategies, then build report
  python3 scripts/cost-eval-sdk.py rfp-02-agent-teams   # run just one
  python3 scripts/cost-eval-sdk.py --report-only        # rebuild report from existing outputs

Requires: claude CLI on PATH (claude_agent_sdk spawns it under the hood),
the claude_agent_sdk pip package (already in .venv), python3.
Must be run with the .venv's python3 (or any interpreter with
claude_agent_sdk installed) — it locates the repo root relative to this
file, so it does not need to be run from any particular cwd.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sdk_eval.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
