"""The properties block at the top of the report, the log, a result and a study design (1.3.0): what it holds,
the rules it keeps, and that experiments.py reads a log or a report with it as it reads one without it."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import helpers
import experiments as ex
from test_gate import CONCEPTS, TODAY, Project

TEMPLATES = helpers.SKILL / "templates"
COMMON = ["type", "plugin", "date", "topic"]
KEYS = {"report.md": COMMON, "experiments.md": COMMON, "result.md": COMMON + ["id", "status", "from"],
        "study.md": COMMON + ["id", "from"]}
FRAGMENTS = ("concept.md", "artefact.md")  # they go inside a report, so a block there would sit mid-file
PROPERTIES = '---\ntype: frontier-report\nplugin: poiesis-frontier\ndate: 2026-11-22\ntopic: "gate test"\n---\n'


def block_of(text: str) -> list[str]:
    lines = text.split("\n")
    if lines[0] != "---" or "---" not in lines[1:]:
        return []
    return lines[1: lines.index("---", 1)]


class TheBlock(unittest.TestCase):
    def test_each_file_template_starts_with_one_and_no_fragment_does(self):
        self.assertEqual(sorted(p.name for p in TEMPLATES.glob("*.md")), sorted([*KEYS, *FRAGMENTS]))
        for name, keys in KEYS.items():
            block = block_of((TEMPLATES / name).read_text(encoding="utf-8"))
            self.assertEqual([l.split(":", 1)[0] for l in block if not l.startswith(" ")], keys, name)
            self.assertIn("plugin: poiesis-frontier", block, name)
        for name in FRAGMENTS:
            self.assertFalse((TEMPLATES / name).read_text(encoding="utf-8").startswith("---"), name)

    def test_it_keeps_the_rules_the_other_plugins_need(self):
        for name in KEYS:
            for line in block_of((TEMPLATES / name).read_text(encoding="utf-8")):
                self.assertFalse(line.lstrip().startswith("#"), f"{name}: {line}")
                if line.startswith(" "):
                    self.assertRegex(line, r'^  - "\[\[[^\]|]+\]\]"$', name)
                else:
                    self.assertRegex(line, r'^[a-z]+:(?: (?:"[^"]*"|\[\]|<[^:"]*>|[a-z-]+))?$', f"{name}: {line}")


class TheLogReadsTheSame(unittest.TestCase):
    def test_the_log_check_prints_the_same_with_properties(self):
        log = helpers.FIXTURES / "logs" / "experiments.md"
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "experiments.md"
            copy.write_text(PROPERTIES.replace("frontier-report", "experiment-log") + log.read_text(encoding="utf-8"),
                            encoding="utf-8")
            with_ = helpers.run(ex, [str(copy)])
        without = helpers.run(ex, [str(log)])
        self.assertEqual(with_[0], without[0])
        self.assertEqual(with_[1].replace(str(copy), "LOG"), without[1].replace(str(log), "LOG"))


class TheGateReadsTheSame(Project):
    def test_the_gate_gives_the_same_result_with_properties(self):
        without = self.gate(CONCEPTS)
        with_ = self.gate(PROPERTIES + CONCEPTS)
        self.assertEqual(with_, without)
        self.assertIn("3 concepts: 1 through, 1 provisional, 1 stopped.", with_[1])

    def test_write_keeps_the_block_and_adds_the_same_three_lines(self):
        self.gate(CONCEPTS, "--write")
        without = self.note.read_text(encoding="utf-8")
        self.gate(PROPERTIES + CONCEPTS, "--write")
        self.assertEqual(self.note.read_text(encoding="utf-8"), PROPERTIES + without)

    def test_a_block_on_the_insight_report_changes_nothing(self):
        without = self.gate(CONCEPTS)
        self.edit(self.insight, "# Gate example", '---\ntype: insight-report\nplugin: poiesis-insight\n---\n# Gate example')
        self.assertEqual(self.gate(CONCEPTS), without)

    def test_ids_count_the_same(self):
        self.note.write_text(CONCEPTS, encoding="utf-8")
        without = helpers.run(ex, ["ids", "CN", str(self.root / "frontier")])
        self.note.write_text(PROPERTIES + CONCEPTS, encoding="utf-8")
        self.assertEqual(helpers.run(ex, ["ids", "CN", str(self.root / "frontier")]), without)
        self.assertIn("CN-004", without[1])


if __name__ == "__main__":
    unittest.main()
