# The three kickoff documents — read 2 November 2026, 11:38 ET

Three PDFs A.J. added after the call. They are **more specific than the slides** and in
four places they change what we should build.

| File | What it is |
|---|---|
| `2026 Hackathon Kick-off Presentation.pdf` | 19 slides — the whole deck, including four slides the photographs did not catch |
| `2026 Build for the Future Hackathon - Technical Evaluation - Google Docs.pdf` | The tech criteria in prose. **Five sections, not four** |
| `2026 Hackathon Resources - Google Docs.pdf` | The promised "enablement resources" — named ODC features with documentation links |

---

## 1. The four things that change the build

### 1.1 DataFabric means **AWS or Microsoft**, not "any external source"

The slide said *"Seamless alignment ODC's DataFabric to unify data access."* The document
says:

> **DataFabric & Hyperscaler Integration:** Seamless alignment **with AWS and Microsoft
> infrastructure** using ODC's DataFabric to unify data access.

That narrows `SCORING-CRITERIA.md §A4` considerably and **partly reverses what
`TOKEN-BUDGET.md §2d` concluded this morning**. The AWS lab account was called optional
because the free token allowance removed the reason to bring our own model — true for
*models*, and wrong for *data*. A Data Fabric connection to something in AWS is now the
direct route to a 20% bucket we score zero in, and the lab account is where that something
would live.

The resources document adds the mechanism: *Integrate with External Data Sources Using
Data Fabric* for enterprise databases, and **Configure a Private Gateway** for *"private
services and data sources hosted on-premises or in cloud environments"* — which is how a
connection reaches a hyperscaler that is not publicly exposed.

### 1.2 Logic Isolation means **ODC Libraries**, specifically

> **Logic Isolation:** Adherence to cloud-native architectural best practices by
> **utilizing ODC Libraries**. Teams may isolate and reuse business logic across
> applications…

`CODE-PLAN.md §8` splits the build into a Web app and an Agentic app. That is good
architecture and it is **not what this asks for**. The named artefact is a **Library**, and
the natural one is already obvious: the guardrail logic, the three-word validator and the
board contract are used by both apps. Moving them into a Library is a small refactor that
converts an unscored design decision into a scored one.

### 1.3 Real-Time Observability is **exactly the TokenUsage entity**

> **Real-Time Observability:** …Teams must showcase operational visibility by **tracking
> reasoning paths and tool usage**, and real-time visibility into **response quality and
> cost**. Further emphasis is placed on the ability to track **execution metrics, token
> consumption, cost, latency, reliability, and workflow outcomes**.

**This corrects what I wrote at 10:30.** `TOKEN-BUDGET.md §2d` said the reserve and the
circuit breaker were "no longer load-bearing" once the token limits turned out to be 10M a
day — true for *scarcity*, and wrong overall. **Token consumption and cost tracking are
named criteria.** The cost-per-board figure is not a nice-to-have for a judge; it is a
listed thing to showcase. The instrument is now worth more than the budget it was built to
protect, and `tools/token-log.csv` plus the `TokenUsage` entity go in the Tech Video.

The resources document names the platform route too: **Streaming Observability Data**,
streaming telemetry to external platforms over **OpenTelemetry**, plus *Monitoring and
Troubleshooting Apps* for execution traces, and **Audit Trail** for platform operations.

### 1.4 Human-in-the-Loop means **pausing agent execution**, not reviewing output

> …configurable human-in-the-loop checkpoints that **can pause agent execution for human
> review or approval before proceeding**.

Our parent-reviews-the-board step is a review of a *finished* board. That is good UX and it
is a weaker claim than this asks for. The resources document points at **Workflows in ODC**
— *"combine AI-driven automation with human activities, approvals, and decision-making"* —
and we already use an ODC Workflow in the Event pattern (`ODC-AGENT-ANATOMY.md §2`). Making
the review an actual workflow checkpoint that holds the agent is a design change worth
making, and it is small because the workflow exists.

---

