# Reference Materials from CalmSkiesTravel
## For Autism Visual Supports Hackathon Project

**Source:** https://github.com/aj-aronoff/CalmSkiesTravel  
**Used For:** Style guide, design patterns, accessibility standards, icon reference, sensory kit guidance  
**Status:** Reference only — not reusing code, reusing design decisions & principles

---

## 1. Color Palette (Autism-Friendly)

✅ **Use these colors for the hackathon app:**

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **Primary Background** | Cloud White | `#F7FBFF` | Page backgrounds, boards, stories |
| **Primary Brand** | Calm Sky Blue | `#5BA4CF` | Headlines, buttons, tab active states |
| **Deep Brand** | Clear Sky | `#2E7CB8` | Strong CTAs, selected items |
| **Soft Accent** | Horizon Blue | `#A8D4EF` | Subtle highlights, borders |
| **Success/Calm** | Meadow Green | `#6BBF8E` | Checkmarks, "ready" states, board icons |
| **Child Section** | Soft Sage | `#B2DFC4` | Child-facing content backgrounds |
| **Parent Section** | Warm Sand | `#F5EFE0` | Parent-facing content backgrounds |
| **Text Primary** | Deep Slate | `#2D3748` | All body text |
| **Text Muted** | Cool Gray | `#718096` | Captions, secondary labels |
| **Alert/Warning** | Soft Amber | `#F4A261` | "When It Gets Hard" section, gentle warnings |

### Color Accessibility Guardrails
- ✅ Deep Slate on Cloud White = 7:1 contrast (WCAG AAA)
- ✅ White text on Calm Sky Blue = 4.5:1 (WCAG AA)
- ❌ **Do NOT use:** Bright red `#FF0000`, neon colors, pure black `#000000`
- **Rule:** Never use color alone to convey meaning — always pair with icon or label

---

## 2. Accessibility Standards (Autism-Specific)

### A. Visual Design
- **No bright colors** on child-facing content (reduces overstimulation)
- **Soft, muted palette** throughout (prevents photosensitivity triggers)
- **No animations or transitions** (unexpected movement is a trigger)
- **No auto-playing audio** (sudden sound is severe sensory trigger)
- **Consistent layout on every page** (autistic children depend on predictability)
- **Line height 1.75** (generous spacing reduces visual crowding)

### B. Language & Text (Child-Facing)
- **First-person language** ("I will…", "I can…") — evidence-based social story format
- **Concrete, plain sentences** — avoid idioms, metaphors, abstract language
- **Short sentences** — reduces cognitive load
- **Warm, positive framing** ("What helps me feel better" vs. "meltdown plan")
- **Child's name in every story** — increases engagement and ownership
- **"I can do this."** — recurring affirmation for self-efficacy

### C. Language & Text (Parent-Facing)
- **Scannable with bullets and checklists**
- **Warm but practical tone** — not clinical
- **Respect parent expertise** about their own child

### D. Structure & Navigation
- **Consistent two-card layout** on every page (reduces cognitive load)
- **Tab navigation** stays visible (child always knows where they are)
- **URL hash navigation** (deep-link support, allows rehearsal/re-reading)
- **Keyboard-navigable** (arrow keys work in tab list, no traps)
- **No hover-only content** (mobile and accessibility friendly)

### E. Font Choice
**Use: Atkinson Hyperlegible** (free, designed for low vision and dyslexia)
- High character distinction (`1` vs `l` vs `I` visually distinct)
- Wide letter spacing (reduces visual crowding)
- Open counters (letters like `a`, `e`, `c` more readable)
- No thin strokes (consistent, reduces blur)

---

## 3. Design Pattern: Two Voices

**From CalmSkiesTravel's tab-based architecture:**

