# The malformed replies were truncation — 11 November 2026, 00:36

**The Composer agent had no Max Tokens value set. It had never had one.** It ran the entire
build on whatever the provider defaults to.

---

## The before, twice

The same sensory message was sent twice on 10 November and **failed both times**, with the
parser refusing and saving nothing:

```
Attempt 1: The reply is not valid JSON: Unterminated string.
           Path 'plan.promptHierarchy[2].level', line 38, position 22.
Attempt 2: The reply is not valid JSON: Unterminated string.
           Path 'plan.promptHierarchy[0].kind', line 56, position 35.
```

**Two failures at different offsets — line 38, then line 56.** A systematic syntax error fails in
the same place every time. Different places is what a cut-off stream looks like.

## The change

One field. `CallTrialClaudeHaiku4_5` → Max Tokens, empty → **10000**, matching the Reviewer.
Nothing else was touched; validation stayed at 0 errors and 6 warnings.

## The after, first attempt

The identical message, after a republish:

> **Draft board saved: Daughter's Loud Place Trip (board 82).** REVIEW: revise

It parsed, validated, saved and was reviewed.

## What this means for `evidence/09`

`evidence/09` recorded *"three runs of the same request gave three shapes; the third did not
parse"* and the project has carried **"roughly one reply in three came back malformed"** as a
property of the model since 9 November. **It was not the model. It was an unset field.**

The sensory case is the one that exposed it because it produces a longer board — a sensory
support list, a fuller plan — and a longer board is the one that hits a cap.

**Supporting arithmetic:** a complete board plus a complete Reviewer verdict measured at **3,003
output tokens** (`evidence/20`). The Composer's share is perhaps two thirds of that. A provider
default of 2048 would pass a short board and cut a long one, which is exactly the observed
pattern.

## What it does NOT prove

- **One success against two failures.** Strong, not conclusive. The model is non-deterministic
  and a third failure would have been possible either way.
- **The stop reason was never read.** `AgentFlow` does not read the connector's `FinishReason`
  field, so **a truncated reply is still indistinguishable from a malformed one** inside the app.
  That is the Phase 2 note: log the reply length and the finish reason, and this diagnosis takes
  one run instead of three days.
- It says nothing about replies that are malformed for other reasons. The retry path and the
  thirty-eight checks remain the defence, and both worked correctly throughout — **the app never
  saved a bad board; it refused twice and said why.**

## The sentence this earns, and the one it costs

**Earns:** *"One reply in three came back malformed, and we treated it as model behaviour for two
days. It was a field nobody had set. The lesson is not about the model — it is that we had no
instrumentation to tell a truncated reply from a broken one."*

**Costs:** `VIDEO-SCRIPTS.md` opens by justifying "record, do not perform live" partly on the
malformed-reply rate. **That justification is now weaker and must be restated** — the reason to
record is the Reviewer's temperature, which is forced and unchanged.

## Also first-seen in the same reply

The Reviewer returned a code not previously observed: **`OVERBUILT (should)`** — *"Five cards for
a single loud-place trip may be more than a parent maintains each time, and the 'Find quiet spot'
step adds a second goal the obstacle does not name."* Note the board was a **five-card schedule,
not a First→Then** — the first time the Composer selected a different support type unprompted in
this evidence set.

## ADDENDUM, 00:50 — the same case failed again, and NOT from truncation

Thirteen minutes after board 82 saved, the identical message failed:

```
Attempt 1: Unexpected character encountered while parsing value: `
           Path '', line 0, position 0.
Attempt 2: Required field missing: evidenceBasis
           (it must be a top-level list, not inside plan).
```

**Neither of those is truncation.** A backtick at position 0 is a **markdown code fence** — the
model wrapped its JSON in ```` ```json ````. The second is a **known, previously recorded defect**:
the model nesting `evidenceBasis` inside `plan`, which `CLAUDE.md` already describes as happening
in roughly one reply in three.

**So the record after the Max Tokens change is: one success, one failure, and the failure was for
two different reasons.**

### What this does and does not change

**The truncation signature has not recurred.** `Unterminated string` was seen twice before the
change and **zero times since**. That is still consistent with the diagnosis, and the diagnosis is
unchanged.

**But the headline must be narrower than it was an hour ago.** The honest sentence is:

> *"`Unterminated string` was a field nobody had set. It has not been seen since. The sensory case
> still fails for other reasons, and they are reasons we had already written down."*

**NOT:** *"one field fixed the malformed replies."* It fixed one failure mode out of several.

### What the retry did, and the limit it hit

Attempt 1 failed on the fence. **The retry message was about the fence, the model fixed it, and
then produced a differently malformed reply** — nested `evidenceBasis`. There is only one retry, so
it stopped there. **Two consecutive, different, recoverable shape errors are enough to exhaust the
budget**, and this is the first observation of that.

### The one cheap fix this points at

**Strip a markdown code fence before parsing.** A reply wrapped in ```` ``` ```` or ```` ```json ````
is not malformed JSON — it is well-formed JSON inside a wrapper, and every model does it sometimes.
Removing the wrapper before `JSON.Deserialize` costs nothing and eliminates a whole class of
failure **without relaxing a single check**. The eleven-to-thirty-eight checks still run on exactly
the same content.

**Not recommended tonight:** lifting a nested `evidenceBasis` out of `plan`. That is content
recovery rather than shape normalisation, and it sits much closer to the "refuse before extract"
line the parser exists to hold.

Source: test app transcript, 10 Nov ~20:44 (failures), 11 Nov 00:36 (success), 11 Nov 00:50
(failure, different causes).
