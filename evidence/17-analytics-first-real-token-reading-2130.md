# The first real token and latency reading — 10 November 2026, ~21:30

**ODC Analytics, app `Autism Visual Supports`, Development, window 09:00–21:00.**
A rolling 12-hour window, so these numbers are gone by tomorrow morning. Recorded here
because they are the only measured cost figures the project has.

| | |
|---|---|
| Tokens | **1,090,913 in · 194,199 out** |
| Total | **1,285,112** |
| Requests | **57** · rate 4.75/hr |
| P90 response time | **35.057 s** |
| Max response time | **1 m** |
| Safety score | — |
| Answer relevance | — |

## What it says, arithmetic only

- **~22,500 tokens per request**: ~19,100 in, ~3,400 out.
- **84.9% of every token is input.** The system message, the retrieved passages, the
  child profile and the draft are re-sent on each call; the board itself is the small
  part. Anything that shortens the prompt is worth six times what shortening the board
  would be.
- **A board costs at least two requests** — one Composer call, one Reviewer call — so
  **~45,000 tokens per board** at the average, and about **222 more boards** before the
  10,000,000 allowance is reached.
- **1,285,112 of 10,000,000 in one day: 12.85%.**

**A "request" here is a model call, not a parent message.** The escalation refusals and
the short-message refusals appear nowhere in this count, because they return before the
model is called — the zero-token claim, visible as an absence rather than as a zero.

## The number that changes how the Demo is recorded

**P90 is 35 seconds and the maximum is a full minute — for ONE call.** A board is two.
So a board realistically takes **40 to 70 seconds** from pressing enter.

`VIDEO-SCRIPTS.md` allots **45 seconds** to `[1:00–1:45] Type the real sentence. Let it
work.` **That is not enough, and the wait is not optional.** Two honest ways to handle
it, and one that is not:

- **Cut the wait** in the edit and say so: *"this takes about a minute."* Preferred.
- **Narrate over it** — that section has 86 spoken words, about 43 seconds at 120 wpm,
  which covers one call but not two.
- **Not acceptable:** silently speeding the clip up so a board appears to arrive
  instantly. It would misrepresent the one number a technical judge can check.

## What this replaces

`LogTokenUsage` writes 0, so `GetTokenUsageTotals` returns nothing useful. **This page
makes that defect cosmetic rather than blocking**: the platform meters tokens per period
for free, in tokens, and it is a screen a judge can be shown. The in-app counter would
only add per-board attribution, which nothing currently depends on.

## Two things the page shows as empty

**Safety score** and **Answer relevance** both read `—`. These are ODC's own agent
evaluation metrics, named at the kickoff as a scored capability, and **nothing has been
configured to populate them.** Recorded, not actioned: configuring an evaluator on the
last build night would put a new, unexercised dependency in the publish path.

Source: ODC Analytics screen, read 10 November 2026 ~21:30, window 09:00–21:00.
