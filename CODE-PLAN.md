# What code exists, and what has to be written

Written 30 October 2026, two days before the kickoff. Companion to
[`SPEC.md`](SPEC.md), [`AWS-ARCHITECTURE.md`](AWS-ARCHITECTURE.md) and
[`PRE-BUILD-LAB.md`](PRE-BUILD-LAB.md).

---

## 1. The constraint that shapes this whole document

**Most of an ODC application is not text.** Entities, screens, server actions and agent
flows are a visual model edited in ODC Studio and stored in a format we neither author
nor diff. There is no repository of ODC source to write ahead of time, no pull request
over a screen, and no way to review a server action as a patch.

That is not a complaint, it is a planning fact, and it splits the work in two:

| | What it is | Can it be written before 2 November? | Can it be reviewed as code? |
|---|---|---|---|
| **Authorable** | Prompts, contracts, validators, C# external libraries, CSS, SQL-shaped seed data, our own tooling | **Yes** | Yes |
| **Studio work** | Entities, screens, logic flows, agent wiring, the Twilio connector | No | Only by demonstration |

So the honest answer to *"can we lay out all the code that needs to be written"* is: yes
for the authorable column, which is larger than it looks, and no for the other, which gets
a build checklist instead of a code review. The two lists are §3 and §4.

## 2. What exists today

Nothing here is application code. All of it is tooling, content or specification — which
is the correct state two days out, but it should be said plainly rather than implied.

| File | Lines | What it is |
|---|---|---|
| `assets/build_cards.py` | 1792 | Draws the 201-card starter library and `MANIFEST.csv` |
| `assets/build_art.py` | 916 | Draws the submission artwork |
| `assets/build_diagram.py` | 321 | Draws both trust-boundary diagrams |
| `tools/build-eval-page.py` | 556 | Builds the A/B board review page from `eval/cases.json` |
| `tools/build-gems-page.py` | 473 | Builds the Gemini Gem comparison page |
| `tools/lab-measure.py` | 135 | Calls Bedrock, prints token usage, appends to the log |
| `tools/token-budget.py` | 125 | Burn rate and reserve against `tools/token-log.csv` |
| `video/build_video.py` | 213 | Builds the concept video |
| `prompts/*.md` | 755 | Composer, Reviewer, Illustrator, and the Gem meta-prompts |
| `eval/cases.json` | 445 | 8 cases, 16 candidate boards |
| `docs/*.html` | ~1650 | The spec, the eval review page, the Gem page, the upload prototype |

**Application code: none.** Not one entity, screen, server action or agent exists, because
none can exist before the instance does.

## 3. The authorable list — what we can write and review before the kickoff

Ordered by how much a late discovery would hurt.

### 3.1 The output contract — *written, needs hardening*

`SPEC.md §5` carries the JSON the Composer returns. It is the interface every other piece
substitutes against: if Agent Workbench is unavailable, three server actions produce the
same JSON and nothing else changes. What is missing is a **schema** rather than an
example — field types, enumerations, required-ness, and the card-count range per support
type. One JSON Schema file, and `eval/cases.json` validates against it. ~120 lines.

**Two changes from the course exercise, 30 October.** ODC has a **structured output**
feature that maps a model response directly into a structure, so the schema's job is to
define that structure — **we do not write a JSON parser, and we never decide anything by
searching for a word in free text.** The exercise demonstrates that trap and its own bug:
`Index(Response, "Approved") <> -1` matches *"Not Approved"*. Our Reviewer's pass/fail
would have walked into it.

And the contract needs a **length discipline**, which it does not currently have. Model
responses overflow database columns — the exercise names the errors (`OS-BERT-60400`,
`22001: value too long`) and uses two defences together: an explicit cap in the
SystemPrompt and a truncation guard in the logic. Our board JSON is far longer than its
200-character summary, so entity attributes get sized deliberately and the guard stays.
[`ODC-AGENT-ANATOMY.md §6`](ODC-AGENT-ANATOMY.md).

### 3.2 The seven guardrails — *specified, not written*

`SPEC.md §6` states them in prose. Each is a validation in a server action, and in ODC
that means a visual flow — but the **logic** is authorable and testable now, as a small
reference implementation with a test table:

