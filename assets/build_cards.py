#!/usr/bin/env python3
"""Starter card library for Autism Visual Supports.

The third generator. build_art.py draws submission artwork, build_diagram.py draws
technical diagrams, this one draws the routine cards the Illustrator agent
reuses instead of generating. Keep them apart — see ASSETS.md caution 11.

Every card is one object or one action on Cloud White, inside a Horizon Blue badge,
at the figure-to-card ratio ASSETS.md fixes at 0.766. No text inside the picture:
the label is drawn by the application, so the same card serves a pre-verbal child
and a reader.

Outputs
  cards/<name>.svg      201 cards, 512x512
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


# ---- the first forty icons -----------------------------------------------------
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


# ---- the second hundred and sixty -----------------------------------------
# Same rule as above: one object or one action, nothing else, inside 0..200.
# Grouped by the part of a day they belong to, because that is how a parent
# looks for them -- see the Illustrator's category filter in SPEC.md.

def _bottle(x, y, w, h, body, cap=GRAY, neck=True):
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*0.22:g}" fill="{body}" '
         f'stroke="{SLATE}" stroke-width="4"/>']
    if neck:
        g.append(f'<rect x="{x+w*0.3:g}" y="{y-20}" width="{w*0.4:g}" height="22" rx="4" fill="{cap}"/>')
    return "".join(g)


def _round(cx, cy, r, fill, stroke=None, leaf=False):
    g = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke or SLATE}" stroke-width="4"/>']
    if leaf:
        g.append(f'<path d="M{cx} {cy-r} q16 -18 30 -10 q-8 18 -30 10 z" fill="{MEADOW}"/>')
    return "".join(g)


def _garment(top, body, trim):
    """A hanging garment silhouette, parameterised by its shoulder line."""
    return (f'<path d="{top}" fill="{body}" stroke="{trim}" stroke-width="5"/>')


def _arrow(x1, y1, x2, y2, col=CLEAR_SKY, w=9):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 16 * math.cos(a), y2 - 16 * math.sin(a)
    return (f'<path d="M{x1} {y1} L{hx:g} {hy:g}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x2} {y2} L{hx - 13*math.cos(a-0.5):g} {hy - 13*math.sin(a-0.5):g} '
            f'L{hx - 13*math.cos(a+0.5):g} {hy - 13*math.sin(a+0.5):g} z" fill="{col}"/>')


def _numeral(cx, cy, n, col=CLEAR_SKY, size=62):
    return (f'<text x="{cx}" y="{cy}" font-family="{FONT}" font-size="{size}" font-weight="bold" '
            f'fill="{col}" text-anchor="middle" dominant-baseline="central">{n}</text>')


# --- self-care ------------------------------------------------------------
def i_shower():
    return (f'<path d="M100 150 v-62 q0 -26 26 -26 h18" fill="none" stroke="{GRAY}" stroke-width="9" stroke-linecap="round"/>'
            f'<ellipse cx="148" cy="58" rx="26" ry="12" fill="{SKY}" stroke="{CLEAR_SKY}" stroke-width="4"/>'
            + "".join(f'<path d="M{132+i*11} 74 v{22+(i%2)*12}" stroke="{HORIZON}" stroke-width="6" '
                      f'stroke-linecap="round"/>' for i in range(4))
            + f'<path d="M44 158 h112" stroke="{CLEAR_SKY}" stroke-width="10" stroke-linecap="round"/>')


def i_hairwash():
    return (figure(100, 118, 0.9)
            + f'<path d="M72 68 q28 -26 56 0 q-28 -14 -56 0 z" fill="{CLOUD_WHITE}" stroke="{HORIZON}" stroke-width="4"/>'
            + f'<circle cx="74" cy="52" r="11" fill="{CLOUD_WHITE}" stroke="{HORIZON}" stroke-width="4"/>'
            + f'<circle cx="124" cy="46" r="9" fill="{CLOUD_WHITE}" stroke="{HORIZON}" stroke-width="4"/>')


def i_medicine():
    return (_bottle(70, 70, 60, 86, ROSE)
            + f'<rect x="78" y="96" width="44" height="30" rx="4" fill="{CLOUD_WHITE}"/>'
            + f'<path d="M100 102 v18 M91 111 h18" stroke="{ROSE}" stroke-width="7" stroke-linecap="round"/>')


def i_bandaid():
    return (f'<rect x="38" y="84" width="124" height="38" rx="19" fill="{SAND}" stroke="{WOOD}" '
            f'stroke-width="5" transform="rotate(-20 100 103)"/>'
            f'<rect x="80" y="88" width="40" height="30" rx="6" fill="{CLOUD_WHITE}" '
            f'transform="rotate(-20 100 103)"/>'
            + "".join(f'<circle cx="{88+ (i%3)*12}" cy="{96+(i//3)*12}" r="2.6" fill="{WOOD}" '
                      f'transform="rotate(-20 100 103)"/>' for i in range(6)))


def i_thermometer():
    return (f'<rect x="90" y="36" width="20" height="104" rx="10" fill="{CLOUD_WHITE}" stroke="{GRAY}" stroke-width="5"/>'
            f'<rect x="95" y="80" width="10" height="58" fill="{ROSE}"/>'
            f'<circle cx="100" cy="148" r="20" fill="{ROSE}" stroke="{SLATE}" stroke-width="4"/>'
            + "".join(f'<path d="M112 {56+i*14} h10" stroke="{GRAY}" stroke-width="4"/>' for i in range(5)))


def i_nosewipe():
    return (figure(100, 120, 0.95)
            + f'<path d="M96 76 l34 -14 l12 28 l-34 14 z" fill="{CLOUD_WHITE}" stroke="{HORIZON}" '
            f'stroke-width="4"/>'
            f'<path d="M130 62 q14 -10 20 4" fill="none" stroke="{HORIZON}" stroke-width="4"/>')


def i_hairdry():
    return (f'<rect x="54" y="74" width="74" height="42" rx="21" fill="{SKY}" stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<rect x="96" y="112" width="26" height="48" rx="10" fill="{CLEAR_SKY}"/>'
            + "".join(f'<path d="M132 {84+i*12} h{18+(i%2)*10}" stroke="{HORIZON}" stroke-width="6" '
                      f'stroke-linecap="round"/>' for i in range(3)))


def i_floss():
    return (f'<rect x="56" y="58" width="88" height="54" rx="12" fill="{SAGE}" stroke="{MEADOW}" stroke-width="5"/>'
            f'<circle cx="100" cy="85" r="16" fill="{CLOUD_WHITE}" stroke="{MEADOW}" stroke-width="4"/>'
            f'<path d="M68 112 v22 M132 112 v22" stroke="{CLOUD_WHITE}" stroke-width="5"/>'
            f'<path d="M68 134 q32 24 64 0" fill="none" stroke="{SLATE}" stroke-width="4"/>'
            f'<rect x="54" y="132" width="28" height="30" rx="8" fill="{SKIN}" stroke="{SLATE}" stroke-width="4"/>'
            f'<rect x="118" y="132" width="28" height="30" rx="8" fill="{SKIN}" stroke="{SLATE}" stroke-width="4"/>')


def i_comb():
    return (f'<rect x="40" y="70" width="120" height="26" rx="8" fill="{CLEAR_SKY}"/>'
            + "".join(f'<rect x="{46+i*13}" y="96" width="7" height="46" rx="3.5" fill="{SKY}"/>'
                      for i in range(9)))


def i_mirror():
    return (f'<ellipse cx="100" cy="82" rx="44" ry="52" fill="{HORIZON}" stroke="{GRAY}" stroke-width="7"/>'
            f'<circle cx="86" cy="74" r="4.5" fill="{SLATE}"/><circle cx="114" cy="74" r="4.5" fill="{SLATE}"/>'
            f'<path d="M86 96 q14 12 28 0" fill="none" stroke="{SLATE}" stroke-width="4" stroke-linecap="round"/>'
            f'<rect x="88" y="134" width="24" height="32" rx="8" fill="{GRAY}"/>')


def i_sunscreen():
    return (_bottle(72, 66, 56, 92, SUNFLOWER)
            + f'<circle cx="100" cy="106" r="16" fill="{CLOUD_WHITE}"/>'
            + "".join(f'<path d="M100 106 m0 -26 v9" stroke="{CLOUD_WHITE}" stroke-width="5" '
                      f'stroke-linecap="round" transform="rotate({i*45} 100 106)"/>' for i in range(8)))


def i_nails():
    return (palm(92, 118, 1.0)
            + f'<path d="M126 52 l34 20 l-34 20 z" fill="{GRAY}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M126 72 h-26" stroke="{GRAY}" stroke-width="8" stroke-linecap="round"/>')


def i_potty():
    return (f'<path d="M58 92 h84 v30 q0 26 -26 26 H84 q-26 0 -26 -26 z" fill="{SAGE}" '
            f'stroke="{MEADOW}" stroke-width="6"/>'
            f'<ellipse cx="100" cy="92" rx="46" ry="16" fill="{CLOUD_WHITE}" stroke="{MEADOW}" stroke-width="6"/>'
            f'<path d="M146 96 q18 4 18 18" fill="none" stroke="{MEADOW}" stroke-width="7"/>')


def i_diaper():
    return (f'<path d="M44 66 h112 v18 q0 62 -56 84 q-56 -22 -56 -84 z" fill="{CLOUD_WHITE}" '
            f'stroke="{HORIZON}" stroke-width="6"/>'
            f'<rect x="44" y="60" width="112" height="20" rx="10" fill="{HORIZON}"/>'
            f'<rect x="30" y="62" width="26" height="30" rx="7" fill="{SKY}" stroke="{CLEAR_SKY}" stroke-width="4"/>'
            f'<rect x="144" y="62" width="26" height="30" rx="7" fill="{SKY}" stroke="{CLEAR_SKY}" stroke-width="4"/>'
            f'<path d="M74 110 q26 16 52 0" fill="none" stroke="{HORIZON}" stroke-width="5"/>')


def i_mouthwash():
    return (_bottle(66, 64, 68, 94, HORIZON)
            + f'<rect x="76" y="98" width="48" height="26" rx="4" fill="{CLOUD_WHITE}"/>'
            + f'<path d="M86 111 q14 -10 28 0" fill="none" stroke="{CLEAR_SKY}" stroke-width="6" stroke-linecap="round"/>')


def i_haircut():
    return (figure(96, 122, 0.95)
            + f'<path d="M136 56 L166 86 M166 56 L136 86" stroke="{GRAY}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="134" cy="92" r="11" fill="none" stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<circle cx="168" cy="92" r="11" fill="none" stroke="{CLEAR_SKY}" stroke-width="5"/>')


# --- dressing -------------------------------------------------------------
def i_pants():
    return (f'<path d="M62 44 h76 v34 l-10 82 h-24 l-4 -66 l-4 66 H72 l-10 -82 z" fill="{CLEAR_SKY}" '
            f'stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="62" y="44" width="76" height="14" fill="{SKY}"/>')


def i_dress():
    return (f'<path d="M74 46 h52 l10 26 l-8 6 l12 76 H64 l12 -76 l-8 -6 z" fill="{ROSE}" '
            f'stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M86 52 q14 14 28 0" fill="none" stroke="{CLOUD_WHITE}" stroke-width="5"/>')


def i_sweater():
    return (f'<path d="M74 48 h52 l30 20 l-16 28 l-10 -6 v62 H70 v-62 l-10 6 l-16 -28 z" fill="{MEADOW}" '
            f'stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M70 140 h60" stroke="{SAGE}" stroke-width="9"/>')


def i_pajamas():
    return (f'<path d="M72 44 h56 l22 16 l-12 22 l-8 -5 v30 H70 V77 l-8 5 l-12 -22 z" fill="{HORIZON}" '
            f'stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M70 112 h60 v46 h-24 v-30 h-12 v30 H70 z" fill="{HORIZON}" stroke="{SLATE}" stroke-width="5"/>'
            + "".join(f'<circle cx="{82+i*18}" cy="{64+ (i%2)*10}" r="4" fill="{CLOUD_WHITE}"/>' for i in range(4)))


def i_underwear():
    return (f'<path d="M58 70 h84 v20 q0 44 -42 62 q-42 -18 -42 -62 z" fill="{CLOUD_WHITE}" '
            f'stroke="{SKY}" stroke-width="6"/>'
            f'<rect x="58" y="70" width="84" height="14" rx="7" fill="{SKY}"/>')


def i_gloves():
    return (palm(70, 110, 0.72, col=ROSE) + palm(134, 110, 0.72, col=ROSE)
            + f'<rect x="44" y="140" width="52" height="14" rx="7" fill="{SLATE}" opacity=".3"/>'
            + f'<rect x="108" y="140" width="52" height="14" rx="7" fill="{SLATE}" opacity=".3"/>')


def i_scarf():
    return (f'<path d="M50 60 q50 30 100 0 l8 26 q-58 32 -116 0 z" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M96 86 v62 h26 v-62" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            + "".join(f'<path d="M{98+i*9} 148 v12" stroke="{SLATE}" stroke-width="4"/>' for i in range(3)))


def i_boots():
    return (f'<path d="M58 44 h34 v70 h26 q14 0 14 16 v14 H58 z" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="54" y="140" width="84" height="16" rx="8" fill="{SLATE}"/>'
            f'<path d="M58 100 h34" stroke="{SAND}" stroke-width="7"/>')


def i_sandals():
    return (f'<ellipse cx="76" cy="118" rx="28" ry="42" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>'
            f'<ellipse cx="136" cy="118" rx="28" ry="42" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M60 102 q16 14 32 0 M120 102 q16 14 32 0" fill="none" stroke="{CLEAR_SKY}" stroke-width="7"/>')


def i_zip():
    return (f'<path d="M96 36 v128 M104 36 v128" stroke="{GRAY}" stroke-width="7"/>'
            + "".join(f'<rect x="{80}" y="{40+i*16}" width="14" height="9" rx="2" fill="{CLEAR_SKY}"/>'
                      f'<rect x="{106}" y="{48+i*16}" width="14" height="9" rx="2" fill="{CLEAR_SKY}"/>'
                      for i in range(4))
            + f'<rect x="84" y="112" width="32" height="34" rx="8" fill="{SKY}" stroke="{SLATE}" stroke-width="4"/>'
            + f'<rect x="94" y="140" width="12" height="26" rx="6" fill="{SLATE}"/>')


def i_buttons():
    return "".join(f'<circle cx="{66+(i%2)*68}" cy="{70+(i//2)*62}" r="30" fill="{SUNFLOWER}" '
                   f'stroke="{SLATE}" stroke-width="5"/>'
                   f'<circle cx="{58+(i%2)*68}" cy="{70+(i//2)*62}" r="4" fill="{SLATE}"/>'
                   f'<circle cx="{74+(i%2)*68}" cy="{70+(i//2)*62}" r="4" fill="{SLATE}"/>'
                   for i in range(4))


def i_laces():
    return (_shoe(40, 118)
            + f'<path d="M66 108 q18 -22 38 -4 q-18 22 -38 4 z" fill="none" stroke="{SUNFLOWER}" stroke-width="7"/>'
            + f'<path d="M104 104 q22 -18 40 2" fill="none" stroke="{SUNFLOWER}" stroke-width="7" stroke-linecap="round"/>')


def i_belt():
    return (f'<rect x="30" y="84" width="140" height="32" rx="8" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="84" y="74" width="44" height="52" rx="6" fill="none" stroke="{GRAY}" stroke-width="8"/>'
            f'<path d="M106 74 v52" stroke="{GRAY}" stroke-width="7"/>')


def i_mittens():
    return (f'<path d="M58 60 h34 q12 0 12 14 v46 q0 18 -18 18 h-22 q-18 0 -18 -18 V74 q0 -14 12 -14 z" '
            f'fill="{SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M46 86 q-14 2 -14 16 q0 14 14 12" fill="{SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="50" y="130" width="56" height="14" rx="7" fill="{CLOUD_WHITE}"/>'
            f'<path d="M118 70 h30 q10 0 10 12 v52 q0 14 -14 14 h-18" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>')

# --- food -----------------------------------------------------------------
def i_toast():
    return (f'<path d="M52 72 q0 -26 26 -26 h44 q26 0 26 26 v72 q0 12 -12 12 H64 q-12 0 -12 -12 z" '
            f'fill="{SAND}" stroke="{WOOD}" stroke-width="6"/>'
            f'<path d="M68 86 q0 -16 16 -16 h32 q16 0 16 16 v46 H68 z" fill="{SUNFLOWER}" opacity=".7"/>')


def i_cereal():
    return (f'<path d="M44 92 h112 q-8 62 -56 62 q-48 0 -56 -62 z" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<ellipse cx="100" cy="92" rx="56" ry="14" fill="{SAND}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            + "".join(f'<circle cx="{74+i*18}" cy="{88+(i%2)*8}" r="7" fill="{WOOD}"/>' for i in range(4)))


def i_milk():
    return (f'<path d="M66 70 h68 v88 q0 10 -10 10 H76 q-10 0 -10 -10 z" fill="{CLOUD_WHITE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<path d="M66 70 l34 -28 l34 28 z" fill="{HORIZON}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<rect x="78" y="104" width="44" height="30" rx="4" fill="{HORIZON}" opacity=".6"/>')


def i_juice():
    return (f'<path d="M72 60 h56 l-8 98 q-2 10 -12 10 H92 q-10 0 -12 -10 z" fill="{SUNFLOWER}" '
            f'stroke="{WOOD}" stroke-width="5"/>'
            f'<rect x="72" y="60" width="56" height="12" rx="6" fill="{CLOUD_WHITE}"/>'
            f'<path d="M116 56 l16 -24" stroke="{ROSE}" stroke-width="9" stroke-linecap="round"/>')


def i_water():
    return (f'<path d="M74 54 h52 l-6 100 q-2 12 -14 12 h-12 q-12 0 -14 -12 z" fill="none" '
            f'stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<path d="M79 96 h42 l-5 58 q-1 12 -13 12 h-6 q-12 0 -13 -12 z" fill="{HORIZON}"/>')


def i_yogurt():
    return (f'<path d="M70 76 h60 l-6 72 q-1 12 -13 12 H89 q-12 0 -13 -12 z" fill="{CLOUD_WHITE}" '
            f'stroke="{SKY}" stroke-width="6"/>'
            f'<rect x="64" y="60" width="72" height="18" rx="6" fill="{ROSE}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M86 108 q14 10 28 0" fill="none" stroke="{ROSE}" stroke-width="6"/>')


def i_egg():
    return (f'<ellipse cx="100" cy="112" rx="52" ry="40" fill="{CLOUD_WHITE}" stroke="{HORIZON}" stroke-width="5"/>'
            f'<circle cx="100" cy="110" r="22" fill="{SUNFLOWER}" stroke="{WOOD}" stroke-width="4"/>')


def i_cheese():
    return (f'<path d="M40 142 L96 56 h64 v86 z" fill="{SUNFLOWER}" stroke="{WOOD}" stroke-width="6"/>'
            + "".join(f'<circle cx="{104+(i%3)*18}" cy="{90+(i//3)*28}" r="{8-(i%2)*2}" fill="{SAND}"/>'
                      for i in range(5)))


def i_pasta():
    return (f'<path d="M44 108 h112 q-10 46 -56 46 q-46 0 -56 -46 z" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            + "".join(f'<path d="M{60+i*16} 104 q8 -30 {6-(i%2)*12} -44" fill="none" stroke="{SUNFLOWER}" '
                      f'stroke-width="7" stroke-linecap="round"/>' for i in range(6)))


def i_soup():
    return (f'<path d="M44 100 h112 q-8 54 -56 54 q-48 0 -56 -54 z" fill="{ROSE}" stroke="{SLATE}" stroke-width="6"/>'
            f'<ellipse cx="100" cy="100" rx="56" ry="13" fill="{SAND}" stroke="{SLATE}" stroke-width="5"/>'
            + "".join(f'<path d="M{84+i*16} 76 q8 -14 0 -26" fill="none" stroke="{HORIZON}" stroke-width="6" '
                      f'stroke-linecap="round"/>' for i in range(3)))


def i_carrot():
    return (f'<path d="M100 164 L66 72 q34 -18 68 0 z" fill="{SUNFLOWER}" stroke="{WOOD}" stroke-width="5"/>'
            + "".join(f'<path d="M{86+i*14} 60 q{6-i*6} -28 {i*8-8} -34" fill="none" stroke="{MEADOW}" '
                      f'stroke-width="8" stroke-linecap="round"/>' for i in range(3))
            + "".join(f'<path d="M{80+i*6} {96+i*22} h{36-i*10}" stroke="{WOOD}" stroke-width="4"/>' for i in range(3)))


def i_broccoli():
    return (f'<path d="M86 160 v-52 h28 v52 z" fill="{SAGE}" stroke="{MEADOW}" stroke-width="5"/>'
            + "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{MEADOW}" stroke="{SLATE}" stroke-width="3"/>'
                      for cx, cy, r in ((100, 60, 30), (66, 82, 24), (134, 82, 24), (100, 96, 22))))


def i_grapes():
    return ("".join(f'<circle cx="{cx}" cy="{cy}" r="17" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="3"/>'
                    for cx, cy in ((100, 70), (74, 96), (126, 96), (100, 100), (88, 126), (112, 126), (100, 150)))
            + f'<path d="M100 54 q10 -22 26 -24" fill="none" stroke="{MEADOW}" stroke-width="7" stroke-linecap="round"/>')


def i_orange():
    return _round(100, 104, 48, "#F5A742", leaf=True) + f'<path d="M100 60 v88 M56 104 h88" stroke="{SAND}" stroke-width="4" opacity=".7"/>'


def i_strawberry():
    return (f'<path d="M100 164 q-46 -22 -46 -62 q0 -26 46 -26 q46 0 46 26 q0 40 -46 62 z" fill="{ROSE}" '
            f'stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M72 74 q28 -18 56 0 q-16 -24 -56 0 z" fill="{MEADOW}"/>'
            + "".join(f'<circle cx="{80+(i%3)*20}" cy="{100+(i//3)*22}" r="3.4" fill="{SAND}"/>' for i in range(6)))


def i_cookie():
    return (_round(100, 104, 46, SAND, stroke=WOOD)
            + "".join(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{HAIR}"/>'
                      for cx, cy in ((84, 86), (118, 92), (96, 118), (124, 122), (76, 114))))


def i_icecream():
    return (f'<path d="M72 96 L100 164 L128 96 z" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>'
            f'<circle cx="86" cy="80" r="24" fill="{ROSE}" stroke="{SLATE}" stroke-width="4"/>'
            f'<circle cx="116" cy="78" r="24" fill="{CLOUD_WHITE}" stroke="{SLATE}" stroke-width="4"/>')


def i_cake():
    return (f'<path d="M50 104 h100 v44 q0 12 -12 12 H62 q-12 0 -12 -12 z" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M50 104 q16 -16 25 0 q16 -16 25 0 q16 -16 25 0 q16 -16 25 0 v10 H50 z" fill="{ROSE}"/>'
            f'<rect x="95" y="52" width="10" height="34" rx="5" fill="{CLOUD_WHITE}"/>'
            f'<path d="M100 52 q-10 -14 0 -20 q10 6 0 20 z" fill="{SUNFLOWER}"/>')


def i_pizza():
    return (f'<path d="M100 164 L40 66 q60 -30 120 0 z" fill="{SUNFLOWER}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M40 66 q60 -30 120 0 l-8 14 q-52 -24 -104 0 z" fill="{SAND}"/>'
            + "".join(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{ROSE}"/>'
                      for cx, cy in ((84, 102), (118, 100), (100, 132))))


def i_crackers():
    return "".join(f'<rect x="{54+i*18}" y="{64+i*16}" width="76" height="60" rx="8" fill="{SAND}" '
                   f'stroke="{WOOD}" stroke-width="5"/>'
                   + "".join(f'<circle cx="{70+i*18+(j%3)*24}" cy="{80+i*16+(j//3)*22}" r="3.4" fill="{WOOD}"/>'
                             for j in range(6))
                   for i in range(2))


def i_spoon():
    return (f'<ellipse cx="100" cy="68" rx="26" ry="32" fill="{CLOUD_WHITE}" stroke="{GRAY}" stroke-width="6"/>'
            f'<rect x="92" y="98" width="16" height="66" rx="8" fill="{GRAY}"/>')


def i_snack():
    return (f'<path d="M62 76 h76 l-8 78 q-2 12 -14 12 H84 q-12 0 -14 -12 z" fill="{HORIZON}" '
            f'stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<rect x="56" y="62" width="88" height="16" rx="8" fill="{CLEAR_SKY}"/>'
            + "".join(f'<circle cx="{82+(i%3)*18}" cy="{106+(i//3)*24}" r="8" fill="{SUNFLOWER}"/>' for i in range(5)))

# --- transitions and places ----------------------------------------------
def i_train():
    return (f'<path d="M48 62 h70 v40 h34 l16 34 v26 H48 z" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="62" y="76" width="42" height="30" rx="5" fill="{HORIZON}"/>'
            f'<rect x="128" y="110" width="28" height="20" rx="4" fill="{HORIZON}"/>'
            f'<circle cx="74" cy="168" r="15" fill="{SLATE}"/><circle cx="138" cy="168" r="15" fill="{SLATE}"/>')


def i_bike():
    return (f'<circle cx="58" cy="128" r="32" fill="none" stroke="{SLATE}" stroke-width="8"/>'
            f'<circle cx="146" cy="128" r="32" fill="none" stroke="{SLATE}" stroke-width="8"/>'
            f'<path d="M58 128 L96 72 h34 l16 56 M96 72 L112 128 H58" fill="none" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<path d="M86 66 h26" stroke="{SKY}" stroke-width="8" stroke-linecap="round"/>')


def i_scooter():
    return (f'<circle cx="54" cy="148" r="20" fill="none" stroke="{SLATE}" stroke-width="7"/>'
            f'<circle cx="152" cy="148" r="20" fill="none" stroke="{SLATE}" stroke-width="7"/>'
            f'<path d="M54 148 h98" stroke="{CLEAR_SKY}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M152 148 V58 h-26" fill="none" stroke="{CLEAR_SKY}" stroke-width="9" stroke-linecap="round"/>')


def i_walk():
    return (figure(100, 104, 1.0)
            + f'<path d="M92 142 l-20 26 M108 142 l20 26" stroke="{SLATE}" stroke-width="9" stroke-linecap="round"/>')


def i_stroller():
    return (f'<path d="M54 108 h76 q0 -46 -38 -46 q-38 0 -38 46 z" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M54 108 h86 l26 -48" fill="none" stroke="{SLATE}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M62 108 l-8 36 M126 108 l10 36" stroke="{SLATE}" stroke-width="6"/>'
            f'<circle cx="54" cy="152" r="14" fill="{SLATE}"/><circle cx="136" cy="152" r="14" fill="{SLATE}"/>')


def i_airplane():
    return (f'<path d="M100 28 q16 0 16 34 v30 l54 34 v20 l-54 -16 v30 l18 16 v14 l-34 -10 l-34 10 v-14 '
            f'l18 -16 v-30 l-54 16 v-20 l54 -34 V62 q0 -34 16 -34 z" fill="{CLOUD_WHITE}" '
            f'stroke="{CLEAR_SKY}" stroke-width="6" stroke-linejoin="round"/>')


def i_elevator():
    return (f'<rect x="52" y="40" width="96" height="124" rx="8" fill="{CLOUD_WHITE}" stroke="{GRAY}" stroke-width="6"/>'
            f'<path d="M100 40 v124" stroke="{GRAY}" stroke-width="5"/>'
            + _arrow(78, 106, 78, 70) + _arrow(122, 98, 122, 134))


def i_stairs():
    return (f'<path d="M34 164 V128 h32 V96 h32 V64 h32 V36 h36 v128 z" fill="{HORIZON}" '
            f'stroke="{CLEAR_SKY}" stroke-width="6" stroke-linejoin="round"/>'
            + "".join(f'<path d="M{34+i*32} {128-i*32} h32" stroke="{CLOUD_WHITE}" stroke-width="4"/>'
                      for i in range(4)))


def i_crosswalk():
    return (f'<rect x="36" y="48" width="128" height="112" rx="6" fill="{SLATE}" opacity=".16"/>'
            + "".join(f'<rect x="{46+i*30}" y="56" width="20" height="96" rx="4" fill="{CLOUD_WHITE}" '
                      f'stroke="{GRAY}" stroke-width="3"/>' for i in range(4)))


def i_seatbelt():
    return (f'<rect x="58" y="70" width="84" height="96" rx="16" fill="{HORIZON}" opacity=".7"/>'
            f'<circle cx="100" cy="48" r="22" fill="{SKIN}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M66 76 L138 158" stroke="{CLEAR_SKY}" stroke-width="16" stroke-linecap="round"/>'
            f'<rect x="92" y="108" width="34" height="26" rx="6" fill="{GRAY}" stroke="{SLATE}" '
            f'stroke-width="4" transform="rotate(42 109 121)"/>')


def i_key():
    return (f'<circle cx="68" cy="100" r="30" fill="none" stroke="{SUNFLOWER}" stroke-width="14"/>'
            f'<path d="M96 100 h62" stroke="{SUNFLOWER}" stroke-width="14" stroke-linecap="round"/>'
            f'<path d="M134 100 v22 M152 100 v22" stroke="{SUNFLOWER}" stroke-width="11" stroke-linecap="round"/>')


def i_coathook():
    return (f'<rect x="36" y="48" width="128" height="18" rx="6" fill="{WOOD}"/>'
            + "".join(f'<path d="M{62+i*38} 66 v22 q0 14 14 14" fill="none" stroke="{GRAY}" stroke-width="8" '
                      f'stroke-linecap="round"/>' for i in range(3)))


def i_home():
    return (f'<path d="M100 44 L168 104 h-20 v60 H52 v-60 H32 z" fill="{SAND}" stroke="{WOOD}" stroke-width="6"/>'
            f'<rect x="86" y="118" width="28" height="46" fill="{WOOD}"/>'
            f'<rect x="60" y="116" width="22" height="22" fill="{HORIZON}" stroke="{WOOD}" stroke-width="3"/>')


def i_school():
    return (f'<rect x="40" y="76" width="120" height="88" fill="{SAND}" stroke="{WOOD}" stroke-width="6"/>'
            f'<path d="M34 76 L100 36 L166 76 z" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="88" y="118" width="24" height="46" fill="{WOOD}"/>'
            + "".join(f'<rect x="{54+i*62}" y="96" width="24" height="24" fill="{HORIZON}" stroke="{WOOD}" '
                      f'stroke-width="3"/>' for i in range(2)))


def i_shop():
    return (f'<rect x="44" y="84" width="112" height="80" fill="{CLOUD_WHITE}" stroke="{GRAY}" stroke-width="6"/>'
            + "".join(f'<rect x="{44+i*28}" y="64" width="28" height="22" fill="{ROSE if i%2 else CLOUD_WHITE}" '
                      f'stroke="{SLATE}" stroke-width="3"/>' for i in range(4))
            + f'<rect x="78" y="112" width="44" height="52" fill="{HORIZON}" stroke="{GRAY}" stroke-width="4"/>')


def i_park():
    return (f'<rect x="92" y="104" width="18" height="60" fill="{WOOD}"/>'
            f'<circle cx="100" cy="80" r="46" fill="{MEADOW}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M36 164 h128" stroke="{SAGE}" stroke-width="12" stroke-linecap="round"/>')


def i_playground():
    return (f'<path d="M40 164 V72 h60 v92" fill="none" stroke="{CLEAR_SKY}" stroke-width="9"/>'
            f'<path d="M40 72 h60" stroke="{CLEAR_SKY}" stroke-width="9"/>'
            f'<path d="M100 78 q54 22 60 86 h-22 q-6 -52 -38 -66 z" fill="{SUNFLOWER}" '
            f'stroke="{WOOD}" stroke-width="5"/>'
            + "".join(f'<path d="M48 {92+i*20} h44" stroke="{HORIZON}" stroke-width="7"/>' for i in range(3)))


def i_doctor():
    return (f'<rect x="52" y="60" width="96" height="104" rx="12" fill="{CLOUD_WHITE}" stroke="{SKY}" stroke-width="6"/>'
            f'<path d="M100 84 v56 M72 112 h56" stroke="{ROSE}" stroke-width="16" stroke-linecap="round"/>')


def i_dentist():
    return (f'<path d="M58 70 q42 -26 84 0 q10 44 -14 84 q-12 16 -20 -8 q-8 -24 -16 0 q-8 24 -20 8 q-24 -40 -14 -84 z" '
            f'fill="{CLOUD_WHITE}" stroke="{SKY}" stroke-width="6"/>'
            f'<path d="M126 48 q18 8 14 26" fill="none" stroke="{SUNFLOWER}" stroke-width="7" stroke-linecap="round"/>')


def i_restaurant():
    return (f'<path d="M66 44 v54 q0 14 12 14 v54 M66 44 v30 M78 44 v30" fill="none" stroke="{GRAY}" stroke-width="7"/>'
            f'<path d="M130 44 q16 10 16 30 q0 16 -16 20 v72" fill="none" stroke="{GRAY}" stroke-width="7"/>')


def i_beach():
    return (f'<circle cx="150" cy="56" r="24" fill="{SUNFLOWER}"/>'
            f'<path d="M30 118 q36 -16 70 0 q34 16 70 0 v46 H30 z" fill="{HORIZON}"/>'
            f'<path d="M30 164 h140" stroke="{SAND}" stroke-width="14"/>'
            f'<path d="M62 118 v-44 q0 -22 22 -22" fill="none" stroke="{WOOD}" stroke-width="8"/>')


def i_grandma():
    return (figure(100, 108, 1.0, shirt=ROSE, hair="#C9C9C9")
            + f'<circle cx="86" cy="76" r="9" fill="none" stroke="{SLATE}" stroke-width="3"/>'
            f'<circle cx="114" cy="76" r="9" fill="none" stroke="{SLATE}" stroke-width="3"/>'
            f'<path d="M95 76 h10" stroke="{SLATE}" stroke-width="3"/>')


def i_carpark():
    return (f'<rect x="48" y="40" width="104" height="124" rx="10" fill="{CLEAR_SKY}"/>'
            f'<text x="100" y="108" font-family="{FONT}" font-size="86" font-weight="bold" fill="{CLOUD_WHITE}" '
            f'text-anchor="middle" dominant-baseline="central">P</text>')


def i_library():
    return ("".join(f'<rect x="{46+i*26}" y="{64+(i%2)*10}" width="20" height="{86-(i%2)*10}" rx="3" '
                    f'fill="{(CLEAR_SKY, ROSE, MEADOW, SUNFLOWER)[i%4]}" stroke="{SLATE}" stroke-width="4"/>'
                    for i in range(4))
            + f'<rect x="36" y="150" width="128" height="14" rx="4" fill="{WOOD}"/>')


def i_church():
    return (f'<rect x="56" y="88" width="88" height="76" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M50 88 L100 50 L150 88 z" fill="{HORIZON}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M100 50 v-22 M90 38 h20" stroke="{GRAY}" stroke-width="7"/>'
            f'<path d="M88 164 v-34 q12 -14 24 0 v34 z" fill="{WOOD}"/>')


def i_mat():
    return (f'<rect x="36" y="92" width="128" height="52" rx="8" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            + _shoe(62, 108, 0.7) + _shoe(106, 108, 0.7, col=SKY))


def i_wait_car():
    return (f'<path d="M44 128 l12 -34 q4 -12 18 -12 h52 q14 0 18 12 l12 34 v22 H44 z" fill="{SKY}" '
            f'stroke="{SLATE}" stroke-width="5"/>'
            f'<circle cx="70" cy="154" r="13" fill="{SLATE}"/><circle cx="130" cy="154" r="13" fill="{SLATE}"/>'
            + palm(100, 70, 0.6))

# --- rewards and play -----------------------------------------------------
def i_trampoline():
    return (f'<ellipse cx="100" cy="96" rx="66" ry="22" fill="{SLATE}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<ellipse cx="100" cy="96" rx="52" ry="14" fill="{GRAY}"/>'
            f'<path d="M48 104 l-10 54 M152 104 l10 54 M78 110 l-6 48 M122 110 l6 48" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            + _arrow(100, 76, 100, 38, SUNFLOWER, 8))


def i_sandbox():
    return (f'<rect x="38" y="96" width="124" height="60" rx="8" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M46 112 q54 -16 108 0 v38 H46 z" fill="{SAND}"/>'
            f'<rect x="116" y="60" width="14" height="52" rx="7" fill="{CLEAR_SKY}" transform="rotate(20 123 86)"/>'
            f'<path d="M126 56 q22 2 20 26 q-22 4 -20 -26 z" fill="{ROSE}" transform="rotate(20 136 70)"/>')


def i_climbing():
    return (f'<rect x="44" y="40" width="112" height="124" rx="10" fill="{SAGE}" stroke="{MEADOW}" stroke-width="5"/>'
            + "".join(f'<circle cx="{66+(i%3)*34}" cy="{66+(i//3)*34}" r="9" fill="{ROSE if i%2 else CLEAR_SKY}" '
                      f'stroke="{SLATE}" stroke-width="3"/>' for i in range(9)))


def i_seesaw():
    return (f'<path d="M34 128 L166 86" stroke="{CLEAR_SKY}" stroke-width="14" stroke-linecap="round"/>'
            f'<path d="M100 164 L82 108 h36 z" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            f'<circle cx="40" cy="116" r="12" fill="{SUNFLOWER}"/><circle cx="160" cy="76" r="12" fill="{ROSE}"/>')


def i_pool():
    return (f'<path d="M26 118 q22 -16 44 0 q22 16 44 0 q22 -16 44 0 q10 8 20 2 v44 H26 z" fill="{HORIZON}"/>'
            f'<circle cx="96" cy="84" r="19" fill="{SKIN}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M110 76 q26 -30 48 -8" fill="none" stroke="{SKIN}" stroke-width="13" stroke-linecap="round"/>'
            f'<path d="M26 148 q22 -14 44 0 q22 14 44 0 q22 -14 44 0" fill="none" stroke="{CLEAR_SKY}" '
            f'stroke-width="6" stroke-linecap="round"/>')


def i_puzzle():
    return (f'<path d="M48 48 h50 v14 q16 -10 16 6 q0 16 -16 6 v14 h50 v50 h-14 q10 16 -6 16 q-16 0 -6 -16 '
            f'H48 z" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M112 138 v14 h50 v-50 h-14" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="5"/>')


def i_toycar():
    return (f'<path d="M44 124 l10 -26 q4 -10 16 -10 h60 q12 0 16 10 l10 26 v16 H44 z" fill="{ROSE}" '
            f'stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="74" y="96" width="52" height="20" rx="5" fill="{HORIZON}"/>'
            f'<circle cx="70" cy="146" r="16" fill="{SLATE}"/><circle cx="130" cy="146" r="16" fill="{SLATE}"/>')


def i_toytrain():
    return (f'<rect x="40" y="94" width="58" height="46" rx="6" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="106" y="80" width="54" height="60" rx="6" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="118" y="52" width="18" height="30" rx="4" fill="{GRAY}"/>'
            + "".join(f'<circle cx="{56+i*32}" cy="152" r="12" fill="{SLATE}"/>' for i in range(4)))


def i_doll():
    return (figure(100, 106, 1.05, shirt=ROSE, hair=SUNFLOWER)
            + f'<circle cx="88" cy="74" r="4" fill="{SLATE}"/><circle cx="112" cy="74" r="4" fill="{SLATE}"/>'
            f'<path d="M92 88 q8 8 16 0" fill="none" stroke="{SLATE}" stroke-width="3.5" stroke-linecap="round"/>')


def i_teddy():
    return (f'<circle cx="68" cy="62" r="20" fill="{WOOD}" stroke="{SLATE}" stroke-width="4"/>'
            f'<circle cx="132" cy="62" r="20" fill="{WOOD}" stroke="{SLATE}" stroke-width="4"/>'
            f'<circle cx="100" cy="86" r="44" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            f'<ellipse cx="100" cy="100" rx="20" ry="15" fill="{SAND}"/>'
            f'<circle cx="86" cy="78" r="5" fill="{SLATE}"/><circle cx="114" cy="78" r="5" fill="{SLATE}"/>'
            f'<ellipse cx="100" cy="146" rx="40" ry="26" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>')


def i_lego():
    return (f'<rect x="48" y="78" width="104" height="58" rx="8" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            + "".join(f'<rect x="{62+i*32}" y="58" width="24" height="22" rx="6" fill="{ROSE}" '
                      f'stroke="{SLATE}" stroke-width="5"/>' for i in range(3)))


def i_drawing():
    return (f'<rect x="48" y="44" width="104" height="120" rx="6" fill="{CLOUD_WHITE}" stroke="{GRAY}" stroke-width="5"/>'
            f'<circle cx="86" cy="82" r="16" fill="{SUNFLOWER}"/>'
            f'<path d="M64 134 l24 -30 l20 22 l18 -26 l12 34 z" fill="{SAGE}"/>'
            f'<path d="M150 50 l16 -12" stroke="{ROSE}" stroke-width="10" stroke-linecap="round"/>')


def i_paint():
    return (f'<path d="M44 108 q0 -46 56 -46 q56 0 56 46 q0 16 -22 16 q-16 0 -16 12 q0 10 8 16 q10 8 -2 16 '
            f'q-10 6 -24 6 q-56 0 -56 -66 z" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>'
            + "".join(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{c}"/>'
                      for cx, cy, c in ((74, 86, ROSE), (104, 76, CLEAR_SKY), (132, 92, MEADOW), (80, 118, SUNFLOWER))))


def i_playdough():
    return (f'<ellipse cx="100" cy="130" rx="54" ry="30" fill="{SUNFLOWER}" stroke="{WOOD}" stroke-width="5"/>'
            f'<ellipse cx="100" cy="112" rx="54" ry="26" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M66 78 q34 -28 68 0" fill="none" stroke="{CLEAR_SKY}" stroke-width="12" stroke-linecap="round"/>')


def i_stickers():
    return "".join(f'<circle cx="{cx}" cy="{cy}" r="26" fill="{c}" stroke="{SLATE}" stroke-width="4"/>'
                   f'<path d="M{cx-9} {cy+4} q9 9 18 0" fill="none" stroke="{SLATE}" stroke-width="3.5" '
                   f'stroke-linecap="round"/>'
                   f'<circle cx="{cx-8}" cy="{cy-7}" r="3" fill="{SLATE}"/>'
                   f'<circle cx="{cx+8}" cy="{cy-7}" r="3" fill="{SLATE}"/>'
                   for cx, cy, c in ((70, 74, SUNFLOWER), (130, 74, ROSE), (100, 132, SAGE)))


def i_dance():
    return (figure(100, 100, 1.0, shirt=ROSE)
            + f'<path d="M86 108 l-26 -22 M114 108 l26 -14" stroke="{SLATE}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M92 142 l-18 28 M108 142 l24 22" stroke="{SLATE}" stroke-width="9" stroke-linecap="round"/>')


def i_tv():
    return (f'<rect x="38" y="52" width="124" height="86" rx="8" fill="{SLATE}" stroke="{GRAY}" stroke-width="5"/>'
            f'<rect x="50" y="64" width="100" height="62" rx="4" fill="{HORIZON}"/>'
            f'<path d="M78 164 h44 M100 138 v26" stroke="{GRAY}" stroke-width="8" stroke-linecap="round"/>')


def i_trike():
    return (f'<circle cx="56" cy="138" r="28" fill="none" stroke="{SLATE}" stroke-width="8"/>'
            f'<circle cx="146" cy="146" r="18" fill="none" stroke="{SLATE}" stroke-width="7"/>'
            f'<path d="M56 138 L104 78 h30 l12 68" fill="none" stroke="{ROSE}" stroke-width="8"/>'
            f'<path d="M96 72 h22" stroke="{CLEAR_SKY}" stroke-width="8" stroke-linecap="round"/>')


def i_balloon():
    return (f'<ellipse cx="100" cy="84" rx="40" ry="48" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M94 132 h12 l-6 10 z" fill="{SLATE}"/>'
            f'<path d="M100 142 q14 22 -4 34 q-18 12 4 24" fill="none" stroke="{GRAY}" stroke-width="4"/>'
            f'<ellipse cx="86" cy="66" rx="10" ry="14" fill="{CLOUD_WHITE}" opacity=".6"/>')


def i_kite():
    return (f'<path d="M100 36 L152 92 L100 148 L48 92 z" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M100 36 v112 M48 92 h104" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M100 148 q18 18 -2 24 q-20 6 2 18" fill="none" stroke="{GRAY}" stroke-width="4"/>')


def i_sprinkler():
    return (f'<path d="M100 164 v-54" stroke="{GRAY}" stroke-width="10" stroke-linecap="round"/>'
            + "".join(f'<path d="M100 104 q{dx} -34 {dx*1.7:g} -46" fill="none" stroke="{HORIZON}" '
                      f'stroke-width="7" stroke-linecap="round"/>' for dx in (-30, -12, 12, 30))
            + f'<path d="M66 164 h68" stroke="{SAGE}" stroke-width="10" stroke-linecap="round"/>')


def i_swingtire():
    return (f'<path d="M100 36 v44" stroke="{WOOD}" stroke-width="7"/>'
            f'<circle cx="100" cy="124" r="42" fill="none" stroke="{SLATE}" stroke-width="18"/>'
            f'<circle cx="100" cy="124" r="42" fill="none" stroke="{GRAY}" stroke-width="5"/>')


def i_hopscotch():
    return "".join(f'<rect x="{(74 if i<3 else 48+(i-3)*52)}" y="{140-i*32 if i<3 else 44}" '
                   f'width="52" height="30" rx="4" fill="{HORIZON}" stroke="{CLEAR_SKY}" stroke-width="4"/>'
                   + _numeral((100 if i < 3 else 74+(i-3)*52), (155-i*32 if i < 3 else 59), i+1, CLEAR_SKY, 22)
                   for i in range(5))


def i_video():
    return (f'<rect x="38" y="60" width="90" height="80" rx="10" fill="{SLATE}"/>'
            f'<path d="M128 90 l34 -22 v64 l-34 -22 z" fill="{GRAY}"/>'
            f'<path d="M72 84 l26 16 l-26 16 z" fill="{CLOUD_WHITE}"/>')


def i_sensory():
    return (f'<circle cx="100" cy="104" r="50" fill="{SAGE}" stroke="{MEADOW}" stroke-width="5"/>'
            + "".join(f'<circle cx="{cx}" cy="{cy}" r="11" fill="{MEADOW}"/>'
                      for cx, cy in ((78, 84), (122, 84), (100, 106), (78, 128), (122, 128))))


def i_pet():
    return (f'<ellipse cx="96" cy="118" rx="48" ry="32" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            f'<circle cx="150" cy="92" r="26" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M140 68 q-6 -22 10 -16" fill="{WOOD}" stroke="{SLATE}" stroke-width="4"/>'
            f'<circle cx="160" cy="88" r="4" fill="{SLATE}"/>'
            f'<path d="M48 108 q-18 -14 -8 -30" fill="none" stroke="{SLATE}" stroke-width="7" stroke-linecap="round"/>'
            + "".join(f'<path d="M{74+i*32} 148 v14" stroke="{SLATE}" stroke-width="8" stroke-linecap="round"/>'
                      for i in range(2)))


def i_sing():
    return (figure(84, 108, 0.95)
            + f'<path d="M126 84 q18 -6 18 10 q0 16 -18 10 z" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="4"/>'
            + f'<path d="M150 72 v32 M150 72 q14 2 14 16 q0 14 -14 16" fill="none" stroke="{CLEAR_SKY}" stroke-width="5"/>')

# --- regulation -----------------------------------------------------------
def i_breathe():
    return (f'<circle cx="100" cy="100" r="30" fill="{HORIZON}" stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<circle cx="100" cy="100" r="52" fill="none" stroke="{SKY}" stroke-width="5" opacity=".7"/>'
            f'<circle cx="100" cy="100" r="72" fill="none" stroke="{HORIZON}" stroke-width="5" opacity=".5"/>'
            + _arrow(100, 76, 100, 46, CLEAR_SKY, 7))


def i_squeeze():
    return (palm(76, 110, 0.9) + palm(130, 110, 0.9)
            + f'<circle cx="103" cy="92" r="20" fill="{ROSE}" stroke="{SLATE}" stroke-width="4"/>')


def i_headphones():
    return (f'<path d="M50 118 V96 a50 50 0 0 1 100 0 v22" fill="none" stroke="{SLATE}" stroke-width="11"/>'
            f'<rect x="36" y="110" width="28" height="48" rx="14" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="136" y="110" width="28" height="48" rx="14" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>')


def i_quiet():
    return (f'<circle cx="100" cy="100" r="56" fill="{HORIZON}" opacity=".5"/>'
            + figure(100, 112, 0.9)
            + f'<rect x="92" y="60" width="9" height="46" rx="4.5" fill="{CLOUD_WHITE}" stroke="{SLATE}" '
            f'stroke-width="3" transform="rotate(-14 96 83)"/>')


def i_break():
    return (f'<rect x="48" y="60" width="104" height="84" rx="12" fill="{SAGE}" stroke="{MEADOW}" stroke-width="6"/>'
            f'<path d="M78 84 v36 M122 84 v36" stroke="{MEADOW}" stroke-width="16" stroke-linecap="round"/>')


def i_calmcorner():
    return (f'<path d="M34 164 V66 h66" fill="none" stroke="{GRAY}" stroke-width="7"/>'
            f'<rect x="46" y="112" width="60" height="52" rx="12" fill="{SAGE}" stroke="{MEADOW}" stroke-width="5"/>'
            f'<circle cx="138" cy="96" r="28" fill="{HORIZON}" stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<path d="M126 100 q12 10 24 0" fill="none" stroke="{CLEAR_SKY}" stroke-width="5" stroke-linecap="round"/>')


def i_weighted():
    return (f'<path d="M44 76 h112 v62 q0 20 -24 20 H68 q-24 0 -24 -20 z" fill="{CLEAR_SKY}" '
            f'stroke="{SLATE}" stroke-width="5"/>'
            + "".join(f'<path d="M{44+i*28} 76 v82" stroke="{SKY}" stroke-width="4"/>' for i in range(1, 4))
            + "".join(f'<circle cx="{58+i*28}" cy="{116}" r="6" fill="{HORIZON}"/>' for i in range(4)))


def i_fidget():
    return (f'<circle cx="100" cy="100" r="22" fill="{GRAY}" stroke="{SLATE}" stroke-width="4"/>'
            + "".join(f'<circle cx="{100+54*__import__("math").cos(a):g}" cy="{100+54*__import__("math").sin(a):g}" '
                      f'r="26" fill="{c}" stroke="{SLATE}" stroke-width="4"/>'
                      for a, c in ((-1.5708, ROSE), (0.5236, CLEAR_SKY), (2.618, SUNFLOWER))))


def i_chew():
    return (f'<path d="M62 92 q38 -34 76 0 q-10 50 -38 62 q-28 -12 -38 -62 z" fill="{SAGE}" '
            f'stroke="{MEADOW}" stroke-width="5"/>'
            f'<path d="M62 92 q38 20 76 0" fill="none" stroke="{MEADOW}" stroke-width="5"/>')


def i_timer():
    return (f'<path d="M62 36 h76 l-30 60 l30 68 H62 l30 -68 z" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<path d="M78 148 h44 l-22 -44 z" fill="{SUNFLOWER}"/>'
            f'<path d="M56 32 h88 M56 168 h88" stroke="{CLEAR_SKY}" stroke-width="8" stroke-linecap="round"/>')


def i_countdown():
    return (f'<circle cx="100" cy="104" r="56" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<path d="M100 104 L100 48 A56 56 0 0 1 148 132 z" fill="{SUNFLOWER}" opacity=".8"/>'
            f'<circle cx="100" cy="104" r="7" fill="{SLATE}"/>')


def i_first():
    return (f'<rect x="42" y="56" width="116" height="96" rx="12" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            + _numeral(100, 106, "1", CLEAR_SKY, 72))


def i_then():
    return (f'<rect x="42" y="56" width="116" height="96" rx="12" fill="{CLOUD_WHITE}" stroke="{MEADOW}" stroke-width="7"/>'
            + _numeral(100, 106, "2", MEADOW, 72))


def i_choice():
    return (f'<rect x="30" y="64" width="62" height="78" rx="10" fill="{HORIZON}" stroke="{CLEAR_SKY}" stroke-width="5"/>'
            f'<rect x="108" y="64" width="62" height="78" rx="10" fill="{SAGE}" stroke="{MEADOW}" stroke-width="5"/>'
            + _numeral(100, 104, "/", GRAY, 54))


def i_help():
    return (palm(100, 116, 1.0)
            + f'<text x="100" y="46" font-family="{FONT}" font-size="54" font-weight="bold" fill="{ROSE}" '
            f'text-anchor="middle" dominant-baseline="central">?</text>')


def i_more():
    return (palm(70, 112, 0.66) + palm(132, 112, 0.66)
            + _arrow(86, 74, 114, 74, MEADOW, 8))


def i_finished():
    return (f'<circle cx="100" cy="100" r="56" fill="{MEADOW}"/>'
            f'<path d="M72 102 l20 22 l38 -46" fill="none" stroke="{CLOUD_WHITE}" stroke-width="14" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def i_feelings():
    return "".join(f'<circle cx="{cx}" cy="{cy}" r="30" fill="{c}" stroke="{SLATE}" stroke-width="4"/>'
                   f'<circle cx="{cx-10}" cy="{cy-8}" r="3.6" fill="{SLATE}"/>'
                   f'<circle cx="{cx+10}" cy="{cy-8}" r="3.6" fill="{SLATE}"/>'
                   f'<path d="{mouth}" fill="none" stroke="{SLATE}" stroke-width="4" stroke-linecap="round"/>'
                   for cx, cy, c, mouth in (
                       (64, 70, SUNFLOWER, "M52 76 q12 12 24 0"),
                       (136, 70, HORIZON, "M124 84 q12 -12 24 0"),
                       (100, 134, ROSE, "M88 136 h24")))


def i_loud():
    return (f'<path d="M48 84 h26 l30 -26 v84 l-30 -26 H48 z" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            + "".join(f'<path d="M{118+i*16} {90-i*8} a{22+i*14} {22+i*14} 0 0 1 0 {44+i*16}" fill="none" '
                      f'stroke="{ROSE}" stroke-width="6" stroke-linecap="round"/>' for i in range(3)))


def i_light_off():
    return (f'<path d="M100 40 a34 34 0 0 1 20 62 v14 H80 v-14 a34 34 0 0 1 20 -62 z" fill="{SAND}" '
            f'stroke="{GRAY}" stroke-width="5"/>'
            f'<rect x="80" y="118" width="40" height="14" rx="4" fill="{GRAY}"/>'
            f'<path d="M46 46 L154 158" stroke="{ROSE}" stroke-width="11" stroke-linecap="round"/>')


# --- people and social ----------------------------------------------------
def i_mum():
    return figure(100, 106, 1.05, shirt=ROSE, hair="#3F2A1C")


def i_dad():
    return figure(100, 106, 1.05, shirt=CLEAR_SKY, hair="#2F2118")


def i_teacher():
    return (figure(84, 112, 0.95, shirt=MEADOW)
            + f'<rect x="124" y="56" width="52" height="68" rx="4" fill="{CLOUD_WHITE}" stroke="{GRAY}" stroke-width="4"/>'
            + "".join(f'<path d="M132 {72+i*16} h36" stroke="{HORIZON}" stroke-width="4"/>' for i in range(3)))


def i_friend():
    return (figure(70, 110, 0.86, shirt=SUNFLOWER)
            + figure(130, 110, 0.86, shirt=CLEAR_SKY)
            + f'<path d="M86 106 q14 -10 28 0" fill="none" stroke="{SLATE}" stroke-width="7" stroke-linecap="round"/>')


def i_share():
    return (palm(62, 108, 0.74) + palm(138, 108, 0.74)
            + f'<circle cx="100" cy="84" r="18" fill="{SUNFLOWER}" stroke="{SLATE}" stroke-width="4"/>'
            + _arrow(78, 60, 122, 60, MEADOW, 7))


def i_turntaking():
    return (f'<circle cx="100" cy="104" r="48" fill="none" stroke="{CLEAR_SKY}" stroke-width="9" '
            f'stroke-dasharray="58 28"/>'
            + _arrow(140, 72, 152, 96, CLEAR_SKY, 8)
            + figure(100, 110, 0.72))


def i_hello():
    return (figure(100, 114, 0.95)
            + f'<path d="M122 104 l24 -34" stroke="{SLATE}" stroke-width="9" stroke-linecap="round"/>'
            + palm(152, 58, 0.5))


def i_goodbye():
    return (figure(84, 114, 0.9)
            + palm(140, 66, 0.55)
            + _arrow(124, 126, 170, 126, GRAY, 7))


def i_hug():
    return (f'<circle cx="80" cy="74" r="22" fill="{SKIN}" stroke="{SLATE}" stroke-width="4"/>'
            f'<circle cx="124" cy="74" r="22" fill="{SKIN}" stroke="{SLATE}" stroke-width="4"/>'
            f'<path d="M48 160 q0 -56 52 -56 q52 0 52 56 z" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M66 126 q34 22 68 0" fill="none" stroke="{CLOUD_WHITE}" stroke-width="8" stroke-linecap="round"/>')


def i_please():
    return (figure(100, 122, 0.95)
            + f'<path d="M118 104 a26 26 0 1 1 -36 0" fill="none" stroke="{ROSE}" stroke-width="7" '
            f'stroke-linecap="round"/>'
            + palm(136, 78, 0.5))


def i_doctor_visit():
    return (figure(78, 114, 0.9, shirt=CLOUD_WHITE)
            + f'<circle cx="140" cy="118" r="22" fill="none" stroke="{GRAY}" stroke-width="7"/>'
            f'<path d="M140 96 v-26 q0 -12 -12 -12" fill="none" stroke="{GRAY}" stroke-width="6"/>')

# --- school ---------------------------------------------------------------
def i_carpet():
    return (f'<rect x="34" y="78" width="132" height="84" rx="10" fill="{CLEAR_SKY}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="52" y="94" width="96" height="52" rx="6" fill="{HORIZON}"/>'
            + "".join(f'<circle cx="{74+i*26}" cy="120" r="9" fill="{CLOUD_WHITE}"/>' for i in range(4)))


def i_circletime():
    return (f'<circle cx="100" cy="104" r="52" fill="none" stroke="{HORIZON}" stroke-width="10"/>'
            + "".join(f'<circle cx="{100+52*__import__("math").cos(i*1.0472):g}" '
                      f'cy="{104+52*__import__("math").sin(i*1.0472):g}" r="15" '
                      f'fill="{(SUNFLOWER, CLEAR_SKY, ROSE, MEADOW, SKY, SAGE)[i]}" stroke="{SLATE}" '
                      f'stroke-width="3"/>' for i in range(6)))


def i_recess():
    return (f'<circle cx="152" cy="48" r="20" fill="{SUNFLOWER}"/>'
            f'<path d="M34 48 h132" stroke="{WOOD}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M66 54 v52 M134 54 v52" stroke="{GRAY}" stroke-width="6"/>'
            f'<rect x="56" y="106" width="88" height="14" rx="7" fill="{CLEAR_SKY}"/>'
            f'<path d="M34 160 h132" stroke="{SAGE}" stroke-width="10" stroke-linecap="round"/>')


def i_gym():
    return (f'<rect x="30" y="92" width="26" height="26" rx="5" fill="{SLATE}"/>'
            f'<rect x="144" y="92" width="26" height="26" rx="5" fill="{SLATE}"/>'
            f'<rect x="56" y="100" width="88" height="10" rx="5" fill="{GRAY}"/>'
            f'<rect x="22" y="80" width="14" height="50" rx="7" fill="{GRAY}"/>'
            f'<rect x="164" y="80" width="14" height="50" rx="7" fill="{GRAY}"/>')


def i_artclass():
    return (f'<rect x="40" y="46" width="120" height="100" rx="6" fill="{CLOUD_WHITE}" stroke="{WOOD}" stroke-width="6"/>'
            f'<path d="M56 130 l28 -40 l22 26 l20 -32 l18 46 z" fill="{SAGE}"/>'
            f'<circle cx="74" cy="76" r="14" fill="{SUNFLOWER}"/>'
            f'<path d="M78 146 v18 M122 146 v18" stroke="{WOOD}" stroke-width="7"/>')


def i_musicclass():
    return (f'<rect x="38" y="78" width="124" height="64" rx="6" fill="{CLOUD_WHITE}" stroke="{SLATE}" stroke-width="5"/>'
            + "".join(f'<rect x="{46+i*17}" y="78" width="11" height="40" fill="{SLATE}"/>' for i in range(7))
            + f'<path d="M38 118 h124" stroke="{GRAY}" stroke-width="3"/>')


def i_handup():
    return (figure(100, 122, 0.95)
            + f'<path d="M116 108 l14 -42" stroke="{SLATE}" stroke-width="9" stroke-linecap="round"/>'
            + palm(136, 48, 0.52))


def i_listen():
    return (f'<path d="M78 46 q44 -16 44 42 q0 34 -22 46 q-16 8 -16 30 h-26 q0 -34 -16 -48 q-16 -14 -16 -34 '
            f'q0 -32 52 -36 z" fill="{SKIN}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M92 98 q-16 -12 0 -24" fill="none" stroke="{SLATE}" stroke-width="5" stroke-linecap="round"/>'
            + "".join(f'<path d="M{140+i*14} {76-i*6} a{18+i*12} {18+i*12} 0 0 1 0 {36+i*14}" fill="none" '
                      f'stroke="{CLEAR_SKY}" stroke-width="5" stroke-linecap="round"/>' for i in range(2)))


def i_sit():
    return (f'<path d="M62 48 h18 v62 h56 v18 H62 z" fill="{WOOD}" stroke="{SLATE}" stroke-width="5"/>'
            f'<path d="M66 128 v34 M132 128 v34" stroke="{SLATE}" stroke-width="8"/>'
            + figure(102, 84, 0.62))


def i_hallway():
    return (f'<path d="M30 164 L70 56 h60 l40 108 z" fill="{SAND}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M70 56 v108 M130 56 v108" stroke="{WOOD}" stroke-width="4"/>'
            + figure(100, 116, 0.62))


def i_locker():
    return ("".join(f'<rect x="{44+i*40}" y="44" width="36" height="116" rx="5" fill="{CLEAR_SKY}" '
                    f'stroke="{SLATE}" stroke-width="4"/>'
                    f'<circle cx="{72+i*40}" cy="104" r="4" fill="{SLATE}"/>'
                    + "".join(f'<path d="M{52+i*40} {60+j*7} h20" stroke="{SKY}" stroke-width="3"/>'
                              for j in range(3))
                    for i in range(3)))


def i_lunchbox():
    return (f'<rect x="44" y="80" width="112" height="78" rx="10" fill="{ROSE}" stroke="{SLATE}" stroke-width="5"/>'
            f'<rect x="44" y="80" width="112" height="20" rx="8" fill="{SLATE}" opacity=".2"/>'
            f'<path d="M80 80 v-14 q0 -12 20 -12 q20 0 20 12 v14" fill="none" stroke="{GRAY}" stroke-width="7"/>')


def i_bell():
    return (f'<path d="M100 42 q38 0 38 46 v30 l12 18 H50 l12 -18 V88 q0 -46 38 -46 z" fill="{SUNFLOWER}" '
            f'stroke="{WOOD}" stroke-width="5"/>'
            f'<circle cx="100" cy="146" r="12" fill="{WOOD}"/>')


def i_busline():
    return ("".join(figure(56 + i * 44, 112, 0.66) for i in range(3))
            + _arrow(38, 158, 162, 158, CLEAR_SKY, 7))


def i_worksheet():
    return (f'<rect x="54" y="38" width="92" height="124" rx="6" fill="{CLOUD_WHITE}" stroke="{GRAY}" stroke-width="5"/>'
            + "".join(f'<path d="M70 {64+i*20} h60" stroke="{HORIZON}" stroke-width="6" stroke-linecap="round"/>'
                      for i in range(5))
            + f'<path d="M118 112 l12 14 l22 -28" fill="none" stroke="{MEADOW}" stroke-width="8" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def i_scissors():
    return (f'<path d="M72 150 L132 60 M128 150 L68 60" stroke="{GRAY}" stroke-width="9" stroke-linecap="round"/>'
            f'<circle cx="68" cy="158" r="16" fill="none" stroke="{CLEAR_SKY}" stroke-width="7"/>'
            f'<circle cx="132" cy="158" r="16" fill="none" stroke="{CLEAR_SKY}" stroke-width="7"/>')


def i_glue():
    return (_bottle(74, 74, 52, 84, CLOUD_WHITE, cap=SUNFLOWER)
            + f'<rect x="84" y="100" width="32" height="34" rx="3" fill="{SUNFLOWER}" opacity=".7"/>')


# --- time and sequence ----------------------------------------------------
def i_morning():
    return (f'<path d="M34 140 h132" stroke="{SAND}" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="100" cy="140" r="38" fill="{SUNFLOWER}"/>'
            + "".join(f'<path d="M100 140 m0 -54 v-14" stroke="{SUNFLOWER}" stroke-width="7" '
                      f'stroke-linecap="round" transform="rotate({-60+i*30} 100 140)"/>' for i in range(5)))


def i_night():
    return (f'<mask id="mn"><rect width="200" height="200" fill="white"/>'
            f'<circle cx="146" cy="68" r="46" fill="black"/></mask>'
            f'<circle cx="112" cy="86" r="50" fill="{CLEAR_SKY}" mask="url(#mn)"/>'
            + "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUNFLOWER}"/>'
                      for cx, cy, r in ((48, 48, 6), (42, 104, 5), (74, 146, 6), (124, 158, 4.5))))


def i_clock():
    return (f'<circle cx="100" cy="100" r="58" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="8"/>'
            f'<path d="M100 100 V62 M100 100 l28 18" stroke="{SLATE}" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="100" cy="100" r="6" fill="{SLATE}"/>'
            + "".join(f'<path d="M100 100 m0 -50 v8" stroke="{GRAY}" stroke-width="5" '
                      f'transform="rotate({i*90} 100 100)"/>' for i in range(4)))


def i_calendar():
    return (f'<rect x="38" y="52" width="124" height="112" rx="8" fill="{CLOUD_WHITE}" stroke="{CLEAR_SKY}" stroke-width="6"/>'
            f'<rect x="38" y="52" width="124" height="26" rx="8" fill="{CLEAR_SKY}"/>'
            + "".join(f'<rect x="{52+(i%4)*28}" y="{90+(i//4)*26}" width="20" height="18" rx="3" '
                      f'fill="{HORIZON}"/>' for i in range(8)))


def i_twomore():
    return (f'<circle cx="100" cy="100" r="56" fill="{HORIZON}" opacity=".45"/>'
            + _numeral(100, 100, "2", CLEAR_SKY, 86))


def i_last():
    return (f'<rect x="34" y="78" width="36" height="48" rx="6" fill="{HORIZON}" opacity=".5"/>'
            f'<rect x="80" y="78" width="36" height="48" rx="6" fill="{HORIZON}" opacity=".7"/>'
            f'<rect x="126" y="70" width="44" height="64" rx="7" fill="{SUNFLOWER}" stroke="{WOOD}" stroke-width="5"/>'
            + _numeral(148, 102, "!", WOOD, 42))


def i_sequence():
    return ("".join(f'<rect x="{30+i*52}" y="76" width="44" height="48" rx="7" fill="{HORIZON}" '
                    f'stroke="{CLEAR_SKY}" stroke-width="4"/>' + _numeral(52+i*52, 100, i+1, CLEAR_SKY, 28)
                    for i in range(3))
            + "".join(_arrow(76 + i * 52, 100, 100 + i * 52, 100, GRAY, 5) for i in range(2)))

# name, label (3 words max -- guardrail 1), alt text, category, suggested role
CARDS_EXTRA = [
    ("shower","Shower","A shower head with running water","Self-care","First"),
    ("hairwash","Wash hair","A child with shampoo in their hair","Self-care","First"),
    ("medicine","Medicine","A medicine bottle with a cross on the label","Self-care","First"),
    ("bandaid","Plaster","An adhesive plaster","Self-care","Step"),
    ("thermometer","Thermometer","A thermometer","Self-care","Step"),
    ("nosewipe","Wipe nose","A child holding a tissue to their nose","Self-care","Step"),
    ("hairdry","Dry hair","A hairdryer blowing air","Self-care","Step"),
    ("floss","Floss","A reel of dental floss","Self-care","Step"),
    ("comb","Comb hair","A comb","Self-care","Step"),
    ("mirror","Mirror","A hand mirror","Self-care","Step"),
    ("sunscreen","Sunscreen","A bottle of sunscreen with a sun on it","Self-care","Step"),
    ("nails","Cut nails","A hand with nail clippers","Self-care","Step"),
    ("potty","Potty","A child's potty","Self-care","First"),
    ("diaper","Clean nappy","A folded nappy","Self-care","Step"),
    ("mouthwash","Rinse","A bottle of mouthwash","Self-care","Step"),
    ("haircut","Haircut","Scissors and a comb","Self-care","First"),

    ("pants","Trousers","A pair of trousers","Dressing","Step"),
    ("dress","Dress","A dress","Dressing","Step"),
    ("sweater","Jumper","A knitted jumper","Dressing","Step"),
    ("pajamas","Pyjamas","A pyjama top and bottoms","Dressing","Step"),
    ("underwear","Pants on","A pair of underpants","Dressing","Step"),
    ("gloves","Gloves","A pair of gloves","Dressing","Step"),
    ("scarf","Scarf","A scarf around a neck","Dressing","Step"),
    ("boots","Boots","A pair of boots","Dressing","Step"),
    ("sandals","Sandals","A pair of sandals","Dressing","Step"),
    ("zip","Zip up","A zip being pulled closed","Dressing","Step"),
    ("buttons","Buttons","Four buttons","Dressing","Step"),
    ("laces","Tie laces","A shoe with a tied bow","Dressing","Step"),
    ("belt","Belt","A belt with a buckle","Dressing","Step"),
    ("mittens","Mittens","A pair of mittens","Dressing","Step"),

    ("toast","Toast","A slice of toast with butter","Food","Then"),
    ("cereal","Cereal","A bowl of cereal","Food","First"),
    ("milk","Milk","A carton of milk","Food","Then"),
    ("juice","Juice","A juice carton with a straw","Food","Then"),
    ("water","Water","A glass of water","Food","Then"),
    ("yogurt","Yogurt","A pot of yogurt","Food","Then"),
    ("egg","Egg","A fried egg","Food","Then"),
    ("cheese","Cheese","A wedge of cheese","Food","Then"),
    ("pasta","Pasta","A bowl of pasta","Food","First"),
    ("soup","Soup","A bowl of soup, steaming","Food","First"),
    ("carrot","Carrot","A carrot with green tops","Food","Then"),
    ("broccoli","Broccoli","A head of broccoli","Food","Step"),
    ("grapes","Grapes","A bunch of grapes","Food","Then"),
    ("orange","Orange","An orange with a leaf","Food","Then"),
    ("strawberry","Strawberry","A strawberry","Food","Then"),
    ("cookie","Biscuit","A biscuit with chocolate chips","Food","Then"),
    ("icecream","Ice cream","An ice cream in a cone","Food","Then"),
    ("cake","Cake","A slice of cake with a candle","Food","Then"),
    ("pizza","Pizza","A slice of pizza","Food","Then"),
    ("crackers","Crackers","Two crackers","Food","Then"),
    ("spoon","Spoon","A spoon","Food","Step"),
    ("snack","Snack","A snack pot with pieces inside","Food","Then"),

    ("train","Train","A train seen from the side","Transitions","Then"),
    ("bike","Bike","A bicycle","Transitions","Then"),
    ("scooter","Scooter","A kick scooter","Transitions","Then"),
    ("walk","Walk","A child walking","Transitions","Step"),
    ("stroller","Buggy","A child's buggy","Transitions","Step"),
    ("airplane","Aeroplane","An aeroplane","Transitions","Then"),
    ("elevator","Lift","A lift with up and down arrows","Transitions","Step"),
    ("stairs","Stairs","A flight of four steps","Transitions","Step"),
    ("crosswalk","Crossing","A zebra crossing","Transitions","Step"),
    ("seatbelt","Seatbelt","A fastened seatbelt","Transitions","Step"),
    ("key","Keys","A key","Transitions","Step"),
    ("coathook","Coat hooks","Three coat hooks on a rail","Transitions","Step"),
    ("mat","Shoes by door","Two shoes on a doormat","Transitions","Step"),
    ("wait_car","Wait in car","A car with an open hand above it","Transitions","Wait"),

    ("home","Home","A house with a door and a window","Places","Then"),
    ("school","School","A school building with a red roof","Places","First"),
    ("shop","Shop","A shop front with an awning","Places","First"),
    ("park","Park","A tree on grass","Places","Then"),
    ("playground","Playground","A climbing frame","Places","Then"),
    ("doctor","Doctor","A medical bag with a cross","Places","First"),
    ("dentist","Dentist","A tooth being brushed","Places","First"),
    ("restaurant","Restaurant","A knife and fork","Places","First"),
    ("beach","Beach","The sea, sand and a sun umbrella","Places","Then"),
    ("grandma","Grandma","An older woman with glasses","Places","Then"),
    ("carpark","Car park","A car park sign","Places","Step"),
    ("library","Library","Four books standing on a shelf","Places","Then"),
    ("church","Church","A church with a steeple","Places","First"),

    ("trampoline","Trampoline","A trampoline with an arrow bouncing up","Rewards","Then"),
    ("sandbox","Sand pit","A sand pit with a spade","Rewards","Then"),
    ("climbing","Climbing wall","A climbing wall with holds","Rewards","Then"),
    ("seesaw","See-saw","A see-saw","Rewards","Then"),
    ("pool","Swimming","A pool of water with ripples","Rewards","Then"),
    ("puzzle","Puzzle","Two interlocking puzzle pieces","Rewards","Then"),
    ("toycar","Toy car","A small red toy car","Rewards","Then"),
    ("toytrain","Toy train","A toy train with carriages","Rewards","Then"),
    ("doll","Doll","A doll with yellow hair","Rewards","Then"),
    ("teddy","Teddy","A teddy bear","Rewards","Then"),
    ("lego","Bricks","Interlocking building bricks","Rewards","Then"),
    ("drawing","Draw","A drawing on paper with a crayon","Rewards","Then"),
    ("paint","Paint","A paint palette with four colours","Rewards","Then"),
    ("playdough","Play dough","Two rolls of play dough","Rewards","Then"),
    ("stickers","Stickers","Three smiling face stickers","Rewards","Then"),
    ("dance","Dance","A child dancing with arms out","Rewards","Then"),
    ("tv","Television","A television on a stand","Rewards","Then"),
    ("trike","Trike","A tricycle","Rewards","Then"),
    ("balloon","Balloon","A balloon on a string","Rewards","Then"),
    ("kite","Kite","A kite with a tail","Rewards","Then"),
    ("sprinkler","Sprinkler","A garden sprinkler spraying water","Rewards","Then"),
    ("swingtire","Tyre swing","A tyre hanging from a rope","Rewards","Then"),
    ("hopscotch","Hopscotch","Numbered hopscotch squares","Rewards","Then"),
    ("video","Video","A screen with a play button","Rewards","Then"),
    ("sensory","Sensory bin","A bowl with coloured balls","Rewards","Then"),
    ("pet","Pet dog","A dog","Rewards","Then"),
    ("sing","Sing","A child singing into a microphone","Rewards","Then"),

    ("breathe","Breathe","Three widening circles with an arrow up","Regulation","Step"),
    ("squeeze","Squeeze","Two hands pressing a ball","Regulation","Step"),
    ("headphones","Ear defenders","A pair of ear defenders","Regulation","Step"),
    ("quiet","Quiet","A child with a finger to their lips","Regulation","Step"),
    ("break","Break","A green pause symbol","Regulation","Step"),
    ("calmcorner","Calm corner","A cushion in a corner with a calm face","Regulation","Step"),
    ("weighted","Weighted blanket","A folded weighted blanket","Regulation","Step"),
    ("fidget","Fidget","A three-armed fidget spinner","Regulation","Step"),
    ("chew","Chew","A chewable pendant","Regulation","Step"),
    ("timer","Timer","An hourglass, part run through","Regulation","Wait"),
    ("countdown","Time left","A clock face with a filled wedge","Regulation","Wait"),
    ("first","First","A card with the numeral one","Regulation","First"),
    ("then","Then","A card with the numeral two","Regulation","Then"),
    ("choice","Choose","Two cards side by side","Regulation","Choice"),
    ("help","Help","An open hand with a question mark","Regulation","Step"),
    ("more","More","Two hands moving together","Regulation","Step"),
    ("finished","Finished","A white tick in a green circle","Regulation","Step"),
    ("feelings","Feelings","Three faces, happy, sad and flat","Regulation","Step"),
    ("loud","Too loud","A loudspeaker with sound waves","Regulation","Stop"),
    ("light_off","Lights off","A light bulb with a line through it","Regulation","Stop"),

    ("mum","Mum","A woman in a pink top","People","Then"),
    ("dad","Dad","A man in a blue top","People","Then"),
    ("teacher","Teacher","A teacher holding a book","People","First"),
    ("friend","Friend","Two children holding hands","People","Then"),
    ("share","Share","Two hands passing an object","People","Step"),
    ("turntaking","Take turns","A child inside a circling arrow","People","Step"),
    ("hello","Hello","A child waving","People","Step"),
    ("goodbye","Goodbye","A waving hand and an arrow away","People","Step"),
    ("hug","Hug","Two children hugging","People","Then"),
    ("please","Please","An open hand with a heart","People","Step"),
    ("doctor_visit","See doctor","A doctor with a stethoscope","People","First"),

    ("carpet","Carpet time","A rug with children sitting on it","School","First"),
    ("circletime","Circle time","Six children in a circle","School","First"),
    ("recess","Playtime","A swing in the sun","School","Then"),
    ("gym","PE","A set of gym bars","School","First"),
    ("artclass","Art","A painting on an easel","School","Then"),
    ("musicclass","Music class","A keyboard","School","Then"),
    ("handup","Hand up","A child with one hand raised","School","Step"),
    ("listen","Listen","An ear with sound waves","School","Step"),
    ("sit","Sit down","A chair with a child on it","School","Step"),
    ("hallway","Walk in hallway","A corridor with a child walking","School","Step"),
    ("locker","Locker","Three lockers","School","Step"),
    ("lunchbox","Lunchbox","A lunchbox with a handle","School","Step"),
    ("bell","Bell","A school bell","School","Step"),
    ("busline","Bus line","Three children in a row with an arrow","School","Step"),
    ("worksheet","Worksheet","A worksheet with a tick","School","First"),
    ("scissors","Cut","A pair of scissors","School","Step"),
    ("glue","Glue","A glue stick","School","Step"),

    ("morning","Morning","A sun rising over a line","Time","Step"),
    ("night","Night","A crescent moon and stars","Time","Step"),
    ("clock","Clock","A clock face","Time","Wait"),
    ("calendar","Calendar","A calendar page with dated squares","Time","Step"),
    ("twomore","Two more","A large numeral two","Time","Wait"),
    ("last","Last one","Three cards, the last one highlighted","Time","Wait"),
    ("sequence","Next","Three numbered cards with arrows","Time","Step"),
]

ICONS_EXTRA = {n: globals()["i_" + n] for n, *_ in CARDS_EXTRA}
CARDS = CARDS + CARDS_EXTRA
ICONS = dict(ICONS, **ICONS_EXTRA)

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
    cols = 12
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
