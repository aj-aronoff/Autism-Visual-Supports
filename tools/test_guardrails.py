"""The guardrail test table. Run: python3 tools/test_guardrails.py

Table-driven on purpose. The table, not the Python, is the deliverable: it is what the
ODC server-action flows are checked against on day 5, and what a clinician reviews.
Each row is (input, expected verdict, why this row exists).
"""
import unittest
from guardrails import (
    check_label_length, check_positive_phrasing, check_then_card, check_card_count,
    check_escalation, check_affirming_language,
    check_figurative_language, check_prompt_hierarchy,
    decision_is, check_board, words,
)

PASS, FAIL = True, False


class Rule1Labels(unittest.TestCase):
    TABLE = [
        ("Swing",                PASS, "one word, the common case"),
        ("Put on shoes",         PASS, "exactly three, the boundary"),
        ("Brush your top teeth", FAIL, "four words, the drift the Reviewer must catch"),
        ("Hand-over-hand help",  PASS, "hyphenated compound counts as one word"),
        ("All done",             PASS, "two words, not one -- the decision in words()"),
        ("",                     FAIL, "empty label is not a card"),
        ("   ",                  FAIL, "whitespace only"),
    ]

    def test_table(self):
        for text, expected, why in self.TABLE:
            with self.subTest(text=text, why=why):
                self.assertEqual(bool(check_label_length(text)), expected, why)

    def test_hyphen_decision_is_explicit(self):
        self.assertEqual(words("hand-over-hand"), ["hand-over-hand"])
        self.assertEqual(words("all done"), ["all", "done"])


class Rule2Positive(unittest.TestCase):
    TABLE = [
        ("Walk",                 PASS, "the replacement the rule exists to produce"),
        ("Don't run",            FAIL, "the canonical negative"),
        ("Do not run",           FAIL, "spelled out, same meaning"),
        ("Dont run",             FAIL, "apostrophe dropped -- must still fail"),
        ("Don’t run",       FAIL, "curly apostrophe -- normalisation matters"),
        ("No hitting",           FAIL, "leading No plus gerund"),
        ("No more tablet",       FAIL, "says what stops, not what comes next"),
        ("Stop sign",            PASS, "THE case a deny-list gets wrong: a legitimate card"),
        ("Stop",                 PASS, "a Stop parameter card is a real card"),
        ("Stop running",         FAIL, "stop plus gerund is a prohibition"),
        ("Never touch",          FAIL, "never is a negation"),
        ("Shoes first",          PASS, "the IfRefusal phrase from SPEC section 5"),
        ("Now swing!",           PASS, "OnCompletion phrase, exclamation is fine"),
        ("Knotted lace",         PASS, "contains 'not' inside a word -- must NOT fail"),
        ("Cannot wait",          FAIL, "cannot is a negation"),
        ("Wait",                 PASS, "a Wait parameter card"),
    ]

    def test_table(self):
        for text, expected, why in self.TABLE:
            with self.subTest(text=text, why=why):
                self.assertEqual(bool(check_positive_phrasing(text)), expected, why)


class Rule3ThenCard(unittest.TestCase):
    TABLE = [
        ("FirstThenBoard", ["First", "Then"], PASS, "the valid board"),
        ("FirstThenBoard", ["First", "Step"], FAIL, "no Then card: the reward is structural"),
        ("FirstThenBoard", ["Then", "First"], PASS, "order is sequenceNo's job, not this rule's"),
        ("FirstThenBoard", ["Step", "Step"],  FAIL, "neither First nor Then"),
        ("VisualSchedule", ["Step", "Step", "Step", "Step"], PASS, "rule does not apply"),
    ]

    def test_table(self):
        for st, roles, expected, why in self.TABLE:
            with self.subTest(st=st, roles=roles, why=why):
                self.assertEqual(bool(check_then_card(st, roles)), expected, why)


