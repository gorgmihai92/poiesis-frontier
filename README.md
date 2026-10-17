# Poiesis Frontier

A Claude Code plugin for thinking past what is known. It starts from the conclusions insight has already tested,
the scenarios foresight built, or the gaps research found, and turns them into **new concepts**. It never states
conclusions: every concept carries the assumption it tests, the smallest experiment that could prove it wrong, and
what would kill it. The experiments produce new data, which insight then reads.

## The Poiesis toolkits

**Collect → connect → explore → create.** Four toolkits, each usable on its own; together, each one builds on what
the previous one left in your project.

| Toolkit | You | What it does | Leaves in your project |
|---|---|---|---|
| [poiesis-research](https://github.com/gorgmihai92/poiesis-research) | **collect** | finds and cites sources: the literature on a topic, the evidence behind a claim, the grants that fit | `research/` |
| [poiesis-insight](https://github.com/gorgmihai92/poiesis-insight) | **connect** | interprets what was collected, or any data: insights and foresight, each conclusion challenged | `insights/`, `foresight/` |
| [poiesis-frontier](https://github.com/gorgmihai92/poiesis-frontier) | **explore** | new concepts from what was tested, each with the experiment that could kill it | `frontier/` |
| [poiesis-design](https://github.com/gorgmihai92/poiesis-design) | **create** | designs the interface and how the app behaves, and checks both before release | `.poiesis-design/`, your design tokens |

Frontier does not look for patterns itself. It starts from the ones insight has tested, and its experiments
produce data for insight to read. Concepts that survive their experiments go to design to be built.

## What it covers

| Method | It asks | It returns |
|---|---|---|
| **Frame** (always first) | what kind of problem is this: simple, complicated, complex, chaotic? | whether frontier fits, and how big the experiments should be |
| **First principles** | what must be true, and which assumptions are not needed? | concepts that become possible once an assumption is removed |
| **Lateral thinking** | what if the opposite were true? what solves this in a far-off field? | provocations, reversals and analogies, mapped by relations, not looks |
| **Systems thinking** | what are the loops, and where does pushing move the system? | interventions placed on the leverage points, from parameters to goals and mindsets |
| **Concepts** | what is this thing for? ("what is a button for?") | the purpose, the affordance and the convention, and other forms of the same purpose |
| **Speculative design** | what ordinary object would exist in this future scenario? | artefacts to put in front of people, so they think about the future or about current practice |
| **Experiment** (always last) | what is the cheapest way this concept could fail? | the assumption, a prediction, the smallest experiment, a kill criterion fixed in advance |

Some ways it works with the other toolkits:

- **UI without classic components, adaptive UI:** frontier generates the concept, then poiesis-ui and poiesis-ux
  build it.
- **The future of education:** foresight (poiesis-insight) produces scenarios, then frontier designs speculative
  artefacts and experiments from them.
- **What is missing from software design:** research and insight find the gaps, then frontier reframes them.
- **Better research methods:** frontier designs a method experiment, then research and insight check it against
  the literature.

## Install

In Claude Code:

```
/plugin marketplace add gorgmihai92/poiesis-frontier
/plugin install poiesis-frontier@poiesis-frontier
```

It needs **Python 3**, which macOS and most Linux systems already have. No keys, no setup.

## What to ask Claude

Ask in plain language. The plugin comes in when the work is new concepts or experiments, and you can name the
agent directly.

- *"From the onboarding insights we kept, what would onboarding look like with no forms at all?"*
- *"What is a button for? Give me concepts for actions without buttons, and how to test each."*
- *"Take the 2035 scenarios in foresight/ and design speculative artefacts for a school in each."*
- *"Map the loops in our marketplace and find the leverage points."*
- *"Use the experimentalist on these five concepts: what's the cheapest way each could fail?"*

## How it works

One skill, `frontier`, is the entry point. It reads what was tested (`insights/`, `foresight/`, `research/`),
frames the problem, picks one or more **method playbooks**, and ends every concept with the **experiment**
playbook.

| Step | Playbook | What it does |
|---|---|---|
| frame | `frame.md` | decides the kind of problem; frontier belongs in the complex ones |
| generate | `first-principles.md`, `lateral.md`, `systems.md`, `concepts.md`, `speculative.md` | produces concepts, each with its starting point and method |
| test | `experiment.md`, agent `experimentalist` | assumption, prediction, smallest experiment, kill criterion; marks each concept ready, sharpen or not testable yet |

- **Start from what was tested.** Insights marked kept or weakened by insight's challenge, foresight scenarios,
  research gaps. Without them, the question's premise becomes the first assumption to test.
- **An independent experimentalist.** The agent gets the concepts and their starting points, not the reasoning
  that produced them, and looks for the cheapest way each could fail.
- **Experiments are logged before they run.** The kill criterion is dated in `frontier/experiments.md` before the
  experiment starts. `experiments.py` lists open and overdue experiments and flags any kill criterion that is
  missing or written after the start.
- **Results go back to insight.** Each result is saved in `frontier/results/` with its raw data; poiesis-insight
  reads it as data and challenges what it means.

## The rules

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

## What it adds to your project

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
- **Lateral thinking (de Bono) and speculative design (Dunne & Raby 2013):** used as methods; their sources are
  not yet read, and no rule rests on them.

## Update or remove

```
/plugin marketplace update poiesis-frontier
/plugin update poiesis-frontier@poiesis-frontier
/plugin uninstall poiesis-frontier@poiesis-frontier
```

## Changing the plugin

Edit the files under `plugins/poiesis-frontier/`, run `claude plugin validate .`, bump the version in
`plugin.json`, `marketplace.json` and `CHANGELOG.md`, and push. Projects get it with the update commands above.

## License

MIT. Requires Python 3.
