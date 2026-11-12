# Evidence — Monday 9 November 2026

**What this is.** The first day anything in this project executed. Nine files recording what
actually ran, with the numbers, read off the running app and the ODC Portal rather than inferred.
The claims in both videos should be traceable to a file here or they should not be made.

**Why it is OUTSIDE the git repo, deliberately.** Files 03/04 and the passage excerpts quoted in
05 and 06 contain text from the **Vanderbilt TRIAD toolkit** and the **National Autism Center's
National Standards Report**. `CLAUDE.md` §2: that material is **never re-hosted**, and a file in a
public GitHub repository is re-hosting. `hackathon-future/` is not a git repo. **Do not move this
directory into `Autism-Visual-Supports/`.** Quoting a passage on screen in the Tech Video is a
different act from publishing the file, and is covered by the toolkit's own distribution
permission.

---

## The files

| | What it is | What it proves |
|---|---|---|
| `01-escalation-fired-1633.txt` | Guardrail 5 firing, request and response verbatim | `CheckEscalation` is genuinely first; **`Regex_Search` runs our pattern 3 at run time**; the short-circuit writes no board; it costs zero model tokens |
| `02-rule17-fired-in-code-1636.txt` | The flow refusing to compose, verbatim | **Rule 17 enforced in code, not prompt wording.** Includes Mentor's admission that it had been prompt-only, in its own words |
| `03-board-1709.json` | The first board ever produced | It validates — but its practices were **ungrounded** and its citation **invented a section name** |
| `04-board-1749.json` | The same request after two fixes | Fully grounded. **Four citations, zero fabrication** |
| `05-retrieval-scores.md` | Before/after score tables | **Evidence went 0.167 → 0.737.** The query was wrong, not the threshold |
| `06-retrieval-attributes.txt` | The eight attributes an ODC result carries | **`chunkPosition` is the part.** `pageNumber` is always 0. There is no `filename` |
| `07-portal-readings.md` | Publishes, model config, knowledge bases, all 15 Settings, validation, one ODC constraint | **The category is BOTH, and proven** — the app runs unchanged on Amazon Bedrock *or* Azure OpenAI, because its only live AI dependency is one model connection |
| `08-audit.py` | A re-runnable audit | `python3 evidence/08-audit.py` |
| `08-audit-output.txt` | Its output | `RESULT: ALL CHECKS PASS` |
| `09-board-1800-MALFORMED.md` | A board that does not parse, with the brace count | Why the parser must **refuse** before it extracts |
| `10-reviewer-first-verdict-2203.md` | **The Reviewer's first working verdict**, verbatim | Temperature 0.2 is rejected by Bedrock Haiku 5.5 — and the verdict **found a flaw in its own wiring**: `BuildReviewerMessages` never receives the parent's request, so three of the fifteen questions could not fire |
| `11-two-agent-design-justified-2215.md` | **`FIRST_NOT_POSSIBLE` as a `must`, and `THEN_ALREADY_AVAILABLE`** — both the first test user's questions firing on her own case, 90 minutes after she said the words | **The Composer drafted the obvious board; the Reviewer caught it.** The two-agent design justified in one run |
| `12-missing-obstacle-false-must-2218.md` | The same Reviewer producing a **`must` on a false premise** — *"the parent may need to buy"* when the parent said *"we have purchased"* | **`BuildReviewerMessages` never receives the parent's request.** Three of the fifteen questions are guessing, and this is the second time `THEN_NOT_DELIVERABLE` doubted something the parent had described |
| `13-q13-q14-both-directions-2220.md` | Boards 16, 17 and 18 as one arc — Q13 **fires** on an impossible task, is **silent** on an achievable one, and Q14 fires **three for three** | **A new check that stays quiet when it should is the hard half, and it did.** Plus the standing Composer gap: it never says where a reward is kept |
| `14-fifteen-cases-2340.md` | The fifteen-case run | **Question 14 CAN be satisfied** — the one unknown that mattered. Plus a **third category of reward** (a fixture cannot be put away), Q13 repeatable, both safety-gate halves proven, and **`SocialNarrative` confirmed unable to produce a board** |
| `15-two-providers-two-rejections-0005.md` | The same app rebound from **Bedrock to Azure OpenAI** in four edits | **The Composer is provider-portable; each provider rejects a DIFFERENT parameter** — Bedrock `temperature=0.2`, OpenAI `max_tokens` — and **neither is visible in ODC's UI.** A multi-provider agentic app cannot be configured without a runtime call |

