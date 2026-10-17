# Changelog

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
