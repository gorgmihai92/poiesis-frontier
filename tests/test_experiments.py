"""The experiment log check of experiments.py prints what it printed in 1.1.4.

fixtures/logs/experiments.md and fixtures/expected/experiments.txt are copies of the Poiesis Lab notebook's test
log and of the output it expects (`fixtures/check.py` there runs the same comparison on the notebook's own copy).
"""
from __future__ import annotations

import subprocess
import sys
import unittest

import helpers
import experiments as ex

LOG = helpers.FIXTURES / "logs" / "experiments.md"
EXPECTED = helpers.FIXTURES / "expected" / "experiments.txt"
SCRIPT = helpers.SCRIPTS / "experiments.py"


class TheLog(unittest.TestCase):
    def test_the_output_for_the_labs_test_log_is_the_same_line_for_line(self):
        code, out, err = helpers.run(ex, [str(LOG)])
        self.assertEqual(out.splitlines(), EXPECTED.read_text(encoding="utf-8").splitlines())
        self.assertEqual(code, 1)  # the test log breaks rules on purpose
        self.assertEqual(err, "")

    def test_the_same_when_run_as_a_command_in_isolated_mode(self):
        run = subprocess.run([sys.executable, "-I", str(SCRIPT), str(LOG)], capture_output=True, text=True)
        self.assertEqual(run.stdout.splitlines(), EXPECTED.read_text(encoding="utf-8").splitlines())
        self.assertEqual(run.returncode, 1)

    def test_provisional_is_not_a_status_of_the_log(self):
        self.assertNotIn("provisional", ex.STATUSES)
        self.assertEqual(ex.STATUSES, ("planned", "running", "kept", "killed", "inconclusive"))
        self.assertIn("Rows not understood: E-008, E-009", EXPECTED.read_text(encoding="utf-8"))

    def test_columns_after_the_tenth_are_ignored(self):
        rows = ex.rows(LOG)
        self.assertEqual(len(rows[0]), 10)
        extra = "| E-001 | CN-001 · c | a | p | fewer than 3 of 8 | 2026-11-17 |  | 2099-12-31 | planned |  | ST-001 | note |\n"
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "experiments.md"
            log.write_text(extra, encoding="utf-8")
            code, out, _ = helpers.run(ex, [str(log)])
        self.assertEqual(code, 0)
        self.assertEqual(out, "1 experiments: 1 planned, 0 running, 0 kept, 0 killed, 0 inconclusive\n")

    def test_help_names_the_three_uses(self):
        code, out, _ = helpers.run(ex, ["-h"])
        self.assertEqual(code, 0)
        for word in ("experiments.py frontier/experiments.md", "experiments.py gate", "experiments.py ids CN"):
            self.assertIn(word, out)


if __name__ == "__main__":
    unittest.main()