## 2. Two ODC features we did not know were features

Both are things this project **built by hand** and the platform apparently provides.

| We built | ODC has | Why it matters |
|---|---|---|
| `GUARDRAILS.md` — 67 rows, 21 tests, implemented as server actions | **Agent Guardrails** — *"configure safeguards, enforce policies, and govern agent behavior"*, with a documentation page and a YouTube talk, *AI Governance with OutSystems: Protect your Agents with Guardrails* | The criteria say *"Developers can define technical and ethical guardrails"*. Hand-rolled logic may satisfy the intent; the **named platform feature** satisfies the wording. Read the doc before building more by hand |
| `eval/cases.json` and the eval review page | **Agent Evaluations** — *"evaluate agent performance, behavior, and output quality"* | Same shape of argument. Our eval set may be portable into the platform's own evaluation feature |

**Neither is a reason to throw away what exists.** The hand-built guardrails encode
clinical decisions no platform feature knows about — guardrail 5, the referral path, is
ours. The right move is to find out what the platform feature covers and **run ours on top
of it**, then show both in the Tech Video.

There is a third, and it is the one closest to how A.J. already works:

> **Agent Experience:** Explore the **OutSystems MCP documentation** to learn how to
> connect **AI coding tools** to OutSystems and develop applications with Mentor.

*Agent Experience* sits inside the **40%** bucket. A.J. is building this with an AI coding
tool right now. If OutSystems ships an MCP server, connecting it is both a scored feature
and an honest description of how the work was actually done.

---

## 3. Four slides the photographs did not catch

### 3.1 Innovation has its own criteria — and one of them is aimed at us

Slide 10, never photographed:

> **1. Originality of Approach**
> - Does this tackle the problem from an unexpected angle, or is it **just a digital
>   version of an existing paper/Excel form**?
> - Does the solution break beyond standard templates to offer a fresh perspective for the
>   nonprofit sector?
>
> **2. Meaningful Application of AI**
> - Is AI integral to the core user journey, or is it an **afterthought tacked on for
>   buzzword points**?
> - Does the solution use AI to solve a genuine operational bottleneck (e.g., triage,
>   automated routing, contextual guidance) rather than just a **basic chatbot wrapper**?

**Read the first bullet honestly: a First→Then board is a paper form, and we digitise it.**
That is the exact failure mode this question is written to catch, and a juror will see it
in the first ten seconds of the Demo. It has to be answered out loud rather than hoped past.

The answer is true and needs saying plainly: **the board is not the product.** A laminated
First→Then board has existed for decades and costs nothing. What does not exist is the part
after it — whether the promised reward actually happened, and whether the child still
trusts the board. The innovation is the **review agent** that checks a board against the
clinical rules before a parent ever sees it, the **semantic reuse** that makes *sneakers*
find the card the child already knows, and **tracking promises kept rather than boards
made**. The paper version cannot do any of those, because paper does not know what happened
next.

On the second criterion we are in good shape: three agents sit in the core journey, not
beside it, and nothing here is a chatbot.

### 3.2 The jury is four people, one per category

| Category | Juror |
|---|---|
| **Tech** | Paulo Garrudo — Product Acceleration, OutSystems |
| **UX** | Menno Cramer — User Experience, OutSystems |
| **Demo** | Kris Lande — CMO, OutSystems |
| **Innovation** | Jennifer Forman — ESG Strategy, **Cisco** |

Two notes. The Tech Video's stated audience, *"Product Management"*, is one named person
whose title is Product Acceleration — so it is a product audience, not a code-review
audience. And **Innovation is judged by someone from outside OutSystems whose field is ESG
strategy**, which is the one seat where *nonprofit value* and *impact* are the native
language rather than the platform.

### 3.3 There is a category to select: **MS or AWS** — and two special awards

The Taikai walkthrough slide carries *"Select category MS or AWS"*, and the deck names two
special awards with their own judges:

- **AWS Award** — Arun Nallathambi, Applied AI Partnerships, AWS
- **Microsoft Award** — Roberto Arocha, Sr Cloud Solution Architect, Microsoft

**This is what replaced the Twilio prize**, and unlike Twilio it costs us nothing to enter.
**Choose AWS.** The hackathon model we will use is `BedrockHaiku5_5` on Amazon Bedrock, the
architecture document is written against AWS, the Well-Architected review is an AWS
framework, and §1.1's DataFabric route points at AWS infrastructure. Nothing about this
build points at Microsoft except the GPT-5.5 entry that is *"deprecated soon"*.

**Unverified:** whether selecting a category changes anything beyond award eligibility, and
whether it can be changed later. The slide shows it as a field on the project page.

### 3.4 Prizes, scale, and support

Prizes: **1st €10,000**, **2nd €5,000**, **3rd €5,000**, each with an OutSystems ODC
licence. Field: **79 teams, 275 developers, 18 countries, 22 nonprofits**. Timeline:
**11 Nov final submission, 30 Nov winners announced.**

Support, in the order the deck gives: **Slack `#help` first** — *"Always first post on
slack"* — then `makeadifference@outsystems.com`, then a support ticket with *hackathon* in
the subject. That ordering is now project policy.

---

## 4. The video briefs are prescriptive — follow the structure

Slides 12 and 13 give a shot list. Both are stricter than the summary slide.

**Tech Video (max 10 min), for Product Management:**
- *Architecture & ODC Setup* — walk through the Studio setup: logic, modules, data entities.
- *Incentivized Features in Action* — **explicitly demonstrate each of the five criteria
  areas**, named one by one.
- *Code/Workflow Walkthrough* — **"Do not just show the UI — open workflows, prompt
  templates, integrations, and logic trees."**
- Clean, high-resolution screen recording of Studio; clear audio commentary on the
  decisions.

**Demo (max 5 min), for the full jury "across Impact, Innovation, UX, and Pitch":**
- **~1 min: The Cause & Problem.** *"Introduce the nonprofit or community cause you are
  supporting"* — **"or community cause" is the phrase that resolves our nonprofit
  problem.** A community cause is exactly what this is, and saying it that way is accurate
  without implying a partner.
- **~4 min: Solution & Live Demo.** A realistic end-to-end scenario in the working app;
  focus on experience and practical value, not backend; show where AI naturally solves the
  problem; show what is innovative; **summarise the measurable difference the app makes**.
- Dynamic, story-driven, no jargon.

That last bullet wants a number. The usability measurement proposed in
`SCORING-CRITERIA.md §B4` — time one real run with the first test user — is the cheapest
honest candidate.

---

## 5. Autism Speaks is on their own nonprofit list

The final slide, *Featured Nonprofits & Partner Organizations*, lists 20 organisations.
**`Autism Speaks (autismspeaks.org)` is one of them.**

This sits oddly beside this morning's answer, *"we do not have relationship with any
nonprofit working in the area of autism"*, and the honest reading is that the two
statements are about different things: a featured organisation on a slide is not the same
as an introduction somebody is willing to make. **Nothing in `CLAUDE.md §2` relaxes.**
Autism Speaks is still named as *intent*, never as a relationship, and the evidence base is
still public material.

What it does change:

1. **It is worth one more question, phrased on their terms** — not *"can you introduce
   us"*, which was asked twice and answered, but *"your kickoff deck lists Autism Speaks
   among featured nonprofits; is there a route to the featured organisations?"* That is a
   different question with a different premise, and the deck is the premise.
2. **It makes the alignment worth stating in the Demo.** The clinical source we build on is
   the Vanderbilt Kennedy Center TRIAD toolkit **published through the Autism Speaks Autism
   Treatment Network** — and Autism Speaks is a featured organisation of this hackathon.
   Both halves are facts, and setting them side by side is not a claim of partnership.
3. **It raises the bar on accuracy.** If a juror knows Autism Speaks, every citation has to
   be exact. `SPEC.md §7`'s practice mapping is what makes that survivable.

