#!/usr/bin/env python3
"""Check an experiment log, check what each concept starts from, and give out ids. Run with `python3 -I`.

  experiments.py frontier/experiments.md
  experiments.py gate frontier/<date>-<topic>.md [--write] [--strict]
  experiments.py ids CN [frontier]
  experiments.py ids --list [frontier]

The log. Columns: id | concept | assumption | prediction | kill criterion | criterion written | started | due |
status | result. Status is planned, running, kept, killed or inconclusive. Prints the count per status, experiments
past their due date that are not finished, and rows that break the rules: no kill criterion, no date for it, a kill
criterion written after the experiment started, or a finished experiment with no result.

The gate. A concept is a heading with `- **Id:** CN-001` and `- **From:** IN-001, IN-004` under it. Each id in
From is looked up in the challenge stamps (insights/challenge-stamps.jsonl, written by poiesis-insight) and in
the notes of insights/ and foresight/. One line per concept:
  THROUGH      every starting point is kept or weakened, its stamp is intact and its sentence is unchanged
  PROVISIONAL  a starting point has no stamp, or its stamp or its sentence was changed, or none is named
  STOPPED      a starting point was dropped
--write puts the result in the note, as a `Provisional` or a `Stopped` line under the concept. Nothing is ever
written to the experiment log. Exit code 1 when a concept is stopped or a provisional one does not say so in the
note; with --strict also when any concept is provisional or was not checked. `gate -h` has the options.

Ids. `ids CN` prints the next free concept id in the folders given (ST for a study design, E for an experiment);
`ids --list` prints the ids in use and exits 1 when one is under two headings.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

STATUSES = ("planned", "running", "kept", "killed", "inconclusive")
FINISHED = ("kept", "killed", "inconclusive")

# The challenge stamp, format 1 (poiesis-insight 2.0.0). Verified here with this script's own code, so the gate
# works when poiesis-insight is not installed.
SEAL_HEAD = "poiesis-challenge-stamp v1"
VERDICTS = ("kept", "weakened", "dropped")
STAMPS = "insights/challenge-stamps.jsonl"
NOTE_FOLDERS = ("insights", "foresight")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HEADING = re.compile(r"^#{1,6}[ \t]+(.*)$")
FENCE = re.compile(r"^[ \t]*(```|~~~)")
ID_LINE = re.compile(r"^[ \t]*[-*+][ \t]+\*\*id:?\*\*:?[ \t]*(\S+)[ \t]*$", re.IGNORECASE)
CHECKED = re.compile(r"[ \t]*·[ \t]*checked \d{4}-\d{2}-\d{2}[ \t]*$")
PREFIXES = {"CN": "a concept", "ST": "a study design", "E": "an experiment"}
NOTHING = {"", "none", "-", "–", "—", "n/a"}


def field(name: str) -> re.Pattern:
    """A line such as `- **Challenge:** kept · reason`, whatever the case of the name."""
    return re.compile(r"^[ \t]*[-*+][ \t]+\*\*" + name + r":?\*\*:?[ \t]*(.*)$", re.IGNORECASE)


CHALLENGE, FROM, PROVISIONAL, STOPPED = field("challenge"), field("from"), field("provisional"), field("stopped")
STARTING_POINT, LOG_ID = field("starting point"), field("log id")


# ---------------------------------------------------------------------------------------------------------------
# The experiment log
# ---------------------------------------------------------------------------------------------------------------

def rows(path: Path) -> list[list[str]]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or set(line) <= {"|", "-", " "}:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0].lower() != "id" and not cells[0].startswith("<"):
            out.append(cells)
    return out


def check_log(log: Path) -> int:
    today = dt.date.today().isoformat()
    counts = {s: 0 for s in STATUSES}
    overdue, problems, bad = [], [], []
    for r in rows(log):
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


# ---------------------------------------------------------------------------------------------------------------
# Reading notes and stamps
# ---------------------------------------------------------------------------------------------------------------

def text_sha256(text: str) -> str:
    """The hash of a conclusion's sentence: NFC, runs of the six layout characters to one space, trimmed."""
    text = unicodedata.normalize("NFC", text)
    text = re.sub("[\t\n\x0b\x0c\r ]+", " ", text).strip(" ")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def seal(id_: str, verdict: str, date: str, sha: str) -> str:
    return hashlib.sha256("\n".join([SEAL_HEAD, id_, verdict, date, sha]).encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    """A note's text. A byte-order mark at the start is not part of it."""
    return path.read_bytes().decode("utf-8-sig", errors="replace")


def blocks(text: str) -> list[dict]:
    """The headings of a note, each with the lines under it up to the next heading of any level.

    Lines inside fenced code are not read. Each block: heading (the sentence), start and end (line numbers from 0,
    end excluded), fields (line numbers of the lines that are not in fenced code).
    """
    out: list[dict] = []
    fenced = False
    lines = text.split("\n")
    for i, raw in enumerate(lines):
        line = raw.rstrip("\r")
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = HEADING.match(line)
        if m:
            if out:
                out[-1]["end"] = i
            out.append({"heading": m.group(1), "start": i, "end": len(lines), "fields": []})
        elif out:
            out[-1]["fields"].append(i)
    for b in out:
        b["lines"] = lines
    return out


def first(block: dict, pattern: re.Pattern) -> tuple[int, str] | None:
    """The first line of the block that matches: (line number, what follows the field's name)."""
    for i in block["fields"]:
        m = pattern.match(block["lines"][i].rstrip("\r"))
        if m:
            return i, m.group(1)
    return None


def block_id(block: dict) -> str | None:
    found = first(block, ID_LINE)
    return found[1] if found else None


def shown_verdict(block: dict) -> str | None:
    """The first word of the Challenge line, in lower case: `**Kept** · …` gives kept."""
    found = first(block, CHALLENGE)
    if not found:
        return None
    word = re.search(r"[A-Za-z]+", found[1])
    return word.group(0).lower() if word else ""


def load_stamps(path: Path) -> tuple[dict[str, tuple[int, dict]], str | None]:
    """The stamp in force for each id (its last line), and what is wrong with the file, if anything."""
    if not path.is_file():
        return {}, None
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return {}, "it is not UTF-8"
    last: dict[str, tuple[int, dict]] = {}
    for n, line in enumerate(text.split("\n"), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            return {}, f"line {n} is not JSON"
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str):
            return {}, f"line {n} is not a stamp"
        last[obj["id"]] = (n, obj)
    return last, None


def stamp_intact(obj: dict) -> bool:
    v = obj.get("v")
    verdict, date, sha = obj.get("verdict"), obj.get("date"), obj.get("text_sha256")
    return (
        type(v) is not bool and v == 1
        and verdict in VERDICTS
        and isinstance(date, str) and bool(DATE.match(date))
        and isinstance(sha, str) and bool(HEX64.match(sha))
        and obj.get("seal") == seal(obj["id"], verdict, date, sha)
    )


def conclusions(folders: list[Path], extra: list[Path]) -> dict[str, list[tuple[Path, dict]]]:
    """Every object with an Id line in the notes of the folders: id -> [(file, block), …]."""
    files: list[Path] = []
    for folder in folders:
        if folder.is_dir():
            files += sorted(p for p in folder.rglob("*.md") if p.is_file())
    files += [p for p in extra if p.is_file()]
    found: dict[str, list[tuple[Path, dict]]] = {}
    read: set[Path] = set()
    for path in files:
        if path.resolve() in read:
            continue
        read.add(path.resolve())
        for block in blocks(read_text(path)):
            id_ = block_id(block)
            if id_:
                found.setdefault(id_, []).append((path, block))
    return found


# ---------------------------------------------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------------------------------------------

def from_ids(value: str) -> list[str]:
    """The ids and keys of a From line: comma-separated, each taken up to its first space."""
    out: list[str] = []
    for part in value.split(","):
        token = part.strip().strip("`").strip()
        token = token[2:-2].strip() if token.startswith("[[") and token.endswith("]]") else token
        token = token.split()[0] if token.split() else ""
        token = token.strip("`").rstrip(".;")
        if token.lower() not in NOTHING and token not in out:
            out.append(token)
    return out


def check_start(id_: str, stamps: dict, damaged: str | None, found: dict, stamps_name: str, root: Path) -> tuple[str, str]:
    """One starting point: ("ok" | "stop" | "open", what to say about it)."""
    places = found.get(id_, [])
    block = places[0][1] if len(places) == 1 else None
    shown = shown_verdict(block) if block else None
    said = f'the note shows "{shown}"' if shown in VERDICTS else ""

    def stop_on_label(why: str) -> tuple[str, str] | None:
        return ("stop", f"{id_} the note says dropped ({why})") if shown == "dropped" else None

    if len(places) > 1:
        names = ", ".join(sorted({_rel(p, root) for p, _ in places}))
        return "open", f"{id_} is under two headings ({names}): neither can be verified"
    if damaged:
        return stop_on_label("the stamp file is damaged") or (
            "open", f"{id_} stamp file damaged ({damaged}): no verdict in it can be trusted")
    if id_ not in stamps:
        if block is None:
            where = " or ".join(f"{f}/" for f in NOTE_FOLDERS)
            return "open", f"{id_} no stamp, and no conclusion with this id in {where}"
        return stop_on_label("no stamp") or (
            "open", f"{id_} no stamp: no challenge is recorded" + (f" ({said})" if said else ""))
    line, obj = stamps[id_]
    if not stamp_intact(obj):
        return stop_on_label("its stamp was altered") or (
            "open", f"{id_} stamp altered: line {line} of {stamps_name} does not match its seal")
    verdict, date = obj["verdict"], obj["date"]
    if block is None:
        if verdict == "dropped":
            return "stop", f"{id_} dropped {date} (its note was not found, so the sentence was not compared)"
        return "open", f"{id_} {verdict} {date} on record, but no note with this id was found, so the sentence was not compared"
    if obj["text_sha256"] != text_sha256(block["heading"]):
        return stop_on_label(f"its sentence was changed after it was stamped {verdict} on {date}") or (
            "open", f"{id_} text changed: the sentence is not the one stamped {verdict} on {date}")
    if verdict == "dropped":
        return "stop", f"{id_} dropped {date}" + (f" ({said}: the stamp is the record)" if said and shown != verdict else "")
    if shown == "dropped":
        return "stop", f"{id_} the note says dropped (the stamp says {verdict}, {date}: one of the two is wrong)"
    return "ok", f"{id_} {verdict} {date}" + (f" ({said}: the stamp is the record)" if said and shown != verdict else "")


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def gate_concept(block: dict, stamps: dict, damaged: str | None, found: dict, stamps_name: str, root: Path) -> dict:
    """The gate's result for one concept: state (through, provisional, stopped), why, and a line per start."""
    start = first(block, FROM)
    ids = from_ids(start[1]) if start else []
    if not ids:
        return {"state": "provisional", "why": "no starting point is named", "starts": [],
                "record": "no starting point is named"}
    checks = [check_start(i, stamps, damaged, found, stamps_name, root) for i in ids]
    stops = [i for i, (kind, _) in zip(ids, checks) if kind == "stop"]
    opens = [i for i, (kind, _) in zip(ids, checks) if kind == "open"]
    record = "; ".join(text for _, text in checks)
    if stops:
        return {"state": "stopped", "why": _list(stops) + (" was" if len(stops) == 1 else " were") + " dropped",
                "starts": [t for _, t in checks], "record": record}
    if opens:
        return {"state": "provisional", "why": _list(opens) + (" was" if len(opens) == 1 else " were")
                + " not challenged on record", "starts": [t for _, t in checks], "record": record}
    return {"state": "through", "why": "every starting point is kept or weakened, with its stamp",
            "starts": [t for _, t in checks], "record": record}


def _list(ids: list[str]) -> str:
    return ids[0] if len(ids) == 1 else ", ".join(ids[:-1]) + " and " + ids[-1]


def mark(result: dict, today: str) -> tuple[str, str]:
    """The line the gate keeps in the note: (field name, value)."""
    if result["state"] == "stopped":
        return "Stopped", f"{result['record']} · checked {today}"
    word = "yes" if result["state"] == "provisional" else "no"
    return "Provisional", f"{word} · {result['record']} · checked {today}"


def noted(block: dict) -> tuple[str | None, str | None]:
    """What the note says now: ("stopped" | "yes" | "no" | None, the record without its date)."""
    stopped, provisional = first(block, STOPPED), first(block, PROVISIONAL)
    if stopped:
        return "stopped", CHECKED.sub("", stopped[1]).strip()
    if provisional:
        value = CHECKED.sub("", provisional[1]).strip()
        word = re.match(r"[A-Za-z]+", value)
        rest = value.split("·", 1)[1].strip() if "·" in value else ""
        return (word.group(0).lower() if word else ""), rest
    return None, None


def write_marks(path: Path, text: str, concepts: list[tuple[dict, dict]], today: str) -> bool:
    """Put each concept's Provisional or Stopped line under it. True when the note changed."""
    lines = text.split("\n")
    for block, result in sorted(concepts, key=lambda c: c[0]["start"], reverse=True):
        name, value = mark(result, today)
        anchor = first(block, FROM) or first(block, ID_LINE)
        anchor_line = lines[anchor[0]]
        lead = re.match(r"^[ \t]*[-*+][ \t]+", anchor_line).group(0)
        ending = "\r" if anchor_line.endswith("\r") else ""
        old = [i for i in block["fields"] if PROVISIONAL.match(lines[i].rstrip("\r")) or STOPPED.match(lines[i].rstrip("\r"))]
        for i in sorted(old, reverse=True):
            del lines[i]
        at = anchor[0] - sum(1 for i in old if i < anchor[0]) + 1
        lines.insert(at, f"{lead}**{name}:** {value}{ending}")
    new = "\n".join(lines)
    if new == text:
        return False
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(new.encode("utf-8"))
    os.replace(tmp, path)
    return True


def project_root(note: Path) -> Path:
    """The folder that holds frontier/, insights/ and foresight/: above the note's frontier folder, else here."""
    for parent in note.resolve().parents:
        if parent.name == "frontier":
            return parent.parent
    return Path.cwd()


def open_experiments(log: Path, concept: str, log_id: str | None) -> list[str]:
    """Experiments of a concept that are still planned or running."""
    out = []
    for r in rows(log):
        if len(r) < 10 or r[8].lower() not in ("planned", "running"):
            continue
        if re.search(r"(?<![\w-])" + re.escape(concept) + r"(?![\w-])", r[1]) or (log_id and r[0] == log_id):
            out.append(f"{r[0]} is {r[8].lower()}")
    return out


def gate(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="experiments.py gate",
        description="Check what each concept in a frontier note starts from, against the challenge stamps.")
    ap.add_argument("note", type=Path, help="the frontier note, e.g. frontier/2026-11-22-topic.md")
    ap.add_argument("--write", action="store_true", help="put each result in the note, as a Provisional or a Stopped line")
    ap.add_argument("--strict", action="store_true", help="exit 1 unless every concept is through")
    ap.add_argument("--root", type=Path, help="the project's folder (default: the folder above the note's frontier/)")
    ap.add_argument("--stamps", type=Path, help=f"the stamp file (default: {STAMPS} in the project)")
    ap.add_argument("--notes", type=Path, action="append", help="a folder of notes to look the ids up in; repeat it "
                    "(default: insights/ and foresight/ in the project)")
    ap.add_argument("--log", type=Path, help="the experiment log (default: experiments.md next to the note)")
    ap.add_argument("--today", help="the date to write as checked, YYYY-MM-DD (default: today)")
    a = ap.parse_args(argv)
    if not a.note.is_file():
        print(f"{a.note}: no such note", file=sys.stderr)
        return 2
    if a.today and not DATE.match(a.today):
        print("--today takes a date as YYYY-MM-DD", file=sys.stderr)
        return 2
    today = a.today or dt.date.today().isoformat()
    root = a.root or project_root(a.note)
    stamps_path = a.stamps or root / STAMPS
    stamps_name = _rel(stamps_path, root)
    stamps, damaged = load_stamps(stamps_path)
    hinted = []
    for _, obj in stamps.values():
        where = obj.get("where")
        if isinstance(where, str) and where.endswith(".md"):
            path = (root / where).resolve()
            if root.resolve() in path.parents:
                hinted.append(path)
    found = conclusions(a.notes or [root / f for f in NOTE_FOLDERS], hinted)

    text = read_text(a.note)
    concepts, unchecked, twice = [], [], []
    seen: dict[str, int] = {}
    for block in blocks(text):
        id_ = block_id(block)
        if id_ and id_.startswith("CN-"):
            seen[id_] = seen.get(id_, 0) + 1
            if seen[id_] == 1:
                concepts.append((block, gate_concept(block, stamps, damaged, found, stamps_name, root)))
            elif id_ not in twice:
                twice.append(id_)
        elif not id_ and (first(block, STARTING_POINT) or first(block, FROM)):
            unchecked.append(block["heading"])
    concepts = [(b, r) for b, r in concepts if block_id(b) not in twice]

    log = a.log or a.note.with_name("experiments.md")
    words = {"through": "THROUGH", "provisional": "PROVISIONAL", "stopped": "STOPPED"}
    unmarked = stale = 0
    for block, result in concepts:
        id_ = block_id(block)
        print(f"{words[result['state']]} {id_}: {result['why']}")
        for line in result["starts"]:
            print("  " + line)
        if result["state"] == "stopped" and log.is_file():
            log_id = first(block, LOG_ID)
            token = re.search(r"E-\d+", log_id[1]) if log_id else None
            for line in open_experiments(log, id_, token.group(0) if token else None):
                print(f"  {line} in {_rel(log, root)}: a stopped concept gets no experiment")
        if a.write:
            continue
        says, record = noted(block)
        want = {"stopped": "stopped", "provisional": "yes", "through": "no"}[result["state"]]
        if says is None and result["state"] == "through":
            continue
        if says != want:
            unmarked += 1
            name, value = mark(result, today)
            print(f"  NOT MARKED: the note {'has no line for this' if says is None else 'says otherwise'}. "
                  f"Run again with --write, or put under the concept: - **{name}:** {value}")
        elif record != result["record"]:
            stale += 1
            print(f'  MARK OUT OF DATE: the note records "{record}". Run again with --write')
    for id_ in twice:
        print(f"TWICE {id_}: this id is under two headings in the note, so neither was checked")
    for heading in unchecked:
        print(f'NO ID "{heading[:70]}": no Id line, so nothing was checked')

    count = {s: sum(1 for _, r in concepts if r["state"] == s) for s in words}
    summary = f"{len(concepts)} concept{'s' if len(concepts) != 1 else ''}: {count['through']} through, " \
              f"{count['provisional']} provisional, {count['stopped']} stopped."
    if unchecked or twice:
        summary += f" Not checked: {len(unchecked) + len(twice)}."
    print(summary)
    if damaged:
        print(f"Stamps: {stamps_name} is damaged ({damaged}). No verdict in it can be trusted until it is repaired.")
    elif stamps_path.is_file():
        print(f"Stamps: {stamps_name}, {len(stamps)} id{'s' if len(stamps) != 1 else ''}.")
    else:
        print(f"Stamps: no file at {stamps_name}, so no challenge is on record here.")
    if a.write:
        changed = write_marks(a.note, text, concepts, today)
        print(f"{'Saved' if changed else 'Unchanged'}: {a.note}")
    failed = count["stopped"] or unmarked or twice
    if a.strict:
        failed = failed or count["provisional"] or unchecked or stale
    return 1 if failed else 0


# ---------------------------------------------------------------------------------------------------------------
# Ids
# ---------------------------------------------------------------------------------------------------------------

def ids(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="experiments.py ids",
        description="Give the next free id, or list the ids in use. Numbers are never reused: an id that is only "
                    "mentioned (in a From line, in the log) counts as taken.",
        epilog="ids CN [FOLDER …] prints the next free id: CN a concept, ST a study design, E an experiment. "
               "ids --list [FOLDER …] prints every id in use. The folder is frontier unless one is given.")
    ap.add_argument("--list", action="store_true", help="list the ids in use, and exit 1 when one is under two headings")
    ap.add_argument("args", nargs="*", metavar="PREFIX|FOLDER")
    a = ap.parse_args(argv)
    args = list(a.args)
    prefix = None
    if not a.list:
        if not args or args[0] not in PREFIXES:
            ap.error("give a prefix (CN a concept, ST a study design, E an experiment), or --list")
        prefix = args.pop(0)
    folders = [Path(x) for x in args] or [Path("frontier")]
    files = sorted({p for f in folders if f.is_dir() for p in f.rglob("*.md") if p.is_file()})
    for f in folders:
        if not f.is_dir():
            print(f"(no folder {f})", file=sys.stderr)
    if a.list:
        places: dict[str, list[str]] = {}
        for path in files:
            for block in blocks(read_text(path)):
                id_ = block_id(block)
                if id_:
                    places.setdefault(id_, []).append(f"{path.as_posix()}: {block['heading'][:70]}")
        for id_ in sorted(places, key=_id_key):
            for place in places[id_]:
                print(f"{id_}  {place}")
        twice = sorted((i for i, found in places.items() if len(found) > 1), key=_id_key)
        for id_ in twice:
            print(f"TWICE {id_}: under {len(places[id_])} headings")
        return 1 if twice else 0
    highest = 0
    pattern = re.compile(r"(?<![\w-])" + prefix + r"-(\d+)(?![\w-])")
    for path in files:
        for m in pattern.finditer(read_text(path)):
            highest = max(highest, int(m.group(1)))
    print(f"{prefix}-{highest + 1:03d}")
    return 0


def _id_key(id_: str) -> tuple[str, int, str]:
    m = re.match(r"^(.*?)(\d+)$", id_)
    return (m.group(1), int(m.group(2)), id_) if m else (id_, 0, id_)


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "gate":
        return gate(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == "ids":
        return ids(sys.argv[2:])
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("log", type=Path)
    a = p.parse_args()
    return check_log(a.log)


if __name__ == "__main__":
    sys.exit(main())
