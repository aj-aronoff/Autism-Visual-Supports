# Build specification

Target: OutSystems Developer Cloud. Build window 2–9 November 2026.
A rendered version of this document, with the layouts drawn, is in
[`docs/build-spec.html`](docs/build-spec.html).

---

## 1. The finding that shapes the build

The three prompt drafts in [`prompts/`](prompts/) look like alternatives. They are
not — each ends in the same three-part deliverable, which means the application has a
single stable output shape rather than one per tool type.

| Prompt draft | Shape | Contribution |
|---|---|---|
| `visual-support-prompt.txt` | Fill-in template, single shot | The **API contract** — every field the generator needs, named |
| `prompt-gem-style.txt` | Persona + 3-question intake | The **system prompt** and the image-prompt style rules |
| `if-then-board-prompt.txt` | 5-step interactive coach | The **intake wizard** and special-interest theming |

All three resolve to **cards → caregiver script → implementation guidance**. That
triple is the data model.

## 2. Support types

Four layout templates, from the TRIAD toolkit and the National Standards Report. Each
renders to a print sheet with cut lines and to a full-screen tablet view.

| Type | Cards | Purpose |
|---|---|---|
| First–Then board | 2 | Motivates a non-preferred task by making the reward visible and immediate |
| Visual schedule | 4–8 | Sequences a routine; answers what, how much, when finished, what's next |
| Parameter cards | 1–3 | Wait, stop, limited availability — communicates boundaries |
| Social narrative | n/a | Who/what/when/where/why, delivered *before* the event |

## 3. Data model

Ten entities plus static entities. The child profile is separate from the board, so
the hard part is filled in once and every later board is three questions.

### Child
Filled once, owned by the parent.
`Nickname` · `AgeYears` · `DevelopmentalStage` → static · `VisualStyle` → RealPhotos |
Icons | LineArt | WordsOnly · `LanguageLevel` → PreVerbal | EarlyReader | Reader ·
`SpecialInterests` (drives theming) · `SensoryNotes` · `TriggerNotes`

### Board
One generated support.
`ChildId` · `SupportTypeId` · `Title` · `Goal` · `Obstacle` · `Environment` → Home |
Classroom | Community · `Theme` · `Status` → Draft | InUse | Retired · `AgentRunId`
(traceability) · `Version`

### Card
The atomic unit, ordered within a board.
`BoardId` · `SequenceNo` · `Role` → First | Then | Step | Choice | Wait | Stop | Oops ·
`Label` *(max 3 words, validated)* · `ImagePrompt` · `Image` · `ImageSource` →
Generated | Uploaded | SymbolSet · `AltText`

### CaregiverScript
One or two low-demand phrases per phase.
`BoardId` · `Phase` → Before | During | OnCompletion | IfRefusal · `PhraseText` ·
`WordCount` *(fewest words wins)*

### ImplementationPlan
One per board.
`Placement` · `Reinforcement` · `IfChallengingBehavior` · `Generalization`

### PromptStep
Ordered hierarchy, least intrusive first.
`PlanId` · `Level` · `Kind` → VisualPoint | Gesture | Verbal | Model | PhysicalGuide ·
`Instruction`

### UsageLog
The loop. Written by SMS reply, not by hand.
`BoardId` · `UsedOn` · `Outcome` → Independent | WithPrompt | Refused | Skipped ·
`PromptLevelUsed` · **`RewardDelivered` (required)** · `Notes`

### TokenUsage
Metered AI consumption, written by the server action that wraps every model call —
including failed calls, which are the ones that spend budget invisibly. We have no AWS or
Azure console, so this is our only view of a limited resource. Plan: [`TOKEN-BUDGET.md`](TOKEN-BUDGET.md).
`OccurredOn` · `AgentRunId` · `Operation` → Composer | Reviewer | Illustrator · `ModelId` ·
`InputTokens` · `OutputTokens` · `ImageCount` · `Outcome` → Success | ValidationRetry |
Error · `BoardId`

### CardLibrary
Reuse beats regeneration — a given activity keeps the same picture forever.
`ChildId` · `Label` · `Image` · `TimesUsed`

### EvidencePractice
Static. The 11 National Standards practices. `Name` · `Description` · `Citation`.
Every board cites which it rests on.

## 4. Screens

1. **My Children** — child cards with boards in use and the trust streak.
2. **Child Profile** — the one-time intake.
3. **New Support** — three questions. Tool type can be inferred from the obstacle text.
4. **Board Editor** — reorder, edit labels against the three-word validator, regenerate
   one card's image, or swap in a photo from the child's own life.
5. **Script & Plan** — on its own tab, because this is the part that gets skipped.
6. **Use it** — print sheet (cut lines, sized for lamination and Velcro) or tablet mode
   (large targets, tap to check off, works offline).
7. **Log** — by SMS; in-app logging stays for prompt level and notes.
8. **Share with the team** — read-only board access for a teacher, aide or SLP.

## 5. AI layer

An orchestrated workflow in ODC Agent Workbench, not a single prompt.

