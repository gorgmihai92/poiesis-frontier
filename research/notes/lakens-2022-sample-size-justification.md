# Sample size justification (Lakens, 2022)

- **Source:** Collabra: Psychology 8(1): 33267 · https://doi.org/10.1525/collabra.33267 (pages = PDF pages of the
  author's version, which is laid out differently from the journal's)
- **File:** `../papers/lakens-2022-sample-size-justification.pdf` (the author's version, from osf.io/9d3yf)
- **Licence:** CC BY 4.0 for the published article (per Crossref); the file kept here is the author's version:
  kept local.
- **Evidence:** analytical · an overview of ways to justify a sample size, with worked examples computed in
  G*Power. A tutorial, not a study.
- **Read:** part of the text: the abstract (p. 1), the sections "Resource constraints" and the opening of
  "A-priori power analysis" with Table 3 (p. 4–6), the example on p. 7, "The minimal statistically detectable
  effect" (p. 12–13) and "Plot a sensitivity power analysis" (p. 17–19), on 2026-11-22. Not read: the sections
  on measuring a whole population, planning for accuracy, heuristics, the six ways to choose an effect size of
  interest other than those above, sequential analyses, and the reference list.

## What it says
- Six ways to justify a sample size: measure almost everyone, resource constraints, a power analysis in advance,
  a wanted accuracy, a heuristic, or saying openly that there is no justification (p. 1).
- Resources always limit a sample, so the limit should be stated and thought through, not hidden. The question
  becomes whether collecting the number one can afford is worth it (p. 4).
- When the sample is set by resources, report three things: the smallest effect that would come out
  statistically significant at that size; the width of the confidence interval to expect; and a sensitivity
  analysis, the effects the design can detect at several power levels such as 80%, 90% and 95% (Table 3, p. 6).
- If effects of the size one expects could not come out significant, say that the data will not be read
  through p values (Table 3, p. 6).
- A sensitivity power analysis fixes the sample size, the power and the alpha level, and answers which effect
  the study could detect (p. 17). It has no cut-off of its own: the detectable effects are compared with the
  effects that are plausible or worth caring about (p. 18).
- **Worked examples**, all for two independent groups compared with a two-sided t test at alpha 0.05:
  - to detect d = 0.4 with 90% power takes 133 people in each condition (p. 7);
  - with 15 in each group, only an observed difference above d = 0.75 is statistically significant (p. 12);
  - with 15 in each group, the study has 90% power for effects of at least d = 1.23 (p. 18);
  - with 50 in each group, a best-case guess of d = 0.57 gives a design in which observed effects below
    d = 0.4 are not significant (p. 13).

## What it means for the plugin
- The study playbook starts from the number of people that can be had, and asks `power.py` what that number
  can detect. It does not start from a guessed effect size and work back to a number nobody can recruit.
- A design reports its detectable effect at 80%, 90% and 95% power, and the smallest difference that would be
  significant. Where that is far above any plausible effect, the comparison is run as a description (counts,
  differences, what people said) and no significance test is claimed.
- `power.py` is tested against the four examples above.
- A tutorial read in part. The parts not read include sequential designs, which a later version could use.

## Quotes
- "a researcher would need to collect 133 participants in each condition" (p. 7)
- "only observed effects larger than d = 0.75 will be statistically significant" (p. 12)
- "the designed study has 90% power to detect effects of at least d = 1.23" (p. 18)
- "A sensitivity power analysis has no clear cut-offs" (p. 18)
