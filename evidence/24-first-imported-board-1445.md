# The first composed board becomes a printable page — 11 November 2026, 14:45

**Board 100. Composed in ODC, emitted as one line, pasted into `board-from-reply.py`, rendered as a
tappable page. The join the Demo could not previously show.**

`EmitBoardJson` = `True`, `KBMinimumScore` = `0.25`, `KBTopK` = `3` — all three read off the Portal,
not Studio.

---

## The request, verbatim — the parent's own words, unedited

```
My daughter does not tie laces. I want her to put on the sneakers with the velcro strips. We have
purchased a new dinosaur toy that she Loves. We keep it in her room, on a shelf that is too high for
her to reach, but that I can get in less than a minute
```

## What came back

```
Draft saved - the review found nothing to change.
Draft board saved: Shoes First, Then Dinosaur (board 100). It is a Draft and has not been approved.
REVIEW: pass
To continue this board, set BoardId to 100.
BOARD-JSON: {"supportType":"FirstThenBoard","title":"Shoes First, Then Dinosaur", ... }
```

## What the paste produced

```
wrote put-on-shoes-dinosaur-toy-7-year-old-daughter.html
  boardKey  Put-on-shoes-Dinosaur-toy-7-year-old-daughter
  history   ...-history.json, and a browser store of its own
  source    ...-source.json  (from the BOARD-JSON line)
```

**Four board pages now exist with four distinct `boardKey`s**, so no two boards' mornings can merge
into one history — the defect the two-key design exists to prevent.

---

## What it proves

1. **The whole chain runs.** Parent's prose → escalation gate → two knowledge-base searches →
   grounding check → Composer → parse → validate → save → Reviewer → `pass` → one emitted line →
   a page with real artwork and four working buttons. **No mock-up anywhere in it.**
2. **Zero invented practices.** `Antecedent Package` and `Behavioral Package` are both in the
   schema's **six citable** of the eleven National Standards Established Treatments. Three
   citations, all in the `<file>, chunk <n>` form that is **built in code, not by the model**.
3. **Guardrail 8 holds.** The prompt hierarchy is levels **1, 2, 3, 4** — contiguous from 1 — with
   every `kind` in the five-value enum. The schema cannot express contiguity; the rule does.
4. **Guardrail 1 holds on both labels.** `Put on shoes` is 3 tokens, `Dinosaur toy` is 2, checked by
   the generator against the schema's own pattern rather than trusted.
5. **The theme came from the child, not from the model's imagination.** `Dinosaur footprints`
   resolves through the page's lookup to the **Happy dinosaur at home** tint and motif, and both
   cards draw real artwork — `Put on shoes` matches the shoe art, `Dinosaur toy` the dinosaur art.
6. **Cost is finally in tokens.** `BedrockHaiku5_5` reads **1,437,705 of 10,000,000** — 14%, with
   86% of one day's allowance unspent, so the circuit breaker never had to fire.

## What it does NOT prove — and two of these are defects

- **The emitted line is NOT schema-valid, in two ways**, both found by checking it rather than
  reading it. The cards carry **no `sequenceNo` and no `altText`**, which `$defs/card` requires —
  and that is **my error, not the model's**: the field list in the Mentor prompt asked only for role
  and label. And **`plan.childChoice` is `""`** where the schema sets `minLength: 15`, because
  `BuildBoardJson` writes every plan key unconditionally, so an empty optional becomes an empty
  string instead of being omitted. `boardAction` and `generalization` carry the same latent risk.
  **Neither affects the page**: `make-board-page.py` never reads `altText`, and each SVG carries its
  own `aria-label`. The cost is that the `-source.json` is a lossy record.
  **So never say the `BOARD-JSON` line validates against `board.schema.json`.** It does not.
- **It is one board and one Reviewer verdict.** The Reviewer runs at **temperature 1**, forced —
  Bedrock Haiku 5.5 rejects 0.2 — so a single `pass` says nothing about repeatability.
- **The sensory branch is still unexercised.** `composer.md:309` makes `sensorySupports`
  *"usually omit"* and this request named no sensory tool, so the two fields never appeared.
- **This board's two cards are objects**, a pair of shoes and a toy dinosaur. Consistent register,
  which is right — but it is **not** the "same child on both cards" showcase, so do not narrate that
  claim over this board. Teeth → swing is where it lives.

## The sentence this earns

> A parent types what is actually hard about their morning. The agent retrieves from two
> evidence bases, composes a board, cites the practice it rests on, and a second agent reviews it
> before anything is approved. One line of JSON later it is a sheet of paper on the child's iPad
> with four buttons on it — and every number in that chain was measured, including the two places
> where the line is still wrong.
