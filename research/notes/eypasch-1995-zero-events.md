# Probability of adverse events that have not yet occurred: a statistical reminder (Eypasch, Lefering, Kum & Troidl, 1995)

- **Source:** BMJ 311(7005): 619–620 · https://doi.org/10.1136/bmj.311.7005.619
- **File:** none. PubMed Central (https://pmc.ncbi.nlm.nih.gov/articles/PMC2550668/) holds the abstract as text
  and the two pages as scanned images.
- **Licence:** © BMJ Publishing Group: closed.
- **Evidence:** a statistical note for surgeons · **abstract only**.
- **Read:** abstract only, on PubMed Central, on 2026-11-22. The two scanned pages, with the article's table,
  were not read.

## What it says (from the abstract)
- When an event has not occurred in n patients, the upper limit of the 95% confidence interval for its
  probability, the "maximum risk", can be estimated as 3/n, for n above 30. The abstract attributes the formula
  to Hanley (Hanley & Lippman-Hand 1983, JAMA, not read).
- The reminder: a reported rate of zero, or never having met a complication oneself, does not mean the risk is
  zero.

## What it means for the plugin
- `power.py rate --k 0` reports, for "none of n people showed it", how large the true rate could still be. It
  computes the exact bound, 1 − 0.05^(1/n), and prints 3/n next to it as the rule of thumb.
- The abstract gives the rule for n above 30. The exact bound is used for the small groups this plugin plans
  for; that calculation is the script's, not the article's.
- Abstract only: the article's own table and examples were not read, so none is quoted.
