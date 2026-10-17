# Experiment (always last)

Every concept ends here. The goal is to find the cheapest way the concept could fail, not to show that it works.

For each concept:
1. **Assumption:** the one thing that must be true for it to work; the riskiest if there are several (most likely
   false, most costly if false).
2. **Prediction:** what you expect to observe if the assumption holds, as a number or an observable event.
3. **Smallest experiment:** the cheapest, fastest test that could make the prediction fail. Prefer, in this order:
   checking data the project already has; a paper or clickable prototype shown to a few people; a fake door or a
   manual version behind a real interface; a small live probe. Say who, how many, how long, what is measured.
4. **Kill criterion:** the result that kills the concept, fixed and dated before the experiment starts (Nosek et
   al. 2018). Also say what result would be inconclusive.
5. **Can it fail?** If no plausible result would kill the concept, the experiment is not a test; make it sharper or
   mark the concept "not testable yet" and say what would make it testable.
6. **Safe to fail:** what happens if it goes wrong, for the people in it and for the project. In a complex problem,
   run several small probes in parallel rather than one big one (Kurtz & Snowden 2003; van Beurden et al. 2011).
   Anything involving personal data, money, a public release or real users' work is proposed to the user, not run.

Verdict on the concept, with one line of reason:
- **Ready:** assumption, prediction, experiment and kill criterion are all clear; log it.
- **Sharpen:** one of them is vague; say which and how to fix it.
- **Not testable yet:** say what is missing.

## Log
Add each ready experiment to `frontier/experiments.md` (`templates/experiments.md`) with status `planned` and the
date the kill criterion was written. When it runs, set `running` and the start date. When it ends, write
`frontier/results/<id>.md` (`templates/result.md`) with the raw data next to it, and set the status:
- **kept:** the kill criterion was not met; the concept survives this test, nothing more.
- **killed:** the kill criterion was met.
- **inconclusive:** the experiment could not tell (too few people, the measure failed); say why.
Results that were not predicted are leads, marked exploratory. Interpreting the results is insight's job.
