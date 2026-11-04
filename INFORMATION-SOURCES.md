# Information Sources & References
## Autism Visual Supports Hackathon Project

**Document Date:** November 4, 2026  
**Source Material Collection:** Nov 3-4, 2026  
**Purpose:** Transparency on where design decisions, accessibility standards, and implementation guidance originate

---

## Planning Documents (Created Nov 3-4, 2026)

### Phase 1 Planning
- **PHASE-1-DETAILED-PLAN.md** — Comprehensive implementation roadmap with rationales
  - Created by: Claude Code
  - Based on: Handoff documents, clarifying questions feedback, locked decisions
  - Contains: Architecture, features, timeline, data model, testing strategy
  - Status: Updated with all locked decisions embedded

- **PHASE-1-FINAL-LOCKED.md** — Dev-ready specification (concise, actionable)
  - Created by: Claude Code
  - Audience: Development team
  - Contains: 7 locked decisions (I1-I7), success criteria, immediate actions
  - Status: Ready for dev team to execute

- **PHASE-1-DECISIONS-LOCKED.md** — All strategic decisions documented
  - Created by: Claude Code (synthesized from user feedback)
  - Contains: 6 clarifying questions + 1 tracking mechanism (I1-I7)
  - User's choices documented Nov 4, 2026

### Phase 2 Planning
- **PHASE-2-FUTURE-WORK.md** — Post-hackathon roadmap
  - Created by: Claude Code
  - Status: Reference only, not in scope for Nov 10 submission
  - Contains: Fading strategy, effectiveness tracking, custom cards, image analysis, KB design

---

## Reference Materials (From External Project)

### CalmSkiesTravel Project
**Source:** https://github.com/aj-aronoff/CalmSkiesTravel (public repo)  
**Author:** A.J. Aronoff  
**Date Accessed:** November 4, 2026

**Files Referenced:**
1. **CalmSkiesColorPalette.md** — Autism-friendly color palette
   - 11 core colors (Calm Sky Blue, Meadow Green, etc.)
   - WCAG AA/AAA compliance verified
   - Decision rationales included
   - Used for: Hackathon project color scheme

2. **ACCESSIBILITY_REPORT.md** — Autism-specific accessibility standards
   - WCAG 2.1 compliance checklist (AA level)
   - Autism-specific design decisions beyond WCAG
   - Language rules (first-person, concrete, warm)
   - Sensory safety principles
   - Font choice: Atkinson Hyperlegible (justified)
   - Used for: Hackathon project accessibility framework

3. **index.html** — Sample webpage (Two Voices pattern)
   - Demonstrates parent + child tab-based navigation
   - Semantic HTML structure
   - Tab pattern with ARIA labels
   - Used for: UI design pattern reference

