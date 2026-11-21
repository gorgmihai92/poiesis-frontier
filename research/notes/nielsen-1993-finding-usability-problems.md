# A mathematical model of the finding of usability problems (Nielsen & Landauer, 1993)

- **Source:** Proceedings of INTERCHI '93 (CHI 1993): 206–213 · https://doi.org/10.1145/169059.169166 (pages =
  the proceedings' printed pages)
- **File:** none; read in the ACM Digital Library's reader. The reader's text is from a scan, and Table 1 is
  partly garbled in it.
- **Licence:** © ACM 1993; free to read on the publisher's site, not open-licence: local only.
- **Evidence:** empirical, a model fitted to data · 11 studies (5 with test users, 6 with expert evaluators),
  13 datasets (p. 206–207).
- **Read:** part of the text: the abstract, the datasets with Table 1, and the section on the model (p. 206–
  208), on 2026-11-22. Not read: the sections on estimating what is left to find and on costs and benefits
  (p. 209–213).

## What it says
- The number of problems found at least once by i people is modelled as N(1 − (1 − λ)^i), where N is the number
  of problems there are and λ is the chance that one person turns up the average problem (p. 208).
- Across the studies λ ran from 0.12 to 0.58, with a mean of 0.31 (Table 1, p. 207, read from a damaged
  table).
- The model assumes that finding a problem with one person is independent of the others, and that problems are
  independent of each other. The authors call the second a simplification: difficulties tend to occur together,
  and problems differ in how easy they are to find (p. 207–208).
- With test users, what is found also depends on the experimenter noticing it (p. 208).

## What it means for the plugin
- `power.py see` uses the per-problem form of the formula: the chance that something each person shows with
  probability p turns up at least once among n people is 1 − (1 − p)^n. It answers "what could five people
  let me see?" for a qualitative probe.
- The value of p is not known in advance, and the paper's 0.31 is an average over interface tests of the
  early 1990s. The playbook asks for a range of p and never quotes 0.31 as a fact about a new study.
- Independence is assumed. People recruited from one circle, or tested together, are less independent than the
  formula takes them to be, so the real chance is lower.
- No quote is kept from this source: the scan renders equation 1 with wrong characters (the λ comes out as "A"
  or "k"), so the formula above is written from the equation and the paragraph that explains it.
