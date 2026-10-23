#!/usr/bin/env python3
"""Generate the Taikai cover / avatar / illustration SVGs for Autism Visual Supports.

Style rules taken from DivergentTravel + Calm Skies symbol library:
  - flat vector, single-weight solid shapes, no gradients on figures, no photo texture
  - every icon sits INSIDE its circle badge with consistent padding (v3.2 lost the badges)
  - never white-on-white; never pure black; never neon; yellow is fill-only, never text
  - green-on-blue is low contrast -> avoid it for figure-on-badge pairings
"""
import os, random

OUT = "/mnt/c/users/ajaro/claude/resume/hackathon-future/assets"
os.makedirs(OUT, exist_ok=True)

# ---- palette -------------------------------------------------------------
CLOUD_WHITE = "#F7FBFF"
SKY         = "#5BA4CF"
CLEAR_SKY   = "#2E7CB8"
HORIZON     = "#A8D4EF"
MEADOW      = "#6BBF8E"
SAGE        = "#B2DFC4"
SAND        = "#F5EFE0"
SLATE       = "#2D3748"
GRAY        = "#718096"
SUNFLOWER   = "#F9C74F"
HDS_YELLOW  = "#FDD835"
HDS_GREEN   = "#006B3C"
ROSE        = "#F28B82"
NAVY        = "#0B1E3D"
NAVY_MID    = "#123A66"
SKIN        = "#F0C49B"
SKIN_2      = "#C98B5E"
HAIR        = "#5A3E2B"
HAIR_2      = "#2F2A26"
WOOD        = "#C98B5E"

FONT = "'Trebuchet MS','Segoe UI',Verdana,sans-serif"


# ---- figures -------------------------------------------------------------
def child_brushing(skin=SKIN, hair=HAIR, shirt=SKY, pants=CLEAR_SKY):
    """Child brushing teeth, drawn in a 200x200 box, feet near y=196.

    Draw order matters: the raised arm and the brush go ON TOP of the head,
    or they vanish behind it (that is how the first pass lost the toothbrush).
    """
    return f'''
<g>
  <!-- legs -->
  <rect x="80"  y="150" width="16" height="44" rx="8" fill="{pants}"/>
  <rect x="104" y="150" width="16" height="44" rx="8" fill="{pants}"/>
  <rect x="74"  y="186" width="26" height="12" rx="6" fill="{SLATE}"/>
  <rect x="100" y="186" width="26" height="12" rx="6" fill="{SLATE}"/>
  <!-- torso -->
  <rect x="72" y="104" width="56" height="56" rx="22" fill="{shirt}"/>
  <!-- left arm resting -->
  <rect x="56" y="110" width="15" height="42" rx="7.5" fill="{shirt}"/>
  <circle cx="63.5" cy="153" r="8.5" fill="{skin}"/>
  <!-- head -->
  <circle cx="100" cy="72" r="33" fill="{skin}"/>
  <path d="M67 68 A33 33 0 0 1 133 68 Q118 50 100 50 Q82 50 67 68 Z" fill="{hair}"/>
  <circle cx="88"  cy="72" r="3.6" fill="{SLATE}"/>
  <circle cx="112" cy="72" r="3.6" fill="{SLATE}"/>
  <circle cx="76"  cy="84" r="5" fill="{ROSE}" opacity=".55"/>
  <circle cx="124" cy="84" r="5" fill="{ROSE}" opacity=".55"/>
  <!-- open mouth, so the brush has somewhere to go -->
  <path d="M89 84 Q100 98 111 84 Z" fill="{SLATE}"/>
  <path d="M91.5 85.5 Q100 90 108.5 85.5 Z" fill="{CLOUD_WHITE}"/>
  <!-- raised arm, bent at the elbow, drawn above the head -->
  <path d="M126 116 L157 118 L134 96" stroke="{shirt}" stroke-width="15" fill="none"
        stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="134" cy="96" r="9" fill="{skin}"/>
  <!-- toothbrush, bristles landing on the mouth -->
  <g transform="translate(134,96) rotate(-75)">
    <rect x="-5" y="4"   width="10" height="44" rx="5" fill="{HORIZON}"/>
    <rect x="-4" y="-7"  width="8"  height="13" fill="{HORIZON}"/>
    <rect x="-9" y="-25" width="18" height="19" rx="5" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="2.5"/>
    <circle cx="0" cy="-29" r="4.5" fill="{SAGE}"/>
  </g>
</g>'''


def sunflower(cx, cy, r):
    """Hidden Disabilities Sunflower mark: green sun on HDS yellow, per the symbol sheet."""
    petals = "".join(
        f'<ellipse cx="{cx}" cy="{cy - r*0.52:.1f}" rx="{r*0.14:.1f}" ry="{r*0.33:.1f}" '
        f'fill="{HDS_GREEN}" transform="rotate({i*36} {cx} {cy})"/>'
        for i in range(10))
    return (f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="{HDS_YELLOW}"/>{petals}'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.30:.1f}" fill="{HDS_GREEN}"/></g>')


def child_swinging(skin=SKIN, hair=HAIR, shirt=SKY, pants=CLEAR_SKY, ropes=True, ponytail=False, lw=1.0):
    """Smiling child on a swing, 200x200 box. Ropes run to the top edge.

    Defaults match child_brushing() exactly: a visual support only works if the
    child on the FIRST card is recognisably the same child on the THEN card.
    """
    tail = f'<path d="M131 36 Q146 44 142 60 Q136 48 128 46 Z" fill="{hair}"/>' if ponytail else ""
    rw = 5 * lw                      # ropes vanish below ~2px once the card shrinks
    sh_ = 13 + (lw - 1) * 5          # thicken the seat with them, but more gently
    rope = f'''
  <path d="M68 2 L66 116"  stroke="{WOOD}" stroke-width="{rw:.1f}" stroke-linecap="round" fill="none"/>
  <path d="M132 2 L134 116" stroke="{WOOD}" stroke-width="{rw:.1f}" stroke-linecap="round" fill="none"/>''' if ropes else ""
    return f'''
<g transform="rotate(-7 100 20)">
  {rope}
  <!-- seat -->
  <rect x="54" y="114" width="92" height="{sh_:.1f}" rx="6" fill="{WOOD}"/>
  <!-- legs swinging forward -->
  <g transform="rotate(-22 112 120)">
    <rect x="104" y="116" width="16" height="50" rx="8" fill="{pants}"/>
    <rect x="100" y="158" width="28" height="12" rx="6" fill="{SLATE}"/>
  </g>
  <g transform="rotate(-34 96 120)">
    <rect x="88" y="116" width="16" height="50" rx="8" fill="{pants}"/>
    <rect x="84" y="158" width="28" height="12" rx="6" fill="{SLATE}"/>
  </g>
  <!-- torso -->
  <rect x="73" y="70" width="54" height="52" rx="21" fill="{shirt}"/>
  <!-- arms up to the ropes -->
  <g transform="rotate(-26 80 78)">
    <rect x="62" y="44" width="14" height="42" rx="7" fill="{shirt}"/>
    <circle cx="69" cy="46" r="7.5" fill="{skin}"/>
  </g>
  <g transform="rotate(26 120 78)">
    <rect x="124" y="44" width="14" height="42" rx="7" fill="{shirt}"/>
    <circle cx="131" cy="46" r="7.5" fill="{skin}"/>
  </g>
  <!-- head -->
  <circle cx="100" cy="42" r="31" fill="{skin}"/>
  <path d="M69 40 A31 31 0 0 1 131 40 Q117 21 100 21 Q83 21 69 40 Z" fill="{hair}"/>
  {tail}
  <circle cx="89"  cy="44" r="3.4" fill="{SLATE}"/>
  <circle cx="111" cy="44" r="3.4" fill="{SLATE}"/>
  <path d="M89 55 Q100 66 111 55 Q100 60 89 55 Z" fill="{SLATE}"/>
  <circle cx="78"  cy="53" r="4.6" fill="{ROSE}" opacity=".55"/>
  <circle cx="122" cy="53" r="4.6" fill="{ROSE}" opacity=".55"/>
</g>'''


