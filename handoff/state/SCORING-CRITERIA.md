# Evaluation criteria — captured from the kickoff, 2 November 2026

Slides photographed from the kickoff Zoom and read directly. **This is criterion one made
concrete** — the thing `KICKOFF-NOV-2.md` item 1 said to write down verbatim, because the
submission has to echo the wording back.

| Category | Slide | Captured |
|---|---|---|
| **Tech** criteria | `Hackathon-scoring.png` | 10:14 ET — §A below |
| **UX** criteria | `UX Evaluation slide.png` | 10:18 ET — §B below |
| **The submission itself** | `Subbmission-details.png` | 10:22 ET — §C below |
| Demo and Innovation criteria | — | not seen as slides, but §C confirms **separate Demo, UX and Innovation juries** exist |

**Both criteria slides use the same shape: 40 / 20 / 20 / 20.** Neither says what share
its category holds of the whole, so the weights are *within* a category and cannot be
compared across them. A 20% gap in Tech is not 20% of the prize. §C adds the one piece of
cross-category information we have: **one video is judged by the Tech side and the other
by three juries at once**, which is a rough guide to where effort pays.

--------------------------------------------------------------------------------

# §A — Tech Evaluation Criteria

## A1. Verbatim

Transcribed exactly as the slide reads, including its own punctuation and spacing.
Where the slide is ungrammatical it is left ungrammatical.

> ### Tech Evaluation Criteria
>
> **40% — Agentic Automation & AI Capabilities**
> *Agent Experience & Mentor:* optimize and accelerate the development process
> *Agent Workbench:* AI-driven decisions, routing, and tasks
>
> **20% — Enterprise Connectivity & Data Integration**
> *DataFabric Integration:* Seamless alignment ODC's DataFabric to unify data access.
>
> **20% — Contextual Intelligence & Grounding**
> *Knowledge Base:* ingest / structure data
> *Semantic Search:* agents to retrieve accurate and  nuanced information
>
> **20% — Modular Architecture, Governance and Security**
> Logic Isolation, Forge Acceleration, Multi-Agent, Human-in-the-Loop,
> Real-time Observability

**What this does NOT say.** It is headed *Tech* Evaluation Criteria, and `rules.txt:40`
says the kickoff would outline *"technical requirements, UX, Demo, and Innovation"*. So
these four weights total 100% **of the technical score**, and what share technical holds
of the whole is not on this slide. Do not plan as though 40% of the prize rides on
Agentic — plan as though 40% of one of four categories does.

## A2. Where we stand, bucket by bucket

| Bucket | Weight | Where we are | What is missing |
|---|---|---|---|
| Agentic Automation & AI | **40%** | Three agents designed (Composer, Reviewer, Illustrator); Agentic app type confirmed present in Studio (open item 2, 1 Nov) | **Mentor is now scored** — see §3. Agent Workbench is named and we have opened it but built nothing in it |
| Enterprise Connectivity & DataFabric | **20%** | **Nothing.** The architecture is self-contained: ODC entities plus Bedrock | **This is the gap.** See §4 |
| Contextual Intelligence & Grounding | **20%** | **Strongest bucket.** Knowledge base + semantic search are confirmed enabled on the tenant (Slack, 30 Oct) and are the design, not a hope. `ODC-GROUNDING.md` is written against both | Only execution: upload the toolkit, enable semantic search on `CardLibrary.Label`, and make *sneakers → Shoes* work |
| Modular Architecture, Governance, Security | **20%** | Logic Isolation ✓ (the Web/Agentic split, `CODE-PLAN.md §8`). Multi-Agent ✓ (three agents, and the slide names it). Human-in-the-Loop ✓ (the parent reviews and edits every board before it prints — this was a clinical decision and it now scores) | **Forge Acceleration** depends on T8, still unasked — and it is now worth points, not just convenience. **Real-time Observability** we have nothing for beyond `TokenUsage` |

## A3. Mentor changed status this morning

The standing decision was *"the hand-build is the primary path, because the intake
exercise says Mentor cannot do scaffolding and this app is mostly scaffolding"*
(`CLAUDE.md §5`). That reasoning was about **efficiency**, and it still holds on
efficiency. But the slide puts *Agent Experience & Mentor* inside the 40% bucket, which
means using Mentor is **evidence**, not just a shortcut — and evidence has to be visible
in the submission, not merely true.

