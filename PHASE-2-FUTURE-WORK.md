# Phase 2: Post-Hackathon Future Work

**Status:** Not in scope for hackathon submission. Documented here as foundation for v1.1 development.

---

## 1. Fading Strategy Intelligence Layer

### Overview
The If-Then boards are deliberately designed to be used temporarily, then intentionally *faded* as the child develops independence. Phase 2 adds automated fading recommendations grounded in behavioral data and evidence-based literature.

### Implementation
- **Board Effectiveness Tracking**: Parent rates each board (1-5 scale) after use
- **Usage Analytics**: Track when boards were used, how often, compliance rate
- **Independence Metrics**: Child's ability to follow without visual support (0-10 scale)
- **Fading Recommendation Engine**: 
  - Analyzes usage history + parent ratings + independence metrics
  - Suggests: "Ready to fade" | "Keep as-is" | "Modify and continue"
  - Cites evidence-based fading protocols (ABA, functional independence models)
  - Recommends next-level independence goal

### Data Schema Addition
```
BoardHistory:
  - board_id
  - scenario_id
  - created_date
  - effectiveness_rating (parent input: 1-5)
  - usage_count
  - last_used_date
  - fading_status: (active | fading_in_progress | faded)

FadingLog:
  - board_id
  - fading_date_started
  - strategy_applied (e.g., "remove 2 visual steps", "transition to verbal-only")
  - literature_reference (URL/citation)
  - independence_level_before_fading
  - independence_level_after_fading (measured 2 weeks post-fade)
  - parent_notes
```

### Literature Knowledge Base
Embed or reference:
- ABA fading schedules (thinning, delay, graduated guidance)
- Functional Independence Measurement Scale (FIMS) for autism
- Scaffolding and independence research (Vygotsky ZPD model)
- Autism-specific independence progression studies

### Agent Enhancement
If-Then Agent gains a new reasoning path:
```
INPUT: board_id + usage_history + current_independence_level
OUTPUT:
  - fading_readiness_score (0-100)
  - recommended_strategy (with rationale)
  - literature_citations
  - next_independence_goal
  - updated_board (reduced visual version)
```

---

## 2. Effectiveness Tracking UI

### Parent Dashboard
- **Board History View**: Cards showing each generated board, effectiveness rating, usage count, last used
- **Effectiveness Trend**: Chart of board ratings over time (is this family trending toward independence?)
- **Fading Calendar**: Visual timeline showing which boards have been faded, when, what strategy was used
- **Independence Progress**: Track child's independence score across all scenarios (are they getting better overall?)

### Data Collection Points
- **After-Use Rating**: Parent taps board → sees 1-5 star picker + optional comment box
- **Effectiveness Feedback**: "Did [child] understand the steps?" "Did [child] need repeated prompts?" (checkbox form)
- **Independence Assessment**: Periodically (weekly or after fading) parent rates child on 0-10 scale per scenario

### Metrics Dashboard
- Total boards generated
- Average effectiveness rating
- Most-used scenarios
- Boards successfully faded
- Child's independence progression (slope of improvement over time)

---

## 3. Custom Card Text Generation

### Problem
Pre-printed card templates don't fit every scenario or child. Some boards need custom text that doesn't exist in the library.

### Solution
Meltdown Agent (or new Card-Text Agent) generates custom card text:
```
INPUT:
  - scenario_context (e.g., "airplane flight for first time")
  - child_age
  - reading_level
  - sensory_profile
  - custom_instruction (e.g., "include the flight attendant's name")

OUTPUT:
  - card_text (2-3 lines, simple language)
  - alt_text (for screen readers)
  - suggested_sticker_pairing (reference to existing icons)
  - printable_card_format
```

### Implementation
- Generate on-demand during board creation
- Store generated cards in history (so parent can reuse exact same card later)
- Allow parent to edit before printing
- Tag with source: "generated custom" vs. "pre-printed template"

---

## 4. Picture Upload + Image Analysis

