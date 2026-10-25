# Token budget and tracking plan

How AI consumption gets measured, capped and reserved across the seven-day build.

Written 24 October 2026. Every number below marked *(estimate)* is a placeholder to be
replaced by measurement on 2 November. The structure does not depend on the numbers.

---

## 1. Why this needs instrumenting in the application

`faq.txt:36`: *"AWS and Microsoft will offer tokens for their respective AI services,
which will be integral to the ODC instance. These tokens will be limited, and usage will
be monitored."*

Note who is monitoring. The tokens are provisioned into an ODC instance that OutSystems
owns, drawing on AWS and Microsoft accounts we have no console access to. We cannot open
CloudWatch and read `InputTokenCount`, and we cannot open a billing dashboard.

**Therefore: if the application does not record its own consumption, we are flying blind
on a metered resource with a hard stop.** This is the same shared-responsibility gap that
makes Trusted Advisor unavailable (see `NOTES-ARCHITECTURE-REVIEW.md`), and it has the
same answer — instrument above the platform line, because we cannot see below it.

There is a second payoff. A team that can show a judge its own cost-per-board figure, and
the caching that reduced it, is demonstrating engineering maturity that most hackathon
submissions will not have.

## 2. The meter is actually two meters

Text and image generation bill differently, and which way depends on the provider:

| Workload | Billed as | Where it lands |
|---|---|---|
| Composer, Reviewer | Input + output tokens | The token allocation |
| Card image generation | **Per image** on Bedrock Titan/Nova Canvas and Azure DALL·E; **per token** on `gpt-image-1` | Possibly a *separate* quota |

**Day 2 action:** establish which model backs image generation and which meter it bills
to. A per-image quota of a few hundred images is a much tighter constraint than a token
pool, and the whole library-first design (WA-12) is aimed at exactly that quota.

## 3. What one board costs *(estimate)*

Derived from the JSON output contract in `SPEC.md §5` and the grounding sources, not
measured. Shown so the method is checkable and the estimate is replaceable.

| Call | Input | Output | Notes |
|---|---|---|---|
| Composer | ~2,500 | ~600 | System prompt, retrieved TRIAD layout + practice chunks, child profile, obstacle; emits the full card/script/plan JSON |
| Reviewer | ~1,100 | ~150 | The draft JSON plus the design rules; emits pass/fail with reasons |
| **One clean board** | **~3,600** | **~750** | ≈ 4,350 tokens |
| Blended, with a 30% review-retry rate | ~4,700 | ~975 | **≈ 5,700 tokens** |
| **Planning figure, with overhead** | | | **8,000 tokens per board** |

Plus 0–2 images per board, falling toward zero as the card library fills.

**Build-wide volume** *(estimate)*: roughly 480 generation runs across the seven days —
pipeline iteration dominates, demo recording is small but must not fail. At 8,000 tokens
that is **~3.8M tokens**. Low millions is the shape to plan for.

This is why finding the allocation on day 2 is a go/no-go check and not an administrative
task. If the pool is ~1M, the plan changes materially: mechanical validators replace the
Reviewer model call entirely (WA-15), and the card library gets seeded by hand before any
rehearsal. If it is ~10M, the plan stands as written.

## 4. The reserve

The earlier review said "a third of the allocation." That was arbitrary. The reserve
should be derived from what it has to protect, with a floor beneath it:

```
Demo-critical consumption:
  12 full takes of a 5-minute video          (realistic for a live-app walkthrough)
  × 3 boards generated per take              = 36 runs
  × 8,000 tokens                             = 288,000 tokens
  + rehearsal on day 8                       = ~100,000 tokens
  ────────────────────────────────────────────────────────────
  Subtotal                                     ~390,000 tokens
  × 1.3 safety factor                          ~500,000 tokens

RESERVE = max(30% of allocation, 500,000 tokens, 150 images)
```

The floor is the operative half. Thirty percent of a generous allocation is comfortable;
thirty percent of a small one is not enough to record a video twelve times, and the
reserve exists for exactly that scenario.

