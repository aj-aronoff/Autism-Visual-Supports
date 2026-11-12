# The run that justifies the whole architecture — 9 November 2026, 22:15

**Board 16. `REVIEW: revise`. Three violations, one of them `must`.**

This is the most important single result in the project, and it is not because the board was good.
**It is because the board was wrong in the predicted way and the second agent caught it** — using
two questions the first test user caused at 20:40, on her own case, ninety minutes later.

---

## What was sent

> My daughter cannot physically tie her shoes. How can I motivate her to do it in the morning? She
> has a favorite musical dinosaur toy that we would use for motivation

**The parent has framed it as a motivation problem.** That is the framing the entire app is built
around — a First→Then board is an antecedent package plus reinforcement. **Answering the question as
asked is the failure**, and the Composer answered it as asked.

## What the Composer produced

`Morning Shoes Dinosaur Station`, board 16, saved as Draft. **First card: `Tie shoes`.**

**The predicted gap, confirmed in production.** The Composer has no rule telling it to check whether
a task is physically possible — rule 0 is written in
`prompts/PENDING-FROM-FIRST-TEST-USER.md` and deliberately **not deployed**. So it took the task the
parent named and built a reward around it.

## What the Reviewer said, verbatim

```json
{
"verdict": "revise",
"violations": [
{
"code": "FIRST_NOT_POSSIBLE",
"severity": "must",
"where": "cards[0].label, script.Before, plan.generalization",
"problem": "The First is 'Tie shoes', and the reasoning states she cannot tie her shoes on her own yet, so the board makes a fine-motor task she cannot currently do the required step before every reward.",
"fix": "Make the First a shoe-related step she can do today, such as 'Put on shoes' with fastenings she can manage, or 'Shoes on', and move 'Tie shoes' into plan.generalization as the later goal."
},
{
"code": "THEN_ALREADY_AVAILABLE",
"severity": "should",
"where": "plan.reinforcement",
"problem": "The reinforcement says to hand over the musical dinosaur toy but never says where it is kept, so the reward could be within the child's reach at all times.",
"fix": "State that the toy is stored out of her reach and within the parent's reach, and that it comes out only after the First is finished."
},
{
"code": "NOUN_MISMATCH",
"severity": "should",
"where": "script.Before, script.OnCompletion, cards[1].label",
"problem": "The card reads 'Musical dinosaur' but the script says 'dinosaur' alone, so the child matches a shorter sound to a card whose label includes the word 'musical'.",
"fix": "Use 'musical dinosaur' in every phase where the Then is named so the spoken word matches the card label."
}
],
"strengths": [
"The boardAction removes the First card on completion and leaves the Then card visible.",
"The prompt hierarchy starts with a visual point and ends with a brief physical guide."
],
"note": "Swap the tying task for something she can do today, and decide where the dinosaur toy will be kept between uses."
}
```

---

## Why this matters, point by point

### 1. `FIRST_NOT_POSSIBLE` fired as a `must`, and its fix is her procedure

**Her words, 9 November ~20:10:** *"The very first test needs to be: is it currently physically
possible? If that is too hard, you need to start with something that can be done."*

**The Reviewer's fix, 22:15:** *"Make the First a shoe-related step she can do today … and move
'Tie shoes' into plan.generalization as the later goal."*

**Nobody told it to say that.** Question 13 says *"if the obstacle describes repeated failure at a
task with a fine-motor demand and the board makes that task the First anyway, say so"* and
*"the right board would substitute something the child can do today and put the original goal in
plan.generalization."* It applied the rule and produced the specific substitution.

### 2. `THEN_ALREADY_AVAILABLE` fired on the exact condition she named

**Her words:** a dedicated toy *"that was ONLY ever used for this purpose"*, and it *"needed to
always be available"* — to the parent.

**The Reviewer:** *"never says where it is kept, so the reward could be within the child's reach at
all times"*, and the fix names **both** halves: *"out of her reach and within the parent's
reach."*

**That is the pair of conditions that pull in opposite directions**, which is the part of her insight
that took the most thought to write down — and the Reviewer reproduced both.

### 3. It fired WITHOUT the input it supposedly needs

`BuildReviewerMessages` still does not receive `request.obstacle` (see
`10-reviewer-first-verdict-2203.md`). So how did it know she cannot tie her shoes?

> *"the **reasoning** states she cannot tie her shoes on her own yet"*

**The Composer wrote the constraint into `reasoning`, and the Reviewer read it from the draft.** The
missing input is still a real bug worth fixing — it is luck, not design, that the fact survived —
but it means **the Composer records faithfully even when it acts wrongly**, and that is what gave the
Reviewer something to catch.

### 4. `NOUN_MISMATCH` caught something nobody was looking for

The card says `Musical dinosaur`; the script says `dinosaur`. **For a child matching a spoken word
to a picture, those are two different words.** Pre-existing question, real catch, and exactly the
class of defect a human reviewer would miss on a Monday night.

---

## The architectural conclusion, and it is uncomfortable in a useful way

**If the Composer had substituted the crocs on its own, the Reviewer would have had nothing to
catch, and the two-agent design would have been invisible.**

So the gap in the Composer **is the demonstration.** The Composer drafts what the parent asked for.
The Reviewer says *"she cannot do that, here is what she can do."* The parent decides. That is the
whole design, running, on a real family's real problem.

**This argues against shipping rule 0 as written.** A Composer that silently substitutes is a
Composer that quietly overrules a parent — and `v2=safety` already settled the principle: **the
Reviewer reports, it does not overrule a parent about their own child.** The substitution is advice,
and advice belongs in a verdict a parent can read and reject, not in a board that arrives already
changed.

**Phase 2 should reconsider rule 0's shape**: perhaps the Composer should *name the concern in
`reasoning`* and leave the substitution to the Reviewer, rather than acting on it alone.

---

## One retrieval note, measured

Only **4 passages** reached the Composer. Two layout chunks were **rejected at 0.244 and 0.234**,
just under the 0.25 floor, and the best layout score was 0.3 — lower than the teeth/swing baseline's
0.32.

So **0.25 is doing real filtering**, and on a shorter, question-shaped request it costs two
passages. The board still carried **3 citations** and the evidence base returned its usual
0.737 / 0.716 / 0.706. **No change recommended** — the floor was set from the lowest passage worth
keeping and it is behaving as intended — but it is worth knowing that a terse request retrieves
less.