Two consequences, and they pull against each other:

- Use Mentor deliberately on the parts it is good at — the logic blocks already written
  in `practice-camera-app/mentor-prompt.md` — and **record what it produced**, because a
  submission cannot claim Mentor without showing it.
- **We still do not know what Mentor spends**, but **10:27 ET took the sting out of it**.
  The AI Services slide (`TOKEN-BUDGET.md §2d`) announced two hackathon models at
  **10,000,000 tokens a day each**, so even if Mentor draws from somewhere, there is room.
  T7 came back as *"we will share enablement resources"* — a pointer, not a figure — so
  `TOKEN-BUDGET.md §8` open question 6 stays open. Still worth the before/after meter
  reading on the first Mentor session, because the *trial* entries are a separate small
  pool of requests and Mentor might draw on those; it is no longer urgent.

## A4. DataFabric is the real gap, and it needs a decision

20% of the technical score is currently zero for us. Nothing in `SPEC.md` or
`AWS-ARCHITECTURE.md` reaches an external data source — that was a deliberate
simplification, and the slide has now priced it.

Data Fabric has appeared in this project exactly once, as a **fallback** for grounding if
knowledge bases were not entitled (`ODC-GROUNDING.md §4`): the provider list includes
three AI search services - Azure AI Search, Amazon Kendra, and a generic custom search
service. Knowledge bases *are* entitled, so that fallback was shelved. **It is no longer a
fallback; it is a scored feature in its own right**, and the honest question is what
external data this app genuinely has.

> **NARROWED 11:38 by the written criteria document:** it is **"DataFabric & Hyperscaler
> Integration: Seamless alignment with AWS and Microsoft infrastructure"**. So the
> external source should live in **AWS or Azure**, which rules candidate 3 further out,
> re-opens a use for the AWS lab account that `TOKEN-BUDGET.md §2d` had just called
> optional, and brings **Configure a Private Gateway** into scope as the connection
> mechanism. See `RESOURCES-AND-CRITERIA-NOV-2.md §1.1`.

> **POSSIBLY DEFUSED, 2 Nov, but NOT yet actionable.** The Zoom AI summary of the
> kickoff Q&A says *"Data Fabric integration is **optional**, with **mock integrations
> also being acceptable**"*. If that is accurate, this whole section becomes a choice
> rather than a 20% hole. It is **second-hand** — machine-generated, stamped *"AI can make
> mistakes"*, and it misnames two jurors in the same paragraph — and *"accepted"* is not
> *"scores the same"* as the written criterion's *"seamless alignment with AWS and
> Microsoft infrastructure"*. **Get it in writing in `#help` before cancelling any AWS
> work.** `RESOURCES-AND-CRITERIA-NOV-2.md §6.2`.

Three candidates, best first:

1. **The card library as an external source.** The 201 seeded cards and the National
   Standards practice table live outside the app and are read through a Data Fabric
   connection, so the library can be corrected or extended without redeploying the app
   and could be shared with a second consumer. This is a true "unify data access" story
   rather than a connector added for the scoring slide, and it is the one that survives a
   judge asking *why*.
2. **An AI search connection for the toolkit**, from `ODC-GROUNDING.md §4`. Cheapest
   in design effort because it is already written up, and Azure AI Search's Free tier was
   the identified candidate. Weakness: it overlaps the Grounding bucket we are already
   strong in, so it may read as one feature counted twice.
3. **Something domain-real but new** — a school or therapy schedule, a shared caregiver
   roster. Strongest story, no chance in seven days. Roadmap, not build.

**Unverified and blocking:** which providers the connection list actually offers on this
tenant, and what any of them cost. Creating a connection needs administrator rights,
which A.J. has (1 Nov). **Open the Data Fabric connections screen and read the provider
list before choosing** — this is a ten-minute check and candidate 1 depends on what is
on it.

## A5. What to do about it, in order

1. **Read the Data Fabric provider list in the Portal.** Ten minutes, decides A4.
2. **Ask T8 in `#help` now** — Forge Acceleration is named on the slide, so whether Forge
   components may be installed on this tenant is worth points and no longer just
   convenience.
3. **Run the Mentor meter experiment** with Studio open: read all four model figures, run
   one prompt from `mentor-prompt.md`, read them again.
