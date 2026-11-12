# Retrieval scores, before and after the evidence-query fix

Both runs: same message, `BoardId: 0`, `ChildId: 0`, `KBTopK` 3, `KBMinimumScore` 0.2,
model `CallBedrockHaiku5_5`, Development stage. Read from the `DebugShowPassages` block.

| | 17:09 | 17:49 |
|---|---|---|
| Layout — TRIAD | 0.32 **PASSED** · 0.289 **PASSED** · 0.289 **PASSED** | 0.311 **PASSED** · 0.264 **PASSED** · 0.26 **PASSED** |
| Evidence — NSP | 0.167 *REJECTED* · 0.149 *REJECTED* · 0.131 *REJECTED* | **0.737 PASSED** · **0.716 PASSED** · **0.706 PASSED** |
| Passages reaching the Composer | **3** | **6** |
| Practices in `evidenceBasis` | 3, **none grounded** | 2, **both grounded** |
| Citations | 1, naming an **invented** section | 4, **every one a real chunk** |

## What changed, and what did not

**Only the evidence query changed.** The layout query, every prompt text and the
template wrapper were untouched.

- **17:09 evidence query** — the parent's narrative:
  `"Evidence-based practice for a visual support for this situation: My 7 year old does not want to brush her teeth in the morning. She loves dinosaurs. Afterwards she likes to swing outside."`
- **17:49 evidence query** — fixed, practice vocabulary, independent of the parent's words:
  `"Established treatment definitions and techniques: Antecedent Package, Behavioral Package, Naturalistic Teaching Strategies, Schedules, Self-management, Story-based Intervention Package"`

## Why the first query could never work

The NSP extract is a **reference table of treatment names and study counts**. At 0.167 the
best-matching passage was **a column header from the report's summary table** — treatment names
and skill categories, nothing more. (Quoted verbatim in the private working copy; described here
because the source document is not ours to republish.) A parent's narrative will not
match that at any threshold, so **lowering `KBMinimumScore` to 0.12 would have bought three
weak table fragments and a citation meaning less than no citation.** The query was wrong, not
the threshold.

## At 0.5, nothing passes

That is the number the app shipped with at 16:23, and it is why the app appeared broken from
16:36 onward — never the wiring, never the child record, never the model.

## The threshold set from these numbers

Lowest passage worth keeping: **0.26**. So the shipping floor is **0.25** — not 0.5, which
passes nothing, and not 0.2, which was a diagnostic value chosen to get any board at all.
