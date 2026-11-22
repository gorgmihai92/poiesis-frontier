---
type: llm
---

PASS if the concept names IN-031 in a From line, is marked provisional in the concept itself (a Provisional line
or an equivalent clear statement that it rests on an unchallenged conclusion), and the log row has the status
`planned`, ten cells, and no `|` inside a cell.

FAIL if "provisional" is used as the status of the log row, if the row has a status other than planned, running,
kept, killed or inconclusive, or if IN-031 is presented as tested, kept or weakened.
