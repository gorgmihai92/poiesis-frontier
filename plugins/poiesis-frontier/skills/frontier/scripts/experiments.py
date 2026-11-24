#!/usr/bin/env python3
"""Check an experiment log, check what each concept starts from, and give out ids. Run with `python3 -I`.

  experiments.py frontier/experiments.md
  experiments.py gate frontier/<date>-<topic>.md [--write] [--strict]
  experiments.py ids CN [frontier]
  experiments.py ids --list [frontier]

The log. Columns: id | concept | assumption | prediction | kill criterion | criterion written | started | due |
status | result. Status is planned, running, kept, killed or inconclusive. Prints the count per status, experiments
past their due date that are not finished, and rows that break the rules: no kill criterion, no date for it, a kill
criterion written after the experiment started, a finished experiment with no result, or an assumption, prediction
or kill criterion that DIFFERS from the concept's own line. The concept is the one whose id starts the concept cell,
looked up in the report the cell names, else in the notes next to the log; one that is not found is a note on
stderr, not a failure.

The gate. A concept is a heading with `- **Id:** CN-001` and `- **From:** IN-001, IN-004` under it. Each id in
From is looked up in the challenge stamps (insights/challenge-stamps.jsonl, written by poiesis-insight) and in
the notes of insights/ and foresight/. One line per concept:
  THROUGH      every starting point is kept or weakened, its stamp is intact and its sentence is unchanged
  PROVISIONAL  a starting point has no stamp, or its stamp or its sentence was changed, or none is named
  STOPPED      a starting point was dropped
--write puts the result in the note, as a `Provisional` or a `Stopped` line under the concept. Nothing is ever
written to the experiment log. Exit code 1 when a concept is stopped or a provisional one does not say so in the
note; with --strict also when any concept is provisional or was not checked; 2 when --write is refused because
the note is not UTF-8 (the results are printed first). `gate -h` has the options.

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

# The challenge stamp, format 1 (poiesis-insight 2.0.0; the reference is its skills/insight/stamp-format.md).
# Verified here with this script's own code, so the gate works when poiesis-insight is not installed. The patterns
# for reading a note are the reference's, copied as they are.
SEAL_HEAD = "poiesis-challenge-stamp v1"
VERDICTS = ("kept", "weakened", "dropped")
STAMPS = "insights/challenge-stamps.jsonl"
NOTE_FOLDERS = ("insights", "foresight")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
STAMP_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEADING = re.compile(r"^#{1,6}[ \t]+(.*)$")
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
ID_LINE = re.compile(r"^[ \t]*(?:[-*+][ \t]+(?:\*\*)?|\*\*)id(?:\*\*)?[ \t]*:(?:\*\*)?[ \t]*(\S+)[ \t]*$", re.IGNORECASE)
CHALLENGE = re.compile(r"^[ \t]*(?:[-*+][ \t]+(?:[*_]{1,2})?|[*_]{1,2})challenge[a-z ]*?(?:[*_]{1,2})?[ \t]*"
                       r"(?::(?:[*_]{1,2})?|(?:[*_]{1,2})?:|[*_]{2}[ \t])[ \t]*(.*)$", re.IGNORECASE)
VERDICT_WORD = re.compile(r"\b(kept|weakened|dropped)\b", re.IGNORECASE)
OBJECT_ID = re.compile(r"(?<![A-Za-z0-9-])[A-Z]{1,3}-[0-9]+(?![A-Za-z0-9-])")
ITEM = re.compile(r"^[ \t]*[-*+][ \t]+")
NEGATION = re.compile(r"\b(?:not|no|never|un\w*)\b", re.IGNORECASE)
CHECKED = re.compile(r"[ \t]*·[ \t]*checked \d{4}-\d{2}-\d{2}[ \t]*$")
PREFIXES = {"CN": "a concept", "ST": "a study design", "E": "an experiment"}
NOTHING = {"", "none", "-", "–", "—", "n/a"}


def field(name: str) -> re.Pattern:
    """A line such as `- **From:** IN-001`, whatever the case of the name, read like the reference's Id line:
    the list dash and the bold marks may be left out, the colon may not."""
    return re.compile(r"^[ \t]*(?:[-*+][ \t]+(?:\*\*)?|\*\*)" + name + r"(?:\*\*)?[ \t]*:(?:\*\*)?[ \t]*(.*)$",
                      re.IGNORECASE)


FROM, PROVISIONAL, STOPPED = field("from"), field("provisional"), field("stopped")
STARTING_POINT, LOG_ID = field("starting point"), field("log id")
ASSUMPTION, PREDICTION, KILL = field("assumption"), field("prediction"), field("kill criterion")
WRITTEN = re.compile(r"[ \t]*·[ \t]*written \d{4}-\d{2}-\d{2}")
CELL_ID = re.compile(r"^[\s*_`\[]*(CN-[0-9]+)(?![\w-])")
CN_ANYWHERE = re.compile(r"(?<![\w-])CN-[0-9]+(?![\w-])")
CELL_PATH = re.compile(r"[^\s()\[\]<>`*]+\.md\b")
CELL_LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]*)?\]\]")


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
    notes: dict = {}  # the notes next to the log, read once when a row needs them
    for r in rows(log):
        if len(r) < 10:
            bad.append(r[0])
            continue
        eid, concept, assumption, prediction, kill, written, started, due, status, result = r[:10]
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
        problems += same_as_concept(log, eid, concept, {"assumption": assumption, "prediction": prediction,
                                                         "kill criterion": kill}, notes)
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


def same_as_concept(log: Path, eid: str, cell: str, cells: dict[str, str], notes: dict) -> list[str]:
    """The row's assumption, prediction and kill criterion against the concept's lines: one DIFFERS per cell.

    The row's cells are the concept's lines copied word for word; the kill criterion without its ` · written <date>`.
    Both sides are normalised as a stamped sentence is (`normalise`). A row whose concept cell starts with no
    concept id is not compared (logs from before 1.2.0). A concept that is not found, or is under two headings, is
    a note on stderr: the row is not compared and the exit code does not change.
    """
    m = CELL_ID.match(cell)
    if not m:
        if CN_ANYWHERE.search(cell):
            print(f"({eid}: the concept cell does not start with the concept's id; its assumption, prediction and "
                  "kill criterion were not compared)", file=sys.stderr)
        return []
    cid = m.group(1)
    root = project_root(log)
    found, where = concept_block(log, cid, cell, root, notes)
    if found is None:
        print(f"({eid}: {where}; its assumption, prediction and kill criterion were not compared)",
              file=sys.stderr)
        return []
    path, block = found
    out = []
    for (name, row), pattern in zip(cells.items(), (ASSUMPTION, PREDICTION, KILL)):
        if pattern is KILL and (not row or row.startswith("<")):
            continue  # already "no kill criterion"
        own = wrapped(block, pattern)
        if own is None:
            print(f"({eid}: {cid} in {_rel(path, root)} has no {name.capitalize()} line, so the {name} was not "
                  "compared)", file=sys.stderr)
            continue
        own = WRITTEN.sub("", own, count=1) if pattern is KILL else own
        if normalise(row) != normalise(own):
            out.append(f"{eid}: {name} DIFFERS from {cid} in {_rel(path, root)}\n"
                       f"    concept: {normalise(own)}\n    row:     {normalise(row)}")
    return out


def wrapped(block: dict, pattern: re.Pattern) -> str | None:
    """A field's value with the lines it is wrapped onto, read as poiesis-insight's `field` reads one: the value
    ends at an empty line, at the next list item, at a line that starts with a bold label, or at a heading."""
    found = first(block, pattern)
    if found is None:
        return None
    index, value = found
    parts = [value]
    for i in block["fields"]:
        if i <= index:
            continue
        line = block["lines"][i].rstrip("\r")
        if i != index + len(parts) or not line.strip() or ITEM.match(line) or line.lstrip().startswith("**"):
            break
        parts.append(line)
    return " ".join(parts)


def concept_block(log: Path, cid: str, cell: str, root: Path, notes: dict) -> tuple[tuple[Path, dict] | None, str]:
    """The concept with this id: in the report the cell names, if it is there; else the one heading with this Id
    in the notes of the log's folder (as the gate finds conclusions). (None, why) when there is not exactly one."""
    named: list[Path] = []
    for token in CELL_PATH.findall(cell):
        named += [root / token, log.parent / token, log.parent / Path(token).name]
    for link in CELL_LINK.findall(cell):
        name = link.strip() if link.strip().endswith(".md") else link.strip() + ".md"
        named += [log.parent / name] + sorted(log.parent.rglob(Path(name).name))
    files = list(dict.fromkeys(p.resolve() for p in named if p.is_file()))
    for path in files:
        hits = [b for b in blocks(read_text(path)) if block_id(b) == cid]
        if len(hits) == 1:
            return (path, hits[0]), ""
    if "found" not in notes:
        notes["found"] = conclusions([log.parent], [])
    places = notes["found"].get(cid, [])
    folder = _rel(log.parent, root) + "/"
    if len(places) == 1:
        return places[0], ""
    if places:
        names = ", ".join(sorted({_rel(p, root) for p, _ in places}))
        return None, f"{cid} is under {len(places)} headings ({names})"
    if files:
        said = f"{cid} is not in {', '.join(_rel(p, root) for p in files)}, and "
    else:
        said = "the report the row names is not there, and " if named else ""
    return None, f"{said}no heading has Id {cid} in {folder}"


