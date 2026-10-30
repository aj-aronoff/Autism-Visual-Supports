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
"is this the thing we meant to build, and does it survive each of the nine open items
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

---

*First → Then. Print it, post it, trust it.*
