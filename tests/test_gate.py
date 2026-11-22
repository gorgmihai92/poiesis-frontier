"""The entry gate of experiments.py, on the stamps poiesis-insight writes.

fixtures/challenge-stamp-vectors.json and fixtures/gate/ are copies, byte for byte, of what the Insight 2.0.0
session left on 2026-11-22: three test vectors for the stamp format, and three conclusions (one kept and stamped,
one dropped and stamped, one never challenged) whose stamps were written by its challenge_stamp.py.
"""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import unicodedata
from pathlib import Path

import helpers
import experiments as ex

VECTORS = json.loads((helpers.FIXTURES / "challenge-stamp-vectors.json").read_text(encoding="utf-8"))["vectors"]
KEPT = "Topic A has more works each year than the year before, from 12 (2016) to 40 (2024)."  # IN-001 in the gate example
TODAY = "2026-11-22"

CONCEPTS = """# Gate test

### If topic A keeps growing, then a reading list by year shows the shift.

- **Id:** CN-001
- **From:** IN-001
- **Method:** first principles
- **Log id:** E-001

### If topic B is neglected, then a call for papers fills the gap.

- **Id:** CN-002
- **From:** IN-002
- **Log id:** E-002

### If the 2025 rise has no single source, then a per-country view explains it.

- **Id:** CN-003
- **From:** IN-003
"""


def concept(id_: str, start: str | None, extra: str = "") -> str:
    lines = [f"### If {id_} holds, then something follows.", "", f"- **Id:** {id_}"]
    if start is not None:
        lines.append(f"- **From:** {start}")
    return "\n".join(lines) + "\n" + extra + "\n"


def stamp_line(id_: str, verdict: str, date: str, text: str, **more) -> str:
    sha = ex.text_sha256(text)
    obj = {"v": 1, "id": id_, "verdict": verdict, "date": date, "text_sha256": sha,
           "seal": ex.seal(id_, verdict, date, sha), **more}
    return json.dumps(obj, ensure_ascii=False) + "\n"


