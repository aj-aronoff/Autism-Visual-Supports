# Prompts

Two different things live in this folder.

## The agent prompts — written to be pasted into Agent Workbench

| File | Agent | Calls tools? |
|---|---|---|
| [`composer.md`](composer.md) | Composer — drafts the whole board as one JSON object | reads only |
| [`reviewer.md`](reviewer.md) | Reviewer — judges what a validator cannot | no |
| [`illustrator.md`](illustrator.md) | Illustrator — reuse before generate | yes |

Each file has a short header explaining the design decision, then the literal prompt
in a `text` fence. The fence contents are the prompt — paste them verbatim.

**The one idea that shapes all three:** anything countable is a server action, not a
model call. Word counts, card counts, banned words, required fields and exact-label
image lookups are `if` statements — deterministic, free, and incapable of drift. The
models are spent only on judgement: is this reward actually deliverable, does this
picture show this label, does this language respect this child.

That split is also the cost control. See [`../TOKEN-BUDGET.md`](../TOKEN-BUDGET.md).

## The originals

`visual-support-prompt.txt`, `if-then-board-prompt.txt` and `prompt-gem-style.txt` are
the three hand-written drafts the project started from. They are kept unchanged.
[`../SPEC.md`](../SPEC.md) §1 explains what each one contributed: the field list, the
system prompt and image rules, and the intake wizard respectively.

## The comparison set

[`gemini-gems.md`](gemini-gems.md) holds a meta-prompt for each agent, written to be
run in Gemini Gems so the prompt it writes can be compared against the one here. The
same set is published as a page with paste-and-save boxes — link in that file.