# ---------------------------------------------------------------------------------------------------------------
# Reading notes and stamps
# ---------------------------------------------------------------------------------------------------------------

def normalise(text: str) -> str:
    """NFC, runs of the six layout characters to one space, trimmed."""
    text = unicodedata.normalize("NFC", text)
    return re.sub("[\t\n\x0b\x0c\r ]+", " ", text).strip(" ")


def text_sha256(text: str) -> str:
    """The hash of a conclusion's sentence, normalised (`normalise`)."""
    return hashlib.sha256(normalise(text).encode("utf-8")).hexdigest()


def seal(id_: str, verdict: str, date: str, sha: str) -> str:
    return hashlib.sha256("\n".join([SEAL_HEAD, id_, verdict, date, sha]).encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    """A note's text. A byte-order mark at the start is not part of it. Bytes that are not UTF-8 are read as U+FFFD,
    so a sentence with them never matches its stamp; such a note is never written back (see `gate`)."""
    return path.read_bytes().decode("utf-8-sig", errors="replace")


def is_utf8(path: Path) -> bool:
    try:
        path.read_bytes().decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def blocks(text: str) -> list[dict]:
    """The headings of a note, each with the lines under it up to the next heading of any level.

    Lines inside fenced code are not read. Each block: heading (the sentence), start and end (line numbers from 0,
    end excluded), fields (line numbers of the lines that are not in fenced code).
    """
    out: list[dict] = []
    fence = ""  # the mark that opened the fenced block we are in, or ''
    lines = text.split("\n")  # at line feeds only
    for i, raw in enumerate(lines):
        line = raw[:-1] if raw.endswith("\r") else raw
        hit = FENCE.match(line)
        if hit:
            mark = hit.group(1)
            if not fence:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence) and not line.strip()[len(mark):].strip():
                fence = ""
            continue
        if fence:
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
        line = block["lines"][i]
        m = pattern.match(line[:-1] if line.endswith("\r") else line)
        if m:
            return i, m.group(1)
    return None


