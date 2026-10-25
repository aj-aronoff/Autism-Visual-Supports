# Architecture review notes

An architecture review of **Autism Visual Supports** against the **AWS Well-Architected
Framework**, plus a manual pass using the **AWS Trusted Advisor** check categories.
Written 24 October 2026, before the build window opens.

---

## Scope, and one honest caveat

This application is built on **OutSystems Developer Cloud**, a managed platform. ODC runs
on AWS, but the account is OutSystems', not ours — we get an ODC tenant and metered
tokens for AWS and Microsoft AI services, not an AWS console.

That has a direct consequence for the second half of the request:

> **AWS Trusted Advisor cannot be run against this project.** Trusted Advisor is an
> account-level inspector — it reads your own AWS account's resource configuration,
> billing data and service quotas and reports on them. There is no AWS account here to
> point it at, and no IAM principal we hold that could authorise it.

What *is* valid, and what Part 2 does, is to take Trusted Advisor's five check categories
and run them by hand against the parts of the stack we do control. The categories are a
good checklist; it is only the automation that is unavailable.

The Well-Architected review in Part 1 has no such limitation. The framework is a set of
design questions, not a tool, and the shared-responsibility line simply moves: the
platform owns the pillars below the application, and we own everything above it.

## Why this is worth an hour before the build starts

Two reasons beyond diligence.

**AWS is a judging track.** The Taikai platform lists three voting tracks — Global Results,
**AWS**, and Microsoft. A reviewer on the AWS track reads architecture in Well-Architected
vocabulary. Having answered its six pillars in writing, in the repository, before the
build, is cheap and it is the language that reader already speaks.

**The tokens are metered.** `faq.txt:36`: *"AWS and Microsoft will offer tokens for their
respective AI services, which will be integral to the ODC instance. These tokens will be
limited, and usage will be monitored."* Cost Optimization is therefore not a theoretical
pillar in a seven-day hackathon — it is a hard constraint with a cliff at the end of it,
and the cliff is on the days the demo gets recorded.

---

# Part 1 — Well-Architected review

Findings are numbered `WA-n` and carry a severity. The ones marked **critical** are
design flaws that would be defects in a shipped product, not hackathon shortcuts.

## Pillar 1 — Security

### WA-1 · critical · The inbound Twilio webhook is an unauthenticated public endpoint

The reward-confirmation loop receives the parent's SMS reply on an ODC-exposed REST
endpoint. Exposed REST in ODC is public by default. As designed, anyone who learns that
URL can `POST` a forged reply and write `UsageLog.RewardDelivered = True`.

That is not a generic injection worry. `RewardDelivered` is the one field the entire
product thesis rests on — the home screen reports promises kept — so an unauthenticated
write path to it corrupts the only number that matters.

**Fix:** validate Twilio's `X-Twilio-Signature` header on every inbound request. Twilio
HMAC-SHA1-signs the full URL plus the sorted POST body with the account auth token;
recompute it and reject on mismatch before touching the database.

ODC gives this a named home. An exposed REST API runs callbacks in sequence on each
request, and two of them fit exactly: `OnAuthentication` for custom authentication, and
`OnRequest` for logic over the request after it arrives. The signature check belongs in
one of those rather than inside the method body, so no method can be added later that
forgets it. Half an hour of work on day 7, and it converts the endpoint from open to
authenticated.

### WA-2 · critical · `SendRoutineSms` must not take a destination number from the agent

The Composer agent reads free text a parent typed — `Obstacle`, `SensoryNotes`,
`TriggerNotes`, `SpecialInterests` — and holds a tool that sends SMS. Untrusted input,
private data about a child, and an outbound channel in the same context is the classic
confused-deputy shape. If the phone number is a parameter the model fills in, text in a
profile field can in principle redirect a message.

