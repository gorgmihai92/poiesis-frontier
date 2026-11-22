# Experiment (always last)

Every concept ends here. The goal is to find the cheapest way the concept could fail, not to show that it works.

## Read first
Notes in `research/notes` of the plugin's repository (`rules.md`, "Sources"):
- `greenberg-2008-usability-evaluation-harmful`, read in full. An essay by two practitioners of usability
  testing: testing a sketch as if it were a prototype finds problems every sketch has and can kill the idea;
  usability testing belongs after several ideas were generated and compared. It asks for tests that try to
  refute. Reasons and examples, no measurements.
- `olsen-2007-evaluating-ui-systems-research`, read in full. One author's position on tools for programmers and
  designers: the evaluation follows from the claim, and a new thing is not rejected for what it leaves out.
  Applying it to early concepts in general is this plugin's step.
- `nosek-2018-preregistration`, read in part: prediction and postdiction; a plan fixed before the outcomes.
- `kurtz-2003-cynefin` (abstract only) and `vanbeurden-2011-cynefin`: small probes in complex problems.

## Before the experiment
1. **Id.** Give the concept the next free id: `python3 -I $S/experiments.py ids CN frontier` prints it.
2. **From.** Write the ids the concept starts from: `- **From:** IN-004, SC-001`. Use the ids as they are in the
   notes; write `none` when the start is the user's question alone.
3. **Stage.** Say which of the four the concept is at. The stage decides the kind of test, never whether there
   is one.

| Stage | What exists | The test that fits | The kill criterion is about | Does not fit yet |
|---|---|---|---|---|
| **sketch** | the idea in words or a rough drawing, with holes | a critique (why it is so, what else was considered, where it would fail), next to at least two other sketches; a check against data the project already has | the assumption: does what the concept rests on hold? | a usability test: it finds the problems every sketch has and says nothing about the idea (Greenberg & Buxton 2008) |
| **probe** | something a few people can react to: a paper or clickable mock, a fake door, a speculative artefact | two or three variants in front of a few people; what they do and say is recorded (`playbooks/study.md`) | whether people do what the concept predicts: take it up, choose it, raise the question | task times, error counts, ratings of polish |
| **prototype** | it works well enough to do its task | a comparison with the way things are done now, set up so that it can come out against the concept; usability problems count from here | the claim, against a named alternative: faster, fewer errors, preferred | claims about what people will do over months |
| **pilot** | a small group uses it for real, over weeks | what people keep doing with it when nobody watches, and what they stop doing | use over time | — |

   The four names are the lab's ladder (sketch, probe, prototype, pilot) and are a product decision. What fits
   each stage follows the two sources above.
4. **What does the concept claim?** The test follows from the claim (Olsen 2007). "This can now be done at all" is
   shown by doing it once, in front of someone. "This is better" needs a comparison. Olsen's rule of thumb for
   new tools: a difference that needs careful statistics to show at all is probably not important.

## For each concept
1. **Assumption:** the one thing that must be true for it to work; the riskiest if there are several (most likely
   false, most costly if false). A missing feature is not an assumption: anything new leaves things out.
2. **Prediction:** what you expect to observe if the assumption holds, as a number or an observable event.
3. **Smallest experiment:** the cheapest, fastest test that could make the prediction fail, of the kind the stage
   allows. Prefer, in this order: checking data the project already has; a critique next to other sketches; a
   paper or clickable prototype shown to a few people; a fake door or a manual version behind a real interface;
   a small live probe. Say who, how many, how long, what is measured. With people, use `playbooks/study.md`.
4. **Kill criterion:** the result that kills the concept, fixed and dated before the experiment starts (Nosek et
   al. 2018). Also say what result would be inconclusive. For a criterion on a count ("fewer than 3 of 8"),
   `python3 -I $S/power.py count --n 8 --at-least 3` shows which true rates it can tell apart.
5. **Can it fail?** If no plausible result would kill the concept, the experiment is not a test; make it sharper or
   mark the concept "not testable yet" and say what would make it testable. For a variation on something
   established, a test built so that the concept wins once is the weak kind (Greenberg & Buxton 2008).
6. **Safe to fail:** what happens if it goes wrong, for the people in it and for the project. In a complex problem,
   run several small probes in parallel rather than one big one (Kurtz & Snowden 2003, abstract only; van Beurden
   et al. 2011). Anything involving personal data, money, a public release or real users' work is proposed to the
   user, not run.

Verdict on the concept, with one line of reason:
- **Ready:** assumption, prediction, experiment and kill criterion are all clear; log it.
- **Sharpen:** one of them is vague; say which and how to fix it.
- **Not testable yet:** say what is missing.

## The gate
When the concepts are saved, check what they start from before any experiment is logged:

```
python3 -I $S/experiments.py gate frontier/<date>-<topic>.md --write
```

It prints one line per concept and writes the result under the concept (`rules.md`, "Starting points are checked,
not trusted"):
- **THROUGH:** go on.
- **PROVISIONAL:** go on, and say "provisional" with its reason wherever the concept is shown. Its experiment is
  logged as usual.
- **STOPPED:** no experiment. Keep the concept in the note under its Stopped line. If the reason the conclusion
  was dropped shows an assumption worth testing, write a new concept from another start.

Copy the gate's lines into the report as they are. The script needs only Python 3; it works when poiesis-insight
is not installed, and then every conclusion counts as not challenged on record. Without saved files there is
nothing to check: say in the chat which starting points are untested.

## Log
Add each ready experiment to `frontier/experiments.md` (`templates/experiments.md`) with status `planned` and the
date the kill criterion was written. Start the concept cell with the concept's id (`CN-001 · …`); no cell holds a
`|`. When it runs, set `running` and the start date. When it ends, write `frontier/results/<id>.md`
(`templates/result.md`) with the raw data next to it, and set the status:
- **kept:** the kill criterion was not met; the concept survives this test, nothing more.
- **killed:** the kill criterion was met.
- **inconclusive:** the experiment could not tell (too few people, the measure failed); say why.
The log has these five statuses and no other. Results that were not predicted are leads, marked exploratory.
Interpreting the results is insight's job.
