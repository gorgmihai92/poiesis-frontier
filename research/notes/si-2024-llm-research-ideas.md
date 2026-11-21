# Can LLMs generate novel research ideas? A large-scale human study with 100+ NLP researchers (Si, Yang & Hashimoto, 2024)

- **Source:** arXiv preprint 2409.04109, version 1 of 6 September 2024 · https://arxiv.org/abs/2409.04109 (pages =
  PDF pages)
- **File:** `../papers/si-2024-can-llms-generate-novel-research-ideas.pdf`
- **Licence:** arXiv preprint; licence not checked: kept local.
- **Evidence:** empirical · research ideas on seven topics in language-model prompting: 49 written by
  researchers, 49 produced by one idea-generating agent, 49 produced by the agent and re-ranked by a person;
  reviewed blind by 79 researchers (p. 1–2).
- **Read:** part of the text: the abstract and the opening (p. 1–2), section 3.2 on generating and removing
  duplicates (p. 5–6), sections 6.2 and 6.3 on the reviews (p. 12–13) and section 7 on the limits of the models
  (p. 13–15), on 2026-11-22. Not read: the statistical tests of section 5, the examples, and the appendices
  (p. 16–94).

## What it says
- The agent was asked for 4,000 seed ideas on each topic, with the titles of all its earlier ideas in the prompt
  and an instruction not to repeat them (p. 5–6).
- An idea counted as a duplicate when its text was more than 0.8 similar to an earlier one, by a sentence
  embedding; the threshold was set by looking at examples. **About 5% were not duplicates: 200 of 4,000**
  (p. 6, 13–14).
- The share of new ideas fell with each further batch, and the count of distinct ideas levelled off. Asking for
  more mostly repeated what was there (p. 13–14).
- Reviewers judged the agent's ideas more novel than the researchers' (p < 0.05) and slightly less feasible
  (p. 1). This is a judgement of ideas on paper, before anyone carried them out.
- Judging ideas is unreliable. Two halves of the reviewers agreed 56.1% of the time on which ideas were in the
  top and bottom quarter, where chance is 50% (p. 13). Overall scores followed novelty and excitement and hardly
  followed feasibility (p. 12–13).
- Models did no better as judges: the best automatic ranker agreed with the reviewers 53.3% of the time (p. 14).
- The researchers placed their own submitted ideas at about the middle of what they usually have, so the
  comparison is with ordinary expert ideas, not their best (p. 12).

## What it means for the plugin
- The rule on distinct ideas: a report says how many concepts were generated, how many are distinct, and how
  "the same" was judged. More generated is not more ideas.
- When a method stops giving new concepts, the playbooks change the method or the operator; they do not ask for
  more of the same.
- The figure of 5% belongs to one agent, one kind of idea, one similarity measure and one threshold. The rule
  takes the pattern (most of a large batch repeats), not the number.
- Neither the model's own ranking nor a quick human rating of an idea on paper is treated as a test. That is
  why concepts are ordered by what their experiment would teach.

## Quotes
- "This leaves about 5% non-duplicated ideas out of all the generated seed ideas." (p. 6)
- "out of the 4000 generated seed ideas, there are only 200 non-duplicate … unique ideas" (p. 13)
- "LLMs cannot evaluate ideas reliably yet" (p. 14)
