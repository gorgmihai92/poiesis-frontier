# Speculative research

Decide whether a study is worth running, before any data exist: contest an assumption, imagine the paper the
study would lead to, then write its protocol. The output is a study design. Running it is the user's decision.

## Read first
Notes in `research/notes` of the plugin's repository:
- `alvesson-2011-problematization`, read in part (the method section; the worked illustration was not read). A
  research question comes from challenging what a body of work takes for granted, not only from a gap in it.
  The authors' test of a good challenge is that it is interesting. That is not evidence that it is true.
- `blythe-2014-imaginary-abstracts`, read in full. One author's essay on a technique from one project: write the
  abstract of a paper about a study that never happened, to see what the study could teach. He says plainly that
  an imagined finding is not a finding.
- `nosek-2018-preregistration`, read in part. A plan made before the outcomes are seen separates what was
  predicted from what was found afterwards. The authors say the experimental evidence that this makes findings
  more reproducible is not yet sufficient.
- `chambers-2013-registered-reports`: title only. Nothing here rests on it.

## 1. Contest the assumptions
If the project has research questions from poiesis-insight (`QN-…` in `insights/`), start from one and go to
step 2: its assumptions were contested there. Otherwise:

1. **The texts.** Choose one to three key texts from `research/notes`: a study that set the path, an
   authoritative summary, or a few recent influential pieces. Say how much of each was read. Narrow and deep is
   the point; this is not a literature review.
2. **What they treat as fact.** Turn statements that are taken as true into assumptions, and sort them:

   | Kind | It is | How to find it |
   |---|---|---|
   | in-house | shared inside one school of thought | follow that school's own debates |
   | root metaphor | the image the subject is seen through | name the image, then write a rival one |
   | paradigm | what exists, what counts as knowledge, which methods count | read from another world view without settling in it |
   | ideology | political, moral or gender-related | take a position with very different interests, or treat something seen as negative as possibly positive |
   | field | shared even by schools that oppose each other | look for what the opposing camps never debate; look at another field |

   One row per assumption: the assumption, its kind, the note and page where it shows.
3. **Choose one.** Not every assumption is worth contesting: ask what contesting it would open. A broad one can
   be contested superficially; a sharp challenge to a narrow one can matter as much.
4. **The alternative.** Write what would hold if the assumption were false. Do not borrow a ready-made
   counter-position from a rival school.
5. **Obvious, absurd or interesting.** If the alternative confirms what the field already assumes, it is obvious.
   If it denies everything, it is absurd. It is worth a study when it accepts some of what the field assumes and
   denies some. If the user can, try it on one or two people from the field.
6. **The question.** Write the question the alternative leads to, in one sentence. It is a question, with the
   assumption it contests named; it is not a finding.

## 2. An imaginary abstract
7. Write the abstract of the paper the study would become: the problem it frames, the study (who, what, how
   many), the findings, what follows from them. About 150 words.
8. **Write it twice:** once with the finding hoped for, once with the opposite or with nothing found.
9. The first line of each is: `IMAGINARY ABSTRACT: no such study has been run.`
10. Ask of each version: would it teach something the field does not already assume? Would the second version be
    worth reporting? If neither would, drop the study or change it. If only the hoped-for version would, the
    study cannot fail in an informative way: reshape it (`playbooks/experiment.md`, "Can it fail?").
11. Both versions go in the study design, under its heading "Imagined" (`templates/study.md`). They are never
    saved in `frontier/results/`, never cited, and never shown without their first line.

## 3. A protocol before the data
12. Write the study design from `templates/study.md` and `playbooks/study.md`, before any data exist: the
    question, who and how many, what is collected, the prediction, what would count against it, what the sample
    can detect, every comparison that will be made, what will be left out, how it will be read.
13. **Date it.** A change after that date is written under "Changes", with its date and its reason. A change made
    before the outcomes are seen is a correction; one made after is reported as such.
14. **If data already exist,** say who has seen them and what was passed on. What was known in advance is part of
    the protocol.
15. **What the plan does not cover is exploratory.** Anything found outside the planned comparisons is a lead for
    a next study. A first round with a small group is exploratory as a whole, and its report says so.
16. Give the design the next id (`python3 -I $S/experiments.py ids ST frontier`), save it as
    `frontier/studies/<id>-<slug>.md` with `- **From:**` naming the concept or the question it tests, and log
    the experiment (`playbooks/experiment.md`, "Log").

## Out
- In the frontier note: the table of assumptions, the one contested and its alternative, the question.
- In `frontier/studies/`: the protocol, with the two imaginary abstracts under "Imagined".
- In the chat: the question, what each version of the abstract would teach, what the sample can detect, and
  **Not checked**. No sentence in any of them reports the imagined finding as a result.