def storyteller(skin=SKIN, hair=HAIR, robe=CLEAR_SKY):
    """Avatar figure: a storyteller holding an open book, 200x200 box."""
    return f'''
<g>
  <!-- shoulders / robe -->
  <path d="M46 200 Q46 136 100 130 Q154 136 154 200 Z" fill="{robe}"/>
  <!-- open book held up -->
  <g transform="translate(0,6)">
    <path d="M44 162 Q72 150 98 162 L98 196 Q72 184 44 196 Z" fill="{CLOUD_WHITE}" stroke="{SLATE}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M102 162 Q128 150 156 162 L156 196 Q128 184 102 196 Z" fill="{CLOUD_WHITE}" stroke="{SLATE}" stroke-width="3" stroke-linejoin="round"/>
    <rect x="96" y="156" width="8" height="44" rx="3" fill="{SUNFLOWER}"/>
    <path d="M56 170 L86 176 M56 180 L80 185" stroke="{HORIZON}" stroke-width="4" stroke-linecap="round"/>
    <path d="M114 176 L144 170 M120 185 L144 180" stroke="{HORIZON}" stroke-width="4" stroke-linecap="round"/>
  </g>
  <!-- head -->
  <circle cx="100" cy="82" r="38" fill="{skin}"/>
  <path d="M62 78 A38 38 0 0 1 138 78 Q120 56 100 56 Q80 56 62 78 Z" fill="{hair}"/>
  <circle cx="86"  cy="84" r="4" fill="{SLATE}"/>
  <circle cx="114" cy="84" r="4" fill="{SLATE}"/>
  <path d="M87 98 Q100 109 113 98" stroke="{SLATE}" stroke-width="3.8" fill="none" stroke-linecap="round"/>
  <circle cx="72"  cy="94" r="5.4" fill="{ROSE}" opacity=".5"/>
  <circle cx="128" cy="94" r="5.4" fill="{ROSE}" opacity=".5"/>
</g>'''


# ---- ODC cloud -----------------------------------------------------------
def odc_cloud(seed=7, glow=SKY, dense=True, fill=NAVY_MID, fill_op=".85", sq=None):
    """Digital cloud: a cloud silhouette filled with a mosaic of small squares.

    `fill`/`sq` switch it to a light-background treatment; the dark default
    matches ODC-Cloud.png.
    """
    sq = sq or [HORIZON, SKY, CLOUD_WHITE, "#7FD7F5", SKY]
    random.seed(seed)
    # cloud outline in a 400x240 space, scaled by caller
    path = ("M60 200 A52 52 0 0 1 72 98 A66 66 0 0 1 196 70 "
            "A58 58 0 0 1 306 96 A54 54 0 0 1 330 200 Z")
    squares = []
    if dense:
        for _ in range(430):
            x = random.uniform(56, 332); y = random.uniform(66, 200)
            s = random.choice([3, 4, 4, 5, 6, 8])
            o = round(random.uniform(.18, .92), 2)
            c = random.choice(sq)
            squares.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s}" height="{s}" fill="{c}" opacity="{o}"/>')
    return f'''
<g>
  <defs>
    <clipPath id="cloudclip"><path d="{path}"/></clipPath>
    <filter id="cloudglow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="9" result="b"/><feMerge>
      <feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g clip-path="url(#cloudclip)">
    <path d="{path}" fill="{fill}" opacity="{fill_op}"/>
    {''.join(squares)}
  </g>
  <path d="{path}" fill="none" stroke="{glow}" stroke-width="4" filter="url(#cloudglow)" opacity=".95"/>
</g>'''


def data_rain(w, h, seed=3, n=16, color=SKY):
    """Thin vertical dotted lines, like the reference ODC image."""
    random.seed(seed)
    out = []
    for _ in range(n):
        x = random.uniform(0, w); top = random.uniform(0, h * .30); ln = random.uniform(h * .18, h * .55)
        out.append(f'<line x1="{x:.0f}" y1="{top:.0f}" x2="{x:.0f}" y2="{top+ln:.0f}" '
                   f'stroke="{color}" stroke-width="1.6" opacity="{random.uniform(.12,.4):.2f}"/>')
        out.append(f'<circle cx="{x:.0f}" cy="{top+ln:.0f}" r="3" fill="#7FD7F5" opacity="{random.uniform(.3,.8):.2f}"/>')
    return "<g>" + "".join(out) + "</g>"