**The table stops at `15`. Files `16` through `23` exist and are NOT indexed above** — add them when
there is time. The newest is the one to know about:

| | What it is | What it proves |
|---|---|---|
| `26-board-101-two-musts-2056.md` + `.png` | **Board 101: question 13 fires a second time, and question 14 fires beside it — both `must`** | **Q13 is repeatable at temperature 1**, which could not be assumed and had to be observed; Q14 caught a reward left within reach. The Composer made the same mistake again, so **the architecture is what catches it, not the prompt** |
| `25-board-on-the-real-ipad-1701.md` | **The imported board on the child's own iPad, with real photographs of her shoe and her toy** | The chain reaches the device with no mock-up in it; `Download with pictures` worked on its first browser run; the photographs never left the iPad. **And it says plainly that board 100 is NOT the Demo's board** |
| `24-first-imported-board-1445.md` | **Board 100: the first composed board rendered as a printable page** | The whole chain runs with no mock-up — zero invented practices, guardrails 1 and 8 holding, cost in tokens at **1,437,705 of 10,000,000**. **And two defects it found: the emitted line is NOT schema-valid** (cards lack `sequenceNo`/`altText`, `plan.childChoice` is `""`) |
| `23-refusal-carries-no-board-json-1443.md` | Guardrail 5 run with **`EmitBoardJson` = `True`** | **A referral carries no `BOARD-JSON:` line** — the one failure that mattered, measured rather than read. And the referral text is **byte-for-byte identical** to `tools/guardrails.py` `REFERRAL_TEXT`, 427 vs 427 |

**And the "What this directory does NOT prove" section below is STALE** — it was written early on
9 November and at least three of its bullets are now false of the app: the Reviewer has run, boards
do save, and `CheckEscalation` is not the only rule in code. Do not narrate from it without
checking `../CLAUDE.md` first.

---

## The three sentences this directory earns

**1. The safety guardrail is code and it fired.** Not "we wrote a rule about it" — `01` is the
request and the response. 21 substrings and 5 regexes, byte-identical between
`tools/guardrails.py` and ODC, compared programmatically.

**2. An ungrounded answer says so, in code.** `02` is the flow refusing to compose, returning
before the model was ever called. The project's own warning was that *"a board grounded in nothing
looks exactly like a board grounded in the toolkit"*; `02` is that case, handled.

**3. Every citation names a passage the model was actually given.** `08-audit-output.txt` checks
all four against the six retrieved and reports `zero fabrication: True` — and it cited **4 of 6**,
omitting the two it did not use. `Antecedent Package` is cited to the chunk that *is* the
Antecedent Package definition.

---

## What this directory does NOT prove — read this before writing narration

- **One escalation pattern was exercised**, not all 26. The repo's Python has 74 rows and 21
  tests; the ODC translation was string-compared, but only pattern 3 has been **run**.
- **The Reviewer has never run.** It is built, correct and unreachable — nothing in `AgentFlow`
  calls it, and it is one of the seven "never used" warnings. The 17:09 citation fault is exactly
  what it exists to catch, and nothing caught it.
- **Nothing saves a board.** No parsing, no `Board` row, no Approve action, no screen. The boards
  in `03` and `04` are JSON returned to a chat panel.
- **Nothing pauses.** A service action runs to the end. The Approve checkpoint is a design, not a
  build.
- **`LogTokenUsage` writes `0`** for both token counts, so the app cannot report what anything
  cost. The Bedrock Portal page is the only cost instrument.
- **Two timestamps are chat-panel times** for the agent's reply, not Portal times. The Portal
  times in `07` are the citable ones.

**Three claims currently in outward-facing text are false of what exists** — the ODC app
description, `for-judges.html` and `for-judges-2000.txt` all say *"the agent stops and waits… a
paused workflow"*, *"eight run as server actions"* and *"two taps the next morning."* **One runs.
Nothing pauses. There are no taps.** Fix before submitting.
