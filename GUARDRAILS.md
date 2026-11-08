# The seven guardrails, written and tested

`SPEC.md §6` states the seven in prose and `CODE-PLAN.md §3.2` listed them as
*specified, not written*. **Written 1 November 2026.** Two artefacts:

| File | What it is |
|---|---|
| [`tools/guardrails.py`](tools/guardrails.py) | Reference implementation. Pure functions, no I/O, no model call |
| [`tools/test_guardrails.py`](tools/test_guardrails.py) | **57 table rows across 19 tests. All passing.** Run `python3 tools/test_guardrails.py` |
| [`schema/board.schema.json`](schema/board.schema.json) | The output contract, JSON Schema 2020-12. Rules 1, 3 and 4 are *also* enforced structurally here |
| [`schema/examples/`](schema/examples) | One valid board and three deliberately invalid ones, used as fixtures by both |

**The Python does not ship.** It is the specification that gets reviewed, and the test
table outlives it: on day 5 the logic is ported into ODC server-action flows, and these
57 rows are what the port is checked against. A row is a decision someone can argue
with, which is the point — three of them are decisions A.J. or a clinician should
confirm, and they are marked below.

---

## 1. Where each rule lives

| # | Rule | Schema | Code | Pure function |
|---|---|---|---|---|
| 1 | Three words maximum per label | ✅ `pattern` | ✅ `check_label_length` | yes |
| 2 | Positive phrasing only | — | ✅ `check_positive_phrasing` | yes |
| 3 | First–Then needs a Then card | ✅ `contains` | ✅ `check_then_card` | yes |
| 4 | Card count within the type's range | ✅ `if`/`then` ×4 | ✅ `check_card_count` | yes |
| 5 | No diagnosis, no clinical advice | — | ✅ `check_escalation` | yes |
| 6 | Neurodiversity-affirming language | — | ⚠️ `check_affirming_language` | yes, **term list needs review** |
| 7 | The parent owns and can export everything | — | — | **not a validator**: a screen and a data decision |
| 8 | Prompt hierarchy least-intrusive-first, levels contiguous | partial | ✅ `check_prompt_hierarchy` | yes |

Rule 8 is not one of the seven. It is here because the schema cannot express
contiguity, and a hierarchy that starts at level 2 or opens with `PhysicalGuide` is
clinically wrong in a way no field-level check catches.

Rules 1, 3 and 4 are enforced in **both** places on purpose. A schema rejection is a
validation error in a log; the code version returns a sentence a parent can read.

---

## 2. The three decisions worth arguing with

**A hyphenated compound counts as one word.** `hand-over-hand` is one, `all done` is
two. The alternative — splitting on hyphens — rejects *Hand-over-hand help* at four
words when a parent reads it as two. `CODE-PLAN.md §3.2` named this as the hard part of
rule 1; this is the call, and it is reversible in one line.

**Rule 2 judges negation as a construction, not a word.** A deny-list is what
`CODE-PLAN.md` warned against, and the case that proves it is **`Stop sign`**, which is a
legitimate parameter card, against **`Stop running`**, which is a prohibition. So `stop`
is judged by what follows it: `stop` + gerund fails, `stop` alone or `stop` + noun
passes. Leading `No ` + word fails. Apostrophe-dropped forms (`dont`, `cant`, `wont`)
fail too — a parent types on a phone.

**Rule 5 is deliberately over-inclusive, and that is a clinical decision, not a tuning
one.** A board withheld in error costs a parent one annoying screen. A board offered in
place of referral guidance is the failure this project must not have. So `meltdown`,
`aggressive` and `destroy` all trigger referral even though some parents use them
loosely. **Any term removed from that list needs a clinician, not a developer.**

Rule 5 also **short-circuits**: it returns referral guidance *instead of* a board, never
a board with a warning attached. `check_board` returns at the first escalation hit and
composes nothing. There is a test pinning exactly that behaviour.

And the referral text itself is tested for what it must **not** contain — no `autism`,
no `diagnos`, no `disorder`, no `you should`, no `probably`. It names who to contact and
states that this app does not assess behaviour.

