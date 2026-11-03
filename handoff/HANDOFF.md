# HANDOFF — Autism Visual Supports, OutSystems hackathon

**Written 2 November 2026 for a Claude Code session taking over, including a cloud session.**
Read this file, then `instructions/project-CLAUDE.md`, then `DO-NOT-PUBLISH.md`. Nothing else
is required to start.

---

## 1. The one thing that decides the schedule

**FINAL SUBMISSION: Wednesday 11 November 2026, 2 PM GMT+1 = 08:00 EST in New York.**

08:00 New York is before the working day starts, so **everything ships the night of Tuesday
10 November**. That is the date to plan against. Converted with `TZ=America/New_York date`,
not estimated. It supersedes both `reference/rules.txt` (9 Nov, 11:59 PM CET) and the Taikai
timeline — the eleven-hour discrepancy is answered by both being wrong. The event was extended
two days to accommodate Diwali.

**THERE IS NO MID-WEEK SUBMISSION.** Confirmed at the kickoff. The 4 November deliverable this
project once planned for does not exist. Anything still showing a 4 Nov milestone is stale.

**TWO videos, not one:**

| Video | Limit | Audience | Purpose |
|---|---|---|---|
| **Demo** | **strictly 5 min** | Demo, UX and Innovation juries | The product working. Focus names "the nonprofit value" — handle as a *cause*, never a partnership |
| **Tech Video** | up to 10 min | Product Management | "technical implementation, key architectural decisions, and agent workflows" |

The Tech Video is **new work nothing in the plan accounts for**, and it is where the Tech
criteria get *shown* instead of claimed.

## 2. What is being built

First→Then visual support boards for autistic children — one "if you do this" card beside one
"then this happens" card. A.J.'s daughter is autistic; his wife is the first test user. Built
in **OutSystems Developer Cloud (ODC)**. MIT licence. Screen-by-screen spec is `SPEC.md` in
the repo.

## 3. The boundary that decides almost everything

**The submission is built in ODC. It is NOT built on AWS.** There is no `aws odc`. ODC is
provisioned and operated by OutSystems inside accounts we do not hold. Scoring criterion one is
*"application of the ODC features presented during the kick-off"* and the prizes are ODC
licences. An AWS-CLI build would be a different, non-qualifying project.

- **The AWS surface is one service:** Amazon Bedrock, reached from our code.
- **AWS Trusted Advisor cannot be run against the submission** — it is an account-level
  inspector and we hold no account in the ODC tenant.
- The personal AWS account is a **lab bench**, not the build, and every call on it bills A.J.'s
  own card.

## 4. Where the code is, and its exact state

```
github.com/aj-aronoff/Autism-Visual-Supports   PUBLIC
main = 3813f83   pushed 3 Nov 2026   working tree clean
```

Recent commits: `3813f83` removes the unlisted concept-video URL from the tracked tree (3 Nov) ·
`9382397` publishes this handoff snapshot (3 Nov) · then, all 2 Nov, `832d563` guardrails layer +
board contract + tests · `f78093e` kickoff and first-login answers, plus the generator path fix ·
`0578cbf` `2df2ed3` `eec5a24` the three that had been held back.

`3813f83` is the **published** tip, measured 3 Nov with `git ls-remote origin main`, not assumed.
An earlier copy of this section said `832d563`; that was two commits stale.

**A cloud session gets the repo by cloning it, and the repo is the authority on the build.**
This `handoff/` directory is the redacted snapshot committed alongside it — see §11 for what
was withheld. The unredacted set stays in the parent folder, which is not in git.

**The checkout a cloud session starts with has no `origin` and cannot push.** Measured 3 Nov:
`git remote -v` is empty and `git ls-remote origin` fails with *"'origin' does not appear to be
a git repository"*. So a cloud session can commit and have the work die with the container.
Attaching the repo (`add_repo`, push access) gives a second clone that does have `origin` and
clones fine — but **push can still be refused** at the GitHub-App layer, which is a separate
permission from attaching. Check it before doing work you intend to ship: if push is refused,
GitHub must be connected and the Claude GitHub App installed on the repository at
`https://claude.ai/connect-github`. **Confirm push works before relying on a cloud session for
anything that has to leave the container.**

**Verify before trusting (two commands):**

1. `python3 tools/test_guardrails.py` → expect `Ran 19 tests ... OK`. Use plain `python3`.
   **Not `python3 -I`**, which drops the script's own directory from `sys.path` and breaks
   `import guardrails`.
