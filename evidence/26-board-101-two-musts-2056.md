# Both of the first test user's questions fire, on one board — 11 November 2026, 20:56

**Board 101. `REVIEW: revise`. Two violations, both `must`.** Screenshot, unedited:
`26-board-101-two-musts-2056.png`.

## The request — the same words as board 16, two days later

```
My daughter cannot physically tie her shoes. How can I motivate her to do it
in the morning? She has a favorite musical dinosaur toy that we would use for
motivation
```

## What came back

```
Draft saved - 2 things to fix before approving it.
Draft board saved: Shoes First, Then Dinosaur (board 101). It is a Draft and has not been approved.
REVIEW: revise
- FIRST_NOT_POSSIBLE (must)  cards[0].label / script.Before
- THEN_ALREADY_AVAILABLE (must)  plan.placement / plan.reinforcement
```

## Why this one matters more than board 16 did

1. **Question 13 is now repeatable.** `evidence/11` was the first firing, on 9 November. This is a
   fresh run of the same request and it fired again, at the same severity, on the same field.
   **The Reviewer runs at temperature 1 and that is forced**, so repeatability could not be
   assumed — it had to be observed. This is the observation.
2. **Question 14 fired on the same board, unprompted.** `THEN_ALREADY_AVAILABLE` caught that the
   plan said to keep the musical dinosaur *in sight beside the board* while never saying where it
   is stored — so the reward is reachable at all times and is not contingent on the First. That is
   the first test user's fourth rule — *a dedicated reward, obtainable only by doing this one
   thing* — enforced by the system she caused.
3. **The Composer made the same mistake again**, which is the honest half: rule 0 is written in
   `prompts/PENDING-FROM-FIRST-TEST-USER.md` and deliberately **not deployed**, so the Composer
   still takes the task the parent names. **The architecture is what catches it, not the prompt.**
4. **Both fixes are specific and actionable**, naming velcro or slip-on shoes, and a high shelf or
   a parent-only drawer. Neither invents a fact about the child.

## What it does NOT prove

- **Three firings of question 13 is still three**, not a rate. Nothing here says how often it
  would be silent when it should fire.
- **The board was still saved.** A `revise` verdict gates the approve step, not the save — a draft
  is unreviewed by definition.
- This is one request shape. Nothing here exercises the other thirteen questions.

## The slide version, and what was cut

`slide4-verdict.png` carries four lines of this screenshot for the deck — the Draft-saved line,
`REVIEW: revise`, and the opening line of each violation. **Every omission is marked with a dashed
rule.** Nothing is reworded and nothing is added. The unedited original is the `.png` beside this
file, and it is the one to cite.