--------------------------------------------------------------------------------

# §6 — The post-kickoff email, and the Zoom AI summary's Q&A

Two emails arrived while this was being written. The first is the organisers' own; the
second is machine-generated and has to be graded differently.

## 6. What the organisers said, and how far to trust each source

Four sources on the same event, in descending order of authority: the organisers' own
email, Zoom's machine summary of the call, the corrections that summary needs, and a
verification of the two live Docs. **6.4 was written on 3 November and numbered 6.3 by
mistake, colliding with the section already called 6.3; renumbered and moved into order
on 7 November.**

## 6.1 `makeadifference@outsystems.com`, 2 Nov 16:34 UTC — authoritative

Snezana Djurisic, *"As promised, we are sharing all information you need"*. Four links,
and **they are the three PDFs A.J. already added plus the recording**:

| Item | Where |
|---|---|
| Kick-off recording | `<ZOOM-LINK-WITHHELD>` |
| Presentation deck | attached — same file as `2026 Hackathon Kick-off Presentation.pdf` |
| Technical evaluation criteria | `https://docs.google.com/document/d/1On1PYbaKPh5l2ZIEo5pAJM6YV8Cttv4yfC8h_p8Jzw4/edit` |
| **Enablement resources** | `https://docs.google.com/document/d/1hYb2Qw37QVN6TY2NZ7ltuFtIzO2Pd7vT1LIP0C2E8jM/edit` — *"your go to place for all technical questions"* |

So **T7 is closed**: the enablement resources are the Resources document, already read.
Two riders. The last two are **live Google Docs**, not frozen PDFs — the PDFs are a
snapshot of 11:38 ET on 2 Nov and the organisers can edit the originals, so re-check the
Docs before the submission rather than trusting the export. And support routing is
restated in the organiser's own words: *"please go to the hackathon Slack space and post
them on **#help channel**"*.

## 6.2 The Zoom AI meeting summary — SECOND-HAND, and it carries the Q&A

The same email thread carries Zoom's AI summary of the call, which **includes the question
period the slides do not**. It is machine-generated and stamped *"AI can make mistakes.
Review for accuracy"*, and it visibly garbles names (*"Chris Lundy"* for Kris Lande,
*"Jennifer Foreman"* for Jennifer Forman, and *"Hugging Face 5.5"* for Haiku 5.5). **Grade
it as a lead, not a fact.** Three of its lines matter more than anything in the slides:

> *"The team was informed that there are **no limits on mentor usage** and that **Data
> Fabric integration is optional, with mock integrations also being acceptable** for the
> project."*

**1. Data Fabric may be optional, and a mock may score.** If true, this substantially
defuses §1.1 and `SCORING-CRITERIA.md §A4`: the 20% Connectivity bucket would not require
a real external source in AWS, and would not require the AWS lab account to host one. **It
is not yet actionable**, for two reasons. It is second-hand from a tool that misnamed the
jury in the same paragraph; and *"optional"* and *"scores the same"* are different claims —
a written criterion that says *"seamless alignment with AWS and Microsoft infrastructure"*
does not stop being a criterion because a mock is *accepted*. **Ask it in `#help` and get
it in writing before cancelling any AWS work.** Until then the §1.1 conclusion stands as
written, with this flagged against it.

**2. Mentor usage is unlimited.** That is `TOKEN-BUDGET.md §8` open question 6, answered —
again second-hand. Cheap to confirm by meter: read the four model figures, run one Mentor
prompt, read them again. If Mentor is free, the *"Mentor cannot do scaffolding"* finding in
`practice-camera-app/studio-build.md` is the only remaining reason to hand-build.

**3. Twilio is not banned — it is unsponsored, and a 2027 partnership is planned.**
*"Twilio is not participating in the current Hackathon and no Twilio accounts or credits
will be provided… participants can use their own Twilio services or other cloud services
like AWS and Azure."* That is narrower than *"we will not use twilio"* read alone, and it
does not change the recommendation in `TWILIO-WITHDRAWN-2-NOV.md`: with no credentials, no
prize and the hardest security work in the project behind it, it still comes out.

