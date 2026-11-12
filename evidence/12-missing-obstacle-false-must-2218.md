# The missing input produces a blocking false positive — 9 Nov 2026, 22:18

**Board 17. `REVIEW: revise`, four violations. Three are right. One is a `must` on a false premise,
and the cause is a known missing input.**

Companion to `11-two-agent-design-justified-2215.md`, which is the same Reviewer getting it right.
**Both runs are needed to describe it honestly.**

---

## What was sent

> We used to motivate my daughter to clean her room, with a toy we kept just for the purpose of
> clean-up. (Clean-up, clean-up, everybody do you share). The old toy is no longer working. **We
> have purchased a new musical dinosaur toy** that we would use, just for this purpose.

## The false positive

```
THEN_NOT_DELIVERABLE | must | plan.reinforcement
problem: "Hand her the new musical dinosaur straight away" requires a new toy, which the
         parent may need to buy, so the Then cannot be guaranteed within sixty seconds at home.
```

**The parent said "we have purchased."** They own it. The Reviewer read the Composer's phrase
*"hand her the **new** musical dinosaur"* and inferred a purchase was pending.

**Cause: `BuildReviewerMessages` does not receive `request.obstacle`.** The Reviewer sees the
profile, the draft, the passages and the count — never the parent's own words. So the word *new*
arrived without *"we have purchased"* beside it.

### This is the second occurrence, and the pattern is diagnostic

| Run | Question | What it doubted | What the parent had said |
|---|---|---|---|
| Board 15, 22:03 | `THEN_NOT_DELIVERABLE` *(should)* | *"the profile does not mention an indoor swing"* | brand, that the school recommended it, used in physical therapy |
| Board 17, 22:18 | `THEN_NOT_DELIVERABLE` **(must)** | *"the parent may need to buy"* | **"We have purchased"** |

**`THEN_NOT_DELIVERABLE` is the question most dependent on the parent's words, and it is the one
that fails without them.** Twice, on the same cause, escalating from `should` to `must`.

**`must` is the severity that blocks Approve.** So the missing input has gone from producing a
cosmetic doubt to producing a **blocking** false refusal.

---

## The three violations that are right

```
THEN_ALREADY_AVAILABLE | should | plan.reinforcement
problem: The plan says to keep the dinosaur "for clean-up only" but never says where it is
         stored, so the parent cannot tell whether it is out of the child's reach.
fix:     State where the reward is kept, for example on a high shelf or in a parent-only
         drawer that she cannot reach, and say that the parent brings it out only after the
         room is clean.
```

**Correct and exactly the first test user's point.** The Composer *did* hear the exclusivity — it
wrote *"for clean-up only"* — and omitted the storage. **Her two conditions, and only one was met.**
Question 14 isolating precisely the half that was missing is the clearest demonstration of that
question working.

```
IMAGE_LABEL_DRIFT | should | cards[1].imagePrompt
problem: The label "Clean room" is paired with an image of an empty toy basket, which shows
         an object rather than the action the label names.
```

**Correct**, and a pre-existing question earning its keep. A child matching a picture to a label
needs them to name the same thing.

```
NOUN_MISMATCH | should | cards[2].label and script.Before
problem: The card reads "Musical dinosaur" but the script says "dinosaur", and the picture
         shows a plain toy dinosaur with no music cue.
```

**Correct — and this is the SECOND time**, after board 16. **So it is a repeatable Composer defect,
not a one-off:** the Composer writes a two-word Then on the card and the bare noun in the script.
Rule 2 of the prompt is about the script and the card naming the same thing, and the Composer is
breaking it consistently. **Worth a Phase 2 note of its own.**

---

## A smaller inconsistency, for anyone parsing `where`

Board 16 used `cards[0]` and `cards[1]`. Board 17 used `cards[1]` and `cards[2]` — on a board with
**two** cards. **The Reviewer is inconsistent about whether card indices are 0-based or 1-based**, so
the `where` field is reliable for a human and **not parseable by code.** Fine as it stands; it would
matter if a screen ever highlighted the offending card.

---

## Retrieval, measured, and the best layout scores yet

```
[Layout]  0.417  0.373  0.352     PASSED   <- highest of the night
[Evidence] 0.737  0.716  0.706    PASSED   <- identical every run, as designed
```

Chunks **16**, **15** and **8** came back — including *"When is it helpful? Visually setting
parameters is helpful in communicating limits…"*, which is genuinely the right passage for a
clean-up boundary. **Retrieval is responding to meaning, not matching keywords**, and the floor of
0.25 was nowhere near binding here.

Compare board 16's terse request: 0.3 / 0.244 / 0.234, two rejected. **A richer request retrieves
better.** That is worth knowing and it is the opposite of what a keyword system would do.

---

## The fix, and why it is worth doing before any recorded verdict

Pass `request.obstacle` into `BuildReviewerMessages` and into the Reviewer's user message, labelled
as the parent's own words. **One input, one message section.**

**Without it, three of the fifteen questions are guessing** — Q7 about what the family has, Q13 about
what the child can do, Q14 about free access — and two of those are the first test user's. They have
fired correctly anyway, because the Composer records faithfully in `reasoning`, **but that is luck
and board 17 is what luck looks like when it runs out.**
