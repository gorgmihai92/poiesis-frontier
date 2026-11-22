# Study design for a small group

A study the user can run with themselves and a small group: a few designers, students or colleagues. At that size
the study is a qualitative probe or a comparison between variants, and it says what it can and cannot detect
before anyone takes part.

## Read first
Notes in `research/notes` of the plugin's repository:
- `tohidi-2006-testing-many-is-better`, read in full. One experiment, 48 students, paper prototypes of a
  thermostat. A design seen alone was rated higher and criticised less than the same design seen among three;
  nobody who saw one design rejected it, three of twelve who saw three rejected one. Seeing three did not bring
  more suggestions.
- `dow-2010-parallel-prototyping`, read in full. One experiment, 33 novices making a web advertisement: building
  several prototypes before any feedback did better than getting feedback after each.
- `lakens-2022-sample-size-justification`, read in part. When resources set the sample, say what that sample can
  detect, with its smallest significant difference and a sensitivity analysis.
- `nielsen-1993-finding-usability-problems`, read in part: the chance of seeing a problem at least once in n
  people, if each shows it with probability p.
- `eypasch-1995-zero-events`, abstract only: none of n showed it does not mean the rate is zero.
- `nosek-2018-preregistration`, read in part: the plan before the data; a first round with few expectations is
  exploratory.
- `gpower-2023-manual`, documentation: how `power.py` computes.

## 1. What kind of study
Choose by what the concept claims and the stage it is at (`playbooks/experiment.md`):
- **A qualitative probe.** A few people meet the concept (a sketch, a paper prototype, an artefact) and what they
  do and say is recorded. It finds what happens and what people raise. It cannot say how often.
- **A comparison between variants.** The same people, or different people, meet two or three variants. Use it
  when the claim is that one variant does something the others do not.
- **A count against a criterion.** "At least 3 of 8 raise the question." A criterion on a count, fixed in
  advance, is how a small probe gets a kill criterion.

## 2. Variants, not one design
- Make two or three variants that differ in the one thing the concept is about, and show them together. A
  design shown alone collects higher ratings and fewer criticisms (Tohidi et al. 2006).
- Build the variants before showing any of them, and collect the reactions to all of them together. Feedback
  after each pulls toward repairing that one (Dow et al. 2010, novices, one kind of task).
- Ask people for problems, preferences and what they would reject. Do not ask them to design: in Tohidi et al.
  seeing more variants did not bring more suggestions.
- With the same people seeing every variant, change the order from person to person, so that being first is
  not mistaken for being better.

## 3. Who and how many
Start from the people that can be had, not from a number in a textbook (Lakens 2022).
1. **Who:** say who they are and how they are found. People from the user's own circle know the user and each
   other: their answers are less independent than the numbers below assume, and they are more polite. Say so in
   the design.
2. **How many:** the number that can really be had, in the time there is.
3. **What that number can detect,** with `power.py` (`$S` is the folder of the skill's scripts), before anyone
   takes part:

   | The question | Command | What it prints |
   |---|---|---|
   | Will a problem show up at all? | `power.py see --n 5 --p 0.1 --p 0.3` | how often a thing that p of people show turns up at least once |
   | Does my count criterion tell rates apart? | `power.py count --n 8 --at-least 3 --if 0.2 --if 0.6` | how often the criterion is met at each true rate |
   | Two variants, a yes/no outcome | `power.py two --n 8 --p1 0.2 --p2 0.8` | the least extreme significant outcome, and the power |
   | Two variants, a measure (time, a score) | `power.py detect --n 8` (different people) or `--paired` (the same people) | the smallest significant difference, and what is found 80, 90 and 95% of the time |
   | Nobody showed it, or k of n did | `power.py rate --n 8 --k 0` | the range the true rate could be in |

4. **No guessed effect size.** The detectable difference is compared with what is plausible. A plausible effect
   comes from the project's earlier data or from a source, with its note and page; otherwise write "unknown". An
   effect is never assumed in order to make a sample look large enough.
5. **If what can be detected is far above anything plausible,** the comparison is run as a description: counts,
   differences, what people said, with the range from `power.py rate`. No significance test is claimed, and the
   report says the study could not have detected a smaller difference. Not finding one is not evidence that
   there is none.

## 4. The protocol, before anyone takes part
Write `templates/study.md`, date it, and log the experiment (`playbooks/experiment.md`, "Log"):
- the question and the concept it tests (`From`), the kind of study, the variants and what differs between them;
- who, how many, how found, and in what order they meet the variants;
- what is collected and how (notes, a recording, a count); what is never collected (personal data beyond what is
  needed, anything that could identify someone in a published report);
- the prediction, the kill criterion, and what would be inconclusive;
- what the sample can detect, from `power.py`, pasted as printed;
- every comparison that will be made, and how the data will be read;
- consent: what people are told before they agree, including when something they meet is fiction
  (`playbooks/speculative.md`).

Anything involving personal data, money, a public release or real users' work is proposed to the user, never run
(`rules.md`). The user runs the sessions; this plugin designs them.

## 5. After
- What happened goes in `frontier/results/<id>.md` (`templates/result.md`): counts as observed, against the kill
  criterion fixed in advance, with what was not predicted marked exploratory.
- A first round with a small group is exploratory as a whole (Nosek et al. 2018). Its findings become predictions
  for a second round, with a new protocol.
- Interpreting the results is insight's job.
