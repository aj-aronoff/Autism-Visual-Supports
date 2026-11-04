# Phase 1 Plan: Hackathon MVP (Ship by Nov 10)

**Scope:** Minimal viable product for OutSystems hackathon submission. Two agents working, child profiles, generated boards, safety stories. No Phase 2 features (fading, image analysis, effectiveness tracking).

**Deadline:** Tuesday, November 10, 2026 (shipping night)  
**Days remaining:** 7 days

---

## Architecture Overview

```
Parent / Child
    ↓
Child Profile Form
    ↓
Scenario Input ("Going to the doctor")
    ↓
[Agent 1: If-Then Architect] ←→ Bedrock Haiku5_5
    ↓
Generate: 2-3 customized First→Then boards
    ↓
Display + Printable Format
    ↓
[Agent 2: Safety Story Co-Creator] ←→ Bedrock Haiku5_5
    ↓
Generate: Comfort story (child OR parent focused)
    ↓
Display + Interactive checkpoints
```

---

## Core Features (Phase 1)

### 1. Child Profile Setup
**What:** Single form to capture child context once, reuse across all scenarios.

**Fields:**
- Child name (for personalization)
- Child age (for story language + board complexity)
- Special interests (3-5: e.g., "space", "dinosaurs", "trains")
- Sensory sensitivities (checklist: lights, sounds, crowds, textures, smells)
- Favorite snacks (for "Then" steps)
- Favorite toys/fidgets (for "Then" steps)
- Favorite activities/rewards (for "Then" steps)
- Sensory kit items available (checkbox: headphones, blanket, fidget, chewlery, lanyard)
- Does child read? (yes/no, for board text complexity)
- Preferred story tone (brave hero | cozy comfort | matter-of-fact)

**Data Storage:** ODC Entity (Child)

**UX:** One-time setup, but editable anytime

---

### 2. Scenario Input + Board Generation

**Workflow:**
1. Parent enters: "Going to the grocery store"
2. Optional: Parent selects from common scenarios OR types custom
3. System prompts If-Then Agent with:
   - Child profile
   - Scenario
   - Sensory kit available to them

**If-Then Agent Output:**
- **3 board variations:**
  - Standard Transition (basic sequence)
  - High-Sensory Input Transition (incorporates fidget, music, movement)
  - On-the-Go Emergency Transition (minimal steps, quick reference)
- **Format:** ASCII mockup (for display) + SVG (for printing)
- **Each board:** 
  - 4-6 steps maximum
  - Icons (reference existing 201 SVG card library)
  - Text minimal, concrete language
  - Sensory kit items called out (↔️ Headphones, 🧸 Fidget, etc.)

**Data Storage:** ODC Board entity
```
Board:
  - id
  - child_id
  - scenario ("grocery store")
  - created_date
  - board_variation ("standard" | "high_sensory" | "emergency")
  - content (SVG + text)
  - printable_format (PDF-ready)
```

---

### 3. Meltdown Agent: Safety Stories

**Trigger:** Parent or child taps "Need a comfort story?" during or before stressful scenario

**Agent 2 Workflow:**
1. Agent determines target audience: **Is this for the child or the parent?**
   - Child story: First person, simple rhythm, sensory language, interactive checkpoints
   - Parent story: Reassurance narrative, what to do, coping strategies, when to use sensory kit
2. Generate story specific to scenario
3. Include 2-3 interactive checkpoints (pauses where child/parent responds)

**Example Child Story (Doctor visit):**
```
"I'm going to the doctor's office. It might feel a little scary.

[CHECKPOINT] What sensory tool would you pick? 
(Headphones? Fidget? Blanket?)

The doctor's office has bright lights and beeping sounds. That's normal.
My headphones help me feel calm when it's too loud.

[CHECKPOINT] How does your body feel right now? 
(Calm? A little worried? You can feel both.)

The doctor will ask me to sit still. I can do this because I have my fidget.
My fidget keeps my hands happy while I'm sitting.

[CHECKPOINT] What will you tell the doctor if you feel scared?"
```

**Data Storage:** ODC Story entity
```
Story:
  - id
  - child_id
  - scenario
  - target_audience ("child" | "parent")
  - content (text + checkpoints)
  - created_date
```

---

### 4. Board Display + Printable Format

**On Screen:**
- Display selected board variation
- Show sensory kit items called out in the board
- "Print this board" button
- "Generate new variation" button
- Printable format: A4 or 8.5x11, ready to laminate

**Print Output:**
- High-contrast version (for visual clarity)
- Icons large enough for quick recognition (target: 2 inches)
- Text concise (avoid fine print)

---

### 5. Pre-Printed Card Links

