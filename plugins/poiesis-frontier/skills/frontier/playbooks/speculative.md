# Speculative design

Build artefacts from possible futures to make people think, and to find out what they value (after Dunne & Raby).
The starting point is a foresight scenario, not a guess. Four parts: a brief, contrasting versions, a staging,
and telling people it is fiction.

## Read first
Notes in `research/notes` of the plugin's repository:
- `auger-2013-speculative-design`, abstract only: the perceptual bridge, and the two purposes (thinking about the
  future, criticising current practice).
- `phadnis-2015-scenario-planning`: one scenario steers judgement toward itself.
- `mancini-2010-contravision`, read in full. Sixteen people in four groups saw one of two versions of the same
  story about an imagined technology, one where it goes well and one where it goes badly. The two versions drew
  different concerns. It did not compare two versions with one.
- `elsden-2017-speculative-enactments`, read in part (the method and its guidelines). People act inside a
  staged speculation that matters to them; they are in on it, give consent, and are debriefed.
- `coulton-2016-design-fiction-deception`, read in full. Plausible fiction slides into deception, often by
  accident: a fiction marked as such was still taken for real when it copied a familiar format.

None of these is a study of whether speculative design changes what people decide. The lab plan names published
critiques of the practice (Bardzell & Bardzell 2013, Pierce 2021, Tonkinwise 2014); they were not read for this
version.

## 1. The scenario
Take one scenario from `foresight/` if the project has it, with its drivers and what holds in every scenario and
what in one only. Its id (`SC-001`) goes in the concept's From line, so the gate checks its challenge. Without
one, build the future from the user's question, label it "assumed, not from foresight", and go on: name its 2–3
drivers and the assumption under each, and build at least two contrasting futures (or say why one is enough), so
none reads as a prediction (Phadnis et al. 2015). Then say in one line what would make it more accurate:
[poiesis-insight](https://github.com/gorgmihai92/poiesis-insight)'s foresight (`foresight-analyst`) for scenarios
built from evidence and signals, [poiesis-research](https://github.com/gorgmihai92/poiesis-research)
(`evidence-scout`) for the facts behind the drivers, or both.

## 2. The artefact brief
Fill `templates/artefact.md` before making anything:
- **Everyday object of that future:** what ordinary thing would exist there (a product, a form, a rule, a
  service, a notice, an app screen). Ordinary things say more about a future than spectacular ones.
- **Purpose:** for thinking about the future, or for criticising current practice (Auger 2013), and the one
  question it should raise in the people who meet it.
- **Perceptual bridge:** close enough to the present to be understood, far enough to make people stop and think.
  Say what makes it plausible: the technology, the look, the behaviour, how it is used (Auger 2013). Too far and
  people dismiss it; too near and it reads as a product.
- **What it is made of:** form, words on it, how people meet it. Every specific on it (a number, a name, a date,
  a quote) comes from a source or is marked "invented for the artefact" in the brief.
- **Its format, and how it is marked as fiction** (section 5). The brief is not finished without this line.

## 3. Contrasting versions
Make two versions of the same artefact, set in the same scene with the same people: one where it goes well and
one where it goes badly (Mancini et al. 2010). Keep everything else the same, so a reaction can be traced to
what differs. Say in the brief what differs between them.

Show each version to different people, or both to the same people, and say which: with one version each, a
concern that comes up under only one version is a lead about the telling, not about the thing. Mancini et al.
showed each group one version; whether one group should see both is not settled in what was read.

## 4. The staging
How people meet the artefact (Elsden et al. 2017):
1. **A familiar routine as the scene:** an everyday situation people already know how to act in. It keeps the
   speculation ordinary and checks wilder utopias and dystopias.
2. **Pilot the materials** with a colleague or a friend first: does the set-up make sense to them?
3. **Who and how many:** chosen for whom the artefact matters; say how they are found. With the small group this
   lab works with, use `playbooks/study.md` for the numbers.
4. **Your own role** in the staging (host, shop assistant, interviewer), and what is recorded. Recording can
   spoil what it records: decide what is needed and no more.
5. **A debrief** afterwards, off-stage: what people thought it was, what they would keep, and what they now know
   is fiction.

The experiment is the staging, with the kill criterion fixed in advance (e.g. "fewer than 3 of 8 people raise
the question the artefact was made for"; `python3 -I $S/power.py count --n 8 --at-least 3` shows which true rates
that can tell apart). It goes through `playbooks/experiment.md`; the responses are data for insight. What people
say records their reaction to this artefact, today, told this way. It is not how the future will be.

## 5. Telling people it is fiction
- **In the artefact itself,** where it cannot be cropped away: a line on it, on every page or screen, not only a
  keyword or a closing remark. Coulton, Lindley & Akmal (2016) found that a fictional paper labelled as fiction
  in its keywords and its conclusion was not fully grasped as fiction by its reviewers.
- **Before and after:** said aloud when people agree to take part, and again in the debrief.
- **The more familiar the format, the stronger the mark.** An artefact in the form of a research paper, a news
  item, a product page, an advertisement or an official notice is the risky case.
- **Nobody is told it is real,** for attention or for a more natural reaction. A staging that needs people to
  believe it is real is not run.
- **Nothing fictional is released in public** unmarked; any public release is proposed to the user, never done
  (`rules.md`).

## Out
- The brief (`templates/artefact.md`), the two versions, the staging and the kill criterion, in the frontier
  note.
- Each artefact is a concept with an id and its From line, and goes through `playbooks/experiment.md` at the
  probe stage.
