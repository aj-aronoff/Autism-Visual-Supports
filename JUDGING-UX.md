# UX judging — criterion by criterion, with where to look

**A map for a judge with limited time, and a self-audit we are willing to publish.**
Each row says what the criterion asks, what this project actually does, where to verify it, and
an honest status. **Where we fall short it says so.**

Criteria are quoted from the kickoff slide of 2 November 2026.

---

## 40% — User Centered Design

### *User Needs: does the design solve a real user problem effectively?* — **MET**

The problem is a real household's. A parent of an autistic child has four minutes to get shoes on
and get out of the door; *"we have to go now"* does not work and saying it louder works less. What
works is a picture: **first this, then the thing the child is working for.**

**The method is not ours, and that is the point.** First→Then boards are documented practice. The
Vanderbilt TRIAD toolkit shows how to build one; the National Standards Report lists the practices
they rest on. **Every board names the practice and the technique it used and cites the passage it
was grounded on.** A parent gets a board; a clinician gets a citation.

**The first test user is the person who lives it.** Three of the Reviewer's fifteen questions came
from one conversation with her, and ninety minutes later one of them fired on her own case — the
board had asked a child who cannot tie her shoes to tie her shoes. **Sixteen evaluation cases and
seventy-four test rows did not find that. One conversation with a parent did.**

**And it says no when it should.** Self-injury or escalation in a parent's text returns referral
guidance instead of a board, naming who to call. That check runs before anything else. **It cost
us a feature and we kept it.**

**Verify:** `evidence/11`, `evidence/26` · `prompts/reviewer.md` · `tools/guardrails.py`

### *Inclusivity: how well does it consider diverse user types?* — **PARTIAL, and this is our weakest point**

What is genuinely built:

- **The child who does not read.** The board is pictures first by design; the words are for the
  adult to say aloud. Every card carries a label **and** alt text as required fields, so a picture
  is never alone.
- **Three words at most on a card**, enforced by a validator against the schema's own pattern, not
  by asking the model nicely — that is what an early reader can take in at a glance.
- **Literal language only.** No idiom, no figures of speech, as a Composer rule and a Reviewer
  question.
- **No gender field exists.** A theme comes from what the child is interested in and **cannot** be
  keyed on their sex, because the data model has no such field. A schema guarantee, not a policy.
- **The printed sheet** is the accessible path for a household with one device, or none.
- **Two input modes for the picture**: the drawn card library, or a photograph of the child's own
  shoe and their own toy, taken on their own device.

**Where we fall short, stated plainly:** this project is deep on **one** user pair — an autistic
child and their parent — and thinner on everyone else. There is no formal accessibility audit, no
contrast report, and no screen-reader pass. **The design decisions above were made for inclusion;
they have not been tested against a standard.**

---

## 20% — Usability

### *Ease of Use* and *Efficiency* — **MET**

A parent types one paragraph in their own words. **One board takes about thirty seconds** — that
is measured, not estimated.

The next morning is **two taps**: the task is done, the reward arrived. There are two more buttons
and they matter as much — **one for *later* and one for *it did not happen*** — because a tool
that only records success tells a family nothing. A planned delay is a named technique; an
unplanned one is the method breaking down, and only the gap between them tells you which.

**The wording is part of the usability.** The button does not say *failed*. It says
**"the dinosaur did not happen"**. A parent recording a bad morning should not also be told off
by software.

**Verify:** `evidence/20`, `evidence/25` · the board page itself

---

## 20% — Design

### *Visual Appeal* and *Information Clarity* — **MET**

**201 cards built to one visual system**, generated rather than collected, so nothing clashes.
Information clarity is close to the definition of a First→Then board: **two pictures, one order,
one sentence to say.**

Two deliberate choices worth noticing: **the same child appears on both cards** — a clinical point
rather than a stylistic one — and a theme shows as a tint and a small corner motif, never as
decoration competing with the two cards.

**Verify:** `assets/ASSETS.md` · `assets/cards/`

---

## 20% — Innovation

### *Originality* and *Problem-Solving* — **MET**

Three things we have not seen elsewhere:

1. **A second agent that can only report.** The Reviewer has no tools and cannot edit anything.
   It asks fifteen questions a validator cannot answer — *can this child physically do this
   today; can the reward be delivered in sixty seconds in this home; can she reach it without
   doing the first task.* **A reviewer that can edit stops reporting.**
2. **Guardrails as code, not as prompt wording.** The safety rule and the grounding rule are steps
   in the flow. The model is never asked to be careful; it is prevented.
3. **Tracking promises kept, rather than boards made.** The outcome data is whether the reward
   actually arrived — which is the thing that decides whether a family keeps using it.

---

## The honest summary

**Strongest:** User Needs, and the grounding that stands behind it. Every claim on a board traces
to a named practice and a real passage.

**Weakest:** Inclusivity beyond the one user pair. The decisions are real; the testing is not.

**What we would not claim:** that anything pauses, that the app has been through an accessibility
audit, or that one Reviewer result is a rate. `evidence/README.md` carries a section on what the
directory does **not** prove, and it is the part we would read first.
