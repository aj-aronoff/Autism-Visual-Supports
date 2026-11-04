# Phase 1: Final Locked Specification
## Autism Visual Supports Hackathon MVP

**Version:** 1.0 LOCKED  
**Date:** November 4, 2026  
**Deadline:** Tuesday, November 10, 2026 (shipping night)  
**Days Remaining:** 7 days  
**Status:** Ready for Development

---

## Executive Summary

Build an ODC app with two AI agents that generate:
1. **If-Then visual support boards** (3 variations: standard, high-sensory, emergency)
2. **Safety comfort stories** (child-focused OR parent-focused, with interactive checkpoints)

Both grounded in the child's profile (name, age, interests, sensory kit).

**Tech Stack:** ODC + Mentor agents + TrialClaudeHaiku (primary) or fallback trial agent + caching

---

## Core Features (Final)

### 1. Child Profile Form
**One-time setup, reusable across scenarios**

**Required Fields:**
- Child name
- Child age

**Optional Fields:**
- Special interests (3-5)
- Sensory sensitivities (checklist)
- Favorite snacks
- Favorite toys/fidgets
- Favorite activities
- Sensory kit items available (headphones, blanket, fidget, chewelry, lanyard)
- Can child read? (yes/no)
- Preferred story tone (brave hero | cozy comfort | matter-of-fact)

**UX:** One-time setup, editable anytime

---

### 2. Scenario Input + If-Then Board Generation

**Workflow:**
1. Parent enters scenario ("Going to the doctor")
2. Scenario can be from pre-defined list OR custom text
3. Agent 1 generates 3 board variations

**Output:**
- **Standard Transition** — basic sequence
- **High-Sensory Input Transition** — incorporates fidget, music, movement
- **On-the-Go Emergency Transition** — minimal steps, quick reference

**Display Strategy:**
- Show Standard by default
- [Show alternatives] button reveals other two
- User indicates preference for this scenario

**Board Specs:**
- 4-6 steps maximum
- Format: FIRST → THEN pattern
- Icons: Reference existing 201-card SVG library
- Text: <20 words per step, concrete language
- Sensory kit items called out (🎧 Headphones, 🧸 Fidget, etc.)
- Printable format: A4 or 8.5×11, ready for lamination

**Data Storage:** ODC Board entity
```
- id (PK)
- child_id (FK)
- scenario ("doctor", "grocery", etc.)
- board_variation ("standard" | "high_sensory" | "emergency")
- content (SVG + markdown)
- preferred_variation (user preference for this scenario)
- created_date
- updated_date
```

---

### 3. Meltdown Agent: Safety Stories

**Trigger:** Parent or child taps "Generate Story"

**Target Audience:** **Explicit tabs**
- [For my child] — First person, simple rhythm, sensory language
- [For me (parent)] — Reassurance narrative, what to do, coping strategies

**Output:**
- 1st or 2nd person narrative
- 2-3 interactive checkpoints (marked [CHECKPOINT])
- Validation language ("It's okay to feel...")
- Sensory kit integration (frame as "superpowers")

**Example Child Checkpoint:**
```
[What sensory tool would you pick?]
(Headphones? Fidget? Blanket?)
```

**Data Storage:** ODC Story entity
```
- id (PK)
- child_id (FK)
- scenario ("doctor", "meltdown", etc.)
- target_audience ("child" | "parent")
- content (text with [CHECKPOINT] markers)
- created_date
- updated_date
```

---

### 4. Checkpoint Interaction (Phase 1)

**Implementation:**
- Checkpoint displays text
- Has [Continue →] button
- Parent/child taps to advance
- **ESC key skips checkpoint** (optional interaction)
- No text input required

**Checkpoint Capture:**
- Button tap = engagement signal (may inform Phase 2 effectiveness tracking)
- ESC key press = user chose to skip/skip

---

### 5. Pre-Printed Card Library

**Phase 1 Approach: Start small**

**Library Contents (10-15 cards):**
- Calm-down routine cards
- Sensory overload alert cards
- Transition warning cards
- Meltdown management cards
- Social story cards

**Agent 2 Integration:**
- Agent recommends 2-3 best-fit cards from library
- Card recommendations include URL link
- Parent can click to view/download or search for others
- Parent's choice is final

**Data Storage:** Reference list (URL + title + category)

---

## Data Model (ODC)