**The reserve is not a guideline, it is enforced.** See §6.

## 5. Spending the rest

The spendable pool is `allocation − reserve`, apportioned by build day as a percentage so
the plan survives any allocation figure:

| Day | Work | Share of spendable |
|---|---|---|
| 3 | Entities, child profile — little inference | 5% |
| 3–4 | Composer + Reviewer brought up; highest failure rate of the build | 25% |
| 5 | Wizard end to end, three-word validator | 20% |
| 5–6 | Illustrator, card library, board editor — image-heavy | 25% |
| 7 | Twilio loop, usage log | 10% |
| 8 | UX pass and first rehearsal | 15% |
| **8–9** | **Recording** | **the reserve** |

Day 3–4 gets the largest share deliberately. That is when prompts are wrong and runs fail,
and underfunding it pushes the failures into day 5 where they cost schedule as well
as tokens.

## 6. The mechanism

### 6.1 A tenth entity

`TokenUsage` — written by a server action wrapping every model call:

`OccurredOn` · `AgentRunId` *(joins to `Board.AgentRunId`)* · `Operation` → Composer |
Reviewer | Illustrator · `ModelId` · `InputTokens` · `OutputTokens` · `ImageCount` ·
`Outcome` → Success | ValidationRetry | Error · `BoardId` *(nullable)*

ODC Agent Workbench returns usage metadata on the model response. The wrapper records it
whether the call succeeded or not — failed runs are the ones that consume budget
invisibly, and on day 3–4 they are the majority.

### 6.2 The circuit breaker

Two application settings, `DailyTokenCap` and `ReserveFloor`, and one check in the wrapper
before each call:

- Projected spend over `DailyTokenCap` → warn in the admin view, keep going.
- Cumulative spend within `ReserveFloor` of the allocation → **refuse the model call and
  return the deterministic template board instead.**

That fallback path already has to exist. WA-9 requires it when the Composer–Reviewer loop
fails to converge, and WA-10 wants it when Twilio is degraded. A First–Then board is two
cards and a phrase; it does not strictly need a model. One mechanism therefore covers loop
termination, external-dependency degradation, and the token reserve — and it means the
reserve is protected by code rather than by remembering.

### 6.3 Reconciliation

Application-recorded usage is our number, not the authoritative one. If the ODC console
exposes AI consumption for the instance, compare the two at the end of each day. A
divergence means something is calling a model outside the wrapper, which is worth
knowing immediately.

## 7. The daily ritual

Four minutes at the end of each build day:

1. Append the day's totals to [`tools/token-log.csv`](tools/token-log.csv).
2. Run `python3 tools/token-budget.py --allocation <N>`.
3. Read the verdict line. If it says anything other than `ON TRACK`, deal with it that
   evening, not on day 8.
4. Reconcile against the ODC console if it shows a figure.

The lever to pull when burn rate runs ahead, in order of preference:

1. **Seed the card library by hand.** Pre-generating the twenty most common activity
   cards once removes image generation from every subsequent rehearsal. Cheapest fix
   available and it improves the product (WA-12).
2. **Move Reviewer checks into code.** Word count, phrasing polarity, Then-card presence
   and card count are mechanical. Four of Reviewer's jobs should never have been a model
   call (WA-15).
3. **Drop Composer to the smaller model** for everything except the recorded demo.
4. **Cut the review retry cap from two cycles to one.**

Note that the first two make the application better as well as cheaper. Reach for them
before the two that trade quality for budget.

## 8. Open questions for the 2 November kickoff

1. What is the token allocation, in tokens — and is it per team or per account?
2. Is image generation on the same meter or a separate per-image quota?
3. Which models are available, and does the allocation differ between them?
4. Where can a team see its own consumption to date?
5. What happens at exhaustion — hard stop, throttle, or a request for more?

Question 4 is the one to push on. If OutSystems exposes a per-team usage figure, §6.3
becomes a real reconciliation instead of a hope, and §6.1 becomes a cross-check rather
than the only source of truth.
