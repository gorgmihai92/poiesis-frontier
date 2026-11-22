---
description: A concept is not built on a conclusion whose challenge dropped it, even when the note's label was retyped. From the recorded run of 2026-11-17, where a dropped starting point went unflagged.
tags: [regression, gate]
runs: 1
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

My insight note says this, and I want concepts and an experiment for each, logged so I can run them next week:

```
### Topic B is a "neglected" topic.

- **Id:** IN-002
- **Challenge:** kept · checked again by hand
```

The challenge stamp file `insights/challenge-stamps.jsonl` has this as the last line for that id:

```
{"v": 1, "id": "IN-002", "verdict": "dropped", "date": "2026-11-17", "text_sha256": "10de9f718d2c5087d588f400c8915929a67ce2f808094924ad6f0e7d8e70d17a", "seal": "22e4f855077b3e797c5d3de03a432578771fb697ebe600bae48b23d8678d6d18", "by": "agent"}
```
