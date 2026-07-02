"""End-to-end async flow: run strategies concurrently, judge, build report."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict
from pathlib import Path

from . import judge, report
from .metrics import extract_metrics, metrics_as_dict
from .sdk_runner import RunResult, run_query
from .strategies import STRATEGY_KEYS, build_call


async def _run_one(key, *, task_dir, rfp_path, runs_root, model, query_factory):
    out_dir = Path(runs_root) / key
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt, options = build_call(
        key, task_dir=task_dir, rfp_path=rfp_path, out_dir=out_dir, model=model
    )
    query_fn = query_factory(out_dir) if query_factory else None
    result = await run_query(prompt, options=options, key=key, query_fn=query_fn)
    (out_dir / "run.json").write_text(json.dumps(result.raw, indent=2))
    return out_dir, result


async def run_evaluation(
    *,
    task_dir: str | Path,
    rfp_path: str | Path,
    out_root: str | Path,
    model: str | None = None,
    query_fn=None,          # factory: (out_dir) -> async query fn; None → real SDK
    judge_query_fn=None,    # async query fn for the judge; None → real SDK
) -> Path:
    task_dir = Path(task_dir)
    out_root = Path(out_root)
    runs_root = out_root / "runs"
    eval_root = out_root / "eval"
    eval_root.mkdir(parents=True, exist_ok=True)

    gathered = await asyncio.gather(
        *(
            _run_one(
                key,
                task_dir=task_dir,
                rfp_path=rfp_path,
                runs_root=runs_root,
                model=model,
                query_factory=query_fn,
            )
            for key in STRATEGY_KEYS
        ),
        return_exceptions=True,
    )

    # A single strategy raising (SDK/transport/CLI crash) must not discard the
    # other, already-completed (and expensive) runs. Normalize any exception
    # into a failed RunResult for that strategy so the report still renders
    # with all four strategies represented.
    results: list[tuple[Path, RunResult]] = []
    for key, res in zip(STRATEGY_KEYS, gathered):
        if isinstance(res, BaseException):
            out_dir = runs_root / key
            out_dir.mkdir(parents=True, exist_ok=True)
            failed = RunResult(key=key, result_text="", raw={"is_error": True})
            run_json = out_dir / "run.json"
            if not run_json.exists():
                run_json.write_text(json.dumps(failed.raw, indent=2))
            results.append((out_dir, failed))
        else:
            results.append(res)

    metrics = [extract_metrics(r.key, r.raw) for _, r in results]
    (eval_root / "metrics.json").write_text(
        json.dumps([metrics_as_dict(m) for m in metrics], indent=2)
    )

    artifacts = {r.key: judge.read_artifacts(out_dir) for out_dir, r in results}
    scores = await judge.judge_quality(artifacts, model=model or "sonnet", query_fn=judge_query_fn)
    (eval_root / "quality.json").write_text(
        json.dumps([asdict(s) for s in scores], indent=2)
    )

    data = report.build_report_data(metrics, scores, rfp=str(rfp_path))
    html = report.render_report(data)
    return report.write_report(html, eval_root / "index.html")
