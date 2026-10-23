# Autism Visual Supports — Mid Submission

| | |
|---|---|
| **Hackathon** | Build for the Future 2026 · OutSystems · **Day 3 deliverable, 4 November 2026** |
| **Team** | Autism Visual Supports (one member) — Avram (A.J.) Aronoff, United States |
| **Nonprofit** | An autism nonprofit, introduction requested through the organizers. Autism Speaks named as intent; the Vanderbilt Kennedy Center's TRIAD toolkit is the clinical source the build is grounded in. |
| **Project** | https://taikai.network/outsystems/hackathons/build-for-the-future-2026/projects |
| **Source** | https://github.com/aj-aronoff/Autism-Visual-Supports (MIT) |
| **Video** | 60-second concept: https://youtu.be/qJgrdQss0Rs |

## 1. Problem statement

A child is on the floor with a toy. In four minutes they need shoes on with their go-bag
and they need to be in the car. *We have to go now* does not work, and saying it louder
works less.

What does work is a picture. **First shoes. Then swing.** Two cards, in order, where the
child can see them. This is not a novel idea — it is documented practice. The Vanderbilt
Kennedy Center's TRIAD / Autism Speaks ATN toolkit *Visual Supports and Autism* (2011)
specifies the First–Then board, the visual schedule, parameter cards and the social
narrative; the National Autism Center's *National Standards Report* (2009) places the
underlying practices — Antecedent Package, Schedules, Story-based Intervention, Behavior
Package, Self-management — among its eleven Established treatments.

So the method is settled. **Two things still fail, and both are delivery problems rather
than clinical ones.**

**First, the making.** A single board means finding pictures the child actually
recognises, cropping them, keeping every label inside three words, printing, cutting,
laminating, adding Velcro. Call it forty minutes — and the morning you needed it was
*this* morning. The predictable result is that a parent makes two or three boards, ever,
and then stops. The practice is free and evidence-based and almost nobody sustains it.

**Second, and worse, the trust.** The toolkit is unambiguous about what the board rests
on: *"In order to teach children with ASD the value of the First-Then Board, you must
give them the reinforcing activity or item after they complete the 'first' task.
Otherwise, your child may not trust the board the next time you use it."* A board whose
promise was not kept is not neutral — it is worse than no board, because it has taught
the child that the cards do not mean anything. Every generator that stops at a
nice-looking PDF has solved the easy half of this problem and left the half that decides
whether it works.

**Therefore the problem this project takes on is not "generate a visual support."** It is:
*produce a correct board in under two minutes, and then make it likely that the promise on
it is actually kept.*

## 2. Use case description

**Primary actor** the parent or caregiver of an autistic child, at home, usually under
time pressure, on a phone.
**Secondary actors** the child, who uses the board; a teacher, aide or SLP, who needs the
same visuals in another setting.

### 2.1 One-time setup — the child profile

The parent fills in a profile once: nickname, age, developmental stage, visual style
(real photos / icons / line art / words only), language level (pre-verbal / early reader /
reader), special interests, sensory notes, trigger notes. This is the part that is hard to
answer well, so it is asked once and reused. Every board afterwards costs three questions.

### 2.2 The main path — three questions to a board

1. **Which routine?** *Getting out the door in the morning.*
2. **What is hard about it?** *He won't put his shoes on.*
3. **What does your child actually want afterwards?** *The swing at the park.*

The application infers the support type from the obstacle text, then returns three things
together:

- **The cards** — `First: Put on shoes` → `Then: Swing`, each with a picture and alt
  text, every label three words or fewer, themed to the child's special interest.
- **The caregiver script** — the words to say out loud, at four moments: before, during,
  on completion, and on refusal. Fewest words wins. *"First shoes, then swing."*
- **The implementation plan** — where to put the board, a least-to-most prompt hierarchy
  (point at the card → hold out the shoes → say four words → brief hand-over-hand), and
  what to do if the child escalates: stay on the task, not the behaviour — *and still give
  the swing.*

The parent then either prints the sheet (cut lines, sized for lamination and Velcro) or
opens tablet mode (large targets, tap to check off, works offline).

### 2.3 The loop that makes it work — SMS

At the time the routine is due, **Twilio sends the parent the script** — not a
notification telling them to open an app, the actual words, on the lock screen, where
they are standing at the front door holding a pair of shoes.

Afterwards, one inbound question: **did the reward happen?** A one-word reply writes
`UsageLog.RewardDelivered`. That single field is what the whole method rests on, and it
is precisely the field no parent would ever open an application to fill in. So the home
screen counts **promises kept, not boards made** — because that is the number that
predicts whether the next board will work.

