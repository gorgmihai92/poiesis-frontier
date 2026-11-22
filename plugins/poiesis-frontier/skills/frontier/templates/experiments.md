---
type: experiment-log
plugin: poiesis-frontier
date: <YYYY-MM-DD, the day the log was started>
topic: "<the project, in a few words>"
---
# Experiment log

One row per experiment. The assumption, prediction and kill criterion are written (and `criterion written` dated)
before the experiment starts; changing them afterwards is a new row. `status`: planned, running, kept, killed,
inconclusive, and no other word. The concept cell starts with the concept's id. No cell holds a `|`, so a link
with an alias (`[[note|name]]`) is not used here. A new column goes after `result`.
Check with: `python3 -I <scripts>/experiments.py frontier/experiments.md`

| id | concept | assumption | prediction | kill criterion | criterion written | started | due | status | result |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | CN-001 · <concept, link to frontier note> | <must be true> | <expected observation> | <result that kills it> | 2026-10-17 |  | 2026-11-15 | planned |  |
