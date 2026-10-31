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

## 2. The meter is requests, not tokens

**Corrected 30 October, from the published trial-model limits.** This document was built
around a token pool. For a Licensed Customer tenant that is the wrong unit: the trial
models cap **requests**, and leave tokens unlimited.

| Model | Context | Max requests | Request rate | Max tokens | Token rate |
|---|---|---|---|---|---|
| **GPT-5** | Licensed Customers | **100** | — | — | — |
| **Claude Haiku 4.5** | Licensed Customers | **1,000** | — | — | — |
| | Personal Edition | 3,000 | 30/min | 5M | 100k/min |
| **Amazon Nova Pro** | Licensed Customers | **1,000** | — | — | — |
| | Personal Edition | 1,000 | **3/min** | 1M | 12k/min |

Three things to take from the table:

- **The caps are totals, not rates, and nothing refills them.** Every rehearsal spends
  permanently. This is the single most important change to this document.
- **Which row applies to us is unknown**, and the two differ by a factor of two:
  Licensed Customers get 2,100 requests across all three models; Personal Edition gets
  4,000 but has no GPT-5 row at all. It is visible on the Trial Model details page and is
  now open item 12.
- **Nova Pro in Personal Edition is rate-limited to 3 requests a minute**, which is 180 an
  hour. That is unusable as a primary model during a build day and confirms Haiku 4.5 as
  the workhorse on either row.

The token figures in §3 are still right, and still worth having — they decide whether we
fit inside Personal Edition's 5M, and they are what a judge will ask about. They are just
no longer the binding constraint.

## 2b. The second meter, and why it closed

Text and image generation bill differently, and which way depends on the provider:

| Workload | Billed as | Where it lands |
|---|---|---|
| Composer, Reviewer | Input + output tokens | The token allocation |
| Card image generation | **Per image** on Bedrock Titan/Nova Canvas and Azure DALL·E; **per token** on `gpt-image-1` | Possibly a *separate* quota |

~~**Day 2 action:** establish which model backs image generation and which meter it bills
to.~~ **Largely settled 30 October.** The three ODC trial models — GPT-5 via OpenAI,
Claude Haiku 4.5 via Amazon Bedrock, Amazon Nova Pro via Amazon Bedrock — are all
text-out. None generates images, and Nova *Canvas* is not among them. So there is no
second meter to budget for unless a non-trial image model can be added, and the
library-first design (WA-12) is now how the product works rather than a quota defence.

**The remaining meter is a hard stop.** Trial-model limits are *not* time-boxed — they are
a total allowance, and when one is reached it *prevents further use of the model*. No
throttle, no grace period. That moves §6.2's circuit breaker from prudent to load-bearing:
it is the difference between stopping on our own terms and a dead demo.

## 3. What one board costs *(estimate)*

Derived from the JSON output contract in `SPEC.md §5` and the grounding sources, not
measured. Shown so the method is checkable and the estimate is replaceable.

**The model, as of 30 October: Claude Haiku 4.5 via Amazon Bedrock**, with GPT-5 held in
reserve. Haiku is the cheapest and fastest of the three trial models for a high-volume
structured-JSON task, which is exactly the Composer and Reviewer workload, and the
allocation is a hard-stopping total rather than a daily refill. GPT-5 is the one to reach
for only on cases the eval set shows Haiku failing, and switching is a model-reference
change, not a redesign — the JSON contract in `SPEC.md §5` is the interface. The estimate
below was made without a named model and is unchanged by naming one; it is the limits
table that will revise it.

| Call | Input | Output | Notes |
|---|---|---|---|
| Composer | ~2,500 | ~600 | System prompt, retrieved TRIAD layout + practice chunks, child profile, obstacle; emits the full card/script/plan JSON |
| Reviewer | ~1,100 | ~150 | The draft JSON plus the design rules; emits pass/fail with reasons |
| **One clean board** | **~3,600** | **~750** | ≈ 4,350 tokens |
| Blended, with a 30% review-retry rate | ~4,700 | ~975 | **≈ 5,700 tokens** |
| **Planning figure, with overhead** | | | **8,000 tokens per board** |

