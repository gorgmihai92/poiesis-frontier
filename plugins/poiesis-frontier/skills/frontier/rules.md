# Rules (every playbook)

## Depth
Some rules hold at every depth; the rest are defaults, scaled to what is at stake. The user picks the depth, or the
project sets it with a `Depth:` line in its `CLAUDE.md` (read in every session, by every Poiesis plugin);
otherwise **standard**.
- **Always:** no conclusions; each concept's assumption and kill criterion fixed before anything runs; no harm, and
  anything with personal data, money or a public release only proposed; nothing invented, and no invented
  specifics to persuade; fiction marked as fiction; what the starting-point check finds is never retyped.
- **Quick:** one method, up to three concepts, each with its assumption, smallest experiment and kill criterion.
- **Standard:** frame, the methods that fit, and the full experiment playbook.
- **Thorough:** several methods, and the experiments designed by the independent `experimentalist` agent, given the
  concepts and starting points but not the reasoning.

A default may be skipped at any depth if the report says which one and why. Every report ends with **Not
checked:** what was skipped, or "nothing". Generating has no limit but harm: these rules apply to what is claimed
and to experiments, never to what may be imagined.

## No conclusions
Frontier proposes; it never concludes. A concept is a hypothesis about what could work or what could be true, not a
finding. Words like "shows", "proves" or "the answer is" do not appear in a concept; "if …, then …" does.

## Every concept carries
- **Id and From:** `CN-001`, from `experiments.py ids CN`, and the ids it starts from: conclusions (`IN-…`),
  scenarios (`SC-…`), questions, sources by their note's name or citation key. `none` when the start is the
  user's question alone.