def block_id(block: dict) -> str | None:
    found = first(block, ID_LINE)
    return found[1] if found else None


def shown_verdicts(block: dict) -> tuple[str, ...] | None:
    """The verdict words of the Challenge label, in lower case and in order, up to the `·` that starts its reason.

    None when there is no label. `**Kept** · …` gives (kept,); `weakened → kept` gives both; a label with a word
    of negation, such as `not challenged` or `not weakened`, gives none.
    """
    found = first(block, CHALLENGE)
    if not found:
        return None
    head = found[1].split("·")[0]
    words = tuple(dict.fromkeys(w.lower() for w in VERDICT_WORD.findall(head)))
    return () if words and NEGATION.search(head) else words


def load_stamps(path: Path) -> tuple[dict[str, tuple[int, dict]], str | None]:
    """The stamp in force for each id (its last line), and what is wrong with the file, if anything."""
    if not path.is_file():
        return {}, None
    try:
        text = path.read_bytes().decode("utf-8-sig")
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
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str) or not STAMP_ID.match(obj["id"]):
            return {}, f"line {n} is not a stamp with a readable id"
        last[obj["id"]] = (n, obj)
    return last, None


def stamp_intact(obj: dict) -> bool:
    v = obj.get("v")
    verdict, date, sha = obj.get("verdict"), obj.get("date"), obj.get("text_sha256")
    return (
        type(v) is int and v == 1
        and verdict in VERDICTS
        and isinstance(date, str) and bool(DATE.match(date)) and _real_date(date)
        and isinstance(sha, str) and bool(HEX64.match(sha))
        and obj.get("seal") == seal(obj["id"], verdict, date, sha)
    )