Plus 0–2 images per board, falling toward zero as the card library fills.

### 3a. The same board, counted in requests

| Design | Requests per board | Why |
|---|---|---|
| Three agents, each a model call | 3 | Composer, Reviewer, Illustrator |
| With a 30% review-retry | **~4** | The blended figure |

**At ~4 requests a board, the build does not fit.** 480 generation runs is ~1,870
requests against a Licensed-Customer ceiling of 2,100 — 89% of everything, before any
reserve. With the §4 reserve applied it fails outright.

Two changes fix it, and both were already in the design as *preferences*. They are now
*requirements*:

| Change | Requests saved | Where it already lives |
|---|---|---|
| **Reviewer deterministic-first** — the seven guardrails in `SPEC.md §6` are rules, not judgements; call the model only on the ambiguous ~20% | ~0.8 | WA-15, and §3.2 of `CODE-PLAN.md` |
| **Illustrator retrieval-first** — search the 201-card library and call a model only when nothing matches, falling toward zero as the library fills | ~0.85 | The library-first gate, WA-12, and option C in `CODE-PLAN.md §8` |

**The larger of those two savings is now confirmed, not assumed.** The Illustrator's
retrieval-first gate only works if *"sneakers"* finds the existing *Shoes* card, which
needs ODC **semantic search** — a Beta feature we could not switch on ourselves. OutSystems
confirmed on 30 October that it is enabled automatically on hackathon instances
(`ODC-GROUNDING.md §4`). Without it the fallback was a normalised label match plus a
synonym table, which would have missed real synonyms, generated duplicate pictures, and
pushed the ~0.85 saving back toward zero — taking the 37% figure with it. **The budget in
this document now rests on a confirmed platform feature rather than a hoped-for one**,
which is the single most load-bearing thing the Slack answer bought.

| Design | Requests per board | 480 runs | Licensed ceiling |
|---|---|---|---|
| Three model calls, blended | ~4 | ~1,870 | **89% — fails** |
| **Gated, blended** | **~1.6** | **~770** | **37% — comfortable** |

**This does not cost us the agentic story, and that is worth being precise about.** The
three agents remain three agents: the Reviewer still owns validation and the Illustrator
still owns artwork. What changes is that each one answers from a rule or from the library
when it can, and reaches for a model when it cannot. A gate in front of a model call is
better engineering than a model call every time, and it is the same gate the clinical
design already wanted — the same activity should keep the same picture forever.

**The convergence is worth noticing.** Option C in `CODE-PLAN.md §8` was chosen to avoid
an unverified dependency cycle between two apps. It turns out to also be the choice that
makes the request budget work. Two independent reasons for the same decision is the
strongest signal available this week.

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
Demo-critical consumption, in REQUESTS (the binding unit, see §2):
  12 full takes of a 5-minute video          (realistic for a live-app walkthrough)
  × 3 boards generated per take              = 36 runs
  + rehearsal on day 8                       = ~40 runs
  ────────────────────────────────────────────────────────────
  76 runs × 1.6 requests per gated board       ~122 requests
  × 1.3 safety factor                          ~160 requests

RESERVE = max(30% of the request cap, 160 requests)

  Licensed Customers: max(630, 160)          = 630 requests
  Personal Edition:   max(1200, 160)         = 1,200 requests