| # | Rule | Hard part |
|---|---|---|
| 1 | Three words maximum | Hyphenation, and whether "all done" is one word or two |
| 2 | Positive phrasing | A deny-list is too blunt; "Do not run" must fail and "Stop sign" must pass |
| 3 | First–Then needs a Then card | Trivial, and structural |
| 4 | Card count in range per type | Needs the range table from §2 |
| — | **No decision is read by substring.** Every verdict compares for equality or maps through a static entity | The shipped underwriter exercise gets this wrong: `Index(Response.Decision, "Approved") <> -1` matches `"Not Approved"`. See `ODC-AGENT-ANATOMY.md §8` |
| 5 | No diagnosis or clinical advice | Escalation terms route to referral guidance, not a board. **The one with a safety cost if wrong** |
| 6 | Neurodiversity-affirming language | Needs a reviewed term list, not a guess |
| 7 | Export and ownership | A screen, not a validator |

Rules 1, 2, 4 and 5 are pure functions over text. Write them in Python with a table of
cases, review them, then port the logic into ODC flows on day 5. The Python version does
not ship — it is the specification that gets reviewed, and the test table outlives it.

### 3.3 The Twilio inbound webhook — *the highest-risk authorable piece*

Boundary **B3** in `AWS-ARCHITECTURE.md` is the only unauthenticated path into the
system, and the one thing a managed platform does not do for us. It needs:

- `X-Twilio-Signature` validation: HMAC-SHA1 over the full URL plus sorted POST
  parameters, compared in constant time.
- `MessageSid` as the idempotency key, because Twilio retries.
- A reply body parsed down to one character, tolerant of "Y", "y", "yes", an emoji, and
  whatever else a parent sends at the front door.

Open item 1 is whether an ODC exposed method can read an inbound header at all. If it
cannot, the fallback is weaker and we should know which we are building. **Authorable
now in C#**, as an external library, which also sidesteps open item 1 — and if the ODC
method can read headers, the same code is the reference for the visual flow.

### 3.4 The image path — *conditional on a kickoff answer*

If the answer to open item 4 is "external library", that library is real C# against
`OutSystems.ExternalLibraries.SDK`: `[OSInterface]`, `[OSAction]`, a call to the image
API, binary out. ~150 lines and fully reviewable. If the answer is `ExtraBody` or a custom
model, no code is needed. **Do not write this until the question is answered** — it is the
one item on this list whose necessity is unknown.

### 3.5 The print sheet — *pure CSS, nobody's critical path, high demo value*

Cut lines, 85×85mm cards sized for lamination and Velcro, four to a sheet, bleed where a
home printer needs it. This is a stylesheet and a page template, authorable today and
visible in the demo video. It is also the only part of the system a parent physically
holds.

### 3.6 The seed data — *done*

`assets/cards/MANIFEST.csv`, 201 rows, loads into `CardLibrary`. Already written and
already verified at card size.

### 3.7 Our own tooling — *done, extend during the build*

`tools/token-budget.py` and `tools/lab-measure.py` read and write the same CSV. During
build week the `TokenUsage` entity exports into that CSV, so the reserve check keeps
working against real consumption.

## 4. The Studio list — what cannot be written, only built

Each is a checklist item with a definition of done, because that is the only review
available. This is the day-by-day build in `SPEC.md §8`, stated as artifacts:

| Area | Items | Done means |
|---|---|---|
| Data | 10 entities, 3 static entities, the 201-row seed | A board round-trips to the database and back |
| Agents | Composer, Reviewer, Illustrator; 8 tools; `GetGroundingData` wired to the knowledge base | A three-question intake returns valid JSON against §3.1 |
| **Workflow** | One ODC Workflow: Start on the board-requested Event, Automatic Activities per agent, a Decision on the Reviewer's verdict | A board request is visible moving through **Workflows** in the Portal |
| **The sync/async split** | The parent-facing request calls `CallComposer` as a **service action directly** and shows progress; the Illustrator top-up and the SMS send go through the Event and the Workflow | A parent never sees a refresh button — see `ODC-AGENT-ANATOMY.md §11` for why the exercise's polling pattern is rejected |
| **Structured output** | A Structure per agent response, with a Description on the structure and every attribute, attached in the `Call Agent` element's **Structured output** tab | `AgentFlow.Response` is a typed object and no string parsing exists anywhere in the app |
| **Settings** | `SystemPrompt` and `UserPrompt` per agent, as Settings | A prompt can be retuned in the Portal **without republishing** |
| **Action calling** | Each tool attached in the `Call Agent` element's Action calling tab, with a Description on the action *and* on every input parameter, a fixed expression (never `Generated by AI`) for `ChildId`, and a **Call Condition** token limit | The Reviewer calls `CheckReadingLevel` unprompted, and a runaway loop stops on the Call Condition rather than on the allowance |
| Validators | 7 guardrails as server actions | Every row of the §3.2 test table behaves the same in ODC as in the reference |
| Screens | 8 screens from `SPEC.md §4` | Each screen the video touches works on a phone |
| Messaging | Outbound SMS, exposed inbound endpoint, idempotency | A real phone receives a script and a reply lands in `UsageLog` |
| Print | Sheet with cut lines; tablet mode | A sheet prints at the right physical size |

