#!/usr/bin/env python3
"""Check an experiment log (Markdown table). Run with `python3 -I`.

  experiments.py frontier/experiments.md

Columns: id | concept | assumption | prediction | kill criterion | criterion written | started | due | status |
result. Status is planned, running, kept, killed or inconclusive. Prints the count per status, experiments past
their due date that are not finished, and rows that break the rules: no kill criterion, no date for it, a kill
criterion written after the experiment started, or a finished experiment with no result.
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

STATUSES = ("planned", "running", "kept", "killed", "inconclusive")
FINISHED = ("kept", "killed", "inconclusive")


def rows(path: Path) -> list[list[str]]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or set(line) <= {"|", "-", " "}:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0].lower() != "id" and not cells[0].startswith("<"):
            out.append(cells)
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("log", type=Path)
    a = p.parse_args()
    today = dt.date.today().isoformat()
    counts = {s: 0 for s in STATUSES}
    overdue, problems, bad = [], [], []
    for r in rows(a.log):
        if len(r) < 10:
            bad.append(r[0])
            continue
        eid, concept, _assumption, _prediction, kill, written, started, due, status, result = r[:10]
        status = status.lower()
        if status not in counts:
            bad.append(eid)
            continue
        counts[status] += 1
        if not kill or kill.startswith("<"):
            problems.append(f"{eid}: no kill criterion")
        if not written:
            problems.append(f"{eid}: kill criterion not dated")
        elif started and written > started:
            problems.append(f"{eid}: kill criterion written {written}, after the start {started}")
        if status in FINISHED and not result:
            problems.append(f"{eid}: {status} but no result")
        if status not in FINISHED and due and due < today:
            overdue.append(f"{eid} (due {due}, {status}): {concept}")
    total = sum(counts.values())
    print(f"{total} experiments: " + ", ".join(f"{n} {s}" for s, n in counts.items()))
    done = sum(counts[s] for s in FINISHED)
    if done:
        print(f"Finished: {done}; killed {counts['killed']} of them ({counts['killed'] / done:.0%})")
    if overdue:
        print("\nPast their due date, not finished:")
        for o in overdue:
            print("  " + o)
    if problems:
        print("\nBreaks the rules:")
        for pr in problems:
            print("  " + pr)
    if bad:
        print("\nRows not understood: " + ", ".join(bad))
    return 1 if problems or bad else 0


if __name__ == "__main__":
    sys.exit(main())