```

**The floor has stopped being the operative half.** Under the old token framing the
percentage was generous and the floor did the work; in requests it is the other way round
— 30% binds on both rows, and the demo itself needs only ~160. That is the one piece of
genuinely good news in this revision: recording the video is cheap, and the risk is
concentrated in the build days, where it can be managed.

Spendable after the reserve: **1,470 requests** as a Licensed Customer, 2,800 in Personal
Edition. Against a gated need of ~770, that is roughly a 2× margin — which is the margin
this build should have, given that 480 runs is itself an estimate.

**The reserve is not a guideline, it is enforced.** See §6.

## 5. Spending the rest

The spendable pool is `cap − reserve`, apportioned by build day as a percentage so the
plan survives either row of the §2 table. Read the percentages against **requests** now,
not tokens:

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

**ODC has one of its own, and we should use both.** When adding an AI model in the Portal
there is a **Usage limit** section that sets a *daily token limit* on the model connection.
That is a platform-enforced ceiling we get for free, and it is worth setting on day 3.

It does not replace ours, for two reasons: it is a *token* limit, and §2 establishes that
our binding constraint is *requests*; and a platform cap simply fails the call, where ours
degrades to the deterministic template board so the parent still gets something. Set the
platform limit as a backstop; keep the wrapper as the behaviour.

**A third control, found 30 October: the Call Condition.** The `Call Agent` element's
**Action calling settings** take a *Call Condition*, and the documented example of one is
**a token usage limit** — described in the *Agent Workbench* lesson as a safeguard "to
prevent an agent from consuming excessive resources during runtime." So there are three
ceilings available, at three different scopes:

| Control | Scope | Unit | What happens at the limit |
|---|---|---|---|
| Portal **Usage limit** on the model | the whole model connection, per day | tokens | the call fails |
| `Call Agent` **Call Condition** | one agent's action calling | tokens (configurable) | the action call is not made |
| Our wrapper (below) | one board, one family, the whole run | requests | falls back to the template board |

The Call Condition is the one that fits the failure mode §3a actually fears — an agent that
keeps calling an action in a loop and burns the allowance in minutes. **Set it on every
`Call Agent` element that has an action attached**, and still keep the wrapper, which is
the only one of the three that degrades gracefully instead of failing.

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

**Partly solved, confirmed 30 October.** The Trial Model details page in the Portal shows
consumption against the caps, so the daily comparison below is a real reconciliation. It
is a page rather than an API, so it is a human step in §7's ritual, not an automated one.

Agent Workbench's product documentation also claims
built-in observability that tracks reasoning, response quality **and costs in real time**,
and that models can be swapped to trade cost against quality without rewiring logic. If
that surfaces a per-team token figure, §6.3 becomes a real reconciliation rather than a
hope. Check it in the first hour on 2 November.

It does not make §6.1 redundant. Platform observability reports; it does not *enforce*.
The reserve needs a circuit breaker that refuses a call (§6.2), and that has to live in
our wrapper. Instrument anyway, and treat the platform figure as the authority to
reconcile against.

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

1. ~~What is the token allocation, in tokens?~~ **Answered 30 Oct, and in the wrong
   unit from what we expected — see §2.** What remains: **is our tenant a Licensed
   Customer or Personal Edition** (open item 12), and is the cap per team or per account?
2. Is image generation on the same meter or a separate per-image quota?
3. Which models are available, and does the allocation differ between them?
4. ~~Where can a team see its own consumption to date?~~ **Answered 30 Oct:** the
   **Trial Model details** page in the ODC Portal.
5. ~~What happens at exhaustion?~~ **Answered 30 Oct: a hard stop.** Reaching a trial
   limit prevents further use of that model. Whether a team can *ask* for more is still
   open, and is now the version of this question worth asking.
5a. **Is the hackathon's AI token allocation the trial-model allowance, or additional to
   it?** The FAQ promises AWS and Microsoft AI services *"free of charge, but with some
   limitations"*; the Portal documents trial models with their own limits. These may be
   the same thing described twice, or two pools. The §4 reserve is sized against one
   number, so it matters which.
6. **Do Mentor Web and Mentor Studio draw on the same allocation?** The ODC getting-
   started page presents both as first-class ways to build: Mentor Web generates an app
   from a prompt in the Portal, Mentor Studio assists inside ODC Studio. Both are
   model-backed. If they bill against the same metered pool as our three agents, then
   scaffolding screens spends the budget this document reserves for boards, and that
   changes whether we use them at all. Nothing we have read says either way.

~~Question 4 is the one to push on.~~ **It resolved in our favour.** OutSystems does
expose a usage figure, so §6.3 is a real reconciliation rather than a hope, and §6.1's
`TokenUsage` entity becomes a cross-check and a per-board attribution record rather than
the only source of truth. Its justification changes but its necessity does not: the Portal
page is a page for a human to read, not a feed our circuit breaker can query, and it
cannot say which board cost what.

**Question 1 is now the one to push on**, and the answer may already be on the Trial Model
details page rather than in anyone's gift.