## 5. The review pipeline

Four stages, each with a named reviewer and an artifact that survives it. Dates assume
the kickoff lands as planned on 2 November.

| Stage | When | What is reviewed | By what standard |
|---|---|---|---|
| **A · Plans** | 31 Oct – 1 Nov | This document, the §3.1 schema, the §3.2 rule table, the B3 design | Does it match `SPEC.md` and `AWS-ARCHITECTURE.md`, and does every open item still have a fallback |
| **B · Authorable code** | 1–2 Nov | The §3.2 reference implementation, the B3 C#, the print CSS | `/code-review`, plus the §3.2 test table passing |
| **C · Security** | 6 Nov | B3, B5, B7 against the real application | `/security-review`, and a Security + Reliability Well-Architected pass |
| **D · Whole system** | 8 Nov | Everything, before the demo is recorded | All six Well-Architected pillars; every guardrail demonstrated, not asserted |

Stage A reviews *plans*, which is worth saying because the usual failure is to review code
that implements the wrong thing. The question at stage A is not "is this correct" but
"is this the thing we meant to build, and does it survive each of the eleven open items
going the wrong way".

Stages C and D are already scheduled in `PRE-BUILD-LAB.md §5`; this table is the same
schedule with the earlier two stages in front of it.

## 6. What is not planned, and why

- **No unit test framework inside ODC.** The §3.2 test table is run outside and the
  behaviour is confirmed by demonstration inside. Pretending otherwise would be the kind
  of plan that looks rigorous and is not.
- **No CI.** Seven days, one person, a visual platform. The review gates above are
  manual on purpose.
- **No infrastructure as code for the application**, because the application's
  infrastructure is not ours. See §7.

## 7. The AWS question, answered precisely

Three different things get called "rolling out to AWS", and only two of them are real:

1. **The application.** No. There is no `aws odc`. ODC is provisioned and operated by
   OutSystems inside accounts we do not hold, and an AWS-CLI build would be a different,
   non-qualifying project. `PRE-BUILD-LAB.md §1` settles this.
2. **The lab account.** Yes, and the instructions are already written —
   `PRE-BUILD-LAB.md §3` for the budget and §7 for the setup order. One step cannot be
   scripted: **enabling model access in the Bedrock console**, which a fresh account
   lacks and which is the step most often mistaken for a broken credential.
3. **The reference architecture in `AWS-ARCHITECTURE.md §4`** — what the system would
   look like built natively on AWS. That is currently a design, and it could be made real
   as CloudFormation or CDK. It would demonstrate AWS competence for the AWS track
   without touching the submission. It would also cost a day we have not got. **Decision
   pending**, and it should be made on 2 November when the scoring emphasis is announced,
   not before.


## 8. How many ODC apps the submission is

Read 30 October against the ODC *App architecture* page. This is the first thing we have
read that forces a decision we had not made, so it is recorded here rather than
discovered in Studio.

**It is at least two apps, and that is not a choice.** Agents are separate elements in
ODC, consumed by a web or mobile app through a `Call<AgentName>` service action, and
*Agentic* is one of the four app types at creation (Web, Mobile, Agentic, Library). So
the three agents live in an Agentic app and everything a parent touches lives in a Web
app:

