# The grounding check fired on a board that retrieved successfully — 10 Nov 2026, 21:24

**Board 70. `REVIEW: pass`, one note: `NO_GROUNDING (should)`.**

This is the first time `NO_GROUNDING` has fired in production, and it is the claim the
Tech Video makes about why there are two checks instead of one.

---

## What was sent

> My daughter does not like loud noises. We would give her noise canceling headphones,
> when there are loud noises. We keep it in her "go bag" it is always with us when we
> are outside. We would only give it to her, when there are loud noises.

Retrieval succeeded. Rule 17 did not fire — passages came back from both knowledge
bases, so the code gate had nothing to object to and the board composed normally.

## What the Reviewer said, verbatim

```
NO_GROUNDING (should) evidenceBasis[1]: The practice 'Schedules' with the technique
'pictures or photographs' does not appear as a practice in any retrieved passage.
'Schedules' occurs only inside a combined example in the Behavioral Package text,
and nothing retrieved supports pictures as its technique.
```

## Why this one matters more than the other fourteen

**The code gate and the model gate catch different failures, and until tonight only the
code gate had ever fired.** The split is written into `VIDEO-SCRIPTS.md` as:

> Code catches "nothing came back". Only the model can judge "passages came back and
> none of them support the practice I want".

`evidence/02` is the first half, from 9 November 16:36 — zero passages, no board, no
model call. **This is the second half.** Six passages came back, the board named two
practices, and **one of them was not in any of them.** No count, no threshold and no
schema `enum` can see that: `Schedules` is a legitimate value in the six-value enum,
so the schema is satisfied; the citation list is non-empty, so the citation audit is
satisfied. The only thing that can notice is something that reads the passages and the
claim together.

**And the reasoning is checkable, which is what makes it worth keeping.** It does not
say "I could not find it" — it says where `Schedules` *did* appear (inside a combined
example in the Behavioral Package text) and what was missing (nothing supporting
pictures as its technique). That is a reading of the retrieved text, not a guess.

## What this does NOT prove

- **One observation.** The Reviewer runs at temperature 1, forced, because Bedrock
  Haiku 5.5 rejects 0.2. Boards 61 and 62 came from an identical message and returned
  different results. **Do not describe this as a rate or as reliable detection.**
- **It did not block anything.** `NO_GROUNDING` came back at `should`, so the verdict
  stayed `pass` and the board is approvable with the ungrounded practice still in it.
- It is not known whether the Composer would have made the same mistake on a re-run.

## The calibration question it raises, recorded and NOT acted on

**Should `NO_GROUNDING` be a `must`?** The project's central claim is that every board
names the practice it used and cites the passage it rests on. A `should` means a board
whose evidence claim is unsupported can still be approved. Against that: the Reviewer
reports and does not overrule a parent (`v2=safety`), and raising a severity is a
prompt change — which is not a change to make on the last build night, because it
would invalidate the passing runs the Demo is recorded against.

**Phase 2. Decide it with a clear head, not at midnight.**

## Two other boards from the same ten minutes

- **Board 71** — asked for a teeth board with a musical toothbrush, and the Composer
  invented **story time** as the Then. The Reviewer caught the storage gap rather than
  the invention: *"says when story time starts but not where the story book is kept."*
- **Board 72** — `IMAGE_LABEL_DRIFT`, the Then card labelled "Reward from shelf" while
  the picture showed a generic gift box, and `PLAN_NOT_ACTIONABLE` because level 2
  **relied on a musical toothbrush the profile does not say the family owns.** That
  second one is the Reviewer cross-checking the plan against the child profile, which
  is a different source from the passages and from the draft.

Source: test app transcript, 10 November 2026, 21:24–21:34.
