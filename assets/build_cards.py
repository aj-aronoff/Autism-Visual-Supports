#!/usr/bin/env python3
"""Starter card library for Autism Visual Supports.

The third generator. build_art.py draws submission artwork, build_diagram.py draws
technical diagrams, this one draws the forty routine cards the Illustrator agent
reuses instead of generating. Keep them apart — see ASSETS.md caution 11.

Every card is one object or one action on Cloud White, inside a Horizon Blue badge,
at the figure-to-card ratio ASSETS.md fixes at 0.766. No text inside the picture:
the label is drawn by the application, so the same card serves a pre-verbal child
and a reader.

Outputs
  cards/<name>.svg      40 cards, 512x512
  cards/MANIFEST.csv    loader for the CardLibrary entity
  cards-contact.svg     one sheet, for checking legibility at card size
"""
import csv
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
SHEET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards-contact.svg")

# ---- palette (ASSETS.md) -------------------------------------------------
CLOUD_WHITE = "#F7FBFF"
HORIZON     = "#A8D4EF"
SKY         = "#5BA4CF"
CLEAR_SKY   = "#2E7CB8"
MEADOW      = "#6BBF8E"
SAGE        = "#B2DFC4"
SAND        = "#F5EFE0"
SLATE       = "#2D3748"
GRAY        = "#718096"
SUNFLOWER   = "#F9C74F"   # fill only, never text
ROSE        = "#F28B82"
WOOD        = "#C98B5E"
SKIN        = "#F0C49B"
HAIR        = "#5A3E2B"
FONT = "'Trebuchet MS','Segoe UI',Verdana,sans-serif"

CARD = 512
BADGE_R = 232
ICON_BOX = 200            # every icon draws inside 0..200
ICON_SPAN = 392           # 0.766 * 512, the ratio ASSETS.md fixes
SCALE = ICON_SPAN / ICON_BOX
OFFSET = (CARD - ICON_SPAN) / 2


# ---- shared parts --------------------------------------------------------
def palm(cx, cy, s=1.0, col=SKIN, edge=SLATE):
    """An open hand, fingers up. Used by WAIT and STOP, the two cards that
    recur on nearly every board."""
    g = []
    g.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="%g"/>'
             % (cx - 34 * s, cy - 18 * s, 68 * s, 62 * s, 16 * s, col, edge, 4 * s))
    for i, fx in enumerate((-24, -8, 8, 24)):
        h = (44, 54, 50, 38)[i]
        g.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="%g"/>'
                 % (cx + (fx - 6) * s, cy - (18 + h) * s, 13 * s, (h + 14) * s, 6.5 * s, col, edge, 4 * s))
    g.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="%g" '
             'transform="rotate(-38 %g %g)"/>'
             % (cx - 52 * s, cy - 6 * s, 13 * s, 42 * s, 6.5 * s, col, edge, 4 * s, cx - 46 * s, cy + 15 * s))
    return "".join(g)


def figure(cx, cy, s=1.0, shirt=SKY, skin=SKIN, hair=HAIR):
    """A small child, for the cards that need a person rather than an object."""
    return ('<circle cx="%g" cy="%g" r="%g" fill="%s"/>'
            '<path d="M%g %g a%g %g 0 0 1 %g 0 z" fill="%s"/>'
            '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s"/>'
            % (cx, cy - 34 * s, 20 * s, skin,
               cx - 21 * s, cy - 36 * s, 21 * s, 21 * s, 42 * s, hair,
               cx - 19 * s, cy - 12 * s, 38 * s, 52 * s, 13 * s, shirt))


def drops(cx, cy, s=1.0, col=SKY):
    return "".join('<path d="M%g %g q%g %g 0 %g q%g %g 0 %g z" fill="%s" opacity=".85"/>'
                   % (cx + dx * s, cy + dy * s, 7 * s, 9 * s, 16 * s, -7 * s, -9 * s, -16 * s, col)
                   for dx, dy in ((-18, 0), (0, 10), (18, 2)))


# ---- the forty icons -----------------------------------------------------
# Each returns SVG inside 0..200. One object or one action, nothing else.

