---
name: frontier
description: New concepts and the experiments that could prove them wrong, starting from what insight has already tested. Methods - first principles, lateral thinking (provocations, reversals, analogies), systems thinking (loops, leverage points), complexity (what kind of problem it is), philosophy of concepts (what a thing is for), speculative design (artefacts from foresight scenarios). Frontier never states conclusions - every concept carries the assumption it tests, the smallest experiment that could prove it wrong, and what would kill it. Use when the user asks for new concepts, reframings, provocations, speculative artefacts, unconventional or "frontier" ideas, or experiments to test an idea.
---

# Frontier

Insight finds and tests patterns; frontier does not look for patterns itself. It starts from the conclusions insight
kept, the scenarios foresight built, or the gaps research found, and turns them into concepts and experiments. The
experiments produce new data, which insight then reads.

| The user wants… | Playbook | Saved in |
|---|---|---|
| (always first) what kind of problem this is | `playbooks/frame.md` | in the frontier note |
| the parts that must be true, with the unneeded assumptions removed | `playbooks/first-principles.md` | `frontier/` |
| provocations, reversals, analogies from far-off fields | `playbooks/lateral.md` | `frontier/` |
| the loops of a system and where to push | `playbooks/systems.md` | `frontier/` |
| what a thing is for ("what is a button for?") | `playbooks/concepts.md` | `frontier/` |
| artefacts from possible futures | `playbooks/speculative.md` | `frontier/` |
| (always last) the assumption, the smallest experiment, the kill criterion | `playbooks/experiment.md`, agent `experimentalist` | `frontier/experiments.md` |

## Every request

1. **Start from what was tested** (see "Input" below). Say what the starting points are and how each was tested.
   If there are none, the user's question is the start, and its premise becomes the first assumption to test.
   Answer on your own; where research (a premise nobody checked) or insight (data or scenarios to start from)
   would make the concepts more accurate, say which and why in one line.
2. **Frame** with `playbooks/frame.md`: what kind of problem it is decides whether frontier fits and how big the
   experiments are.
3. **Generate** with one or more method playbooks. A request may combine them (e.g. first principles, then a
   reversal of the assumption that is left).
4. **Every concept goes through `playbooks/experiment.md`** before it is reported: the assumption it tests, the
   smallest experiment that could prove it wrong, and what would kill it, written before anything runs. At
   thorough depth (rules.md, "Depth"), or for many concepts at once, use the `experimentalist` agent; give it the
   concepts and the starting points, not the reasoning that produced them.
5. **Follow `rules.md`**, the same for every playbook.

## Input

What frontier reads, if the project has it (it works without them too):
- `insights/<date>-<topic>.md` (poiesis-insight): start from insights marked **kept** or **weakened** (use the
  narrower claim). Dropped ones are not starting points; their reasons may still show an assumption worth testing.
- `foresight/<date>-<topic>.md`: the scenarios, the robust and contingent findings, the signals. Speculative design
  starts here.
- `foresight/forecasts.md`: an open forecast can be the question an experiment answers.
- `research/README.md` and `research/notes/` (poiesis-research): the gaps ("not studied", disagreements). Cite back
  to the note and page.
- `frontier/experiments.md`: what was already tried, killed or kept; do not propose a killed concept again without
  saying what is different.
Frontier never edits these files; it writes only to `frontier/`.

## Output (when saved: SKILL.md, "Saving")

- `frontier/<YYYY-MM-DD>-<topic>.md`: starting points, frame, the concepts (`templates/concept.md`), each with its
  experiment.
- `frontier/experiments.md`: the experiment log (`templates/experiments.md`), one row per experiment.
- `frontier/results/<id>.md`: what an experiment produced (`templates/result.md`), with the raw data next to it.
  These are data for insight: to interpret them, the user asks poiesis-insight, which reads them as "your own data".
- Concepts that survive their experiments go to building (poiesis-ui, poiesis-ux, or the project's own work).

Check the log with `python3 -I $S/experiments.py frontier/experiments.md`: open, overdue, kept, killed,
inconclusive, and rows missing a kill criterion or with a kill criterion written after the start.
Scripts are in `${CLAUDE_SKILL_DIR}/scripts` (called `$S`; if that path does not exist, Glob for
`**/frontier/scripts/experiments.py` under `~/.claude`). They need only Python 3; run them with `python3 -I`.

## Saving
Save the work (paths in the playbooks) when any of these holds: the depth is standard or thorough; the user asks;
the project already has the folder (`frontier/`), so it keeps a record; or something must be tracked later (an experiment with a kill criterion).
Otherwise (quick depth, a one-off question) answer in the chat only, and end with one line offering to save it.
Never create a folder the user did not want.

## Answers
Short and direct: the answer first, then what it rests on, in bullets or a table; no preamble, no recap. When the
work is saved, the chat gets the summary, the "Not checked" line and the file's path. Use an agent
only for independent parts that can run in parallel, or for the independent check at thorough depth; otherwise
work inline.

## Other Poiesis plugins
This plugin works alone. Suggest another one only when it would change the result: once, in one line, and go
on without it if the user says no (say what was left out). Check with `claude plugin list`; install only after
the user agrees, with `claude plugin marketplace add gorgmihai92/<repo>` and then
`claude plugin install <plugin>@<repo>` (it works after Claude Code restarts).
- **poiesis-research** (repo `poiesis-research`): when a concept rests on a factual premise nobody has checked.
- **poiesis-insight** (repo `poiesis-insight`): when the question rests on data with no tested starting points yet,
  and to interpret experiment results.
- **poiesis-ui** (repo `poiesis-design`): to build a concept that survived its experiment: how it looks.
- **poiesis-ux** (repo `poiesis-design`): the same: how it behaves; its tester walks the prototype.

## Files shared with other Poiesis plugins
These paths and fields are a contract between the Poiesis plugins: rename or remove one only in a major version,
and say so in the changelog; adding fields is free. Read other plugins' files tolerantly: a missing file or field
means "unknown", said in the report, never an error.
- Writes `frontier/<date>-<topic>.md`: concepts with **Starting point**, **Assumption**, **Kill criterion**,
  **Verdict** and **Log id**; `frontier/experiments.md` (columns `id | concept | assumption | prediction | kill
  criterion | criterion written | started | due | status | result`); `frontier/results/<id>.md` ("What happened",
  "Against the kill criterion", "Not predicted (exploratory)", **Raw data**), read by poiesis-insight.
- Reads `insights/` (poiesis-insight: the **Challenge** line), `foresight/` (scenarios) and `research/notes/`
  (poiesis-research: gaps, "Later work").
