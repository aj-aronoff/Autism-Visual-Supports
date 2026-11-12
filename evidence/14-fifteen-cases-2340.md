# The fifteen-case run — 9 November 2026, ~23:40

**The run that characterised questions 13 and 14, confirmed a structural bug, and found a third
category of reward nobody had considered.** Source: `test-cases-v2.json`.

---

## 1. THE HEADLINE: question 14 can be satisfied

**`v1`** — *"We keep it on top of the wardrobe where she cannot reach it, and we only bring it down
after her shoes are on."*

```
REVIEW: pass
Draft saved - the review found nothing to change.
```

**`THEN_ALREADY_AVAILABLE` did not fire.** It had fired on **four boards out of four** before this,
and the open question was whether it was *conditional* or simply *unconditional* — a check that
always fires is noise, not a check.

**It is conditional.** State the storage and the exclusivity and it goes silent. **Question 14 is a
usable check**, and that was the single most important unknown on the page.

### And it generalises without a second branch

**`v2`** — *"It is locked behind my passcode and I only unlock it after her shoes are on."*

`REVIEW: pass`, only an `IMAGE_LABEL_DRIFT` note. **`THEN_ALREADY_AVAILABLE` did not fire for a
digital reward either.** So **a passcode counts as a restriction**, and the physical/digital split
proposed after board 19 is **not needed.** The question asks the right thing in both worlds; only
its *example wording* was physical.

### The counter-case, and it is the sharpest observation of the night

**`v3`** — the Composer wrote *"bring the musical dinosaur from where you keep it"*:

```
THEN_ALREADY_AVAILABLE (must) plan.reinforcement
The plan says to bring the musical dinosaur "from where you keep it" but never says
where that is, so nothing stops the child reaching it.
```

**A `must`, for a phrase that gestures at storage without stating it.** *"From where you keep it"*
is exactly the kind of sentence that looks like compliance and is not, and the Reviewer refused to
accept it. **Note the severity: `should` elsewhere, `must` here** — the Reviewer is choosing
severity per instance rather than per code.

---

## 2. A THIRD CATEGORY OF REWARD: the fixture

Two independent runs surfaced the same idea, and neither prompt mentioned it.

**`r2`**, on the ceiling-hung sensory swing:
> *"A ceiling-hung swing is a fixed fixture the child can use at any time, and the reinforcement
> text does not say the swing is…"*

**`b1`**, on a park swing:
> *"The swing is in plain view and reachable the whole time, so the reward's restriction rests only
> on the adult's word."*

**Some rewards cannot be put away.** A ceiling swing, a park swing, a trampoline, a television in
the living room. **For those, restriction is not storage — it is the adult's word plus a routine**,
and that is a weaker contingency that the plan should acknowledge rather than pretend otherwise.

**This is better than the physical/digital split I proposed.** The real axis is **restrictable by
removal / restrictable by access control / not restrictable at all** — and the third case needs
different advice: *say that the restriction depends on the adult holding the line, and put the
routine in `plan.boardAction`.*

**Phase 2: question 14 needs the third branch, and `prompts/PENDING-FROM-FIRST-TEST-USER.md` needs
updating to match.** The first test user's musical toy is case one; her iPad app is case two; the
swing the school recommended is case three, and it is her child's actual reward.

---

## 3. Question 13 is repeatable

**`r3`**, second run of the motor-planning case:

```
FIRST_NOT_POSSIBLE (must) cards[0].label, plan.boardAction, reasoning
The First is tying shoes, a fine-motor task, and the reasoning itself says tying is
physically hard...
```

**`must` again**, at temperature 1, on a separate run. **Two for two.** That moves it from a single
observation to a finding, and it is the claim the Tech Video rests on.

---

## 4. Both halves of the safety gate are now proven in production

**`f1`** — *"She runs into traffic…"* → the referral text, no board, no debug block.

The 16:33 firing matched **regex** pattern 3 (`hits himself`). This matched a **substring**
(`runs into traffic`). **Two different mechanisms, both exercised**, and until now only one had ever
run.

---

## 5. CONFIRMED BUG: SocialNarrative cannot produce a board

**`b2`** — *"Her grandmother is coming to stay next week…"*

```
No board this time - the draft came back incomplete, so I did not save it. Please try again.
```

**Predicted and confirmed.** `SocialNarrative`'s card range is **(0, 0)**, the parser requires
`cards`, and an empty list trips *"Required field missing"*. **One of four support types cannot be
produced at all**, and it has zero eval coverage because `c5-dentist` was removed on 8 Nov and
nothing replaced it.

**Phase 2, and it is a small fix:** treat an empty `cards` list as valid when
`supportType = SocialNarrative`, and add an eval case so it never regresses silently.

---

## 6. `IMAGE_LABEL_DRIFT` is now the most frequent violation

It fired on `r4`, `v2` and `r5`-adjacent runs, and the catches are good:

- **`r4`:** *"The label is 'Clean room', a place and task, but the imagePrompt depicts only a broom,
  which is a tool and does not show the action."*
- **`v2`:** *"The Then card is labelled 'Drawing app' but its image shows a pencil drawing a line,
  which reads as a pencil activity rather than the app."*

**Both are right, and both describe the same Composer habit: it illustrates a noun adjacent to the
label rather than the label itself.** A broom for *clean room*; a pencil for *drawing app*.

**Phase 2:** the image-prompt rule should say *depict the thing the label names, not a thing
associated with it.* That is one sentence and it would remove the most common violation in the set.

---

## 7. A test-case correction from the developer

> *"Physical Therapy vs Occupational therapy."*

**`r2`'s wording says the sensory swing is used in *physical* therapy. A sensory swing is
occupational-therapy equipment.** The test case should be corrected before it is used again or
quoted anywhere — **a clinician reading the Demo would notice immediately**, and the project's whole
posture is that a clinician can check every claim.

**Also noted:** `r4`'s prompt was simplified between runs, so the disappearance of its false `must`
**cannot be attributed to the obstacle fix.** The clean comparison for that fix is `r2`, which still
shows `THEN_NOT_DELIVERABLE` reasoning from the profile — **so the obstacle may not have reached the
Reviewer yet, and that is still open.**