def i_toothbrush():
    return (f'<rect x="38" y="118" width="108" height="20" rx="10" fill="{CLEAR_SKY}" '
            f'transform="rotate(-28 92 128)"/>'
            f'<rect x="124" y="60" width="38" height="24" rx="6" fill="{SKY}" '
            f'transform="rotate(-28 143 72)"/>'
            + "".join(f'<rect x="{126+i*7}" y="44" width="5" height="20" rx="2.5" fill="{HORIZON}" '
                      f'transform="rotate(-28 {128+i*7} 54)"/>' for i in range(5))
            + f'<path d="M58 150 q14 -10 28 0" fill="none" stroke="{SUNFLOWER}" stroke-width="9" stroke-linecap="round"/>')


def i_handwash():
    return (palm(74, 112, 0.78) + palm(132, 112, 0.78)
            + drops(100, 38, 1.0)
            + f'<path d="M44 162 h112" stroke="{SKY}" stroke-width="10" stroke-linecap="round"/>')


def i_towel():
    # Straight sides on a rail read as a bin. Stripes and a folded hem say towel.
    return (f'<rect x="36" y="42" width="128" height="13" rx="6" fill="{GRAY}"/>'
            f'<path d="M58 48 h84 v92 q0 16 -16 16 H74 q-16 0 -16 -16 z" fill="{SAGE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<rect x="58" y="62" width="84" height="9" fill="{CLOUD_WHITE}" opacity=".9"/>'
            f'<rect x="58" y="112" width="84" height="9" fill="{CLOUD_WHITE}" opacity=".9"/>'
            f'<rect x="58" y="126" width="84" height="5" fill="{CLOUD_WHITE}" opacity=".7"/>')

def i_bath():
    return (f'<path d="M34 96 h132 v38 q0 26 -26 26 H60 q-26 0 -26 -26 z" fill="{CLOUD_WHITE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<path d="M44 110 h112 q0 22 -16 22 H60 q-16 0 -16 -22 z" fill="{HORIZON}"/>'
            f'<path d="M150 96 v-34 q0 -16 -18 -16 h-18" fill="none" stroke="{GRAY}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="62" cy="80" r="11" fill="{CLOUD_WHITE}" stroke="{SKY}" stroke-width="4"/>'
            f'<circle cx="88" cy="66" r="8" fill="{CLOUD_WHITE}" stroke="{SKY}" stroke-width="4"/>')


def i_toilet():
    return (f'<rect x="56" y="40" width="88" height="46" rx="8" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<rect x="122" y="50" width="14" height="10" rx="5" fill="{GRAY}"/>'
            f'<path d="M58 86 h84 v26 q0 30 -30 30 H88 q-30 0 -30 -30 z" fill="{CLOUD_WHITE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<ellipse cx="100" cy="104" rx="30" ry="14" fill="{HORIZON}"/>'
            f'<rect x="84" y="142" width="32" height="20" rx="5" fill="{GRAY}"/>')


def i_hairbrush():
    return (f'<ellipse cx="100" cy="80" rx="46" ry="38" fill="{SKY}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            + "".join(f'<circle cx="{76+ (i%4)*16}" cy="{66 + (i//4)*18}" r="4" fill="{CLOUD_WHITE}"/>'
                      for i in range(8))
            + f'<rect x="88" y="112" width="24" height="56" rx="12" fill="{CLEAR_SKY}"/>')


def i_tissue():
    return (f'<rect x="44" y="92" width="112" height="66" rx="10" fill="{SKY}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<rect x="72" y="92" width="56" height="12" rx="6" fill="{CLOUD_WHITE}"/>'
            f'<path d="M78 96 q22 -56 44 0 q-22 -22 -44 0 z" fill="{CLOUD_WHITE}" stroke="{HORIZON}" stroke-width="4"/>')


def i_soap():
    return (f'<rect x="48" y="104" width="104" height="52" rx="22" fill="{SAGE}" stroke="{MEADOW}" stroke-width="6"/>'
            f'<circle cx="78" cy="68" r="17" fill="none" stroke="{SKY}" stroke-width="5"/>'
            f'<circle cx="112" cy="50" r="12" fill="none" stroke="{SKY}" stroke-width="5"/>'
            f'<circle cx="132" cy="76" r="8" fill="none" stroke="{SKY}" stroke-width="5"/>')