```
┌─────────────────────────────────────┐
│ SITE HEADER                         │
├─────────────────────────────────────┤
│ TAB LIST:                           │
│ [Child] [Parent] [Other Tabs...]    │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ PANEL 1: Child-Facing Content   │ │
│ │ - First person ("I will…")      │ │
│ │ - Icons + simple language       │ │
│ │ - Soft Sage background          │ │
│ └─────────────────────────────────┘ │
│                                     │
│ OR (via tab switch)                 │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ PANEL 2: Parent-Facing Content  │ │
│ │ - Checklists + practical tips   │ │
│ │ - Warm Sand background          │ │
│ │ - Concise, scannable            │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

**Hackathon Application:**
- **Child vs. Parent story tabs** (already planned, matches this pattern)
- **Separate board/story display** for each audience
- **Color distinction:** Soft Sage (child) vs. Warm Sand (parent)
- **Tab icons:** Help with quick visual orientation

---

## 4. Icon Reference Strategy

**From CalmSkiesTravel's icon folder:**

### Journey Icons (5 main stages)
- `journey-home.png` — Starting home
- `journey-airport.png` — Arriving at airport
- `journey-plane.png` — On the plane
- `journey-destination.png` — At destination
- `journey-goinghome.png` — Returning home

### Character Icons
- `child.png` — Child figure (first-person perspective)
- `parent.png` — Parent figure (caregiver perspective)
- `parent-figure.png` — Simplified parent

### Travel Icons
- `plane.png`, `plane-takeoff.png` — Plane-related

### Hackathon Adaptation
**For Autism Visual Supports (non-travel scenarios):**
- Similar icon-per-stage approach for: Doctor Visit, Grocery Store, School, etc.
- **Character consistency:** Use same child/parent figures across all boards
- **Scenario icons:** Quick visual ID (hospital, store shelf, classroom, etc.)
- **Sensory kit icons:** Headphones, fidget, snack, blanket, lanyard

---

## 5. Go Bag Pattern (Sensory Kit Integration)

**From CalmSkiesTravel's "Pack the Calm" section:**

### Physical Items Checklist
**Child & Parent Both See:**
- ☐ Noise-canceling headphones
- ☐ Preloaded music / favorite playlist
- ☐ Fidget toys / sensory items
- ☐ Chewelry
- ☐ Favorite snacks
- ☐ Comfort item (blanket, stuffed animal)
- ☐ Sunflower lanyard (Hidden Disabilities signal)
- ☐ Water in reusable bottle

### Integration into Hackathon App
**When generating If-Then boards:**
- Agent references child's available sensory kit items
- Boards suggest: "FIRST [wait in line] → THEN [headphones + fidget]"
- Print includes checklist: "Pack before we go"

**When generating safety stories:**
- Frame kit items as "superpowers" (Agent 2 already does this)
- List them as options in checkpoints: "What sensory tool would help?"

---

## 6. Social Story Format (Evidence-Based)

**From CalmSkiesTravel's Story Builder implementation:**

### Carol Gray's Social Story Framework
1. **Descriptive section:** What actually happens in this situation
2. **Perspective section:** How it feels (validation: "It's okay to feel scared")
3. **Directive section:** What I can do (first-person affirmations)
4. **Control section:** Coping strategies specific to this child

### Implementation in Hackathon
- **Story Builder already follows this** in Agent 2 prompts
- Stories are: personalized, first-person, positive, concrete
- Include: sensory kit suggestions, affirmations, interactive checkpoints

---

## 7. Accessibility Checklist for Phase 1

### Must-Have (Before Ship Nov 10)
- ✅ Color palette: Use Calm Skies colors
- ✅ Font: Atkinson Hyperlegible (or similar high-legibility font)
- ✅ Line height: 1.75 minimum
- ✅ Contrast: 7:1 for body text (test with WAVE or Lighthouse)
- ✅ No flashing or auto-play audio (hard rule)
- ✅ Consistent layout (same pattern on every page)
- ✅ Keyboard navigation works (arrow keys in tab list)
- ✅ Child-facing language: First-person, concrete, warm
- ✅ Icons + labels (never color alone)

### Nice-to-Have (Post-Hackathon)
- ☐ High-contrast mode toggle
- ☐ Font size slider (user-facing)
- ☐ Read-aloud option (browser SpeechSynthesis API, no auto-play)
- ☐ AAC export (Boardmaker-compatible format)
- ☐ Symbol-based reading mode (visual symbols with every word)

---

## 8. Print-Friendly Design

**From CalmSkiesTravel's approach:**

### Board Printing Requirements
- Print background: **Cloud White** (`#F7FBFF`) or `#FFFFFF`
- Icons: **2-inch minimum** for quick visual recognition
- Text: **No fine print** — large enough for stressed reading
- High contrast: Ensure black/dark text on white background
- **Laminate-friendly:** Matte finish when printed, durable for repeated use