```
CHILD
  - id (PK)
  - name (required)
  - age (required)
  - special_interests (optional: list)
  - sensory_sensitivities (optional: list)
  - favorite_snacks (optional: list)
  - favorite_toys (optional: list)
  - favorite_activities (optional: list)
  - sensory_kit_items (optional: list)
  - can_read (optional: boolean)
  - preferred_story_tone (optional: enum)
  - created_date
  - updated_date

BOARD
  - id (PK)
  - child_id (FK) → CHILD
  - scenario (string)
  - board_variation (enum: "standard" | "high_sensory" | "emergency")
  - content (SVG + markdown)
  - printable_format (binary or SVG)
  - preferred_variation (string: user preference for this scenario)
  - created_date
  - updated_date

STORY
  - id (PK)
  - child_id (FK) → CHILD
  - scenario (string)
  - target_audience (enum: "child" | "parent")
  - content (text with [CHECKPOINT] markers)
  - created_date
  - updated_date

CARD_REFERENCE (Reference only, not edited in app)
  - scenario (string)
  - card_type (enum: calm_routine | sensory_alert | transition | meltdown | social_story)
  - url (string)
  - title (string)
  - description (string)
```

---

## Agents & Models

### Agent 1: Visual Support Architect

**Model:** TrialClaudeHaiku (primary) → fallback to second trial agent → BedrockHaiku5_5 (tertiary)

**Inputs:**
- Child profile (age, interests, sensory items, sensory kit available)
- Scenario ("going to the doctor")
- Board variation ("standard" | "high_sensory" | "emergency")

**Outputs:**
- 3 board layouts (markdown + ASCII for mockup)
- SVG icon references (concept names that map to 201-card library)
- Sensory kit integrations (when to use items)

**Constraints:**
- 4-6 steps maximum
- Concrete language, no figurative speech
- All text <20 words per step
- Always mention sensory kit items
- Return structured JSON with clear parsing instructions

**System Prompt:** See `/handoff/reference/dual-agent-system-prompt.md` (Agent 1 section)

---

### Agent 2: Safety & Story Co-Creator

**Model:** TrialClaudeHaiku (primary) → fallback to second trial agent → BedrockHaiku5_5 (tertiary)

**Inputs:**
- Child profile (age, interests, tone preference)
- Scenario
- Target audience ("child" | "parent")

**Outputs:**
- 1st or 2nd person narrative
- 2-3 interactive checkpoints (marked [CHECKPOINT])
- Validation language
- Sensory kit integration (frame as "superpowers")
- Card recommendations (2-3 most-relevant card URLs with rationale)

**Constraints:**
- Child story: simple words, rhythm, sensory language, positive framing
- Parent story: practical, reassuring, warm
- No scary scenarios (reframe as adventures/preparations)
- Always include choice points
- Return structured JSON with checkpoints clearly marked

**System Prompt:** See `/handoff/reference/dual-agent-system-prompt.md` (Agent 2 section)

---

## Implementation Timeline (Week of Nov 3-10)

### Phase 1a: Setup & Agent Prompts (Nov 3-5)
**Owner:** A.J. / Dev team lead