def _shoe(x, y, s=1.0, col=CLEAR_SKY):
    return (f'<path d="M{x} {y} q0 -30 26 -30 q10 0 16 10 l14 20 q18 4 18 18 q0 10 -12 10 H{x+10} q-10 0 -10 -14 z" '
            f'fill="{col}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M{x-2} {y+12} h78" stroke="{CLOUD_WHITE}" stroke-width="6"/>')


def i_shoes():
    return _shoe(30, 112) + _shoe(96, 142, col=SKY)


def i_socks():
    return (f'<path d="M62 44 h34 v56 q0 14 -14 22 l-16 10 q-14 8 -22 -6 q-8 -14 6 -22 l12 -8 z" '
            f'fill="{SAGE}" stroke="{MEADOW}" stroke-width="5"/>'
            f'<path d="M62 60 h34" stroke="{MEADOW}" stroke-width="5"/>'
            f'<path d="M112 70 h34 v56 q0 14 -14 22 l-16 10 q-14 8 -22 -6 q-8 -14 6 -22 l12 -8 z" '
            f'fill="{HORIZON}" stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<path d="M112 86 h34" stroke="{CLEAR_SKY}" stroke-width="5"/>')


def i_coat():
    return (f'<path d="M70 48 h60 l34 20 -14 32 -10 -6 v70 H60 v-70 l-10 6 -14 -32 z" '
            f'fill="{SKY}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<path d="M100 48 v116" stroke="{CLOUD_WHITE}" stroke-width="6"/>'
            f'<path d="M70 48 l30 22 30 -22" fill="{CLEAR_SKY}"/>'
            + "".join(f'<circle cx="100" cy="{92+i*22}" r="5" fill="{SUNFLOWER}"/>' for i in range(3)))


def i_hat():
    return (f'<path d="M52 118 a48 56 0 0 1 96 0 z" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="40" y="114" width="120" height="26" rx="13" fill="{SAND}" stroke="{SLATE}" stroke-width="5"/>'
            f'<circle cx="100" cy="58" r="12" fill="{SAND}" stroke="{SLATE}" stroke-width="5"/>')


def i_shirt():
    return (f'<path d="M72 54 h56 l32 18 -16 28 -12 -6 v62 H68 v-62 l-12 6 -16 -28 z" '
            f'fill="{SKY}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<path d="M72 54 q28 22 56 0" fill="none" stroke="{CLEAR_SKY}" stroke-width="6"/>')


def i_backpack():
    return (f'<path d="M66 56 q34 -22 68 0 v86 q0 14 -14 14 H80 q-14 0 -14 -14 z" '
            f'fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M66 100 h68 v30 q0 10 -10 10 H76 q-10 0 -10 -10 z" fill="{SKY}"/>'
            f'<rect x="88" y="108" width="24" height="12" rx="6" fill="{SUNFLOWER}"/>'
            f'<path d="M78 58 q-18 26 -4 50 M122 58 q18 26 4 50" fill="none" stroke="{SLATE}" '
            f'stroke-width="7" stroke-linecap="round"/>')


def i_cup():
    return (f'<path d="M62 56 h76 l-10 100 q-2 12 -14 12 H86 q-12 0 -14 -12 z" '
            f'fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<path d="M68 96 h64 l-7 60 q-1 6 -8 6 H83 q-7 0 -8 -6 z" fill="{HORIZON}"/>')


def i_bowl():
    return (f'<path d="M38 100 h124 q0 46 -40 56 H78 q-40 -10 -40 -56 z" fill="{CLOUD_WHITE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<path d="M50 104 h100 q-4 32 -34 40 H84 q-30 -8 -34 -40 z" fill="{SAND}"/>'
            f'<rect x="118" y="38" width="14" height="62" rx="7" fill="{GRAY}" transform="rotate(16 125 69)"/>'
            f'<ellipse cx="140" cy="44" rx="16" ry="11" fill="{GRAY}" transform="rotate(16 140 44)"/>')


