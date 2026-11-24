# Tests

Tests for the scripts in `plugins/poiesis-frontier/skills/frontier/scripts` and for how the plugin's files hold
together. They need Python 3.9 or later and nothing else, and never use the network.

```
python3 -I -m unittest discover -s tests
```

This folder is not part of the plugin, so it is not installed with it.

| File | What it checks |
|---|---|
| `test_power.py` | `power.py` against the worked examples of the G*Power 3.1 manual and of Lakens 2022, the lab plan's "five checks leave up to 45%", and second calculations made another way (closed forms, a simulation, exact fractions) |
| `test_gate.py` | the stamp format's three test vectors; the gate on the three stamped conclusions of poiesis-insight (kept goes through, dropped is stopped, never challenged is provisional); what the gate refuses; the reading rules of the stamp format; `ids` |
| `test_experiments.py` | the experiment log check prints what 1.1.4 printed for the lab's test log, line for line; a row's assumption, prediction and kill criterion against the concept's lines (1.3.1) |
| `test_files.py` | the eval cases' format, "Read first" in the playbooks, a **Read** line in every new note, the version in three places |

## Fixtures

- `fixtures/challenge-stamp-vectors.json` and `fixtures/gate/insights/` are byte-for-byte copies of
  `tests/vectors/challenge-stamp.json` and `tests/fixtures/gate/insights/` in gorgmihai92/poiesis-insight at
  `229aa06` (2.0.0). The two stamps were written by its `challenge_stamp.py`.
- `fixtures/logs/experiments.md` and `fixtures/expected/experiments.txt` are copies of the Poiesis Lab notebook's
  test log and the output it expects; the notebook's own `fixtures/check.py` runs the same comparison there.
