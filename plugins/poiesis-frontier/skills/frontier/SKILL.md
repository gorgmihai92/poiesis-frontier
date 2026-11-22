---
name: frontier
description: New concepts and the experiments that could prove them wrong, starting from what insight has already tested and checked by a script against the challenge stamps. Methods - first principles, lateral thinking (provocations, reversals, analogies), systems thinking (loops, leverage points), complexity (what kind of problem it is), philosophy of concepts (what a thing is for), design spaces, estrangement, recombination, speculative design (artefacts from foresight scenarios), speculative research (contested assumptions, imaginary abstracts, a protocol before the data), and study design for a small group with what its sample can detect. Frontier never states conclusions - every concept carries the assumption it tests, the smallest experiment that could prove it wrong, and what would kill it. Use when the user asks for new concepts, reframings, provocations, speculative artefacts, unconventional or "frontier" ideas, a design space, a study design, or experiments to test an idea.
---

# Frontier

Insight finds and tests patterns; frontier does not look for patterns itself. It starts from the conclusions insight
kept, the scenarios poiesis-foresight built, or the gaps research found, and turns them into concepts and experiments. The
experiments produce new data, which insight then reads.

| The user wants… | Playbook | Saved in |
|---|---|---|
| (always first) what kind of problem this is | `playbooks/frame.md` | in the frontier note |
| the parts that must be true, with the unneeded assumptions removed | `playbooks/first-principles.md` | `frontier/` |
| provocations, reversals, analogies from far-off fields | `playbooks/lateral.md` | `frontier/` |
| the loops of a system and where to push | `playbooks/systems.md` | `frontier/` |
| what a thing is for ("what is a button for?") | `playbooks/concepts.md` | `frontier/` |
| every way an interaction could work, and the cells nobody has tried | `playbooks/design-space.md` | `frontier/` |
| a familiar thing made strange: a stranger's description, relabelling, an extreme character, a removed function | `playbooks/estrangement.md` | `frontier/` |
| an ordinary base with one unusual pairing | `playbooks/recombination.md` | `frontier/` |
| artefacts from possible futures: brief, contrasting versions, staging, marked as fiction | `playbooks/speculative.md` | `frontier/` |
| whether a study is worth running: contested assumptions, an imaginary abstract, a protocol before the data | `playbooks/speculative-research.md` | `frontier/studies/` |
| a study for the user and a small group, and what its sample can detect | `playbooks/study.md`, `scripts/power.py` | `frontier/studies/` |
| (always last) the stage, the assumption, the smallest experiment, the kill criterion, the gate | `playbooks/experiment.md`, agent `experimentalist` | `frontier/experiments.md` |

## Every request