**Fix:** `SendRoutineSms` takes a `BoardId` and nothing else. The server action resolves
the destination number from the authenticated owner's record. The model gets to decide
*whether* and *what*, never *to whom*. Same rule for every tool: no tool parameter is
ever an identity or a destination.

### WA-3 · high · Tenant isolation belongs in the server action, not the query

`GetChildProfile` receives a `ChildId`. Every entity in the model hangs off `ChildId` or
`BoardId`. If any server action trusts an identifier handed to it — by the client or by
an agent — one parent can read another family's child profile. In a data model this
heavily keyed by id, that is the likeliest single bug in the build.

**Fix:** every server action that reads or writes child-scoped data filters on the
authenticated user's id in the query itself, and returns not-found rather than
unauthorised. Write it once as a pattern on day 3 and the remaining six days inherit it.

### WA-4 · high · This is special-category data about a minor

The child profile holds developmental stage, language level, sensory notes and trigger
notes. That is data concerning health, about a child, under GDPR Article 9 — and the
account holder is the parent while the data subject is the child, which is the awkward
case in every privacy regime. The hackathon does not require compliance, but a judge may
well ask, and the answer should be architecture rather than a promise.

**Fix, and most of it is already in the spec:** data minimisation (no legal name — the
model has `Nickname` and should keep it that way), parent-owned export and delete, no
profile data as training input, and ODC's platform encryption at rest and in transit.
Add one thing not yet written down: a documented deletion path that removes the card
library images too, since those are derived personal data.

### WA-5 · medium · SMS content lands on a lock screen

The outbound script is deliberately sent at the moment the parent's hands are full,
which means it is read off a notification on a locked phone, possibly in public. SMS is
also unencrypted across the carrier network.

**Fix:** extend the existing no-name-in-image-prompts rule to SMS. The script text ships
as *"First shoes, then swing."* — the routine, never the nickname, never a sensory or
trigger note. The guardrail is a validator on `CaregiverScript.PhraseText`, same shape as
the three-word check.

### WA-6 · medium · Credentials in the ODC secret store

Twilio account SID, auth token, and the model endpoint keys. None in application
settings, none in code, none in the repository — the repository is public and MIT.

**Fix:** ODC's secret management only, and a `.gitignore` check before each commit. Worth
one grep over the history before final submission.

**Caveat found while surveying Forge:** the `Twilio Messaging (ODC)` connector stores its
credentials in *Application Settings*, not in the secret store. If we adopt it, the auth
token has to be relocated — and the auth token is also the HMAC key for WA-1, which makes
it the most sensitive value in the application.

## Pillar 2 — Reliability

### WA-7 · high · Twilio trial accounts only send to verified numbers

A trial Twilio project can send SMS only to numbers verified on the console, and prefixes
every message with a trial notice. The headline feature of this application is SMS. If
that is discovered on 7 November it costs a day; if it is discovered while recording on
8 November it costs the submission.

**Fix:** verify the demo phone number on day 2, the same hour the credentials arrive, and
send one test message before building anything on top of it.

### WA-8 · high · The webhook needs an idempotency key

Twilio retries a webhook that does not return 2xx quickly. Without deduplication, a
retried delivery counts one kept promise twice — which again lands on the one metric the
product is judged by.

**Fix:** store Twilio's `MessageSid` on `UsageLog` with a unique index and make the write
an upsert. Return 2xx fast, do the work after.

### WA-9 · medium · The Composer–Reviewer loop must be bounded

Reviewer sends a draft back to Composer on drift. Two generative agents handing work to
each other is a loop with no guaranteed fixed point, and it sits directly on the demo
path.

**Fix:** cap it at two review cycles. On the third failure, fall back to a deterministic
template board — the First–Then layout is two cards and a phrase; it does not actually
require a model. A demo that degrades gracefully beats one that hangs on camera.

### WA-10 · medium · Twilio is a hard dependency on the demo path

**Fix:** keep in-app logging of `RewardDelivered` as a working path, not just a legacy
one. The spec already has screen 7 doing this. It is also the fallback if Twilio is
degraded during judging, and it costs nothing to preserve.