**What:** For scenarios where custom cards don't fit templates, provide links to standard pre-printed card resources.

**Implementation:**
- Meltdown Agent can suggest: "For this scenario, consider these standard cards from the web"
- Provide 3-5 relevant links (user must fetch externally, not embedded)
- Example: 
  - "Calm-down routine cards" (link)
  - "Sensory overload alert cards" (link)
  - "Waiting patiently cards" (link)

**Data Storage:** Reference list (URL + title)

---

## Data Model (ODC)

```
CHILD
  - id (PK)
  - name
  - age
  - special_interests (list)
  - sensory_sensitivities (list)
  - favorite_snacks (list)
  - favorite_toys (list)
  - favorite_activities (list)
  - sensory_kit_items (list: headphones, blanket, fidget, chewlery, lanyard)
  - can_read (boolean)
  - preferred_story_tone (enum)
  - created_date
  - updated_date

BOARD
  - id (PK)
  - child_id (FK)
  - scenario (string: "grocery store", "doctor", etc.)
  - board_variation (enum: "standard" | "high_sensory" | "emergency")
  - content (SVG + markdown)
  - printable_format (binary: PDF or image)
  - created_date
  - updated_date

STORY
  - id (PK)
  - child_id (FK)
  - scenario (string)
  - target_audience (enum: "child" | "parent")
  - content (text with checkpoints marked)
  - created_date
  - updated_date

CARD_LINK (Reference only, not editable in app)
  - scenario
  - card_type
  - url
  - title
  - description
```

---

## Agents: System Prompts

### Agent 1: Visual Support Architect
**File:** `/handoff/reference/dual-agent-system-prompt.md` (already documented)

**Inputs:**
- Child profile (age, interests, sensory items)
- Scenario
- Board variation (standard | high_sensory | emergency)

**Outputs:**
- 3 board layouts (markdown + ASCII mockup for display)
- SVG references (which icons from the library)
- Sensory kit integrations (text notes on when to use items)

**Constraints:**
- Keep steps to 4-6 maximum
- Language concrete, no figurative language
- All text <20 words per step
- Always mention sensory kit items

### Agent 2: Safety & Story Co-Creator
**File:** `/handoff/reference/dual-agent-system-prompt.md` (already documented)

**Inputs:**
- Child profile (age, interests, tone preference)
- Scenario
- Target audience (child | parent)

**Outputs:**
- 1st or 2nd person narrative
- 3-4 interactive checkpoints (marked with [CHECKPOINT])
- Validation language ("It's okay to feel...")
- Sensory kit integration (frame as "superpowers")

**Constraints:**
- Child story: simple words, rhythm, sensory language
- Parent story: practical + reassuring
- No scary scenarios (reframe as adventures)
- Always include choice points

---

## Critical Decisions (Locked Nov 4)

### I1: Caching Layer Implementation ✅
**Decision:** Simple ODC DB cache
- Store agent responses in Board entity with timestamp
- TTL: 24 hours
- Invalidate cache when child profile is updated
- Implementation: Basic query before calling Bedrock; if cache hit and <24hrs old, return cached response

### I2: TrialClaudeHaiku Fallback Strategy ✅
**Decision:** Fallback to second trial agent
- Primary: TrialClaudeHaiku (awaiting Slack confirmation)
- Fallback: Second trial agent (clarify which one on Slack)
- Tertiary: BedrockHaiku5_5 (if both trial agents unavailable)
- Handle model selection via config (not hardcoded)

### I3: SVG Icon Integration Strategy ✅
**Decision:** Fallback icons + manual override
- Use existing 201-card SVG library from Autism Visual Supports repo
- Common icons (headphones, fidget, snack, blanket, lanyard) → auto-mapped concept names
- Agent returns concept names; UI looks up SVG from library
- Parent can override/customize icons on board (stretch goal)
- For unknown concepts: use generic icon + parent can replace

### I4: Checkpoint Interaction for Phase 1 ✅
**Decision:** Click-to-continue with ESC exit
- Checkpoints display text + [Continue →] button
- Parent/child taps [Continue →] to advance to next section
- **ESC key skips checkpoint** (optional interaction, not required)
- No text input required in Phase 1 (captures engagement via button taps)

### I5: Pre-Printed Card Library Sourcing ✅
**Decision:** Start with small library
- Phase 1: Curate 10-15 most-common card types only
  - Calm-down routine cards
  - Sensory overload alert cards
  - Transition warning cards
  - Meltdown management cards
  - Social stories
- Phase 2: Expand to 30+ cards
- Agent recommends best fit from small library; parent can search for others