class Rule4CardCount(unittest.TestCase):
    TABLE = [
        ("FirstThenBoard", 2,  PASS, "exactly two"),
        ("FirstThenBoard", 3,  FAIL, "a third card is not a First-Then board"),
        ("FirstThenBoard", 1,  FAIL, "one card is a prompt, not a board"),
        ("VisualSchedule", 4,  PASS, "lower bound"),
        ("VisualSchedule", 8,  PASS, "upper bound"),
        ("VisualSchedule", 12, FAIL, "the SPEC section 6 example: thoroughness as failure"),
        ("VisualSchedule", 3,  FAIL, "below the range"),
        ("ParameterCards", 1,  PASS, "a single Wait card is valid"),
        ("ParameterCards", 4,  FAIL, "above the range"),
        ("SocialNarrative", 0, PASS, "no cards by design"),
        ("ChoiceBoard",    2,  FAIL, "unknown type fails closed, it does not default"),
    ]

    def test_table(self):
        for st, n, expected, why in self.TABLE:
            with self.subTest(st=st, n=n, why=why):
                self.assertEqual(bool(check_card_count(st, n)), expected, why)


class Rule5Escalation(unittest.TestCase):
    """The only rule with a safety cost if it is wrong. Over-inclusive on purpose."""

    TABLE = [
        ("He refuses to put his shoes on and we are late",     PASS, "the core use case must not be blocked"),
        ("She will not brush her teeth",                       PASS, "ordinary refusal"),
        ("He bangs his head on the floor when we leave",       FAIL, "self-injury"),
        ("She bites me when I take the tablet away",           FAIL, "aggression toward a caregiver"),
        ("He hits himself",                                    FAIL, "self-injury, short form"),
        ("He has a meltdown every morning",                    FAIL, "escalation language, deliberately caught"),
        ("He runs into traffic",                               FAIL, "elopement with immediate danger"),
        ("She says she wants to die",                          FAIL, "must route to a human, always"),
        ("He is aggressive at school",                         FAIL, "aggression stem"),
        ("He hit the ball at t-ball practice",                 PASS, "a predicted false positive that did NOT occur -- 'hit the ball' is excluded by name"),
        ("He hits his sister when she takes the tablet",        FAIL, "harm to a sibling, the target that is neither 'me' nor self"),
        ("He bangs his head on the floor",                      FAIL, "the exact phrasing a parent writes; substrings alone missed this"),
        ("",                                                   PASS, "empty obstacle is not an escalation"),
    ]

    def test_table(self):
        for text, expected, why in self.TABLE:
            with self.subTest(text=text, why=why):
                self.assertEqual(bool(check_escalation(text)), expected, why)

    def test_referral_text_never_diagnoses(self):
        v = check_escalation("he bangs his head")
        for banned in ("autism", "diagnos", "disorder", "you should", "probably"):
            self.assertNotIn(banned, v.reason.lower(), f"referral text must not say {banned!r}")


class Rule6Affirming(unittest.TestCase):
    TABLE = [
        ("First shoes, then swing",       PASS, "the ordinary title"),
        ("Help for my high-functioning son", FAIL, "functioning labels"),
        ("He suffers from autism",        FAIL, "suffers from"),
        ("A board for an autistic child",  PASS, "identity-first is the preferred form"),
        ("Like a normal child",           FAIL, "normal as the comparison"),
    ]

    def test_table(self):
        for text, expected, why in self.TABLE:
            with self.subTest(text=text, why=why):
                self.assertEqual(bool(check_affirming_language(text)), expected, why)