2. The board contract, against its own examples — `jsonschema` is present in the cloud
   container (4.26.0, measured 3 Nov), so this runs there: validate `schema/examples/*.json`
   with `Draft202012Validator` against `schema/board.schema.json`. Expect
   `first-then-shoes-swing.json` **valid** and all three `INVALID-*.json` **rejected**, each for
   the reason its name gives — the four-word label fails the label pattern, the invented
   practice fails the `evidenceBasis` enum, and the missing Then card fails the cards contract.
   Verified 3 Nov: 1 valid, 3 rejected, as designed.

## 5. Four generators own their output — never hand-edit, never hand-copy

| Generator | Owns |
|---|---|
| `assets/build_cards.py` | `assets/cards/*.svg` (201), `MANIFEST.csv`, `cards-contact.svg` |
| `assets/build_art.py` | the submission artwork (21 SVGs) |
| `assets/build_diagram.py` | `trust-boundaries*` — reference **and** deck variant |
| `tools/build-eval-page.py`, `tools/build-gems-page.py` | the two review HTML pages |

Every generator derives its output path from
`os.path.dirname(os.path.abspath(__file__))`. **`build_diagram.py` has a regression test:
`build(slide=False)` must reproduce the committed `trust-boundaries.svg` byte for byte** — diff
it after any change. The check that catches a recurrence of the old bug:
`grep -rn "hackathon-future/" --include="*.py"` inside the repo must return
`video/make_video.py` and nothing else (that one is a deliberate, annotated exception — the
concept video is kept out of the repo on purpose).

`assets/ASSETS.md` carries 19 numbered cautions. Read it before touching any image.

## 6. What a CLOUD session does and does not have

> **This section was written from prediction and was wrong in five places. Corrected 3 November
> from inside a cloud container (`anthropic_cloud`), by running the commands rather than
> guessing at them.** The pattern in the errors is one-directional: every wrong line
> *understated* what the cloud can do, and the work was handed back to A.J. unnecessarily. The
> rule from §14 applies to this file too — measure, and when the measurement contradicts the
> prediction, say so.

**Genuinely not available, and these are the ones that matter:**

- **No ODC Studio and no ODC Portal session.** Studio is a desktop application and the tenant
  needs an interactive login. **Any task that says "check in Studio" or "read the Portal" is
  A.J.'s, not the agent's.** This is the one real boundary, and it is the whole reason §12
  exists.
- **No Google Tasks.** It needs `../google-tasks/tasks.py` run with that directory's own
  `.venv/bin/python`, which lives outside the repo.
- **No `boto3`** — measured, absent. So no Bedrock call from a cloud session even if credentials
  existed, which they do not.
- **No push remote by default**, and attaching one may still not grant push. See §4.
- **The AWS lab account has nothing in it** — measured 2 Nov, not assumed: `aws configure list`
  returns `<not set>` for key, secret and region; `aws configure list-profiles` is empty;
  `~/.aws/` has no credentials file; no Bedrock model access; no budget;
  `tools/token-log.csv` holds only its header, so **no lab call has ever run**.
  `aws configure agent-toolkit` installs skills — **it does not sign you in**.
  **Do not stand any of it up** (§8, question A1/A2).

**Available after all — five lines this section previously got wrong:**

| Previously claimed | Measured 3 Nov in the container |
|---|---|
| "No Windows Chrome, so **SVG cannot be rasterized**" | **Chrome is present and rasterizing works.** `/usr/bin/google-chrome` (Chrome for Testing 153.0.8010.12), plus Playwright's Chromium at `/opt/pw-browsers/chromium`. Rendering the committed `assets/trust-boundaries.svg` headless produced a 1600×1200 RGBA PNG. The Windows path in `ASSETS.md` is A.J.'s machine, not a requirement |
| "No `soffice`, so the deck cannot be re-exported to PDF" | **`/usr/bin/soffice` and `/usr/bin/libreoffice` are both present.** The deck can be re-exported from the cloud |
| "`python-pptx` … not installed" | **Present, 1.0.2.** The deck's `.pptx` source can be read and edited from the cloud |
| "`jsonschema` … not installed" | **Present, 4.26.0.** The board contract validates in the cloud — see §4, verification 2 |
| "No Gmail, Notion or Docs MCP, so the organiser mail cannot be re-read" | **Gmail and Claude Docs MCP were both connected in this session.** The organiser mail *can* be re-read from the cloud when those connectors are attached. Do not assume; check what this session actually has, and do not hand this back to A.J. without looking |

**So the work that travels to the cloud is: documents, specs, schema, guardrails, Python, video
scripts, the two descriptions — and, contrary to the original version of this section, every
image regeneration and raster, the deck's PPTX and PDF, and anything needing the organiser
mail. The work that genuinely does not travel is ODC Studio, the ODC Portal, Google Tasks, and
anything that must reach Bedrock.**

