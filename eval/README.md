# Eval set

Eight cases. Two candidate boards each. One question per case: which board would you
actually put on a fridge, and why.

**Review page:** https://claude.ai/artifact/4VgPMnit8eknyXFdvtoS2o

## Why two tries and not one right answer

A single hand-written "correct" board makes a judge that rewards imitation. The second
candidate is not a decoy — in most of these cases both boards are defensible, and the
pick says which principle wins when two good principles disagree.

The comment matters more than the pick. The pick gives one gold answer for one case;
the reason behind it generalises into a rule, and rules are what the prompt is made of.

## What each case is for

| # | Case | The axis it tests |
|---|---|---|
| 1 | Out the door in four minutes | A reward the parent named, against one that fits the window |
| 2 | Teeth at bedtime | Motivation against sequencing |
| 3 | Leaving the playground | Whether the default support type is the wrong default here |
| 4 | Morning routine | Granularity — six steps complete against four steps finished |
| 5 | Dentist next Tuesday | Social narrative voice: first person against third |
| 6 | Asking for the tablet | A boundary against a contingency |
| 7 | Swimming cancelled | Predictability against agency, and a real gap in the spec |
| 8 | Head-banging in the supermarket | Whether a referral should also offer something |

Case 1 is the project's own story. Case 8 has no board in it at all — it tests the
safety gate, which is the path that matters most and gets exercised least.

## The spec gap case 7 exposes

`Card.Role` in [`../SPEC.md`](../SPEC.md) includes `Choice`, but section 2 defines no
choice-board support type, and `ParameterCards` is specified as Wait, Stop and Oops
only. Try B uses role `Choice` and is therefore not currently constructible. Preferring
B means the spec needs either a fifth support type or a widened `ParameterCards` — a
decision, not a bug fix, which is why it is in the eval set rather than in an issue.

## How the set gets used

1. A.J. picks and comments on the review page.
2. The picks become the reference answers in `cases.json`.
3. `tools/lab-measure.py` runs the Composer prompt against each case's profile and
   obstacle and records tokens, latency and whether the output parses.
4. A change to the Composer prompt is kept only if it does not regress a case that was
   already passing. Without this, "the prompt works" is a feeling.

The set is small on purpose. Eight cases that are argued over beat forty that are
skimmed, and on a metered token allowance a forty-case suite is a daily cost.

## Files

| File | What it is |
|---|---|
| `cases.json` | The set. Profiles, obstacles, and two candidate boards per case |
| `../docs/eval-review.html` | The generated review page |
| `../tools/build-eval-page.py` | Builds the page from `cases.json` |

## Two copies of the page, one builder

`tools/build-eval-page.py` writes both forms, so they cannot drift:

| File | For | How Save behaves |
|---|---|---|
| `docs/eval-review.html` | the published artifact | writes to the artifact database; I read it from here |
| `eval-review.html` | opening from disk | writes `eval-review.json` next to it |

The published page carries no `<!doctype>` or charset because the artifact runtime
supplies them. A file opened from disk gets no such wrapper, so the standalone copy
carries its own skeleton — without it the page renders in quirks mode and every em-dash
arrives as mojibake.

Saving from disk uses `showSaveFilePicker`, which exists in Chrome and Edge: it asks
once where the JSON goes, then every later save writes that same file silently. Other
browsers fall back to an ordinary download, which lands in Downloads and cannot be
aimed. Either way the state is also kept in that browser's local storage, so reopening
the file restores it, and **Load JSON** brings a saved file back on another machine.
