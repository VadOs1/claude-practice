"""CLI: uv run python -m rfp_eval [--rfp ...] [--out ...] [--model ...]"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from .orchestrator import run_evaluation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="rfp_eval",
        description="Run the RFP through single / swarm / dynamic strategies on the "
        "Claude Agent SDK and build a charted cost/quality report.",
    )
    parser.add_argument("--rfp", default="synthetic-data/rfp-acme-corp.md")
    parser.add_argument("--out", default="outputs")
    parser.add_argument("--task-dir", default=".")
    parser.add_argument("--model", default="claude-sonnet-5")
    args = parser.parse_args(argv)

    index = asyncio.run(
        run_evaluation(
            task_dir=args.task_dir,
            rfp_path=args.rfp,
            out_root=args.out,
            model=args.model,
        )
    )
    print(f"Report written to: {Path(index).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
