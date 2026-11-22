# Design space

Lay out every way an interaction could work as a table of choices, place what exists in it, and read the cells
nobody has filled. It answers "how else could this work?" for one interaction at a time.

## Read first
`card-1991-design-space-input-devices` in `research/notes` of the plugin's repository, read in full. The authors
describe input devices as points in a space built from a few primitives and a few ways to combine them, place
existing devices in a table, and generate new ones from its other cells. They say many of the generated points
are undesirable, and that a calculation on the space pointed to a promising region whose performance they could
not confirm. It is one domain, analysed by the method's authors: it shows how to generate, not that what is
generated is better.

## Build the space
1. **The interaction, without its usual form.** One sentence: what the person and the system have to get done
   between them ("confirm an action that cannot be undone", not "a confirmation dialog"). `playbooks/concepts.md`,
   step 2, gives the purpose.
2. **What exists.** List five to ten existing ways it is done, each with where it comes from: the project, a
   research note (note and page), or "from general knowledge, unverified".
3. **The dimensions.** Take the existing ways two at a time and ask what differs between them. Each difference
   that could vary without the others is a dimension; its values are what it can be. Keep three to five
   dimensions with two to four values each, and name each from the differences found. As a prompt only (this
   plugin's list, not the source's): who acts first; when (before, during, after); through which sense or
   movement; how much is asked of the person; what is shown; whether it can be taken back; who else sees it.
4. **The table.** Two dimensions make the rows and the columns; the others are written inside the cells or as
   one table per value. Place every existing way in its cell. If one cannot be placed, a dimension is missing:
   add it and place them again.
5. **Combinations.** The source combines its primitives in three ways: merged into one, laid out side by side,
   and one connected to the next. Note which values of this space can be joined in those ways. A combination is
   one more point in the space.

## Read the empty cells
6. For each empty cell say which of three it is:
   - **impossible:** the values exclude each other; say why;
   - **undesirable:** it can be built and there is a known reason not to; give the reason and its source;
   - **untried:** no reason is known.
7. Keep the untried cells. Each is a candidate, not a recommendation and not yet "new": an empty cell in this
   table means no existing way was listed there. Whether anything exists there is a search, not a guess.
   [poiesis-research](https://github.com/gorgmihai92/poiesis-research), `prior-art`, finds the nearest
   existing work; without it, write "prior art not checked".
8. **How a point will be judged.** Before choosing among the untried cells, name two or three measures a point
   in this space is judged by. The source's list for input devices: speed, precision, errors, time to learn,
   preference, cost. They become the experiment's measure.

## Out
- The table goes in the frontier note, with the dimensions, where each existing way sits, and the three kinds
  of empty cell.
- Each untried cell that is kept becomes a concept with **Method:** `design space (dimension = value, …)`, and
  goes through `playbooks/experiment.md`. A concept from a cell starts at the sketch stage.
- Report how many cells there are, how many are filled, and how many of the empty ones are untried.
