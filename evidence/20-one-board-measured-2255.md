# One board, alone in a window — 10 November 2026, 22:40–22:55

**ODC Analytics, 15-minute window, Development. Exactly one request in it: board 80.**

| | |
|---|---|
| **Tokens** | **31,249 in · 3,003 out — 34,252 total** |
| **Requests** | **1** |
| **P90 response time** | **28.05 s** |
| **Max response time** | **30 s** |

The message was the 22:46 shoes wording; it returned `REVIEW: pass` with no violations,
so **no retry inflates this figure.** This is one clean board, end to end.

---

## What one board costs and takes

**34,252 tokens and about 30 seconds**, covering the whole flow: the escalation check,
two knowledge-base searches, the Composer call, parsing and eleven-plus validation
checks, the save, the Reviewer call and the verdict.

**One board is ONE request.** That is now certain: a single flow run, two model calls
inside it. It confirms the reading of the earlier windows — 9 requests = 7 boards + 2
refusals — and makes the per-board arithmetic sound.

**At this rate the 10,000,000 allowance is about 291 boards.**

## The share that matters

**91.2% of every token is input.** Output — a complete board as JSON, plus a full
Reviewer verdict — is only 3,003 tokens. Everything else is what we *send*: two system
prompts (the Composer's 19,111 characters and the Reviewer's), the retrieved passages,
the child profile and the draft.

**So the lever on cost is the prompt, not the board.** Halving the output would save 1,500
tokens; a 10% cut in what is sent would save three times that.

## A hypothesis worth one test, not worth acting on tonight

The 22:00–22:15 window averaged **~28,570** tokens per board across seven boards. This
single board, later in the same session, cost **34,252 — 20% more.** One plausible cause:
**the test app is a conversation, and conversation history is part of what is sent.** If
so, the cost of a board grows through a session, and a first board in a fresh chat is
cheaper than the tenth.

**Cheap test, if there is ever time:** send the identical message in a brand-new
conversation and compare. **Do not act on this tonight** — it is one pair of observations
and it changes nothing that ships.

## The practical consequence: the Demo timing is FINE

`VIDEO-SCRIPTS.md` gives `[1:00–1:45]` forty-five seconds to *"Type the real sentence.
Let it work."* **A board arrives in about thirty.** The section carries 86 spoken words,
which is 43 seconds at 120 wpm — **the narration covers the wait almost exactly.**

This **supersedes the earlier concern** raised from the 12-hour window, where P90 was 35 s
and the maximum a full minute, and a board was assumed to be two requests and therefore
60–70 seconds. **A board is one request of about 30 seconds.** No edit to the wait is
needed, and no clip needs speeding up.

Source: ODC Analytics, read 10 November 2026 ~22:55, window 22:40–22:55.
