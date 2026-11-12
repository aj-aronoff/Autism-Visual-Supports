# The Reviewer's first working verdict — 9 November 2026, 22:03

**The first usable verdict in this project's history.** The Reviewer had never once returned one:
built against the trial model at temperature 0.2, never run, then bound to Bedrock Haiku 5.5 at
~17:00 — which **rejects temperature 0.2 outright.** Every attempt failed with
`litellm.UnsupportedParamsError … Only temperature=1 is supported`. Set to 1 at ~21:55; this is the
next run.

Board 15 saved. Verdict `pass`, two `should` violations, two strengths, `note: null`, valid JSON,
and the tolerant parse was not needed.

---

## What was sent

> My 7 year old does not want to brush her teeth in the morning. She loves dinosaurs. Afterward
> brushing her teeth she likes to use the indoor swing. We bought the OUTREE Sensory Swing for
> Kids&Adult, Indoor Swing with 360° Hanger. This is the swing that the school recommended. It is
> the one that uses during physical Therapy.

**Context from the developer, which matters for judging violation 2:** the swing is real, it was
bought for their daughter, **the school recommended it**, it is the one used in **physical therapy**,
and *"she found it very comforting."*

## The verdict, verbatim

```json
{
"verdict": "pass",
"violations": [
{
"code": "SEQUENCE_NOT_TAUGHT",
"severity": "should",
"where": "cards[0] (First: Brush teeth)",
"problem": "The First is a non-preferred task, and the profile lists EarlyReader language with a Primary developmental stage, so the child may still be learning that the two pictures form a sequence the adult always follows through on.",
"fix": "Consider starting with two preferred activities for the first few sessions so the sequence and follow-through are learned, then introduce brushing as the First once the child reliably checks the board and receives the Then."
},
{
"code": "THEN_NOT_DELIVERABLE",
"severity": "should",
"where": "cards[1] (Then: Swing), plan.reinforcement",
"problem": "The Then assumes an indoor swing the family has, but the profile does not mention one, so the parent may not be able to deliver it within a minute.",
"fix": "Confirm the indoor swing is available in this home and name it in the Then card, or substitute a Then the parent can produce on the spot from what the family already owns."
}
],
"strengths": [
"Removing the First card on completion while leaving the Swing card visible makes the sequence change on the board",
"The prompt hierarchy starts with a visual point and ends with a brief physical guide"
],
"note": null
}
```

---

## What it got right

**The verdict is `pass` with two `should` notes, not a rejection.** That is the design working: the
severity split exists so a parent is not blocked by a matter of taste, and `v2=safety` says only
guardrail 5 blocks. **It reported and did not overrule.**

**The two strengths are real and specific.** *"Removing the First card on completion while leaving
the Swing card visible makes the sequence change on the board"* is an observation about the board's
mechanics, not flattery. A reviewer that only finds faults is one nobody reads.

**And `THEN_NOT_DELIVERABLE` is the right question to ask.** Whether a reward can be produced
within a minute is exactly the kind of judgement a validator cannot make. It asked it, and the
reasoning is sound — it is the *premise* that was wrong.

---

## THE BUG IT EXPOSED, and it is the most valuable thing in this run

> *"The Then assumes an indoor swing the family has, **but the profile does not mention one**."*

**The parent said so, at length.** Brand, that the school recommended it, that it is used in physical
therapy. It is in `request.obstacle`, which was sent to the **Composer** verbatim.

**The Reviewer never saw it.** `BuildReviewerMessages` takes the **profile**, the **draft**, the
**passages text** and the **passage count**. It does **not** take the request.

### What that breaks, measured against the fifteen questions

The Reviewer cannot see the parent's own words, so it cannot answer any question that depends on
them:

- **Q7 `THEN_NOT_DELIVERABLE`** — it guessed from the profile and got it backwards here.
- **Q13 `FIRST_NOT_POSSIBLE`** — needs *"the obstacle describes repeated failure at a task with a
  fine-motor demand."* **The obstacle is the only place that fact can live.**
- **Q14 `THEN_ALREADY_AVAILABLE`** — needs to know whether the child has free access, which a
  parent states in prose and a profile does not record.

**So the three questions the first test user caused, added at 20:40, could never have fired.** Test
cases `n1`–`n4` were written to exercise exactly those, and they would have been meaningless.
**This run caught that before they were run.**

### The fix

Pass `request.obstacle` into `BuildReviewerMessages` and into the Reviewer's user message, labelled
as the parent's own words. **One input, one message section.** The Reviewer is then judging the board
against what was actually asked for, which is what it was always meant to do.

---

## The second violation is an over-flag, and it is a prompt disagreement

`SEQUENCE_NOT_TAUGHT` fired on a child who is **`Primary` / `EarlyReader`** — the second of four
developmental stages and the second of three language levels.

**The Composer's rule 12 applies only at the earliest stage**: *"If developmentalStage is the
earliest stage, or languageLevel is PreVerbal."* `composer.md:188`. And **`Primary` was chosen
deliberately on 9 November** precisely so rule 12 would not fire — because at the earliest stage the
Composer correctly refuses to make a task the child avoids the First, which would break the
teeth→swing board the whole Demo rests on.

**So the Composer and the Reviewer disagree about when sequence-teaching applies.** The Reviewer's
advice is not clinically wrong — it is conservative, and *"start with two preferred activities for
the first few sessions"* is sound — but it contradicts a decision the Composer was told to respect.

**Not urgent, because it is a `should`.** But the two prompts should name the same threshold, and
right now only one of them names a threshold at all.

---

## What this run is worth saying out loud

**The Reviewer's first working verdict found a flaw in its own wiring.** It asked a correct question,
reasoned soundly, reached a wrong conclusion, and the wrongness pointed straight at a missing input
that would have silently broken three of its fifteen questions.

**That is a reviewer earning its place on the first attempt** — and it is a better Tech Video moment
than a clean `pass` would have been.