### I6: Error Handling for Agent Failures ✅
**Decision:** Retry once after 2-second delay
- Validate agent output structure (JSON schema check)
- If invalid: automatically retry once after 2-second wait
- If still invalid: show user-friendly error: "Oops, couldn't generate board right now. Try again."
- Log error for debugging; no user-facing stack trace

### I7: Effort Estimate Tracking ✅
**Decision:** Checkpoint Thursday Nov 6 + daily revisions
- Initial estimate: 40 hours (from plan)
- **Thursday Nov 6 checkpoint** (end of Phase 1b):
  - Review: % complete, velocity, blockers
  - Revise estimate based on actual hours burned
  - Adjust scope if timeline at risk (drop features, simplify interactions)
- **Daily brief check-in** (15 min): progress vs. estimate, blockers, next day plan
- **Daily adjust** effort estimate if needed

---

## Implementation Phases (Week of Nov 3-10)

### Phase 1a: Setup & Agent Prompts (Nov 3-5)
- [ ] Finalize Agent 1 system prompt (detailed version from template)
- [ ] Finalize Agent 2 system prompt (child vs. parent variations)
- [ ] Set up ODC project
- [ ] Create ODC entities (Child, Board, Story)
- [ ] Test Bedrock connection (verify Haiku5_5 available)

**Deliverable:** Working agents in Mentor, test calls succeed

---

### Phase 1b: Child Profile Form (Nov 5-6)
- [ ] Design form UI (ODC screen)
- [ ] Build form validation
- [ ] Connect to Child entity
- [ ] Add "Edit Profile" flow

**Deliverable:** Form saves child profile, user can edit

---

### Phase 1c: Board Generation (Nov 6-7)
- [ ] Build scenario input screen
- [ ] Orchestrate Agent 1 call (child profile + scenario → Bedrock)
- [ ] Parse agent output → display 3 variations
- [ ] Generate printable format (SVG layout)
- [ ] Test with 3 real scenarios (doctor, grocery, new place)

**Deliverable:** Board generation working, printable output

---

### Phase 1d: Safety Stories (Nov 7-8)
- [ ] Build "Generate Story" button/flow
- [ ] Implement child vs. parent branching
- [ ] Orchestrate Agent 2 call
- [ ] Display story with interactive checkpoints (clickable)
- [ ] Test stories for both audiences

**Deliverable:** Story generation working, checkpoints interactive

---

### Phase 1e: Refinement & Testing (Nov 8-9)
- [ ] End-to-end user flow test (new user → profile → generate board → generate story)
- [ ] Edge cases (missing fields, empty special interests, etc.)
- [ ] Performance: ensure Bedrock calls return <5 seconds
- [ ] UI polish: error messages, loading states, help text
- [ ] Test on iPad (if available) — check touch targets, font sizes

**Deliverable:** No broken flows, graceful error handling

---

### Phase 1f: Demo & Tech Video (Nov 9-10)
- [ ] Script demo (3-5 min) showing scenario → board → story
- [ ] Film demo (or record screen walkthrough)
- [ ] Script Tech Video (up to 10 min) explaining:
  - Two-agent architecture
  - Bedrock integration (Haiku5_5)
  - Contextual intelligence (child profile grounding)
  - How agents handle neurodiversity-affirming language
  - Phase 2 vision: fading strategy (future work)
- [ ] Final commit & push to main

**Deliverable:** Working demo + video ready for submission

---

## UI Mockup (Rough)

### Screen 1: Child Profile
```
┌─────────────────────────────────┐
│  Child Profile Setup             │
├─────────────────────────────────┤
│ Child's Name: [_________]        │
│ Age: [____]                      │
│                                  │
│ Special Interests (pick 3-5):    │
│ ☐ Space   ☐ Dinosaurs ☐ Trains │
│ ☐ Animals ☐ Music     ☐ Art     │
│                                  │
│ Sensory Sensitivities:           │
│ ☐ Bright lights ☐ Loud sounds   │
│ ☐ Crowds       ☐ Textures       │
│                                  │
│ Favorite Snacks:                 │
│ [_____] [_____] [_____]          │
│                                  │
│ Sensory Kit Available:           │
│ ☑ Headphones ☑ Fidget Toy       │
│ ☐ Blanket    ☐ Lanyard          │
│                                  │
│         [Save Profile]           │
└─────────────────────────────────┘
```

