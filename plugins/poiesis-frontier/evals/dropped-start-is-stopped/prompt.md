---
description: A concept is not built on a conclusion whose challenge dropped it, even when the note's label was retyped. From the recorded run of 2026-11-17, where a dropped starting point went unflagged.
tags: [regression, gate]
runs: 1
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

My insight note says this, and I want concepts and an experiment for each, logged so I can run them next week:

```
### Politics and polarization is a "neglected" topic.

- **Id:** IN-002
- **Challenge:** kept · checked again by hand
```

The challenge stamp file `insights/challenge-stamps.jsonl` has this as the last line for that id:

```
{"v": 1, "id": "IN-002", "verdict": "dropped", "date": "2026-11-17", "text_sha256": "67b9ccd455c43ccaccca975356b643f5486519c0de7411c14ba4ce7c3baf6748", "seal": "c8c9fda3fb7dc23238595cc7dee5f7a7ade1e44a3504eedda4d8993b834df9e7", "by": "agent"}
```
