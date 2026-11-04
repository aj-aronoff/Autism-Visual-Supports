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

## Notes for Developers

- **Do not include Phase 2 in Nov 10 submission** — it dilutes the MVP
- **Phase 1 demonstrates vision strategically** — fading strategy shown in tech video as future roadmap
- **Phase 2 is the innovation moat** — what makes this different from existing visual support tools
- **Clinical grounding is the key** — Phase 2 success depends on evidence-based recommendations, not just AI generation
