# Pre-build lab

What the AWS account is for between now and the kickoff, and what it is not for.

Written 25 October 2026. Companion to [`TOKEN-BUDGET.md`](TOKEN-BUDGET.md),
[`AWS-ARCHITECTURE.md`](AWS-ARCHITECTURE.md) and
[`NOTES-ARCHITECTURE-REVIEW.md`](NOTES-ARCHITECTURE-REVIEW.md).

---

## 1. The boundary, stated once

**The submission is built in OutSystems Developer Cloud.** Scoring criterion one is
*"application of the ODC features presented during the kick-off"*; the prizes are ODC
licences; the registration is for an ODC hackathon. That is settled.

**The AWS CLI cannot build it.** There is no `aws odc …`. ODC is provisioned and operated
by OutSystems inside accounts we do not hold, and we reach it through ODC Studio and the
ODC portal. An AWS CLI build would be a different, non-qualifying project.

So the AWS account is not the build. **It is the lab bench** — and it is a good one,
because of an accident of the calendar.

## 2. The eight idle days

ODC access arrives only *after* registration closes on 28 October, and possibly not until
the 2 November kickoff. That leaves roughly eight days in which the submission cannot be
touched. The build window that follows is seven days.

The highest-value work available in those eight days is the work that is **portable** —
artifacts that are identical whether a model is called from our own account or from Agent
Workbench:

| Portable (do it now) | Not portable (needs ODC) |
|---|---|
| Composer and Reviewer prompt text | Screens, server actions, entities |
| The JSON output contract | Validators, the three-word check |
| Measured token cost per board | Twilio webhook, the SMS loop |
| Measured latency per board | Agent Workbench wiring |
| Card image style and prompt wording | The print sheet |
| A seeded starter card library | Everything the demo video shows |

Prompt engineering is the long pole and the highest-failure-rate phase of the build —
[`TOKEN-BUDGET.md §5`](TOKEN-BUDGET.md) allocates it the largest share of spendable
tokens precisely because that is when prompts are wrong and runs fail. Moving that
failure into the eight free days, on a separate budget, is the single biggest schedule
win available.

**What transfers on 2 November:** prompt text, the contract, the measured numbers, and a
library of card images already generated and chosen. What we paste into Agent Workbench
is then a known-good prompt rather than a first draft.

## 3. Cost guard — before a single model call

The hackathon's free tokens live in the ODC instance. **They are not in this account.**
Every lab call is billed to the card on this AWS account.

Text is cheap — a board costs fractions of a cent. Image generation is billed *per image*
and is where a careless loop becomes real money. So the budget comes first, not after:

```bash
aws configure set region us-east-1
ACCT=$(aws sts get-caller-identity --query Account --output text)

cat > /tmp/budget.json <<'EOF'
{ "BudgetName": "avs-lab", "BudgetType": "COST", "TimeUnit": "MONTHLY",
  "BudgetLimit": { "Amount": "25", "Unit": "USD" } }
EOF

cat > /tmp/notify.json <<'EOF'
[ { "Notification": { "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN", "Threshold": 50,
      "ThresholdType": "PERCENTAGE" },
    "Subscribers": [ { "SubscriptionType": "EMAIL",
      "Address": "REPLACE@example.com" } ] } ]
EOF

aws budgets create-budget --account-id "$ACCT" \
  --budget file:///tmp/budget.json \
  --notifications-with-subscribers file:///tmp/notify.json
```

Twenty-five dollars is deliberately low. If the lab approaches it, something is looping.

## 4. The measurement programme

The per-board figures in [`TOKEN-BUDGET.md §3`](TOKEN-BUDGET.md) are *estimates* derived
from the output contract. The lab replaces them with facts, and the facts land in the same
CSV the build-week tracker already reads — so the estimate quietly becomes a measurement
without any other document changing.