## Pillar 3 — Performance Efficiency

### WA-11 · medium · The two-minute promise is a latency budget, so write it down

"Three questions in, a board out" is the product claim. The work behind it: one Composer
call, up to two Reviewer calls, a library lookup per card, and image generation on a
miss. Image generation dominates.

**Budget:** p50 end-to-end under 45 seconds, p95 under 90. Above that the claim in the
README stops being true, and the fix is architectural rather than cosmetic.

### WA-12 · medium · The card library is a cache — treat it as one and measure it

`CardLibrary` with `TimesUsed` is already the right design, and it is doing cache work:
on a hit, a card costs a database read instead of an image generation. Recognition is the
product reason (the same activity keeps the same picture); latency and cost are the free
side effects.

**Measure:** library hit rate. It is the single number that moves latency, token spend and
energy use together, and it is worth one line on the demo video.

### WA-13 · low · Render the print sheet server-side, once, and cache it

A laminate-ready PDF does not change after the board is final. Generate on first request,
store, serve. Tablet mode works offline, which the spec already requires.

## Pillar 4 — Cost Optimization

### WA-14 · high · Reserve token budget for 8–9 November

The tokens are limited and monitored. The build days that burn them hardest are 5 and 6
November, when the agent pipeline is being iterated. The days that *must not fail* are 8
and 9 November, when the five-minute demo is recorded, probably several times.

**Fix:** instrument consumption in the application — we have no AWS console, so nothing
below the ODC line is visible to us — and enforce a reserve derived from what recording
actually costs, `max(30% of allocation, 500,000 tokens)`, as a circuit breaker in code
rather than a note in a plan. Full model, daily ritual and tracker in
[`TOKEN-BUDGET.md`](TOKEN-BUDGET.md). The cheapest way to protect the reserve is WA-12:
every library hit during a rehearsal is a generation not paid for.

### WA-15 · medium · Match the model to the job

Composer is an author and needs the capable model. Reviewer is a validator: it checks
word counts, phrasing polarity, card presence and card count against fixed rules. That is
small-model work, and four of those checks should not be a model call at all.

**Fix:** mechanical rules in server-action validators; the small fast model for Reviewer's
remaining judgement calls; the large model for Composer only. Cuts the per-board cost and
the latency in WA-11 at the same time.

### WA-16 · low · Generate card images small

Cards are printed at roughly two inches square and displayed as tap targets. There is no
reason to pay for or store large images. Smallest size the generator offers that still
prints cleanly.

## Pillar 5 — Operational Excellence

### WA-17 · medium · `AgentRunId` is good observability — and a PII leak if logged naively

`Board.AgentRunId` giving a traceable path back to the run that produced a board is the
right instinct, and it is exactly what makes agent reasoning demonstrable to a judge.
But an agent trace contains the prompt, and the prompt contains the child profile.

**Fix:** traces are retained with the same protections as the profile, and no profile text
goes to any log line, error message or third-party monitor. There is no external analytics
in this project, which helps.

### WA-18 · medium · Write the demo runbook on day 7, not day 9

The submission is a five-minute video of a path a judge must be able to replicate. That
path should exist as a written script — seed child, routine, expected board, the phone
that receives the SMS, the reply — so that a rehearsal is repeatable and a failure is
diagnosable.

### WA-19 · low · One tool type end to end

Already the plan in `SPEC.md §8`, and it is the correct operational call for a
seven-day window. Recorded here because it is the decision most likely to be second-guessed
on day 5, and it should not be.

## Pillar 6 — Sustainability

### WA-20 · low · The library-first design *is* the sustainability answer

Inference is where the energy goes. A library hit avoids an image generation entirely, and
the design already prefers reuse for a clinical reason. Small cached images, no
regeneration of what exists, a validator in code rather than a model call where a rule
will do. Cost Optimization and Sustainability recommend the same architecture here, which
is the easy case.