### Screen 2: Scenario Input & Board Display
```
┌─────────────────────────────────┐
│  Create a Visual Support Board   │
├─────────────────────────────────┤
│ Scenario: [Select from list or  │
│           type custom...]        │
│           "Going to the doctor"  │
│                                  │
│         [Generate Boards]        │
│                                  │
├─────────────────────────────────┤
│ BOARD VARIATION: Standard        │
│                                  │
│  FIRST        →      THEN        │
│ [Walk to     →    [Listen to    │
│  doctor's    →     favorite     │
│  office]     →      music on    │
│              →      headphones] │
│                                  │
│  FIRST        →      THEN        │
│ [Wait in     →     [Fidget toy  │
│  waiting     →      in hands]   │
│  room]       →                  │
│              →                  │
│                                  │
│  [Variation 2] [Variation 3]    │
│                                  │
│  [Print Board] [New Scenario]   │
└─────────────────────────────────┘
```

### Screen 3: Generate Story
```
┌─────────────────────────────────┐
│  Safety & Comfort Story          │
├─────────────────────────────────┤
│ For: [Child / Parent] (tab)     │
│ Scenario: Going to the doctor   │
│                                  │
│         [Generate Story]         │
│                                  │
├─────────────────────────────────┤
│ "I'm going to the doctor's      │
│  office. It might feel a little │
│  scary.                          │
│                                  │
│  [What sensory tool would you   │
│   pick?]  ← Interactive          │
│                                  │
│  The bright lights and beeping   │
│  sounds are normal. My headphones│
│  help me feel calm..."           │
│                                  │
│  [How does your body feel?]     │
│                                  │
│         [Print Story]            │
└─────────────────────────────────┘
```

---

## Testing Strategy

### Unit Tests
- Child profile validation (all fields required? defaults?)
- Board parsing (agent output → valid format)
- Story checkpoint parsing (mark interactive points)

### Integration Tests
- End-to-end: profile → board generation → display
- End-to-end: profile → story generation → checkpoints work
- Bedrock calls succeed and return expected structure

### User Testing (if time allows)
- 1-2 parent testers: walk through full flow
- Collect feedback on board clarity, story resonance
- Check print output quality

### Edge Cases
- What if child has no special interests listed?
- What if user tries to generate 10 boards in a row (token cost)?
- What if Bedrock returns malformed JSON?

---

## Known Constraints & Decisions

### Out of Scope (Phase 1)
- ❌ Picture upload or image analysis (Phase 2)
- ❌ Effectiveness tracking / ratings (Phase 2)
- ❌ Fading recommendations (Phase 2)
- ❌ Custom card generation (Phase 2)
- ❌ Multi-child profiles (1 child per session for now)
- ❌ Persistent history across sessions (locked decision: SAVE boards in DB, not ephemeral)

### Early Decisions (From Locked Decisions Doc)
- ✅ Child profile: **Minimal required** (name, age) — others optional
- ✅ Data persistence: **SAVE board history** — parent can revisit and reuse
- ✅ Meltdown agent: **Explicit tabs** — child vs. parent (not auto-detect)
- ✅ Board variations: **Progressive disclosure** — standard first, "show alternatives" button
- ✅ Card library: **Agent-driven with user choice** — agent recommends, parent picks
- ✅ Model: **TrialClaudeHaiku (trial model)** with fallback to second trial agent
- ✅ Caching: **Simple ODC DB cache** (24hr TTL, invalidate on profile change)

### Open A1/A2 Questions (Still Pending)
- **A1:** Does a mocked integration score the same as real Data Fabric?
- **A2:** Is AWS/Microsoft category about sponsored models or personal account?
- ➡️ **Action:** Await Slack response (awaiting info from user on TrialClaudeHaiku availability)

---

## Success Criteria for Phase 1

✅ **By Nov 10 shipping night:**
- [ ] Child profile form works (edit, save)
- [ ] If-Then agent generates 3 board variations for any scenario
- [ ] Boards display on screen + print cleanly
- [ ] Meltdown agent generates child-focused AND parent-focused stories
- [ ] Stories have interactive checkpoints (user can read + interact)
- [ ] No broken flows (all buttons work, errors are graceful)
- [ ] Demo shows end-to-end workflow (3-5 min)
- [ ] Tech Video explains architecture + Phase 2 vision (up to 10 min)

✅ **Scoring alignment:**
- Demo shows neurodiversity-affirming design (UX jury)
- Tech Video shows Bedrock + Mentor agents (Tech jury)
- Agents demonstrate contextual intelligence (child profile grounding)

---

## Notes

- **Token Budget:** Phase 1 is light on Bedrock calls (1-2 per scenario). Token budget is not constraining.
- **ODC Features:** Showcase at least one ODC feature mentioned in kickoff (Mentor orchestration is primary).
- **Effort Estimate:** ~40 hours of development, assuming Bedrock + Mentor APIs are stable.
- **Risk:** API latency (Bedrock calls slow) → mitigation: implement caching or request batching if needed.
- **After Nov 10:** Can pivot to Phase 2 with solid foundation.
