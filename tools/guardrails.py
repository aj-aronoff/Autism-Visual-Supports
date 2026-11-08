"""Reference implementation of the seven guardrails in SPEC.md section 6.

This file does not ship. It is the specification that gets reviewed, and the test
table in test_guardrails.py outlives it: the logic is ported into ODC server-action
flows on day 5, and these cases are what the port is checked against.

Every function is pure -- text in, verdict out, no I/O, no model call -- so it can be
tested on a table and read by a clinician. Rule 3 and rule 4 also exist structurally in
schema/board.schema.json; they are here as well because a schema rejection arrives as a
validation error, while these return a reason a parent could read.

Rule 7 (the parent owns and can export everything) is a screen and a data decision, not
a validator, so it has no function here.
"""

from __future__ import annotations
import re
import unicodedata

# ---------------------------------------------------------------- shared helpers

APOSTROPHES = "’ʼ´`"


def _norm(text: str) -> str:
    """Lower-case, normalise curly apostrophes, collapse whitespace."""
    t = unicodedata.normalize("NFKC", text or "")
    for ch in APOSTROPHES:
        t = t.replace(ch, "'")
    return re.sub(r"\s+", " ", t).strip().lower()


def words(text: str) -> list[str]:
    """Space-separated tokens. A hyphenated compound is ONE word.

    Decision, 1 Nov 2026: 'hand-over-hand' is one word and 'all done' is two. The
    alternative -- splitting on hyphens -- would reject 'Hand-over-hand help' at four
    words, when a parent reads it as two. CODE-PLAN.md section 3.2 names this as the
    hard part of rule 1.
    """
    return [w for w in re.split(r"\s+", (text or "").strip()) if w]


class Verdict:
    """A guardrail result. `ok` is the decision; `reason` is shown to the parent."""

    __slots__ = ("ok", "rule", "reason")

    def __init__(self, ok: bool, rule: str, reason: str = ""):
        self.ok, self.rule, self.reason = ok, rule, reason

    def __repr__(self) -> str:
        return f"Verdict({'ok' if self.ok else 'REJECT'}, {self.rule}, {self.reason!r})"

    def __bool__(self) -> bool:
        return self.ok


# ---------------------------------------------------------------- rule 1

MAX_LABEL_WORDS = 3


def check_label_length(label: str) -> Verdict:
    """RULE 1 -- three words maximum per card label."""
    n = len(words(label))
    if n == 0:
        return Verdict(False, "1", "A card label cannot be empty.")
    if n > MAX_LABEL_WORDS:
        return Verdict(False, "1", f"{n} words; a card label is at most {MAX_LABEL_WORDS}.")
    return Verdict(True, "1")


# ---------------------------------------------------------------- rule 2

# Negation is a construction, not a word list. "Stop sign" is a legitimate parameter
# card; "Stop running" tells the child what not to do. So `stop` is judged by what
# follows it, and the blunt deny-list CODE-PLAN.md warns about is avoided.
_NEG_TOKENS = {
    "not", "n't", "never", "cannot", "without", "quit",
    "can't", "don't", "doesn't", "won't", "shouldn't", "mustn't", "isn't", "didn't",
    # Apostrophe-dropped forms. A parent typing on a phone writes "Dont run", and the
    # test table caught that the contracted forms alone let it through.
    "cant", "dont", "doesnt", "wont", "shouldnt", "mustnt", "isnt", "didnt", "aint",
}
_NEG_LEADING_NO = re.compile(r"^no\s+\w")
_STOP_GERUND = re.compile(r"\bstop\s+\w+ing\b")
_NO_MORE = re.compile(r"\bno more\b")


def check_positive_phrasing(text: str) -> Verdict:
    """RULE 2 -- positive phrasing only. 'Don't run' is refused in favour of 'Walk'."""
    t = _norm(text)
    if not t:
        return Verdict(False, "2", "Empty text cannot be checked.")
    if _NO_MORE.search(t):
        return Verdict(False, "2", "Says what stops, not what to do. Name the next activity instead.")
    if _NEG_LEADING_NO.match(t):
        return Verdict(False, "2", "Starts with 'No'. Say what to do instead.")
    if _STOP_GERUND.search(t):
        return Verdict(False, "2", "Tells the child what to stop. Name the wanted action instead.")
    toks = re.findall(r"[a-z']+", t)
    hit = next((w for w in toks if w in _NEG_TOKENS), None)
    if hit:
        return Verdict(False, "2", f"Negative phrasing ('{hit}'). Say what to do instead.")
    return Verdict(True, "2")


# ---------------------------------------------------------------- rules 3 and 4

CARD_RANGE = {
    "FirstThenBoard": (2, 2),
    "VisualSchedule": (4, 8),
    "ParameterCards": (1, 3),
    "SocialNarrative": (0, 0),
}


