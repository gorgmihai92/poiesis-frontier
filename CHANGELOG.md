# Changelog

## 1.3.1
A fix. The log keeps its ten columns and five statuses; no path, field or column is renamed or removed.
- **The row copies the concept.** The same assumption, prediction and kill criterion were written twice, in the
  concept and in its log row, and nothing checked that the two agreed; in the first real use they were already two
  wordings. `playbooks/experiment.md` now says the three cells are the concept's lines copied word for word (the
  kill criterion without its ` · written <date>`, which goes in `criterion written`), and that those three lines
  of the concept hold no `|`.
- **`experiments.py <log>` checks it.** For each row whose concept cell starts with a concept id, the concept is
  looked up in the report the cell names, else by its Id line in the notes next to the log; each of the three
  cells that differs from the concept's line, after the whitespace normalisation of a stamped sentence, is a
  `DIFFERS` problem (exit 1) showing both wordings. A concept line wrapped onto the next lines is read whole, as
  poiesis-insight reads a field. A concept not found, under two headings, or a concept cell that names the id but
  does not start with it, is a note on stderr and changes no exit code. Rows with no concept id are not compared,
  so the 1.1.4 output of the lab's test log is unchanged.
- **Rows written before 1.3.1.** A row that put the concept's lines in other words now gives `DIFFERS`, finished
  or not, until it is fixed. When the concept was not changed after the start, copy its three lines into the row.
  When the concept was edited after the experiment started, the row is the record of what was fixed in advance:
  that is the drift the check is for, so the concept goes back to the row's wording or the change becomes a new
  row, as the log's header says.
- **Tests.** `test_experiments.py`: a matching row, each cell differing, the ` · written` part, whitespace, a
  wrapped line, the report named in the cell or found by id, a concept not found or under two headings, an id
  after a link.
- **Not checked in this version:** any run on a topic.

## 1.3.0
Everything is added: no path, field or column of 1.2.0 was renamed or removed, and `experiments.py` reads every
file as before.
- **Properties.** `templates/report.md` is the top of every report in `frontier/<date>-<topic>.md`: a block of
  Obsidian properties (YAML between two `---` lines) with `type`, `plugin`, `date` and `topic`, then the title.
  The log's template starts with the same four; a result adds `id`, `status` and `from`, and a study design `id`
  and `from`. A report holds several concepts and the log several rows, so their properties carry no id: the Id,
  From, Stage, Verdict and Log id lines, the gate's Provisional or Stopped line and the log rows stay the record.
  The concept and artefact templates go inside a report and get no block.
- **The block is a copy.** `SKILL.md` asks for it to change in the same edit as what it copies, and for no
  experiment id to be linked.
- **Tests.** `test_templates.py`: the block in each template and its rules; the log check, the gate (with and
  without `--write`) and `ids` giving the same results with the block on a report, on the log and on the insight
  report the gate reads.
- **Docs.** The README's Design row names `poiesis-studio`, as the other READMEs do.
- **Not checked in this version:** how Obsidian shows the properties (no vault was opened), and any run on a topic.

## 1.2.0
All additions to the 1.1.4 file contract; nothing is renamed or removed.
- **Entry gate.** `experiments.py gate frontier/<note>.md [--write]` checks each concept's **From** against the
  challenge stamps of poiesis-insight (`insights/challenge-stamps.jsonl`, format 1), with this plugin's own code:
  through when every start is kept or weakened with an intact stamp and an unchanged sentence; provisional when a
  start could not be verified, in a **Provisional** line in the concept's own note; stopped when a start was
  dropped. A research question is followed one step to what it rests on. The experiment log is never written and
  keeps its five statuses.
- **Ids.** Concepts `CN-001`, study designs `ST-001`, each with **From**; `experiments.py ids CN|ST|E` gives the
  next free one, `ids --list` the ones in use. The concept cell of the log starts with the concept's id.
- **Evaluation that fits the stage** (`experiment.md`): sketch, probe, prototype, pilot; an early idea is
  criticised and compared, not usability-tested; the test follows from what the concept claims.
- **Three generation playbooks:** `design-space.md`, `estrangement.md` (a stranger's description, before and
  elsewhere, relabelling, an extreme character, a counter-function) and `recombination.md` (an ordinary base with
  one unusual pairing).
- **Distinct ideas** (`rules.md`): a report gives how many concepts were generated and how many are distinct.
- **Speculative research** (`speculative-research.md`): assumptions contested, two imaginary abstracts marked as
  fiction, a protocol written and dated before the data.
- **Speculative design** (`speculative.md`, `templates/artefact.md`): an artefact brief, two contrasting
  versions, the staging, and the fiction marked in the artefact itself.
- **Study design for a small group** (`study.md`, `templates/study.md`, saved in `frontier/studies/`) and
  `power.py`: what a sample can detect, checked against the worked examples of the G*Power manual and Lakens 2022.
- Twenty-three new research notes, each with how much of its source was read; `rules.md` ends with the list.
- Tests (`tests/`, offline) and eval cases (`plugins/poiesis-frontier/evals/`, not run). Scripts run on Python 3.9
  and later.

## 1.1.4
- Suggestions of another Poiesis plugin, from the skill or its agents, give the plugin's link and name the skill or
  agent to use.

## 1.1.3
- Convincing is not evidence: no invented specifics to persuade; each comes from a source or is marked "invented
  for the artefact". Concepts ranked by what their test would teach, not by appeal.
- Speculative design without foresight: names the drivers and their assumptions, and builds at least two
  contrasting futures.
- Two new research notes: Tversky & Kahneman 1983, Phadnis et al. 2015.

## 1.1.2
- Saving: files only at standard or thorough depth, when asked, when `frontier/` already exists, or for an
  experiment; otherwise the answer stays in the chat.
- Answers on its own without insight or research (speculative design labels its future "assumed") and says in
  one line which of them would make it more accurate.
- "Files": the paths and fields shared with the other Poiesis plugins, as a contract (changed only in a major
  version), in the skill and the README; other plugins' files are read tolerantly.

## 1.1.1
- Depth is set with a `Depth:` line in the project's `CLAUDE.md`, so it works without poiesis-research.

## 1.1.0
- Depth: quick, standard (default) or thorough, per request or `Depth:` in `research.config.md`. A few rules hold
  at every depth; the rest are defaults, skippable if the report says why. Every report ends with "Not checked".
  Rules limit what is reported as true, never what may be explored.
- The `experimentalist` agent runs at thorough depth or for many concepts; otherwise the playbook runs inline.
- Answers short and direct, the answer first; agents only for independent parallel parts or the thorough check;
  each agent has a word limit.
- "Other Poiesis plugins": when another one would change the result, Claude suggests it once and installs it only
  if the user agrees.
- README: the four toolkits, their roles, agents, what each reads and leaves, and how they connect.

## 1.0.0
- `frontier` skill: starts from what poiesis-insight kept, foresight scenarios and research gaps; never states
  conclusions.
- Playbooks: frame (what kind of problem it is), first principles, lateral (provocation, reversal, analogies),
  systems (loops, leverage points), concepts (what a thing is for), speculative design, experiment.
- Rules, each naming its source: every concept carries its starting point, assumption, prediction, smallest
  experiment and a kill criterion dated before the experiment runs.
- Agent: experimentalist.
- `experiments.py` checks the experiment log: status counts, overdue, kill criteria missing or written late.
- Results saved in `frontier/results/` for poiesis-insight to interpret.