def i_plate():
    # An ellipse plate with concentric rings reads as a clock face at card size.
    # Oval rim, filling off-centre, and the fork clearly outside the plate.
    return (f'<ellipse cx="116" cy="104" rx="58" ry="50" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<ellipse cx="116" cy="104" rx="38" ry="31" fill="{SAND}"/>'
            f'<path d="M96 100 q20 -14 40 0 q-20 14 -40 0 z" fill="{MEADOW}" opacity=".8"/>'
            f'<rect x="30" y="56" width="13" height="94" rx="6" fill="{GRAY}"/>'
            + "".join(f'<rect x="{24+i*9}" y="40" width="6" height="26" rx="3" fill="{GRAY}"/>' for i in range(3)))

def i_apple():
    return (f'<path d="M100 62 q34 -12 44 22 q10 32 -14 62 q-16 20 -30 20 q-14 0 -30 -20 '
            f'q-24 -30 -14 -62 q10 -34 44 -22 z" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M100 62 v-18" stroke="{WOOD}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M102 50 q24 -16 34 2 q-24 12 -34 -2 z" fill="{MEADOW}"/>')


def i_sandwich():
    # Two triangles read as a mountain. A stack reads as a sandwich.
    return (f'<path d="M34 96 q66 -52 132 0 v10 H34 z" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M34 106 q16 14 33 0 q16 14 33 0 q16 14 33 0 q16 14 33 0 v12 H34 z" fill="{MEADOW}"/>'
            f'<rect x="34" y="118" width="132" height="16" fill="{ROSE}"/>'
            f'<rect x="34" y="134" width="132" height="26" rx="8" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>')

def i_banana():
    return (f'<path d="M46 56 q6 76 70 92 q34 8 42 -14 q-10 10 -34 2 q-54 -18 -60 -82 z" '
            f'fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M46 56 q-8 -14 8 -14 q10 0 10 14" fill="{WOOD}" stroke="{SLATE}" stroke-width="4"/>')


def i_car():
    return (f'<path d="M26 128 l12 -34 q4 -12 18 -12 h88 q14 0 18 12 l12 34 v18 q0 8 -8 8 H34 q-8 0 -8 -8 z" '
            f'fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M56 94 l6 -20 h76 l6 20 z" fill="{HORIZON}"/>'
            f'<path d="M100 74 v20" stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<circle cx="58" cy="152" r="17" fill="{SLATE}"/><circle cx="58" cy="152" r="7" fill="{CLOUD_WHITE}"/>'
            f'<circle cx="142" cy="152" r="17" fill="{SLATE}"/><circle cx="142" cy="152" r="7" fill="{CLOUD_WHITE}"/>')


def i_door():
    return (f'<rect x="54" y="30" width="92" height="130" rx="6" fill="{WOOD}" stroke="{SLATE}" stroke-width="6"/>'
            f'<rect x="68" y="46" width="64" height="44" rx="4" fill="{HORIZON}"/>'
            f'<circle cx="130" cy="112" r="8" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="3"/>'
            f'<rect x="40" y="160" width="120" height="14" rx="7" fill="{SAGE}"/>')


def i_bus():
    return (f'<rect x="26" y="52" width="148" height="96" rx="14" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="5"/>'
            + "".join(f'<rect x="{38+i*34}" y="64" width="26" height="28" rx="4" fill="{HORIZON}"/>' for i in range(4))
            + f'<rect x="38" y="106" width="124" height="16" rx="6" fill="{CLOUD_WHITE}" opacity=".7"/>'
            f'<circle cx="60" cy="152" r="16" fill="{SLATE}"/><circle cx="60" cy="152" r="6" fill="{CLOUD_WHITE}"/>'
            f'<circle cx="140" cy="152" r="16" fill="{SLATE}"/><circle cx="140" cy="152" r="6" fill="{CLOUD_WHITE}"/>')


