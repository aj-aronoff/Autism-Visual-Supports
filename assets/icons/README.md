# Icons — Font Awesome Free, CC BY 4.0, recoloured

**Attribution, which the licence requires:**

> Icons: [Font Awesome Free](https://fontawesome.com) — licensed **CC BY 4.0**.
> **Changed from the originals:** each glyph has been recoloured to one of this
> project's three role colours. The shapes are unaltered.

That line belongs anywhere these are shown: the deck's last slide, a submission
page, a README. **Font Awesome Free's icons are CC BY 4.0, and CC BY requires both
the credit and a statement of changes** — the recolour is the change.

## What they are

Ten 256×256 RGBA PNGs, carried over from an earlier autism hackathon of A.J.'s.
They are **source assets, not generated output**: the recolouring script lives
outside this repo at `hackathon-future/deck-icons/recolour.py`, because its input
lives outside this repo too. Nothing in the build chain regenerates them, so a
change here is a deliberate one.

## Colour carries a role, not a mood

| Colour | Means | Icons |
|---|---|---|
| `#4f8a5b` child green | the child's side | `child` |
| `#3d6f99` parent blue | the parent's side | `parent`, `people` |
| `#1f4e52` structural teal | everything else | `repeat`, `code`, `scales`, `search`, `book`, `badge`, `heart` |

## Why these ten and not the other fourteen

**Ten of the twenty-four source glyphs were pure `#ffffff` at full opacity** — they
sat on dark chips in the deck they came from, and they render as nothing on a light
slide. Four of those ten are here, recoloured. The rest were left behind:

- **`phone`** — a phone beside a reward reads as a text message. **Twilio is out of
  this hackathon and no SMS is built**, and one icon is enough to re-introduce a
  claim that was swept out of this repo on 8 November.
- **`sunflower`** — the Hidden Disabilities Sunflower is a specific real-world
  scheme. Borrowing its symbol for an unrelated product misrepresents it.
- `plane`, `plane-departure`, `hotel`, `bag`, `truck`, `tag`, `id-card`, `couch` —
  travel-specific, and this is not a travel product.
