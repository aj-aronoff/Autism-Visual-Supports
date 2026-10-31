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
| Text generation (Composer, Reviewer) | **Amazon Bedrock** | **Confirmed** — two of the three ODC trial models are *via Amazon Bedrock* | Model choice, prompts, temperature |
| Image generation (Illustrator) | Bedrock Titan/Nova Canvas, or Azure | **Unknown — and the documentation points the wrong way** | Prompts, size, library-first gating |
| Agent orchestration | **ODC Agent Workbench** | **Unknown** (availability) | Agents, tools, knowledge source, guardrails |
| Composer grounding | **ODC knowledge bases** (Beta) | **Unknown** (entitlement) | The uploaded toolkit, and its chunking |
| Card library reuse | **ODC semantic search** (Beta) | **Unknown** (entitlement) | Searchable attributes, chunking per attribute |
| Token metering | Provided, limited, monitored | **Confirmed**, and there *is* a console: the **Trial Model details** page in the ODC Portal | Our own `TokenUsage` logging, now a cross-check rather than the only record |

`faq.txt:36` confirms AWS and Microsoft AI tokens are *"integral to the ODC instance"* and
*"limited, and usage will be monitored."* It never names Bedrock.

**The ODC Portal does, as of 30 October.** ODC ships ready-to-use **trial models**,
available in every tenant and in Personal Edition, **in the development stage**:

| Trial model | Provider | Image output? |
|---|---|---|
| **GPT-5** | OpenAI | No |
| **Claude Haiku 4.5** | **Amazon Bedrock** | No |
| **Amazon Nova Pro** | **Amazon Bedrock** | No |

Four things follow, and three of them close open items:

1. **Bedrock is pre-wired.** Two of three trial models are reached through it. The Forge
   connector comes off the critical path — see the struck-out fallback below.
2. **No trial model generates images.** All three are text-out chat models; Nova *Canvas*,
   the image generator in that family, is not on the list. With trial models alone there
   is no image generation, which makes the seeded card library the design rather than the
   contingency.
3. **Trial models are a development-stage feature**, and `1-Click publish` targets
   Development by default. **Decision: the demo runs from Development.** That also keeps
   the knowledge base in one stage, which is the `ODC-GROUNDING.md §2` trap defused.
4. **Limits are a hard stop, and they are visible.** The limits are not time-boxed — they
   are a total allowance, and *"when reached, prevent the further use of the models."*
   Consumption is shown on the **Trial Model details** page in the Portal. There is no
   throttle and no grace period, so the circuit breaker in `TOKEN-BUDGET.md §6.2` is now
   the difference between a measured stop and a dead demo.

#### We can also add our own model, and that reopens the image question

`INTEGRATE > AI models > Add AI model` offers two tabs. **Trial** adds one of the three
above in a click. **Provider** configures our own, from: AI21, **Amazon Bedrock**,
**Anthropic**, Azure OpenAI, Cohere, Databricks, Gemini, IBM watsonx.ai, Mistral, OpenAI,
or a **Custom** connection with arbitrary headers.

Three consequences, in order of how much they change:

**1. Open item 4 becomes a concrete experiment instead of a question.** A Bedrock
connection takes a **Model ID** we supply — so `amazon.nova-canvas-v1:0` can be
configured, and the only remaining unknown is whether ODC's chat-shaped contract can
carry an image back. That is a 30-minute day-3 test, which is what path A always was,
except now we know exactly where the dialog is. **It bills to A.J.'s own AWS account**,
which means the lab bench and the build would stop being separate things — a `CLAUDE.md`
§1 claim to revisit *only if* we take this path, not now.

**2. The Bedrock authentication design is better than ours was going to be.** The
recommended method is **IAM Role**, not access keys: *"OutSystems doesn't store any AWS
credentials. Access is granted through a trust relationship between your AWS account and
OutSystems, using short-lived credentials that are issued and refreshed automatically at
runtime."* We supply a **Role ARN**; the Portal offers a **Download policy** button for
the required trust-policy format, which includes an **External ID** condition — the
textbook confused-deputy defence. Access keys remain available and are explicitly the
weaker option.

This matters beyond configuration. §1.4 previously listed credential storage as a risk on
path C, where an External Library would need our own long-lived keys inside it. The IAM
Role path removes that risk entirely, and it is the kind of control the Security pillar
pass on 6 November should credit rather than flag. If we take this path, the
trust-boundary diagram gains one arrow: `sts:AssumeRole` with an External ID, from
OutSystems into our account.

**3. There is a platform usage limit.** The add-model flow has a **Usage limit** section
setting a *daily token limit* per connection — a platform-enforced ceiling worth setting
on day 3. It backs up but does not replace our own circuit breaker; see
[`TOKEN-BUDGET.md §6.2`](TOKEN-BUDGET.md).

Two smaller facts from the same page. Endpoints are **per stage**, with priority ordering
and fallback between them, which is more resilience than we had planned to have. And
**managing AI models uses the same permissions as managing connections** — so check 1 on
the first-login sheet gates the model list too, not just Data Fabric.