- **Starting point:** the tested insight, scenario, gap or question it comes from, with its reference (file, note
  and page) and how it was tested (insight's challenge verdict, or "untested").
- **Stage:** sketch, probe, prototype or pilot (`playbooks/experiment.md`). It decides the kind of test.
- **Assumption:** the one thing that must be true for the concept to work. If there are several, name the riskiest:
  the one most likely to be false and most costly if it is.
- **Smallest experiment:** the cheapest, fastest thing that could show the assumption false: who, what, how many,
  how long, what is measured.
- **Kill criterion:** the result that would kill the concept, as a number or an observable event, written and dated
  before the experiment runs. Generating an idea and testing it are different steps; once the result is known,
  hindsight makes any outcome look predicted (Nosek et al. 2018).
- **Method:** which playbook produced it, so it is clear the concept came from a provocation or a reframing and not
  from evidence.

## Starting points are checked, not trusted
- **The check is a script.** When concepts are saved, `experiments.py gate` looks up every id in a concept's From:
  in the challenge stamps poiesis-insight writes, and in the notes of `insights/` and `foresight/`. A label in a
  note is not the record. In the recorded run of 2026-11-17 one "weakened" was retyped as "kept" on the published
  page.
- **Through:** every starting point is kept or weakened, its stamp is intact and its sentence is the one that was
  challenged. A weakened one is used in its narrower form.
- **Provisional:** a starting point has no stamp, or its stamp or its sentence was changed, or it is a source, a
  question or a signal that no challenge covers, or none is named. The concept says so in its own note, in a
  **Provisional** line the script writes, and wherever it is shown. It can still be tested.
- **Stopped:** a starting point was dropped. The concept gets no experiment. It stays in the note with a
  **Stopped** line; the reason the conclusion was dropped may still show an assumption worth testing from
  another start.
- **Never in the log.** The experiment log keeps its five statuses: planned, running, kept, killed,
  inconclusive. "Provisional" is about what a concept rests on, not about an experiment.
- **Never by hand.** The Provisional and Stopped lines are written with `--write`, not typed. A report copies the
  gate's lines; it does not reword them.

## Experiments
- **Fixed in advance:** the assumption, the measure and the kill criterion are logged in `frontier/experiments.md`
  before the experiment starts. Changing them afterwards is a new experiment, with a new row.
- **The test fits the stage.** An early idea is a sketch: it is criticised, compared with other sketches and
  checked against what is already known. It is not put through a usability test, which finds the problems every
  sketch has and says nothing about the idea (Greenberg & Buxton 2008). The test follows from what the concept
  claims: that something can now be done is shown by doing it, that something is better by a comparison (Olsen
  2007). Stage decides the kind of test, never whether there is one.
- **A missing feature does not kill a concept.** The kill criterion is about the assumption. Anything new leaves
  things out (Olsen 2007).
- **Several variants, shown together.** A thing shown alone collects politeness: in one experiment a design seen
  alone was rated higher and criticised less than the same design seen among three (Tohidi et al. 2006). Build
  two or three variants before showing any (Dow et al. 2010, one experiment with novices).
- **What the sample can detect, not a guessed effect.** A study design starts from the number of people that can
  be had and says, from `power.py`, what that number can detect (Lakens 2022). An effect size is not assumed in
  order to make a sample look large enough: a plausible effect comes from the project's earlier data or from a
  source, or it is "unknown". Where the detectable difference is far above anything plausible, the study
  describes and does not test.
- **Unexpected results are leads.** What the experiment showed but did not predict is reported as exploratory,
  not as a confirmed result (Nosek et al. 2018). A first round with a small group is exploratory and says so.
- **Safe to fail:** in a complex problem, run several small probes rather than one plan, and amplify what works
  (Kurtz & Snowden 2003, abstract only; van Beurden et al. 2011). No experiment may harm the people in it; one
  that needs personal data, money or a public release is proposed to the user, never run.
- **Results go back to insight.** Frontier records what happened (`frontier/results/`); interpreting it is
  insight's job, with its challenge.

## Generating
- **Distinct ideas, not ideas generated.** A report says how many concepts were generated, how many are distinct,
  and how "the same" was judged. Here two concepts are the same idea when they rest on the same assumption and
  use the same mechanism, whatever the wording. When one agent was asked for 4,000 research ideas on a topic,
  about 200 were not duplicates, and asking for more mostly repeated the ones it had (Si, Yang & Hashimoto 2024).
  When a method stops giving distinct concepts, change the method or the operator; do not ask for more.
- **More varied is not better by itself.** Variety is a way to find a concept worth testing, not a score. In the
  one experiment read on it, how varied a person's prototypes were did not predict how good their final design
  was (Dow et al. 2010).
- **An empty cell is a candidate.** A design space shows what has not been tried. Many untried things are
  untried for a reason (Card, Mackinlay & Robertson 1991).
- **Estrangement produces questions, not knowledge of people.** Describing a thing as a stranger would, designing
  for an extreme character or removing a function opens concepts. It is not a way of learning about real users
  (Bell, Blythe & Sengers 2005). An extreme character is defined by an attitude to the task, never by a group of
  people (Djajadiningrat, Gaver & Frens 2000).
- **One unusual pairing on an ordinary base.** The recombination playbook keeps a concept conventional except in
  one place. This copies a pattern found in which scientific papers get cited most (Uzzi et al. 2013); as a way
  of generating concepts it is this plugin's analogy and is untested.
- **Analogies by relations, not looks.** An analogy is useful when the relations carry over (what causes what, what
  depends on what), not the surface features (Gentner 1983). People rarely use a distant analogy unless prompted
  to (Gick & Holyoak 1980, abstract only), so the lateral playbook prompts for them on purpose.
- **Far is not automatically better.** In one large study, ideas built on conceptually closer sources were judged
  more creative than those built on far ones (Chan et al. 2015, from the authors' summary, not the paper). Use
  far analogies to break a frame, then check near ones too.
- **Push where it moves the system.** Most attention goes to parameters, where there is little leverage; goals,
  rules and mindsets move more but resist more (Meadows 1999, p. 8, 21). Leverage points interact (Abson et al.
  2017).
- **Look at what a thing is for, not what it looks like.** On a screen, the designer controls only what the user
  perceives to be possible, and conventions (Norman 1999).
- **A speculative artefact needs a perceptual bridge:** close enough to the present to be understood, far enough
  to make people think (Auger 2013, abstract only).

## Fiction
- **Fiction is marked as fiction.** A speculative artefact, an imagined abstract and an imagined result each say
  what they are: in the artefact itself, before people meet it and after. A label alone has failed: the
  reviewers of a fictional research paper that was marked as design fiction did not fully grasp that it was
  fiction (Coulton, Lindley & Akmal 2016). The more familiar the format it borrows, the stronger the mark.
- **People are in on it.** Nobody is deceived in a staging; they know it is fiction and what taking part
  involves before they agree (Elsden et al. 2017).
- **An imagined result is never a result.** It is written to decide whether a study is worth running (Blythe
  2014). It is never saved in `frontier/results/` and never cited.
- **What people say to a fiction is about the present.** It records their reaction to this artefact, today, told
  this way; it is not how the future will be. A reaction that appears under one version of the story only is a
  lead about the telling (Mancini et al. 2010).

## Honesty
- Facts come from the input or from sources read; nothing is added from memory without marking it "from general
  knowledge, unverified". Named methods (de Bono, Dunne & Raby) are used as methods, not as evidence.
- **Convincing is not evidence.** Detail makes a story feel more likely while making it less likely: each detail
  is one more assumption (Tversky & Kahneman 1983, not read: from general knowledge). No specifics (numbers,
  names, dates, quotes, "studies show") are added to make a concept or scenario persuasive; each one comes from
  a source or is marked "invented for the artefact".
- **Ranked by the test, not the appeal.** Concepts are ordered by what their experiment would teach and how cheap
  it is, never by how good they sound. How an idea is rated on paper says little about what it is worth once
  carried out: when 43 researchers each executed one idea, the ratings of generated ideas fell more than those of
  researchers' ideas (Si, Hashimoto & Yang 2025; the authors call the sample modest). In the study before it,
  reviewers agreed with each other 56% of the time on which ideas were best, where chance is 50%, and the best
  automatic ranker agreed with them 53% of the time (Si, Yang & Hashimoto 2024).
- **An interesting question is not a true answer.** Contesting an assumption gives a question worth asking
  (Alvesson & Sandberg 2011). The alternative stays an assumption until a study tests it.
- A concept that cannot be tested yet says so, and says what would make it testable. It is not reported as a
  concept until then.

## Sources, and how much of each was read
One note per source in `research/notes` of the plugin's repository
(https://github.com/gorgmihai92/poiesis-frontier/tree/main/research/notes). A rule rests on what was read and no
more.
- **Full text:** Card, Mackinlay & Robertson 1991; Djajadiningrat, Gaver & Frens 2000; Tohidi et al. 2006; Olsen
  2007; Greenberg & Buxton 2008; Dow et al. 2010; Mancini et al. 2010; Uzzi et al. 2013 (without its supplement);
  Blythe 2014; Pierce & Paulos 2014; Coulton, Lindley & Akmal 2016. Each is an essay, a method described by its
  authors, or one study: the notes say which.
- **Part of the text:** Bell, Blythe & Sengers 2005 (the argument and the method, not the three accounts of
  homes); Alvesson & Sandberg 2011 (the method section); Elsden et al. 2017 (the method and the guidelines, not
  the three cases); Nosek et al. 2018 (the abstract and six sections); Lakens 2022 (resource constraints, the
  detectable effect, sensitivity analysis); Si, Yang & Hashimoto 2024 and Si, Hashimoto & Yang 2025 (the design,
  the main results and the limits; not the appendices); Nielsen & Landauer 1993 (the model).
- **Documentation:** the G*Power 3.1 manual of 1 June 2023, three sections, read on 2026-11-22.
- **Abstract only:** Gick & Holyoak 1980; Kurtz & Snowden 2003 (the domains come from van Beurden et al. 2011);
  Auger 2013; Eypasch et al. 1995; Yilmaz et al. 2016, on which no rule rests.
- **A summary on the authors' page, not the paper:** Chan et al. 2015. **An earlier post by the author, not the
  article:** Norman 1999.
- **Not read:** Tversky & Kahneman 1983, from general knowledge, unverified; Chambers 2013, title only, on which
  no rule rests. De Bono and Dunne & Raby are used as methods only.
- **Read for version 1.0.0 or 1.1.3, as their notes record it, and not again for 1.2.0:** Gentner 1983 and
  Meadows 1999 (from the PDF, with pages), van Beurden et al. 2011 (on the publisher's page; in full, according
  to the note on Kurtz & Snowden), Abson et al. 2017 (on PubMed Central), Phadnis et al. 2015 (page 1 of an
  author's manuscript).
