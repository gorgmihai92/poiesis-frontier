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
2. **Frame** with `playbooks/frame.md`: what kind of problem it is decides whether frontier fits and how big the
   experiments are.
3. **Generate** with one or more method playbooks. A request may combine them (e.g. first principles, then a
   reversal of the assumption that is left).
4. **Every concept goes through `playbooks/experiment.md`** before it is reported: the assumption it tests, the
   smallest experiment that could prove it wrong, and what would kill it, written before anything runs. For
   independent experiment design, or several concepts at once, use the `experimentalist` agent; give it the
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

## Output

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
