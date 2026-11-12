#!/usr/bin/env python3
"""Stamp out one First-Then board page per board (decision d8, 8 Nov 2026).

    python3 make-board-page.py <board.json> [--who "7 year old daughter"] [--out DIR]

<board.json> is anything valid against Autism-Visual-Supports/schema/board.schema.json
with supportType FirstThenBoard. The output is a self-contained HTML page carrying
that board and its own boardKey, so each board keeps a separate history: a separate
file, a separate browser store, a separate JSON.

boardKey is written ONCE, here. The page never recomputes it from the card labels,
because editing a label would otherwise split the history in two.
"""
import json, re, sys, os, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_THEME = "Happy dinosaur at home"
TEMPLATE = os.path.join(HERE, "first-then-board.html")
BLOCK = re.compile(
    r'(<script type="application/json" id="BOARD">)(.*?)(</script>)', re.S)


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "-", str(s or "").strip()).strip("-")
    return s or "board"


# GUARDRAIL 1, the same pattern as schema/board.schema.json
# $defs/card/properties/label, and the same check first-then-board.html enforces in
# its editor: one to three space-separated tokens, 40 characters. Checked HERE so it
# covers every route in - a hand-written JSON, a fixture, or a reply pasted out of the
# agent app. If these three ever disagree, the schema is the one that is right.
LABEL_RE = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9'\u2019-]*( [A-Za-z0-9][A-Za-z0-9'\u2019-]*){0,2}$")


def label_problem(v):
    t = str(v or "").strip()
    if not t:
        return "a card needs a label"
    if len(t) > 40:
        return "too long, 40 characters at most (%d here)" % len(t)
    if len(t.split()) > 3:
        return "three words at most (%d here)" % len(t.split())
    if not LABEL_RE.match(t):
        return "letters, numbers, hyphens and apostrophes only"
    return ""


def read_board(path):
    with open(path, encoding="utf-8") as fh:
        o = json.load(fh)
    if o.get("supportType") != "FirstThenBoard":
        sys.exit("not a FirstThenBoard: supportType is %r" % o.get("supportType"))
    cards = o.get("cards") or []
    first = next((c for c in cards if c.get("role") == "First"), None)
    then = next((c for c in cards if c.get("role") == "Then"), None)
    if not first or not then:
        sys.exit("that board has no First card, no Then card, or neither")
    for role, card in (("First", first), ("Then", then)):
        bad = label_problem(card.get("label"))
        if bad:
            sys.exit("refusing to write: the %s card label is invalid - %s: %r"
                     % (role, bad, card.get("label")))
    ev = ""
    basis = o.get("evidenceBasis") or []
    if basis and isinstance(basis[0], dict):
        ev = " — ".join(x for x in (basis[0].get("practice"),
                                        basis[0].get("technique")) if x)
    saying = ""
    for line in (o.get("script") or []):
        if line.get("phase") == "Before":
            saying = line.get("phrase", "")
            break
    return o, first, then, ev, saying


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--who", default="",
                    help='relationship, never a name, e.g. "7 year old daughter"')
    ap.add_argument("--out", default=HERE)
    ap.add_argument("--theme", default="",
                    help='override the board\'s theme, e.g. "Happy dinosaur at home"')
    a = ap.parse_args()

    o, first, then, ev, saying = read_board(a.board)
    # the board JSON names a theme when the agent could derive one. A parent page
    # with none shows a plain board, so fall back to the suggested default -- that is
    # the PARENT picking, not the Composer inventing one to dodge the TBD sentinel.
    theme = a.theme or o.get("theme") or DEFAULT_THEME
    if theme == "TBD" and not a.theme:
        theme = DEFAULT_THEME
    key = slug(first["label"]) + "-" + slug(then["label"])
    if a.who:
        key += "-" + slug(a.who)

    cfg = {
        "boardKey": key,
        "boardId": o.get("agentRunId", ""),
        "supportType": o["supportType"],
        "title": o.get("title", "First Then board"),
        "theme": theme,
        "evidence": ev,
        "first": {"label": first["label"]},
        "then": {"label": then["label"]},
        "saying": saying,
        # the grown-up panel is rendered from these two; without them a generated
        # page prints two pictures and no plan
        "script": o.get("script", []),
        "plan": o.get("plan", {}),
        "sensorySupports": o.get("sensorySupports", []),
        "evidenceBasis": o.get("evidenceBasis", []),
        "citations": o.get("citations", []),
    }

    with open(TEMPLATE, encoding="utf-8") as fh:
        html = fh.read()
    if len(BLOCK.findall(html)) != 1:
        sys.exit("the template no longer has exactly one BOARD block")
    if "</script>" in json.dumps(cfg):
        sys.exit("refusing to write: the board text would close the script tag")

    body = "\n" + json.dumps(cfg, indent=2, ensure_ascii=True) + "\n"
    html = BLOCK.sub(lambda m: m.group(1) + body + m.group(3), html, count=1)

    out = os.path.join(a.out, key.lower() + ".html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote %s" % out)
    print("  boardKey  %s" % key)
    print("  history   %s-history.json, and a browser store of its own" % key)


if __name__ == "__main__":
    main()