def i_carseat():
    return (f'<path d="M58 44 q46 -12 84 10 v60 q0 12 -12 12 H70 q-12 0 -12 -12 z" '
            f'fill="{SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M54 126 h92 q10 0 10 12 v12 q0 10 -10 10 H64 q-10 0 -10 -10 z" '
            f'fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M78 52 l22 74 22 -74" fill="none" stroke="{SUNFLOWER}" stroke-width="9"/>'
            f'<rect x="88" y="118" width="24" height="18" rx="5" fill="{SLATE}"/>')


def i_gobag():
    return (f'<path d="M34 86 h132 q10 0 10 12 v48 q0 12 -12 12 H46 q-12 0 -12 -12 v-48 q0 -12 10 -12 z" '
            f'fill="{MEADOW}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M74 86 q0 -26 26 -26 q26 0 26 26" fill="none" stroke="{SLATE}" stroke-width="8" stroke-linecap="round"/>'
            f'<rect x="34" y="110" width="142" height="14" fill="{SAGE}"/>'
            f'<rect x="86" y="104" width="28" height="26" rx="5" fill="{SAND}" stroke="{SLATE}" stroke-width="4"/>')


def i_swing():
    return (f'<rect x="28" y="34" width="144" height="13" rx="6" fill="{WOOD}"/>'
            f'<path d="M64 46 L72 128 M136 46 L128 128" stroke="{SLATE}" stroke-width="7" stroke-linecap="round"/>'
            f'<rect x="60" y="126" width="80" height="18" rx="7" fill="{WOOD}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M22 166 h156" stroke="{MEADOW}" stroke-width="12" stroke-linecap="round"/>')


def i_slide():
    return (f'<path d="M38 162 L38 56 M66 162 L66 56" stroke="{SLATE}" stroke-width="8" stroke-linecap="round"/>'
            + "".join(f'<path d="M38 {72+i*22} h28" stroke="{SLATE}" stroke-width="7" stroke-linecap="round"/>'
                      for i in range(4))
            + f'<path d="M66 54 q84 24 96 108 q-18 6 -22 -6 q-16 -72 -74 -82 z" fill="{SKY}" '
              f'stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<path d="M22 166 h156" stroke="{MEADOW}" stroke-width="12" stroke-linecap="round"/>')


def i_bubbles():
    return (f'<circle cx="82" cy="70" r="26" fill="none" stroke="{SKY}" stroke-width="7"/>'
            f'<circle cx="134" cy="48" r="17" fill="none" stroke="{SKY}" stroke-width="6"/>'
            f'<circle cx="138" cy="98" r="12" fill="none" stroke="{SKY}" stroke-width="6"/>'
            f'<circle cx="74" cy="118" r="9" fill="none" stroke="{SKY}" stroke-width="5"/>'
            f'<ellipse cx="60" cy="132" rx="20" ry="12" fill="none" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<path d="M52 142 l-22 26" stroke="{CLEAR_SKY}" stroke-width="10" stroke-linecap="round"/>')


def i_ball():
    return (f'<circle cx="100" cy="104" r="58" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M42 104 q58 -34 116 0" fill="none" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M42 104 q58 34 116 0" fill="none" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M100 46 v116" stroke="{SLATE}" stroke-width="5"/>')


def i_tablet():
    return (f'<rect x="50" y="32" width="100" height="136" rx="12" fill="{SLATE}"/>'
            f'<rect x="60" y="44" width="80" height="104" rx="4" fill="{HORIZON}"/>'
            f'<circle cx="100" cy="158" r="6" fill="{GRAY}"/>'
            f'<rect x="72" y="60" width="56" height="34" rx="4" fill="{CLOUD_WHITE}" opacity=".8"/>'
            f'<rect x="72" y="102" width="56" height="10" rx="5" fill="{CLOUD_WHITE}" opacity=".6"/>'
            f'<rect x="72" y="120" width="36" height="10" rx="5" fill="{CLOUD_WHITE}" opacity=".6"/>')


def i_book():
    return (f'<path d="M100 58 q-32 -18 -62 -10 v96 q30 -8 62 10 z" fill="{CLOUD_WHITE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<path d="M100 58 q32 -18 62 -10 v96 q-30 -8 -62 10 z" fill="{CLOUD_WHITE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<path d="M100 58 v96" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            + "".join(f'<path d="M{54} {76+i*18} q22 -6 36 2 M{110} {78+i*18} q22 -8 36 -2" '
                      f'stroke="{HORIZON}" stroke-width="5" fill="none"/>' for i in range(3)))