### Parent Checklist Print
- List format (bullets or checkboxes)
- Simple, scannable
- Suitable for airport/waiting room conditions (low light, distracting)

---

## 9. Sensory Safety "Do Not Use" List

❌ **Absolutely avoid:**
- Bright red `#FF0000`
- Neon / fluorescent colors
- Pure black `#000000`
- Flashing or blinking
- Auto-playing audio/video
- Animations or transitions
- Hover-only content
- Tiny fonts (< 12px body)
- Pure white backgrounds (use `#F7FBFF` instead)
- Figurative language, idioms, sarcasm in child-facing content

---

## 10. Success Criteria: Autism-Accessibility Test

**Before shipping, ask:**

1. **Sensory Safety:**
   - ✓ Could a photosensitive child read this safely?
   - ✓ Is there any unexpected sound or movement?
   - ✓ Are all instructions concrete and literal?

2. **Predictability:**
   - ✓ Does the layout stay consistent across pages?
   - ✓ Can the child predict where to find things?
   - ✓ Is the tab structure clear and stable?

3. **Language:**
   - ✓ Is child-facing text in first person?
   - ✓ Are sentences short and concrete?
   - ✓ Is the tone warm, not clinical?
   - ✓ Is there positive affirmation?

4. **Accessibility:**
   - ✓ Can I navigate with keyboard alone?
   - ✓ Are all colors paired with icons/labels?
   - ✓ Is contrast ratio ≥ 4.5:1?
   - ✓ Can I resize text and still read?

5. **Printability:**
   - ✓ Does it print with good contrast?
   - ✓ Are icons large enough (2 inches)?
   - ✓ Is it suitable for laminating?

---

## 11. Team Feedback & Iteration (From CalmSkiesTravel)

**Key insight:** A.J. Aronoff has **real-world parent experience** and autism expertise. Use that.

- Review design decisions with **parent + child** if possible
- Test with **autistic children** before shipping (even informal testing)
- Iterate based on **actual sensory feedback**, not assumptions
- Document **why** each design choice was made (rationale > compliance checklist)

---

## 12. References from CalmSkiesTravel Worth Reading

1. **ACCESSIBILITY_REPORT.md** — Detailed autism-specific guidance (all principles above sourced from this)
2. **CalmSkiesColorPalette.md** — Full color decision log (5 open questions for future refinement)
3. **RESPONSIBLE_ENGINEERING.md** — Child safety principles in engineering decisions
4. **index.html** — Real HTML example of two-voice tab pattern with semantic markup

---

## How to Use This Reference

**For Phase 1 Hackathon Dev:**

1. **Colors:** Copy the color palette into ODC design system
2. **Font:** Set `font-family` to Atkinson Hyperlegible
3. **Accessibility:** Use the "Must-Have" checklist before shipping
4. **Language:** Use dual-agent prompts (already written, sourced from similar patterns)
5. **Icons:** Adapt journey stages to non-travel scenarios (doctor, school, etc.)
6. **Testing:** Ask user (A.J.) or a parent/child to review before Nov 10

---

## Attribution

All reference materials extracted from **CalmSkiesTravel** (https://github.com/aj-aronoff/CalmSkiesTravel)  
Design and accessibility principles documented by **IBM Bob** in that project  
Adapted for **Autism Visual Supports Hackathon** by Claude Code

---

*Reference Guide v1.0 | Nov 4, 2026*
