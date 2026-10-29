# AWS architecture

The system of record for every AWS service in the path, who owns it, and where the
security controls go.

Companion to [`NOTES-ARCHITECTURE-REVIEW.md`](NOTES-ARCHITECTURE-REVIEW.md) (the
Well-Architected findings) and [`TOKEN-BUDGET.md`](TOKEN-BUDGET.md) (AI consumption).

---

## The shape of this document, and why

A conventional AWS architecture document specifies an account, a VPC, subnets, security
groups and IAM roles. **This system has none of those to specify**, and that is a finding
rather than an omission.

OutSystems Developer Cloud is a managed platform. OutSystems runs it on AWS in accounts
they own; we receive a tenant. The OutSystems evaluation guide is explicit that for ODC
the customer's infrastructure decision is *region selection* — there is no statement
anywhere in their documentation about customers provisioning AWS accounts, VPCs or
infrastructure, and the opposite is stated for OutSystems 11 Cloud, where OutSystems
provisions it on the customer's behalf.

So this document does the thing that is actually useful and actually possible:

1. Enumerate every component, labelled by **how sure we are** and **who owns it**.
2. Draw the trust boundaries.
3. Put each security control on the boundary it defends — and show that the boundaries
   *we* own number four, are individually small, and are completely enumerable.

A small, fully-enumerated attack surface is a stronger security position than a large one
with a thick document in front of it. The useful claim this design makes is not "we have
hardened AWS." It is: **here is every place an attacker can reach us, and here is the
control on each one.**

## Confidence labels

| Label | Means |
|---|---|
| **Confirmed** | Stated in the hackathon rules/FAQ, or in official OutSystems documentation read directly |
| **Likely** | Consistent third-party or marketing sources, not confirmed in official docs |
| **Unknown** | Needs an answer at the 2 November kickoff |

Nothing below is designed to depend on an **Unknown**. Where one exists, the fallback is
named.

---

## 1. Component inventory

### 1.1 Edge and transport — OutSystems-owned

| Component | AWS service | Confidence | What we configure |
|---|---|---|---|
| Content delivery | CloudFront or equivalent CDN | Likely | Nothing |
| Web application firewall | AWS WAF | Likely | Nothing |
| Request routing, load balancing | **Amazon API Gateway** | **Confirmed** | Nothing |
| TLS termination | Managed | **Confirmed** | Nothing |
| Multi-AZ resiliency, health checks, autoscaling | Managed | **Confirmed** | Nothing |

The evaluation guide names API Gateway and states that OutSystems manages resiliency,
load balancing, health monitoring, scaling and backups. CDN and WAF come from a
third-party architecture summary, hence *Likely*.

### 1.2 Application runtime — OutSystems-owned, our code inside it

| Component | AWS service | Confidence | What we configure |
|---|---|---|---|
| Application containers | ECS/EKS, OutSystems-managed | Likely | Nothing |
| Dev / Test / Production stages | Separate runtimes | Likely | Which stage we deploy to |
| Region | Customer choice | **Confirmed** | **The one infrastructure decision we make** |

**Region decision:** US region. The data subjects are US children and the test user is in
the US; there is no reason to place special-category data about minors in a jurisdiction
we have no connection to. Confirm at provisioning, because it is not changeable later
without a migration.

### 1.3 Data — OutSystems-owned infrastructure, our schema

| Component | AWS service | Confidence | What we configure |
|---|---|---|---|
| Relational database | **Aurora Serverless v2**, encrypted at rest | **Confirmed** | The ten entities, indexes, delete rules |
| Per-stage isolation | One encrypted database per stage | Likely | Nothing |
| Backups | Managed | **Confirmed** | Nothing |
| Secret storage | **AWS Secrets Manager** behind ODC's secret management | Likely | Which values go in it |
| Identity and sessions | ODC built-in identity service | Likely | Roles, and the isolation rule in every query |
| Generated card images | ODC binary storage, likely S3-backed | Likely | What we store, and the deletion path |

### 1.4 AI — the one AWS service our code reaches out to

| Component | AWS service | Confidence | What we configure |
|---|---|---|---|
| Text generation (Composer, Reviewer) | **Amazon Bedrock** | Likely | Model choice, prompts, temperature |
| Image generation (Illustrator) | Bedrock Titan/Nova Canvas, or Azure | **Unknown** | Prompts, size, library-first gating |
| Agent orchestration | **ODC Agent Workbench** | **Unknown** (availability) | Agents, tools, knowledge source, guardrails |
| Token metering | Provided, limited, monitored | **Confirmed** that it exists; amount **Unknown** | Our own `TokenUsage` logging |