4. **Work out what Real-time Observability means in ODC** and whether anything in Agent
   Workbench or the Portal gives it to us for free. Nothing in the project covers this yet.
5. **Re-read `MID-SUBMISSION.md` against these four buckets** — it was written before this
   slide existed, and the submission format changed this year as well.

--------------------------------------------------------------------------------

# §B — UX Evaluation Criteria

Source: `UX Evaluation slide.png`, photographed at 10:18 ET.

## B0. A warning before the content: Innovation appears twice

`rules.txt:40` says the kickoff would outline *"technical requirements, UX, Demo, and
Innovation"* — four categories. But **Innovation is a 20% bucket inside the UX slide**.
Either the rules list was loose, or Innovation is both a category and a sub-bucket and is
counted twice. **Do not assume four equal categories.** Watch the remaining slides, and if
no standalone Innovation slide appears, the rules list was simply describing the topics
rather than the scoring. This matters for where effort goes, so it is worth hearing stated.

## B1. Verbatim

> ### UX Evaluation Criteria
>
> **40% — User Centered Design**
> *User Needs:* Does the design solve real user problem effectively?
> *Inclusivity:* How well does it consider diverse user types?
>
> **20% — Usability**
> *Ease of Use:* Is the design intuitive and simple to navigate?
> *Efficiency:* Can users complete tasks quickly with minimal friction?
>
> **20% — Design**
> *Visual Appeal:* Is the design attractive and functional?
> *Information Clarity:* Is important content clearly presented?
>
> **20% — Innovation**
> *Originality:* Is there creativity in the solution?
> *Problem-Solving:* How does it address the challenge you are trying to solve?

## B2. This is the inverse of the Tech picture

Tech found us a zero. UX is the category this project was *built* for, and the 40% bucket
is the one it is strongest in — but only half of it.

| Bucket | Weight | Where we are | What is missing |
|---|---|---|---|
| User Centered Design | **40%** | **User Needs is as strong as it gets.** The problem is a real household's, the first test user is the person who lives it, and the design is grounded in the Vanderbilt TRIAD toolkit with every board naming the National Standards practice it rests on (`SPEC.md §7`). Guardrail 5 — self-injury or escalation surfaces referral guidance instead of a board — is a user-needs decision that cost us a feature | **Inclusivity is close to unwritten.** See B3 |
| Usability | **20%** | The whole design is an efficiency argument: three questions to a printable board in under two minutes, and one tap for the reward question | **"Under two minutes" is a target, never a measurement.** See B4 |
| Design | **20%** | 201 cards built to one visual system, a badge that makes an uploaded photo match the drawn cards, a print sheet with cut lines. Information Clarity is almost the definition of a First→Then board: two pictures, one order | Nothing structural. The weakest link is any screen the demo touches that has not had the day-8 UX pass |
| Innovation | **20%** | Multi-agent compose-and-review; semantic reuse, where *sneakers* finds **Shoes**; tracking promises kept rather than boards made | Originality is argued nowhere in writing — it is visible in the build and absent from the documents a judge reads first |

## B3. Inclusivity is the gap, and it is a 20-point gap

*"How well does it consider diverse user types?"* is half of the 40% bucket — the single
heaviest sub-criterion on either slide so far.

**Searched before claiming it:** `grep -i "accessib|contrast|inclusiv|WCAG|touch target|
font size|nonverbal|pre-reading"` across `SPEC.md`, `CODE-PLAN.md` and `assets/ASSETS.md`
returns **one hit** — caution 4 in `ASSETS.md`, *"green on blue fails contrast"*, which is
an artwork rule, not a UI one. The project is deep on **one** user pair, an autistic child
and their parent, and silent on everyone else.

What is genuinely true and simply not written down yet:

- **The child who does not read.** The board is pictures first by design; the words are
  for the adult to say out loud. That is an inclusivity decision already made.
- **The three-word validator** (`SPEC.md §6`) keeps labels short enough for an early
  reader and is already specified.
- **The printed sheet** is the accessible path for a household with one device, or none at
  the moment it is needed.
- **Tablet use mode** exists for the child-facing view, separate from the parent's editing
  view — two user types, two interfaces, already in the plan.

What is **not** true yet and should not be claimed until it is: contrast ratios checked
against WCAG, touch-target sizes, a reduced-motion path, or any text-size setting. These
are a half-day of real work on the screens that already exist, and the gap is what gets
written rather than what gets built.

