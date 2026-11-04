# Phase 1: Decisions Locked ✅

**Date Locked:** November 3, 2026  
**Status:** Ready for development

---

## Key Strategic Decisions

### 1. Child Profile: Minimal Entry Barrier
✅ **Decision:** Minimal required fields (name, age) — others optional

**What this means:**
- Parent can generate a board with just: child name + age
- Special interests, sensory items, favorite snacks = optional but recommended
- Form shows "recommended" vs. "required" clearly
- Can edit profile anytime to add more detail

**UX Impact:** Lower friction to first board generation. Parent can start experimenting immediately.

**Data Schema:** Mark fields as `required: boolean` in ODC entity.

---

### 2. Data Persistence: Save & Reuse Boards
✅ **Decision:** Save board history — parent can revisit and reuse

**What this means:**
- Every generated board is persisted in ODC
- Parent can see history: "boards generated for [child]"
- Reuse action: parent can load previous board + regenerate variation
- Database schema includes: `Board` entity with created_date, scenario, child_id

**UX Impact:** Parents build up a library of working boards over time. "Go-to" boards for recurring scenarios (morning routine, doctor, school transition).

**Development Impact:** Adds ODC database layer, history view. Medium complexity.

**Token/Cost Impact:** Potential for request caching (see #6).

---

### 3. Meltdown Agent: Explicit Audience Choice
✅ **Decision:** Tabs or buttons — user explicitly chooses (child vs. parent)

**What this means:**
- When generating a safety story, show two tabs/buttons: "For my child" | "For me (parent)"
- User taps one, agent generates story for that audience
- Both versions can be generated if desired (not mutually exclusive)

**UX Impact:** Clear, intentional. Parent knows exactly what they're getting.

**Agent Impact:** Agent 2 system prompt needs clear branching: child narrative vs. parent reassurance narrative. Both are in the same agent, different reasoning paths.

**Alternative considered (not chosen):** Auto-detect based on login. Rejected because explicit is clearer and more flexible.

---

### 4. Board Variations: Progressive Disclosure
✅ **Decision:** Show standard first, "show alternatives" button for others. User states preference.

**What this means:**
- Initial board generation displays: **Standard Transition** (default, simplest)
- Button below: "Show high-sensory variant" + "Show emergency variant"
- Parent can tap to expand and see alternatives
- Preference stored: next time for same scenario, default to preferred variant

**UX Impact:** Less overwhelming UI. Doesn't shove 3 boards at user. Progressive reveal.

**Data Schema:** Add `preferred_variation` to Board entity. Remember user's preference per child.

**Development:** Requires two-stage rendering:
- Stage 1: Generate + display standard only
- Stage 2: Generate other variants on demand (lazy load)

---

### 5. Pre-Printed Card Library: Agent-Driven with Choices
✅ **Decision:** Agent recommends card links, parent picks the path they want

**What this means:**
- When Meltdown Agent generates a story, it suggests: "Here are pre-printed cards that might help:"
- Agent recommends 2-3 most-relevant cards (with brief reason: "for sensory regulation" / "for calming scripts")
- Parent clicks to view/download those cards or search for others
- Parent's choice is final — not prescriptive

**UX Impact:** Personalized recommendations without being rigid. Respects parent expertise.

**Agent Impact:** Agent 2 needs knowledge of card taxonomy:
  - Sensory regulation cards
  - Calming routine cards
  - Transition warning cards
  - Meltdown management cards
  - Social stories

**Data Schema:** Card reference library (curated URLs + metadata):
```
CardReference:
  - id
  - title
  - url
  - category (sensory | routine | transition | meltdown | social-story)
  - scenario_tags (doctor, grocery, airplane, etc.)
  - age_range
  - description
```

---

### 6. Technical: TrialClaudeHaiku + Caching + Model Comparison
✅ **Decision:** Use TrialClaudeHaiku (trial model), add request caching, potentially compare models

**What this means:**
- Primary model: **TrialClaudeHaiku** (awaiting Slack info on availability/limits)
- Fallback: BedrockHaiku5_5 (if trial unavailable)
- **Request Caching:** Same child profile + scenario → cache response (don't call Bedrock again)
  - Caching key: `hash(child_id + scenario + variation_type)`
  - TTL: 24 hours (if child profile changes, cache invalidates)
  - Token savings: Significant (same scenario used multiple times)
- **Model Comparison (stretch goal):** If time allows, A/B test output quality:
  - TrialClaudeHaiku vs. Haiku5_5 on same prompts
  - Measure: parent satisfaction, board clarity, story resonance
  - Report findings in tech video (if meaningful)

**Token Budget Impact:**
- 10M tokens/day budget is ample for Phase 1 if caching implemented
- Without caching: ~2M tokens/day estimated (if 100 unique scenarios, 2 agent calls each)
- With caching: ~200K tokens/day (same scenario reused 10x+)

**Development Notes:**
- Implement caching layer in ODC (simple: store agent responses in Board entity with created_date)
- Invalidation: if child profile updated, clear cache for that child
- Monitor token usage daily via ODC logs or Bedrock CloudWatch

**Slack Action Item:**
- Post: "What are the limits on TrialClaudeHaiku? Can we use it for Phase 1 production, or is it evaluation-only?"
- Clarify: Can we compare TrialClaudeHaiku vs. Haiku5_5 in Phase 1?

---

## Updated Phase 1 Scope (Locked Decisions)

### Features Confirmed
✅ Child profile (minimal fields, editable)  
✅ Board generation (3 variations, progressive disclosure, saved to history)  
✅ Meltdown stories (explicit child vs. parent choice)  
✅ Pre-printed card recommendations (agent-driven, user picks)  
✅ Request caching (token savings + speed)  
✅ Model comparison (if time allows, stretch goal)  

### Out of Scope (Phase 1)
❌ Picture upload / image analysis (Phase 2)  
❌ Effectiveness tracking / parent ratings (Phase 2)  
❌ Fading recommendations (Phase 2)  
❌ Custom card generation (Phase 2)  
❌ Multi-child management (single child per session for now)  

---

## Implementation Impact

### Data Schema Updates
- **Child entity:** Mark fields as required vs. optional
- **Board entity:** Add `preferred_variation`, `printable_format`, `saved_date`
- **Story entity:** No changes (already handles child vs. parent)
- **CardReference entity:** New, for curated card library

### Agent Prompt Updates
- **Agent 1:** Add caching context ("this is a cached response") to disclosure
- **Agent 2:** Enhance with card recommendation logic + taxonomy knowledge

### UX Changes
- Progressive disclosure on board variations
- Explicit tabs for story audience (child vs. parent)
- Card recommendation display in story output
- Board history / reuse flow

### Performance
- Caching layer critical for speed
- Bedrock latency: target <5 sec per unique call
- Cached responses: <100ms

---

## Locked for Development

These decisions are **final for Phase 1**. No revisiting unless:
1. Slack response on TrialClaudeHaiku changes availability
2. A1/A2 scoring questions answered (affects data persistence strategy)

Dev team: Use this document as the specification. Any deviation requires approval.

---

## Next Steps

1. **Confirm TrialClaudeHaiku availability** (post to Slack)
2. **Update PHASE-1-DETAILED-PLAN.md** with decision details
3. **Begin Phase 1a** (Nov 3-5): Setup + agent prompts
4. **Implement caching layer** (critical for Phase 1b)
5. **Test board history persistence** (Phase 1c)

---

**Owner:** A.J. Aronoff  
**Reviewed:** Claude (Haiku 4.5)  
**Status:** Ready for Development
