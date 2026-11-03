# Twilio is out — 2 November 2026

The organiser, answering the credentials question asked on 1 November:

> "We will not use twilio for this hackathon"

That is five words and it removes a whole subsystem. **It supersedes `rules.txt:36`**,
which still reads *"teams are expected to use Twilio services to be eligible for special
Twilio proce [sic]"*. The rules text was the **only** evidence that Twilio was required;
`AWS-ARCHITECTURE.md §1.5` had marked it *"Confirmed as required"* on the strength of that
one line, which was a fair reading at the time and is now wrong.

## What dies, and what does not

**Dies:** the SMS transport. Boundary **B3** (Twilio → our exposed endpoint) was the only
unauthenticated path into the system and the only place we had to write real security code
— HMAC-SHA1 over URL plus sorted body, constant-time compare, `MessageSid` idempotency.
**B6** (our code → Twilio outbound) goes with it. `CODE-PLAN.md §3.3` called the webhook
*"the highest-risk authorable piece"*, and with no prize behind it, that risk now buys
nothing: scoring criterion one rewards **named ODC features**, and Twilio was never one.

**Does not die:** the reward loop itself. The Vanderbilt TRIAD toolkit is blunt that an
unkept promise is worse than no board — *"otherwise, your child may not trust the board the
next time you use it"* — and that is a clinical point, not a feature choice. The usage log
and the promises-kept streak are ours and need no third party.

## Recommendation: cut it

Reclaim day 7 for the UX pass and the demo. A reclaimed day in a seven-day hackathon is
worth more than a feature nobody is scoring, and the cut *removes* two trust boundaries
from the Well-Architected pass rather than adding mitigations to them.

**What replaces it, honestly stated.** The old argument was that SMS reaches the parent at
the front door, when no one would open an app. Without SMS that argument is gone and must
not be re-used in a weaker form. The honest replacement: the script and the reward promise
are **on the board itself** — on screen and on the printed sheet — and the app asks exactly
one question the next time it is opened: *did the reward happen?* One tap, nothing else
asked, and the home screen counts promises kept rather than boards made. That is a smaller
claim and it is true.

## Three things still to do, in order

1. **`MID-SUBMISSION.md` is due 4 November and has a whole `§3.4 Twilio`.** It also has to
   be re-checked against whatever the kickoff says, because the submission format changed
   this year (`KICKOFF-NOV-2.md` item 2). Do both passes at once, after the call.
2. **The published Taikai description names Twilio twice** — once in the body and once in
   the tagline. Drafts below. This is public text about a service the hackathon has said it
   is not using, so it should not sit for long.
3. **`trust-boundaries.svg` draws the Twilio box.** It is generated — `assets/build_diagram.py`
   owns it, never hand-edit, and `build(slide=False)` must still reproduce the committed
   file byte for byte after any change (`CLAUDE.md §3`). Regenerate only once the cut is
   decided, and re-run both variants plus the 2x renders.

## Drafted replacement wording — not yet published

**Short description, the body sentence.** Replace:

> So Twilio texts you the script when the routine is due, and afterwards asks one question
> — did the reward happen? That single reply is the field the whole method rests on, and the
> one no parent would ever open an app to fill in, because at that moment they are at the
> front door holding a pair of shoes.

with:

> So the board carries the script and the promise with it, on screen and on the printed
> sheet, and the app asks exactly one question the next time you open it — did the reward
> happen? Nothing else is asked, because at the moment it matters you are at the front door
> holding a pair of shoes. The home screen tracks promises kept, not boards made.

**Tagline.** Replace `*OutSystems ODC · Agentic AI · Twilio · Build for the Future Hackathon 2026*`
with `*OutSystems ODC · Agentic AI · Build for the Future Hackathon 2026*`.

**Long description** (`project-description.md:90` and `:122`, and the diverged copy in
`Autism-Visual-Supports/docs/`): the §"Twilio carries the script" paragraph goes, and the
day-7 line in the roadmap sentence becomes *"the reward question and the trust streak"*.
The two copies differ already — reconcile them in the same pass.