## 6.3 Four smaller corrections from the same summary

1. **The category may be BOTH.** *"select the appropriate category (AWS, Microsoft, **or
   both**) to be eligible for partner awards."* §3.3 recommended AWS; if the Taikai field
   accepts both, take both — there are two special awards and no stated cost.
2. **Why the deadline moved.** The event *"was extended by two days until November 11th to
   accommodate Diwali celebrations in India"*. Independent confirmation of the 11 Nov date
   from a second source, and it explains the discrepancy with `rules.txt`.
3. **Jon Levesque opened the call** alongside Snezana, thanking *"sponsors AWS and
   Microsoft"*. Not a judge, and not on the jury slide.
4. **Support escalation, restated:** `#help` first, and a support ticket for *"bugs or
   product friction"* must carry **"Hackathon" in the title** — and be posted in `#help`
   as well, not instead.

---

## 6.4 Both Docs fetched and verified, 3 November 2026

**No drift.** Both live Google Docs were exported and compared against the 2 November PDF
snapshots. Ignoring whitespace only, each pair is **character-identical with a matching
SHA-256** — technical criteria 2,803 chars (`bdb5cb81397951f6`), enablement resources 4,238
chars (`0f738d1a0f301792`). So the PDFs in this directory are faithful, and the §6.2 warning
that the organisers can edit the originals has **not** yet come true. Re-run the check before
submitting; the method is below.

**Link inventory.** The **technical criteria doc contains no links at all.** The
**enablement resources doc contains 27**, and two of them are broken:

| Dead link, as the doc has it | The page that actually exists |
|---|---|
| `outsystems_developer_cloud/libraries/` | `outsystems_developer_cloud/building_apps/libraries/` — plus `.../libraries/use_public_elements/` |
| `outsystems_developer_cloud/forge/install_or_update_a_forge_asset/` | `outsystems_developer_cloud/building_apps/forge/install_or_update_a_forge_asset/` |

**The Libraries one matters**: ODC Libraries is exactly what §1.2 identifies as the
requirement behind *Logic Isolation* in the Modular Architecture bucket, and the organisers'
own pointer to it 404s. Use the corrected path.

**How these were checked, because the obvious method does not work.**
`success.outsystems.com` is a single-page app that returns **HTTP 200 for any path** — a
deliberately bogus URL returns 200 with the same shell. **A status code proves nothing
there.** Each link was instead matched against the site's own sitemap (4,502 URLs, from
`https://extranetprdintegrations.outsystems.net/Documentation_API/rest/Sitemap/GetSitemap`,
which `robots.txt` points to), with the bogus path as a control — absent, as it should be.
The three YouTube links were confirmed through oEmbed, which 404s on a dead video id.

**Provenance, and why to distrust the list a little.** **23 of the 27 links carry
`?utm_source=chatgpt.com`**, so the document was assembled with ChatGPT's help and not fully
proofed — which is exactly how `/outsystems_developer_cloud/libraries/` comes to exist as a
plausible-looking path that was never real. Treat it as a reading list to verify, not an
index. It is also a second, independent reason to distrust the Zoom summary's *"Hugging Face
5.5"* (§6.2): the same materials, assembled the same way.

**The three videos, titles as returned by YouTube:** *A sneak peek into Agent Workbench* ·
*Agent Workbench: Agent Orchestration, workflows and humans!* · *AI Governance with
OutSystems: Protect your Agents with Guardrails* — all in playlist
`PLxALhSwsaivy1afIHT5TElTJJs9OMHNcX`. The third is on the feature this project built by hand.

**All 27 links, each with its verdict, are in a file of their own** so this one stays an
analysis rather than an index: **`RESOURCES-LINK-INDEX-NOV-3.md`**, beside this file. The
two dead links and their working paths are repeated there.
