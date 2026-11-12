#!/usr/bin/env python3
"""The agent loop, drawn as a loop. Autism Visual Supports.

    python3 assets/build_pipeline.py

Writes 1920x1080 plus a 2560x1440 retina pass:
  agent-loop*        the reference drawing, with the three stop-marks keyed
  agent-loop-slide*  the deck version -- larger type, no footer, no key

Separate from build_diagram.py on purpose, and it does NOT import it: that file
renders at import time, so importing it would restamp four PNGs as a side effect.
The palette is deliberately the same four diagram colours plus two marks:
AMBER for a clinical judgement, RED for a stop with a safety cost.

Why this file exists at all: build_diagram.py draws TRUST BOUNDARIES -- who owns
which security control. It is not the agent loop, and the hackathon's own guidance
asks for the loop: framework, model, tools. Nothing in this project had ever drawn
one. Written 10 November 2026.

Every claim on the drawing is traceable:
  escalation first, zero tokens ........ evidence/01, 9 Nov 16:33
  rule 17 in code ...................... evidence/02, 9 Nov 16:36
  two queries, two knowledge bases ..... evidence/05
  eleven checks, one retry ............. CLAUDE.md section 4
  save before review ................... CLAUDE.md section 4, held four times
  fifteen questions, cannot edit ....... prompts/reviewer.md
  temperature 1, not by choice ......... evidence/10, Bedrock rejects 0.2
  Bedrock or Azure OpenAI .............. evidence/15, 10 Nov 00:15
"""
import os
import subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
W, H = 1920, 1080

INK     = "#2D3748"
GRAY    = "#718096"
GRAY_LT = "#CBD5E0"
PAPER   = "#FFFFFF"
OURS    = "#006B3C"
OURS_BG = "#EBF7F0"
EXT     = "#A8600C"
EXT_BG  = "#FDF6EC"
AMBER   = "#8A5A00"      # a clinical judgement
AMBER_BG= "#FDF3D6"
RED     = "#99272B"      # stops, and has a safety cost
RED_BG  = "#FAE3E3"

FONT = "'Trebuchet MS','Segoe UI',Verdana,sans-serif"

# --- geometry ---------------------------------------------------------------
# Seven stages on one strip. The widths are equal because no stage is more
# important than another to a reader seeing it for the first time.
ROW_Y, BOX_H = 318, 196
X0, GAP = 62, 18
RIGHT = 196                      # reserved for the output column, measured: "A BOARD"
BOX_W = (W - X0 - RIGHT - 6 * GAP) / 7.0

STAGES = [
    ("1", "REFUSE", "CheckEscalation", OURS,
     ["21 phrases, 5 patterns",
      "runs FIRST, before",
      "any search or model call"], "red"),
    ("2", "RETRIEVE", "two knowledge bases", OURS,
     ["layout: the parent's",
      "own words",
      "evidence: a fixed query"], "red"),
    ("3", "COMPOSE", "the Composer", EXT,
     ["Bedrock Haiku 5.5",
      "or Azure OpenAI",
      "17 rules, no memory"], None),
    ("4", "VALIDATE", "parse before extract", OURS,
     ["eleven checks",
      "writes NOTHING on",
      "failure, names the check"], None),
    ("5", "SAVE", "as a Draft", OURS,
     ["transaction rollback",
      "a Draft is unreviewed",
      "by definition"], None),
    ("6", "REVIEW", "the Reviewer", EXT,
     ["fifteen questions",
      "CANNOT EDIT anything",
      "temperature 1"], "amber"),
    ("7", "APPROVE", "the parent", OURS,
     ["the only place in the",
      "app that sets InUse",
      "a human, every time"], "human"),
]

p = []


def add(s):
    p.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=20, fill=INK, weight="normal", anchor="start",
         spacing="0", style=""):
    add('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
        'font-weight="%s" text-anchor="%s" letter-spacing="%s"%s>%s</text>'
        % (x, y, FONT, size, fill, weight, anchor, spacing,
           (' font-style="%s"' % style) if style else "", esc(s)))


