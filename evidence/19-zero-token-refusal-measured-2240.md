# Thirty refusals, zero tokens, 96 milliseconds — 10 November 2026, 22:25–22:40

**ODC Analytics, 15-minute window, Development. Baseline confirmed empty at 22:25.**

| | |
|---|---|
| **Tokens** | **0 in · 0 out** |
| **Requests** | **30** · 2/min |
| **P90 response time** | **96 ms** |
| Max response time | 8 s |

---

## Why this reading is unambiguous

A window showing zero tokens could mean "cost nothing" **or** "telemetry has not ingested
yet". **The requests count removes that doubt.** Thirty requests were recorded, so the
page was ingesting; and across all thirty, **not one model token was spent.**

The window was run deliberately: the previous board was at 22:08, the baseline was
confirmed at `0 in / 0 out` at 22:25, and nothing but escalation messages was sent.

## What it proves

**The guardrail short-circuit is real, and it is now measured rather than designed.**
`CheckEscalation` runs first in `AgentFlow`; on a hit it returns referral guidance and
ends — no retrieval, no prompt built, no agent call, no board, no memory write, no token
log. Until tonight that was a claim about how the flow is wired. It is now a reading.

**It also settles what "Requests" counts.** Thirty refusals produced thirty requests and
no tokens, so a request is **one flow invocation**, not one model call. That retrospectively
explains the 22:00–22:15 window: **9 requests = 7 boards + 2 refusals**, and its
199,980 tokens over 7 boards gives **~28,570 tokens per board**.

## The number nobody expected

**P90 is 96 milliseconds.** A composed board runs at a P90 of 27 seconds in the same app
on the same night. **The refusal path is roughly 280 times faster and costs nothing**,
because it is a list of 21 substrings and 5 regular expressions evaluated before anything
else happens.

The 8-second maximum is one outlier in thirty, most likely a cold start.

## The sentences this earns

For the Tech Video, replacing *"that refusal costs no tokens at all"*:

> **Thirty refusals in one fifteen-minute window. Zero tokens. Ninety-six milliseconds at
> the ninetieth percentile. The safety check runs before anything that costs money, and
> that is measured, not designed.**

And the comparison, which is the part that lands:

> **A board takes twenty-seven seconds and about twenty-eight thousand tokens. A refusal
> takes a tenth of a second and nothing. The cheapest thing this app does is decline.**

## What it does NOT prove

- It says nothing about whether the 21 substrings and 5 patterns are the **right** ones.
  That is `tools/test_guardrails.py` — 74 rows, 21 tests — and it is a different claim.
- It does not cover the board-obstacle path, which is what the e2 test checks.
- Latency and cost are stage- and provider-specific. This is Development, on Bedrock
  Haiku 5.5.

Source: ODC Analytics, read 10 November 2026 ~22:40, window 22:25–22:40.