## 7. Scoring — where the points are and where we are weak

Both categories are 40/20/20/20 *within themselves*, and **neither slide says what the
category is worth overall**, so a 20% gap in Tech is not 20% of the prize.

**Tech:** Agentic Automation & AI **40%** (Mentor is named inside it, so *using* Mentor is
evidence) · Enterprise Connectivity & Data Integration **20%** — **our zero** · Contextual
Intelligence & Grounding **20%** — our strongest, both Beta features entitled · Modular
Architecture / Governance / Security **20%**, naming Forge Acceleration and **Real-time
Observability**, which we have nothing for.

**UX:** User Centered Design **40%** — User Needs is our strongest ground anywhere, but its
other half, **Inclusivity, is close to unwritten** · Usability **20%** (note: *"under two
minutes" is a target, never a measurement*) · Design **20%** · Innovation **20%**.

**Innovation is scored twice** — a 20% UX sub-bucket *and* a jury of its own. One of its
criteria asks whether the entry is *"just a digital version of an existing paper/Excel form"*,
which is aimed squarely at a First→Then board. The answer is in
`state/RESOURCES-AND-CRITERIA-NOV-2.md` §3.1.

**The written criteria are more specific than the slides, and in four places they move the
design:** DataFabric means **AWS or Microsoft infrastructure**, not any external source ·
Logic Isolation means **ODC *Libraries*** specifically, which our Web/Agentic app split does
not satisfy on its own · Real-Time Observability names **token consumption and cost**, so
`TokenUsage` is scored rather than merely prudent · Human-in-the-Loop means a checkpoint that
**PAUSES agent execution**, not a review of finished output.

**Jury:** Paulo Garrudo (Tech), Menno Cramer (UX), Kris Lande (Demo), Jennifer Forman (Cisco,
Innovation). Special awards: AWS — Arun Nallathambi; Microsoft — Roberto Arocha.

## 8. The two open questions that gate this week

Both are in `state/QUESTIONS-consolidated.txt` as **GROUP A**, and A.J. posts them in the
hackathon Slack `#help` himself:

- **A1 — does a mocked integration score the same as a real Data Fabric connection?** The
  kickoff Q&A said Data Fabric is *"optional, with mock integrations also being acceptable"* —
  but that comes from a machine-generated Zoom summary which **misnames two jurors and a model
  in the same paragraph**, and *"accepted"* is not *"scores the same"*. **Treat it as a lead,
  not a fact.** If true it erases the 20% DataFabric gap; if false it is still our zero.
- **A2 — is the AWS/Microsoft category about the sponsored models or about our own account?**

**Until those are answered, do not create billable AWS resources and do not cancel AWS work.**
The reason to need it flipped twice in one day.

**Model configuration, which is settled:** two hackathon models, `BedrockHaiku5_5` (AWS) and
`Microsoft_OpenAI_GPT5_5_…` (Microsoft), at **10,000,000 tokens a day each**, per day and
refilling. One day on one model is 2.6× the whole build, so the token budget is no longer
load-bearing. **The GPT entry will be deprecated and replaced, so the model must be a Setting,
never a constant**, and anything load-bearing prefers the Bedrock Haiku entry.

## 9. Open build work, roughly in order

1. Write the **Inclusivity** section into `SPEC.md` and check contrast and touch targets — it
   is half of UX's heaviest bucket. **Not "close to unwritten" — absent.** Measured 3 Nov:
   `grep -niE "inclusiv|contrast|touch target|WCAG|accessib" SPEC.md` returns **nothing**, and
   the eight section headings run from "The finding that shapes the build" to "Build order" with
   no accessibility section among them. This is the largest single scoring gap in the repo and
   it is pure document work, so a cloud session can close it.
2. Move guardrails, the validator and the board contract into an **ODC Library** (Logic
   Isolation, 20% bucket).
3. Make the parent review a **Workflow checkpoint that pauses agent execution** (HITL).
4. Script the **Tech Video** — nothing in the plan accounts for it.
5. Read the **Agent Guardrails** and **Agent Evaluations** docs; we built both by hand and the
   platform has them.
6. **Update the published Taikai description** — it still names Twilio in the body *and* the
   tagline. Replacement wording is drafted in `state/TWILIO-WITHDRAWN-2-NOV.md`.
7. **`assets/trust-boundaries.svg` still draws the Twilio box.** Regenerate via
   `assets/build_diagram.py` once the cut is confirmed, then re-run the byte-for-byte
   regression and both 2x renders. The repo currently says Twilio is withdrawn in prose while
   the diagram still shows it.
8. **The deck's content is still 28 October** — it predates the guardrails, the board schema,
   the first ODC login and the Agentic confirmation. Current as a *file*, behind as a document.

## 10. Known stale, so you are not misled

- **`next-steps/next-steps.html` has the wrong calendar.** Its own headings still read "The
  kickoff is tomorrow", "Tonight, Sunday 1 November" and **"By Wednesday 4 November — the
  mid-submission"**. The items are useful; the dates are wrong. Stamped 1 Nov 17:14, before
  the kickoff.
- `next-steps/odc-studio-next-steps.html` holds up much better — it is Studio build order,
  which the kickoff did not change. Its "held until after the kickoff" section is now
  unblocked. Single stale references to 4 Nov and 9 Nov.
- `SPEC.md`'s day table and the Google Tasks list also predate the kickoff.

## 11. You are reading the REDACTED, PUBLIC copy

This directory is committed to the **public** repo on purpose, so a cloud session gets it by
cloning. That means six values were removed before it was published, each replaced by a
visible placeholder:

| Placeholder you will see | What it was |
|---|---|
| `<ODC-TENANT-HOSTNAME-WITHHELD>` | the ODC tenant hostname |
| `<UNLISTED-VIDEO-LINK-WITHHELD>` | the unlisted concept-video link |
| `<ZOOM-LINK-WITHHELD>` `<MEETING-ID-WITHHELD>` `<PASSCODE-WITHHELD>` | kickoff Zoom joining details and the recording share link |
| `<PARENT-DIR-WITHHELD>` `<PROJECT-ROOT>` `<HOME-WITHHELD>` | local filesystem paths |

**If you need one of those values, ask A.J. — do not reconstruct or guess it, and never write
one back into this repo.** Nine files were withheld entirely; `README.md` beside this file
lists them and says why.

The unredacted set lives outside git, in the parent directory, and is not published.

## 12. A.J.'s own actions — not the agent's

- Post **GROUP A** in Slack `#help`, A1 and A2 first.
- Recheck the Taikai project resources pages: does the category field accept **both** AWS and
  Microsoft, are there two video slots, is there any mention of AWS credits, and does the
  published description still name Twilio.
- **Select the AWS (or both) category on Taikai**, then **publish explicitly** — Taikai does
  not treat an edited project as submitted until it is republished.
- Verify in ODC Studio that an agent can bind `BedrockHaiku5_5`, and read the Data Fabric
  provider list in the Portal (a ten-minute look; A.J. is an Administrator).
- Run the Mentor meter experiment: read all four model figures in the Portal, run one prompt
  from `practice-camera-app/mentor-prompt.md`, read them again.

## 13. Support routing

**Slack `#help` is now the only route** — the organisers' own wrap-up email says so. The
earlier rule, that scoring and deadline questions were held for the kickoff call, **expired
with the call**. Then `makeadifference@outsystems.com`. Then a support ticket, which for a bug
or product friction must carry **"Hackathon" in the title** *and* be posted in `#help` as well,
not instead. Before posting, check the **eliminated** list in
`state/QUESTIONS-consolidated.txt` — about 20 questions are already answered.

## 14. How to report

`instructions/global-CLAUDE.md` asks for the iteration-loop format and it applies:
🧠 Thought Process & Iteration Loop, then 🚀 Final Solution, with a confidence score that must
reach 95%. Beyond the format: **measure rather than estimate, and when a measured number
contradicts a prediction, say so and find out why.** State what was left undone and why, in
the same breath as what was finished.

---
## 15. Inventory of this published copy

```
HANDOFF.md                                      18940 bytes
instructions/project-CLAUDE.md                  38839 bytes
next-steps/lab-1-agent-teardown.html            35127 bytes
next-steps/next-steps-tasks.txt                  3417 bytes
next-steps/next-steps.html                      32883 bytes
next-steps/odc-plan-review.html                 28968 bytes
next-steps/odc-studio-next-steps.html           33237 bytes
next-steps/odc-studio-next-steps.json            1056 bytes
reference/if-then-board-prompt.txt               2692 bytes
reference/project-link.txt                        637 bytes
reference/visual-support-prompt.txt              2392 bytes
state/QUESTIONS-consolidated.txt                27912 bytes
state/RESOURCES-AND-CRITERIA-NOV-2.md           17928 bytes
state/SCORING-CRITERIA.md                       23424 bytes
state/SOURCE-MATERIAL.md                        14927 bytes
state/TWILIO-WITHDRAWN-2-NOV.md                  4508 bytes
```