# ---- building blocks -----------------------------------------------------
def badge(cx, cy, r, fill, inner, pad=0.46):
    """Circle badge with a figure scaled to sit inside it with consistent padding.
    The v3.2 symbol sheet lost these badges; keep them."""
    s = (r * 2 * (1 - pad * 0.0)) / 200.0 * 0.86
    return (f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<g transform="translate({cx - 100*s:.2f},{cy - 100*s:.2f}) scale({s:.4f})">{inner}</g></g>')


def card(x, y, w, h, label, inner, accent, bg=CLOUD_WHITE, fs=34):
    """A First/Then card: picture box above a 1-3 word label."""
    pic = h - fs - 34
    s = min(w - 28, pic - 18) / 200.0
    return f'''
<g>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{bg}" stroke="{accent}" stroke-width="6"/>
  <g transform="translate({x + w/2 - 100*s:.1f},{y + 14 + pic/2 - 100*s:.1f}) scale({s:.4f})">{inner}</g>
  <text x="{x + w/2}" y="{y + h - 20}" font-family="{FONT}" font-size="{fs}" font-weight="700"
        fill="{SLATE}" text-anchor="middle">{label}</text>
</g>'''


def first_then_board(x, y, w, bg=CLOUD_WHITE, show_header=True):
    """The product itself: FIRST -> THEN, brush teeth -> swing."""
    cw = (w - 3 * 22) / 2.0
    ch = cw * 1.16
    hdr = 54 if show_header else 10
    h = hdr + ch + 44
    arrow_y = y + hdr + ch / 2
    head = ""
    if show_header:
        head = (f'<text x="{x + 22 + cw/2}" y="{y + 38}" font-family="{FONT}" font-size="30" '
                f'font-weight="700" fill="{CLEAR_SKY}" text-anchor="middle" letter-spacing="3">FIRST</text>'
                f'<text x="{x + w - 22 - cw/2}" y="{y + 38}" font-family="{FONT}" font-size="30" '
                f'font-weight="700" fill="#A8600C" text-anchor="middle" letter-spacing="3">THEN</text>')
    return h, f'''
<g>
  <rect x="{x-16}" y="{y-16}" width="{w+32}" height="{h+32}" rx="26" fill="{bg}" stroke="{HORIZON}" stroke-width="5"/>
  {head}
  {card(x+22, y+hdr, cw, ch, "Brush teeth", child_brushing(), CLEAR_SKY)}
  {card(x+w-22-cw, y+hdr, cw, ch, "Swing", child_swinging(), SUNFLOWER)}
  <circle cx="{x + w/2}" cy="{arrow_y}" r="26" fill="{MEADOW}"/>
  <path d="M{x+w/2-10} {arrow_y-10} L{x+w/2+10} {arrow_y} L{x+w/2-10} {arrow_y+10} Z" fill="{CLOUD_WHITE}"/>
</g>'''


def svg(w, h, body, bg=CLOUD_WHITE):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def write(name, content):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


# =========================================================================
# 1. BACKGROUND — ODC cloud
# =========================================================================
W, H = 1920, 1080
cloud_s = 2.6
body = f'''
<defs>
  <radialGradient id="bgrad" cx="50%" cy="46%" r="72%">
    <stop offset="0%" stop-color="{NAVY_MID}"/><stop offset="100%" stop-color="{NAVY}"/>
  </radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bgrad)"/>
<g opacity=".30" fill="none" stroke="{SKY}" stroke-width="2">
  <circle cx="{W/2}" cy="{H/2}" r="300"/><circle cx="{W/2}" cy="{H/2}" r="420"/>
  <circle cx="{W/2}" cy="{H/2}" r="540"/><circle cx="{W/2}" cy="{H/2}" r="660"/>
</g>
{data_rain(W, H, n=22)}
<g transform="translate({W/2 - 195*cloud_s},{H/2 - 135*cloud_s}) scale({cloud_s})">{odc_cloud()}</g>
'''
write("background-odc.svg", svg(W, H, body, NAVY))

# =========================================================================
# 2. SWING CHILD — standalone illustration
# =========================================================================
body = f'''
<defs><radialGradient id="sg" cx="50%" cy="40%" r="70%">
  <stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="{SAGE}"/></radialGradient></defs>
<rect width="1000" height="1000" fill="url(#sg)"/>
<circle cx="800" cy="190" r="86" fill="{SUNFLOWER}" opacity=".85"/>
<g opacity=".5">
  <ellipse cx="210" cy="230" rx="104" ry="46" fill="{CLOUD_WHITE}"/>
  <ellipse cx="282" cy="212" rx="70" ry="38" fill="{CLOUD_WHITE}"/>
</g>
<rect x="110" y="120" width="780" height="20" rx="10" fill="{WOOD}"/>
<rect x="150" y="128" width="26" height="730" rx="13" fill="{WOOD}" opacity=".85" transform="rotate(10 163 128)"/>
<rect x="824" y="128" width="26" height="730" rx="13" fill="{WOOD}" opacity=".85" transform="rotate(-10 837 128)"/>
<ellipse cx="500" cy="898" rx="300" ry="34" fill="{MEADOW}" opacity=".35"/>
<rect x="0" y="880" width="1000" height="120" fill="{MEADOW}" opacity=".55"/>
<g transform="translate(260,150) scale(2.4)">{child_swinging(shirt=SKY)}</g>
'''
write("swing-child.svg", svg(1000, 1000, body, CLOUD_WHITE))

# =========================================================================
# 3. AVATAR — storyteller (square)
# =========================================================================
A = 512
body = f'''
<defs><clipPath id="rc"><circle cx="{A/2}" cy="{A/2}" r="{A/2}"/></clipPath></defs>
<g clip-path="url(#rc)">
  <rect width="{A}" height="{A}" fill="{SKY}"/>
  <circle cx="{A/2}" cy="{A/2}" r="208" fill="{CLEAR_SKY}" opacity=".45"/>
  <circle cx="{A/2}" cy="{A/2}" r="160" fill="{CLEAR_SKY}" opacity=".35"/>
  <g transform="translate(76,86) scale(1.80)">{storyteller(robe=HDS_GREEN)}</g>
</g>
<circle cx="{A/2}" cy="{A/2}" r="{A/2-10}" fill="none" stroke="{SUNFLOWER}" stroke-width="20"/>
'''
write("avatar-storyteller.svg", svg(A, A, body, SKY))

# =========================================================================
# 4-6. THREE COVER VARIANTS  (1600 x 900)
# =========================================================================
CW, CH = 1600, 900
TITLE = "Autism Visual Supports"
SUB = "First &#8594; Then boards that parents can print, post and trust"

# ---- Variant 1: Storybook (warm, parent-facing) ----
bh, board = first_then_board(830, 330, 700, bg=CLOUD_WHITE)
body = f'''
<rect width="{CW}" height="{CH}" fill="{SAND}"/>
<g opacity=".55"><ellipse cx="250" cy="150" rx="150" ry="62" fill="{CLOUD_WHITE}"/>
<ellipse cx="350" cy="128" rx="100" ry="50" fill="{CLOUD_WHITE}"/></g>
<rect x="0" y="770" width="{CW}" height="130" fill="{SAGE}" opacity=".7"/>
<!-- the book -->
<g transform="rotate(-4 400 470)">
  <rect x="150" y="196" width="520" height="560" rx="22" fill="{CLEAR_SKY}"/>
  <rect x="150" y="196" width="46"  height="560" rx="22" fill="{NAVY_MID}"/>
  <rect x="214" y="236" width="420" height="480" rx="14" fill="{CLOUD_WHITE}"/>
  <text x="424" y="300" font-family="{FONT}" font-size="34" font-weight="700" fill="{CLEAR_SKY}"
        text-anchor="middle" letter-spacing="2">MY FIRST &#8594; THEN</text>
  {card(252, 328, 160, 200, "Brush teeth", child_brushing(), CLEAR_SKY, fs=22)}
  {card(436, 328, 160, 200, "Swing", child_swinging(), SUNFLOWER, fs=22)}
  <circle cx="424" cy="428" r="22" fill="{MEADOW}"/>
  <path d="M415 418 L433 428 L415 438 Z" fill="{CLOUD_WHITE}"/>
  <text x="424" y="600" font-family="{FONT}" font-size="26" fill="{GRAY}" text-anchor="middle">a story for</text>
  <rect x="304" y="620" width="240" height="4" rx="2" fill="{HORIZON}"/>
  {sunflower(424, 676, 30)}
</g>
<text x="830" y="152" font-family="{FONT}" font-size="56" font-weight="700" fill="{SLATE}">Autism</text>
<text x="830" y="214" font-family="{FONT}" font-size="56" font-weight="700" fill="{SLATE}">Visual Supports</text>
<text x="830" y="264" font-family="{FONT}" font-size="26" fill="{GRAY}">Boards parents can print, post and trust</text>
<rect x="830" y="286" width="120" height="6" rx="3" fill="{SUNFLOWER}"/>
{board}
<text x="830" y="{330+bh+62}" font-family="{FONT}" font-size="21" font-weight="700" fill="{CLEAR_SKY}"
      letter-spacing="1">BUILT ON OUTSYSTEMS ODC &#183; BUILD FOR THE FUTURE 2026</text>
'''
write("cover-v1-storybook.svg", svg(CW, CH, body, SAND))

# ---- Variant 2: Board first (clean, product-forward) ----
bh2, board2 = first_then_board(560, 292, 840, bg=CLOUD_WHITE)
light_cloud = odc_cloud(fill=HORIZON, fill_op=".45", sq=[SKY, CLEAR_SKY, HORIZON, "#7FD7F5"], glow=CLEAR_SKY)
body = f'''
<rect width="{CW}" height="{CH}" fill="{CLOUD_WHITE}"/>
<g transform="translate(1090,-30) scale(1.35)" opacity=".55">{light_cloud}</g>
<rect x="0" y="0" width="22" height="{CH}" fill="{HDS_GREEN}"/>
<rect x="22" y="0" width="12" height="{CH}" fill="{HDS_YELLOW}"/>
<text x="92" y="150" font-family="{FONT}" font-size="70" font-weight="700" fill="{SLATE}">{TITLE}</text>
<text x="92" y="206" font-family="{FONT}" font-size="30" fill="{GRAY}">{SUB}</text>
<rect x="92" y="240" width="130" height="6" rx="3" fill="{SUNFLOWER}"/>
{board2}
<g transform="translate(150,392)">
  <circle cx="100" cy="100" r="100" fill="{SKY}"/>
  <g transform="translate(34,26) scale(0.66)">{storyteller(robe=HDS_GREEN)}</g>
</g>
{sunflower(322, 566, 38)}
<text x="92" y="790" font-family="{FONT}" font-size="24" font-weight="700" fill="{CLEAR_SKY}" letter-spacing="1">BUILT ON OUTSYSTEMS ODC</text>
<text x="92" y="828" font-family="{FONT}" font-size="22" fill="{GRAY}">Agentic AI &#183; Twilio &#183; Build for the Future 2026</text>
'''
write("cover-v2-board-first.svg", svg(CW, CH, body, CLOUD_WHITE))

# ---- Variant 3: ODC night (tech / hackathon-forward) ----
bh3, board3 = first_then_board(800, 318, 700, bg=CLOUD_WHITE)
body = f'''
<defs><radialGradient id="n3" cx="34%" cy="46%" r="78%">
  <stop offset="0%" stop-color="{NAVY_MID}"/><stop offset="100%" stop-color="{NAVY}"/></radialGradient></defs>
<rect width="{CW}" height="{CH}" fill="url(#n3)"/>
<g opacity=".26" fill="none" stroke="{SKY}" stroke-width="2">
  <circle cx="360" cy="330" r="250"/><circle cx="360" cy="330" r="350"/><circle cx="360" cy="330" r="450"/>
</g>
{data_rain(CW, CH, n=18)}
<g transform="translate(165,148) scale(1.0)">{odc_cloud()}</g>
<text x="92" y="130" font-family="{FONT}" font-size="64" font-weight="700" fill="{CLOUD_WHITE}">{TITLE}</text>
<text x="92" y="182" font-family="{FONT}" font-size="28" fill="{HORIZON}">{SUB}</text>
{board3}
{sunflower(1244, 184, 64)}
<text x="92" y="790" font-family="{FONT}" font-size="26" font-weight="700" fill="{SUNFLOWER}" letter-spacing="2">OUTSYSTEMS ODC &#183; AGENTIC AI &#183; TWILIO</text>
<text x="92" y="828" font-family="{FONT}" font-size="22" fill="{HORIZON}">Build for the Future Hackathon 2026</text>
'''
write("cover-v3-odc-night.svg", svg(CW, CH, body, NAVY))

print("done")


# =========================================================================
# 7-9. DECK ARTWORK
# =========================================================================
bhd, boardd = first_then_board(40, 40, 1120, bg=CLOUD_WHITE)
write("deck-board.svg", svg(1200, bhd + 112, boardd, "#FFFFFF"))


def bubble(x, y, w, h, text_lines, fill, fg, tail="left", fs=30):
    rows = "".join(f'<text x="{x+30}" y="{y+52+i*40}" font-family="{FONT}" font-size="{fs}" '
                   f'fill="{fg}">{t}</text>' for i, t in enumerate(text_lines))
    tp = (f'<path d="M{x+6} {y+h-26} L{x-14} {y+h} L{x+34} {y+h-4} Z" fill="{fill}"/>' if tail == "left"
          else f'<path d="M{x+w-6} {y+h-26} L{x+w+14} {y+h} L{x+w-34} {y+h-4} Z" fill="{fill}"/>')
    return f'<g>{tp}<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}"/>{rows}</g>'


PW, PH = 900, 1120
body = f'''
<rect width="{PW}" height="{PH}" fill="#FFFFFF"/>
<rect x="110" y="30" width="680" height="1060" rx="62" fill="{SLATE}"/>
<rect x="128" y="48" width="644" height="1024" rx="48" fill="{CLOUD_WHITE}"/>
<rect x="128" y="48" width="644" height="92" rx="48" fill="{CLEAR_SKY}"/>
<rect x="128" y="112" width="644" height="28" fill="{CLEAR_SKY}"/>
<text x="450" y="106" font-family="{FONT}" font-size="34" font-weight="700" fill="#FFFFFF" text-anchor="middle">Visual Supports</text>
<text x="168" y="206" font-family="{FONT}" font-size="24" fill="{GRAY}">Today 7:40 AM</text>
{bubble(160, 226, 470, 160, ["First shoes,", "then swing."], HORIZON, SLATE)}
<text x="168" y="446" font-family="{FONT}" font-size="24" fill="{GRAY}">8:05 AM</text>
{bubble(160, 466, 530, 200, ["Did the swing happen?", "Reply Y or N."], HORIZON, SLATE)}
{bubble(640, 706, 110, 92, ["Y"], MEADOW, "#FFFFFF")}
<g transform="translate(160,850)">
  <rect width="580" height="146" rx="20" fill="{SAGE}" opacity=".55"/>
  {sunflower(66, 73, 34)}
  <text x="128" y="62" font-family="{FONT}" font-size="28" font-weight="700" fill="{SLATE}">Reward delivered</text>
  <text x="128" y="104" font-family="{FONT}" font-size="26" fill="{SLATE}">9 mornings in a row</text>
</g>
'''
write("deck-sms.svg", svg(PW, PH, body, "#FFFFFF"))


def agent(cx, cy, r, title, sub, col, glyph):
    return f'''
<g>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>
  <text x="{cx}" y="{cy+16}" font-family="{FONT}" font-size="54" font-weight="700" fill="#FFFFFF" text-anchor="middle">{glyph}</text>
  <text x="{cx}" y="{cy+r+52}" font-family="{FONT}" font-size="36" font-weight="700" fill="{SLATE}" text-anchor="middle">{title}</text>
  <text x="{cx}" y="{cy+r+94}" font-family="{FONT}" font-size="26" fill="{GRAY}" text-anchor="middle">{sub}</text>
</g>'''


def flow_arrow(x1, x2, y):
    return (f'<g><line x1="{x1}" y1="{y}" x2="{x2-18}" y2="{y}" stroke="{HORIZON}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M{x2-22} {y-14} L{x2} {y} L{x2-22} {y+14} Z" fill="{HORIZON}"/></g>')


AW, AH = 1500, 620
body = f'''
<rect width="{AW}" height="{AH}" fill="#FFFFFF"/>
{agent(240, 190, 96, "Composer", "drafts the board", CLEAR_SKY, "1")}
{flow_arrow(350, 640, 190)}
{agent(750, 190, 96, "Reviewer", "sends it back", MEADOW, "2")}
{flow_arrow(860, 1150, 190)}
{agent(1260, 190, 96, "Illustrator", "reuses the card", SUNFLOWER, "3")}
<g transform="translate(240,470)">
  <rect width="1020" height="110" rx="20" fill="{SAGE}" opacity=".45"/>
  <text x="40" y="48" font-family="{FONT}" font-size="30" font-weight="700" fill="{HDS_GREEN}">Grounded knowledge source</text>
  <text x="40" y="88" font-family="{FONT}" font-size="26" fill="{SLATE}">TRIAD Visual Supports Toolkit &#183; National Standards Report, 11 evidence-based practices</text>
</g>
<path d="M750 300 L750 462" stroke="{HORIZON}" stroke-width="7" stroke-dasharray="14 12" stroke-linecap="round"/>
'''
write("deck-agents.svg", svg(AW, AH, body, "#FFFFFF"))
print("deck art done")


# =========================================================================
# 10-11. TRANSPARENT CIRCULAR BADGES (for the dark deck slides)
# =========================================================================
def svg_t(w, h, body):
    """No background rect, so Chrome can screenshot it with alpha."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{body}</svg>')


BD = 600
body = f'''
<defs>
  <clipPath id="sb"><circle cx="{BD/2}" cy="{BD/2}" r="{BD/2-14}"/></clipPath>
  <radialGradient id="sbg" cx="50%" cy="38%" r="70%">
    <stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="{SAGE}"/>
  </radialGradient>
</defs>
<g clip-path="url(#sb)">
  <rect width="{BD}" height="{BD}" fill="url(#sbg)"/>
  <circle cx="470" cy="128" r="54" fill="{SUNFLOWER}" opacity=".85"/>
  <rect x="0" y="516" width="{BD}" height="84" fill="{MEADOW}" opacity=".55"/>
  <g transform="translate(140,52) scale(1.6)">{child_swinging(shirt=SKY)}</g>
</g>
<circle cx="{BD/2}" cy="{BD/2}" r="{BD/2-14}" fill="none" stroke="{SUNFLOWER}" stroke-width="22"/>
'''
write("swing-badge.svg", svg_t(BD, BD, body))

body = f'''
<defs><clipPath id="ab"><circle cx="{BD/2}" cy="{BD/2}" r="{BD/2-14}"/></clipPath></defs>
<g clip-path="url(#ab)">
  <rect width="{BD}" height="{BD}" fill="{SKY}"/>
  <circle cx="{BD/2}" cy="{BD/2}" r="244" fill="{CLEAR_SKY}" opacity=".45"/>
  <circle cx="{BD/2}" cy="{BD/2}" r="188" fill="{CLEAR_SKY}" opacity=".35"/>
  <g transform="translate(89,101) scale(2.11)">{storyteller(robe=HDS_GREEN)}</g>
</g>
<circle cx="{BD/2}" cy="{BD/2}" r="{BD/2-14}" fill="none" stroke="{SUNFLOWER}" stroke-width="22"/>
'''
write("avatar-badge.svg", svg_t(BD, BD, body))
print("badges done")


# =========================================================================
# 12. COVER V4 — reading in the shade, lit by the ODC cloud
# =========================================================================
def child_reading(skin=SKIN, hair=HAIR, shirt=SKY, pants=CLEAR_SKY):
    """Same child as the other two, sitting cross-legged with an open book.
    200x200 box, seat on the ground at y=190."""
    return f'''
<g>
  <path d="M50 190 Q50 148 100 148 Q150 148 150 190 Z" fill="{pants}"/>
  <rect x="46" y="176" width="108" height="18" rx="9" fill="{pants}"/>
  <rect x="72" y="96" width="56" height="62" rx="22" fill="{shirt}"/>
  <path d="M76 114 L58 146" stroke="{shirt}" stroke-width="15" fill="none" stroke-linecap="round"/>
  <path d="M124 114 L142 146" stroke="{shirt}" stroke-width="15" fill="none" stroke-linecap="round"/>
  <circle cx="100" cy="64" r="32" fill="{skin}"/>
  <path d="M68 60 A32 32 0 0 1 132 60 Q118 42 100 42 Q82 42 68 60 Z" fill="{hair}"/>
  <path d="M84 70 Q89 77 94 70" stroke="{SLATE}" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <path d="M106 70 Q111 77 116 70" stroke="{SLATE}" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <path d="M92 84 Q100 91 108 84" stroke="{SLATE}" stroke-width="3" fill="none" stroke-linecap="round"/>
  <circle cx="76"  cy="78" r="4.6" fill="{ROSE}" opacity=".55"/>
  <circle cx="124" cy="78" r="4.6" fill="{ROSE}" opacity=".55"/>
  <g transform="translate(100,150)">
    <path d="M-46 -14 Q-24 -25 -2 -14 L-2 17 Q-24 6 -46 17 Z" fill="{CLOUD_WHITE}" stroke="{SLATE}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M2 -14 Q24 -25 46 -14 L46 17 Q24 6 2 17 Z" fill="{CLOUD_WHITE}" stroke="{SLATE}" stroke-width="3" stroke-linejoin="round"/>
    <rect x="-3" y="-18" width="6" height="37" rx="2" fill="{SUNFLOWER}"/>
    <path d="M-38 -3 L-12 3 M-38 7 L-18 12" stroke="{HORIZON}" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M12 3 L38 -3 M18 12 L38 7" stroke="{HORIZON}" stroke-width="3.5" stroke-linecap="round"/>
  </g>
  <circle cx="56"  cy="148" r="8.5" fill="{skin}"/>
  <circle cx="144" cy="148" r="8.5" fill="{skin}"/>
</g>'''


def tree(trunk=WOOD, leaf=HDS_GREEN, leaf2=MEADOW):
    """400x600 box, trunk base on the ground at y=600."""
    return f'''
<g>
  <path d="M174 600 Q182 470 166 366 L234 366 Q218 470 226 600 Z" fill="{trunk}"/>
  <path d="M194 430 L138 368" stroke="{trunk}" stroke-width="17" stroke-linecap="round"/>
  <path d="M208 408 L266 350" stroke="{trunk}" stroke-width="17" stroke-linecap="round"/>
  <ellipse cx="200" cy="252" rx="182" ry="142" fill="{leaf}"/>
  <ellipse cx="104" cy="304" rx="112" ry="92"  fill="{leaf}"/>
  <ellipse cx="296" cy="300" rx="114" ry="94"  fill="{leaf}"/>
  <ellipse cx="162" cy="194" rx="106" ry="84"  fill="{leaf2}" opacity=".50"/>
  <ellipse cx="262" cy="236" rx="88"  ry="70"  fill="{leaf2}" opacity=".40"/>
</g>'''


def sunflower_bloom(cx, cy, r):
    """A real sunflower head: yellow petals, green heart. Hidden Disabilities colours."""
    petals = "".join(
        f'<ellipse cx="{cx}" cy="{cy - r*0.54:.1f}" rx="{r*0.22:.1f}" ry="{r*0.50:.1f}" '
        f'fill="{HDS_YELLOW}" transform="rotate({i*30} {cx} {cy})"/>' for i in range(12))
    return (f'<g>{petals}<circle cx="{cx}" cy="{cy}" r="{r*0.36:.1f}" fill="{HDS_GREEN}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.20:.1f}" fill="#0E3F26"/></g>')


def sunflower_plant(x, ground, h=150, r=44):
    top = ground - h
    return f'''
<g>
  <path d="M{x} {ground} Q{x-12} {ground-h*0.5} {x} {top+8}" stroke="{HDS_GREEN}" stroke-width="9" fill="none" stroke-linecap="round"/>
  <ellipse cx="{x-28}" cy="{ground-h*0.40:.0f}" rx="28" ry="13" fill="{HDS_GREEN}" transform="rotate(-22 {x-28} {ground-h*0.40:.0f})"/>
  <ellipse cx="{x+27}" cy="{ground-h*0.60:.0f}" rx="26" ry="12" fill="{MEADOW}" transform="rotate(18 {x+27} {ground-h*0.60:.0f})"/>
  {sunflower_bloom(x, top, r)}
</g>'''


GROUND = 800
body = f'''
<defs>
  <radialGradient id="v4sky" cx="26%" cy="34%" r="88%">
    <stop offset="0%" stop-color="{NAVY_MID}"/><stop offset="100%" stop-color="{NAVY}"/>
  </radialGradient>
  <radialGradient id="v4glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{SUNFLOWER}" stop-opacity=".26"/>
    <stop offset="100%" stop-color="{SUNFLOWER}" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="{CW}" height="{CH}" fill="url(#v4sky)"/>
<g opacity=".22" fill="none" stroke="{SKY}" stroke-width="2">
  <circle cx="390" cy="450" r="250"/><circle cx="390" cy="450" r="360"/><circle cx="390" cy="450" r="480"/>
</g>
{data_rain(CW, CH, n=16)}
<g transform="translate(200,318) scale(0.95)">{odc_cloud()}</g>
<ellipse cx="640" cy="470" rx="880" ry="600" fill="url(#v4glow)"/>
<rect x="0" y="{GROUND}" width="{CW}" height="{CH-GROUND}" fill="#143A2A"/>
<ellipse cx="0" cy="{GROUND}" rx="0" ry="0" fill="none"/>
<ellipse cx="1150" cy="{GROUND+14}" rx="430" ry="56" fill="#0A2419" opacity=".75"/>
<g transform="translate(960,50) scale(1.25)">{tree()}</g>
{sunflower_plant(790, GROUND, 160, 46)}
<g transform="translate(880,{GROUND-190*1.35:.0f}) scale(1.35)">{child_reading()}</g>
<text x="90" y="152" font-family="{FONT}" font-size="60" font-weight="700" fill="{CLOUD_WHITE}">Autism</text>
<text x="90" y="222" font-family="{FONT}" font-size="60" font-weight="700" fill="{CLOUD_WHITE}">Visual Supports</text>
<text x="90" y="278" font-family="{FONT}" font-size="27" fill="{HORIZON}">Printable visual supports, made in two minutes</text>
<rect x="90" y="300" width="128" height="6" rx="3" fill="{SUNFLOWER}"/>
<text x="90" y="790" font-family="{FONT}" font-size="25" font-weight="700" fill="{SUNFLOWER}" letter-spacing="2">OUTSYSTEMS ODC &#183; AGENTIC AI &#183; TWILIO</text>
<text x="90" y="828" font-family="{FONT}" font-size="21" fill="{HORIZON}">Build for the Future Hackathon 2026</text>
'''
write("cover-v4-reading-tree.svg", svg(CW, CH, body, NAVY))
print("v4 done")


# =========================================================================
# 13. The same scene with no type on it, for use inside the deck
# =========================================================================
SW, SH, SG = 1400, 800, 712
body = f'''
<defs>
  <radialGradient id="s4sky" cx="28%" cy="36%" r="90%">
    <stop offset="0%" stop-color="{NAVY_MID}"/><stop offset="100%" stop-color="{NAVY}"/>
  </radialGradient>
  <radialGradient id="s4glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{SUNFLOWER}" stop-opacity=".26"/>
    <stop offset="100%" stop-color="{SUNFLOWER}" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="{SW}" height="{SH}" fill="url(#s4sky)"/>
<g opacity=".22" fill="none" stroke="{SKY}" stroke-width="2">
  <circle cx="330" cy="360" r="220"/><circle cx="330" cy="360" r="320"/><circle cx="330" cy="360" r="430"/>
</g>
{data_rain(SW, SH, n=13)}
<g transform="translate(135,245) scale(0.86)">{odc_cloud()}</g>
<ellipse cx="520" cy="400" rx="760" ry="520" fill="url(#s4glow)"/>
<rect x="0" y="{SG}" width="{SW}" height="{SH-SG}" fill="#143A2A"/>
<ellipse cx="950" cy="{SG+12}" rx="370" ry="48" fill="#0A2419" opacity=".75"/>
<g transform="translate(770,52) scale(1.1)">{tree()}</g>
{sunflower_plant(600, SG, 140, 40)}
<g transform="translate(700,{SG-190*1.2:.0f}) scale(1.2)">{child_reading()}</g>
'''
write("scene-reading-tree.svg", svg(SW, SH, body, NAVY))
print("scene done")


# =========================================================================
# 14-16. DARK COVERS — the board running on a tablet, in the child's hands
# =========================================================================
def board_screen(w, h, pad=9, fs=None):
    """The First->Then board sized to fit a tablet screen of w x h, on white."""
    # Every pad here is a fraction of the card, not a fixed number of pixels.
    # Fixed padding is what shrank the figures when the board moved onto a tablet:
    # it matched card() at 368px tall and swamped the card at 104px tall.
    cw = (w - 3 * pad) / 2.0
    hdr = h * 0.13
    ch = h - hdr - h * 0.07
    lab = fs or min(ch * 0.092, (cw * 0.86) / (11 * 0.66))
    hs = hdr * 0.58
    pic = ch - lab - ch * 0.092
    sc = min(cw - cw * 0.088, pic - ch * 0.049) / 200.0
    lw = max(1.0, min(2.5, 0.8 / sc))
    uid = abs(hash((w, h, pad))) % 99999

    def cell(cx0, inner, label, accent):
        return (f'<rect x="{cx0:.1f}" y="{hdr:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="{ch*0.08:.1f}" '
                f'fill="{CLOUD_WHITE}" stroke="{accent}" stroke-width="{max(2, ch*0.022):.1f}"/>'
                f'<g transform="translate({cx0 + cw/2 - 100*sc:.1f},{hdr + ch*0.049 + pic/2 - 100*sc:.1f}) scale({sc:.4f})">{inner}</g>'
                f'<text x="{cx0 + cw/2:.1f}" y="{hdr + ch - lab*0.58:.1f}" font-family="{FONT}" '
                f'font-size="{lab:.1f}" font-weight="700" fill="{SLATE}" text-anchor="middle">{label}</text>')

    ax, ay = w / 2.0, hdr + ch / 2.0
    ar = max(7, ch * 0.085)
    return f'''
<g>
  <rect width="{w:.1f}" height="{h:.1f}" fill="#FFFFFF"/>
  <text x="{pad + cw/2:.1f}" y="{hdr*0.80:.1f}" font-family="{FONT}" font-size="{hs:.1f}" font-weight="700"
        fill="{CLEAR_SKY}" text-anchor="middle" letter-spacing="1.5">FIRST</text>
  <text x="{w - pad - cw/2:.1f}" y="{hdr*0.80:.1f}" font-family="{FONT}" font-size="{hs:.1f}" font-weight="700"
        fill="#A8600C" text-anchor="middle" letter-spacing="1.5">THEN</text>
  {cell(pad, child_brushing(), "Brush teeth", CLEAR_SKY)}
  {cell(w - pad - cw, child_swinging(lw=lw), "Swing", SUNFLOWER)}
  <circle cx="{ax:.1f}" cy="{ay:.1f}" r="{ar:.1f}" fill="{MEADOW}"/>
  <path d="M{ax-ar*0.38:.1f} {ay-ar*0.38:.1f} L{ax+ar*0.4:.1f} {ay:.1f} L{ax-ar*0.38:.1f} {ay+ar*0.38:.1f} Z" fill="#FFFFFF"/>
  <rect width="{w:.1f}" height="{h:.1f}" fill="none" stroke="#E2E8EE" stroke-width="1"/>
</g>'''


def tablet(x, y, w, h, bezel=14):
    """iPad-ish slab: dark bezel, white screen carrying the board."""
    sw, sh = w - bezel * 2, h - bezel * 2
    uid = abs(hash((x, y, w, h))) % 99999
    return f'''
<g>
  <rect x="{x+5:.1f}" y="{y+9:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{bezel+6}" fill="#06101F" opacity=".5"/>
  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{bezel+6}" fill="{SLATE}"/>
  <rect x="{x+3:.1f}" y="{y+3:.1f}" width="{w-6:.1f}" height="{h-6:.1f}" rx="{bezel+3}" fill="none" stroke="#8795A6" stroke-width="2"/>
  <defs><clipPath id="scr{uid}"><rect width="{sw:.1f}" height="{sh:.1f}" rx="4"/></clipPath></defs>
  <g transform="translate({x+bezel:.1f},{y+bezel:.1f})">
    <g clip-path="url(#scr{uid})">{board_screen(sw, sh)}</g>
  </g>
</g>'''


def child_bust_tablet(skin=SKIN, hair=HAIR, shirt=SKY, sleeve=CLEAR_SKY, tw=200, th=150):
    """Child holding a tablet toward the viewer. 300x420 box.

    Built to match child_brushing(): a torso wider than the head, sleeves in a
    second tone so the arms read as arms instead of melting into the shirt, and
    the whole head clear of the frame.
    """
    tx, ty = 150 - tw / 2.0, 224
    hy = ty + th * 0.52
    return f'''
<g>
  <rect x="136" y="122" width="28" height="32" rx="12" fill="{skin}"/>
  <path d="M118 166 Q62 184 54 {hy-6:.0f}" stroke="{sleeve}" stroke-width="24" fill="none" stroke-linecap="round"/>
  <path d="M182 166 Q238 184 246 {hy-6:.0f}" stroke="{sleeve}" stroke-width="24" fill="none" stroke-linecap="round"/>
  <rect x="94" y="146" width="112" height="172" rx="46" fill="{shirt}"/>
  <circle cx="150" cy="92" r="45" fill="{skin}"/>
  <path d="M105 88 A45 45 0 0 1 195 88 Q174 61 150 61 Q126 61 105 88 Z" fill="{hair}"/>
  <circle cx="133" cy="94" r="5" fill="{SLATE}"/>
  <circle cx="167" cy="94" r="5" fill="{SLATE}"/>
  <path d="M136 112 Q150 124 164 112" stroke="{SLATE}" stroke-width="4.4" fill="none" stroke-linecap="round"/>
  <circle cx="115" cy="106" r="7" fill="{ROSE}" opacity=".55"/>
  <circle cx="185" cy="106" r="7" fill="{ROSE}" opacity=".55"/>
  {tablet(tx, ty, tw, th)}
  <circle cx="{tx-3:.0f}" cy="{hy:.0f}" r="16" fill="{skin}"/>
  <circle cx="{tx+tw+3:.0f}" cy="{hy:.0f}" r="16" fill="{skin}"/>
</g>'''


def child_seated_tablet(skin=SKIN, hair=HAIR, shirt=SKY, pants=CLEAR_SKY):
    """Cross-legged, slab resting on the lap. 200x200 box, seat on the ground at y=190."""
    tw, th = 112, 68
    tx, ty = 100 - tw / 2.0, 120
    hy = ty + th * 0.62
    return f'''
<g>
  <path d="M50 190 Q50 148 100 148 Q150 148 150 190 Z" fill="{pants}"/>
  <rect x="46" y="176" width="108" height="18" rx="9" fill="{pants}"/>
  <rect x="72" y="86" width="56" height="72" rx="22" fill="{shirt}"/>
  <path d="M76 106 L46 {hy:.0f}" stroke="{shirt}" stroke-width="15" fill="none" stroke-linecap="round"/>
  <path d="M124 106 L154 {hy:.0f}" stroke="{shirt}" stroke-width="15" fill="none" stroke-linecap="round"/>
  <circle cx="100" cy="58" r="32" fill="{skin}"/>
  <path d="M68 54 A32 32 0 0 1 132 54 Q118 36 100 36 Q82 36 68 54 Z" fill="{hair}"/>
  <path d="M84 64 Q89 71 94 64" stroke="{SLATE}" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <path d="M106 64 Q111 71 116 64" stroke="{SLATE}" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <path d="M92 78 Q100 85 108 78" stroke="{SLATE}" stroke-width="3" fill="none" stroke-linecap="round"/>
  <circle cx="76"  cy="72" r="4.6" fill="{ROSE}" opacity=".55"/>
  <circle cx="124" cy="72" r="4.6" fill="{ROSE}" opacity=".55"/>
  {tablet(tx, ty, tw, th, bezel=8)}
  <circle cx="{tx-2:.0f}" cy="{hy:.0f}" r="9" fill="{skin}"/>
  <circle cx="{tx+tw+2:.0f}" cy="{hy:.0f}" r="9" fill="{skin}"/>
</g>'''


def night(w, h, rcx, rcy, ctx, cty, cs=1.0, rain=15, gid="n"):
    return f'''
<defs><radialGradient id="{gid}sky" cx="30%" cy="30%" r="86%">
  <stop offset="0%" stop-color="{NAVY_MID}"/><stop offset="100%" stop-color="{NAVY}"/></radialGradient></defs>
<rect width="{w}" height="{h}" fill="url(#{gid}sky)"/>
<g opacity=".24" fill="none" stroke="{SKY}" stroke-width="2">
  <circle cx="{rcx}" cy="{rcy}" r="250"/><circle cx="{rcx}" cy="{rcy}" r="360"/>
  <circle cx="{rcx}" cy="{rcy}" r="480"/></g>
{data_rain(w, h, n=rain)}
<g transform="translate({ctx},{cty}) scale({cs})">{odc_cloud()}</g>'''


FOOT1 = f'<text x="92" y="792" font-family="{FONT}" font-size="25" font-weight="700" fill="{SUNFLOWER}" letter-spacing="2">OUTSYSTEMS ODC &#183; AGENTIC AI &#183; TWILIO</text>'
FOOT2 = f'<text x="92" y="830" font-family="{FONT}" font-size="21" fill="{HORIZON}">Build for the Future Hackathon 2026</text>'

# ---- V5: standing, device held out, text column on the left ----
body = f'''
{night(CW, CH, 300, 230, 40, 30, 0.80, 15, "v5")}
<text x="92" y="372" font-family="{FONT}" font-size="62" font-weight="700" fill="{CLOUD_WHITE}">Autism</text>
<text x="92" y="444" font-family="{FONT}" font-size="62" font-weight="700" fill="{CLOUD_WHITE}">Visual Supports</text>
<text x="92" y="500" font-family="{FONT}" font-size="27" fill="{HORIZON}">On the fridge, or in their hands</text>
<rect x="92" y="524" width="128" height="6" rx="3" fill="{SUNFLOWER}"/>
{sunflower_bloom(1452, 152, 50)}
<g transform="translate(877,55) scale(2.02)">{child_bust_tablet()}</g>
{FOOT1}{FOOT2}
'''
write("cover-v5-tablet-hands.svg", svg(CW, CH, body, NAVY))

# ---- V6: framed close, so the screen is the hero ----
body = f'''
{night(CW, CH, 290, 210, 36, 24, 0.74, 13, "v6")}
<text x="92" y="400" font-family="{FONT}" font-size="58" font-weight="700" fill="{CLOUD_WHITE}">Autism</text>
<text x="92" y="468" font-family="{FONT}" font-size="58" font-weight="700" fill="{CLOUD_WHITE}">Visual Supports</text>
<text x="92" y="522" font-family="{FONT}" font-size="26" fill="{HORIZON}">First &#8594; Then, on the screen they already use</text>
<rect x="92" y="546" width="128" height="6" rx="3" fill="{SUNFLOWER}"/>
<g transform="translate(786,-59) scale(2.43)">{child_bust_tablet()}</g>
{FOOT1}{FOOT2}
'''
write("cover-v6-tablet-closeup.svg", svg(CW, CH, body, NAVY))

# ---- V7: sitting on the floor with it, calmer ----
body = f'''
{night(CW, CH, 330, 250, 44, 34, 0.84, 15, "v7")}
<ellipse cx="1140" cy="814" rx="320" ry="44" fill="#06101F" opacity=".6"/>
<text x="92" y="384" font-family="{FONT}" font-size="62" font-weight="700" fill="{CLOUD_WHITE}">Autism</text>
<text x="92" y="456" font-family="{FONT}" font-size="62" font-weight="700" fill="{CLOUD_WHITE}">Visual Supports</text>
<text x="92" y="512" font-family="{FONT}" font-size="27" fill="{HORIZON}">Printable, or tappable. Same board.</text>
<rect x="92" y="536" width="128" height="6" rx="3" fill="{SUNFLOWER}"/>
{sunflower_plant(840, 812, 150, 42)}
<g transform="translate(930,252) scale(2.95)">{child_seated_tablet()}</g>
{FOOT1}{FOOT2}
'''
write("cover-v7-tablet-floor.svg", svg(CW, CH, body, NAVY))
print("tablet covers done")


# =========================================================================
# 17. TAIKAI COVER — 16:3 letterbox, 1360x255, three cloud sizes
# =========================================================================
BW, BH = 1360, 255


def boy_head(cx, cy, r, skin=SKIN, hair=HAIR, eyes=True):
    k = r / 45.0
    return f'''
<g>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{skin}"/>
  <path d="M{cx-r} {cy-4*k} A{r} {r} 0 0 1 {cx+r} {cy-4*k} Q{cx+24*k} {cy-31*k} {cx} {cy-31*k} Q{cx-24*k} {cy-31*k} {cx-r} {cy-4*k} Z" fill="{hair}"/>
  {f'<circle cx="{cx-17*k:.1f}" cy="{cy+2*k:.1f}" r="{5*k:.1f}" fill="{SLATE}"/>' if eyes else ''}
  {f'<circle cx="{cx+17*k:.1f}" cy="{cy+2*k:.1f}" r="{5*k:.1f}" fill="{SLATE}"/>' if eyes else ''}
  {f'<path d="M{cx-14*k:.1f} {cy+20*k:.1f} Q{cx} {cy+32*k:.1f} {cx+14*k:.1f} {cy+20*k:.1f}" stroke="{SLATE}" stroke-width="{4.4*k:.1f}" fill="none" stroke-linecap="round"/>' if eyes else ''}
  <circle cx="{cx-35*k:.1f}" cy="{cy+14*k:.1f}" r="{7*k:.1f}" fill="{ROSE}" opacity=".55"/>
  <circle cx="{cx+35*k:.1f}" cy="{cy+14*k:.1f}" r="{7*k:.1f}" fill="{ROSE}" opacity=".55"/>
</g>'''


def banner(name, cs, ctx, cty, rain=11):
    """1360x255, laid out for the TWO crops Taikai makes of one upload: the
    project page shows all 1360, the project-LIST card centre-crops to roughly
    the middle 490px. So the child and the board sit dead centre and carry the
    card alone; the title block and the cloud are wings the card may discard.
    The card also drops an avatar disc over roughly x 461-573, y 200-255, so
    nothing load-bearing goes there."""
    tx, ty, tw, th = 578, 86, 244, 158            # tablet centred on x=700
    hy = ty + th * 0.55
    hcx, hcy, hr = tx + tw / 2.0, 44, 33
    body = f'''
<defs><radialGradient id="b{name}sky" cx="50%" cy="34%" r="92%">
  <stop offset="0%" stop-color="{NAVY_MID}"/><stop offset="100%" stop-color="{NAVY}"/></radialGradient></defs>
<rect width="{BW}" height="{BH}" fill="url(#b{name}sky)"/>
<g opacity=".22" fill="none" stroke="{SKY}" stroke-width="2">
  <circle cx="230" cy="124" r="130"/><circle cx="230" cy="124" r="200"/><circle cx="230" cy="124" r="280"/></g>
{data_rain(BW, BH, n=rain)}
<g transform="translate({ctx},{cty}) scale({cs})">{odc_cloud()}</g>
<text x="56" y="78" font-family="{FONT}" font-size="40" font-weight="700" fill="{CLOUD_WHITE}">Autism</text>
<text x="56" y="122" font-family="{FONT}" font-size="40" font-weight="700" fill="{CLOUD_WHITE}">Visual Supports</text>
<rect x="58" y="140" width="92" height="5" rx="2.5" fill="{SUNFLOWER}"/>
<text x="58" y="177" font-family="{FONT}" font-size="19" fill="{HORIZON}">Print it, post it, trust it.</text>
<text x="58" y="209" font-family="{FONT}" font-size="14" font-weight="700" fill="{SUNFLOWER}" letter-spacing="1.2">OUTSYSTEMS ODC &#183; AGENTIC AI &#183; TWILIO</text>
{boy_head(hcx, hcy, hr)}
<rect x="{hcx-44:.0f}" y="{hcy+28:.0f}" width="88" height="34" rx="14" fill="{SKY}"/>
<path d="M{tx+56} {ty+th-6} Q{tx-26} {hy+40:.0f} {tx-12} {hy:.0f}" stroke="{CLEAR_SKY}" stroke-width="21" fill="none" stroke-linecap="round"/>
<path d="M{tx+tw-56} {ty+th-6} Q{tx+tw+26} {hy+40:.0f} {tx+tw+12} {hy:.0f}" stroke="{CLEAR_SKY}" stroke-width="21" fill="none" stroke-linecap="round"/>
{tablet(tx, ty, tw, th, bezel=14)}
<rect x="{tx-23:.0f}" y="{hy-24:.0f}" width="38" height="48" rx="17" fill="{SKIN}"/>
<rect x="{tx+tw-15:.0f}" y="{hy-24:.0f}" width="38" height="48" rx="17" fill="{SKIN}"/>
{sunflower_bloom(1300, 196, 26)}
'''
    write(name + ".svg", svg(BW, BH, body, NAVY))


banner("cover-banner-cloud-small",  0.34, 1049, 54)
banner("cover-banner-cloud-medium", 0.52, 1014, 30)
banner("cover-banner-cloud-large",  0.74,  971,  0)

# =========================================================================
# 18. TAIKAI AVATAR — 1:1, 300x300
# =========================================================================
AV = 300
body = f'''
<defs><clipPath id="av1"><circle cx="{AV/2}" cy="{AV/2}" r="{AV/2}"/></clipPath></defs>
<g clip-path="url(#av1)">
  <rect width="{AV}" height="{AV}" fill="{SKY}"/>
  <circle cx="{AV/2}" cy="{AV/2}" r="122" fill="{CLEAR_SKY}" opacity=".45"/>
  <circle cx="{AV/2}" cy="{AV/2}" r="94"  fill="{CLEAR_SKY}" opacity=".35"/>
  <g transform="translate(44,54) scale(1.04)">{storyteller(robe=HDS_GREEN)}</g>
</g>
<circle cx="{AV/2}" cy="{AV/2}" r="{AV/2-6}" fill="none" stroke="{SUNFLOWER}" stroke-width="12"/>
'''
write("avatar-300-storyteller.svg", svg(AV, AV, body, SKY))

body = f'''
<defs><clipPath id="av2"><circle cx="{AV/2}" cy="{AV/2}" r="{AV/2}"/></clipPath></defs>
<g clip-path="url(#av2)">
  <rect width="{AV}" height="{AV}" fill="{NAVY_MID}"/>
  <circle cx="{AV/2}" cy="{AV/2}" r="124" fill="{CLEAR_SKY}" opacity=".40"/>
  <circle cx="{AV/2}" cy="{AV/2}" r="96"  fill="{SKY}" opacity=".30"/>
  <rect x="86" y="214" width="128" height="120" rx="46" fill="{SKY}"/>
  {boy_head(150, 140, 72)}
</g>
<circle cx="{AV/2}" cy="{AV/2}" r="{AV/2-6}" fill="none" stroke="{SUNFLOWER}" stroke-width="12"/>
'''
write("avatar-300-child.svg", svg(AV, AV, body, NAVY_MID))
print("taikai assets done")
