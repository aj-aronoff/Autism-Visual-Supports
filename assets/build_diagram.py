#!/usr/bin/env python3
"""Technical diagrams for Autism Visual Supports.

Separate from build_art.py on purpose: that file draws the storybook artwork
(children, swings, sunflowers) on a warm illustrative palette. This one draws
architecture, on a four-colour diagram palette with a different type scale.
Keeping them apart means a change to the banner cannot disturb a diagram.

    python3 assets/build_diagram.py

Writes two variants, each 1920x1080 plus a 2560x1440 retina pass:
  trust-boundaries*        the full reference drawing, with the boundary key
  trust-boundaries-slide*  the deck version -- no key column, no footer,
                           larger captions, one callout instead of seven rows

Both come off the same geometry, so the slide cannot drift from the reference.
Rasterized by headless Chrome. The output directory must live under /mnt/c —
Windows Chrome cannot read Linux-only paths such as /tmp.
"""
import os
import subprocess

# Beside this file, so the generator writes into the repo and no hand copy is
# ever needed -- ASSETS.md caution 11.
OUT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

W, H = 1920, 1080

# Four colours, and no more. Ownership is the thing being encoded; every extra
# hue competes with it.
INK     = "#2D3748"   # text
GRAY    = "#718096"   # managed by someone else / inherited
GRAY_LT = "#CBD5E0"   # managed-zone rules
ZONE_BG = "#F7FAFC"   # managed-zone fill
OURS    = "#006B3C"   # ours to secure
OURS_BG = "#EBF7F0"
EXT     = "#A8600C"   # external dependency
EXT_BG  = "#FDF6EC"
PAPER   = "#FFFFFF"

FONT = "'Trebuchet MS','Segoe UI',Verdana,sans-serif"

# --- geometry ---------------------------------------------------------------
ZONE = (330, 200, 1090, 744)          # x, y, w, h  of the OutSystems-managed zone
EDGE = (560, 310, 620, 66)            # CDN / WAF / API Gateway
CODE = (540, 430, 660, 272)           # OUR CODE -- the hero
SVC_Y, SVC_H = 782, 100
SVC = [("Aurora Serverless v2", "encrypted at rest", 370),
       ("Secrets Manager",      "via ODC secrets",   625),
       ("Identity service",     "built in",          880),
       ("Agent Workbench",      "agents and tools", 1135)]
SVC_W = 245
PARENT = (60, 300, 240, 86)           # parent browser / tablet
PHONE  = (1480, 200, 380, 86)
# TWILIO removed 8 November 2026. The organisers confirmed Twilio is not used in this
# hackathon and A.J. confirmed no SMS at all, so the transport is gone from the design.
# The reward-confirmation LOOP survives -- it is now an on-screen check-off, which is why
# the parent's phone stays on the diagram and now talks to our own edge like any browser.
BEDROCK= (1480, 782, 380, 100)

p = []
def add(s): p.append(s)

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, s, size=20, fill=INK, weight="normal", anchor="start",
         spacing="0", style=""):
    add('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
        'font-weight="%s" text-anchor="%s" letter-spacing="%s"%s>%s</text>'
        % (x, y, FONT, size, fill, weight, anchor,
           spacing, (' font-style="%s"' % style) if style else "", esc(s)))