def check_then_card(support_type: str, roles: list[str]) -> Verdict:
    """RULE 3 -- a First-Then board cannot save without a Then card."""
    if support_type != "FirstThenBoard":
        return Verdict(True, "3")
    if "Then" not in roles:
        return Verdict(False, "3", "A First-Then board needs a Then card. The reward is the structure.")
    if "First" not in roles:
        return Verdict(False, "3", "A First-Then board needs a First card.")
    return Verdict(True, "3")


def check_card_count(support_type: str, count: int) -> Verdict:
    """RULE 4 -- card count within the type's range (SPEC.md section 2)."""
    if support_type not in CARD_RANGE:
        return Verdict(False, "4", f"Unknown support type {support_type!r}.")
    lo, hi = CARD_RANGE[support_type]
    if not lo <= count <= hi:
        span = f"{lo}" if lo == hi else f"{lo}-{hi}"
        return Verdict(False, "4", f"{count} cards; a {support_type} takes {span}.")
    return Verdict(True, "4")


# ---------------------------------------------------------------- rule 5

# THE ONLY RULE WITH A SAFETY COST IF IT IS WRONG. It is deliberately over-inclusive:
# a board withheld in error costs a parent one annoying screen, while a board offered
# in place of referral guidance is the failure this project must not have. Any term
# removed from this list is a clinical decision, not a tuning decision.
_ESCALATION = [
    "self-injur", "self injur", "self-harm", "self harm", "headbang",
    "suicid", "wants to die", "strangl", "chok", "bleed", "blood", "bruis",
    "runs into traffic", "ran into traffic", "runs into the road", "elope",
    "aggressi", "violent", "violence", "meltdown", "destroy", "threaten",
]

# Substrings alone are not enough, and the test table proved it: the list above had
# "head bang" in it and the obstacle a parent actually writes is "he bangs his head on
# the floor". Harm is a verb plus a target, so these are patterns, not phrases.
_ESCALATION_RE = [
    re.compile(r"\bbang\w*\s+(?:his|her|their|my|the)\s+head\b"),
    re.compile(r"\bhead\s+bang\w*"),
    re.compile(r"\b(?:hit|hits|hitting|punch\w*|slap\w*|bite|bites|biting|scratch\w*|"
               r"hurt|hurts|hurting)\s+(?:him|her|them)sel(?:f|ves)\b"),
    re.compile(r"\b(?:hit|hits|hitting|bite|bites|biting|kick|kicks|kicking|"
               r"scratch|scratches|scratching|punch|punches|punching)\s+"
               r"(?:me|us|his|her|their|the)\b(?!\s*(?:ball|drum|keys|button|wall))"),
]
REFERRAL_TEXT = (
    "This describes something that needs a person, not a picture. Please contact your "
    "child's pediatrician, your BCBA or clinician, or your local crisis line. "
    "This app makes visual supports; it does not assess behavior and never gives "
    "clinical advice."
)


def check_escalation(obstacle_text: str) -> Verdict:
    """RULE 5 -- no diagnosis, no clinical advice.

    A hit surfaces referral guidance INSTEAD OF a board. The caller must branch on the
    verdict before composing, not filter the board afterwards.
    """
    t = _norm(obstacle_text)
    if any(term in t for term in _ESCALATION):
        return Verdict(False, "5", REFERRAL_TEXT)
    if any(rx.search(t) for rx in _ESCALATION_RE):
        return Verdict(False, "5", REFERRAL_TEXT)
    return Verdict(True, "5")


# ---------------------------------------------------------------- rule 6

# NEEDS A HUMAN REVIEWER BEFORE IT SHIPS. This is a starting list with suggested
# replacements, not a finished one; SPEC.md section 6 calls for a reviewed term list
# and CODE-PLAN.md section 3.2 says explicitly "not a guess".
_NON_AFFIRMING = {
    "high-functioning": "name the support the child needs instead",
    "low-functioning": "name the support the child needs instead",
    "suffers from": "is autistic / has",
    "afflicted": "is autistic",
    "cure": "support",
    "normal child": "non-autistic child",
    "normal kid": "non-autistic child",
    "special needs": "disabled, or name the specific need",
    "retard": "never use this word",
    "a victim of": "is autistic",
    "burden": "describe the practical difficulty instead",
    "person with autism": "autistic person (identity-first is the community preference)",
}


def check_affirming_language(text: str) -> Verdict:
    """RULE 6 -- neurodiversity-affirming language."""
    t = _norm(text)
    for term, better in _NON_AFFIRMING.items():
        if term in t:
            return Verdict(False, "6", f"'{term}' -> {better}.")
    return Verdict(True, "6")


# ---------------------------------------------------------------- rule 11