### 2.4 What the judges will be able to replicate

The five-minute demo is one support type carried end to end: profile → three questions →
agents compose and review → board persisted → printable sheet → SMS script out → reply in
→ reward logged → streak updated. One complete loop, not four partial features.

### 2.5 Explicitly out of scope for 9 November

Visual schedules, parameter cards, social narratives, multi-caregiver team sharing and
offline sync are designed in the data model and named as roadmap. They are not being
built this week. **No diagnosis and no clinical advice** at any point: self-injury,
aggression or escalation in the obstacle text surfaces referral guidance instead of a
board.

## 3. Integration and AI services planned to use

### 3.1 OutSystems Developer Cloud

The whole application is built in ODC — reactive web app for the parent-facing screens,
server actions for every validation, and ODC's data model for the nine entities plus
static entities. Exposed REST endpoint for the Twilio inbound webhook. The validations
live in server actions rather than in prompt text, so a model that drifts cannot ship a
bad board.

> The ODC feature set and scoring emphasis presented at the 2 November kickoff will be
> taken as the authority on this section; the plan below is written to be re-ordered
> against it rather than defended.

### 3.2 Agentic AI — ODC Agent Workbench

Not one prompt. An orchestrated workflow of **three agents**, which is also what makes the
reasoning path visible to a judge:

| Agent | Responsibility |
|---|---|
| **Composer** | Reads the child profile and the obstacle, selects the support type, drafts cards, script and plan against its knowledge source, and names the evidence-based practice it used. |
| **Reviewer** | Validates that draft against the design rules and sends it back on drift: a label over three words, negative phrasing, a missing Then card, a card count outside the type's range. |
| **Illustrator** | Searches the child's own card library *before* generating anything, so a given activity keeps the same picture forever — recognition matters more than novelty. |

**Agent tools:** `GetChildProfile` · `SearchCardLibrary` · `CreateBoard` · `AddCard` ·
`SetScript` · `SetPlan` · `GenerateCardImage` · `SendRoutineSms`

**Knowledge source / grounding:** the TRIAD toolkit's layout definitions and the National
Standards Report practice list, loaded as the Composer's knowledge source. Boards cite
which practice they rest on; the content is retrieved, not invented.

**Structured output contract:** every run returns one JSON shape — `cards`, `script`,
`plan.promptHierarchy`, `reinforcement`, `evidenceBasis`, `citations` — which is what lets
the Reviewer and the server-side validators check it mechanically. The contract is in
[`SPEC.md §5`](SPEC.md).

### 3.3 Foundation models

Text generation and review through the LLM access bundled with the hackathon ODC instance
(**Azure OpenAI / Amazon Bedrock**), called from Agent Workbench. Card artwork by
text-to-image generation, library-first: the Illustrator generates only on a library miss.
Image prompts are constrained to flat, high-contrast, plain-background icons — the style
the toolkit calls for — and **never contain the child's name**; prompts say "a child".

### 3.4 Twilio

**Twilio Programmable SMS**, in both directions, and it is load-bearing rather than
decorative:

- **Outbound** — the caregiver script, sent when the routine is due, from the
  `SendRoutineSms` agent tool.
- **Inbound** — the single reward-confirmation question, answered by reply, received on an
  ODC-exposed REST webhook and written to `UsageLog.RewardDelivered`.

SMS is the correct channel here for a specific reason: the moment the data is worth
capturing is the moment the parent's hands are full. Anything that requires opening an
application loses that moment, and with it the only field that tells you whether the board
is still trusted.

### 3.5 Other

Print/PDF generation for the laminate-ready sheet with cut lines. No third-party image
libraries, no external analytics, no profile data used as training input — the parent owns
and can export everything.

---

## Build order to final submission

| Day | Ships |
|---|---|
| 2 Nov | Kickoff — re-order everything below against the announced ODC features and scoring |
| 3 | Entities and static entities; child profile |
| 3–4 | Composer + Reviewer, First–Then branch only, returning the JSON contract |
| **4 Nov** | **This document** |
| 5 | Three-question wizard → agents → persisted board; three-word validator |
| 5–6 | Illustrator agent, card library reuse, board editor |
| 6 | Print sheet with cut lines; tablet use mode |
| 7 | Twilio script-and-reward SMS; usage log; promises-kept streak |
| 8 | UX pass over every screen the video touches. Nothing new built |
| 8–9 | Record and cut the five-minute demo |

Full data model, screen flow, guardrails and evidence mapping: [`SPEC.md`](SPEC.md).

*First → Then. Print it, post it, trust it.*
