# Poiesis Frontier

New concepts, each with the experiment that could kill it, in Claude Code. Poiesis Frontier thinks past what is
known. It starts from the conclusions Poiesis Insight has already tested, the scenarios Poiesis Foresight built, or
the gaps research found, checks by script that what it starts from really survived its challenge, and turns them
into **new concepts**. It never states conclusions: every concept carries the assumption it tests, the smallest
experiment that could prove it wrong, and what would kill it. The experiments produce new data, which Poiesis
Insight then reads.

For anyone who knows what the evidence says and wants to try something new: a product, a service, an interface, a
research method. Poiesis Frontier is one of the five products in the [Poiesis Toolkit](#part-of-the-poiesis-toolkit)
and works on its own, as one plugin. Install it below and ask in plain language.

## Part of the Poiesis Toolkit

The Poiesis Toolkit is five products for Claude Code, one for each step from a question to a finished product:
**Research** collects, **Insight** connects, **Foresight** anticipates, **Frontier** explores, **Design** creates.
Each installs and works on its own. Insight, Foresight and Frontier also read what the other steps left in your
project, as plain files, and Design builds a Frontier concept when you ask.

| Product | What it does | Plugins | Agents | Reads | Leaves in your project |
|---|---|---|---|---|---|
| [Poiesis Research](https://github.com/gorgmihai92/poiesis-research) | **collect:** the literature on a topic, the evidence for and against a claim, the grants that fit, yearly counts, signals | `poiesis-research` | `paper-scout`, `evidence-scout`, `funding-scout`, `signal-scout` | the web's scholarly databases, official funding pages | `research/` |
| [Poiesis Insight](https://github.com/gorgmihai92/poiesis-insight) | **connect:** what the evidence or your data mean, what it leaves unanswered; every conclusion challenged and its verdict recorded | `poiesis-insight` | `insight-analyst`, `challenger` | `research/`, your own data, `frontier/results/` | `insights/` |
| [Poiesis Foresight](https://github.com/gorgmihai92/poiesis-foresight) | **anticipate:** signals, trends, scenarios, forecasts, signposts | `poiesis-foresight` | `foresight-analyst`, `forecaster` | `research/`, `insights/`, your own data | `foresight/` |
| [Poiesis Frontier](https://github.com/gorgmihai92/poiesis-frontier) | **explore:** new concepts, each with the smallest experiment that could kill it; study designs for a small group | `poiesis-frontier` | `experimentalist` | `insights/`, `foresight/`, `research/` | `frontier/` |
| [Poiesis Design](https://github.com/gorgmihai92/poiesis-design) | **create:** how the interface looks, behaves and what it says, built from components that already pass, checked before release | `poiesis-ui`, `poiesis-ux`, `poiesis-copy`, `poiesis-components` | `ui-auditor`, `ux-tester`, `copy-reviewer` | your code, `.poiesis-design/` | `.poiesis-design/`, design tokens, components |

```
Research ──► Insight ──► Foresight ──► Frontier ──► Design
               ▲                          │
               └──────── results ◄────────┘   (experiment results go back to Insight as data)
```

- **One job each.** Research says what sources say; Insight says what it means; Foresight reads it forward;
  Frontier proposes what could be and how to test it; Design builds and checks. None does another's job.
- **None needs another.** When another product would really improve the answer, Claude says so once, in one line,
  and offers to install it. You can say no; the work goes on and the report says what was left out.
- **Depth you choose:** quick, standard (the default) or thorough, per request or as a line in your project's
  `CLAUDE.md`, e.g. `Depth: quick`. A few rules hold at every depth (nothing invented, sources cited, interpretation
  labelled); the rest scale with what is at stake, and every report ends with what was **not checked**.
- **Short answers.** The answer first; the full work goes in the saved file. Agents are used only for independent
  parts in parallel, or for an independent check at thorough depth.
- **Rules limit what is reported as true, never what may be explored.**

## Eleven methods, from framing the problem to the experiment

| Method | It asks | It returns |
|---|---|---|
| **Frame** (always first) | what kind of problem is this: simple, complicated, complex, chaotic? | whether frontier fits, and how big the experiments should be |
| **First principles** | what must be true, and which assumptions are not needed? | concepts that become possible once an assumption is removed |
| **Lateral thinking** | what if the opposite were true? what solves this in a far-off field? | provocations, reversals and analogies, mapped by relations, not looks |
| **Systems thinking** | what are the loops, and where does pushing move the system? | interventions placed on the leverage points, from parameters to goals and mindsets |
| **Concepts** | what is this thing for? ("what is a button for?") | the purpose, the affordance and the convention, and other forms of the same purpose |
| **Design space** | every way this interaction could work, as a table of choices | the cells nobody has tried, each a candidate to test |
| **Estrangement** | what would a stranger find odd here? what if it could not do what it is known for? | what the thing takes for granted, and concepts that drop it |
| **Recombination** | what is the ordinary solution, and which one unusual part could it take? | concepts that stay conventional except in one place |
| **Speculative design** | what ordinary object would exist in this future scenario? | an artefact brief, two contrasting versions, a staging, marked as fiction |
| **Speculative research** | which assumption of the field is worth contesting, and would the study be worth running? | a question, two imaginary abstracts marked as fiction, a protocol written before the data |
| **Experiment and study** (always last) | what is the cheapest way this concept could fail, at the stage it is at? | the assumption, a prediction, the smallest experiment, a kill criterion fixed in advance; for people, what the sample can detect |

Some ways it works with the other products:

- **Interfaces that do not exist yet:** Poiesis Frontier lays out the design space of an interaction and finds
  the untried cells, Poiesis Research checks prior art, then Poiesis Design builds the concept that survived.
- **The future of education:** Poiesis Foresight produces scenarios, then Poiesis Frontier designs speculative
  artefacts from them and stages them with a small group.
- **Research directions:** Poiesis Insight describes a gap and contests its assumptions, then Poiesis Frontier
  writes the study that would answer it, sized for the people you have.
- **Better research methods:** Poiesis Frontier designs a method experiment, then Poiesis Research and Poiesis
  Insight check it against the literature.

## Install

In Claude Code:

```
/plugin marketplace add gorgmihai92/poiesis-frontier
/plugin install poiesis-frontier@poiesis-frontier
```

It needs **Python 3** (3.9 or later), which macOS and most Linux systems already have. No keys, no setup.

## Ask in plain language

The plugin comes in when the work is new concepts, experiments or a study design, and you can name the agent
directly.

- *"From the onboarding insights we kept, what would onboarding look like with no forms at all?"*
- *"Lay out the design space for confirming a destructive action. Which cells has nobody tried?"*
- *"Make a familiar thing strange: our checkout, as someone from 1950 would describe it."*
- *"Take the 2035 scenarios in foresight/ and design speculative artefacts for a school in each."*
- *"I can get eight students for an afternoon. Design a study for these two variants and tell me what it can detect."*
- *"Use the experimentalist on these five concepts: what's the cheapest way each could fail?"*

## Every concept ends with an experiment that could kill it

One skill, `frontier`, is the entry point. It reads what was tested (`insights/`, `foresight/`, `research/`),
frames the problem, picks one or more **method playbooks**, and ends every concept with the **experiment**
playbook.

| Step | Playbook | What it does |
|---|---|---|
| frame | `frame.md` | decides the kind of problem; Poiesis Frontier belongs in the complex ones |
| generate | `first-principles.md`, `lateral.md`, `systems.md`, `concepts.md`, `design-space.md`, `estrangement.md`, `recombination.md`, `speculative.md` | produces concepts, each with its id, its starting points and its method; the report says how many are distinct |
| decide whether to study | `speculative-research.md` | contests an assumption, imagines the paper both ways, writes the protocol before the data |
| test | `experiment.md`, `study.md`, agent `experimentalist` | the stage, the assumption, the prediction, the smallest experiment, the kill criterion; for people, what the sample can detect |

- **Starting points are checked, not trusted.** `experiments.py gate` looks up each id a concept starts from in
  the challenge stamps Poiesis Insight writes, with this plugin's own code. A concept from a kept or weakened
  conclusion goes through; one from a conclusion with no valid stamp is marked **provisional** in its own note;
  one from a dropped conclusion is **stopped**. The verdict is never retyped.
- **The test fits the stage.** A sketch is criticised next to other sketches, not put through a usability test;
  a prototype is compared with the way things are done now.
- **What a sample can detect, not a guessed effect.** `power.py` says, for the people you actually have, the
  smallest difference a comparison would find, how often a count criterion is met, and how likely a problem is to
  show up at all. A study too small to test describes, and says so.
- **An independent experimentalist at thorough depth.** The agent gets the concepts and their starting points, not
  the reasoning that produced them, and looks for the cheapest way each could fail.
- **Experiments are logged before they run.** The kill criterion is dated in `frontier/experiments.md` before the
  experiment starts. `experiments.py` lists open and overdue experiments and flags any kill criterion that is
  missing or written after the start.
- **Results go back to Poiesis Insight.** Each result is saved in `frontier/results/` with its raw data; Poiesis
  Insight reads it as data and challenges what it means.

## The same rules for every concept: no conclusions

The same rules apply to every playbook (`skills/frontier/rules.md`), each with its source and how much of it was
read:

- **No conclusions.** A concept is a hypothesis, written "if …, then …", never "this shows".
- **Every concept carries** its id, what it starts from and how that was tested, the method that produced it, its
  stage, the riskiest assumption, a prediction, the smallest experiment and a kill criterion.
- **Fixed in advance.** Assumption, measure and kill criterion are logged before the experiment starts; changing
  them is a new experiment. What was not predicted is reported as exploratory.
- **Several variants, shown together.** A design shown alone collects higher ratings and fewer criticisms.
- **Distinct ideas, not ideas generated.** The report says how many concepts are distinct; asking for more of the
  same is not a method.
- **Fiction is marked as fiction,** in the artefact itself, before and after. People are in on it, and an
  imagined result is never a result.
- **Safe to fail.** Several small probes rather than one plan in complex problems. Anything with personal data,
  money or a public release is proposed to you, never run.
- **Nothing invented, and convincing is not evidence.** Facts come from the input or from sources read; no
  invented specifics to make a concept persuasive; concepts are ranked by what their test would teach.

## Concepts and experiments stay in `frontier/`

```
frontier/<date>-<topic>.md      starting points, frame, concepts (CN-001), each with From, its experiment,
                                and the gate's Provisional or Stopped line
frontier/experiments.md         the experiment log: assumption, prediction, kill criterion and its date,
                                start, due, status (planned, running, kept, killed, inconclusive), result
frontier/results/<id>.md        what an experiment produced, with the raw data next to it; data for insight
frontier/studies/<id>-<slug>.md a study design (ST-001), written and dated before any data
```

## What's in this repository

The repository is a Claude Code **marketplace** holding one **plugin**, plus the research behind its rules and the
tests of its scripts.

```
.claude-plugin/
  marketplace.json            the marketplace: its name and the plugins it lists (here, one)
plugins/
  poiesis-frontier/           the plugin
    .claude-plugin/
      plugin.json             name, version, description
    skills/frontier/          the skill: what Claude follows when you ask for new concepts or experiments
      SKILL.md                entry point: reads what was tested, frames, picks the playbooks
      rules.md                no conclusions, what every concept carries, the gate, experiments fixed in
                              advance, fiction; with sources and how much of each was read
      playbooks/
        frame.md              what kind of problem it is (always first)
        first-principles.md   what must be true; remove the assumptions not needed
        lateral.md            provocations, reversals, analogies
        systems.md            loops and leverage points
        concepts.md           what a thing is for: purpose, affordance, convention
        design-space.md       every way an interaction could work; the untried cells
        estrangement.md       a stranger's description, relabelling, an extreme character, a counter-function
        recombination.md      an ordinary base with one unusual pairing
        speculative.md        artefacts from foresight scenarios: brief, versions, staging, fiction marked
        speculative-research.md  contested assumptions, imaginary abstracts, a protocol before the data
        study.md              a study for a small group, and what its sample can detect
        experiment.md         stage, assumption, smallest experiment, kill criterion, the gate (always last)
      scripts/                Python 3, standard library only
        experiments.py        check the experiment log; gate the starting points; give ids
        power.py              what a sample of a given size can detect
      templates/
        concept.md            one concept with everything it carries
        experiments.md        the experiment log
        result.md             one experiment's result, for insight
        study.md              one study design
        artefact.md           one speculative artefact's brief
    agents/
      experimentalist.md      designs the experiment for each concept
    evals/                    eval cases for `claude plugin eval` (not run yet)
research/                     the sources behind the rules: one note per source, with how much was read
tests/                        tests of the scripts, offline: python3 -I -m unittest discover -s tests
CHANGELOG.md                  what changed in each version
LICENSE                       MIT
```

## Where the rules come from

Each rule names its source; there is one note per source in `research/notes`, which says whether the full text,
part of it, a web page or only the abstract was read, and on what date. `research/README.md` lists them by
topic. In short:

- **What kind of problem it is, and probes in complex ones:** Kurtz & Snowden 2003 (abstract) and van Beurden et
  al. 2011.
- **Leverage points:** Meadows 1999; Abson et al. 2017.
- **Analogies:** Gentner 1983; Gick & Holyoak 1980 (abstract); Chan, Dow & Schunn 2015 (authors' summary).
- **What a thing is for:** Norman 1999.
- **Evaluation that fits the stage:** Greenberg & Buxton 2008; Olsen 2007.
- **Generating:** Card, Mackinlay & Robertson 1991 (design spaces); Bell, Blythe & Sengers 2005 (defamiliarisation,
  in part); Djajadiningrat, Gaver & Frens 2000 (relabelling, extreme characters); Pierce & Paulos 2014
  (counterfunctional things); Uzzi et al. 2013 (an unusual pairing on a conventional base, a pattern in citations,
  used here as an untested analogy).
- **Distinct ideas, and ideas on paper against ideas carried out:** Si, Yang & Hashimoto 2024; Si, Hashimoto &
  Yang 2025 (both in part).
- **Speculative design:** Auger 2013 (abstract); Phadnis et al. 2015; Mancini et al. 2010; Elsden et al. 2017 (in
  part); Coulton, Lindley & Akmal 2016.
- **Speculative research:** Alvesson & Sandberg 2011 (in part); Blythe 2014; Nosek et al. 2018 (in part).
- **Small studies:** Tohidi et al. 2006; Dow et al. 2010; Lakens 2022 (in part); Nielsen & Landauer 1993 (in
  part); Eypasch et al. 1995 (abstract); the G*Power 3.1 manual (three sections).
- **Detail adds plausibility, not probability:** Tversky & Kahneman 1983, from general knowledge, not read.
- **Lateral thinking (de Bono) and speculative design (Dunne & Raby 2013):** used as methods; their sources are
  not yet read, and no rule rests on them.

## Files shared with the other products

Writes `frontier/<date>-<topic>.md` concepts (**Starting point**, **Assumption**, **Kill criterion**, **Verdict**,
**Log id**, and since 1.2.0 **Id**, **From**, **Stage** and the gate's **Provisional** or **Stopped** line); the log
`frontier/experiments.md` (ten columns, five statuses; the concept cell starts with the concept's id); results in
`frontier/results/<id>.md`, read by Insight; study designs in `frontier/studies/` (since 1.2.0). It reads Insight's
**Id** and **Challenge** lines and its challenge stamps (`insights/challenge-stamps.jsonl`, format 1, verified with
its own code), Foresight's scenarios (`SC-001`) and research notes.

The paths and fields the other products read are a contract: they change only in a major version, noted in the
changelog. Every plugin reads the others' files tolerantly: a missing file or field is reported as unknown, never
an error. The full list is in each skill's `SKILL.md`, so Claude knows it too.

## Update or remove

```
/plugin marketplace update poiesis-frontier
/plugin update poiesis-frontier@poiesis-frontier
/plugin uninstall poiesis-frontier@poiesis-frontier
```

## Changing the plugin

Edit the files under `plugins/poiesis-frontier/`, run the tests (`python3 -I -m unittest discover -s tests`) and
`claude plugin validate plugins/poiesis-frontier` (at the root it checks only the marketplace file), bump the
version (major if a field under "Files" changes) in `plugin.json`, `marketplace.json` and `CHANGELOG.md`, and push.
Projects get it with the update commands above.

## License

MIT.