def box(x, y, w, h, stroke, fill, sw=2, r=10, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    add('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
        'stroke="%s" stroke-width="%g"%s/>' % (x, y, w, h, r, fill, stroke, sw, d))


def arrow(pts, color=GRAY, sw=2.5, dash=None):
    d = "M %g %g" % pts[0]
    if len(pts) == 2:
        d += " L %g %g" % pts[1]
    else:
        d += " Q %g %g %g %g" % (pts[1][0], pts[1][1], pts[2][0], pts[2][1])
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    add('<path d="%s" fill="none" stroke="%s" stroke-width="%g" '
        'marker-end="url(#ah-%s)"%s/>' % (d, color, sw, color.lstrip("#"), da))


def mark(cx, cy, kind):
    """A small disc on a stage that can stop the run. Colour carries the meaning,
    and the letter repeats it, because colour alone fails for a colour-blind judge
    and on a printed handout."""
    col, bg, lab = {"red":   (RED, RED_BG, "S"),
                    "amber": (AMBER, AMBER_BG, "C"),
                    "human": (OURS, OURS_BG, "H")}[kind]
    add('<circle cx="%g" cy="%g" r="17" fill="%s" stroke="%s" stroke-width="2.5"/>'
        % (cx, cy, bg, col))
    text(cx, cy + 6, lab, 17, col, "bold", "middle")


def build(slide=False):
    """slide=True enlarges the type and drops the key and footer."""
    global CAP, BODY
    CAP  = 17 if slide else 15
    BODY = 23 if slide else 21
    del p[:]
    add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d">' % (W, H, W, H))
    add("<defs>")
    for c in (GRAY, OURS, EXT, RED, AMBER):
        add('<marker id="ah-%s" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker>' % (c.lstrip("#"), c))
    add("</defs>")
    add('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))
    if slide:
        # Dropping the key and the footer leaves ~360px dead at the bottom against
        # 40 at the top. Nudge the whole drawing down so the two margins match.
        add('<g transform="translate(0,140)">')

    text(48, 78, "The agent loop", 40, INK, "bold")
    text(48, 112, "Autism Visual Supports  \u00b7  one parent's message, seven steps  \u00b7  "
                  "two of them stop it before the model is ever called, and a human ends it",
         19, GRAY)

    # the parent, left of the strip
    text(48, 212, "A PARENT WRITES THE HARD MOMENT", 18, INK, "bold", spacing="1.4")
    text(48, 240, "free text \u00b7 no form \u00b7 their own words", 17, GRAY)

    # --- the seven stages ---------------------------------------------------
    cxs = []
    for i, (num, title, sub, col, lines, m) in enumerate(STAGES):
        x = X0 + i * (BOX_W + GAP)
        fill = OURS_BG if col == OURS else EXT_BG
        box(x, ROW_Y, BOX_W, BOX_H, col, fill, sw=3, r=12)
        cx = x + BOX_W / 2
        cxs.append(cx)
        text(x + 14, ROW_Y + 30, num, 16, col, "bold")
        text(cx, ROW_Y + 56, title, BODY + 3, col, "bold", "middle", spacing="1.2")
        text(cx, ROW_Y + 82, sub, CAP + 1, INK, "normal", "middle", style="italic")
        add('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.5"/>'
            % (x + 24, ROW_Y + 98, x + BOX_W - 24, ROW_Y + 98,
               "#A7D7BD" if col == OURS else "#E6CBA4"))
        for j, ln in enumerate(lines):
            text(cx, ROW_Y + 124 + j * 23, ln, CAP, INK, "normal", "middle")
        if m:
            mark(x + BOX_W - 16, ROW_Y + 16, m)
        if i:
            arrow([(x - GAP - 2, ROW_Y + BOX_H / 2), (x - 3, ROW_Y + BOX_H / 2)], GRAY, 3)

    # in from the parent, out to the board
    arrow([(X0 - 14, 252), (X0 - 14, ROW_Y + BOX_H / 2 - 40),
           (X0 - 4, ROW_Y + BOX_H / 2)], GRAY, 3)
    out_x = X0 + 6 * (BOX_W + GAP) + BOX_W
    arrow([(out_x + 3, ROW_Y + BOX_H / 2), (out_x + 44, ROW_Y + BOX_H / 2)], OURS, 3)
    text(out_x + 52, ROW_Y + BOX_H / 2 - 6, "A BOARD", 21, OURS, "bold")
    text(out_x + 52, ROW_Y + BOX_H / 2 + 22, "printed, posted,", CAP, GRAY)
    text(out_x + 52, ROW_Y + BOX_H / 2 + 44, "and in use", CAP, GRAY)

    # --- the two ways out, drawn downward so they read as exits -------------
    exits = [
        (0, RED, RED_BG,
         "REFERRAL GUIDANCE, NOT A BOARD",
         "self-injury, aggression or escalation in the words a parent used."),
        (1, RED, RED_BG,
         "NO BOARD, AND IT SAYS SO",
         "either knowledge base returns nothing \u2014 rule 17, in code, not in a prompt."),
    ]
    ey = ROW_Y + BOX_H + 96
    BW, BH, BGAP = 606, 112, 30
    for idx, (si, col, bg, head, body) in enumerate(exits):
        cx = cxs[si]
        bx = X0 + idx * (BW + BGAP)
        box(bx, ey, BW, BH, col, bg, sw=2.5, r=10)
        arrow([(cx, ROW_Y + BOX_H + 4), (cx, ey - 4)], col, 3)
        text(bx + 20, ey + 34, head, 20, col, "bold")
        text(bx + 20, ey + 62, body, CAP + 1, INK)
        text(bx + 20, ey + 88,
             "Costs ZERO model tokens \u2014 it returns before the model is called."
             if si == 0 else
             "An ungrounded board looks exactly like a grounded one. So it is a check "
             "in the flow.", CAP, GRAY, style="italic")

    # the retry, back from VALIDATE to COMPOSE
    ry = ROW_Y - 44
    arrow([(cxs[3], ROW_Y - 4), (cxs[3] - (cxs[3] - cxs[2]) / 2, ry - 34),
           (cxs[2], ROW_Y - 4)], EXT, 2.5, dash="7 6")
    text((cxs[2] + cxs[3]) / 2, ry - 30,
         "one retry, with the validation error fed back", CAP + 1, EXT,
         "normal", "middle", style="italic")

    # the ordering sentence, under the strip and above the exits
    text(X0 + 2 + 2 * (BOX_W + GAP), ROW_Y + BOX_H + 54,
         "The save comes before the review \u2014 so a Reviewer failure", BODY - 2, INK, "bold")
    text(X0 + 2 + 2 * (BOX_W + GAP), ROW_Y + BOX_H + 82,
         "costs the verdict, not the board.", BODY - 2, INK, "bold")

    if slide:
        add("</g>")
        add("</svg>")
        return "\n".join(p)

    # --- key and footer -----------------------------------------------------
    ky = H - 190
    for i, (kind, lab) in enumerate((
            ("red",   "stops the run before the model is called, and has a safety "
                      "cost if it is wrong"),
            ("amber", "a clinical judgement \u2014 three of the fifteen questions came "
                      "from one parent, in one evening"),
            ("human", "a person decides \u2014 the agent cannot put a board in use"))):
        mark(X0 + 17, ky + i * 46, kind)
        text(X0 + 48, ky + 6 + i * 46, lab, 18, INK)

    text(X0 + 2, H - 36,
         "Five of the seven boxes are our own code. The other two are a model call and a "
         "knowledge-base search \u2014 and both are measured, not assumed.",
         17, GRAY, style="italic")
    add("</svg>")
    return "\n".join(p)


def win(path):
    d, rest = path[len("/mnt/"):].split("/", 1)
    return "%s:/%s" % (d.upper(), rest)


def render(stem, svg):
    sp = os.path.join(OUT, stem + ".svg")
    with open(sp, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("svg  %s" % sp)
    for suffix, factor in (("", 1), ("-2x", 2560.0 / W)):
        png = os.path.join(OUT, stem + suffix + ".png")
        if os.path.exists(png):
            os.remove(png)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars",
                        "--force-device-scale-factor=%g" % factor,
                        "--window-size=%d,%d" % (W, H),
                        "--screenshot=%s" % win(png), "file:///%s" % win(sp)],
                       check=False, capture_output=True, timeout=120)
        print("png  %s  %s" % (png, "ok" if os.path.exists(png) else "FAILED"))


os.makedirs(OUT, exist_ok=True)
render("agent-loop", build(slide=False))
render("agent-loop-slide", build(slide=True))
