# Two recorded runs of the Poiesis plugins (Poiesis Lab notebook, 17 November 2026)

- **Source:** the owner's Poiesis Lab notebook, a private folder: `fixtures/` (data of two runs of 2026-11-17, with
  its `README.md`) and `lab/plan.md` (the lab plan approved on 2026-11-21). Not public. Copied here: one sentence
  in `tests/fixtures/gate/` (IN-003, from the trend-scan run; the other two there are synthetic, for the test).
  Nothing else here comes from a recorded run: the vectors of `tests/fixtures/challenge-stamp-vectors.json` are
  synthetic, for the test, made-up text that reports nothing real.
- **File:** none here.
- **Licence:** the owner's own material.
- **Evidence:** observation of two runs · what went wrong in them is the reason for several checks in 1.2.0.
- **Read:** on 2026-11-22: `lab/plan.md` in full; `fixtures/README.md` in full; the first row of
  `fixtures/trend-scan/challenge.published.json` and of `challenge.corrected.json`. Not read: the other fixture
  files. The sessions themselves were not saved as files, so what the plan says about them could not be checked
  against a record.

## What was observed
- **A verdict label drifted when it was retyped.** In `challenge.published.json`, the file the published page
  used, row `c6` has the verdict "kept". In `challenge.corrected.json` the same row has "weakened", which the
  fixtures' README gives as the challenger's verdict. Seen in both files on 2026-11-22.

## What the plan states about the runs (read in the plan, not checked against a record)
- A starting point that had been dropped was not flagged when a concept was built on it.
- The effect sizes in the experiments proposed were guessed.
- Of 16 conclusions sent to the challenger, one came back unchanged.
- Rules that would have prevented these existed in the plugins and were not applied, because nothing applied
  them by code.

## What it means for the plugin
- The entry gate is a script (`experiments.py gate`), and the Provisional and Stopped lines are written by it,
  not typed.
- A study design says what its sample can detect (`power.py`), and does not assume an effect size.
- The three sentences in the plan's own words are reasons the owner gave for this version. They are product
  decisions resting on his account of the runs, not findings.