`faq.txt:36` confirms AWS and Microsoft AI tokens are *"integral to the ODC instance"* and
*"limited, and usage will be monitored."* It never names Bedrock — hence *Likely*.

**Fallback if Agent Workbench is unavailable:** the three agents become three server
actions calling the model directly, orchestrated in ODC logic. We lose the visible
reasoning path, which is a scoring loss, not a functional one. The JSON output contract
in [`SPEC.md §5`](SPEC.md) is what makes this substitution cheap — the contract is the
interface, not the tool.

**Fallback if Bedrock is not pre-wired:** the `Amazon Bedrock Connector (ODC)` on Forge.
Community-supported, v0.1.2, May 2024, explicitly *"not supported by OutSystems."* Usable,
but not something to discover a dependency on during a seven-day build — which is why
this is a kickoff question.

### 1.5 Messaging — not AWS, and the only third party we hold credentials for

| Component | Service | Confidence | What we configure |
|---|---|---|---|
| Outbound caregiver script | **Twilio Programmable SMS** | **Confirmed** as required | Message content, send trigger |
| Inbound reward confirmation | Twilio → our exposed ODC REST endpoint | **Confirmed** supported | The endpoint, its auth, its idempotency |
| Credentials source | Provided with instance, or our own account | **Unknown** | Where the auth token is stored |

`rules.txt:36` makes Twilio use a condition of the Twilio prize. A Forge component
`Twilio Messaging (ODC)` v0.1.1 exists and returns the message SID — useful, because that
SID is the idempotency key the design needs.

### 1.6 What is explicitly *not* in this system

Stated so no reviewer looks for it:

- No customer AWS account, VPC, subnets, NAT gateways, security groups or route tables.
- No IAM roles, policies or cross-account trust relationships of ours.
- No S3 bucket policies, KMS key policies or CloudFront distributions of ours.
- No Terraform, CloudFormation or CDK. There is nothing for infrastructure-as-code to
  describe, because we provision no infrastructure.
- No external analytics, no third-party image libraries, no CDN of our own.
- No training use of any profile data.

---

## 2. Trust boundaries

```
         Parent (browser / tablet)                    Parent's phone
                    │                                       │
            HTTPS   │                                  SMS  │
                    ▼                                       ▼
   ─ ─ ─ ─ ─ ─ ─ ─ B1 ─ ─ ─ ─ ─ ─ ─ ─               ┌───────────────┐
  ╔═════════════════════════════════════╗           │    Twilio     │
  ║  OUTSYSTEMS-MANAGED  (AWS, their    ║           │ Programmable  │
  ║   accounts — we configure none)     ║           │      SMS      │
  ║                                     ║           └───┬───────▲───┘
  ║   CDN → WAF → API Gateway           ║      HTTPS    │       │
  ║              │                      ║      POST     │       │ B6
  ║              ▼                      ║               │       │
  ║  ┌───────────────────────────────┐  ║ ─ ─ ─ ─ ─ B3 ─┘       │
  ║  │   ODC application runtime     │◄─╫───────────────────────┘
  ║  │   containers · multi-AZ       │  ║
  ║  │                               │  ║
  ║  │  ┌─────────────────────────┐  │  ║
  ║  │  │  OUR CODE               │  │  ║   ← the whole of our
  ║  │  │  screens                │  │  ║     security responsibility
  ║  │  │  server actions         │  │  ║
  ║  │  │  validators             │  │  ║
  ║  │  │  exposed REST + OnReq   │  │  ║
  ║  │  │  agent + tool defs      │  │  ║
  ║  │  └───────┬────────┬────────┘  │  ║
  ║  └──────────┼────────┼───────────┘  ║
  ║        B2   │        │   B4         ║
  ║      ┌──────▼──┐  ┌──▼───────────┐  ║
  ║      │ Aurora  │  │ Agent        │  ║
  ║      │ Svls v2 │  │ Workbench    │  ║
  ║      │ (enc.)  │  └──────┬───────┘  ║
  ║      └─────────┘         │          ║
  ║      ┌─────────┐         │ B5       ║
  ║      │ Secrets │         │          ║
  ║      │ Manager │         │          ║
  ║      └─────────┘         │          ║
  ║      ┌──────────┐        │          ║
  ║      │ Identity │        │          ║
  ║      └──────────┘        │          ║
  ╚══════════════════════════╪══════════╝
                             ▼
                  ┌─────────────────────┐
                  │   Amazon Bedrock    │
                  │   text + image      │
                  └─────────────────────┘

        B7 — data at rest: their encryption, our minimisation
```

