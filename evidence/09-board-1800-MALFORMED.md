# The third run — a board that does not parse. ~18:00, 9 November 2026

Same message, same inputs, `KBMinimumScore` now 0.25. **All six passages passed** (layout
0.315 / 0.271 / 0.268, evidence 0.737 / 0.716 / 0.706) and the citations are all real chunks.
The grounding is fine. **The envelope is not.**

The raw response is kept beside this file as `09-board-1800-MALFORMED.txt.raw`.

## Three defects, measured

```
braces   { = 15    } = 14    -> UNBALANCED BY ONE
brackets [ =  6    ] =  6    -> balanced
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 2 column 1 (char 2671)
```

**1. It does not parse.** One closing brace short. The root object is never closed.

**2. `evidenceBasis`, `citations` and `reasoning` are nested inside `plan`.** Adding the missing
brace makes it parse, and then:

```
top-level keys    cards, outcome, plan, script, sensorySupportOther,
                  sensorySupports, supportType, theme, title
MISSING REQUIRED  evidenceBasis, citations
plan keys         boardAction, citations, evidenceBasis, generalization,
                  ifChallengingBehavior, placement, promptHierarchy,
                  reasoning, reinforcement
```

**3. `sensorySupportOther: null`** against a schema `type` of `"string"`. `null` is not a string.

## The missing brace and the misnesting are ONE error, which is why this is not a paste artifact

The model opened `plan`, wrote its six fields, then carried on writing `evidenceBasis`,
`citations` and `reasoning` **still inside `plan`**, and emitted a single `}` at the very end.
It never closed `plan` before moving on. One mistake, two symptoms.

A copy-paste can drop a character. **A copy-paste cannot move three keys inside another
object.** So the nesting is from the token stream, and the missing brace is its consequence.

## Why this is the most important finding of the evening

**The app returned it to the chat without complaint, because nothing parses it.** A malformed
board is indistinguishable from a good one until something tries to read it — and today nothing
does.

Three runs of the same request produced three different shapes:

| | Grounding | Structure |
|---|---|---|
| 17:09 | practices **ungrounded**, citation **invented a section name** | valid |
| 17:49 | **fully grounded**, 4 citations, zero fabrication | valid |
| ~18:00 | **fully grounded**, 4 citations, zero fabrication | **does not parse** |

So the output is **not deterministic in shape**, and:

- **A live demo is a coin flip.** Record the Demo, do not perform it.
- **`x1` parsing is no longer "the next build step."** It is the only thing that makes the
  output trustworthy, and its first requirement is to **reject and write nothing**, not to
  extract fields.
- **The Reviewer cannot help here.** It receives the draft as text; a draft that does not parse
  never reaches a structure for it to review.
