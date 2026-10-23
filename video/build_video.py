#!/usr/bin/env python3
"""Purpose-made 1920x1080 frames for the concept video.

Deck slides carry far too much text to read while they are moving, so these are
built for motion: one idea per frame, type large enough to read at a glance, and
the same artwork the product itself draws.
"""
import os, sys

ASSETS = "/mnt/c/users/ajaro/claude/resume/hackathon-future/assets"
sys.path.insert(0, ASSETS)
import build_art as A  # noqa: E402  (regenerates the asset set on import; idempotent)

OUT = "/mnt/c/users/ajaro/claude/resume/hackathon-future/video/frames"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
F = A.FONT


def sky(gid, rcx=620, rcy=430, ctx=None, cty=None, cs=0.0, rain=16):
    cloud = ""
    if cs:
        cloud = f'<g transform="translate({ctx},{cty}) scale({cs})">{A.odc_cloud()}</g>'
    return f'''
<defs><radialGradient id="{gid}" cx="30%" cy="32%" r="92%">
  <stop offset="0%" stop-color="{A.NAVY_MID}"/><stop offset="100%" stop-color="{A.NAVY}"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="url(#{gid})"/>
<g opacity=".20" fill="none" stroke="{A.SKY}" stroke-width="2">
  <circle cx="{rcx}" cy="{rcy}" r="300"/><circle cx="{rcx}" cy="{rcy}" r="430"/>
  <circle cx="{rcx}" cy="{rcy}" r="570"/></g>
{A.data_rain(W, H, n=rain)}
{cloud}'''


def t(x, y, s, txt, fill=None, w=700, anchor="start", ls=0):
    return (f'<text x="{x}" y="{y}" font-family="{F}" font-size="{s}" font-weight="{w}" '
            f'fill="{fill or A.CLOUD_WHITE}" text-anchor="{anchor}" letter-spacing="{ls}">{txt}</text>')


def write(name, body, bg=None):
    A.write(name + ".svg", A.svg(W, H, body, bg or A.NAVY))


def mv(path, name):
    os.replace(os.path.join(ASSETS, name + ".svg"), os.path.join(OUT, name + ".svg"))


frames = []


def frame(name, body, bg=None):
    write(name, body, bg)
    mv(OUT, name)
    frames.append(name)


# 01 — open
bh, board = A.first_then_board(1120, 300, 700, bg=A.CLOUD_WHITE)
frame("f01-open", f'''
{sky("s1", 520, 420, 150, 300, 1.15, 18)}
{t(150, 470, 112, "Autism", w=700)}
{t(150, 600, 112, "Visual Supports", w=700)}
{t(150, 690, 44, "First &#8594; Then. Print it, post it, trust it.", A.HORIZON, 400)}
<rect x="150" y="730" width="200" height="8" rx="4" fill="{A.SUNFLOWER}"/>
{A.sunflower_bloom(1700, 190, 62)}
''')

# 02 — the scene
frame("f02-four-minutes", f'''
{sky("s2", 1400, 500)}
{t(150, 430, 200, "Four minutes", w=700)}
{t(150, 560, 48, "to get shoes on, grab the go-bag,", A.HORIZON, 400)}
{t(150, 630, 48, "and be in the car.", A.HORIZON, 400)}
{t(150, 760, 40, "&#8220;We have to go now&#8221; does not work.", A.SKY, 400)}
{t(150, 826, 40, "Saying it louder works less.", A.SKY, 400)}
''')

# 03 — what does work
frame("f03-what-works", f'''
{sky("s3", 500, 400)}
{t(960, 230, 64, "What works is a picture.", A.HORIZON, 400, "middle")}
{board.replace('x="1104"', 'x="1104"')}
''')

# 04 — the cost
frame("f04-forty-minutes", f'''
{sky("s4", 1500, 300)}
{t(150, 400, 54, "Find the pictures. Cut them to size.", A.HORIZON, 400)}
{t(150, 474, 54, "Three words a label. Laminate. Velcro.", A.HORIZON, 400)}
{t(150, 690, 190, "Forty minutes", A.SUNFLOWER, 700)}
{t(150, 790, 46, "and the morning you needed it was this morning.", A.SKY, 400)}
''')