- **Composer** reads the profile and the obstacle, picks the support type, and drafts
  cards, script and plan against its knowledge source. Names the practice it used.
- **Reviewer** checks that draft against the design rules and sends it back on drift:
  labels over three words, negative phrasing, missing Then card, card count out of range.
- **Illustrator** searches the child's card library before generating anything new.

Tools: `GetChildProfile` · `SearchCardLibrary` · `CreateBoard` · `AddCard` ·
`SetScript` · `SetPlan` · `GenerateCardImage` · `SendRoutineSms`

### Output contract

```json
{
  "supportType": "FirstThenBoard",
  "title": "First shoes, then swing",
  "theme": "Train station",
  "cards": [
    { "sequenceNo": 1, "role": "First", "label": "Put on shoes",
      "imagePrompt": "Flat vector icon, plain white background, no detail: a child's sneakers",
      "altText": "A pair of sneakers" },
    { "sequenceNo": 2, "role": "Then", "label": "Swing", "...": "..." }
  ],
  "script": [
    { "phase": "Before",       "phrase": "First shoes, then swing." },
    { "phase": "During",       "phrase": "One more shoe, then swing." },
    { "phase": "OnCompletion", "phrase": "All done shoes. Now swing!" },
    { "phase": "IfRefusal",    "phrase": "Shoes first." }
  ],
  "plan": {
    "promptHierarchy": [
      { "level": 1, "kind": "VisualPoint",   "instruction": "Point to the FIRST card." },
      { "level": 2, "kind": "Gesture",       "instruction": "Hold out the shoes." },
      { "level": 3, "kind": "Verbal",        "instruction": "Say \"Shoes first.\"" },
      { "level": 4, "kind": "PhysicalGuide", "instruction": "Hand-over-hand, briefly." }
    ],
    "reinforcement": "Deliver the swing immediately. Do not delay or substitute.",
    "placement": "By the front door, at the child's eye level.",
    "ifChallengingBehavior": "Keep prompting the FIRST task. Stay on the task, not the behavior. Then still give the swing."
  },
  "evidenceBasis": ["Antecedent Package", "Schedules"],
  "citations": ["TRIAD Visual Supports and Autism (2011), First-Then Board"]
}
```

The child's name never appears in an image prompt — prompts say "a child".

## 6. Guardrails

Each is a validation in a server action, so a model that drifts cannot ship a bad board.

1. **Three words maximum per label.** Rejected and regenerated.
2. **Positive phrasing only.** "Don't run" is refused in favour of "Walk".
3. **A First–Then board cannot save without a Then card.** The reward is structural.
4. **Card count within the type's range.** A 12-step schedule for a pre-verbal
   four-year-old is a failure, not thoroughness.
5. **No diagnosis, no clinical advice.** Self-injury, aggression or escalation in the
   obstacle text surfaces referral guidance instead of a board.
6. **Neurodiversity-affirming language**, checked.
7. **The parent owns and can export everything.** Profiles are never training input.

## 7. Evidence basis

| Feature | Practice | Source detail |
|---|---|---|
| First–Then board | Antecedent Package | Modifies what precedes the challenge; cueing and prompt fading |
| Visual & task schedules | Schedules | Answers what, how much, when finished, what's next |
| Social narrative | Story-based Intervention | Who/what/when/where/why, delivered before the event |
| Choice board | Antecedent Package | Constrained choice; open-ended choice can overwhelm |
| Special-interest theming | Antecedent Package | Incorporating special interests into tasks |
| Tap-to-check-off, streaks | Self-management | Child records the behaviour and is reinforced for doing so |
| Prompt hierarchy & fading | Behavior Package | Chaining, positive reinforcement, mand training |
| Share with teacher / SLP | Peer Training, Modeling | Same visuals carried across every setting |

## 8. Build order

One tool type end to end before any second tool type. A First–Then board that
generates, prints, goes on a fridge, texts the parent and records the reward is a
complete five-minute demo. Four half-built tool types are not.

| Day | Ships |
|---|---|
| 2 Nov | Kickoff — re-order everything below against the announced ODC features and scoring |
| 3 | Entities and static entities; child profile |
| 3–4 | Composer + Reviewer, First–Then branch only, returning the JSON contract |
| **4 Nov** | **Mid submission** — problem, use case, AI services and integrations |
| 5 | Three-question wizard → agents → persisted board; three-word validator |
| 5–6 | Illustrator agent, card library reuse, board editor |
| 6 | Print sheet with cut lines; tablet use mode |
| 7 | Twilio script-and-reward SMS; usage log; trust streak |
| 8 | UX pass over every screen the video touches. Nothing new built |
| 8–9 | Record and cut the five-minute demo |
| — | *Roadmap:* visual schedule, parameter cards, social narrative, team sharing, offline |

ODC access opens **after registration closes on 28 October** — not at the kickoff. It may
therefore land on the 29th, giving up to four days on the real platform before 2 November.
Use any such days for the parts the kickoff cannot change: entities, static entities and the
child profile, all settled by this document. Hold the agent wiring until after the kickoff,
because that is where the announced scoring emphasis lands.
