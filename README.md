# Poiesis Frontier

New concepts, each with the experiment that could kill it, in Claude Code. Poiesis Frontier thinks past what is
known. It starts from the conclusions Poiesis Insight has already tested, the scenarios its foresight built, or the
gaps research found, and turns them into **new concepts**. It never states conclusions: every concept carries the
assumption it tests, the smallest experiment that could prove it wrong, and what would kill it. The experiments
produce new data, which Poiesis Insight then reads.

For anyone who knows what the evidence says and wants to try something new: a product, a service, a research method.
Poiesis Frontier is one of the four products in the [Poiesis Toolkit](#part-of-the-poiesis-toolkit) and works on its
own, as one plugin. Install it below and ask in plain language.

## Part of the Poiesis Toolkit

The Poiesis Toolkit is four products for Claude Code, one for each step from a question to a finished product:
**Research** collects, **Insight** connects, **Frontier** explores, **Design** creates. Each installs and works on
its own. Insight and Frontier also read what the other steps left in your project, as plain files, and Design
builds a Frontier concept when you ask.

| Product | What it does | Plugins | Agents | Reads | Leaves in your project |
|---|---|---|---|---|---|
| [Poiesis Research](https://github.com/gorgmihai92/poiesis-research) | **collect:** the literature on a topic, the evidence for and against a claim, the grants that fit | `poiesis-research` | `paper-scout`, `evidence-scout`, `funding-scout` | the web's scholarly databases, official funding pages | `research/` |
| [Poiesis Insight](https://github.com/gorgmihai92/poiesis-insight) | **connect:** what the evidence or your data mean, and what is emerging; every conclusion challenged | `poiesis-insight` | `insight-analyst`, `foresight-analyst`, `challenger` | `research/`, your own data, `frontier/results/` | `insights/`, `foresight/` |
| [Poiesis Frontier](https://github.com/gorgmihai92/poiesis-frontier) | **explore:** new concepts, each with the smallest experiment that could kill it | `poiesis-frontier` | `experimentalist` | `insights/`, `foresight/`, `research/` | `frontier/` |
| [Poiesis Design](https://github.com/gorgmihai92/poiesis-design) | **create:** how the interface looks, behaves and what it says, built from components that already pass, checked before release | `poiesis-ui`, `poiesis-ux`, `poiesis-copy`, `poiesis-components` | `ui-auditor`, `ux-tester`, `copy-reviewer` | your code, `.poiesis-design/` | `.poiesis-design/`, design tokens, components |

```
Research ──► Insight ──► Frontier ──► Design
               ▲            │
               └─ results ◄─┘   (experiment results go back to Insight as data)
```

- **One job each.** Research says what sources say; Insight says what it means; Frontier proposes what could be
  and how to test it; Design builds and checks. None does another's job.
- **None needs another.** When another product would really improve the answer, Claude says so once, in one line,
  and offers to install it. You can say no; the work goes on and the report says what was left out.
- **Depth you choose:** quick, standard (the default) or thorough, per request or as a line in your project's
  `CLAUDE.md`, e.g. `Depth: quick`. A few rules hold at every depth (nothing invented, sources cited, interpretation
  labelled); the rest scale with what is at stake, and every report ends with what was **not checked**.
- **Short answers.** The answer first; the full work goes in the saved file. Agents are used only for independent
  parts in parallel, or for an independent check at thorough depth.
- **Rules limit what is reported as true, never what may be explored.**

## Seven methods, from framing the problem to the experiment

| Method | It asks | It returns |
|---|---|---|
| **Frame** (always first) | what kind of problem is this: simple, complicated, complex, chaotic? | whether frontier fits, and how big the experiments should be |
| **First principles** | what must be true, and which assumptions are not needed? | concepts that become possible once an assumption is removed |
| **Lateral thinking** | what if the opposite were true? what solves this in a far-off field? | provocations, reversals and analogies, mapped by relations, not looks |
| **Systems thinking** | what are the loops, and where does pushing move the system? | interventions placed on the leverage points, from parameters to goals and mindsets |
| **Concepts** | what is this thing for? ("what is a button for?") | the purpose, the affordance and the convention, and other forms of the same purpose |
| **Speculative design** | what ordinary object would exist in this future scenario? | artefacts to put in front of people, so they think about the future or about current practice |
| **Experiment** (always last) | what is the cheapest way this concept could fail? | the assumption, a prediction, the smallest experiment, a kill criterion fixed in advance |

Some ways it works with the other products:

- **UI without classic components, adaptive UI:** Poiesis Frontier generates the concept, then Poiesis Design
  (poiesis-ui and poiesis-ux) builds it.
- **The future of education:** foresight (Poiesis Insight) produces scenarios, then Poiesis Frontier designs
  speculative artefacts and experiments from them.
- **What is missing from software design:** Poiesis Research and Poiesis Insight find the gaps, then Poiesis
  Frontier reframes them.
- **Better research methods:** Poiesis Frontier designs a method experiment, then Poiesis Research and Poiesis
  Insight check it against the literature.

## Install

In Claude Code:

```
/plugin marketplace add gorgmihai92/poiesis-frontier
/plugin install poiesis-frontier@poiesis-frontier
```

It needs **Python 3**, which macOS and most Linux systems already have. No keys, no setup.

## Ask in plain language

The plugin comes in when the work is new concepts or experiments, and you can name the
agent directly.

- *"From the onboarding insights we kept, what would onboarding look like with no forms at all?"*
- *"What is a button for? Give me concepts for actions without buttons, and how to test each."*
- *"Take the 2035 scenarios in foresight/ and design speculative artefacts for a school in each."*
- *"Map the loops in our marketplace and find the leverage points."*
- *"Use the experimentalist on these five concepts: what's the cheapest way each could fail?"*

## Every concept ends with an experiment that could kill it

One skill, `frontier`, is the entry point. It reads what was tested (`insights/`, `foresight/`, `research/`),
frames the problem, picks one or more **method playbooks**, and ends every concept with the **experiment**
playbook.

| Step | Playbook | What it does |
|---|---|---|
| frame | `frame.md` | decides the kind of problem; Poiesis Frontier belongs in the complex ones |
| generate | `first-principles.md`, `lateral.md`, `systems.md`, `concepts.md`, `speculative.md` | produces concepts, each with its starting point and method |
| test | `experiment.md`, agent `experimentalist` | assumption, prediction, smallest experiment, kill criterion; marks each concept ready, sharpen or not testable yet |

- **Start from what was tested.** Insights marked kept or weakened by Poiesis Insight's challenge, foresight
  scenarios, research gaps. Without them, the question's premise becomes the first assumption to test.
- **An independent experimentalist at thorough depth.** The agent gets the concepts and their starting points, not
  the reasoning that produced them, and looks for the cheapest way each could fail. Otherwise the experiment
  playbook runs inline.
- **Experiments are logged before they run.** The kill criterion is dated in `frontier/experiments.md` before the
  experiment starts. `experiments.py` lists open and overdue experiments and flags any kill criterion that is
  missing or written after the start.
- **Results go back to Poiesis Insight.** Each result is saved in `frontier/results/` with its raw data; Poiesis
  Insight reads it as data and challenges what it means.

## The same rules for every concept: no conclusions

The same rules apply to every playbook (`skills/frontier/rules.md`), each with its source:

- **No conclusions.** A concept is a hypothesis, written "if …, then …", never "this shows".
- **Every concept carries** its starting point and how it was tested, the method that produced it, the riskiest
  assumption, a prediction, the smallest experiment and a kill criterion.
- **Fixed in advance.** Assumption, measure and kill criterion are logged before the experiment starts; changing
  them is a new experiment. What was not predicted is reported as exploratory.
- **Safe to fail.** Several small probes rather than one plan in complex problems. Anything with personal data,
  money or a public release is proposed to you, never run.
- **Analogies by relations, near and far.** Keep an analogy only if its relations carry over, and check near
  sources next to far ones.
- **Push where it moves the system,** knowing that deeper leverage meets more resistance.
- **Nothing invented.** Facts come from the input or from sources read; named methods are used as methods, not as
  evidence.
- **Convincing is not evidence.** No invented specifics to make a concept persuasive; an assumed future names its
  drivers and comes with a contrasting one; concepts are ranked by what their test would teach, not by appeal.

## Concepts and experiments stay in `frontier/`

```
frontier/<date>-<topic>.md      starting points, frame, concepts, each with its experiment
frontier/experiments.md         the experiment log: assumption, prediction, kill criterion and its date,
                                start, due, status (planned, running, kept, killed, inconclusive), result
frontier/results/<id>.md        what an experiment produced, with the raw data next to it; data for insight
```

## What's in this repository

The repository is a Claude Code **marketplace** holding one **plugin**, plus the research behind its rules.

```
.claude-plugin/
  marketplace.json            the marketplace: its name and the plugins it lists (here, one)
plugins/
  poiesis-frontier/           the plugin
    .claude-plugin/
      plugin.json             name, version, description
    skills/frontier/          the skill: what Claude follows when you ask for new concepts or experiments
      SKILL.md                entry point: reads what was tested, frames, picks the playbooks
      rules.md                no conclusions, what every concept carries, experiments fixed in advance; with sources
      playbooks/
        frame.md              what kind of problem it is (always first)
        first-principles.md   what must be true; remove the assumptions not needed
        lateral.md            provocations, reversals, analogies
        systems.md            loops and leverage points
        concepts.md           what a thing is for: purpose, affordance, convention
        speculative.md        artefacts from foresight scenarios
        experiment.md         assumption, smallest experiment, kill criterion (always last)
      scripts/                Python 3, standard library only
        experiments.py        check the experiment log
      templates/
        concept.md            one concept with everything it carries
        experiments.md        the experiment log
        result.md             one experiment's result, for insight
    agents/
      experimentalist.md      designs the experiment for each concept
research/                     the sources behind the rules: one note per source
CHANGELOG.md                  what changed in each version
LICENSE                       MIT
```

## Where the rules come from

Each rule names its source; there is one note per source in `research/notes`, which says whether the full text,
a web page or only the abstract was read.

- **What kind of problem it is, and probes in complex ones:** Kurtz & Snowden 2003 (the Cynefin framework) and van
  Beurden et al. 2011 (the domains and their decision models: probe, sense, respond).
- **Leverage points, and the obvious one pushed the wrong way:** Meadows 1999. Most attention goes to parameters,
  with little leverage; the deeper the point, the more the system resists.
- **Four groups of leverage points, which interact:** Abson et al. 2017.
- **Analogies by relations, not attributes:** Gentner 1983, structure-mapping.
- **Prompting for analogies:** Gick & Holyoak 1980. People used the analogy mostly when told to.
- **Near sources next to far ones:** Chan, Dow & Schunn 2015. Closer sources went with more creative ideas.
- **Real and perceived affordances, conventions:** Norman 1999.
- **The perceptual bridge in speculative design:** Auger 2013.
- **Kill criteria fixed and dated in advance; the unpredicted as exploratory:** Nosek et al. 2018, preregistration.
- **Detail adds plausibility, not probability:** Tversky & Kahneman 1983, the conjunction fallacy.
- **At least two contrasting futures:** Phadnis et al. 2015. One scenario steers judgment toward itself.
- **Lateral thinking (de Bono) and speculative design (Dunne & Raby 2013):** used as methods; their sources are
  not yet read, and no rule rests on them.

## Files shared with the other products

Writes `frontier/<date>-<topic>.md` concepts (**Starting point**, **Assumption**, **Kill criterion**, **Verdict**, **Log id**); the log `frontier/experiments.md`; results in `frontier/results/<id>.md`, read by Insight. It reads Insight's **Challenge** line, foresight scenarios and research notes.

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

Edit the files under `plugins/poiesis-frontier/`, run `claude plugin validate .`, bump the version (major if a field under "Files" changes) in
`plugin.json`, `marketplace.json` and `CHANGELOG.md`, and push. Projects get it with the update commands above.

## License

MIT.