---

## 3. What the table caught that review would not have

Four tests failed on the first run. Three were real defects and one was a wrong
prediction about my own code. All four are worth recording, because they are the argument
for writing the table before the ODC flows.

| What failed | Why it matters |
|---|---|
| **`He bangs his head on the floor` was not detected.** The list contained `head bang`; a parent writes `bangs his head` | The most safety-critical rule in the project had a hole, and it was a word-order hole. Harm is a verb plus a target, so rule 5 now carries four regexes alongside the substrings |
| **The escalation short-circuit test failed** for the same reason | A single root cause showing up twice is what a table gives you that a read-through does not |
| **`Dont run` passed.** `don't` was in the token set; `dont` was not | Apostrophe-dropped contractions are the normal case on a phone keyboard, not the edge case |
| **`He hit the ball at t-ball practice` — I predicted a false positive and was wrong** | The row was written expecting rejection; the implementation excluded `hit the ball` by name and passed it. The table row is now corrected to `PASS`, and the honest version is in the file |

---

## 4. The decision trap, pinned as a test

The shipped OutSystems course exercise contains this:

```
Index(AgentFlow.Response.Decision, "Approved") <> -1
```

**`"Not Approved"` contains `"Approved"`**, so a rejected application reads as approved.
`ODC-AGENT-ANATOMY.md §8` records it; `decision_is()` is the corrected form and there are
three tests on it, including one that *demonstrates the bug* by asserting that the
substring match succeeds.

Two rules follow, and they apply to every agent in this build, not just this one:

1. **Compare a decision for equality, or map it through a static entity.** Never a
   substring test, never `Index(…) <> -1`.
2. **An unrecognised value raises.** `decision_is("Maybe", "Approved")` throws rather
   than falling through to the happy path, and so does a case mismatch. Failing closed on
   a verdict you do not recognise is the whole discipline.

---

## 5. Running them

```bash
python3 tools/test_guardrails.py          # 19 tests, 57 table rows, no dependencies
```

The schema fixtures need `jsonschema`, which is not installed system-wide and cannot be
(PEP 668). Use a throwaway venv:

```bash
python3 -m venv /tmp/sv && /tmp/sv/bin/pip install jsonschema
```

Last run, 1 November 2026: **19 tests OK**, and all four schema fixtures behaved —
the SPEC example accepted, the four-word label, the missing Then card and the invented
evidence practice each rejected with the right error.

---

## 6. What is still open

- **Rule 6's term list needs a human.** `SPEC.md §6` asks for a reviewed list and
  `CODE-PLAN.md §3.2` says explicitly *not a guess*. What is there now is a starting
  list of twelve with suggested replacements, including the identity-first preference
  (`autistic person`, not `person with autism`) — which is a community preference with
  real disagreement in it, and therefore exactly the kind of thing not to settle alone.
- **~~The `evidenceBasis` enum must stay in step with the `EvidencePractice` static
  entity.~~ RESOLVED 7 November 2026 — and it was worse than this note said.** The three
  naming mismatches recorded here were real, but the prompt and the schema also held
  **different sets**: `prompts/composer.md` rule 10 listed `Peer Training` *and*
  `Peer Training Package` as separate entries, so it named only **ten** distinct
  practices, and it **omitted Pivotal Response Treatment** entirely. Every board citing
  one of six abbreviated names would have failed the enum.
  **Settled against the primary source** — the legend under Table 3 of the National
  Standards Report (2009), read from the report itself, not from memory. All three files
  now use those names. The enum holds the **six practices this application can honestly
  claim**; all eleven stay in `EvidencePractice` as the reference table, with a `Citable`
  flag. An item is now `{practice, technique}` and the schema binds the technique to its
  own practice, so *Schedules — token economy* is rejected.
- **No image-prompt check for the child's name.** `SPEC.md §5` requires that prompts say
  *"a child"*. The schema cannot see the profile and the pure functions do not take it,
  so this is a server-action check against `Child.Nickname` at generation time.

---

*First → Then. Print it, post it, trust it.*