| # | Boundary | Owner | Control |
|---|---|---|---|
| **B1** | Internet → ODC edge | OutSystems | TLS, WAF, API Gateway. Inherited; nothing for us to configure |
| **B2** | Authenticated parent → data | **Ours** | Tenant isolation in every query |
| **B3** | Twilio → our exposed endpoint | **Ours** | HMAC signature validation + idempotency |
| **B4** | Our code → the agent | **Ours** | Tool parameter design |
| **B5** | Agent → Bedrock | Shared | We own prompt content; they own transport and credentials |
| **B6** | Our code → Twilio outbound | **Ours** | Server-resolved destination, validated content |
| **B7** | Data at rest | Shared | They encrypt; we minimise and provide deletion |

**Four boundaries are fully ours** (B2, B3, B4, B6), **two are shared** (B5, B7), and one
is inherited entire (B1). Each of the six we touch gets one named control below.

Rendered as an image: [`assets/trust-boundaries.png`](assets/trust-boundaries.png).
A cut-down variant without the key column carries the same drawing on slide 10 of
the overview deck: [`assets/trust-boundaries-slide.png`](assets/trust-boundaries-slide.png).
Both come out of `assets/build_diagram.py`, so the slide cannot drift from the reference.

---

## 3. The security design

### B2 · Tenant isolation — the control that matters most

Every entity hangs off `ChildId` or `BoardId`. The failure mode is one parent reading
another family's child profile, and in a model this heavily keyed by id it is the single
likeliest bug in the build.

**Control.** Every server action touching child-scoped data filters on the *authenticated
user's* id inside the query itself — never on an id received from the client, the URL or
an agent. Return not-found rather than unauthorised, so the endpoint does not confirm
that another family's record exists.

**Why this and not row-level security:** we are writing the first server action on day 3.
Establishing the pattern once, in the first one, means the remaining six days inherit it.
Retrofitting isolation across thirty server actions on day 8 is how this bug ships.

### B3 · The inbound webhook — the only unauthenticated path into the system

Everything else requires a logged-in parent. This one endpoint accepts a request from the
public internet and writes `UsageLog.RewardDelivered`, which is the field the entire
product thesis rests on. Unprotected, anyone who learns the URL can forge kept promises
and corrupt the only number the home screen reports.

**Control, two parts.**

1. **Signature validation.** Twilio HMAC-SHA1-signs the full URL plus the sorted POST body
   using the account auth token. Recompute and compare; reject on mismatch before
   touching the database. ODC runs `OnAuthentication` and `OnRequest` callbacks on an
   exposed REST API *before* the method body — the check belongs in a callback, not in the
   method, so that a method added later cannot forget it.
2. **Idempotency.** Twilio retries any webhook that does not return 2xx promptly. Store
   the Twilio `MessageSid` on `UsageLog` under a unique index and make the write an
   upsert. Return 2xx fast; do the work after.

**Open item:** the ODC docs describe the callback sequence but do not state whether an
exposed method can read an arbitrary inbound header such as `X-Twilio-Signature`. Verify
in ODC Studio on day 2 — this control depends on it. If headers are not reachable, the
fallback is a high-entropy secret path segment plus a shared token in the body, which is
weaker and should be treated as a last resort.

### B4 · The agent tool surface — the confused-deputy boundary

The Composer reads free text a parent typed — `Obstacle`, `SensoryNotes`, `TriggerNotes`,
`SpecialInterests` — and holds a tool that sends SMS. Untrusted input, private data about
a child, and an outbound channel in one context is the classic lethal combination.

**Control.** No tool parameter is ever an identity or a destination.

| Tool | Takes | Never takes |
|---|---|---|
| `GetChildProfile` | nothing — resolves from session | a `ChildId` |
| `SendRoutineSms` | `BoardId` | a phone number |
| `CreateBoard`, `AddCard`, `SetScript`, `SetPlan` | content | an owner id |
| `GenerateCardImage` | a prompt, server-sanitised | a URL or a path |

The model decides *whether* and *what*. The server decides *who* and *where*. Every tool
is a server action that re-validates its inputs, because a tool call is an untrusted
input even when the caller is our own agent.

### B5 · Prompt content — what crosses into Bedrock

**Control.** The child's name never leaves the application. Image prompts say "a child."
Text prompts carry the profile *attributes* needed for the board — developmental stage,
language level, interests — and never the nickname. No profile data is used as training
input; model invocation is inference only.

### B6 · Outbound SMS — read off a lock screen

