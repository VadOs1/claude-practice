import tempfile
import unittest
from pathlib import Path

from sdk_eval.artifacts import check_expected_artifacts


class CheckExpectedArtifactsTests(unittest.TestCase):
    def test_empty_dir_reports_all_three_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            warnings = check_expected_artifacts(Path(tmp))
            self.assertEqual(len(warnings), 3)

    def test_all_present_reports_no_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "proposal-acme-corp-2026-07-06.md").write_text("x")
            (run_dir / "proposal-acme-corp-2026-07-06.docx").write_bytes(b"x")
            (run_dir / "risk-assessment-acme-corp-2026-07-06.html").write_text("x")
            self.assertEqual(check_expected_artifacts(run_dir), [])

    def test_partial_reports_only_missing_ones(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "proposal-acme-corp-2026-07-06.md").write_text("x")
            warnings = check_expected_artifacts(run_dir)
            self.assertEqual(len(warnings), 2)
            self.assertTrue(any("docx" in w for w in warnings))
            self.assertTrue(any("risk-assessment" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