def _real_date(value: str) -> bool:
    try:
        dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


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
    """The ids and keys of a From value.

    Every object id in it (two or three capital letters, a dash, digits: IN-002, SC-001) is taken wherever it
    stands, so `IN-001 and IN-002`, `IN-001; IN-002`, `[IN-002](…)` or `**IN-002**` each name every id they hold.
    Besides those, each comma-separated part that names no object id is a key (a note's name or a citation key),
    taken up to its first space. `none` and a dash name nothing.
    """
    out: list[str] = []
    for part in re.split(r"[,;/]|\s+(?:and|&)\s+|^\s*[-*+]\s+|\s[-*+]\s+", value):
        ids = OBJECT_ID.findall(part)
        if ids:
            out += [i for i in dict.fromkeys(ids) if i not in out]
            continue
        token = part.strip().strip("`*_").strip()
        token = token[2:-2].strip() if token.startswith("[[") and token.endswith("]]") else token
        token = token.split()[0] if token.split() else ""
        token = token.strip("`*_[]()").rstrip(".;:")
        if token.lower() not in NOTHING and token not in out:
            out.append(token)
    return out


def from_value(block: dict) -> tuple[int, str, int] | None:
    """The From line with the lines it runs on to: (its line, the whole value, the value's last line).

    A value runs on over the lines indented more than the From line, including a nested list of ids; it ends at an
    empty line, at a line indented no more than the From line, or at a line that starts with a bold label."""
    found = first(block, FROM)
    if not found:
        return None
    index, value = found
    parts, last = [value], index
    own = len(block["lines"][index]) - len(block["lines"][index].lstrip(" \t"))
    for i in block["fields"]:
        if i <= index:
            continue
        line = block["lines"][i]
        line = line[:-1] if line.endswith("\r") else line
        indent = len(line) - len(line.lstrip(" \t"))
        if i != last + 1 or not line.strip() or indent <= own or line.lstrip().startswith("**") \
                or HEADING.match(line):
            break
        parts.append(line.strip())
        last = i
    return index, " ".join(parts), last


