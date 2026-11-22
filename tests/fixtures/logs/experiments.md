# Experiment log (test fixture)

These are not real experiments. Each row exercises one behaviour of `experiments.py`, and
`../expected/experiments.txt` is what the script must print. Due dates are in the past or in 2099, so the result
does not depend on the day the check runs.

| id | concept | assumption | prediction | kill criterion | criterion written | started | due | status | result |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | Planned and in order | a | p | fewer than 3 of 8 raise the question | 2026-11-17 |  | 2099-12-31 | planned |  |
| E-002 | Running past its due date | a | p | difference under 5 points | 2026-01-10 | 2026-01-15 | 2026-02-01 | running |  |
| E-003 | Finished and kept | a | p | difference under 5 points | 2026-01-01 | 2026-01-05 | 2026-02-01 | kept | criterion not met |
| E-004 | Finished and killed | a | p | difference under 5 points | 2026-01-01 | 2026-01-05 | 2026-02-01 | killed | criterion met |
| E-005 | Finished with no result | a | p | difference under 5 points | 2026-01-01 | 2026-01-05 | 2026-02-01 | inconclusive |  |
| E-006 | No kill criterion and no date | a | p |  |  |  | 2099-12-31 | planned |  |
| E-007 | Kill criterion written after the start | a | p | difference under 5 points | 2026-03-10 | 2026-03-01 | 2099-12-31 | running |  |
| E-008 | A status the script does not know | a | p | difference under 5 points | 2026-01-01 |  | 2099-12-31 | provisional |  |
| E-009 | Too few cells | a | p | difference under 5 points | 2026-01-01 |
