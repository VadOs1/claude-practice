"""Check that a strategy run produced the artifacts its prompt asked for."""
from pathlib import Path

EXPECTED_PATTERNS = ("proposal-*.md", "proposal-*.docx", "risk-assessment-*.html")


def check_expected_artifacts(run_dir: Path) -> list[str]:
    warnings = []
    for pattern in EXPECTED_PATTERNS:
        if not any(run_dir.glob(pattern)):
            warnings.append(f"missing expected artifact matching {pattern!r} in {run_dir}")
    return warnings
