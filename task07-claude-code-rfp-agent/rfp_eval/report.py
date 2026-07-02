"""Merge metrics + quality scores and render the comparison dashboard."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .judge import RUBRIC_DIMS, QualityScore
from .metrics import RunMetrics
from .strategies import LABELS, STRATEGY_KEYS

DEFAULT_TEMPLATE = Path(__file__).parent / "templates" / "report.html.tmpl"
_DATA_MARKER = "__REPORT_DATA__"


def rubric_dims() -> list[str]:
    """Return the rubric dimension keys."""
    return list(RUBRIC_DIMS)


def _quality_per_dollar(total: int, cost: float) -> float:
    return round(total / cost, 4) if cost > 0 else 0.0


def build_report_data(
    metrics: list[RunMetrics],
    scores: list[QualityScore],
    *,
    rfp: str = "",
    generated_at: str | None = None,
) -> dict:
    metrics_by = {m.strategy_key: m for m in metrics}
    scores_by = {s.strategy_key: s for s in scores}
    entries: list[dict] = []
    for key in STRATEGY_KEYS:
        m = metrics_by.get(key)
        if m is None:
            continue
        sc = scores_by.get(key)
        quality = {**(sc.scores if sc else {d: 0 for d in RUBRIC_DIMS})}
        quality["total"] = sc.total if sc else 0
        quality["rationale"] = sc.rationale if sc else ""
        entries.append(
            {
                "strategy_key": key,
                "label": LABELS.get(key, key),
                "cost_usd": m.cost_usd,
                "input_tokens": m.input_tokens,
                "output_tokens": m.output_tokens,
                "cache_read_tokens": m.cache_read_tokens,
                "cache_creation_tokens": m.cache_creation_tokens,
                "total_tokens": m.total_tokens,
                "num_turns": m.num_turns,
                "duration_ms": m.duration_ms,
                "is_error": m.is_error,
                "quality": quality,
                "quality_per_dollar": _quality_per_dollar(quality["total"], m.cost_usd),
            }
        )
    winner_quality = max(entries, key=lambda e: e["quality"]["total"], default=None)
    winner_value = max(entries, key=lambda e: e["quality_per_dollar"], default=None)
    return {
        "rfp": rfp,
        "generated_at": generated_at
        or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "rubric_dims": list(RUBRIC_DIMS),
        "strategies": entries,
        "winner_quality": winner_quality["strategy_key"] if winner_quality else None,
        "winner_value": winner_value["strategy_key"] if winner_value else None,
    }


def render_report(data: dict, *, template_path: Path | None = None) -> str:
    tmpl = (template_path or DEFAULT_TEMPLATE).read_text()
    return tmpl.replace(_DATA_MARKER, json.dumps(data))


def write_report(html: str, dest: str | Path) -> Path:
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    return dest
