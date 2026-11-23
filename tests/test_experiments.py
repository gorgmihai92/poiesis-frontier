"""The experiment log check of experiments.py prints what it printed in 1.1.4, and (1.3.1) compares each row's
assumption, prediction and kill criterion with the concept's own lines.

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


REPORT = """# Report

### If the bar is at the bottom, then people find an item faster

- **Id:** CN-001
- **From:** none
- **Assumption:** people use the filters.
- **Prediction:** at least 5 of 6 are faster at the bottom.
- **Kill criterion:** 3 or fewer of 6 faster · written 2026-11-17; inconclusive if exactly 4
- **Log id:** E-001
"""
ASSUMPTION = "people use the filters."
PREDICTION = "at least 5 of 6 are faster at the bottom."
KILL = "3 or fewer of 6 faster; inconclusive if exactly 4"


def log_row(concept="CN-001 · bar at the bottom (frontier/2026-11-17-bar.md)", assumption=ASSUMPTION,
            prediction=PREDICTION, kill=KILL) -> str:
    return (f"| id | concept | assumption | prediction | kill criterion | criterion written | started | due | status | result |\n"
            f"|---|---|---|---|---|---|---|---|---|---|\n"
            f"| E-001 | {concept} | {assumption} | {prediction} | {kill} | 2026-11-17 |  | 2099-12-31 | planned |  |\n")


class TheRowCopiesTheConcept(unittest.TestCase):
    """The row's assumption, prediction and kill criterion are the concept's lines, word for word (1.3.1)."""

    def check(self, row: str, report: str | None = REPORT, where: str = "frontier/2026-11-17-bar.md"):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "frontier").mkdir()
            if report is not None:
                (root / where).parent.mkdir(parents=True, exist_ok=True)
                (root / where).write_text(report, encoding="utf-8")
            log = root / "frontier" / "experiments.md"
            log.write_text(row, encoding="utf-8")
            return helpers.run(ex, [str(log)])

    def test_a_row_that_copies_the_concept_has_no_problem(self):
        code, out, err = self.check(log_row())
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, "1 experiments: 1 planned, 0 running, 0 kept, 0 killed, 0 inconclusive\n")

    def test_each_cell_that_differs_is_a_problem_that_names_it(self):
        for name in ("assumption", "prediction", "kill criterion"):
            with self.subTest(name):
                other = {"assumption": ASSUMPTION, "prediction": PREDICTION, "kill": KILL}
                other["kill" if name == "kill criterion" else name] = "something else"
                code, out, err = self.check(log_row(**other))
                self.assertEqual(code, 1)
                self.assertIn(f"E-001: {name} DIFFERS from CN-001 in frontier/2026-11-17-bar.md", out)
                self.assertEqual(out.count("DIFFERS"), 1)
                self.assertIn("    row:     something else", out)
                self.assertEqual(err, "")

    def test_a_dropped_full_stop_is_a_difference(self):
        code, out, _ = self.check(log_row(prediction=PREDICTION.rstrip(".")))
        self.assertEqual(code, 1)
        self.assertIn("E-001: prediction DIFFERS", out)

    def test_written_and_its_date_go_in_their_own_column_not_in_the_cell(self):
        kept = "3 or fewer of 6 faster · written 2026-11-17; inconclusive if exactly 4"
        code, out, _ = self.check(log_row(kill=kept))
        self.assertEqual(code, 1)
        self.assertIn("E-001: kill criterion DIFFERS", out)
        self.assertIn("    concept: " + KILL + "\n", out)

    def test_whitespace_is_normalised_on_both_sides(self):
        code, out, err = self.check(log_row(assumption="people  use the\tfilters."))
        self.assertEqual((code, err), (0, ""))
        self.assertNotIn("DIFFERS", out)

    def test_without_a_path_the_concept_is_found_by_its_id_in_the_logs_folder(self):
        code, out, err = self.check(log_row(concept="CN-001 · bar at the bottom"))
        self.assertEqual((code, err), (0, ""))
        code, out, _ = self.check(log_row(concept="CN-001 · bar at the bottom", assumption="other"))
        self.assertEqual(code, 1)
        self.assertIn("E-001: assumption DIFFERS from CN-001 in frontier/2026-11-17-bar.md", out)

    def test_the_report_named_in_the_cell_may_be_outside_the_logs_folder(self):
        cell = "CN-001 · bar at the bottom (elsewhere/bar.md)"
        code, out, err = self.check(log_row(concept=cell, assumption="other"), where="elsewhere/bar.md")
        self.assertEqual(code, 1)
        self.assertIn("E-001: assumption DIFFERS from CN-001 in elsewhere/bar.md", out)
        self.assertEqual(err, "")

    def test_a_concept_not_found_is_a_note_and_the_exit_code_does_not_change(self):
        code, out, err = self.check(log_row(), report=None)
        self.assertEqual(code, 0)
        self.assertEqual(out, "1 experiments: 1 planned, 0 running, 0 kept, 0 killed, 0 inconclusive\n")
        self.assertIn("(E-001: the report the row names is not there, and no heading has Id CN-001 in frontier/; "
                      "its assumption, prediction and kill criterion were not compared)", err)
        code, out, err = self.check(log_row(concept="CN-002 · another"))
        self.assertEqual(code, 0)
        self.assertIn("(E-001: no heading has Id CN-002 in frontier/;", err)
        code, out, err = self.check(log_row(concept="CN-002 · another (frontier/2026-11-17-bar.md)"))
        self.assertEqual(code, 0)
        self.assertIn("(E-001: CN-002 is not in frontier/2026-11-17-bar.md, and no heading", err)

    def test_a_concept_under_two_headings_is_a_note(self):
        code, out, err = self.check(log_row(concept="CN-001 · c"), report=REPORT + "\n" + REPORT)
        self.assertEqual(code, 0)
        self.assertNotIn("DIFFERS", out)
        self.assertIn("(E-001: CN-001 is under 2 headings (frontier/2026-11-17-bar.md)", err)

    def test_a_line_wrapped_in_the_report_is_read_whole(self):
        report = REPORT.replace("- **Assumption:** people use the filters.\n",
                                "- **Assumption:** people use\n  the filters.\n")
        code, out, err = self.check(log_row(), report=report)
        self.assertEqual((code, err), (0, ""))
        self.assertNotIn("DIFFERS", out)
        code, out, _ = self.check(log_row(assumption="people use"), report=report)
        self.assertIn("    concept: people use the filters.\n", out)

    def test_the_next_item_or_an_empty_line_ends_the_value(self):
        report = REPORT.replace("- **Prediction:** at least 5 of 6 are faster at the bottom.\n",
                                "- **Prediction:** at least 5 of 6 are faster at the bottom.\n\nNot part of it.\n")
        code, out, err = self.check(log_row(), report=report)
        self.assertEqual((code, err), (0, ""))

    def test_a_cell_that_names_the_id_after_a_link_is_a_note(self):
        code, out, err = self.check(log_row(concept="[[2026-11-17-bar]] CN-001", assumption="other"))
        self.assertEqual(code, 0)
        self.assertNotIn("DIFFERS", out)
        self.assertIn("(E-001: the concept cell does not start with the concept's id;", err)

    def test_a_row_whose_concept_cell_starts_with_no_id_is_not_compared(self):
        code, out, err = self.check(log_row(concept="bar at the bottom", assumption="other"))
        self.assertEqual((code, err), (0, ""))

    def test_the_other_problems_are_still_reported_with_it(self):
        code, out, _ = self.check(log_row(kill="", assumption="other"))
        self.assertEqual(code, 1)
        self.assertIn("E-001: no kill criterion", out)
        self.assertIn("E-001: assumption DIFFERS", out)
        self.assertNotIn("kill criterion DIFFERS", out)


if __name__ == "__main__":
    unittest.main()