**And one new risk, which lands on a check we already had.** In a multi-portfolio
organization, *trial models are available only in the main portfolio.* If the hackathon
organization is multi-portfolio and our apps are not in the main portfolio, we have no
models at all — not a degraded path, none. That makes check 2a in
[`ODC-FIRST-LOGIN.md`](ODC-FIRST-LOGIN.md) the single highest-value thing to look at on
first login.

**Fallback if Agent Workbench is unavailable:** the three agents become three server
actions calling the model directly, orchestrated in ODC logic. We lose the visible
reasoning path, which is a scoring loss, not a functional one. The JSON output contract
in [`SPEC.md §5`](SPEC.md) is what makes this substitution cheap — the contract is the
interface, not the tool.

~~**Fallback if Bedrock is not pre-wired:** the `Amazon Bedrock Connector (ODC)` on
Forge.~~ **Resolved 30 October — not needed.** Claude Haiku 4.5 and Amazon Nova Pro are
both trial models reached *via Amazon Bedrock*, so the integration is native. Recorded
rather than deleted because the community connector was on the risk register for a week
and someone may remember it being there.

#### Image generation: ODC can see pictures, and is not documented to make them

The native AI model integration is **chat-shaped and text-out**. A call builds a `Messages`
list with `Role` set to `user`, and the answer comes back in `Response.Messages[0]` with
`Role` `assistant`; the optional parameters are `Temperature`, `MaxTokens`, `Stop` and
`ExtraBody`. There is a documented path for image **input** — `ContentUrl` or
`ContentBinaryData` inside `UserMessage.Content`, PNG/JPEG/WebP/GIF, 20 MB per image,
512px minimum — and **no documented path for image output**. The agent-actions page
documents no action returning binary.

So this is a sharper question than metering. Three candidate paths, cheapest first:

| Path | Mechanism | Risk |
|---|---|---|
| A | `ExtraBody` on a registered Bedrock model | **Weaker than undocumented — see below.** The response is a text field, and the API shape underneath is almost certainly Converse, which has no image-output path at all. Still a 30-minute day-3 test, but expect it to fail at validation |
| B | *Add a custom AI model* + the custom API contract | Contract not readable from outside the portal. A kickoff question |
| C | An **External Library** (C#, `OutSystems.ExternalLibraries.SDK`) calling the image API directly and returning binary | Works regardless of the connector, but needs **our own** credentials inside the library, which contradicts *"integral to the ODC instance"* and lands on B5 and on Credentials below |

**Why path A is worse than "undocumented", established 30 October.** ODC's model contract
is chat-shaped in a very specific way: a `Messages` list in, `Response.Messages[0]` out,
with `Temperature`, `MaxTokens`, `Stop` and `ExtraBody`. That is the shape of Bedrock's
**Converse** API, the unified interface AWS tells you to prefer. In Converse the content
block types — `text`, `image`, `document`, `video`, `audio` — are all **input** types;
`image` is documented as *"Image input (base64 or S3)."* **There is no image-output block.**
Image generators return base64 in a provider-specific response body and have to be called
with **InvokeModel**, which Converse-shaped clients do not expose.

So if ODC rides on Converse, registering `amazon.nova-canvas-v1:0` as a provider model
cannot work however `ExtraBody` is used, and may be rejected at validation. We do not know
ODC's internals, so the experiment is still worth half an hour — but **path C is the only
one of the three with a mechanism that can actually work**, and it carries the credential
cost. This raises the confidence on the standing decision in point 2 above: **the seeded
201-card library is the design, and generated artwork is a stretch goal.**

#### Path C already exists on Forge, 31 October

Searching the Forge for Bedrock turns up four ODC components, and one of them is path C
built and published:

| Forge component | Version | What it is |
|---|---|---|
| **`AWSBedrockRuntime` (ODC)** | **1.2.5** | An **external logic library wrapping the `InvokeModel` operation of the official .NET SDK for Amazon Bedrock.** Source: `github.com/stefan-d-p/odc-awsbedrock-library` |
| `AWS Bedrock Runtime Demo` (ODC) | 1.1.5 | A demo app showing the library's actions |
| `AWS Bedrock Model Invocations` (ODC) | 0.1.0 | A layer over the same library, for custom imported models |
| `Amazon Bedrock Connector` (ODC) | 0.1.2 | The older one already on our risk register. May 2024, Claude v2 / Titan / SDXL. Superseded |

**`AWSBedrockRuntime` exposes nine actions, and one of them is
`StabilityDiffusionTextToImage`** — text to image through Stable Diffusion SDXL 1.0. It
also exposes `Converse`, and credentials may be **IAM user keys or an IAM role with a
session token**.

Three things follow:

1. **Image generation through ODC is demonstrated, not hypothetical.** The chat-shaped
   contract has no image-output path, which is still true and still rules out path A — but
   `InvokeModel` sidesteps the contract entirely, and somebody has already shipped the
   wrapper. **Open item 4 is no longer "probably impossible"; it is "possible, at a stated
   cost."**
2. **The cost is unchanged and is the real decision.** The library needs **our own AWS
   credentials** and bills image generation to A.J.'s card, which is exactly the conflict
   with *"tokens integral to the ODC instance"* that B5 and the Credentials section name.
   An IAM role with a session token is better than long-lived keys, but the credentials are
   still ours and still inside a library.
3. **It needs External Logic to be available on the tenant**, which is a capability we have
   not confirmed — uploading a .NET package goes through the External Library Generation
   Service. Added to the second batch in `next-slack-questions.txt`.

The model on offer is **SDXL**, not Nova Canvas. For First→Then cards — flat, iconic,
consistent across a library — SDXL is a harder tool to get consistency out of than a
purpose-built icon style, which is an argument for the seeded library quite apart from
cost.

**The standing decision does not change: the 201 seeded cards plus parent photo upload
remain the design.** What changes is the fallback's quality. If generation becomes worth
having on day 5, there is a published component to start from rather than a C# project to
write — so the stretch goal is genuinely reachable, and open item 4's day-3 experiment
should test *this* library rather than `ExtraBody`.

**The fallback is already built, and it is arguably the better design.** `ImageSource` in
[`SPEC.md §3`](SPEC.md) is already `Generated | Uploaded | SymbolSet`, and
`assets/cards/` already holds **40 original starter cards**. If generation is
unavailable or metered punitively, the Illustrator becomes a pure retrieval agent over
that seeded library plus the parent's own photographs — and `VisualStyle` → `RealPhotos`
exists in the profile because a photograph of *the child's own shoes* beats any generated
icon. Nothing about the demo path depends on generating a picture live.

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

**One regional caveat on retrieval.** In Cape Town, Hong Kong, Jakarta, Singapore, Tel
Aviv and the UAE, ODC semantic search routes its *query* through `eu-central-1` because
the embedding model is not deployed in those regions; stored data stays local. The query
is built from the obstacle text a parent typed, so in those regions that text crosses a
region boundary. We need a US region regardless — open item 7 — which is why this is a
caveat and not a control.

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
| 1 | Can an exposed method read an inbound HTTP header? | ODC Studio — installable now | Secret path segment + body token (weaker) |
| 2 | Is Agent Workbench enabled on hackathon instances? | **First login** | Three server actions against the JSON contract |
| ~~3~~ | ~~Is Bedrock pre-wired?~~ **Answered 30 Oct: yes.** Claude Haiku 4.5 and Nova Pro are trial models *via Amazon Bedrock* | — | Not needed |
| 4 | **Reframed 31 Oct.** Not *can ODC's chat contract return an image* — it cannot — but *can we use the Forge `AWSBedrockRuntime` external library, and is External Logic available on this tenant?* | **Day-3 experiment**: install the Forge library, call `StabilityDiffusionTextToImage` | **The plan, not the fallback:** 201 seeded cards + parent photo upload |
| 5 | Are Twilio credentials provided? | Kickoff | Own trial account, number verified day 2 |
| 6 | Token allocation — the *number*. **Where to see consumption is answered:** the Trial Model details page in the Portal | The limits table on that page | Our own `TokenUsage` logging either way |
| 7 | Region available for provisioning | **Already decided** — visible in the Portal | US region required |
| ~~8~~ | ~~Are ODC knowledge bases enabled on the instance?~~ **Answered 30 Oct — yes, automatically.** OutSystems in the hackathon Slack: *"Yes, both are enabled in the the hackathon instance automatically, you dont need to do anything"* | — | Not needed |
| ~~9~~ | ~~Is ODC semantic search enabled on the instance?~~ **Answered 30 Oct — yes, automatically**, same reply | — | Not needed |
| ~~10~~ | ~~Does ODC allow a *cycle* of weak dependencies between two apps?~~ **Answered 30 Oct: the question dissolves.** The consumer app raises an **Event**, an **ODC Workflow** calls the agent, and only the agent depends on the consumer app. See [`ODC-AGENT-ANATOMY.md §2`](ODC-AGENT-ANATOMY.md) | — | Not needed |
| 11 | Is this tenant a **Licensed Customer** or **Personal Edition**? The trial caps differ by 2×, the rate limits differ, and Personal Edition has no GPT-5 row | **First login** — the Trial Model details page | Plan against the Licensed row, which is the tighter of the two |

Items 2–6 are questions in `email-4-kickoff-questions.txt`. Items 8 and 9 are newer than
that email and are detailed in [`ODC-GROUNDING.md`](ODC-GROUNDING.md); unlike 2–6 they
are entitlements rather than behaviours, so no amount of trying it resolves them — but
whether the Portal offers the feature at all is still visible, and that is the test.

**The ODC environment was created on 30 October**, three days before the kickoff, which
is why the Resolve column above now says *first login* where it used to say *kickoff*.
[`ODC-FIRST-LOGIN.md`](ODC-FIRST-LOGIN.md) turns that into seven things to look at, in
order, each naming the item it closes. Two things looking cannot resolve: the token
allocation number, and item 9's entitlement.

---

*First → Then. Print it, post it, trust it.*
