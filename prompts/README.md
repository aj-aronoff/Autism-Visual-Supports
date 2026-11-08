# Prompts

Two different things live in this folder.

## The agent prompts — written to be pasted into Agent Workbench

| File | Agent | Calls tools? |
|---|---|---|
| [`composer.md`](composer.md) | Composer — drafts the whole board as one JSON object | reads only |
| [`reviewer.md`](reviewer.md) | Reviewer — judges what a validator cannot | no |
| [`illustrator.md`](illustrator.md) | Illustrator — reuse before generate | yes |

**Two further prompts in this folder are NOT the shipping architecture.**
[`AGENT-1-IF-THEN-ARCHITECT.md`](AGENT-1-IF-THEN-ARCHITECT.md) and
[`AGENT-2-SAFETY-STORY-COCREATOR.md`](AGENT-2-SAFETY-STORY-COCREATOR.md) came from a
parallel session on 4 November and describe a different pair of agents. **A.J. decided on
7 November to ship Composer + Reviewer and port three ideas out of those two files rather
than switch** — the Sensory Safety Kit, literal-language-only, and giving the child a real
choice. Each file now opens with a banner saying so and naming where its ideas went. Do
not wire either to an agent for this hackathon. The reasoning and the measurements are in
`../../kb-with-new-agents.html`, in the parent directory.

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
