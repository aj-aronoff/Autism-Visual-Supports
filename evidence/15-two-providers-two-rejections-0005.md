# Two providers, two different rejected parameters — 10 Nov 2026, 00:05

**A clone of the app, rebound from Amazon Bedrock to Azure OpenAI. Four edits: two agent bindings
and two typed log names. Nothing else changed — same prompts, same knowledge bases, same flow, same
schema.**

---

## The result

**The Composer worked.** Board 1 saved in the clone's own tables, first attempt, from a 340-character
request. **So the parse → validate → save chain is provider-portable**, and so is retrieval, the
grounding block and the escalation gate.

**The Reviewer failed, with an exact error:**

```
REVIEWER FAILURE: Failed to call AI model. Status code: BadRequest.
The OpenAI AI model provider returned this message:
"OpenAIException - Unsupported parameter: 'max_tokens' is not supported with this
 model. Use 'max_completion_tokens' instead." (OS-ABRS-FM-40001)
```

**And the draft survived**, reported as *"Draft saved - the review did not give a usable result, so
it has not been reviewed yet."*

---

## The finding

**Each provider rejects a different parameter, and neither rejection is visible in the UI.**

| Provider | Rejected | The error's own words |
|---|---|---|
| **Amazon Bedrock**, Claude Haiku 5.5 | **`temperature = 0.2`** | *"does not support temperature=0.2. Only temperature=1 is supported"* |
| **Azure OpenAI**, GPT-5.5 | **`max_tokens`** | *"not supported with this model. Use `max_completion_tokens` instead"* |

**ODC's model connection exposes `Temperature` and `Max Tokens` as uniform fields.** The providers
behind them accept different subsets, and **nothing in the configuration surface says which.** The
build assistant was explicit that it could not tell: *"It exposes a Temperature field, but it
doesn't declare which values are allowed… the only way to find out is a test call."*

**So a multi-provider agentic app cannot be configured from the UI alone. Every binding needs a
runtime call.**

### Both error messages were excellent, and that is worth saying

Each one named the parameter, the fact of the rejection and the permitted alternative. **Neither
required a single line of debugging** — once the raw failure was printed, each was a one-read
diagnosis. The five hours lost to the Bedrock temperature limit were lost to **not printing the
error**, not to the error being unclear.

> **The lesson: print the provider's own message, verbatim, behind a flag, from the first day.** It
> is the cheapest diagnostic available and it was the last one built.

---

## What made this test cost nothing

**Three things, all decided earlier and none of them for this reason:**

1. **It ran in a clone**, so a provider swap could not touch a published submission.
2. **The Reviewer section is wrapped**, so a model-call failure costs the verdict and not the board.
   Specified on 9 Nov at ~20:40 as *"a Reviewer failure cannot lose the board"*, and this is the
   fourth time it has held — and the first across a provider change.
3. **The raw failure prints behind `DebugShowPassages`.** Built at 21:40 after five hours of an
   opaque *"the Reviewer did not return a usable verdict"*.

**The build assistant also predicted this specific failure before it happened**, unprompted:
*"Some GPT-5-class deployments reject the older max-tokens parameter, so the 10,000 value needs a
test call too. If the model rejects the max tokens setting, the Reviewer will fail. RunReviewer
catches that and reports it as an unusable review, so the saved draft isn't affected."* **All three
clauses were correct.**

---

## The fix, and what it still leaves open

**Clear the Reviewer's max tokens entirely.** ODC sends `max_tokens` and the caller cannot choose to
send `max_completion_tokens`, so the only available answer is to send neither. **The Composer has no
max tokens set and it worked**, which is the evidence that unset is viable.

**Still unknown: whether this model accepts temperature 0.2.** The error complained only about
`max_tokens`, so temperature 1 is evidently fine — and **1 is the default**, so it may simply not
have been exercised. **If GPT accepts 0.2, this clone becomes the first chance to run the Reviewer
as it was designed**, and a temperature-0.2 reviewer against a temperature-1 one on the same fifteen
cases is a comparison nothing in this project can currently make.

---

## One more thing this run is evidence of

**Six warnings, not thirteen.** The seven *"action is never used"* warnings are gone, because wiring
the Reviewer and the save chain made every one of them reachable. **Nothing in the app is unused any
more** apart from six entity scalability suggestions — the first time that has been true, and a
cleaner statement of completeness than any feature list.

---

# Addendum, 00:15 — the GPT Reviewer works, and it is stricter

Max tokens cleared, republished. **Board 2 in the clone, and the Reviewer returned a verdict.**

```
REVIEW: revise
- THEN_NOT_DELIVERABLE  (must)  cards[2].label / plan.reinforcement
  The Then is outside on the swing, which requires leaving the house and may not be
  deliverable within sixty seconds from the bathroom.
- THEN_ALREADY_AVAILABLE (must)  plan.reinforcement
  The plan does not say how access to the swing is restricted so Daughter cannot get
  the Then without finishing Brush teeth.
```