```bash
# What models this account can actually reach (they must be enabled in the
# console first -- a fresh account has no model access by default).
aws bedrock list-foundation-models --region us-east-1 \
  --query 'modelSummaries[].modelId' --output text | tr '\t' '\n' | sort

# One Composer call, with its token usage printed and logged.
python3 tools/lab-measure.py --prompt prompts/composer-draft.txt --op Composer
```

`tools/lab-measure.py` calls Bedrock through the AWS CLI, prints the input and output
token counts from the response, and appends a row to
[`tools/token-log.csv`](tools/token-log.csv) — the same file
`tools/token-budget.py` reads. Run twenty boards and `--allocation` projections stop
being guesswork.

**Five questions the lab answers before the kickoff, each of which is otherwise a day-3
discovery:**

1. What does one board actually cost in tokens?
2. How long does one board actually take, end to end?
3. Does the Reviewer converge, and in how many cycles?
4. Is image generation billed per image or per token, and what does a card look like?
5. Which model is good enough for the Reviewer — because
   [`WA-15`](NOTES-ARCHITECTURE-REVIEW.md) argues most of its job should not be a model
   call at all, and the lab is where that gets proved rather than asserted.

## 5. Well-Architected review schedule

Three passes, not one. The design-stage review is already written; the value of the later
two is that they run against code rather than intent.

| When | Scope | Against |
|---|---|---|
| **Done — 24 Oct** | All six pillars, by hand | The specification |
| **6 Nov, day 5** | Security and Reliability only | The real application, once the agent pipeline and the data model exist |
| **8 Nov, day 7** | All six pillars | The complete application, before the demo is recorded |

The 6 November pass is scoped deliberately. Mid-build, only two pillars can produce
findings that are still cheap to act on; a full review on day 5 generates Cost and
Sustainability findings that compete with shipping.

The `aws-well-architected-review` skill installed by the agent toolkit works from code,
IaC and configuration, so it has nothing to analyse until there is an application. Its
output cites best-practice IDs, which is the vocabulary an AWS-track reviewer reads in —
worth having on day 7 even though the manual review already covers the same ground.

**Caveat:** the skill is written for AWS workloads. ODC is managed, so a large fraction of
its checks will be inapplicable or unanswerable for the same reason Trusted Advisor is.
Expect to discard the infrastructure findings and keep the application ones. The trust
boundaries in [`AWS-ARCHITECTURE.md §2`](AWS-ARCHITECTURE.md) are the filter: a finding
that lands on B2, B3, B4, B6 or B7 is ours and actionable, and one that lands below the
ODC line is not.

## 6. Trusted Advisor — a correction

Earlier notes said Trusted Advisor could not be run against this project. That remains
true **for the ODC tenant**, and for the reason given: it is an account-level inspector
and we hold no account there.

It is no longer true for the **lab account**, which we now do hold. Trusted Advisor can
inspect it for service quotas, cost and security.

Two things keep this modest rather than exciting:

- On Basic support, Trusted Advisor exposes only a limited check set — service quotas and
  a handful of security checks. The full set needs Business or Enterprise support.
- The lab account is not the submission. Findings there are about our own hygiene, not
  about the application being judged.

Worth one run after the first week of lab work, mainly to confirm nothing was left
running.

## 7. Setup, in order

Current state, verified 25 October: **AWS CLI 2.38.5 installed; the agent toolkit
installed 24 skills into `~/.claude/skills`; no credentials, no region, no profile.**
`aws configure agent-toolkit` installs skills — it does not sign you in.

1. `aws configure sso` *(preferred)* or `aws configure` with an access key.
2. `aws configure set region us-east-1` — Bedrock model availability varies by region;
   `us-east-1` and `us-west-2` are the safe choices.
3. `aws sts get-caller-identity` — confirms the credentials resolve.
4. **Enable model access** in the Bedrock console. A fresh account has none, and this is
   the step most likely to be mistaken for a broken credential.
5. Create the budget (§3).
6. `aws bedrock list-foundation-models` — confirms what is actually reachable.
7. Start measuring (§4).

Steps 1–4 are worth doing today. Everything in §4 depends on them, and the eight free
days are the whole point.
