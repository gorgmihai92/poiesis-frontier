# G*Power 3.1 manual (Heinrich Heine University Düsseldorf, version of 1 June 2023)

- **Source:** the manual of the G*Power program, dated June 1, 2023 on its first page ·
  https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower (pages =
  PDF pages). The program is described in Faul, Erdfelder, Lang & Buchner 2007, Behavior Research Methods
  39(2): 175–191, https://doi.org/10.3758/BF03193146, which was not read.
- **File:** `../papers/gpower-2023-manual.pdf` (from the university's site)
- **Licence:** not stated in the pages read: kept local.
- **Evidence:** documentation of a program · worked examples with the program's output, some of them checked by
  its authors against Cohen's tables.
- **Read:** documentation, read on 2026-11-22: section 4, the exact test of one proportion against a constant
  (p. 11–12); section 19, the t test for two dependent means (p. 48–49); section 21, the t test for two
  independent means (p. 52). Not read: the other 28 sections.

## What it says
- **One proportion against a constant, exact binomial test** (p. 11–12). With a constant of 0.65, a true
  proportion of 0.80, a one-sided test at alpha 0.05 and 20 people: reject when 17 or more of the 20 show the
  event; the power is 0.411449 and the alpha actually reached is 0.044376.
- Because counts are whole numbers, the power of this test goes up and down as the sample grows; it does not
  rise smoothly (p. 12).
- **Two dependent means, matched pairs** (p. 48). With 50 pairs, an effect of dz = 0.421637, two-sided at
  alpha 0.05: noncentrality 2.981424, critical t 2.009575 with 49 degrees of freedom, power 0.832114. The
  manual says this replicates an example in Cohen (1969, p. 48), where the tables give 0.84. With
  dz = 0.2828427 the power is 0.500352.
- How the tests are computed: the null distribution is the central t; the alternative is the noncentral t, with
  noncentrality dz·√N and N − 1 degrees of freedom for pairs (p. 49), and d·√(n1·n2/(n1 + n2)) and N − 2
  degrees of freedom for two groups (p. 52).
- For the one-sample binomial case the null distribution is B(N, π0) and the alternative B(N, π0 + g) (p. 12).

## What it means for the plugin
- `power.py` computes power the way these pages describe: the noncentral t for comparisons of means, exact
  binomial sums for a count against a threshold.
- The tests of `power.py` check its output against the numbers above, to the digits the manual prints.
- Cohen's book was not read; the manual's statement that its example comes from it is taken as the manual's.

## Quotes
- "The computed power of 0.832114 is close to the value 0.84 estimated by Cohen using his tables." (p. 48)
- "we should reject the null hypothesis of π = 0.65 if in 17 out of the 20 possible cases the relevant event is observed" (p. 12)