def i_music():
    return (f'<path d="M78 40 l62 -12 v22 l-62 12 z" fill="{CLEAR_SKY}"/>'
            f'<rect x="72" y="46" width="9" height="86" fill="{CLEAR_SKY}"/>'
            f'<rect x="131" y="34" width="9" height="86" fill="{CLEAR_SKY}"/>'
            f'<ellipse cx="58" cy="136" rx="22" ry="16" fill="{SKY}" transform="rotate(-18 58 136)"/>'
            f'<ellipse cx="117" cy="124" rx="22" ry="16" fill="{SKY}" transform="rotate(-18 117 124)"/>')


def i_blocks():
    return (f'<rect x="40" y="110" width="54" height="54" rx="6" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="104" y="110" width="54" height="54" rx="6" fill="{SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="72" y="52" width="54" height="54" rx="6" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="5"/>')


def i_wait():
    # Hand plus hourglass plus clock is three objects on one card. One hand,
    # one clock. WAIT appears on nearly every board, so it has to read instantly.
    return (palm(96, 122, 1.04)
            + f'<circle cx="140" cy="52" r="28" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="7"/>'
              f'<path d="M140 34 v18 h14" fill="none" stroke="{CLEAR_SKY}" stroke-width="7" '
              f'stroke-linecap="round" stroke-linejoin="round"/>')

def i_stop():
    return (f'<path d="M72 26 h56 l46 46 v56 l-46 46 H72 l-46 -46 V72 z" fill="none" '
            f'stroke="{ROSE}" stroke-width="9"/>'
            + palm(100, 112, 0.92))