def check_start(id_: str, stamps: dict, damaged: str | None, found: dict, stamps_name: str, root: Path,
                follow: bool = True) -> tuple[str, str]:
    """One starting point: ("ok" | "stop" | "via" | "open", what to say about it).

    "via" is a stop one step away: the start is not a conclusion (a research question, say) and what it rests
    on, in its own From line, was dropped. Following From can only stop a concept; it never lets one through.
    """
    places = found.get(id_, [])
    block = places[0][1] if len(places) == 1 else None
    shown = shown_verdicts(block) if block else None
    said = f'the note shows "{" and ".join(shown)}"' if shown else ""

    def drift(verdict: str) -> str:
        """What the label says against the stamp; the stamp is the record."""
        if shown is None or shown == (verdict,):
            return ""
        if not shown:
            return " (the note's label holds no verdict: the stamp is the record)"
        return f" ({said}: the stamp is the record)"

    def stop_on_label(why: str) -> tuple[str, str] | None:
        return ("stop", f"{id_} the note says dropped ({why})") if shown and "dropped" in shown else None

    if len(places) > 1:
        names = ", ".join(sorted({_rel(p, root) for p, _ in places}))
        if not damaged and id_ in stamps and stamp_intact(stamps[id_][1]) and stamps[id_][1]["verdict"] == "dropped":
            obj = stamps[id_][1]
            return "stop", f"{id_} dropped {obj['date']} (it is under two headings, {names}, so the sentence was not compared)"
        if any("dropped" in (shown_verdicts(b) or ()) for _, b in places):
            return "stop", f"{id_} the note says dropped (it is under two headings, {names})"
        return "open", f"{id_} is under two headings ({names}): neither can be verified"
    if damaged:
        return stop_on_label("the stamp file is damaged") or (
            "open", f"{id_} stamp file damaged ({damaged}): no verdict in it can be trusted")
    if id_ not in stamps:
        if block is None:
            where = " or ".join(f"{f}/" for f in NOTE_FOLDERS)
            return "open", f"{id_} no stamp, and no conclusion with this id in {where}"
        rests = from_value(block)
        if shown is None and rests and follow:
            inner = [check_start(i, stamps, damaged, found, stamps_name, root, follow=False)
                     for i in from_ids(rests[1]) if i != id_]
            if inner:
                texts = "; ".join(text for _, text in inner)
                if any(kind in ("stop", "via") for kind, _ in inner):
                    return "via", f"{id_} rests on a dropped conclusion ({texts})"
                return "open", f"{id_} no stamp and no Challenge line, so it was not challenged; it rests on {texts}"
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
        return "stop", f"{id_} dropped {date}" + drift(verdict)
    if shown and "dropped" in shown:
        return "stop", f"{id_} the note says dropped (the stamp says {verdict}, {date}: one of the two is wrong)"
    return "ok", f"{id_} {verdict} {date}" + drift(verdict)


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def gate_concept(block: dict, stamps: dict, damaged: str | None, found: dict, stamps_name: str, root: Path) -> dict:
    """The gate's result for one concept: state (through, provisional, stopped), why, and a line per start."""
    start = from_value(block)
    ids = from_ids(start[1]) if start else []
    if not ids:
        return {"state": "provisional", "why": "no starting point is named", "starts": [],
                "record": "no starting point is named"}
    checks = [check_start(i, stamps, damaged, found, stamps_name, root) for i in ids]
    stops = [i for i, (kind, _) in zip(ids, checks) if kind == "stop"]
    via = [i for i, (kind, _) in zip(ids, checks) if kind == "via"]
    opens = [i for i, (kind, _) in zip(ids, checks) if kind == "open"]
    record = "; ".join(text for _, text in checks)
    if stops or via:
        why = [_list(stops) + (" was" if len(stops) == 1 else " were") + " dropped"] if stops else []
        why += [_list(via) + (" rests" if len(via) == 1 else " rest") + " on a dropped conclusion"] if via else []
        return {"state": "stopped", "why": "; ".join(why), "starts": [t for _, t in checks], "record": record}
    if opens:
        return {"state": "provisional", "why": _list(opens) + " could not be verified",
                "starts": [t for _, t in checks], "record": record}
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
        start = from_value(block)
        head = start[0] if start else first(block, ID_LINE)[0]
        anchor = (start[2] if start else head, "")
        head_line = lines[head]
        item = ITEM.match(head_line)
        lead = item.group(0) if item else re.match(r"^[ \t]*", head_line).group(0) + "- "
        anchor_line = lines[anchor[0]]
        ending = "\r" if anchor_line.endswith("\r") else ""
        old = [i for i in block["fields"] if PROVISIONAL.match(lines[i].rstrip("\r")) or STOPPED.match(lines[i].rstrip("\r"))]
        for i in sorted(old, reverse=True):
            del lines[i]
        at = anchor[0] - sum(1 for i in old if i < anchor[0]) + 1
        lines.insert(at, f"{lead}**{name}:** {value}{ending}")
    new = "\n".join(lines)
    if new == text:
        return False
    bom = b"\xef\xbb\xbf" if path.read_bytes().startswith(b"\xef\xbb\xbf") else b""
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(bom + new.encode("utf-8"))
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
    if a.write and not is_utf8(a.note):
        print(f"Not saved: {a.note} is not UTF-8 text, and writing it back would change its other bytes. "
              "Save it as UTF-8 first.")
        return 2
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