---

# Part 2 — Trusted Advisor, run by hand

Trusted Advisor's automated checks need an AWS account we do not have. Its five categories
still map cleanly onto what we control. This is that pass.

| Trusted Advisor category | Automated check needs | Our equivalent, checked manually | Status |
|---|---|---|---|
| **Cost Optimization** | Billing + idle resource data | Daily AI token spend; model-to-task matching; library hit rate | WA-14, WA-15, WA-16 |
| **Performance** | CloudWatch metrics, instance configuration | End-to-end board latency budget; cache hit rate; image sizing | WA-11, WA-12, WA-13 |
| **Security** | IAM, security groups, public resources, key rotation | Public exposed REST endpoints; tool parameter surface; tenant isolation; secret storage | WA-1, WA-2, WA-3, WA-6 |
| **Fault Tolerance** | Multi-AZ, backup and snapshot configuration | External dependency failure modes; webhook retry semantics; agent loop termination; graceful degradation | WA-7, WA-8, WA-9, WA-10 |
| **Service Quotas** | Account quota utilisation | ODC tenant limits; AI token allocation; Twilio trial sending limits | see below |

### Service quotas — the hackathon-specific list

The one Trusted Advisor category worth running explicitly, because every item on it is a
hard stop rather than a degradation, and three of the four are unknown until credentials
arrive:

1. **AI token allocation** — limited and monitored per `faq.txt:36`; amount unknown.
   Find the number on day 2 and divide it by the plan.
2. **Twilio trial limits** — verified destinations only, message volume cap, trial prefix
   on message bodies. Confirm on day 2 (WA-7).
3. **ODC tenant limits** — hackathon instances are not production instances. Check whether
   exposed REST, external SMS callbacks and image storage have caps.
4. **Image generation rate limits** — a demo rehearsal that builds six boards in a row can
   hit a per-minute quota that single-board testing never reveals. Test a burst before
   recording.

**The one question to ask at the 2 November kickoff:** what the token allocation actually
is, and whether it is per team or per account. Everything in Cost Optimization is
guesswork until that number exists.

---

# Part 3 — What this changes in the build

Nothing in Part 1 contradicts `SPEC.md`. Eleven findings are new; the rest confirm
decisions already made. Folded into the existing day-by-day order:

| Day | Added by this review |
|---|---|
| **2 Nov** | Verify Twilio demo number and send one test SMS (WA-7). Find the token allocation (WA-14, quotas). Check tenant limits. |
| **3** | Tenant-isolation pattern in the first server action, inherited by all later ones (WA-3). Secrets into the ODC secret store (WA-6). |
| **3–4** | Mechanical validators in code, not in Reviewer's prompt (WA-15). Bound the review loop with a deterministic fallback (WA-9). |
| **5** | SMS text validator — routine only, never the nickname (WA-5). |
| **5–6** | Library hit rate instrumented (WA-12). Small images (WA-16). Daily token spend logged (WA-14). |
| **7** | `X-Twilio-Signature` validation (WA-1). `MessageSid` idempotency key (WA-8). `SendRoutineSms` takes `BoardId` only (WA-2). |
| **8** | Demo runbook written and rehearsed against the reserved token budget (WA-18). Burst-test image generation (quotas). |
| **8–9** | Record. In-app logging path confirmed working as the Twilio fallback (WA-10). |

Documented, not built, before final submission: the deletion path covering derived card
images (WA-4), and trace retention policy (WA-17).

### The three that are not negotiable

If the seven days compress and something has to go, these do not:

1. **WA-1** — signature validation on the webhook. An open write path to `RewardDelivered`
   invalidates the metric the project is built on.
2. **WA-2** — no destination in an agent tool parameter.
3. **WA-7** — verify the Twilio number on day 2. It is five minutes of work that can cost
   the submission.

---

*First → Then. Print it, post it, trust it.*