def i_alldone():
    return (f'<circle cx="100" cy="100" r="62" fill="{MEADOW}"/>'
            f'<path d="M66 102 l24 26 46 -56" fill="none" stroke="{CLOUD_WHITE}" stroke-width="15" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def i_oops():
    return (f'<rect x="38" y="46" width="124" height="118" rx="10" fill="{CLOUD_WHITE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<rect x="38" y="46" width="124" height="26" rx="10" fill="{CLEAR_SKY}"/>'
            f'<rect x="62" y="34" width="12" height="24" rx="6" fill="{GRAY}"/>'
            f'<rect x="126" y="34" width="12" height="24" rx="6" fill="{GRAY}"/>'
            f'<rect x="76" y="90" width="48" height="48" rx="4" fill="{SAND}" stroke="{GRAY}" stroke-width="3"/>'
            f'<path d="M70 84 l60 60 M130 84 l-60 60" stroke="{ROSE}" stroke-width="11" stroke-linecap="round"/>')


def i_desk():
    return (f'<rect x="28" y="88" width="144" height="14" rx="6" fill="{WOOD}" stroke="{SLATE}" stroke-width="4"/>'
            f'<rect x="40" y="102" width="12" height="62" rx="5" fill="{WOOD}"/>'
            f'<rect x="148" y="102" width="12" height="62" rx="5" fill="{WOOD}"/>'
            f'<rect x="104" y="46" width="12" height="46" rx="5" fill="{CLEAR_SKY}"/>'
            f'<rect x="104" y="46" width="48" height="12" rx="6" fill="{CLEAR_SKY}"/>'
            f'<rect x="110" y="102" width="10" height="62" rx="4" fill="{CLEAR_SKY}"/>')


def i_pencil():
    # Drawn upright and rotated as one group, so the tip stays attached to the body.
    return (f'<g transform="rotate(32 100 100)">'
            f'<rect x="83" y="32" width="34" height="20" rx="5" fill="{ROSE}" stroke="{SLATE}" stroke-width="4"/>'
            f'<rect x="83" y="52" width="34" height="11" fill="{GRAY}"/>'
            f'<rect x="83" y="63" width="34" height="68" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M83 131 L100 168 L117 131 Z" fill="{SAND}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M93 153 L100 168 L107 153 Z" fill="{SLATE}"/>'
            f'</g>')

def i_lineup():
    return (figure(52, 112, 0.92, shirt=SKY) + figure(100, 112, 0.92, shirt=MEADOW)
            + figure(148, 112, 0.92, shirt=ROSE)
            + f'<path d="M26 170 h148" stroke="{HORIZON}" stroke-width="10" stroke-linecap="round"/>')


# ---- the catalogue -------------------------------------------------------
# name, label (what the app prints), alt text, category, suggested role
CARDS = [
    ("toothbrush", "Brush teeth",  "A toothbrush with a line of toothpaste",      "Self-care",   "First"),
    ("handwash",   "Wash hands",   "Two hands under falling water",               "Self-care",   "First"),
    ("towel",      "Dry hands",    "A towel hanging on a rail",                   "Self-care",   "Step"),
    ("bath",       "Bath",         "A bath tub with water and a tap",             "Self-care",   "First"),
    ("toilet",     "Toilet",       "A toilet with a cistern",                     "Self-care",   "Step"),
    ("hairbrush",  "Brush hair",   "A paddle hairbrush",                          "Self-care",   "Step"),
    ("tissue",     "Tissue",       "A box of tissues with one pulled up",          "Self-care",   "Step"),
    ("soap",       "Soap",         "A bar of soap with bubbles",                  "Self-care",   "Step"),
    ("shoes",      "Shoes",        "A pair of sneakers",                          "Dressing",    "First"),
    ("socks",      "Socks",        "Two socks",                                   "Dressing",    "Step"),
    ("coat",       "Coat on",      "A zipped coat",                               "Dressing",    "Step"),
    ("hat",        "Hat",          "A sun hat",                                   "Dressing",    "Step"),
    ("shirt",      "Get dressed",  "A t-shirt",                                   "Dressing",    "Step"),
    ("backpack",   "Pack bag",     "A school backpack",                           "Dressing",    "Step"),
    ("cup",        "Drink",        "A cup of water",                              "Food",        "Then"),
    ("bowl",       "Eat breakfast","A bowl with a spoon",                         "Food",        "First"),
    ("plate",      "Eat dinner",   "A dinner plate with a fork",                  "Food",        "First"),
    ("apple",      "Apple",        "A red apple with a leaf",                     "Food",        "Then"),
    ("sandwich",   "Sandwich",     "A sandwich cut in half",                      "Food",        "Then"),
    ("banana",     "Banana",       "A banana",                                    "Food",        "Then"),
    ("car",        "Car",          "A car seen from the side",                    "Transitions", "Then"),
    ("door",       "Front door",   "A front door with a doormat",                 "Transitions", "Step"),
    ("bus",        "Bus",          "A school bus",                                "Transitions", "Step"),
    ("carseat",    "Car seat",     "A child's car seat with straps",              "Transitions", "Step"),
    ("gobag",      "Go-bag",       "A packed duffel bag",                         "Transitions", "Step"),
    ("swing",      "Swing",        "A swing hanging from two ropes",              "Rewards",     "Then"),
    ("slide",      "Slide",        "A playground slide with a ladder",            "Rewards",     "Then"),
    ("bubbles",    "Bubbles",      "A bubble wand and bubbles",                   "Rewards",     "Then"),
    ("ball",       "Ball",         "A ball",                                      "Rewards",     "Then"),
    ("tablet",     "Tablet",       "A tablet device",                             "Rewards",     "Then"),
    ("book",       "Book",         "An open book",                                "Rewards",     "Then"),
    ("music",      "Music",        "Two music notes",                             "Rewards",     "Then"),
    ("blocks",     "Blocks",       "Three stacked building blocks",               "Rewards",     "Then"),
    ("wait",       "Wait",         "An open hand held up beside a clock",         "Regulation",  "Wait"),
    ("stop",       "Stop",         "An open hand inside an octagon",              "Regulation",  "Stop"),
    ("alldone",    "All done",     "A white tick inside a green circle",          "Regulation",  "Step"),
    ("oops",       "Plan changed", "A calendar square crossed through",           "Regulation",  "Oops"),
    ("desk",       "Desk work",    "A desk and chair",                            "School",      "First"),
    ("pencil",     "Pencil",       "A pencil",                                    "School",      "Step"),
    ("lineup",     "Line up",      "Three children standing in a row",            "School",      "Step"),
]

ICONS = {
    "toothbrush": i_toothbrush, "handwash": i_handwash, "towel": i_towel, "bath": i_bath,
    "toilet": i_toilet, "hairbrush": i_hairbrush, "tissue": i_tissue, "soap": i_soap,
    "shoes": i_shoes, "socks": i_socks, "coat": i_coat, "hat": i_hat, "shirt": i_shirt,
    "backpack": i_backpack, "cup": i_cup, "bowl": i_bowl, "plate": i_plate, "apple": i_apple,
    "sandwich": i_sandwich, "banana": i_banana, "car": i_car, "door": i_door, "bus": i_bus,
    "carseat": i_carseat, "gobag": i_gobag, "swing": i_swing, "slide": i_slide,
    "bubbles": i_bubbles, "ball": i_ball, "tablet": i_tablet, "book": i_book, "music": i_music,
    "blocks": i_blocks, "wait": i_wait, "stop": i_stop, "alldone": i_alldone, "oops": i_oops,
    "desk": i_desk, "pencil": i_pencil, "lineup": i_lineup,
}


def card_svg(name):
    icon = ICONS[name]()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD}" height="{CARD}" '
            f'viewBox="0 0 {CARD} {CARD}">'
            f'<rect width="{CARD}" height="{CARD}" fill="{CLOUD_WHITE}"/>'
            f'<circle cx="{CARD/2}" cy="{CARD/2}" r="{BADGE_R}" fill="{HORIZON}" opacity=".34"/>'
            f'<g transform="translate({OFFSET},{OFFSET}) scale({SCALE})">{icon}</g>'
            f'</svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    missing = [n for n, *_ in CARDS if n not in ICONS]
    extra = [n for n in ICONS if n not in {c[0] for c in CARDS}]
    if missing or extra:
        raise SystemExit("catalogue and icons disagree: missing=%s extra=%s" % (missing, extra))

    for name, *_ in CARDS:
        with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
            f.write(card_svg(name))

    with open(os.path.join(OUT, "MANIFEST.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "label", "alt_text", "category", "suggested_role", "image_source", "scope"])
        for name, label, alt, cat, role in CARDS:
            w.writerow([name + ".svg", label, alt, cat, role, "SymbolSet", "starter"])

    # contact sheet: 40 cards, 8 across, at card size so legibility is checked
    # at the size that actually matters rather than at full resolution
    cell, gap, lab = 150, 18, 26
    cols = 8
    rows = (len(CARDS) + cols - 1) // cols
    sw = cols * cell + (cols + 1) * gap
    sh = rows * (cell + lab) + (rows + 1) * gap + 56
    parts = [f'<rect width="{sw}" height="{sh}" fill="{CLOUD_WHITE}"/>',
             f'<text x="{gap}" y="38" font-family="{FONT}" font-size="24" font-weight="bold" '
             f'fill="{SLATE}">Starter card library &#8212; {len(CARDS)} cards at {cell}px</text>']
    for i, (name, label, *_rest) in enumerate(CARDS):
        cx = gap + (i % cols) * (cell + gap)
        cy = 56 + gap + (i // cols) * (cell + lab + gap)
        s = cell / CARD
        parts.append(f'<g transform="translate({cx},{cy}) scale({s})">{card_svg(name)[card_svg(name).index(">")+1:-6]}</g>')
        parts.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" rx="10" fill="none" '
                     f'stroke="{HORIZON}" stroke-width="2"/>')
        parts.append(f'<text x="{cx + cell/2}" y="{cy + cell + 18}" font-family="{FONT}" font-size="14" '
                     f'fill="{SLATE}" text-anchor="middle">{label}</text>')
    with open(SHEET, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{sw}" height="{sh}" '
                f'viewBox="0 0 {sw} {sh}">{"".join(parts)}</svg>')

    print("wrote %d cards to %s" % (len(CARDS), OUT))
    print("wrote MANIFEST.csv and %s" % os.path.basename(SHEET))


if __name__ == "__main__":
    main()