## B4. The cheapest strong evidence we are not collecting

Usability asks *"Can users complete tasks quickly with minimal friction?"* and we have a
first test user who is not a developer. **Time her.** From opening the app to a printed
board, once, with a stopwatch, and write the number down. One measured figure from a real
parent outscores any amount of "designed to take under two minutes", and it costs the
length of one board.

Same for the inclusivity claim: watch which screen she hesitates on and fix that one.

## B5. What to do about it, in order

1. **Write the inclusivity section** — in `SPEC.md`, not in a slide. Four items in B3 are
   already true and merely unrecorded; that is an hour.
2. **Check contrast and touch targets** on the screens the demo touches, and fix what
   fails. Half a day, and it converts a claim into a fact.
3. **Measure one real run** with the first test user and record the time (B4).
4. **Say the originality out loud** in whatever the submission turns out to be: the review
   agent, the semantic reuse, and tracking promises kept rather than boards made.

--------------------------------------------------------------------------------

# §C — The submission itself

Source: `Subbmission-details.png`, photographed at 10:22 ET. **This is the answer to L2**
— *"the submission this year will be different"* — and it is different in two ways that
matter more than the format: **the deadline moved, and there are two videos, not one.**

## C1. Verbatim

> ### Submission
> **November 11, 2026 - 2 PM GMT+1**
>
> | | **Tech Video** | **Demo** |
> |---|---|---|
> | **Primary Audience** | Product Management | Demo, UX and Innovation juries |
> | **Max Duration** | Up to **10 minutes** | Strictly max **5 minutes** |
> | **Core Goal** | Prove your technical execution under the hood | Pitch your solution, user story, and real-world impact |
> | **Focus** | Technical implementation, key architectural decisions, and agent workflows | The problem, the live app in action, the nonprofit value and innovation |

## C2. The deadline — read this twice

**November 11, 2026, 2 PM GMT+1 = Wednesday 11 November, 08:00 EST in New York.**
GMT+1 is CET; 14:00 CET is 13:00 UTC; the US left daylight saving on 1 November, so New
York is UTC−5. Checked with `TZ=America/New_York date`, not estimated.

Two things follow, and the second is the dangerous one:

1. **Two more days.** The rules said 9 November and the Taikai timeline disagreed by about
   eleven hours — **that is L5, and it is now answered: both were wrong.** The date moved
   out to the 11th.
2. **The final morning does not exist.** 08:00 in New York is before a normal working day
   starts. Everything must be finished and uploaded **the night of Tuesday 10 November**,
   and the only safe plan treats **Tuesday evening as the deadline**. A plan that plans to
   "finish on the 11th" has already missed it.

Also worth re-checking: `PRE-BUILD-LAB.md` schedules deleting the AWS lab key on 10
November, which is now the night everything ships. Move it to the 11th or do it earlier —
not on the busiest evening of the week.

## C3. Two videos, and only one of them was planned

`SPEC.md` day 8–9 says *"Record and cut the five-minute demo"*. That is the **Demo** video
and the duration matches exactly — *strictly* max 5 minutes, so it is a hard cut.

**The 10-minute Tech Video is entirely new work and nothing in the plan accounts for it.**
It is also the single best thing that has happened to the Tech score this morning, because
it solves the evidence problem from §A3: a submission cannot *claim* Mentor was used, and
now there is a ten-minute slot whose stated purpose is *"technical implementation, key
architectural decisions, and agent workflows"*. Mentor, Agent Workbench, the knowledge
base, semantic search, the DataFabric connection and the Web/Agentic split are all things
to **show on screen** rather than assert.

| | Tech Video | Demo |
|---|---|---|
| Scores | §A, all four tech buckets | §B, plus the Demo and Innovation juries |
| Audience | *Product Management* — technical, but not the people who wrote our code | Three juries at once |
| Length | up to 10 min — a ceiling, not a target | **strictly** 5 min — a wall |
| Already planned | **No.** New work | Yes, `SPEC.md` day 8–9 |
| Hardest part | Showing Mentor and DataFabric actually running | Cutting it to 5 minutes |

## C4. "Demo, UX and Innovation juries" settles B0 — and raises the stakes

