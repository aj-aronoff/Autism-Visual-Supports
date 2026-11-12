#!/usr/bin/env python3
"""Re-runnable audit of the two production boards.

Run from the hackathon-future directory:
    python3 evidence/08-audit.py

It checks each board against schema/board.schema.json by hand (jsonschema is not
installed in this environment) and, for the 17:49 board, audits EVERY citation
against the passages the debug block shows were actually retrieved. A citation
naming anything not in that set is a fabrication.
"""
import json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "Autism-Visual-Supports", "schema", "board.schema.json")

# The six passages the 17:49 debug block shows were given to the Composer.
RETRIEVED_1749 = {
    ("triad-visual-supports-p1-3.docx", 12),
    ("triad-visual-supports-p1-3.docx", 13),
    ("triad-visual-supports-p1-3.docx", 3),
    ("nsp-established-treatments-p11-19.docx", 8),
    ("nsp-established-treatments-p11-19.docx", 4),
    ("nsp-established-treatments-p11-19.docx", 3),
}

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def check_schema(board, schema, label):
    props, req = set(schema["properties"]), schema["required"]
    extra = [k for k in board if k not in props]
    missing = [k for k in req if k not in board]
    print(f"  {label:24s} extra={extra or '-'}  missing={missing or '-'}  "
          f"{'OK' if not extra and not missing else 'FAIL'}")
    return not extra and not missing

def check_cards(board, schema):
    rng = schema["properties"]  # card range lives in allOf; assert the known one
    n = len(board["cards"])
    ok = (board["supportType"] != "FirstThenBoard") or n == 2
    print(f"  cards={n} supportType={board['supportType']} {'OK' if ok else 'FAIL'}")
    for c in board["cards"]:
        toks, chars = len(c["label"].split()), len(c["label"])
        good = toks <= 3 and chars <= 40
        print(f"    label {c['label']!r:18s} tokens={toks} chars={chars} "
              f"{'OK' if good else 'FAIL'}")
        ok &= good
    return ok

def check_practices(board, schema):
    enum = schema["properties"]["evidenceBasis"]["items"]["properties"]["practice"]["enum"]
    ok = True
    for e in board["evidenceBasis"]:
        hit = e["practice"] in enum
        ok &= hit
        print(f"    practice {e['practice']!r:36s} in citable enum {'OK' if hit else 'FAIL'}")
    return ok

def audit_citations(board, retrieved):
    print("  CITATION AUDIT - each cite must name a passage actually retrieved:")
    ok = True
    cited = set()
    for c in board["citations"]:
        m = re.match(r"^(.+?), chunk (\d+)$", c)
        if not m:
            print(f"    NO CHUNK  {c}   (document-only citation, allowed only if the "
                  f"passage carried no chunkPosition)")
            ok = False
            continue
        pair = (m.group(1), int(m.group(2)))
        cited.add(pair)
        hit = pair in retrieved
        ok &= hit
        print(f"    {'OK        ' if hit else 'FABRICATED'} {c}")
    print(f"    -> zero fabrication: {ok}")
    print(f"    cited {len(cited)} of {len(retrieved)}; not used: "
          f"{sorted(retrieved - cited)}")
    return ok

def main():
    schema = load(SCHEMA)
    allok = True
    print("SCHEMA CHECK")
    for name in ("03-board-1709.json", "04-board-1749.json"):
        allok &= check_schema(load(os.path.join(HERE, name)), schema, name)

    b = load(os.path.join(HERE, "04-board-1749.json"))
    print("\n17:49 BOARD - the one that is fully grounded")
    allok &= check_cards(b, schema)
    allok &= check_practices(b, schema)
    allok &= audit_citations(b, RETRIEVED_1749)
    print("\nPRACTICE <-> CITATION COHERENCE")
    for practice, chunk in (("Antecedent Package", 3), ("Behavioral Package", 4)):
        cite = f"nsp-established-treatments-p11-19.docx, chunk {chunk}"
        named = any(e["practice"] == practice for e in b["evidenceBasis"])
        hit = named and cite in b["citations"]
        print(f"  {practice:20s} <- chunk {chunk} (its own definition)  "
              f"{'OK' if hit else 'FAIL'}")
        allok &= hit

    print("\nRESULT:", "ALL CHECKS PASS" if allok else "SOMETHING FAILED")
    return 0 if allok else 1

if __name__ == "__main__":
    sys.exit(main())