def box(x, y, w, h, stroke, fill, sw=2, r=10, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    add('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
        'stroke="%s" stroke-width="%g"%s/>' % (x, y, w, h, r, fill, stroke, sw, d))

# Set by build(). The slide variant enlarges captions and nothing else, so every
# box keeps the width it was laid out for.
SUB  = 16
BODY = 19


def chip(x, y, w, h, title, sub, stroke=GRAY, fill=PAPER, tcol=INK):
    box(x, y, w, h, stroke, fill, sw=2, r=8)
    if sub:
        text(x + w / 2, y + h / 2 - 2, title, 21, tcol, "bold", "middle")
        text(x + w / 2, y + h / 2 + 24, sub, SUB, GRAY, "normal", "middle")
    else:
        text(x + w / 2, y + h / 2 + 7, title, 21, tcol, "bold", "middle")

def arrow(pts, color=GRAY, sw=2.5, dash=None):
    d = "M %g %g" % pts[0]
    if len(pts) == 2:
        d += " L %g %g" % pts[1]
    else:                                      # quadratic through a control pt
        d += " Q %g %g %g %g" % (pts[1][0], pts[1][1], pts[2][0], pts[2][1])
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    add('<path d="%s" fill="none" stroke="%s" stroke-width="%g" '
        'marker-end="url(#ah-%s)"%s/>'
        % (d, color, sw, color.lstrip("#"), da))

def badge(cx, cy, label, kind):
    """kind: 'ours' filled, 'shared' half, 'inherited' hollow."""
    r = 20
    if kind == "ours":
        add('<circle cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" '
            'stroke-width="2.5"/>' % (cx, cy, r, OURS, PAPER))
        text(cx, cy + 7, label, 17, PAPER, "bold", "middle")
    elif kind == "shared":
        # Half-signalled by an OUTER arc, never by filling half the disc:
        # ink on a dark half is unreadable, which is how B5 and B7 first shipped.
        add('<circle cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" '
            'stroke-width="2.5"/>' % (cx, cy, r, PAPER, OURS))
        add('<path d="M %g %g A %g %g 0 0 0 %g %g" fill="none" stroke="%s" '
            'stroke-width="4.5" stroke-linecap="round"/>'
            % (cx, cy - r - 5, r + 5, r + 5, cx, cy + r + 5, OURS))
        text(cx, cy + 7, label, 17, OURS, "bold", "middle")
    else:
        add('<circle cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" '
            'stroke-width="2.5"/>' % (cx, cy, r, PAPER, GRAY))
        text(cx, cy + 7, label, 17, GRAY, "bold", "middle")

def build(slide=False):
    """Emit one variant. slide=False reproduces the reference exactly."""
    global SUB, BODY
    SUB  = 19 if slide else 16
    BODY = 21 if slide else 19
    del p[:]

    # --- document -----------------------------------------------------------
    add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d">' % (W, H, W, H))
    add("<defs>")
    for c in (GRAY, OURS, EXT):
        add('<marker id="ah-%s" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker>'
            % (c.lstrip("#"), c))
    add("</defs>")
    add('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))
    if slide:
        # Dropping the footer leaves 135px dead at the bottom against 40 at the
        # top. Nudge the whole drawing down so the two margins match.
        add('<g transform="translate(0,46)">')

    # title
    text(48, 74, "Trust boundaries", 40, INK, "bold")
    text(48, 106, "Autism Visual Supports on OutSystems Developer Cloud  \u00b7  who owns which control",
         19, GRAY)

    # Legend. On the slide it moves into the column the key vacates, where it has
    # room to be read from the back of a room.
    lx, ly, step, rr, tsz = (64, 556, 48, 13, 24) if slide else (1322, 60, 30, 9, 18)
    # Counts recomputed 8 Nov 2026 after Twilio came out: B2 and B3 ours, B4 and B5
    # shared, B1 inherited. It was 4/2/1 with the two Twilio hops in.
    for i, (kind, lab) in enumerate((("ours", "ours to secure \u2014 2"),
                                     ("shared", "shared \u2014 2"),
                                     ("inherited", "inherited \u2014 1"))):
        y = ly + i * step
        if kind == "ours":
            add('<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (lx, y, rr, OURS))
        elif kind == "shared":
            add('<circle cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" stroke-width="2"/>'
                % (lx, y, rr, PAPER, OURS))
            add('<path d="M %g %g A %g %g 0 0 0 %g %g" fill="none" stroke="%s" '
                'stroke-width="3" stroke-linecap="round"/>'
                % (lx, y - rr - 4, rr + 4, rr + 4, lx, y + rr + 4, OURS))
        else:
            add('<circle cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" stroke-width="2"/>'
                % (lx, y, rr, PAPER, GRAY))
        text(lx + rr + 11, y + tsz / 3, lab, tsz, INK if kind != "inherited" else GRAY)

    # the managed zone
    zx, zy, zw, zh = ZONE
    box(zx, zy, zw, zh, GRAY_LT, ZONE_BG, sw=3, r=16, dash="10 7")
    text(zx + 26, zy + 40, "OUTSYSTEMS-MANAGED", 20, GRAY, "bold", spacing="1.5")
    text(zx + 26, zy + 66, "AWS, in their accounts \u00b7 we configure none of it", 17, GRAY)

    # edge
    chip(EDGE[0], EDGE[1], EDGE[2], EDGE[3],
         "CDN  \u2192  WAF  \u2192  API Gateway", "TLS terminated here", GRAY, PAPER)

    # our code -- the hero
    cx, cy, cw, ch = CODE
    add('<rect x="%g" y="%g" width="%g" height="%g" rx="12" fill="%s" stroke="%s" '
        'stroke-width="4"/>' % (cx, cy, cw, ch, OURS_BG, OURS))
    text(cx + cw / 2, cy + 44, "OUR CODE", 28, OURS, "bold", "middle", spacing="2")
    text(cx + cw / 2, cy + 72, "the whole of our security responsibility",
         17, OURS, "normal", "middle", style="italic")
    add('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.5"/>'
        % (cx + 40, cy + 92, cx + cw - 40, cy + 92, "#A7D7BD"))
    for i, line in enumerate(("screens  \u00b7  server actions  \u00b7  validators",
                              "exposed REST  +  OnRequest / OnAuthentication",
                              "agent definitions  +  tool signatures",
                              "ten entities, every query scoped to the session")):
        text(cx + cw / 2, cy + 124 + i * 33, line, BODY, INK, "normal", "middle")

    # platform services
    for title, sub, x in SVC:
        is_agent = title == "Agent Workbench"
        chip(x, SVC_Y, SVC_W, SVC_H, title, sub,
             GRAY, PAPER, INK)
        if is_agent:
            text(x + SVC_W / 2, SVC_Y + SVC_H + 24, "availability unconfirmed",
                 SUB - 1, EXT, "normal", "middle", style="italic")

    # external actors
    chip(PARENT[0], PARENT[1], PARENT[2], PARENT[3], "Parent", "browser / tablet", INK, PAPER)
    chip(PHONE[0], PHONE[1], PHONE[2], PHONE[3], "Parent's phone",
         "the board \u00b7 hands full", INK, PAPER)
    chip(BEDROCK[0], BEDROCK[1], BEDROCK[2], BEDROCK[3], "Amazon Bedrock",
         "metered tokens \u00b7 no console for us", EXT, EXT_BG, EXT)

    # --- flows ------------------------------------------------------------------
    ey = EDGE[1] + EDGE[3] / 2
    arrow([(PARENT[0] + PARENT[2], ey), (EDGE[0] - 4, ey)], GRAY)
    text(392, ey - 14, "HTTPS", SUB, GRAY, "normal", "middle")

    # edge down into our code
    arrow([(cx + cw / 2, EDGE[1] + EDGE[3]), (cx + cw / 2, cy - 4)], GRAY)

    # B2  our code -> data
    arrow([(cx + 150, cy + ch), (cx + 150, SVC_Y - 40), (492, SVC_Y - 4)], OURS)
    # B4  our code -> agent workbench
    arrow([(cx + cw - 150, cy + ch), (cx + cw - 150, SVC_Y - 40),
           (1135 + SVC_W / 2, SVC_Y - 4)], OURS)
    # B5  agent workbench -> bedrock
    ay = SVC_Y + SVC_H / 2
    arrow([(1135 + SVC_W, ay), (BEDROCK[0] - 4, ay)], EXT)
    # phone -> the same edge every browser reaches. It crosses B1 like any other
    # client; the old inbound webhook and outbound SMS hops are gone with Twilio.
    arrow([(PHONE[0] - 4, PHONE[1] + PHONE[3] / 2), (1300, 243),
           (EDGE[0] + EDGE[2] / 2 + 60, EDGE[1] - 4)], GRAY)
    text(1300, 228, "HTTPS", SUB, GRAY, "normal", "middle")

    # --- boundary badges --------------------------------------------------------
    badge(zx, ey, "B1", "inherited")
    badge(548, 744, "B2", "ours")
    badge(1198, 744, "B3", "ours")
    badge(zx + zw, ay, "B4", "shared")
    badge(370 + SVC_W / 2, SVC_Y + SVC_H + 32, "B5", "shared")

    # --- the key, or the callout that replaces it ---------------------------
    if slide:
        # Seven rows of 19px text is a reference table, not a slide. The one
        # sentence a viewer needs is this one; the rest is narration.
        # Rewritten 8 Nov 2026: it used to read "the only unauthenticated path in is
        # B3", meaning Twilio's inbound webhook. With Twilio gone there is no
        # unauthenticated path at all, which is a stronger sentence than the one it
        # replaces -- and leaving the old one would have pointed at B3, which is now
        # "our code -> agent" and needs a logged-in parent like everything else.
        text(64, 452, "There is no unauthenticated", 30, INK, "bold")
        text(64, 490, "path in. None.", 30, INK, "bold")
        add("</g>")
        add("</svg>")
        return "\n".join(p)

    kx, ky = 60, 478
    text(kx, ky, "BOUNDARIES", 18, INK, "bold", spacing="1.5")
    add('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2"/>'
        % (kx, ky + 12, kx + 240, ky + 12, OURS))
    KEY = [("B1", "internet \u2192 edge", "inherited"),
           ("B2", "parent \u2192 their data", "ours"),
           ("B3", "our code \u2192 agent", "ours"),
           ("B4", "agent \u2192 Bedrock", "shared"),
           ("B5", "data at rest", "shared")]
    for i, (b, lab, kind) in enumerate(KEY):
        y = ky + 48 + i * 37
        col = OURS if kind == "ours" else (INK if kind == "shared" else GRAY)
        text(kx, y, b, 19, col, "bold")
        text(kx + 42, y, lab, 19, INK if kind != "inherited" else GRAY)

    text(kx, 800, "There is no unauthenticated", 17, INK, "bold")
    text(kx, 824, "path in. None.", 17, INK, "bold")
    text(kx, 856, "Every path needs a", 17, GRAY)
    text(kx, 878, "logged-in parent.", 17, GRAY)

    text(48, H - 28,
         "Two boundaries fully ours, two shared, one inherited.  "
         "A small enumerable surface beats a large one with a thick document in front of it.",
         17, GRAY, style="italic")

    add("</svg>")
    return "\n".join(p)



os.makedirs(OUT, exist_ok=True)


def win(path):
    d, rest = path[len("/mnt/"):].split("/", 1)
    return "%s:/%s" % (d.upper(), rest)


def render(stem, svg):
    sp = os.path.join(OUT, stem + ".svg")
    with open(sp, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("svg  %s" % sp)
    # --window-size is in CSS pixels and the scale factor multiplies it, so the
    # window stays at W,H and only the factor changes. Passing 2560,1440 *and*
    # a 1.333 factor is what produced a 3413x1920 "2x" file.
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


render("trust-boundaries", build(slide=False))
render("trust-boundaries-slide", build(slide=True))