There are **separate Demo, UX and Innovation juries**, so Innovation is a category of its
own *and* a 20% bucket inside the UX slide. The B0 warning is resolved in the direction
that costs us if ignored: **innovation is scored twice, by two different juries, from the
same five-minute video.** It is the highest-leverage thing to say out loud in the Demo,
and §B2 noted it is currently argued nowhere in writing.

## C5. "The nonprofit value" — the one phrase we have to handle carefully

The Demo's stated focus includes **the nonprofit value**, and this project has no
nonprofit partner — confirmed this morning by the organisers, who have none either
(`TWILIO-WITHDRAWN-2-NOV.md` sits next to that answer in the same reply set).

**Do not paper over it, and do not invent a relationship.** `CLAUDE.md §2` is absolute on
this. The honest and stronger line is that *nonprofit value* is about who the work serves,
not who signed a letter:

- The clinical grounding is **public material from nonprofits** — the Vanderbilt Kennedy
  Center TRIAD toolkit published through the Autism Speaks Autism Treatment Network, and
  the National Autism Center's National Standards Report. Every board names the practice
  it rests on.
- The beneficiaries are **families**, and the first test user is one.
- The adoption story is real and costs nothing to state: an autism organisation could hand
  this to parents without licensing anything, because it is MIT-licensed and the evidence
  base is already theirs.

Say that plainly in the Demo and it reads as rigour. Imply a partnership and one jury
member who knows the field ends the entry.

## C6. What this changes, in order

1. **Re-plan the days.** Two more of them, a morning deadline, and a second video that was
   never in the schedule. `SPEC.md`'s table is now wrong in both directions.
2. **Write the Tech Video outline early**, because it is the only place the Tech criteria
   get *shown*, and because what it needs to film dictates what gets built first.
3. **Move the AWS key deletion off 10 November** (C2).
4. **Draft the nonprofit-value paragraph once**, carefully (C5), and reuse it everywhere.
5. ~~Still unknown: where the two videos are uploaded~~ — **answered 10:26, see C7:**
   both go on the Taikai project page, the Demo as a YouTube/Vimeo link in the **Gallery**
   and the Tech Video as a link in the **Description**. ~~Still unknown: whether the
   4 November mid-submission survives~~ — **it does not exist. There is no mid-week
   submission at all**, confirmed at the kickoff. Nothing is due before 11 November.

## C7. Where the two videos actually go — answered 10:26 ET

Source: `more-details2.png`, a walkthrough of the Taikai project page.

> **Unpublished Project.** This is a draft project that only you and your team can view.
> After editing your project, don't forget to publish it.
> **After you publish the project, it will be visible to everyone.**
>
> **Gallery** → *Links from platform like youtube, vimeo…*
> "Here you can have a slider with your presentation video and project images. To add a
> video, please click on the button above, and to add images, please add them to the
> attachments section at the bottom of the page."
>
> **Description** → *Links from Google drive and similar*

So **there is no separate upload portal**: both videos go on the **Taikai project page**,
which is the page already published at 139 views. Two different fields take two different
kinds of link:

| | Goes where | As what |
|---|---|---|
| **Demo** (5 min) | **Gallery** | A YouTube or Vimeo link — it is the presentation video in the slider |
| **Tech Video** (10 min) | **Description** | A Google Drive or similar link. Nothing stops it being a second YouTube link, and that is probably better than Drive for a juror who just wants to press play |
| Project images | Attachments, at the bottom of the page | Not the Gallery directly — the Gallery pulls from attachments |

**Three things that follow:**

1. **The unlisted video decision survives.** `CLAUDE.md §2` records that the concept video
   is unlisted by A.J.'s choice. An unlisted YouTube link works exactly like a public one
   for anyone holding it, so both submission videos can stay unlisted. **Unlisted is not
   private** — do not confuse the two — but it keeps them off search and off the channel.
2. **Editing the page unpublishes nothing, but publishing is a separate click.** The
   banner is explicit: *"After editing your project, don't forget to publish it."* The
   project is already live, so a last-minute edit that is never published is a silent
   failure mode on the morning of the 11th. **Publish, then reload the public URL and
   look at it.**
3. **The description field now has a job beyond prose.** It carries the Tech Video link,
   so the wording rewrite in `TWILIO-WITHDRAWN-2-NOV.md` and the video link should be done
   in one pass rather than two edits to the same field.