The script is deliberately sent when the parent's hands are full, which means it is read
from a notification on a locked phone, possibly in public. SMS is also unencrypted across
the carrier network.

**Control.** A validator on `CaregiverScript.PhraseText`, the same shape as the three-word
label check: the routine only. *"First shoes, then swing."* Never the nickname, never a
sensory or trigger note. The destination number is resolved server-side from the
authenticated owner (B4), never from message content or an agent parameter.

### B7 · Data at rest — minimisation is our half

The profile holds developmental stage, language level, sensory notes and trigger notes:
data concerning health, about a child. OutSystems encrypts it. The part encryption cannot
do for us is not collect it.

**Controls.** `Nickname` only, never a legal name. Parent-owned export and delete, with
the deletion path covering generated card images, which are derived personal data.
No profile text in any log line, error message or agent trace that outlives the request —
`Board.AgentRunId` is good observability and a PII channel, so traces inherit the
profile's protections and retention.

### Credentials

All secrets in ODC's secret management, which is Secrets Manager underneath — never in
Application Settings, never in code, never in this repository, which is public and MIT.

**Specific caveat:** the Forge `Twilio Messaging (ODC)` connector stores credentials in
*Application Settings* by default. If we adopt it, the auth token must be relocated. That
token is also the HMAC key for B3, making it the most sensitive value in the system.

---

## 4. For an AWS-track reviewer: the native equivalent

Not a plan — the hackathon requires ODC, and nothing here is a recommendation to leave it.
Included because an AWS reviewer will reasonably ask what ODC is doing on our behalf.

| This system | Hand-built AWS equivalent | What ODC saves us |
|---|---|---|
| ODC runtime | ECS Fargate behind an ALB | Cluster, task definitions, autoscaling, deploys |
| Per-stage databases | Aurora Serverless v2 × 3 | Provisioning, encryption, backups, failover |
| ODC identity | Amazon Cognito | User pools, token handling, session management |
| Agent Workbench | Bedrock Agents + Step Functions | Orchestration, traces, tool wiring, evals |
| Exposed REST | API Gateway + Lambda | Routing, throttling, stage management |
| **Webhook auth** | **API Gateway + Lambda authorizer doing the HMAC** | *Nothing — this one is still ours either way* |
| Card images | S3 + CloudFront, signed URLs | Buckets, policies, invalidation |
| Secrets | Secrets Manager | Rotation, access policy |
| Observability | CloudWatch + X-Ray | Dashboards, log groups, alarms |
| Token metering | CloudWatch metrics on Bedrock `InvokeModel` | *Nothing — see below* |

Two rows are worth a reviewer's attention, because they are the two the platform does
*not* solve:

- **Webhook authentication is ours on either architecture.** A managed platform does not
  authenticate a third party's callback for you. This is why B3 is the top finding in the
  Well-Architected review rather than a checklist item.
- **Token metering is ours *because* of the platform.** On native AWS we would read
  `InvokeModel` token metrics in CloudWatch. Here the tokens are provisioned into an
  instance OutSystems owns, so there is no console for us to read, and consumption has to
  be recorded by the application or it is invisible. That is the reason `TokenUsage`
  exists as a tenth entity. See [`TOKEN-BUDGET.md`](TOKEN-BUDGET.md).

The same logic explains why **AWS Trusted Advisor cannot be run against this project** —
it is an account-level inspector and we hold no account. Its five check categories are
run manually instead, in
[`NOTES-ARCHITECTURE-REVIEW.md`](NOTES-ARCHITECTURE-REVIEW.md) Part 2.

---

## 5. Open items

Each has a named fallback, so none of them blocks the build.

| # | Unknown | Resolve | Fallback if the answer is bad |
|---|---|---|---|
| 1 | Can an exposed method read an inbound HTTP header? | ODC Studio, day 2 | Secret path segment + body token (weaker) |
| 2 | Is Agent Workbench enabled on hackathon instances? | Kickoff | Three server actions against the JSON contract |
| 3 | Is Bedrock pre-wired, or do we need the Forge connector? | Kickoff | Forge connector, community-supported |
| 4 | Which image model, and is it metered per image or per token? | Kickoff | Hand-seed the card library |
| 5 | Are Twilio credentials provided? | Kickoff | Own trial account, number verified day 2 |
| 6 | Token allocation, and where we can see consumption | Kickoff | Our own `TokenUsage` logging either way |
| 7 | Region available for provisioning | Provisioning | US region required |

Items 2–6 are questions in `email-4-kickoff-questions.txt`.

---

*First → Then. Print it, post it, trust it.*
