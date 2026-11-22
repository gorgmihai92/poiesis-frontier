"""The plugin's files hold together: eval cases in the format `claude plugin eval init --bare` writes, playbooks that
start by saying what they read, notes that say how much of their source was read, and the version in three places.
"""
from __future__ import annotations

import json
import re
import unittest

import helpers
import experiments as ex

EVALS = helpers.PLUGIN / "evals"
NOTES = helpers.ROOT / "research" / "notes"


def front_matter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    return dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)


class EvalCases(unittest.TestCase):
    def cases(self):
        return sorted(p for p in EVALS.iterdir() if p.is_dir())

    def test_there_are_six_cases_each_with_a_prompt_and_graders(self):
        self.assertEqual(len(self.cases()), 6)
        for case in self.cases():
            meta = front_matter((case / "prompt.md").read_text(encoding="utf-8"))
            for key in ("description", "runs", "max_turns", "allowed_tools"):
                self.assertIn(key, meta, case.name)
            graders = sorted((case / "graders").glob("*.md"))
            self.assertTrue(graders, case.name)
            for g in graders:
                kind = front_matter(g.read_text(encoding="utf-8")).get("type", "").strip()
                self.assertIn(kind, ("llm", "regex", "tool_used"), g)

    def test_no_grader_pattern_uses_an_inline_flag(self):
        # claude plugin eval compiles patterns with JavaScript's RegExp, which rejects (?i) and the like; a flag
        # goes in a `flags:` line, as in the cases of poiesis-research.
        for g in EVALS.rglob("graders/*.md"):
            meta = front_matter(g.read_text(encoding="utf-8"))
            for key in ("pattern", "input_match"):
                self.assertNotRegex(meta.get(key, ""), r"\(\?[a-zA-Z]", g)

    def test_the_readme_lists_every_case(self):
        readme = (EVALS / "README.md").read_text(encoding="utf-8")
        for case in self.cases():
            self.assertIn(f"`{case.name}`", readme)

    def test_the_stamp_in_the_dropped_case_is_intact_and_dropped(self):
        text = (EVALS / "dropped-start-is-stopped" / "prompt.md").read_text(encoding="utf-8")
        stamp = json.loads(next(l for l in text.splitlines() if l.startswith('{"v"')))
        self.assertTrue(ex.stamp_intact(stamp))
        self.assertEqual(stamp["verdict"], "dropped")
        self.assertEqual(stamp["text_sha256"], ex.text_sha256('Politics and polarization is a "neglected" topic.'))


class Playbooks(unittest.TestCase):
    NEW = ("design-space", "estrangement", "recombination", "speculative", "speculative-research", "study", "experiment")

    def test_each_new_or_changed_playbook_starts_with_read_first(self):
        for name in self.NEW:
            text = (helpers.SKILL / "playbooks" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("\n## Read first\n", text, name)

    def test_every_note_a_playbook_names_exists(self):
        for path in sorted((helpers.SKILL / "playbooks").glob("*.md")):
            for slug in re.findall(r"`([a-z][a-z-]+-\d{4}-[a-z0-9-]+)`", path.read_text(encoding="utf-8")):
                self.assertTrue((NOTES / f"{slug}.md").is_file(), f"{path.name}: {slug}")

    def test_every_note_says_how_much_was_read(self):
        for note in sorted(NOTES.glob("*.md")):
            self.assertRegex(note.read_text(encoding="utf-8"), r"\n- \*\*Read:\*\* ", note.name)

    def test_playbooks_say_power_py_and_the_gate_the_way_the_scripts_are_called(self):
        text = (helpers.SKILL / "playbooks" / "experiment.md").read_text(encoding="utf-8")
        self.assertIn("python3 -I $S/experiments.py gate frontier/<date>-<topic>.md --write", text)
        study = (helpers.SKILL / "playbooks" / "study.md").read_text(encoding="utf-8")
        for mode in ("see", "count", "two", "detect", "rate"):
            self.assertIn(f"power.py {mode}", study)


class Version(unittest.TestCase):
    def test_the_version_is_the_same_in_three_places(self):
        plugin = json.loads((helpers.PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((helpers.ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["version"], "1.3.0")
        self.assertEqual(market["plugins"][0]["version"], "1.3.0")
        self.assertTrue((helpers.ROOT / "CHANGELOG.md").read_text(encoding="utf-8").startswith("# Changelog\n\n## 1.3.0\n"))


if __name__ == "__main__":
    unittest.main()
