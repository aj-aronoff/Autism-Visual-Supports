# Questions 13 and 14, tested in both directions — 9 Nov 2026, 22:15–22:20

**Three boards, fifteen minutes, and between them they establish that the first test user's
questions work.** This file ties `11`, `12` and board 18 together, because no single run proves a
check and these three together nearly do.

---

## The arc

| Board | What the parent wrote | First card | `FIRST_NOT_POSSIBLE` | Verdict |
|---|---|---|---|---|
| **16**, 22:15 | *"cannot physically tie her shoes. How can I **motivate** her"* | `Tie shoes` | **FIRED — `must`** | `revise` |
| **17**, 22:18 | *"We **have purchased** a new musical dinosaur toy"* | `Clean room` | n/a | `revise` — **false `must`** on `THEN_NOT_DELIVERABLE` |
| **18**, 22:20 | *"She has a pair of crocs she thinks are very cool… reward… reserve for this purpose"* | `Put on crocs` | **SILENT** | `pass` |

**Board 16 proves it fires. Board 18 proves it does not over-fire. Board 17 shows its one failure
mode and names the cause.** That is as close to a characterised check as three organic runs can get.

### Why board 18 matters most, and it is the least dramatic of the three

**A new check that fires is easy. A new check that stays quiet when it should is the hard half.**
`c15-nothing-wrong` exists in the eval set for exactly this reason — it is the only case testing for
over-flagging — and board 18 is that test, run live, on a parent who had applied the substitution
themselves.

Had `FIRST_NOT_POSSIBLE` fired on `Put on crocs`, question 13 would have been unusable: a check that
flags every shoe board is noise. **It stayed silent, and the verdict came back `pass`.**

---

## And the severity-to-verdict logic held across all three

- Board 16: one `must` + two `should` → **`revise`**
- Board 17: one `must` + three `should` → **`revise`**
- Board 18: two `should`, no `must` → **`pass`**

**That is `v2=safety` behaving exactly as specified** — a parent is not blocked over a matter of
judgement, and only a `must` changes the verdict. Consistent across three runs with different
violation counts.

---

## The repeatable Composer defect this exposed

**`THEN_ALREADY_AVAILABLE` fired on all three boards — 16, 17 and 18.**

And on board 18 the parent had *said it outright*: *"a special musical dinosaur toy, that we would
**reserve for this purpose**."* The Composer still did not write where the toy is kept.

```
THEN_ALREADY_AVAILABLE | should | plan.reinforcement
problem: The reinforcement says to hand over the musical dinosaur straight away but never says
         where it is kept between uses, so nothing stops the child reaching it at any time.
fix:     Say the dinosaur is kept on a high shelf or in a parent-held bag, out of the child's
         reach and within the parent's, and is only brought down when the First is finished.
```

**So: the Composer has no concept of where a reward lives, and will omit it every time.** Three for
three, including once when told explicitly.

**That is the first test user's insight confirmed completely.** Rule 3 of the Composer prompt asks
only whether the Then can be *delivered* in sixty seconds. **Nothing asks where it is kept between
uses**, so nothing produces it — and until 20:40 tonight nothing would have noticed. The pending
rule 3 extension in `prompts/PENDING-FROM-FIRST-TEST-USER.md` is the fix, and **this is the evidence
that it is needed rather than merely sensible.**

Expect `THEN_ALREADY_AVAILABLE` on essentially every board until that ships. **It is not a flaky
check; it is a standing Composer gap being reported accurately.**

---

## One `should` worth a second look

```
IMAGE_LABEL_DRIFT | should | cards[0].imagePrompt
problem: The label says 'Put on crocs' but the prompt and altText depict generic slip-on clog
         shoes, so the picture and the word may not match what the child wears.
fix:     Make the prompt depict a pair of crocs specifically, or change the label to
         'Put on clogs' so the word and picture agree.
```

**The reasoning is right and the fix has a wrinkle.** A child matching a spoken word to a picture
needs them to name the same thing, so `crocs` + generic clog is a real mismatch. But the first half
of the fix asks the image prompt to depict **a brand**, and `SPEC.md` §5 keeps image prompts generic.
**The second half of the fix — relabel to `Put on clogs` — is the one to take.**

Worth noting because it is the Reviewer giving two fixes where one is right. **It reports; the human
chooses.** Which is the design.

---

## Retrieval, and the 0.25 floor is now visibly binding

```
board 16   0.3    0.244 REJECTED   0.234 REJECTED
board 17   0.417  0.373            0.352
board 18   0.275  0.253            0.229 REJECTED
```