# 05 — the quote
frame("f05-trust", f'''
{sky("s5", 960, 540, 1430, 120, 0.9, 12)}
{t(960, 360, 58, "&#8220;Otherwise, your child may not trust", A.CLOUD_WHITE, 400, "middle")}
{t(960, 450, 58, "the board the next time you use it.&#8221;", A.CLOUD_WHITE, 400, "middle")}
{t(960, 560, 30, "VANDERBILT TRIAD &#183; AUTISM SPEAKS ATN", A.HORIZON, 700, "middle", 3)}
<rect x="430" y="660" width="1060" height="4" rx="2" fill="{A.SUNFLOWER}" opacity=".7"/>
{t(960, 790, 54, "A board the child has stopped trusting", A.SUNFLOWER, 700, "middle")}
{t(960, 862, 54, "is worse than no board.", A.SUNFLOWER, 700, "middle")}
''')

# 06 — the ask
frame("f06-three-questions", f'''
{sky("s6", 1450, 540, 120, 150, 0.8, 14)}
{t(960, 300, 150, "Three questions.", A.CLOUD_WHITE, 700, "middle")}
{t(960, 470, 52, "Which routine.", A.HORIZON, 400, "middle")}
{t(960, 560, 52, "What is hard about it.", A.HORIZON, 400, "middle")}
{t(960, 650, 52, "What your child actually wants afterwards.", A.HORIZON, 400, "middle")}
{t(960, 830, 60, "Under two minutes.", A.SUNFLOWER, 700, "middle")}
''')

# 07 — the output
def chip(x, y, w, h, head, sub, col):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{A.CLOUD_WHITE}" '
            f'stroke="{col}" stroke-width="7"/>'
            f'{t(x + w/2, y + 86, 46, head, A.SLATE, 700, "middle")}'
            f'{t(x + w/2, y + 148, 30, sub, "#4C5C57", 400, "middle")}')


frame("f07-three-things", f'''
{sky("s7", 960, 300)}
{t(960, 230, 90, "Three things back.", A.CLOUD_WHITE, 700, "middle")}
{chip(150, 400, 520, 200, "The cards", "three words, printable", A.CLEAR_SKY)}
{chip(700, 400, 520, 200, "The script", "the words to say out loud", A.MEADOW)}
{chip(1250, 400, 520, 200, "The plan", "and what to do if it fails", A.SUNFLOWER)}
{t(960, 760, 44, "Most tools stop at the picture.", A.HORIZON, 400, "middle")}
{t(960, 826, 44, "The words are what parents fumble.", A.HORIZON, 400, "middle")}
''')

# 08 — the loop
frame("f08-loop", f'''
{sky("s8", 1500, 500)}
{t(130, 300, 72, "At the moment it matters,", A.CLOUD_WHITE, 700)}
{t(130, 390, 72, "they are holding shoes.", A.CLOUD_WHITE, 700)}
{t(130, 490, 46, "Not a tablet.", A.SUNFLOWER, 400)}
<g transform="translate(1190,120) scale(0.75)">
  <rect x="0" y="0" width="900" height="1120" rx="0" fill="none"/>
</g>
<g transform="translate(1230,90) scale(0.80)">
  <rect x="110" y="30" width="680" height="1060" rx="62" fill="{A.SLATE}"/>
  <rect x="128" y="48" width="644" height="1024" rx="48" fill="{A.CLOUD_WHITE}"/>
  <rect x="128" y="48" width="644" height="92" rx="48" fill="{A.CLEAR_SKY}"/>
  <rect x="128" y="112" width="644" height="28" fill="{A.CLEAR_SKY}"/>
  {t(450, 106, 34, "Visual Supports", "#FFFFFF", 700, "middle")}
  <rect x="160" y="226" width="470" height="150" rx="22" fill="{A.HORIZON}"/>
  {t(190, 288, 30, "First shoes,", A.SLATE, 400)}
  {t(190, 328, 30, "then swing.", A.SLATE, 400)}
  <rect x="160" y="456" width="530" height="190" rx="22" fill="{A.HORIZON}"/>
  {t(190, 518, 30, "Did the swing happen?", A.SLATE, 400)}
  {t(190, 558, 30, "Reply Y or N.", A.SLATE, 400)}
  <rect x="640" y="696" width="110" height="92" rx="22" fill="{A.MEADOW}"/>
  {t(695, 758, 34, "Y", "#FFFFFF", 700, "middle")}
</g>
{t(130, 700, 44, "Twilio sends the script when it is due,", A.HORIZON, 400)}
{t(130, 766, 44, "then asks the one question that decides", A.HORIZON, 400)}
{t(130, 832, 44, "whether the board keeps working.", A.HORIZON, 400)}
''')