class Project(unittest.TestCase):
    """A temporary project holding the Insight session's three conclusions and their two stamps."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve() / "project"
        self.root.mkdir()
        shutil.copytree(helpers.FIXTURES / "gate" / "insights", self.root / "insights")
        (self.root / "frontier").mkdir()
        self.note = self.root / "frontier" / "2026-11-22-topic.md"
        self.stamps = self.root / "insights" / "challenge-stamps.jsonl"
        self.insight = self.root / "insights" / "2026-11-17-gate-example.md"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def gate(self, text: str | None = None, *args: str) -> tuple[int, str]:
        if text is not None:
            self.note.write_text(text, encoding="utf-8")
        code, out, err = helpers.run(ex, ["gate", str(self.note), "--today", TODAY, *args])
        self.assertEqual(err, "")
        return code, out

    def edit(self, path: Path, old: str, new: str) -> None:
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")


class StampFormat(unittest.TestCase):
    def test_the_three_vectors_hash_and_seal_as_the_format_note_says(self):
        for v in VECTORS:
            stamp = v["stamp"]
            self.assertEqual(ex.text_sha256(v["text"]), stamp["text_sha256"], v["name"])
            self.assertEqual(ex.seal(v["id"], v["verdict"], v["date"], stamp["text_sha256"]), stamp["seal"], v["name"])
            self.assertTrue(ex.stamp_intact(stamp), v["name"])

    def test_the_normalised_text_has_the_number_of_bytes_the_note_gives(self):
        for v in VECTORS:
            self.assertEqual(ex.text_sha256(v["normalised"]), v["stamp"]["text_sha256"])
            self.assertEqual(len(v["normalised"].encode("utf-8")), v["normalised_utf8_bytes"])

    def test_the_third_vector_is_read_from_its_note(self):
        v = VECTORS[2]
        found = [b for b in ex.blocks(v["note"]) if ex.block_id(b) == "IN-003"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["heading"], v["text"])
        self.assertEqual(ex.shown_verdict(found[0]), "dropped")
        self.assertEqual(ex.text_sha256(found[0]["heading"]), v["stamp"]["text_sha256"])

    def test_layout_is_folded_and_nothing_else_is(self):
        base = ex.text_sha256("Slow growth, with no detectable change in rate.")
        self.assertEqual(base, "c54c859e8f85c160dac9ba94d4066d6a8eec8686ced2d25c485c08fc24acb95c")  # the note's worked example
        self.assertEqual(ex.text_sha256("  Slow growth,\r\n\twith no detectable\x0b\x0cchange in rate. "), base)
        for other in ("slow growth, with no detectable change in rate.", "Slow growth, with no detectable change in rate",
                      "Slow growth, with no detectable change in rate.", "Slow growth – with no detectable change in rate."):
            self.assertNotEqual(ex.text_sha256(other), base, other)

    def test_a_letter_typed_as_base_plus_accent_hashes_like_the_composed_letter(self):
        composed, split = "pădure", unicodedata.normalize("NFD", "pădure")
        self.assertNotEqual(composed, split)
        self.assertEqual(ex.text_sha256(composed), ex.text_sha256(split))

    def test_the_worked_example_of_the_format_note_verifies(self):
        line = ('{"v": 1, "id": "IN-004", "verdict": "weakened", "date": "2026-11-22", "text_sha256": '
                '"c54c859e8f85c160dac9ba94d4066d6a8eec8686ced2d25c485c08fc24acb95c", "seal": '
                '"3fe815f110e58f56a0c527f53ad71cbc3e34291bb547d15859f92f6e8c110cc5", "by": "agent", '
                '"where": "insights/2026-11-22-trends.md"}')
        self.assertTrue(ex.stamp_intact(json.loads(line)))

    def test_a_stamp_with_a_field_changed_is_not_intact(self):
        good = VECTORS[0]["stamp"]
        for change in ({"verdict": "weakened"}, {"date": "2026-11-23"}, {"id": "IN-009"}, {"v": 2}, {"v": True},
                       {"text_sha256": good["text_sha256"].upper()}, {"seal": "0" * 64}, {"verdict": "split"}):
            self.assertFalse(ex.stamp_intact({**good, **change}), change)
        self.assertTrue(ex.stamp_intact({**good, "by": "inline", "again": "new data", "unknown": 3}))


class ThreeConclusions(Project):
    """The lab plan's gate test, on the Insight session's three conclusions."""

    def test_a_concept_from_a_kept_conclusion_goes_through(self):
        code, out = self.gate(CONCEPTS)
        self.assertIn("THROUGH CN-001: every starting point is kept or weakened, with its stamp\n  IN-001 kept 2026-11-17\n", out)

    def test_a_concept_from_a_dropped_conclusion_is_stopped(self):
        code, out = self.gate(CONCEPTS)
        self.assertEqual(code, 1)
        self.assertIn("STOPPED CN-002: IN-002 was dropped\n  IN-002 dropped 2026-11-17\n", out)

    def test_a_concept_from_a_conclusion_nobody_challenged_is_provisional(self):
        code, out = self.gate(CONCEPTS)
        self.assertIn("PROVISIONAL CN-003: IN-003 could not be verified\n  IN-003 no stamp: no challenge is recorded\n", out)
        self.assertIn("3 concepts: 1 through, 1 provisional, 1 stopped.", out)
        self.assertIn("Stamps: insights/challenge-stamps.jsonl, 2 ids.", out)

    def test_write_marks_each_concept_in_its_own_note(self):
        code, out = self.gate(CONCEPTS, "--write")
        self.assertEqual(code, 1)  # CN-002 is stopped, marked or not
        self.assertIn("Saved: ", out)
        text = self.note.read_text(encoding="utf-8")
        self.assertIn("- **From:** IN-001\n- **Provisional:** no · IN-001 kept 2026-11-17 · checked 2026-11-22\n", text)
        self.assertIn("- **From:** IN-002\n- **Stopped:** IN-002 dropped 2026-11-17 · checked 2026-11-22\n", text)
        self.assertIn("- **From:** IN-003\n- **Provisional:** yes · IN-003 no stamp: no challenge is recorded · checked 2026-11-22\n", text)

    def test_write_adds_three_lines_and_changes_nothing_else(self):
        self.gate(CONCEPTS, "--write")
        after = self.note.read_text(encoding="utf-8").split("\n")
        kept = [line for line in after if "**Provisional:**" not in line and "**Stopped:**" not in line]
        self.assertEqual("\n".join(kept), CONCEPTS)
        self.assertEqual(len(after) - len(kept), 3)

    def test_write_twice_gives_the_same_bytes(self):
        self.gate(CONCEPTS, "--write")
        first = self.note.read_bytes()
        code, out = self.gate(None, "--write")
        self.assertEqual(self.note.read_bytes(), first)
        self.assertIn("Unchanged: ", out)

    def test_without_write_the_note_is_not_touched_and_the_missing_mark_is_named(self):
        code, out = self.gate(CONCEPTS)
        self.assertEqual(self.note.read_text(encoding="utf-8"), CONCEPTS)
        self.assertIn("NOT MARKED: the note has no line for this. Run again with --write, or put under the concept: "
                      "- **Provisional:** yes · IN-003 no stamp: no challenge is recorded · checked 2026-11-22", out)

    def test_the_experiment_log_and_the_insight_files_are_never_written(self):
        log = self.root / "frontier" / "experiments.md"
        log.write_text("| id | concept | assumption | prediction | kill criterion | criterion written | started | due | status | result |\n"
                       "|---|---|---|---|---|---|---|---|---|---|\n"
                       "| E-002 | CN-002 · a call for papers | a | p | fewer than 3 of 8 | 2026-11-20 |  | 2099-12-31 | planned |  |\n",
                       encoding="utf-8")
        before = {p: p.read_bytes() for p in (log, self.stamps, self.insight)}
        code, out = self.gate(CONCEPTS, "--write")
        self.assertEqual({p: p.read_bytes() for p in before}, before)
        self.assertIn("  E-002 is planned in frontier/experiments.md: a stopped concept gets no experiment\n", out)

    def test_a_marked_note_with_nothing_stopped_exits_0(self):
        two = concept("CN-001", "IN-001") + concept("CN-003", "IN-003")
        code, out = self.gate(two)
        self.assertEqual(code, 1)  # CN-003 is provisional and the note does not say so
        code, out = self.gate(None, "--write")
        self.assertEqual(code, 0)
        code, out = self.gate(None)
        self.assertEqual(code, 0)
        self.assertNotIn("NOT MARKED", out)

    def test_strict_fails_while_any_concept_is_provisional(self):
        two = concept("CN-001", "IN-001") + concept("CN-003", "IN-003")
        self.gate(two, "--write")
        self.assertEqual(self.gate(None, "--strict")[0], 1)
        self.gate(concept("CN-001", "IN-001"), "--write")
        self.assertEqual(self.gate(None, "--strict")[0], 0)


class WhatTheGateRefuses(Project):
    def test_a_verdict_edited_in_the_stamp_file_does_not_pass(self):
        self.edit(self.stamps, '"id": "IN-002", "verdict": "dropped"', '"id": "IN-002", "verdict": "kept"')
        self.edit(self.insight, "- **Challenge:** dropped ·", "- **Challenge:** kept ·")
        code, out = self.gate(concept("CN-002", "IN-002"))
        self.assertIn("PROVISIONAL CN-002", out)
        self.assertIn("IN-002 stamp altered: line 2 of insights/challenge-stamps.jsonl does not match its seal", out)

    def test_a_note_that_says_dropped_stops_the_concept_whatever_the_stamp_file_says(self):
        self.edit(self.stamps, '"id": "IN-002", "verdict": "dropped"', '"id": "IN-002", "verdict": "kept"')
        code, out = self.gate(concept("CN-002", "IN-002"))
        self.assertEqual(code, 1)
        self.assertIn("STOPPED CN-002", out)
        self.assertIn("IN-002 the note says dropped (its stamp was altered)", out)

    def test_a_sentence_changed_after_the_challenge_makes_the_concept_provisional(self):
        self.edit(self.insight, "more works each year", "more works")
        code, out = self.gate(concept("CN-001", "IN-001"))
        self.assertIn("PROVISIONAL CN-001", out)
        self.assertIn("IN-001 text changed: the sentence is not the one stamped kept on 2026-11-17", out)

    def test_a_label_retyped_from_weakened_to_kept_is_reported_and_the_stamp_is_used(self):
        v = VECTORS[1]
        (self.root / "insights" / "2026-11-22-methods.md").write_text(
            f"### {v['normalised']}\n\n- **Id:** IN-020\n- **Challenge:** **Kept** · retyped by hand\n", encoding="utf-8")
        with self.stamps.open("a", encoding="utf-8") as f:
            f.write(json.dumps({**v["stamp"], "id": "IN-020", "seal": ex.seal("IN-020", "weakened", v["date"], v["stamp"]["text_sha256"])}) + "\n")
        code, out = self.gate(concept("CN-001", "IN-020"))
        self.assertIn("THROUGH CN-001", out)
        self.assertIn('IN-020 weakened 2026-11-22 (the note shows "kept": the stamp is the record)', out)

    def test_a_label_retyped_from_dropped_to_kept_still_stops(self):
        self.edit(self.insight, "- **Challenge:** dropped ·", "- **Challenge:** kept ·")
        code, out = self.gate(concept("CN-002", "IN-002"))
        self.assertEqual(code, 1)
        self.assertIn('IN-002 dropped 2026-11-17 (the note shows "kept": the stamp is the record)', out)

    def test_a_label_that_says_dropped_stops_even_when_the_stamp_says_kept(self):
        self.edit(self.insight, "- **Challenge:** kept ·", "- **Challenge:** dropped ·")
        code, out = self.gate(concept("CN-001", "IN-001"))
        self.assertEqual(code, 1)
        self.assertIn("IN-001 the note says dropped (the stamp says kept, 2026-11-17: one of the two is wrong)", out)

    def test_a_damaged_stamp_file_lets_nothing_through(self):
        with self.stamps.open("a", encoding="utf-8") as f:
            f.write("<<<<<<< HEAD\n")
        code, out = self.gate(concept("CN-001", "IN-001"))
        self.assertIn("PROVISIONAL CN-001", out)
        self.assertIn("IN-001 stamp file damaged (line 3 is not JSON): no verdict in it can be trusted", out)
        self.assertIn("Stamps: insights/challenge-stamps.jsonl is damaged (line 3 is not JSON).", out)

    def test_a_line_that_is_json_but_not_a_stamp_damages_the_file(self):
        with self.stamps.open("a", encoding="utf-8") as f:
            f.write('["IN-001"]\n')
        self.assertIn("line 3 is not a stamp", self.gate(concept("CN-001", "IN-001"))[1])

    def test_the_last_line_for_an_id_is_the_one_in_force(self):
        with self.stamps.open("a", encoding="utf-8") as f:
            f.write(stamp_line("IN-001", "dropped", "2026-11-21", KEPT, again="new data"))
        code, out = self.gate(concept("CN-001", "IN-001"))
        self.assertEqual(code, 1)
        self.assertIn("STOPPED CN-001", out)
        self.assertIn("IN-001 dropped 2026-11-21", out)

    def test_an_altered_last_line_does_not_fall_back_to_the_earlier_one(self):
        line = json.loads(stamp_line("IN-001", "weakened", "2026-11-21", KEPT))
        line["verdict"] = "kept"
        with self.stamps.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line) + "\n")
        code, out = self.gate(concept("CN-001", "IN-001"))
        self.assertIn("PROVISIONAL CN-001", out)
        self.assertIn("IN-001 stamp altered: line 3", out)

    def test_an_id_under_two_headings_cannot_be_verified(self):
        (self.root / "insights" / "2026-11-20-copy.md").write_text(f"### {KEPT}\n\n- **Id:** IN-001\n", encoding="utf-8")
        code, out = self.gate(concept("CN-001", "IN-001"))
        self.assertIn("PROVISIONAL CN-001", out)
        self.assertIn("IN-001 is under two headings (insights/2026-11-17-gate-example.md, insights/2026-11-20-copy.md)", out)

    def test_with_no_stamp_file_nothing_was_challenged_on_record(self):
        self.stamps.unlink()
        code, out = self.gate(concept("CN-001", "IN-001"))
        self.assertIn("PROVISIONAL CN-001", out)
        self.assertIn('IN-001 no stamp: no challenge is recorded (the note shows "kept")', out)
        self.assertIn("Stamps: no file at insights/challenge-stamps.jsonl, so no challenge is on record here.", out)

    def test_a_stamp_whose_note_is_gone_passes_only_as_a_stop(self):
        self.insight.unlink()
        code, out = self.gate(concept("CN-001", "IN-001") + concept("CN-002", "IN-002"))
        self.assertIn("PROVISIONAL CN-001", out)
        self.assertIn("IN-001 kept 2026-11-17 on record, but no note with this id was found", out)
        self.assertIn("STOPPED CN-002", out)
        self.assertIn("IN-002 dropped 2026-11-17 (its note was not found, so the sentence was not compared)", out)

    def test_a_source_or_a_question_in_from_is_not_a_challenged_conclusion(self):
        code, out = self.gate(concept("CN-001", "IN-001, walters-2023, QN-002"))
        self.assertIn("PROVISIONAL CN-001: walters-2023 and QN-002 could not be verified", out)
        self.assertIn("  IN-001 kept 2026-11-17\n", out)
        self.assertIn("  walters-2023 no stamp, and no conclusion with this id in insights/ or foresight/\n", out)

    def test_a_question_is_not_a_conclusion_and_the_gate_says_what_it_rests_on(self):
        (self.root / "insights" / "2026-11-22-questions.md").write_text(
            "### Does a reading list by year change what students cite?\n\n- **Id:** QN-001\n- **From:** IN-001\n",
            encoding="utf-8")
        code, out = self.gate(concept("CN-001", "QN-001"))
        self.assertIn("PROVISIONAL CN-001: QN-001 could not be verified", out)
        self.assertIn("  QN-001 no stamp: it is not a conclusion and was not challenged; it rests on IN-001 kept 2026-11-17\n", out)

    def test_a_question_built_on_a_dropped_conclusion_stops_the_concept(self):
        (self.root / "insights" / "2026-11-22-questions.md").write_text(
            "### Why is topic B neglected?\n\n- **Id:** QN-002\n- **From:** IN-002, QN-002\n", encoding="utf-8")
        code, out = self.gate(concept("CN-001", "QN-002"))
        self.assertEqual(code, 1)
        self.assertIn("STOPPED CN-001: QN-002 rests on a dropped conclusion", out)
        self.assertIn("  QN-002 rests on a dropped conclusion (IN-002 dropped 2026-11-17)\n", out)

    def test_following_from_goes_one_step_and_never_lets_a_concept_through(self):
        (self.root / "insights" / "2026-11-22-questions.md").write_text(
            "### A.\n\n- **Id:** QN-003\n- **From:** QN-004\n\n### B.\n\n- **Id:** QN-004\n- **From:** IN-002\n",
            encoding="utf-8")
        code, out = self.gate(concept("CN-001", "QN-003"))
        self.assertIn("PROVISIONAL CN-001", out)
        self.assertIn("QN-003 no stamp: it is not a conclusion and was not challenged; it rests on QN-004 no stamp: no challenge is recorded", out)

    def test_one_dropped_start_among_several_stops_the_concept(self):
        code, out = self.gate(concept("CN-001", "IN-001, IN-002, IN-003"))
        self.assertEqual(code, 1)
        self.assertIn("STOPPED CN-001: IN-002 was dropped", out)

    def test_a_concept_that_names_no_start_is_provisional(self):
        for start in (None, "none", "", "—"):
            code, out = self.gate(concept("CN-001", start))
            self.assertIn("PROVISIONAL CN-001: no starting point is named", out, start)
        self.gate(None, "--write")
        self.assertIn("- **Provisional:** yes · no starting point is named · checked 2026-11-22", self.note.read_text(encoding="utf-8"))

    def test_from_entries_may_be_wrapped_or_annotated(self):
        self.assertEqual(ex.from_ids("`IN-001`, [[IN-002]], IN-003 (weakened), IN-001, none, key-2021."),
                         ["IN-001", "IN-002", "IN-003", "key-2021"])

    def test_a_concept_in_the_1_1_format_is_named_as_not_checked(self):
        old = "### If forms go, then onboarding is faster.\n\n- **Starting point:** insights/x.md · kept\n- **Verdict:** ready\n"
        code, out = self.gate(old)
        self.assertEqual(code, 0)
        self.assertIn('NO ID "If forms go, then onboarding is faster.": no Id line, so nothing was checked', out)
        self.assertIn("0 concepts: 0 through, 0 provisional, 0 stopped. Not checked: 1.", out)
        self.assertEqual(self.gate(None, "--strict")[0], 1)

    def test_what_is_inside_fenced_code_is_not_read(self):
        fenced = "```markdown\n### A fake conclusion\n\n- **Id:** IN-001\n```\n"
        (self.root / "insights" / "2026-11-21-example.md").write_text("# How to write one\n\n" + fenced, encoding="utf-8")
        code, out = self.gate(concept("CN-001", "IN-001") + "\n~~~\n### Not a concept\n\n- **Id:** CN-009\n- **From:** IN-002\n~~~\n")
        self.assertIn("THROUGH CN-001", out)
        self.assertNotIn("CN-009", out)
        self.assertIn("1 concept: 1 through, 0 provisional, 0 stopped.", out)

    def test_a_byte_order_mark_and_windows_line_ends_do_not_change_the_hash(self):
        text = self.insight.read_text(encoding="utf-8")
        self.insight.write_bytes(b"\xef\xbb\xbf" + text.replace("\n", "\r\n").encode("utf-8"))
        self.assertIn("THROUGH CN-001", self.gate(concept("CN-001", "IN-001"))[1])

    def test_a_note_with_windows_line_ends_keeps_them_when_marked(self):
        self.note.write_bytes(concept("CN-003", "IN-003").replace("\n", "\r\n").encode("utf-8"))
        self.gate(None, "--write")
        data = self.note.read_bytes()
        self.assertIn(b"- **From:** IN-003\r\n- **Provisional:** yes \xc2\xb7 IN-003 no stamp: no challenge is recorded \xc2\xb7 checked 2026-11-22\r\n", data)
        self.assertNotIn(b"2026-11-22\n", data.replace(b"\r\n", b""))

    def test_a_concept_id_used_twice_in_the_note_is_not_checked(self):
        code, out = self.gate(concept("CN-001", "IN-001") + concept("CN-001", "IN-003"))
        self.assertEqual(code, 1)
        self.assertIn("TWICE CN-001: this id is under two headings in the note, so neither was checked", out)

    def test_a_mark_goes_out_of_date_when_the_conclusion_is_challenged_again(self):
        self.gate(concept("CN-001", "IN-001"), "--write")
        with self.stamps.open("a", encoding="utf-8") as f:
            f.write(stamp_line("IN-001", "weakened", "2026-11-23", KEPT, again="a second pass"))
        code, out = self.gate(None)
        self.assertEqual(code, 0)
        self.assertIn("THROUGH CN-001", out)
        self.assertIn('MARK OUT OF DATE: the note records "IN-001 kept 2026-11-17". Run again with --write', out)
        self.assertEqual(self.gate(None, "--strict")[0], 1)

    def test_a_mark_typed_by_hand_with_the_wrong_state_is_named(self):
        text = concept("CN-003", "IN-003", "- **Provisional:** no · looks fine to me\n")
        code, out = self.gate(text)
        self.assertEqual(code, 1)
        self.assertIn("NOT MARKED: the note says otherwise.", out)
        self.gate(None, "--write")
        after = self.note.read_text(encoding="utf-8")
        self.assertNotIn("looks fine to me", after)
        self.assertEqual(after.count("**Provisional:**"), 1)

    def test_a_stopped_concept_that_was_cleared_loses_its_stopped_line(self):
        self.gate(concept("CN-002", "IN-002"), "--write")
        self.assertIn("**Stopped:**", self.note.read_text(encoding="utf-8"))
        self.edit(self.note, "- **From:** IN-002", "- **From:** IN-001")
        code, out = self.gate(None, "--write")
        text = self.note.read_text(encoding="utf-8")
        self.assertEqual(code, 0)
        self.assertNotIn("**Stopped:**", text)
        self.assertIn("- **Provisional:** no · IN-001 kept 2026-11-17 · checked 2026-11-22", text)

    def test_a_scenario_in_foresight_with_a_stamp_is_a_valid_start(self):
        (self.root / "foresight").mkdir()
        sentence = "By 2035 a designer signs for what a system does."
        (self.root / "foresight" / "2026-11-22-design.md").write_text(
            f"## {sentence}\n\n- **Id:** SC-001\n- **Challenge:** weakened · rests on one driver\n", encoding="utf-8")
        with self.stamps.open("a", encoding="utf-8") as f:
            f.write(stamp_line("SC-001", "weakened", "2026-11-22", sentence, where="foresight/2026-11-22-design.md"))
        code, out = self.gate(concept("CN-001", "SC-001"))
        self.assertIn("THROUGH CN-001", out)
        self.assertIn("SC-001 weakened 2026-11-22", out)

    def test_a_where_that_points_outside_the_project_is_not_followed(self):
        outside = self.root.parent / "outside-note.md"  # still inside this test's temporary folder
        outside.write_text("### Outside.\n\n- **Id:** IN-050\n", encoding="utf-8")
        with self.stamps.open("a", encoding="utf-8") as f:
            f.write(stamp_line("IN-050", "kept", "2026-11-22", "Outside.", where="../outside-note.md"))
        code, out = self.gate(concept("CN-001", "IN-050"))
        self.assertIn("PROVISIONAL CN-001", out)
        self.assertIn("no note with this id was found", out)

    def test_a_missing_note_is_a_usage_error(self):
        code, out, err = helpers.run(ex, ["gate", str(self.root / "frontier" / "nothing.md")])
        self.assertEqual(code, 2)
        self.assertIn("no such note", err)

    def test_the_project_is_found_from_the_note_not_from_where_the_command_runs(self):
        self.note.write_text(concept("CN-001", "IN-001"), encoding="utf-8")
        self.assertEqual(ex.project_root(self.note), self.root)


class Ids(Project):
    def test_the_next_id_counts_ids_that_are_only_mentioned(self):
        self.note.write_text(CONCEPTS + "\nSee also CN-007, which was removed.\n", encoding="utf-8")
        (self.root / "frontier" / "experiments.md").write_text("| E-012 | CN-002 | a | p | k | 2026-11-20 |  |  | planned |  |\n", encoding="utf-8")
        for prefix, want in (("CN", "CN-008"), ("E", "E-013"), ("ST", "ST-001")):
            code, out, err = helpers.run(ex, ["ids", prefix, str(self.root / "frontier")])
            self.assertEqual((code, out.strip()), (0, want))

    def test_list_names_every_id_and_fails_on_one_used_twice(self):
        self.note.write_text(CONCEPTS, encoding="utf-8")
        code, out, _ = helpers.run(ex, ["ids", "--list", str(self.root / "frontier")])
        self.assertEqual(code, 0)
        self.assertEqual([line.split()[0] for line in out.splitlines()], ["CN-001", "CN-002", "CN-003"])
        self.note.write_text(CONCEPTS + concept("CN-002", "IN-001"), encoding="utf-8")
        code, out, _ = helpers.run(ex, ["ids", "--list", str(self.root / "frontier")])
        self.assertEqual(code, 1)
        self.assertIn("TWICE CN-002: under 2 headings", out)

    def test_ids_needs_a_prefix_or_list(self):
        code, _, err = helpers.run(ex, ["ids"])
        self.assertEqual(code, 2)
        self.assertIn("give a prefix", err)


if __name__ == "__main__":
    unittest.main()