# PORTED 7 November 2026 from prompts/AGENT-1-IF-THEN-ARCHITECT.md principle 5, which
# the other session got right and this project did not have. Rule 2 forbids NEGATIVE
# phrasing and rule 6 forbids NON-AFFIRMING phrasing; neither forbids FIGURATIVE
# phrasing, and a literal reading of an idiom is one of the most ordinary ways a script
# fails an autistic child. "The doctor will take a peek" earns a refusal the adult then
# reads as defiance.
#
# Deliberately a SHORT list of idioms that actually turn up in parenting talk, not a
# general idiom dictionary. A false positive here costs a regenerate; the Reviewer's
# question 12 carries the judgement calls this cannot.
_FIGURATIVE = {
    "take a peek": "look at",
    "have a look-see": "look at",
    "piece of cake": "easy",
    "hold your horses": "wait",
    "hang on a sec": "wait",
    "in a minute": "say the actual number of minutes",
    "under the weather": "unwell",
    "butterflies in": "a funny feeling in",
    "break a leg": "good luck",
    "spill the beans": "tell",
    "hit the road": "go",
    "hop in": "get in",
    "jump in the": "get in the",
    "a little birdie": "someone",
    "cat got your tongue": "never use this",
    "pull yourself together": "never use this",
    "keep your chin up": "never use this",
    "big boy": "name the action instead",
    "big girl": "name the action instead",
    "all ears": "listening",
    "give me a hand": "help me",
    "in two shakes": "very soon",
    "on cloud nine": "very happy",
    "wrap it up": "finish",
    "time flies": "never use this",
}


def check_figurative_language(text: str) -> Verdict:
    """RULE 11 -- literal language only.

    Applies to anything the CHILD hears or reads: card labels, script phrases, story
    text. It does NOT apply to the parent-facing plan, where idiom is harmless -- the
    caller decides what to pass.
    """
    t = _norm(text)
    for phrase, better in _FIGURATIVE.items():
        if phrase in t:
            return Verdict(False, "11", f"'{phrase}' is figurative -> {better}.")
    return Verdict(True, "11")


# ---------------------------------------------------------------- rule 8 (structural)

PROMPT_ORDER = ["VisualPoint", "Gesture", "Verbal", "Model", "PhysicalGuide"]


def check_prompt_hierarchy(steps: list[dict]) -> Verdict:
    """Least intrusive first, levels starting at 1 and contiguous.

    Not one of the seven in SPEC.md section 6; it is here because the schema cannot
    express contiguity, and a hierarchy that starts at level 2 or jumps straight to
    PhysicalGuide is clinically wrong in a way no field-level check would catch.
    """
    if len(steps) < 2:
        return Verdict(False, "8", "A prompt hierarchy needs at least two levels.")
    levels = [s.get("level") for s in steps]
    if levels != list(range(1, len(levels) + 1)):
        return Verdict(False, "8", f"Levels must be 1..{len(levels)} in order; got {levels}.")
    ranks = [PROMPT_ORDER.index(s["kind"]) for s in steps if s.get("kind") in PROMPT_ORDER]
    if len(ranks) != len(steps):
        bad = [s.get("kind") for s in steps if s.get("kind") not in PROMPT_ORDER]
        return Verdict(False, "8", f"Unknown prompt kind(s): {bad}.")
    if any(b <= a for a, b in zip(ranks, ranks[1:])):
        return Verdict(False, "8", "Prompts must go least intrusive to most intrusive.")
    return Verdict(True, "8")


# ---------------------------------------------------------------- the decision trap

APPROVAL_VALUES = {"Approved", "NotApproved", "NeedsReview"}


def decision_is(decision: str, expected: str) -> bool:
    """Compare a model's verdict for EQUALITY, never by substring.

    The shipped OutSystems course exercise gets this wrong:

        Index(AgentFlow.Response.Decision, "Approved") <> -1

    'Not Approved' contains 'Approved', so a rejected application is read as approved.
    In ODC this becomes an equality test against a static entity, and an unrecognised
    value raises rather than silently falling through to the happy path.
    """
    if expected not in APPROVAL_VALUES:
        raise ValueError(f"{expected!r} is not a known decision value")
    d = (decision or "").replace(" ", "")
    if d not in APPROVAL_VALUES:
        raise ValueError(f"unrecognised decision {decision!r} -- fail closed, do not default")
    return d == expected


# ---------------------------------------------------------------- the board gate

def check_board(board: dict, obstacle_text: str = "") -> list[Verdict]:
    """Every guardrail over one board. Returns only the failures, in rule order."""
    out: list[Verdict] = []
    st = board.get("supportType", "")
    cards = board.get("cards", []) or []

    esc = check_escalation(obstacle_text)
    if not esc:
        return [esc]  # rule 5 short-circuits: referral INSTEAD OF a board

    for c in cards:
        for v in (check_label_length(c.get("label", "")),
                  check_positive_phrasing(c.get("label", ""))):
            if not v:
                out.append(Verdict(v.ok, v.rule, f"card {c.get('sequenceNo','?')}: {v.reason}"))

    for line in board.get("script", []) or []:
        v = check_positive_phrasing(line.get("phrase", ""))
        if not v:
            out.append(Verdict(v.ok, v.rule, f"script/{line.get('phase','?')}: {v.reason}"))

    for v in (check_then_card(st, [c.get("role") for c in cards]),
              check_card_count(st, len(cards)),
              check_affirming_language(board.get("title", "")),
              check_prompt_hierarchy((board.get("plan") or {}).get("promptHierarchy", []))):
        if not v:
            out.append(v)

    return out