# 09 — what gets measured
frame("f09-promises", f'''
{sky("s9", 500, 500, 1380, 140, 1.0, 12)}
{t(150, 420, 112, "Promises kept.", A.CLOUD_WHITE, 700)}
{t(150, 560, 112, "Not boards made.", A.SUNFLOWER, 700)}
{t(150, 680, 44, "The home screen tracks the only number", A.HORIZON, 400)}
{t(150, 744, 44, "the method actually depends on.", A.HORIZON, 400)}
''')

# 10 — how
frame("f10-agents", f'''
{sky("s10", 960, 900)}
{t(960, 190, 76, "Three agents. Grounded, not invented.", A.CLOUD_WHITE, 700, "middle")}
<g transform="translate(210,290) scale(1.0)">
  <rect width="1500" height="620" rx="30" fill="{A.CLOUD_WHITE}"/>
  <g transform="translate(0,-20)">{A.agent(240, 190, 96, "Composer", "drafts the board", A.CLEAR_SKY, "1")}</g>
  <g transform="translate(0,-20)">{A.flow_arrow(350, 640, 190)}</g>
  <g transform="translate(0,-20)">{A.agent(750, 190, 96, "Reviewer", "sends it back", A.MEADOW, "2")}</g>
  <g transform="translate(0,-20)">{A.flow_arrow(860, 1150, 190)}</g>
  <g transform="translate(0,-20)">{A.agent(1260, 190, 96, "Illustrator", "reuses the card", A.SUNFLOWER, "3")}</g>
  <g transform="translate(240,440)">
    <rect width="1020" height="110" rx="20" fill="{A.SAGE}" opacity=".45"/>
    {t(40, 48, 30, "Grounded knowledge source", A.HDS_GREEN, 700)}
    {t(40, 88, 26, "TRIAD Visual Supports Toolkit &#183; National Standards Report", A.SLATE, 400)}
  </g>
</g>
{t(960, 1000, 38, "OUTSYSTEMS ODC &#183; AGENTIC AI &#183; TWILIO", A.SUNFLOWER, 700, "middle", 3)}
''')

# 11 — why
frame("f11-why", f'''
{sky("s11", 1500, 400, 110, 120, 0.85, 12)}
{t(150, 400, 76, "My daughter is autistic.", A.CLOUD_WHITE, 700)}
{t(150, 500, 76, "My wife is the first test user.", A.CLOUD_WHITE, 700)}
{t(150, 630, 46, "I have been making these boards by hand for years,", A.HORIZON, 400)}
{t(150, 696, 46, "and I know exactly which forty minutes", A.HORIZON, 400)}
{t(150, 762, 46, "this gives back.", A.HORIZON, 400)}
<g transform="translate(1420,560) scale(0.62)">{A.child_bust_tablet()}</g>
''')

# 12 — end card
frame("f12-end", f'''
{sky("s12", 960, 540, 760, 180, 1.3, 16)}
{t(960, 560, 104, "Autism Visual Supports", A.CLOUD_WHITE, 700, "middle")}
{t(960, 650, 44, "First &#8594; Then. Print it, post it, trust it.", A.HORIZON, 400, "middle")}
<rect x="810" y="700" width="300" height="7" rx="3.5" fill="{A.SUNFLOWER}"/>
{t(960, 810, 36, "github.com/aj-aronoff/Autism-Visual-Supports", A.SKY, 400, "middle")}
{t(960, 900, 32, "A.J. ARONOFF &#183; BUILD FOR THE FUTURE 2026", A.SUNFLOWER, 700, "middle", 3)}
''')

print("\n".join(frames))
print(f"{len(frames)} frames -> {OUT}")
