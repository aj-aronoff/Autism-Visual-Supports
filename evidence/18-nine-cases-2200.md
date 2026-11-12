# Nine cases in twelve minutes — 10 November 2026, 21:57–22:08

Boards 73 to 79, run against the same `BoardId: 71` context. Three results here change
what can honestly be claimed; the rest are routine passes.

---

## 1. Question 13 has now fired THREE times, on the same case

**Board 76**, from the original 22:15 wording sent again, unchanged:

> My daughter cannot physically tie her shoes. How can I motivate her to do it in the
> morning? She has a favorite musical dinosaur toy that we would use for motivation

```
FIRST_NOT_POSSIBLE (must) cards[0].label, reasoning, plan.generalization
```

**This is the third observation, and the reasoning is stricter than the first two.** It
no longer only objects that the task is impossible — it objects that the Composer's
*justification* is unsupported: *"The reasoning asserts she can fasten wide straps
without laces, but the profile does not establish this, and the original goal of tying
is not carried into plan.generalization."*

That is the Reviewer checking a claim against the **child profile**, a source that is
neither the draft nor the retrieved passages. `evidence/11` and `evidence/13` are the
first two firings. **Three observations at temperature 1 is still not a rate.**

## 2. Question 14 fired at `must` for the first time

**Board 77**, the clean-up-the-room case:

```
THEN_ALREADY_AVAILABLE (must) plan.reinforcement: The reinforcement field says the
dinosaur is 'kept only for this' but does not say WHERE it is stored, so the child may
be able to reach it at any time, including in the bedroom where the board is placed.
```

Every previous firing of question 14 was `should`. **This one blocked**, and the reason
it blocked is precise: the parent said the toy was reserved, and the Reviewer accepted
that *reserved* is not *out of reach* — the distinction the first test user drew at
20:10 on 9 November. The board placed in the bedroom made the toy's location load-bearing.

## 3. The crocs board passed, and the Reviewer said why

**Board 78.** This is the case A.J. described when the 30-second hook was written —
*"start with what is physically possible: velcro / crocs"*.

> She will not tie her shoelaces. We have been trying for months and every morning ends
> in tears. She has a pair of crocs she thinks are very cool…

```
REVIEW: pass
note: The board is sound: the crocs need no laces, the reward is reserved and within
reach of the parent only, and the prompts start with a point.
```

**It also named the one thing still missing**, which is the remedy half of question 13:
*"the stated obstacle is tying shoelaces, but the board replaces that goal with crocs and
the generalization step only adds a backpack task, so the original goal is not carried
forward."* The substitution was accepted; the dropped goal was not.

---

## What these three do NOT establish

- **Not a detection rate.** Temperature 1 is forced. Boards 61 and 62 came from an
  identical message and returned different results.
- **Severity is not stable either.** `NOUN_MISMATCH` has been seen at both `must` and
  `should`; question 14 has now been seen at both. **Never quote a severity as fixed.**
- These runs all carried `BoardId: 71`, whose own obstacle is a teeth request. The
  board's obstacle therefore contributed context that a first-time parent would not have.

Source: test app transcript, 10 November 2026, 21:57–22:08.