1. **Start from what was tested** (see "Input" below). Say what the starting points are and how each was tested.
   If there are none, the user's question is the start, and its premise becomes the first assumption to test.
   Answer on your own; where [poiesis-research](https://github.com/gorgmihai92/poiesis-research) (a premise nobody checked) or
   [poiesis-insight](https://github.com/gorgmihai92/poiesis-insight) (data to start from) or
   [poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight) (scenarios to start from) would make the concepts more accurate,
   say which and why in one line, with the link.
2. **Frame** with `playbooks/frame.md`: what kind of problem it is decides whether frontier fits and how big the
   experiments are.
3. **Generate** with one or more method playbooks. A request may combine them (e.g. first principles, then a
   reversal of the assumption that is left). Report how many concepts were generated and how many are distinct
   (`rules.md`, "Generating").
4. **Every concept goes through `playbooks/experiment.md`** before it is reported: the assumption it tests, the
   smallest experiment that could prove it wrong, and what would kill it, written before anything runs. At
   thorough depth (rules.md, "Depth"), or for many concepts at once, use the `experimentalist` agent; give it the
   concepts and the starting points, not the reasoning that produced them.
5. **Check the starting points** of saved concepts with the gate (`playbooks/experiment.md`, "The gate"). A
   concept from a dropped conclusion is stopped; one from a conclusion with no valid stamp is provisional, and
   says so. Copy the gate's lines; never retype a verdict.
6. **Follow `rules.md`**, the same for every playbook.

## Input

What frontier reads, if the project has it (it works without them too):
- `insights/<date>-<topic>.md` (poiesis-insight): start from insights marked **kept** or **weakened** (use the
  narrower claim). Dropped ones are not starting points; their reasons may still show an assumption worth testing.
  The label in the note is not the record: `insights/challenge-stamps.jsonl` is, and the gate reads it.
- `insights/` research questions (`QN-…`): a question is not challenged; the gate follows its From line one step.
- `foresight/<date>-<topic>.md` (poiesis-foresight): the scenarios (`SC-001`), what holds in every scenario and
  what in one only, the signals. Speculative design starts here. A scenario's challenge is checked like a
  conclusion's: by its stamp, when it has one.
- `foresight/forecasts.md` (poiesis-foresight): an open forecast can be the question an experiment answers.
- `research/README.md` and `research/notes/` (poiesis-research): the gaps ("not studied", disagreements). Cite back
  to the note and page.
- `frontier/experiments.md`: what was already tried, killed or kept; do not propose a killed concept again without
  saying what is different.
Frontier never edits these files; it writes only to `frontier/`.

## Output (when saved: SKILL.md, "Saving")

- `frontier/<YYYY-MM-DD>-<topic>.md`: its top from `templates/report.md` (properties and title), then starting
  points, frame, the concepts (`templates/concept.md`), each with its experiment.
- `frontier/experiments.md`: the experiment log (`templates/experiments.md`), one row per experiment.
- `frontier/results/<id>.md`: what an experiment produced (`templates/result.md`), with the raw data next to it.
  These are data for insight: to interpret them, the user asks poiesis-insight, which reads them as "your own data".
- `frontier/studies/<id>-<slug>.md`: a study design (`templates/study.md`), written and dated before any data.
- Concepts that survive their experiments go to building (poiesis-ui, poiesis-ux, or the project's own work).

Check the log with `python3 -I $S/experiments.py frontier/experiments.md`: open, overdue, kept, killed,
inconclusive, and rows missing a kill criterion or with a kill criterion written after the start.
Check what concepts start from with `python3 -I $S/experiments.py gate frontier/<date>-<topic>.md --write`, and
give ids with `python3 -I $S/experiments.py ids CN frontier` (`ST` for a study design, `E` for an experiment).
Say what a sample can detect with `python3 -I $S/power.py` (`detect`, `power`, `n`, `count`, `two`, `see`, `rate`).
Scripts are in `${CLAUDE_SKILL_DIR}/scripts` (called `$S`; if that path does not exist, Glob for
`**/frontier/scripts/experiments.py` under `~/.claude`). They need only Python 3 (3.9 or later); run them with
`python3 -I`.

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
Every suggestion, from the skill or an agent, gives the plugin's link (below) and names the skill or agent
to use, e.g. "[poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight), `foresight-analyst`".
- **[poiesis-research](https://github.com/gorgmihai92/poiesis-research)**: when a concept rests on a factual premise nobody has checked.
- **[poiesis-insight](https://github.com/gorgmihai92/poiesis-insight)**: when the question rests on data with no tested starting points yet,
  to challenge a conclusion a concept starts from (after its `challenger` answers, the session records the verdict
  with `challenge_stamp.py`, and the gate reads that stamp), and to
  interpret experiment results.
- **[poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight)**: when speculative design needs scenarios built from evidence and signals
  (`foresight-analyst`), not an assumed future.
- **poiesis-ui** ([poiesis-design](https://github.com/gorgmihai92/poiesis-design)): to build a concept that survived its experiment: how it looks.
- **poiesis-ux** ([poiesis-design](https://github.com/gorgmihai92/poiesis-design)): the same: how it behaves; its tester walks the prototype.

## Files shared with other Poiesis plugins
These paths and fields are a contract between the Poiesis plugins: rename or remove one only in a major version,
and say so in the changelog; adding fields is free. Read other plugins' files tolerantly: a missing file or field
means "unknown", said in the report, never an error.
- Writes `frontier/<date>-<topic>.md`: concepts with **Starting point**, **Assumption**, **Kill criterion**,
  **Verdict** and **Log id**; `frontier/experiments.md` (columns `id | concept | assumption | prediction | kill
  criterion | criterion written | started | due | status | result`); `frontier/results/<id>.md` ("What happened",
  "Against the kill criterion", "Not predicted (exploratory)", **Raw data**), read by poiesis-insight.
- Added in 1.2.0, all additive: each concept also has **Id** (`CN-001`), **From** (the ids it starts from,
  comma-separated), **Stage**, and one line the gate writes, **Provisional** (`yes` or `no` · why · checked
  date) or **Stopped** (why · checked date); `frontier/studies/<id>-<slug>.md`, a study design with **Id**
  (`ST-001`) and **From**; the concept cell of the log starts with the concept's id. The log keeps its ten
  columns and five statuses: "provisional" is never a status. A new log column would go after `result`, and no
  cell holds a `|`.
- Reads `insights/` (poiesis-insight: the **Id**, the **Challenge** line, and research questions with their
  **From**), `insights/challenge-stamps.jsonl` (the challenge stamps, format 1, verified with this plugin's own
  code), `foresight/` (scenarios with **Id** `SC-001`) and `research/notes/` (poiesis-research: gaps, "Later
  work"). Never writes outside `frontier/`.

Added in 1.3.0. Everything above is unchanged.
- A report, the log, a result and a study design start with a block of Obsidian properties, as their templates
  show (`type`, `plugin`, `date`, `topic`; a result adds `id`, `status` and `from`, a study design `id` and
  `from`). Copy the values from the file itself; the block is a copy for Obsidian's views, and the label lines,
  the gate's line and the log rows stay the record. In the block no line starts with `#`, text values are quoted,
  and a link is one quoted list item. Never put a link in a heading (the stamp and the gate hash it) or an **Id**
  line, or a link with an alias (`[[a|b]]`) in the log or any table.
- When a value the block copies changes in the file, change the block in the same edit. Inside a quoted value
  write `\"` for a quotation mark and `\\` for a backslash.
- Link a concept or a study by its id, `"[[CN-001]]"`, but never an experiment: `frontier/results/E-001.md` and the
  notebook's card for E-001 share the name.