| App | Holds | From `SPEC.md` |
|---|---|---|
| **Web** | 10 entities + 3 static entities, 8 screens, the 7 guardrail server actions, the print sheet, the exposed Twilio endpoint | §3, §4, §6 |
| **Agentic** | Composer, Reviewer, Illustrator, and their tools | §5 |

**The problem is that the dependency wants to go both ways.** The Web app depends on the
Agentic app, through `Call<AgentName>`. But the Illustrator's reuse check reads
`CardLibrary`, which is a Web-app entity — so if that check is a tool the agent calls,
the Agentic app depends on the Web app too. Both are *weak* dependencies, which is the
only kind ODC allows between apps, but whether ODC permits a **cycle** between two apps
is not something the page states. It is now open item 10 in
[`AWS-ARCHITECTURE.md §5`](AWS-ARCHITECTURE.md).

Three ways out, and the order matters more than the choice:

| | What it does | Cost |
|---|---|---|
| **A. Keep the cycle** | The Illustrator's reuse check stays a real tool call | Nothing to restructure — *if* ODC allows it. Strongest agentic story, which is scoring criterion one |
| **B. Shared entities into a Library** | Breaks the cycle properly | **Wrong trade here.** Libraries are *strong* dependencies, packaged into each app at publish. A data-model change would mean republishing both apps — during the days the data model changes most |
| **C. Pass candidates in as input** | The Web app runs the search and hands the agent a candidate list | One-way dependency, and the agent becomes testable with no data at all. But the Illustrator stops being agentic in the way criterion one rewards |

**Resolved the same day, and none of the three is the answer.** The course exercise shows
the real pattern: the consumer app raises an **Event**, an **ODC Workflow** listens for it
and calls `Call<AgentName>`, and only the agentic app takes a dependency — on the consumer
app's entities and on one service action it uses to write results back. The consumer app
never references the agent, so there is no cycle to permit.
[`ODC-AGENT-ANATOMY.md §2`](ODC-AGENT-ANATOMY.md) has the node-by-node shape, and open
item 10 is closed.

The table above stays, because the **request** half of it still binds: `TOKEN-BUDGET.md
§3a` needs the Reviewer and Illustrator gated behind rules and the card library, at ~1.6
requests a board against ~4. That is now a budget decision on its own merits rather than a
dependency workaround — and the agents keep their tools either way. The promotion is additive rather than a
rewrite: A is C plus a tool, with the input parameter kept as an override. B is recorded
so that nobody reaches for it under time pressure on day 6 — it is the one that looks
tidiest and costs the most.

Two smaller consequences of the same page:

- **Configuration lives in the app, per stage** — including values an app consumes from a
  library. So the Twilio credentials are Web-app settings, set once per stage, which is
  the same per-stage discipline as the knowledge base in `ODC-GROUNDING.md §2`.
- **The course for this decision** is *Architecture fundamentals in ODC*, a free journey
  in the training catalog: <https://learn.outsystems.com/training/journeys/architecture-fundamentals-559>.
  Not the paid two-day *ODC Architecture Boot Camp*, which is a different thing.
- **Public elements do not cross portfolios.** We assume one portfolio. If the hackathon
  organization turns out to be multi-portfolio, then both the two-app reuse above *and*
  the Data Fabric connection from `ODC-GROUNDING.md §4` have to sit in the same portfolio
  as the apps. Added to the first-login checks.


---

*First → Then. Print it, post it, trust it.*

---

## 9. The arithmetic does not go in the prompt

The enrichment-agent exercise closes with OutSystems' own warning that the model may get
the debt-to-income ratio wrong, and that the fix is to put the calculation in a server
action and let the agent call it through **Action calling**. Taken as a rule:

**Anything a board computes is a server action, not a sentence in a prompt.** Specifically:

| Computed thing | Where it lives |
|---|---|
| Step count, and whether it is within the range table in §2 | `ValidateStepCount` — guardrail 4, already in §3.2 |
| Total duration, and each step's timer | `ComputeBoardTiming`, a new server action — **add to the §3 authorable list** |
| Reading level of the phrase | `CheckReadingLevel` — guardrail 2 |
| Card-to-step ratios on the print sheet | print CSS and the sheet logic, never the model |

