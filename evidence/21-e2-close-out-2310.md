# e2 close-out: the gate screens the board's own text — 10 November 2026, 23:10

**The claim, stated the way it should be stated in both videos and in the paper:**

> **The escalation gate screens the board's stored goal and obstacle as well as the
> incoming message.** Verified two ways: a read-back of the flow order, and a production
> run in which a twelve-character message passed a twenty-character guard *because* the
> board's text had been appended to the string being checked.
> **The end-to-end case — a stored obstacle containing a trigger phrase — was not run**,
> because ODC has no table browser, and the only way to plant one would have been to add
> a publicly reachable action whose purpose is to write unscreened text into a board, on
> submission night.

---

## The gap this closes, and why it existed

`CheckEscalation` originally screened `UserInput` only. A request can carry text the gate
never sees: a returning parent re-running a saved board whose obstacle describes
self-injury passes the gate on an innocuous message.

**This was not hypothetical. It was observed.** On 10 November at 18:36 the sequence ran
in production: a self-injury message was correctly refused, then the message
`run it again` **composed and saved board 44.** Twelve characters passed the gate and a
complete board came out, so the content came from somewhere the gate had never looked.

## The three changes made

1. **Screen the resolved text.** `ScreenText` = `UserInput`, plus the board's `Goal` and
   `Obstacle` when a `BoardId` is supplied. `CheckEscalation` itself is untouched — the
   same 21 substrings, 5 regular expressions and referral text.
2. **Use the same string for the retrieval query**, so the gate and the query can never
   disagree about what is being handled.
3. **Refuse a message under 20 characters**, which closes the `run it again` path.

Flow order, read back from the canvas: `GetScreenBoard` → `BuildScreenText` →
`CheckEscalation` → `Escalation?` → `MessageTooShort?`.

## The two verifications

**Verification 1 — construction.** Mentor read back the order above and the binding:
`CheckEscalation` receives `ScreenText`, not `UserInput`. The escalation branch is
evaluated *before* the length branch, and both read the same variable.

**Verification 2 — behaviour, in production.** At 21:16, `BoardId: 68` with the message
`run it again` **composed and saved board 69** rather than returning the short-message
refusal. Twelve characters would have tripped the twenty-character guard. **The only way
it passed is that the board's goal and obstacle had already been appended.** The same
message with `BoardId: 0` returns the refusal, repeatedly — four times across the
evening — which is the control.

**So the variable demonstrably contains the board's stored text, and the gate
demonstrably reads that variable.** What was not demonstrated is the join between those
two facts firing on a real trigger.

## Why the last test was not run

**ODC has no table browser** — already recorded in `CLAUDE.md`, and the reason the demo
child is seeded by a timer and resolved by nickname rather than by id. Mentor can read and
edit the app's design but not the rows, and it **correctly refused to invent a "current
value"** for the obstacle, which would have risked restoring the wrong text afterwards.

The remaining route was a temporary action that reads and overwrites a board's obstacle
directly. **A server action is genuinely private, but then nothing can invoke it; the
moment it is made reachable it becomes a service action, and every service action in this
ODC version is public by nature.** That would have meant adding, hours before submission,
a publicly reachable action whose only purpose is to write unscreened text into a board —
**the exact hole e2 exists to close.**

**Judgement: not worth it for the last ten per cent of a proof.** The test is a good one
to run on Wednesday with daylight: a server action, invoked once, deleted immediately,
nothing published while it exists.

## What may and may not be said

**May be said:** the gate screens the saved board's own words, not only the message;
a twelve-character message no longer composes a board; and the refusal path costs nothing
and returns in 96 milliseconds (`evidence/19`).

**May not be said:** that a board carrying a triggering obstacle has been shown to be
refused end to end. It has not.

Source: test app transcripts 18:36–21:16, Mentor flow read-backs, 10 November 2026.
