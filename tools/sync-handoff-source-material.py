#!/usr/bin/env python3
"""Publish the parent SOURCE-MATERIAL.md into handoff/state/, with its one redaction.

Why this exists. The published copy is a hand copy with a hand edit, and on 7 November 2026
it was found to be two whole sections behind its source -- a cloud session reading handoff/
knew nothing about either 7 November source or the two gaps they exposed. eval-review.html
cannot drift because a generator owns it; this file had no owner. Now it does.

Run it from anywhere:   python3 tools/sync-handoff-source-material.py
Check without writing:  python3 tools/sync-handoff-source-material.py --check

--check exits 1 when the copy is stale, so it can gate a commit.
"""
import io, os, re, sys, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC  = os.path.join(os.path.dirname(REPO), "SOURCE-MATERIAL.md")
DST  = os.path.join(REPO, "handoff", "state", "SOURCE-MATERIAL.md")

# (regex matching what appears in the parent, what the published copy must say instead)
REDACTIONS = [
    (r"/mnt/c/[Uu]sers/[^/\s]+/claude/resume/", "<PARENT-DIR-WITHHELD>/"),
]

# Nothing matching these may reach the published copy. Checked AFTER redaction.
#
# These are SHAPES, never values. This file is tracked in a PUBLIC repository, so a list
# of literal secrets here would publish the very strings it exists to withhold -- which is
# exactly what the first version of this file did, caught by a pre-push scan on
# 7 November 2026 before anything left the machine. Matching the shape is also the better
# guard: it catches a DIFFERENT tenant hostname or a DIFFERENT video id, which a literal
# list never would.
FORBIDDEN = [
    (r"[A-Za-z0-9-]+\.outsystems\.dev",          "an ODC tenant hostname"),
    (r"youtu\.be/|youtube\.com/(watch|embed)",   "a YouTube link (the concept video is unlisted)"),
    (r"zoom\.us/(rec|j)/",                        "a Zoom recording or meeting link"),
    (r"/mnt/c/[Uu]sers/",                         "an absolute path on A.J.'s machine"),
    (r"[A-Za-z0-9._%+-]+@gmail\.com",             "a personal email address"),
]


def build():
    if not os.path.exists(SRC):
        sys.exit(f"source not found: {SRC}")
    text = io.open(SRC, encoding="utf-8").read()
    applied = []
    for pattern, repl in REDACTIONS:
        text, n = re.subn(pattern, repl, text)
        if n:
            applied.append(f"{repl} x{n}")
    leaks = []
    for pattern, what in FORBIDDEN:
        m = re.search(pattern, text)
        if m:
            # name the KIND and the line, never the matched value
            line = text[:m.start()].count("\n") + 1
            leaks.append(f"{what} (line {line})")
    if leaks:
        sys.exit("REFUSING TO PUBLISH -- these reached the output:\n  "
                 + "\n  ".join(leaks))
    return text, applied


def main():
    check = "--check" in sys.argv
    text, applied = build()
    current = io.open(DST, encoding="utf-8").read() if os.path.exists(DST) else None

    if current == text:
        print(f"in step  {os.path.relpath(DST, REPO)}  ({len(text):,} bytes)")
        return 0

    if check:
        a = (current or "").split("\n")
        b = text.split("\n")
        d = [l for l in difflib.unified_diff(a, b, "published", "parent", n=0)
             if l[:1] in "+-" and l[:3] not in ("+++", "---")]
        print(f"STALE    {os.path.relpath(DST, REPO)}  {len(d)} lines differ")
        for l in d[:12]:
            print("   ", l[:110])
        if len(d) > 12:
            print(f"    ... and {len(d)-12} more")
        print("\nRun without --check to republish.")
        return 1

    io.open(DST, "w", encoding="utf-8", newline="\n").write(text)
    was = f"{len(current):,}" if current is not None else "absent"
    print(f"published {os.path.relpath(DST, REPO)}  {was} -> {len(text):,} bytes")
    for a in applied:
        print(f"  redacted {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