**Observed passes go down to 0.253; observed rejections are 0.244, 0.234, 0.229.** The floor sits
inside the distribution rather than below it, so it is doing real work on most runs.

**No change tonight.** Every board still carried three citations and the evidence base returned its
constant 0.737 / 0.716 / 0.706. But **Phase 2 should revisit the floor with this data**, because the
gap between the lowest pass and the highest rejection is now **nine thousandths** — which is noise,
not a judgement.

And board 17 is the counter-example to the obvious theory: **it is not request length that drives
retrieval, it is topic overlap.** Board 17 was long and scored highest (0.417) because it is about
boundaries and clean-up, which is what the TRIAD passages discuss. Board 18 was equally long and
scored lowest, because shoes and rewards are not.

---

# Board 19, 22:24 — a limitation in question 14 itself

Added after the fact. **This run found a gap in a question written ninety minutes earlier**, which
is the fastest any check in this project has been characterised and corrected.

## What the parent wrote

> She will not put her shoes on to leave the house. She sometimes wears her silvery crocs. She would
> rather be on her tablet, **which she carries around with her most of the day anyway**. There is a
> **new program on the iPad** she has wanted. **We can limit playtime to days when she wears her
> crocs.**

**The parent solved the exclusivity problem themselves, and solved it the way the first test user
described it.** Not *"the tablet"* — she already has that — but **a specific new program**, with
access limited. That is her own refinement, verbatim from
`FIRST-TEST-USER-9-NOV.md`: *"For kids motivated by time on iPad, extra time for some specific app
might work."*

## What the Reviewer said

```
REVIEW: pass
THEN_ALREADY_AVAILABLE | should | plan.reinforcement
problem: The plan limits the iPad program to crocs days but never says where the iPad or the
         new program is kept, so the child may be able to reach the reward without finishing
         the First.
fix:     State where the iPad is stored between uses, out of the child's reach and within the
         parent's, and say that the child gets it only after the crocs are on.
```

## The finding: question 14 assumes a physical object

**"Out of the child's reach" is meaningless for a device she carries all day.** A digital reward is
restricted by **screen-time limits, an app lock, a parent passcode, a controlled unlock** — not by a
shelf.

Question 14 was written around the first test user's musical dinosaur, which is a physical object
with a storage location. **It asks "where is it kept", and software has no answer to that
question.**

So the Reviewer **fired for the right reason** — `reinforcement` does not state how access is
restricted — and **asked for the wrong kind of answer.** It also did not credit the restriction the
parent had already described, which is a second-order version of the same gap: the question has one
model of exclusivity and the parent used another.

### The Phase 2 correction

Question 14 needs two branches, and they are not the same question:

- **A physical reward** — where is it kept? Out of the child's reach, within the parent's.
- **A digital reward** — how is access controlled? A time limit, an app lock, a passcode, a
  parent-held device. **And "a specific named program" is already stronger than "screen time"**,
  so a parent who names one has done most of the work and should be credited, not flagged.

**The same applies to the pending rule 3 extension** in
`prompts/PENDING-FROM-FIRST-TEST-USER.md`, which currently says `reinforcement` must say *"where it
lives"*. That wording inherits the same assumption and should carry both branches.

## One thing that went right and is worth recording

**`NOUN_MISMATCH` did not fire**, and the Reviewer said why in a strength:

> *"The First and Then cards match the script wording exactly, and boardAction moves the First card
> off the board on completion."*

After firing on boards **16** and **17**, that defect is **not universal** — it depends on whether
the Then's name has a qualifier the script can drop (`Musical dinosaur` → `dinosaur`). **The
Composer can get it right**, which makes the earlier two real defects rather than a broken check.

## Retrieval

`0.338 / 0.336 / 0.322`, all passed, six passages. Chunk **13** came back —
*"What if challenging behaviors occur? … Keep your focus on the task rather than on the challenging
behavior"* — which is the right passage for a child who refuses at the door.

## Question 14, after four runs

| Board | Reward | Fired | Right reason? | Right remedy? |
|---|---|---|---|---|
| 16 | musical dinosaur toy | yes | **yes** | **yes** |
| 17 | new musical dinosaur | yes | **yes** | **yes** |
| 18 | reserved musical dinosaur | yes | **yes** | **yes** |
| 19 | a named iPad program | yes | **yes** | **no — physical storage for software** |

**Four for four on the reason. Three for four on the remedy.** For a question that did not exist at
20:00 tonight, characterised against four real family situations by 22:24.