- [ ] Confirm TrialClaudeHaiku availability (post to Slack #Help)
- [ ] Finalize Agent 1 system prompt (detailed version)
- [ ] Finalize Agent 2 system prompt (child vs. parent branches)
- [ ] Set up ODC project & entities (Child, Board, Story, CardReference)
- [ ] Test Bedrock/TrialClaudeHaiku connection
- [ ] Set up caching layer in ODC (basic query-before-call pattern)

**Deliverable:** Working agents in Mentor, test calls succeed, caching layer ready

---

### Phase 1b: Child Profile Form (Nov 5-6)
**Owner:** ODC UI dev

- [ ] Design form UI (ODC screen)
- [ ] Build form validation (name + age required, others optional)
- [ ] Connect to Child entity (create + save)
- [ ] Add "Edit Profile" flow
- [ ] Test with 2-3 scenarios

**Deliverable:** Form saves child profile, user can edit, validation works

**Thursday Nov 6 Checkpoint:** Review progress, revise effort estimate

---

### Phase 1c: Board Generation (Nov 6-7)
**Owner:** Agent orchestration + UI dev

- [ ] Build scenario input screen
- [ ] Orchestrate Agent 1 call (child profile + scenario → TrialClaudeHaiku)
- [ ] Parse agent output → JSON validation (schema check, retry on error)
- [ ] Display 3 variations (standard default, show alternatives button)
- [ ] Map icon concepts to 201-card SVG library
- [ ] Generate printable format (SVG layout, A4/letter size)
- [ ] Test with 3 real scenarios (doctor, grocery, school)

**Deliverable:** Board generation working, printable output readable, error handling in place

---

### Phase 1d: Safety Stories (Nov 7-8)
**Owner:** Agent orchestration + UI dev

- [ ] Build "Generate Story" button/flow
- [ ] Implement child vs. parent branching (explicit tabs)
- [ ] Orchestrate Agent 2 call
- [ ] Parse output → checkpoint detection ([CHECKPOINT] markers)
- [ ] Display story with [Continue →] buttons
- [ ] Implement ESC key to skip checkpoints
- [ ] Test stories for both audiences

**Deliverable:** Story generation working, checkpoints interactive, both audiences tested

---

### Phase 1e: Refinement & Testing (Nov 8-9)
**Owner:** QA + all devs

- [ ] End-to-end user flow (new user → profile → generate board → generate story)
- [ ] Edge cases:
  - Missing optional fields (should still generate board)
  - Empty special interests (agent should still work)
  - Very long scenario text (truncate gracefully)
  - Bedrock timeout / retry logic working
  - Invalid JSON from agent (retry, then show error)
- [ ] Performance: Bedrock calls return <5 seconds (cached or new)
- [ ] UI polish:
  - Error messages are user-friendly
  - Loading states visible (especially during Bedrock calls)
  - Help text for each form field
  - Color palette correct (reference: CalmSkiesTravel colors)
  - Fonts: Atkinson Hyperlegible (or similar high-legibility)
- [ ] Accessibility:
  - Contrast ratio ≥ 4.5:1 (WCAG AA)
  - Keyboard navigation (tab between fields, arrow keys in tabs)
  - No auto-playing audio/animations
  - Icons have alt text

**Deliverable:** No broken flows, graceful error handling, accessible, performant

---

### Phase 1f: Demo & Tech Video (Nov 9-10)
**Owner:** A.J. + dev team

- [ ] Script demo (3-5 min):
  - New user creates profile
  - Enters scenario ("going to the doctor")
  - Sees 3 board variations
  - Generates story for child
  - Shows [Continue] checkpoint interaction
  - Prints board
- [ ] Film/record demo (screen walkthrough or live walkthrough)
- [ ] Script Tech Video (up to 10 min):
  - Two-agent architecture (If-Then + Safety Story)
  - Bedrock model integration (TrialClaudeHaiku + fallback strategy)
  - Contextual intelligence (child profile grounding)
  - Neurodiversity-affirming language (first-person, concrete, warm)
  - Caching strategy (token efficiency)
  - Phase 2 vision: fading strategy, effectiveness tracking
- [ ] Final commit & push to main

**Deliverable:** Working demo + Tech Video ready for submission

---

## Critical Implementation Details

### Caching Layer (I1 - LOCKED)
```
When generating boards:
1. Check cache: hash(child_id + scenario + variation_type)?
2. If cache hit + <24hrs old → return cached response
3. If cache miss or expired → call Bedrock → store in cache with timestamp
4. On child profile update → invalidate all caches for that child_id
```

Implementation: Store cache in Board entity with `created_date` or separate cache table in ODC.

### Model Fallback Strategy (I2 - LOCKED)
```
1. Try TrialClaudeHaiku (primary)
2. If unavailable → try second trial agent (clarify which on Slack)
3. If both fail → fall back to BedrockHaiku5_5
4. Handle via config (not hardcoded in agent calls)
```

### SVG Icon Mapping (I3 - LOCKED)
```
Agent 1 returns: concept names ("put on headphones", "wait", "snack break")
UI maps to 201-card library:
  - Common concepts (headphones, fidget, snack, blanket, lanyard) → auto-mapped icons
  - Unknown concepts → use generic icon + parent can override (stretch goal)
```

### Checkpoint Interaction (I4 - LOCKED)
```
Story displays text + [Continue →] button
- Tap [Continue →] → advance to next checkpoint
- Press ESC → skip checkpoint, go to end of story
- No required text input in Phase 1
```

### Pre-Printed Card Library (I5 - LOCKED)
```
Start with 10-15 most common cards:
  - Calm-down routine (sample URLs to be sourced)
  - Sensory overload alert
  - Transition warning
  - Meltdown management
  - Social story

Agent 2 recommends 2-3 best-fit cards with URLs.
Parent clicks to view/download or search for more.
```

### Error Handling (I6 - LOCKED)
```
When Bedrock returns invalid JSON:
1. Validate against schema (expected structure)
2. If invalid → retry once after 2-second delay
3. If still invalid → show user: "Oops, couldn't generate board right now. Try again."
4. Log error for debugging (but no stack trace to user)
5. Handle gracefully without crashing the flow
```

### Effort Tracking (I7 - LOCKED)
```
- Initial estimate: 40 hours
- Thursday Nov 6 checkpoint: Review % complete, revise estimate
- Daily 15-min check-in: progress vs. estimate, adjust scope if needed
- Daily revise effort estimate based on actual velocity
```

---

## Success Criteria (FINAL)

✅ **By Nov 10 shipping night, these MUST be true:**

**Functionality:**
- [ ] Child profile form works (create, save, edit)
- [ ] If-Then agent generates 3 board variations for any scenario
- [ ] Boards display on screen + print cleanly (A4/letter, readable contrast)
- [ ] Meltdown agent generates child-focused AND parent-focused stories
- [ ] Stories have [Continue →] interactive checkpoints
- [ ] ESC key skips checkpoints
- [ ] Caching works (same scenario = fast second load)
- [ ] Error handling: retry + user-friendly message if Bedrock fails

**Quality:**
- [ ] No broken flows (all buttons work, paths are complete)
- [ ] No crashes (edge cases handled gracefully)
- [ ] Loading states visible during Bedrock calls
- [ ] Help text / guidance on forms

**Accessibility:**
- [ ] Color palette: Calm Skies Travel colors (from reference doc)
- [ ] Font: Atkinson Hyperlegible or high-legibility alternative
- [ ] Contrast: ≥ 4.5:1 (WCAG AA)
- [ ] Keyboard navigation works
- [ ] No auto-play audio/animations
- [ ] Icons have alt text

**Demos & Submission:**
- [ ] Demo (3-5 min) shows end-to-end workflow
- [ ] Tech Video (up to 10 min) explains architecture + Phase 2 vision
- [ ] All code committed & pushed to main
- [ ] Readme updated with how to run the app

**Scoring Alignment:**
- Demo shows neurodiversity-affirming design (UX jury)
- Tech Video shows Bedrock + Mentor agents + caching (Tech jury)
- Agents demonstrate contextual intelligence (child profile grounding)
- Stories show "one guide, two voices" pattern (Innovation jury)

---

## Known Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|-----------|
| TrialClaudeHaiku unavailable | Medium | Fallback to second trial agent, then BedrockHaiku5_5 |
| Bedrock API latency | Low | Caching + <5 sec timeout acceptable |
| Agent JSON parsing failures | Medium | Schema validation + retry logic (I6) |
| SVG icon library unclear | Medium | Use existing 201-card library from repo, clarify mapping |
| Effort estimate underestimated | Medium | Daily tracking (I7), adjust scope if needed |
| Accessibility not met | Low | Use reference guide from CalmSkiesTravel + WAVE testing |

---

## Phase 2 (Post-Hackathon)

See `PHASE-2-FUTURE-WORK.md` for:
- Fading strategy intelligence
- Effectiveness tracking UI
- Custom card text generation
- Picture upload + image analysis
- Fading knowledge base

**Phase 1 does NOT include these features.**

---

## Reference Documents

- `PHASE-1-DETAILED-PLAN.md` — Full plan with rationales
- `PHASE-1-DECISIONS-LOCKED.md` — All decisions from clarifying questions
- `REFERENCE-FROM-CALMSKIESTRAVEL.md` — Design, accessibility, color palette, icons
- `dual-agent-system-prompt.md` — Agent 1 & 2 detailed prompts
- `/handoff/` directory — All original hackathon handoff materials

---

## Immediate Actions (Nov 4)

1. **Post to Slack #Help:**
   - TrialClaudeHaiku availability + limits?
   - Which is the "second trial agent" for fallback?
   - A1/A2 scoring questions (if not yet answered)

2. **Dev Team Setup:**
   - Read this document (PHASE-1-FINAL-LOCKED.md) in full
   - Read `REFERENCE-FROM-CALMSKIESTRAVEL.md` for design/accessibility
   - Read `dual-agent-system-prompt.md` for agent specifications
   - Clone repo, set up ODC project, create entities

3. **Thursday Nov 6 Checkpoint:**
   - 15-min sync: What's done, what's blocked, revise estimate
   - Adjust scope if timeline at risk

---

**Status:** ✅ LOCKED AND READY FOR DEVELOPMENT

*Last Updated: November 4, 2026*
*Owner: A.J. Aronoff*
*Ready for: Dev Team to execute*