4. **icons/** folder — Icon library
   - Journey stage icons (home, airport, plane, destination)
   - Character icons (child, parent)
   - Used for: Visual reference (hackathon will use existing 201-card SVG library)

**Attribution:** All materials from CalmSkiesTravel are referenced with attribution. Colors, accessibility principles, and design patterns are adapted (not reused directly) for the hackathon project.

---

## Handoff Documents (From Original Hackathon Repo)

**Source:** /handoff/ directory in Autism-Visual-Supports repo  
**Author:** A.J. Aronoff (original project owner)  
**Date:** Originally Nov 3, 2026

**Key Files Used:**
- **HANDOFF.md** — Overall project context, deadlines, scoring alignment
- **reference/dual-agent-system-prompt.md** — Original dual-agent framework
- **state/RESOURCES-AND-CRITERIA-NOV-2.md** — Scoring criteria & hackathon requirements
- **state/QUESTIONS-consolidated.txt** — Open A1/A2 questions (still pending)

---

## User Input & Clarifications

### Clarifying Questions (Nov 3-4)
- **Source:** Interactive HTML form (clarifying-questions.html)
- **User Input Date:** Nov 4, 2026
- **Questions:** 6 clarifying questions on project scope
- **User Selections:**
  1. Profile fields: Minimal required
  2. Data persistence: Save & reuse boards
  3. Story audience: Explicit tabs (child vs. parent)
  4. Board variations: Progressive disclosure
  5. Card library: Agent-driven with user choice
  6. Model selection: TrialClaudeHaiku + fallback

### Plan Review (Nov 4)
- **Source:** Interactive HTML form (plan-review.html)
- **User Input Date:** Nov 4, 2026
- **Review:** 10 plan minuses + 7 improvement options (I1-I7)
- **User Selections:**
  - I1: Simple ODC DB cache
  - I2: Fallback to second trial agent
  - I3: Fallback icons + manual override
  - I4: Click-to-continue buttons + ESC key
  - I5: Start with small card library
  - I6: Retry once then show error
  - I7: Daily tracking + Thursday checkpoint

---

## Research & Validation

### Autism-Specific Design (Validation Sources)
**Sources consulted:**
1. **Carol Gray's Social Story Framework** — Evidence-based intervention for autism (referenced in CalmSkiesTravel ACCESSIBILITY_REPORT.md)
2. **Atkinson Hyperlegible Font** — Braille Institute design for low vision/dyslexia (verified accessible)
3. **WCAG 2.1 Standards** — Web Content Accessibility Guidelines Level AA/AAA (compliance framework)
4. **Hidden Disabilities Sunflower Lanyard** — Real accessibility initiative (referenced in handoff project)
5. **Sensory Sensitivity Literature** — Hypersensitivity, photosensitivity, auditory triggers (referenced in CalmSkiesTravel)

### Scoring Criteria (Verified Against)
- **Hackathon Tech Scoring:** Agentic Automation (40%), Enterprise Connectivity (20%), Contextual Intelligence (20%), Modular Architecture (20%)
- **Hackathon UX Scoring:** User Centered Design (40%), Usability (20%), Design (20%), Innovation (20%)
- **Source:** state/SCORING-CRITERIA.md from handoff

### Open Questions (Pending Resolution)
- **A1:** Does a mocked integration score the same as real Data Fabric? (Answer awaited from hackathon organizers)
- **A2:** Is AWS/Microsoft category about sponsored models or personal account? (Answer awaited)
- **TrialClaudeHaiku Availability:** Pending Slack response (posted Nov 4, 2026)

---

## Documentation Lineage

```
Handoff Project (Nov 2-3, 2026)
    ↓
Clarifying Questions (Nov 4)
    ↓
Plan Review & Improvements (Nov 4)
    ↓
CalmSkiesTravel Reference Extract (Nov 4)
    ↓
PHASE-1-FINAL-LOCKED.md (Nov 4)
    ↓
Agent Prompts (Nov 4 - IN PROGRESS)
    ↓
Development Ready (Target: Nov 4 EOD)
```

---

## Accessibility & Inclusivity Commitment

All planning documents and implementation guidance:
- ✅ Grounded in autism-specific accessibility research (not generic WCAG compliance only)
- ✅ Authored with input from an autistic child's parent (A.J. Aronoff)
- ✅ Reference established interventions (Carol Gray's social stories, sensory kit integration)
- ✅ Explicitly exclude practices harmful to autistic users (bright colors, auto-play audio, animations)
- ✅ Prioritize neurodiversity-affirming language ("can do this" not "behavior problem")
- ✅ Support child agency & independence (fading strategy in Phase 2)

---

## Version Control & Attribution

**Repository:** https://github.com/aj-aronoff/Autism-Visual-Supports  
**Branch:** main  
**Commits:** All planning documents tracked with attribution lines per hackathon requirements

**Attribution Standard:**
```
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016LzkPfvgXeLZtNT6W7xWAo
```

---

## How to Use This Document

**For Team Members:**
- Reference this doc to understand where each design decision came from
- Check "Open Questions" section to see what's still pending
- Refer to "Autism-Specific Design" section for evidence basis

**For Code Review:**
- Use this to verify that decisions are evidence-based, not arbitrary
- Check accessibility claims against listed sources

**For Future Handoff:**
- This document serves as a "sources & citations" page
- Allows future readers to trace design decisions back to primary sources

---

## Questions or Additions?

If you need to add new sources or clarify origins:
1. Update this document
2. Add commit message: "docs: add/clarify information sources"
3. Reference the decision/doc this applies to

---

*Information Sources v1.0 | Created Nov 4, 2026*  
*Compiled by: Claude Code*  
*Owner: A.J. Aronoff*