The guardrails were already server actions for a different reason: §3.2 wants them
testable outside ODC. Action calling means the Reviewer can *invoke* them rather than being
told their verdict after the fact, which is both a better demo and one fewer model turn.
The mechanics are in [`ODC-AGENT-ANATOMY.md §7`](ODC-AGENT-ANATOMY.md).

---

## 10. The clinical rules want to be an entity

The underwriter agent grounds on two serialized sources, and the second one is a
**`BankPolicy` entity** — the bank's lending rules as rows, labelled separately in the
system message and editable without republishing
([`ODC-AGENT-ANATOMY.md §11`](ODC-AGENT-ANATOMY.md)).

Our clinical basis is currently prose: the practices named in `SPEC.md §7` and the
guardrails in §6 live in prompts and in validation logic. The underwriter pattern says they
should live in a table — call it `ClinicalPractice`, one row per named practice from the
National Standards Report, each with the rule it implies and the citation it carries.

Three reasons this is worth the extra entity, in order:

1. **A clinician can correct a row; only a developer can correct a prompt.** The project's
   standing claim is that every board names the practice it rests on. That claim is stronger
   when the practice is data the board links to.
2. **It is authorable before 2 November.** Rows are SQL-shaped seed data, which §1 puts
   firmly in the left-hand column — so this is §3 work, not Studio work.
3. **It survives a prompt rewrite.** Prompts get retuned in the Portal all week
   (`§4`, Settings). Evidence should not be a casualty of tuning.

**Not yet reflected in `SPEC.md`'s data model**, which still says ten entities plus three
static. Adding it is a one-line change to that count and a seed file; it is listed here
rather than done silently because the entity count appears in the submission material.

---

## 11. Yes, ODC configuration can be written as JSON

*Answered 31 October. The question was whether ODC can be configured from a file rather
than by clicking through the Portal.*

**ODC exposes twelve REST APIs**, authenticated with OAuth 2.0 client credentials from an
**API client** created in the Portal, with permissions granted **per stage**:

| API | What it manages |
|---|---|
| **Asset Configurations** | **global environment settings and per-asset configuration settings** — this is the one |
| Environment Configurations | IP filters, private gateways, custom domains |
| Deployments | deploying assets to stages, tracking progress |
| Build Operations | starting builds, build status |
| Asset Repository | asset information and revisions |
| Dependency Management | impact analysis, dependency detail |
| External Library Generation Service | generating external libraries from .NET packages |
| Portfolio v2 | which assets are deployed where |
| User and Access Management | end users, groups, access policies |
| Code Quality | analysis requests, findings, scores |
| Subscription | metrics, object counts, capacity |
| Native Mobile Build | iOS/Android configuration and builds |

The configuration model has a **default value and a current value** per setting; the
current one wins, and the default applies when no current value is set. **Changes apply
asynchronously** — a write is not immediately in effect. OutSystems states directly that
configuration can be folded into CI/CD pipelines or infrastructure-as-code tooling.

### What it is good for here, and what it is not

**Not for building the app.** The app itself is `.oml` — a visual model in a proprietary
binary. No JSON uploads an entity, a screen or an agent flow. §1's split stands unchanged.

**Good for three things**, in descending order of value to this project:

1. **Prompts.** `SystemPrompt` and `UserPrompt` are Settings (§4), and Settings are what the
   Asset Configurations API writes. That means a week of prompt tuning can be
   **version-controlled as JSON in this repo and applied**, rather than retyped into the
   Portal and lost. For a project whose whole quality story is prompt iteration, that is
   the difference between an experiment log and a pile of forgotten edits.
2. **Reproducibility for the judges.** "The configuration that produced this demo is in
   the repo" is a stronger claim than a screenshot, and it costs one JSON file.
3. **The Well-Architected passes.** Operational Excellence asks whether changes are made
   through repeatable mechanisms. An API client plus a committed settings file answers it
   with evidence.

**Two cautions.** Creating an API client needs administrator rights — the same gate as
first-login check 1 — and the asynchronous apply means a settings change needs a confirm
step, not fire-and-forget. **Do not put secrets in the committed JSON**: Twilio credentials
and any AWS key stay out of the repo, as `CLAUDE.md` §4 already requires of the environment
hostname.

**Day 3 task, half an hour**: create an API client, read the current settings of one app,
commit the JSON, change a prompt through the API, confirm it applied. If it works, prompt
tuning moves into git for the rest of the week.

