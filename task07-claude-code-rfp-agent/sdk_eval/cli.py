"""Orchestration + argument parsing — the Python equivalent of
scripts/cost-eval.sh, driving sdk_eval's strategy/metrics/judge/report
modules instead of shelling out to the claude CLI.
"""
import argparse
import asyncio
import os
import sys
from pathlib import Path

from . import artifacts as artifacts_mod
from . import judge as judge_mod
from . import metrics as metrics_mod
from . import report as report_mod
from .runner import run_strategy
from .strategies import STRATEGIES, Strategy, get_strategy

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "outputs" / "runs-sdk"
COMPARISON_DIR = RUNS_DIR / "comparison-cost-eval"
TEMPLATE_PATH = REPO_ROOT / "templates" / "report.html.tmpl"
DEFAULT_PERMISSION_MODE = "bypassPermissions"


def resolve_commands(command_keys: list[str]) -> list[Strategy]:
    if not command_keys:
        return list(STRATEGIES)
    return [get_strategy(key) for key in command_keys]


def check_report_inputs_ready(runs_dir: Path, strategies: list[Strategy]) -> list[str]:
    missing = []
    for s in strategies:
        run_dir = runs_dir / s.dir_name
        if not (run_dir / "cost-eval.metrics.json").exists():
            missing.append(f"missing: {run_dir / 'cost-eval.metrics.json'}")
        if not any(run_dir.glob("risk-assessment-*.html")):
            missing.append(f"missing: {run_dir}/risk-assessment-*.html")
    return missing


def format_summary_table(rows: list[dict]) -> str:
    header = (
        f"{'command':<24}{'cost_usd':>12}{'input_tok':>12}"
        f"{'output_tok':>12}{'cache_creat':>14}{'cache_read':>14}"
    )
    lines = [header]
    for m in rows:
        t = m["tokens"]
        lines.append(
            f"{m['command']:<24}{m['cost_usd']:>12.6f}{t['input_tokens']:>12}"
            f"{t['output_tokens']:>12}{t['cache_creation_input_tokens']:>14}"
            f"{t['cache_read_input_tokens']:>14}"
        )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run RFP strategies via the Agent SDK and build a cost/quality comparison report."
    )
    parser.add_argument("commands", nargs="*", help="strategy keys to run (default: all 3)")
    parser.add_argument(
        "--report-only", action="store_true",
        help="skip running strategies; just (re)build the comparison report",
    )
    return parser.parse_args(argv)


async def build_report(force_judge: bool, permission_mode: str) -> None:
    quality_path = COMPARISON_DIR / "quality.json"
    if force_judge or judge_mod.load_quality_cache(quality_path) is None:
        scores = await judge_mod.judge_quality(RUNS_DIR, STRATEGIES, REPO_ROOT, permission_mode)
        judge_mod.save_quality_cache(quality_path, scores)
        print(f"wrote {quality_path}")
    else:
        print(f"quality cache already exists at {quality_path}")
    report_data = report_mod.build_report_data(RUNS_DIR, COMPARISON_DIR, STRATEGIES)
    output_path = COMPARISON_DIR / "report.html"
    report_mod.render(report_data, TEMPLATE_PATH, output_path)
    print(f"wrote {output_path}")
    print(f"wrote {output_path.parent / 'report-data.json'}")


async def run_pipeline(command_keys: list[str], permission_mode: str, report_only: bool) -> int:
    if report_only:
        missing = check_report_inputs_ready(RUNS_DIR, STRATEGIES)
        if missing:
            for m in missing:
                print(m, file=sys.stderr)
            print(
                "error: --report-only requires cost-eval + risk-assessment "
                "outputs for all 3 runs", file=sys.stderr,
            )
            return 1
        await build_report(force_judge=False, permission_mode=permission_mode)
        return 0

    try:
        strategies = resolve_commands(command_keys)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Permission mode: {permission_mode} (override with PERMISSION_MODE env var)\n")

    rows = []
    for strategy in strategies:
        run_dir = RUNS_DIR / strategy.dir_name
        print(f"=== Running {strategy.key} ===")
        result = await run_strategy(strategy, REPO_ROOT, permission_mode)
        metrics = metrics_mod.save_metrics(run_dir, strategy.key, result)
        for warning in artifacts_mod.check_expected_artifacts(run_dir):
            print(f"  warning: {warning}", file=sys.stderr)
        print(
            f"  cost_usd (all agents): ${metrics['cost_usd']}  "
            f"(orchestrator-only: ${metrics['orchestrator_cost_usd']})  "
            f"-> {run_dir / 'cost-eval.metrics.json'}\n"
        )
        rows.append(metrics)

    print("=== Summary ===")
    print(format_summary_table(rows))
    print()

    missing = check_report_inputs_ready(RUNS_DIR, STRATEGIES)
    if not missing:
        print("=== Comparison report ===")
        await build_report(force_judge=True, permission_mode=permission_mode)
    else:
        print(
            "note: skipping comparison report — not all 3 strategy runs "
            "have outputs yet", file=sys.stderr,
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.report_only and args.commands:
        print("error: --report-only does not take additional arguments", file=sys.stderr)
        return 1
    permission_mode = os.environ.get("PERMISSION_MODE", DEFAULT_PERMISSION_MODE)
    return asyncio.run(run_pipeline(args.commands, permission_mode, args.report_only))


if __name__ == "__main__":
    sys.exit(main())