class Rule11Figurative(unittest.TestCase):
    """Ported 7 Nov 2026 from the other session's AGENT-1 principle 5.

    Rule 2 forbids negative phrasing and rule 6 forbids non-affirming phrasing.
    NEITHER forbids figurative phrasing, which is how "the doctor will take a peek"
    reached a child's script unflagged. A literal reading of that sentence is a
    reasonable reading, and the refusal it earns gets read back as defiance.
    """

    TABLE = [
        ("First shoes, then swing",                PASS, "the ordinary board, untouched"),
        ("The doctor will look in your ears",      PASS, "the literal rewrite must survive"),
        ("The doctor will take a peek",            FAIL, "the canonical example"),
        ("Hold your horses",                       FAIL, "idiom for wait"),
        ("We are leaving in a minute",             FAIL, "a number of minutes, or the child times it"),
        ("You are being such a big boy",           FAIL, "praise that is really surprise, and figurative"),
        ("Give me a hand with the blocks",         FAIL, "asks for a body part"),
        ("Brush teeth",                            PASS, "two-word label"),
        ("Put the blocks in the box",              PASS, "concrete, literal, unambiguous"),
        ("Cat got your tongue?",                   FAIL, "never use this one"),
    ]

    def test_table(self):
        for text, expected, why in self.TABLE:
            with self.subTest(text=text, why=why):
                self.assertEqual(bool(check_figurative_language(text)), expected, why)

    def test_reason_names_the_replacement(self):
        """A flag the Composer cannot act on is a flag it will reproduce."""
        v = check_figurative_language("The doctor will take a peek")
        self.assertFalse(bool(v))
        self.assertIn("take a peek", v.reason)
        self.assertIn("look at", v.reason)


class Rule8Hierarchy(unittest.TestCase):
    GOOD = [{"level": 1, "kind": "VisualPoint", "instruction": "Point."},
            {"level": 2, "kind": "Gesture", "instruction": "Hold out."},
            {"level": 3, "kind": "Verbal", "instruction": "Say it."},
            {"level": 4, "kind": "PhysicalGuide", "instruction": "Guide."}]

    def test_good(self):
        self.assertTrue(check_prompt_hierarchy(self.GOOD))

    def test_must_start_at_one(self):
        bad = [dict(s, level=s["level"] + 1) for s in self.GOOD]
        self.assertFalse(check_prompt_hierarchy(bad), "levels starting at 2")

    def test_must_be_least_intrusive_first(self):
        bad = list(reversed(self.GOOD))
        for i, s in enumerate(bad, 1):
            s["level"] = i
        self.assertFalse(check_prompt_hierarchy(bad), "PhysicalGuide first is clinically wrong")

    def test_single_level_is_not_a_hierarchy(self):
        self.assertFalse(check_prompt_hierarchy(self.GOOD[:1]))


class DecisionTrap(unittest.TestCase):
    """The bug the shipped course exercise contains, pinned as a test."""

    def test_not_approved_is_not_approved(self):
        self.assertFalse(decision_is("Not Approved", "Approved"))
        self.assertTrue(decision_is("Not Approved", "NotApproved"))

    def test_the_substring_version_would_have_passed(self):
        # This is the exercise's logic. It is here to show the failure, not to use it.
        self.assertNotEqual("Not Approved".find("Approved"), -1,
                            "substring test matches, which is exactly the bug")

    def test_unknown_value_raises_rather_than_defaulting(self):
        with self.assertRaises(ValueError):
            decision_is("Maybe", "Approved")
        with self.assertRaises(ValueError):
            decision_is("Approved", "approved")


class WholeBoard(unittest.TestCase):
    import json as _json
    import os as _os
    ROOT = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "schema", "examples")

    def _load(self, name):
        import json
        with open(__import__("os").path.join(self.ROOT, name), encoding="utf-8") as fh:
            return json.load(fh)

    def test_spec_example_passes_every_guardrail(self):
        failures = check_board(self._load("first-then-shoes-swing.json"),
                               "He refuses to put his shoes on and we are late")
        self.assertEqual(failures, [], f"the SPEC example must pass: {failures}")

    def test_missing_then_card_is_caught(self):
        failures = check_board(self._load("INVALID-no-then-card.json"), "shoes")
        self.assertIn("3", [f.rule for f in failures])

    def test_four_word_label_is_caught(self):
        failures = check_board(self._load("INVALID-four-word-label.json"), "teeth")
        self.assertIn("1", [f.rule for f in failures])

    def test_escalation_short_circuits_instead_of_filtering(self):
        failures = check_board(self._load("first-then-shoes-swing.json"),
                               "he bangs his head when we leave")
        self.assertEqual(len(failures), 1, "rule 5 returns referral INSTEAD OF a board")
        self.assertEqual(failures[0].rule, "5")


if __name__ == "__main__":
    unittest.main(verbosity=2)