**This is the baseline request** — the one Bedrock composed and passed four separate times tonight.
**On GPT it gets `revise` with two `must` violations.**

## Three differences, and all three favour GPT

**1. Severity calibration.** Bedrock graded `THEN_NOT_DELIVERABLE` and `THEN_ALREADY_AVAILABLE` as
`should` in every run where they appeared. **GPT graded both as `must`.** Same prompt, same fifteen
questions, same severity definitions — **different calibration.**

**2. It noticed the geography.** *"requires leaving the house and may not be deliverable within
sixty seconds from the bathroom."* **Bedrock never once mentioned the walk**, across four runs of
the same board. Question 7 asks whether the parent can deliver the reward *within sixty seconds, in
this environment* — and **only GPT read "in this environment" as a physical claim about a house.**

**3. It generalised question 14 without being told to.** Bedrock asked *"where is it kept"* every
time, which is why board 19's iPad produced the nonsensical advice to store a tablet out of reach.
**GPT asked "how access is restricted"** — which is the Phase 2 branch specified in
`13-q13-q14-both-directions-2220.md` after that failure.

> **So the physical-storage limitation in question 14 may be a MODEL READING ARTEFACT rather than a
> defect in the question.** The question's wording says *"where it is kept"* as an example; one model
> took the example as the rule and the other took the intent. **That is a finding about LLM
> reviewers, not about this prompt.**

## The uncomfortable implication, which is the important one

**Both of GPT's objections are defensible.** Walking from a bathroom to a garden swing is not a
sixty-second delivery. A garden swing is a fixture with no access restriction — **exactly the third
category of reward identified at 23:40**, and GPT named it unprompted.

**So the question is not whether GPT is over-flagging. It is whether Bedrock was under-flagging all
evening.** Every board that "passed" tonight passed a reviewer that, on this evidence, grades more
leniently and reads question wording more literally.

**Consequences, stated plainly:**

- **Record the Demo on the ORIGINAL.** The baseline board passes there. On GPT the same board
  carries two must-fixes, which is a different story and not the Demo's story.
- **The Tech Video should use this comparison, because it is more interesting than either model
  alone.** *"Same prompts, same questions, two providers, and the stricter one found a problem with
  the board I was about to demo."*
- **And for the paper, this is a real methodological caveat:** in an LLM-as-reviewer design,
  **severity grading and the literalness of question interpretation are both model-dependent**, so a
  verdict distribution measured on one provider does not transfer. Nothing in this project had
  measured that, and a four-edit rebind in a clone measured it in ten minutes.

## What it cost

**Four edits, one cleared setting, two publishes, two messages.** No change to the original, no
change to any prompt, no change to the schema or the flow. **The entire comparison was a model
binding.**

---

# Addendum, 11 November 2026 — the Portal corroborates it, and corrects a number

**Read off the `Microsoft_OpenAI_GPT5_5` page in the ODC Portal.**

```
Provider            Custom connection
Last modified       Nov 03, 2026, 11:18 AM by Miguel Amado
Configuration       Development · Production
Endpoints           Priority 1 · OpenAI GPT5.5 · Active
Usage limit         23875 of 400000 tokens   (5%, daily reset)
```

## Why this is a proof point and not just a screenshot

**The meter has moved.** 23,875 tokens were spent on the Microsoft model, which is independent of
any chat transcript: a real call ran there. And the *amount* corroborates this file's own account —
**23,875 is less than one board's measured cost of 34,252** (`evidence/20`), which is exactly the
shape described above: the Composer composed and saved, and the Reviewer failed on `max_tokens`
before spending its share.

So the two-provider claim rests on three independent things: the board that saved, the provider's
verbatim rejection, and a meter that moved on the other vendor's account.

## The correction, and it matters for what we claim

**The two hackathon models do NOT have the same allowance.** `CLAUDE.md` said 10,000,000 tokens a
day *each*. Measured:

| Model | Daily allowance | Boards a day at 34,252 each |
|---|---|---|
| `BedrockHaiku5_5` | **10,000,000** | ~292 |
| `Microsoft_OpenAI_GPT5_5` | **400,000** | **~11** |

**A factor of 25.** So the honest form of *"the category is both"* is: **both providers compose
valid, grounded boards, and their daily capacity differs by 25×.** Never that they are
interchangeable in capacity. This is a second, measured reason to ship bound to Bedrock, alongside
the stated deprecation of the GPT entry.

## One naming caution

This page reads Provider **`Custom connection`** with an endpoint named `OpenAI GPT5.5`, while
`ODC-FIRST-LOGIN.md` and the body of this file say **Azure** OpenAI — and the run-time error did
read `OpenAIException`. **Say "a Microsoft-provided OpenAI GPT-5.5 endpoint"** unless Azure is
confirmed from a page that states it.
