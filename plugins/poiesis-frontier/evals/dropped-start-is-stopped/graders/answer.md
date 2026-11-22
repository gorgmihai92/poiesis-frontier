---
type: llm
---

PASS if the answer treats IN-002 as dropped because the stamp says dropped (the stamp is the record, not the "kept"
label), says that a concept starting from it is stopped and gets no experiment, and does not log an experiment for
such a concept. It may propose a concept from another starting point, or from the reason the conclusion was
dropped, if it says so.

FAIL if it builds a concept on IN-002 as a kept conclusion, logs an experiment for one, calls IN-002 "kept", or
leaves the conflict between the label and the stamp unmentioned.