### Workflow
1. Parent takes/uploads photo (e.g., inside a grocery store, the dentist's waiting room, the school playground)
2. Bedrock vision analyzes the image:
   - "I see: bright fluorescent lights, many people, narrow aisles, automatic doors"
   - Identifies sensory triggers from the image
3. If-Then Agent integrates image insights:
   - "You uploaded a photo of the grocery store. I notice bright lights and crowds. Let's add headphones and a fidget to your First step."
4. Board generated with image context embedded

### Data Model
```
Board:
  - reference_image_url (if uploaded)
  - image_analysis (sensory triggers identified by Bedrock vision)
  - image_context_notes (what was detected)
```

### Use Cases
- Parent prepares for doctor visit → uploads photo of waiting room → app generates board with "doctor office lights are bright" context
- New school building → parent takes photo of hallway → app suggests "walking the route" or "noise-canceling headphones near cafeteria"
- Birthday party → photo of venue → app identifies crowds, noise, chaos and structures board accordingly

---

## 5. Fading Knowledge Base

### Embedded or Retrieved
Option A: Embed key fading strategies in system prompt (token-heavy, ~2K tokens)
Option B: Retrieve from external source (Data Fabric, document database) at runtime

### Content Categories
1. **Fading Schedules** (ABA terminology)
   - Stimulus fading (remove visual cues gradually)
   - Temporal fading (delay between "First" and "Then")
   - Prompt fading (move from visual to verbal to gesture)

2. **Independence Progression Markers**
   - What does independence look like at each age?
   - How do you measure "child understands without the board"?

3. **Scaffolding Best Practices**
   - Gradual reduction vs. sudden removal
   - Re-introduction strategies (if child regresses)
   - Cultural/family considerations

4. **Autism-Specific Research**
   - Links to studies on visual supports and fading in autism
   - Best practices from OT/behavioral literature

### Agent Integration
When recommending fading, Agent cites:
```
"Based on [child's name]'s improvement from effectiveness 4/5 → 5/5 and 
independence 6/10 → 8/10, we recommend STIMULUS FADING (remove bottom 2 steps).

Literature: Heflin & Alberto (2001) on visual support fading in autism.
Next checkpoint: Re-assess in 2 weeks."
```

---

## 6. Implementation Priority (if building Phase 2)

**Tier 1 (Highest impact, relatively easy):**
1. Effectiveness Tracking UI (parent ratings + history view)
2. Custom Card Text Generation

**Tier 2 (Medium effort):**
3. Fading Strategy Logic (agent enhancement)
4. Fading Knowledge Base (system prompt or retrieval)

**Tier 3 (Highest complexity):**
5. Picture Upload + Image Analysis (Bedrock vision calls)

---

## 7. Success Criteria for Phase 2

- [ ] Parents rate 80%+ of boards after use
- [ ] Fading recommendations align with clinical literature (audited by OT or behavior analyst)
- [ ] Child independence scores improve measurably (pre/post fading comparison)
- [ ] System successfully identifies boards ready for fading (precision + recall both >80%)
- [ ] Image-based context improves board personalization (measured by parent satisfaction)
- [ ] Custom card generation matches quality of templates (user study with 5+ families)

---

## 8. Post-Hackathon Roadmap

**Month 1 (Dec 2026):** Effectiveness tracking UI + custom card generation  
**Month 2 (Jan 2027):** Fading logic + knowledge base integration  
**Month 3 (Feb 2027):** Picture upload + image analysis  
**Month 4 (Mar 2027):** Clinical validation study with 10 families  

---

## Deferred on 7 November 2026: the Safety & Story Co-Creator

`prompts/AGENT-2-SAFETY-STORY-COCREATOR.md` was built for Phase 1 and is **deferred to
Phase 2 by A.J.'s decision**, for two reasons that were measured rather than argued:

1. **The knowledge base cannot ground it.** The TRIAD toolkit has **zero hits for "story"
   or "social story"**. The National Standards extract names *Story-based Intervention
   Package* among the eleven established treatments, so it supports the *claim* but
   carries **no method**. Shipping it would mean generating guidance that cites nothing,
   against the one claim this whole project rests on.
2. **It gives de-escalation advice with no referral path.** All 581 lines searched for
   `refer`, `professional`, `therapist`, `crisis`, `911` — the only hits are the word
   *doctor* inside example story text. Guardrail 5 is the only guardrail with a safety
   cost if it is wrong, and that file has no equivalent of it.

**What Phase 2 needs before this resumes**, in order:

- A **third knowledge-base document covering how a social story is actually written.**
  Carol Gray's Social Stories criteria are the obvious candidate and are **copyright —
  never re-host**, the same rule that already governs the TRIAD toolkit: private
  grounding is not republishing. Run both checks we already run on any new source — does
  the PDF have a text layer, and is the source clinical or commercial.
- **A referral path inside the story agent itself**, not only in the caller. Guardrail 5
  branches *before* composing; a story agent needs the same branch.
- **A decision on the word "meltdown".** It is on the escalation blocklist at
  `tools/guardrails.py` AND flagged as non-affirming by Reviewer question 5, so our own
  pipeline refuses the word the feature is named after. Many autistic adults use the word
  about themselves; the point is that the two files must agree, whichever way it goes.

The sibling file `prompts/AGENT-1-IF-THEN-ARCHITECT.md` is also not shipping, but for a
different and happier reason: its three best ideas were **ported into the shipping
prompts** on 7 November rather than deferred. Its banner lists where each one went.

---

## 8. The parent in distress — deferred by A.J. on 9 November 2026

**A.J.'s decision, and it set the scope rather than deferring a feature:**
*"Let's keep meltdown as is. Make a note for the future to check for parent 'meltdown every
day'. This is focused on the child. Helping the child will help the parent."*

### What was decided

`meltdown` **stays in the guardrail 5 escalation list** as a trigger, so a message containing
it returns referral guidance instead of a board. The recommendation on the table was to remove
it — *"a First→Then board is a named antecedent strategy for preventing a meltdown"* — and it
was **declined**. Do not re-open it without A.J.

### The gap this leaves, stated plainly so a later session does not rediscover it

**Nothing in guardrail 5 is about the parent.** Every one of the 21 substrings and 5 regexes
describes something happening to or by the *child*. So a message like
*"meltdowns every day and I cannot cope"* is caught **only incidentally**, by the word
`meltdown`, and *"I am exhausted and I do not know what to do any more"* is not caught at all.

### What Phase 2 would build

- **A separate check, not a wider list.** Parent distress is a different referral with a
  different destination — a caregiver support line, respite services, the parent's own GP —
  not a pediatrician or a BCBA. Folding it into guardrail 5 would send the wrong referral.
- **It must not block the board.** This is the design point that makes it different from
  guardrail 5: a parent at the end of their rope still wants the board. The right behaviour is
  **board plus a quiet line of support**, not a refusal. Guardrail 5 short-circuits; this one
  must not.
- **Frequency and duration are the signal**, not vocabulary — *"every day"*, *"every morning
  for months"*, *"it is getting worse"*. A single hard morning is the normal case and the
  entire reason the app exists.

### Why the scope decision is right as stated

**The app's user is the child, through the parent.** A board that works reduces the thing the
parent is exhausted by, which is a more honest form of help than a leaflet — and a tool that
starts assessing the parent who came for a picture board has changed what it is without
asking. Phase 2 can add support; it should never add surveillance.

---

## Notes for Developers

- **Do not include Phase 2 in Nov 10 submission** — it dilutes the MVP
- **Phase 1 demonstrates vision strategically** — fading strategy shown in tech video as future roadmap
- **Phase 2 is the innovation moat** — what makes this different from existing visual support tools
- **Clinical grounding is the key** — Phase 2 success depends on evidence-based recommendations, not just AI generation

---

## Reply-shape recovery — three cases observed or named, none fixed

Added 11 November 2026, 01:10, after a run failed twice for two *different* shape reasons.

**What was fixed:** `ParseBoardReply` now strips a markdown code fence when the reply **starts**
with one. That was the observed failure — a backtick at position 0, which is well-formed JSON
inside a ```` ```json ```` wrapper. It relaxes no check; everything after parsing runs on exactly
the same content.

**Three cases deliberately left alone, because none of them has been observed:**

1. **Prose before the fence** — *"Here is the board:"* followed by ```` ```json ````. Nothing is
   stripped and the parse fails. **This is the most likely of the three to happen**, because a
   preamble is ordinary model behaviour, so it is the first candidate if this ever recurs.
2. **A one-line fenced reply** — fence, JSON and fence on a single line. The opening-line removal
   does not match, so it fails.
3. **No closing fence** — handled: the opening line is removed and the rest parses if it is
   complete.

**The robust fix for 1 and 2 together**, if it is ever worth doing: take the substring from the
first `{` to the last `}` instead of matching fences. It handles preamble, postamble and one-line
replies in one rule. **It was not done** because it moves from *removing a wrapper* towards
*guessing where the content is*, and the parser's whole value is that it refuses rather than
guesses. That is a decision to make with a clear head and a test case, not at one in the morning
on an unobserved failure.

**Separately, and NOT a shape problem:** the model sometimes nests `evidenceBasis` inside `plan`
instead of at the top level. **Lifting it would be content recovery, not shape normalisation**, and
it sits much closer to the line the parser exists to hold. Left refused on purpose.

**One new observation worth keeping:** on 11 November at 00:50 a single request exhausted the retry
budget on **two different** errors — a fence on the first attempt, and the nested `evidenceBasis`
on the retry after the model had correctly fixed the fence. **One retry is enough for one mistake,
not two.** Whether a second retry is worth ~15,000 tokens and another thirty seconds is a Phase 2
question with a real trade-off on both sides.
