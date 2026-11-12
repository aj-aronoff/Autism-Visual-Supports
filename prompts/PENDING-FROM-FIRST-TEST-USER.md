# Pending prompt changes — from the first test user, 9 November 2026

**Status: WRITTEN, NOT DEPLOYED.** None of this is in the running app. `prompts/composer.md` and
`prompts/reviewer.md` are unchanged, so the repo still describes what actually executes.

**Why it is not deployed, and the reason is not effort.** It was written at 20:20 on the last build
night. A Composer prompt change would have **invalidated six test cases that passed forty minutes
earlier**, and a rule reading *"substitute when the task is too hard"* could make the model
substitute on the teeth→swing case — **which is the board the Demo is built on.** We would have found
that out mid-recording. The change is right; 20:20 was the wrong time to make it.

**Source:** A.J.'s wife, the first test user, from lived experience with their autistic daughter, who
has a **motor planning issue**. Full write-up and the measured gaps:
`../FIRST-TEST-USER-9-NOV.md`.

---

## 1. Composer — a new rule, and it goes FIRST

Place it **before rule 1**, as **rule 0**, because its whole point is that it precedes support-type
selection. Every other rule assumes the obstacle is motivational. This one does not.

```text
0. IS THE FIRST PHYSICALLY POSSIBLE TODAY? ASK THIS BEFORE ANYTHING ELSE.

   The obstacle may describe a task the child CANNOT YET DO, not one they will
   not do. Those need different answers and only one of them is a First-Then
   board. A board plus a reward is an antecedent package -- it changes whether
   a child is willing. NO REWARD REMOVES A MOTOR-PLANNING BARRIER.

   A board that asks for the impossible, every morning, with a reward in front
   of it, teaches the child that the board predicts failure and teaches the
   parent that visual supports do not work. BOTH ARE WORSE THAN NO BOARD.

   So: if the profile or the obstacle suggests the task is beyond this child
   right now, DO NOT make it the First. Substitute down a response-effort
   gradient until you reach something they can do TODAY. Each step should
   remove a demand, not just shrink the task.

     Shoes, as the worked example:
       tying laces  ->  velcro, which removes the tying
                    ->  slip-ons or crocs, which remove the fastening

   Then:
     - Name the substitution in "reasoning" and say what it removed. The
       parent asked for one thing and is getting another; they are owed the
       reason in a sentence.
     - Put the ORIGINAL goal in plan.generalization. That field exists for
       exactly this shape -- it is the path back to what the parent wanted.
     - PREFER A SUBSTITUTION THE CHILD WILL LIKE. Crocs they think are cool
       beat plain slip-ons. The First then carries a little motivation of its
       own, on top of the lower effort, and that is two mechanisms for one
       choice.

   WHAT YOU CANNOT DO is diagnose the difficulty. You are not deciding WHY the
   task is hard. You are noticing that the parent has described months of
   failure at a task with a fine-motor demand, and choosing an entry point
   where the board can succeed.
```

**Note the deliberate limit in that last paragraph.** `CLAUDE.md` §2: no diagnosis, no clinical
advice. The rule must let the model *substitute* without letting it *attribute*, or it has started
assessing a child, and a board generator does not do that.

---

## 2. Composer — rule 3 extended

Rule 3 currently reads, in full:

> *A FirstThenBoard MUST have a Then card, and the Then must be something the parent can deliver in
> the next sixty seconds. "Extra screen time tonight" is not a Then. The reward is structural —
> without it this is just an instruction with a picture.*

**That is deliverability only.** Add two paragraphs:

```text
   AND THE THEN MUST NOT BE SOMETHING THEY ALREADY HAVE. A reward the child
   can reach whenever they like is not a reward; it is a thing that happens
   to be nearby. The power comes from the restriction. So the Then should be
   obtainable ONLY by finishing this First, and "reinforcement" must say
   WHERE IT LIVES: out of the child's reach, within the parent's. Those are
   two different storage decisions and they pull in opposite directions on
   purpose -- a reward kept somewhere safe but inconvenient fails on the
   third morning.

   AND MATCH THE THEN TO sensoryNotes WHERE YOU CAN. You already use that
   field to avoid a collision. Use it to CHOOSE as well: a child who seeks
   sound should be offered sound, a child who seeks movement should be
   offered movement. "Extra time on one named app" is a better Then than
   "screen time" for the same reason the dedicated toy beats the toy box --
   it is bounded and identifiable.
```

**The second paragraph closes a measured asymmetry.** `composer.md:242` uses `sensoryNotes` as a
**veto** — *"anything you name here must not collide with sensoryNotes"* — and never as a selector.
The first test user's daughter is the case that breaks it: **musical toys are especially
compelling**, and the field that knows to avoid music for one child cannot propose it for another.

---

## 3. Reviewer — questions 13, 14, 15

Twelve becomes fifteen. **All three are judgements a validator cannot make**, which is the test for
whether a question belongs to the Reviewer rather than to code.

```text
13. IS THE FIRST SOMETHING THIS CHILD CAN PHYSICALLY DO TODAY?
    Not "is it reasonable" -- is it POSSIBLE. If the obstacle describes
    repeated failure at a task with a fine-motor demand and the board makes
    that task the First anyway, say so. A board that asks for the impossible
    is not a mild problem; it is the one failure that teaches a family this
    approach does not work.
    Code: FIRST_NOT_POSSIBLE

14. CAN THE CHILD GET THE THEN WITHOUT DOING THE FIRST?
    If the reward is something they have free access to, the board has no
    contingency and the Then is decoration. Check whether "reinforcement"
    says where it is kept. A Then that is simply nearby is the commonest way
    a well-formed board does nothing.
    Code: THEN_ALREADY_AVAILABLE

15. DOES THE THEN IGNORE WHAT THIS CHILD ACTUALLY SEEKS?
    sensoryNotes may name what they seek, not only what they avoid. A reward
    that matches it is stronger than a generic one. This is the weakest of
    the three -- report it, never block on it.
    Code: THEN_IGNORES_SENSORY_PROFILE
```

---

## 4. What the data model needs, and it is the real constraint

**The `Child` entity cannot express the child this came from.** Eight fields —
`nickname`, `ageYears`, `developmentalStage`, `visualStyle`, `languageLevel`, `specialInterests`,
`sensoryNotes`, `triggerNotes` — and **not one of them is about what her hands can do.**

So rule 0 above would run on inference from the obstacle text alone. It would work, because a parent
describing months of failure at laces is telling you something. **But it would work better with the
fact stated**, and the fact has nowhere to live.

Two fields, for Phase 2:

- **`motorNotes`** — what is physically hard, independent of willingness. *"Motor planning
  difficulty; laces and buttons are beyond her."*
- **`reservedRewards`** — items deliberately kept back. **`specialInterests` says what she likes; it
  does not say what she is allowed at will.**

**The data model, not the prompt, is the binding constraint here** — which is the cheapest possible
place for a gap to be, because adding a field is smaller than rewriting a rule.

---

## 5. Three eval cases, and they should be hers

`c18-motor-planning-shoes` · `c19-dedicated-reinforcer` · `c20-sensory-matched-reward`.

Each an A/B pair: try A takes the obvious First or the nearby reward, try B substitutes. **The eval
set has sixteen cases written by the developer and none by a parent.**

---

## 6. Deploy order, after the submission

1. The two `Child` fields, and the grounding JSON that carries them.
2. Rule 0 and the rule 3 extension, as one prompt re-paste. **Re-run all ten test cases
   immediately** — rule 0 is the one change capable of altering a board that currently works.
3. The three Reviewer questions, which are free to add because **nothing calls the Reviewer yet.**
4. The three eval cases.

**Step 2 is the one with teeth, and the risk is over-substitution.** A model told to substitute when
a task is too hard may substitute when it is not. `c15-nothing-wrong` is the negative control and it
will be the test that matters.
