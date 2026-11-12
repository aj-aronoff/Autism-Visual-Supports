#!/usr/bin/env python3
"""Turn a reply pasted out of the agent app into a board page, on this computer.

    python3 board-from-reply.py reply.txt  [--who "7 year old daughter"] [--out DIR]
    pbpaste | python3 board-from-reply.py -                 (or paste, then Ctrl-D)
    python3 board-from-reply.py reply.txt --json-only       (just print the JSON)

The app prints the board it saved as one compact line at the very end of its reply:

    BOARD-JSON: {"supportType":"FirstThenBoard", ...}

That marker exists because of what a person actually does: copy the WHOLE reply, not
an exact selection. This script finds the object inside the paste, and then hands it
to make-board-page.py, which stays the only thing that writes a board page - so the
boardKey is still derived in one place and guardrail 1 is still checked in one place.

It REFUSES and names the reason rather than writing half a board. Nothing here
invents a card, a label or a theme.
"""
import argparse, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GENERATOR = os.path.join(HERE, "make-board-page.py")
MARKER = re.compile(r"BOARD-JSON\s*:", re.I)


def slice_object(s, start):
    """From the '{' at start, return the matching '}' index, string-aware."""
    depth, i, n = 0, start, len(s)
    in_str, esc = False, False
    while i < n:
        c = s[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def extract(text):
    """(obj, how) or (None, why). Never guesses at a board; only finds one."""
    s = text.strip()
    if not s:
        return None, "nothing to read - the paste was empty"

    # The LAST marker wins: a copied conversation can hold several boards, and the
    # one a parent means is the one they just made.
    marks = list(MARKER.finditer(s))
    if marks:
        after = marks[-1].end()
        a = s.find("{", after)
        if a < 0:
            return None, ("there is a BOARD-JSON line but no object after it - the "
                          "paste may have been cut short")
        b = slice_object(s, a)
        if b < 0:
            return None, ("the BOARD-JSON object is not closed - the paste was cut "
                          "off before the end of the line")
        try:
            return json.loads(s[a:b + 1]), "from the BOARD-JSON line"
        except ValueError as e:
            return None, "the BOARD-JSON object could not be read - %s" % e

    # No marker: walk every '{' and take the first object that is actually a board.
    # This is what steps over a debug block, which prints JSON of its own.
    saw_json = False
    a = s.find("{")
    while a >= 0:
        b = slice_object(s, a)
        if b > a:
            try:
                o = json.loads(s[a:b + 1])
            except ValueError:
                o = None
            if isinstance(o, dict):
                saw_json = True
                if "supportType" in o:
                    return o, "found an object with no BOARD-JSON marker"
        a = s.find("{", a + 1)
    if saw_json:
        return None, ("that paste holds JSON, but none of it is a board - nothing in "
                      "it carries supportType")
    return None, ("no board JSON in that paste. With EmitBoardJson on, the reply ends "
                  "with a line beginning BOARD-JSON:")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reply", nargs="?", default="-",
                    help="file holding the pasted reply, or - for standard input")
    ap.add_argument("--who", default="",
                    help='relationship, never a name, e.g. "7 year old daughter"')
    ap.add_argument("--out", default=HERE)
    ap.add_argument("--theme", default="")
    ap.add_argument("--json-only", action="store_true",
                    help="print the extracted board JSON and stop")
    a = ap.parse_args()

    if a.reply == "-":
        text = sys.stdin.read()
    else:
        with open(a.reply, encoding="utf-8", errors="replace") as fh:
            text = fh.read()

    obj, how = extract(text)
    if obj is None:
        sys.exit("refused: %s" % how)

    if a.json_only:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
        return

    # hand it to the generator, which owns the boardKey and guardrail 1
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                      encoding="utf-8")
    try:
        json.dump(obj, tmp, ensure_ascii=False)
        tmp.close()
        cmd = [sys.executable, "-I", GENERATOR, tmp.name, "--out", a.out]
        if a.who:
            cmd += ["--who", a.who]
        if a.theme:
            cmd += ["--theme", a.theme]
        r = subprocess.run(cmd, capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            sys.exit(r.returncode)
        # keep the agent's own words beside the page, named after the same key
        key = ""
        for line in r.stdout.splitlines():
            if line.strip().startswith("boardKey"):
                key = line.split(None, 1)[1].strip()
        if key:
            keep = os.path.join(a.out, key + "-source.json")
            with open(keep, "w", encoding="utf-8") as fh:
                json.dump(obj, fh, indent=2, ensure_ascii=False)
            print("  source    %s  (%s)" % (os.path.basename(keep), how))
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


if __name__ == "__main__":
    main()
