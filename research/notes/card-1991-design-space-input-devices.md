# A morphological analysis of the design space of input devices (Card, Mackinlay & Robertson, 1991)

- **Source:** ACM Transactions on Information Systems 9(2): 99–122 · https://doi.org/10.1145/123078.128726 (pages =
  the journal's printed pages)
- **File:** none; read in the ACM Digital Library's reader, where the article is marked "free access".
- **Licence:** © ACM 1991; free to read on the publisher's site, not open-licence: local only.
- **Evidence:** analytical · a method shown on one domain (input devices), with back-of-the-envelope calculations.
  Not a study of whether the method finds better designs than another method.
- **Read:** full text, p. 99–120, on 2026-11-22. Not read: the reference list (p. 120–122).

## What it says
- Morphological design space analysis takes different designs as points in a design space described by
  parameters. The goal is to find abstractions both for generating the space and for testing the designs in it
  (p. 99, 101).
- The technique was used before on other design spaces: Bertin on graphics, Zwicky on jet engines. In both, the
  authors say, the result was insight into the space and novel designs (p. 101).
- The space is generated from two things: a vocabulary of primitives (here, the physical properties a device can
  sense) and a small set of composition operators (merge, layout, connect) (p. 102–104).
- A table of the space classified nearly all existing devices; voice was the exception. New devices are generated
  by placing marks in other cells of the table (p. 107–108).
- Many of the devices generated this way "might be undesirable" (p. 108).
- Points are then tested on two criteria taken from Mackinlay: expressiveness (the input conveys exactly and only
  the intended meaning) and effectiveness (how well it does so). Figures of merit for effectiveness include desk
  footprint, pointing speed, precision, errors, time to learn, user preference and cost (p. 108–109).
- A calculation on the space pointed to a region the authors call promising (devices driven by the fingers).
  Whether that performance can be reached "is unknown" (p. 117).
- The stated virtue: one can generate regions of the space and calculate their consequences, then put prototyping
  effort where the analysis shows promise. The calculations are "highly approximative" on purpose (p. 120).

## What it means for the plugin
- The design-space playbook follows the paper's two halves: generate (name the dimensions and their values, place
  what exists, read the empty cells) and test (each cell worth pursuing becomes a concept with its experiment).
- An empty cell is a candidate, not a recommendation: the paper itself says many generated points are undesirable.
- The paper shows the method on one domain, by the method's authors. It is a way to generate, not evidence that
  what it generates is better.

## Quotes
- "different input device designs are taken as points in a parametrically described design space" (p. 99)
- "it can be used both to classify nearly all existing devices and to generate ideas for new devices not yet invented" (p. 108)
- "Of course, many of these devices might be undesirable" (p. 108)
