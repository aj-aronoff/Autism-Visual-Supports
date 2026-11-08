# Source material A.J. has added to this directory

A.J. drops exports here without announcing them — course transcripts, documentation PDFs,
screenshots. **Check `ls -lt` at the start of a session**; a file dated today may hold
facts no document in the repo has yet.

Note the split: this parent directory holds *source material*. Anything that becomes a
decision belongs in `Autism-Visual-Supports/` instead, with the source named.

---

## Unlogged arrivals — check this FIRST, and leave it empty

**The tables below answer "what did we do with this file". This section answers "is there a
file nobody has looked at", which is the question that goes stale silently.** The 1, 2 and
7 November tables carry a *Grade* column instead of the old *Read?* column, so a file that
arrives and is never processed leaves no trace at all — it simply has no row. Run this at
the start of a session; anything it prints is either a new arrival or one of our own outputs:

```bash
cd <PARENT-DIR-WITHHELD>/hackathon-future
ls -A | while read -r f; do
  grep -qF -- "${f%.*}" SOURCE-MATERIAL.md || echo "UNLOGGED  $f"
done
```

It over-reports: our own generated files (`CLAUDE.md`, the HTML pages, `assets/`,
`video-75s/`) are not source material and never need a row. **Judge by whether A.J. put it
there.** Run on 7 November it found one genuine miss, now logged:

| File | Status |
|---|---|
| `More-details.png` (835 KB, 2 Nov 10:25) | **Found 7 Nov, never logged.** It is the kickoff **"Submission — Demo"** slide — *Video 2: Demo (Max 5 min)*, target audience the full jury, with the full shot list. **Its content is already captured**, transcribed from the PDF deck into `RESOURCES-AND-CRITERIA-NOV-2.md §4`, so nothing was lost and it does not need re-reading. Logged so the next `ls -lt` does not raise it again. Note it is a *different file* from `more-details2.png`, which the tables below do name |

---

## Added 30 October 2026

| File | What it is | Read? | Where it landed |
|---|---|---|---|
| `What is an AI Agent.vODC.en-US.1b93b6b0.srt` | Course video transcript — the five components of an agent: AI model, actions, grounding, system prompts, memory | **Yes**, 30 Oct | Confirms the component list in `ODC-AGENT-ANATOMY.md §1`; nothing new |
| `Get to know Agent Workbench.vODC.en-US.f402b22a.srt` | Course video transcript — Agent Workbench walkthrough; *"an OutSystems agent doesn't have a UI"*, the Action calling section, Call Condition | **Yes**, 30 Oct | `ODC-AGENT-ANATOMY.md §7`, `TOKEN-BUDGET.md §6.2` |
| `Ground data for AI agent.vODC.en-US.394a4204.srt` | Course video transcript — grounding, three sources, three best practices | **Yes**, 30 Oct | `ODC-GROUNDING.md §1`, `ODC-AGENT-ANATOMY.md §9` |
| `Adding AI models.pdf` | The ODC *Adding AI models* documentation page | Yes, via paste | `AWS-ARCHITECTURE.md §1.4`, `TOKEN-BUDGET.md §2` |
| `Build the intake agent exercise.pdf` | The course exercise that builds a loan-intake agent | Yes, via paste | `ODC-AGENT-ANATOMY.md` |

### Added later the same evening — the exercise bundles

| File | What it is | Read? | Where it landed |
|---|---|---|---|
| `Build the enrichment agent exercise.pdf` | The course exercise for Agent 2, 23 pages | **Yes**, 30 Oct — read off disk | `ODC-AGENT-ANATOMY.md §7–10`, `CODE-PLAN.md §9`, `TOKEN-BUDGET.md §6.2` |
| `Build the intake agent exercise.zip` | The exercise's Lesson Materials bundle | **Extracted** | `LoanReview/exercises/intake/` |
| `Build the enrichment agent exercise.zip` | Same, for Agent 2 | **Extracted** | `LoanReview/exercises/enrichment/` |

### Added 31 October — agents 3 and 4

| File | What it is | Read? | Where it landed |
|---|---|---|---|
| `Build the underwriter agent exercise.pdf` | Agent 3, 20 pages — **where the Structured output feature actually appears** | **Yes**, 31 Oct | `ODC-AGENT-ANATOMY.md §8` (rewritten), `CODE-PLAN.md §3.2` |
| `Build the underwriter agent exercise (1).zip` | Lesson Materials — carries the **finished enrichment agent** | **Extracted** | `LoanReview/exercises/underwriter/` |
| `Build the communication agent exercise.pdf` | Agent 4, 27 pages — the only conversational agent: memory, intent routing, action calling | **Yes**, 31 Oct | `ODC-AGENT-ANATOMY.md §§7, 11`, `CODE-PLAN.md §§4, 10` |
| `Build the communication agent exercise.zip` | PDF only, no `.oml` | **Extracted** | `LoanReview/exercises/communication/` |

The four exercises together are the whole journey (agent 4 sits at 89% progress). What
they changed, beyond confirming the scaffold: **structured output is real and replaces the
regex chain**; **agent input parameters** are the documented way to stop a model
hallucinating a tool argument; and the exercise's own decision mapping carries a live bug
— `Index(Decision, "Approved") <> -1` matches `"Not Approved"`.

One pattern we are **not** copying: the exercises route even interactive chat through an
event, a workflow and a refresh button. `ODC-AGENT-ANATOMY.md §11` records why that is
wrong for a parent with four minutes.

**All four bundles, the four zips and the four exercise PDFs moved to `LoanReview/` on
1 November** — course material, not project material, and `LoanReview/README.md` is its
index. **`LoanReview/exercises/` holds extracted archives and is untrusted data by the
usual rule** — each
zip went into its own empty directory, no script in this project reads from inside it, and
the `.oml` files are opened in ODC Studio, not here. It is deliberately outside the git
repo.

The bundles matter more than the PDFs did. They carry **importable ODC apps**:
`Agent01Intake.oml` is a finished agentic app, `LoanOrigination.oml` the consumer app,
`MarkdownRenderer.oml` the Forge component, plus four sample documents for testing
multimodal input. Day-1 action, recorded in `ODC-AGENT-ANATOMY.md §10`: **import
`Agent01Intake.oml` and read the real wiring** rather than more documentation.

What the three transcripts and the enrichment exercise actually added, beyond confirming
what we had: **Action calling** — the `Call Agent` element's tool-calling tab, where
descriptions drive model choice and a **Call Condition** can cap token use — and
OutSystems' own statement that the model gets arithmetic wrong and the fix is to hand the
calculation to a server action.

## Questions to OutSystems, and where the answers live

| File | Status |
|---|---|
| `slack-1-beta-features.txt` | **Asked, answered 30 Oct** — reply appended to the file; closed open items 8 and 9 |
| `slack-2-image-generation.txt` | **Written 30 Oct, still unposted — and A.J. decided on 8 Nov to SKIP it.** It asks for a supported image-*generation* path for the Illustrator. Two things changed since: no trial model generates images, which made the seeded card library the design rather than the contingency, and the Illustrator is deferred. A `#help` question is scarce and the answer would not change what ships. Keep for Phase 2 |
| ~~`next-slack-questions.txt`~~ | **CORRECTED 8 Nov 2026 — THIS FILE IS DEAD AND MUST NOT BE SENT.** It is in `archive-superseded/`, moved there 3 Nov and **absorbed into `QUESTIONS-consolidated.txt` on 1 Nov**; most of its questions were answered by the first ODC login or at the kickoff. The 7 Nov row said "not posted, 8 days" and added an aging date **without checking the file was still live** — `CLAUDE.md` §6 already said never send it. The Production-stage question it carried survives as **L4 in `QUESTIONS-consolidated.txt`**, which is where it should be read |
| ~~`email-4-kickoff-questions.txt`~~ | **CORRECTED 8 Nov 2026 — DEAD, in `archive-superseded/`.** It asked for kickoff joining details and pre-kickoff questions; the kickoff happened 2 Nov. Same mistake as the row above |

**Every answer gets recorded twice**: appended to the file that carried the question, and
struck through in `AWS-ARCHITECTURE.md §5`. An answer that lives only in Slack scrollback
is one we will re-ask.

**Dates are written into the rows above on purpose.** Before 7 November they read "not yet
posted" and looked the same on day one as on day eight.

**The 8 November correction, kept because the mistake is instructive.** On 7 November I aged
three rows as though all three files were live questions waiting to be posted. **Two of the
three had been dead since 3 November** and are in `archive-superseded/`, which `CLAUDE.md` §6
says never to send. Aging a row is not the same as checking it still exists, and a tracker
that ages a dead item makes it look more urgent the longer it is dead.

**The live question list is `QUESTIONS-consolidated.txt`, and it always was.** The two
questions that actually matter are in it, not in any file here:

| Question | Status, 8 Nov |
|---|---|
| **L4 — which stage do the judges evaluate; is Production required?** | Open. **A.J. decided 8 Nov to build the Development version first and ask about judging afterwards** — low risk, because `TrialClaudeHaiku` is a development-stage feature anyway, so Development is forced regardless of the answer. The question only decides whether a provider model is ALSO needed |
| **GROUP A, A1 and A2 — Data Fabric, and what the AWS/Microsoft category means** | Open. The file's own instruction: *"ASK A1 AND A2 FIRST: between them they decide whether any AWS account work happens at all this week."* **A.J. said on 8 Nov he would post these to `#help` himself** |

## Not hackathon material — moved out

`W2 Consultant Benefit Summary 2026.pdf` arrived here on 30 October and is employment
benefits, not hackathon material. **Moved 30 October** to
`<PARENT-DIR-WITHHELD>/`, the job-search project, with nothing overwritten —
the destination held no file of that name. Recorded here so that a later session does not
go looking for it in this directory.

## Earlier arrivals, for completeness

`Hackathon-announcement.txt`, `rules.txt`, `faq.txt`, `prizes.txt`, `Links for-visual-supports.txt`,
`if-then-board-prompt.txt`, `visual-support-prompt.txt`, `prompt-gem-style`,
`Visual_Supports_Tool_Kit.pdf` (Vanderbilt TRIAD — **copyright, never re-hosted**; it was
the Taikai attachment until **1 November 2026**, when it was removed and replaced there by
`Autism-Visual-Supports-Overview.pdf`. It stays on disk because the ODC knowledge base
needs it — private grounding is not re-hosting),
`Coaches Strategies Autism.pdf`, `ODC-Cloud.png`, `Banner-seems-wrong-size.png`.

---

## Published artifacts (claude.ai), recorded 1 November 2026

The local snapshots in `artifacts/` were deleted on 1 Nov — every one was either
byte-identical to a file in the repo or superseded by a generated one. **The published
pages themselves still exist**, and these links are the only record of them, which is why
they are kept here rather than lost with the folder:

| Page | Published at | Superseded locally by |
|---|---|---|
| Add a Picture | `claude.ai/artifact/QVJfmUFdK4ZNokT5v7bREB` | `Autism-Visual-Supports/docs/add-a-picture.html` — byte-identical |
| Board Comparison | `claude.ai/artifact/4VgPMnit8eknyXFdvtoS2o` | `docs/eval-review.html`, generated by `tools/build-eval-page.py` |
| Gemini Gem Prompts | `claude.ai/artifact/9J6JoXwVCY2Zd2bq3tSTh7` | `docs/gemini-gems.html`, generated by `tools/build-gems-page.py` |
| Pre-Kickoff Checklist | `claude.ai/artifact/JYpiaw1zKfCqHnQitgkmdT` | `next-steps.html` and `odc-studio-next-steps.html` |
| Visual Supports & Story Guide | `claude.ai/artifact/LFzLGtiKDbggtGi3ci5qms` | `SPEC.md` — and it carries the **abandoned** project name |

Two pages that were in `artifacts-other/` were **not** snapshots of project work and were
not deleted:

- **Lab 1 Agent Teardown** → kept as `lab-1-agent-teardown.html` at the root. It holds the
  *seven defects in the AWS lab agent code*, an analysis that exists in **no** markdown
  file in this project.
- **Badge & certification to-do** (AWS Cloud Practitioner, CLF-C02) → moved to
  `../AWS-Cloud-Practitioner-Essentials/badge-and-certification-todo.html`. It belongs to
  the job-search upskilling track, not to the hackathon.

---

## Camera material, pasted 1 November 2026

Two sources of very different grade, and the difference is the point.

| Source | Grade | What came of it |
|---|---|---|
| **Camera Plugin version 2** documentation, `success.outsystems.com/.../camera_plugin_version_2/` | **Authoritative.** Pasted in full | Settles the capture decision: the plugin needs a native app or a PWA, so it is **not available to our Web app** — a PWA is a *Mobile* app in ODC, which would make it a third app. **Re-fetched 1 Nov and one of my own arguments withdrawn**: I had written that `MediaResult` gives "only a thumbnail", which the page does not support. It also **never mentions iPad, iPadOS or Safari**. Recorded in `practice-camera-app/studio-build.md` step 2 |
| A summary naming two Forge components — **Camera Capture (ODC)** (`VideoCapture`, `VideoCaptureAndDisplay`) and **Camera Overlay Plugin (ODC)** | **Unverified AI prose.** Treated as claims | Both are worth ten minutes in Forge. The overlay one is interesting for a reason the summary did not give: a square crop *guide* over the live feed would let a parent frame the card at capture time. `studio-build.md` §2c, flagged as unverified — this project has had one AI-written summary need reframing already (`slack-2-image-generation.txt`) |

**Also named by the official page and worth installing: the Camera Sample App** on Forge —
a prebuilt app demonstrating take-a-photo, choose-from-gallery and edit. Worth reading even
though we will not use the plugin.


---

## Kickoff material, 2 November 2026

| Source | Grade | What came of it |
|---|---|---|
| **The organiser's answers to the five questions sent 1 Nov**, relayed by A.J. | **Authoritative** — the organiser's own words, five lines | One closes a subsystem (*"We will not use twilio for this hackathon"* → `TWILIO-WITHDRAWN-2-NOV.md`), one closes the nonprofit question for good (*"we do not have relationship with any nonprofit working in the area of autism"*), one reveals the **submission format is different this year**, and two defer to the call or to unpublished "enablement resources". Transcribed in the status header of `QUESTIONS-consolidated.txt` |
| **`Hackathon-scoring.png`**, **`UX Evaluation slide.png`**, **`Subbmission-details.png`**, **`more-details2.png`** and **`AI-model-details.png`** — the *Tech* criteria, *UX* criteria, *Submission*, Taikai project-page walkthrough and *AI Services* slides, photographed from the kickoff Zoom between 10:14 and 10:27 ET | **Authoritative.** They are the slides themselves, read directly | Transcribed verbatim and mapped in **`SCORING-CRITERIA.md`**. This is criterion one made concrete: 40% Agentic (Mentor and Agent Workbench named inside it), 20% DataFabric, 20% Knowledge Base + Semantic Search, 20% Modular Architecture / Governance / Security. **Between them they found two gaps**: nothing in the design reaches an external data source, so the DataFabric bucket scores nothing — and **Inclusivity**, half of UX's 40% bucket, is almost unwritten. UX adds User Centered Design 40%, Usability 20%, Design 20%, Innovation 20%; note that Innovation appears here as a UX sub-bucket although `rules.txt:40` lists it as a category of its own — the submission slide then confirms **separate Demo, UX and Innovation juries**, so it is scored twice. The submission slide is the biggest of the three: the deadline moved to **11 Nov, 2 PM GMT+1 (08:00 EST)** and the submission is **two videos**, only one of which was ever planned. The last two slides answer the rest: the videos go on the **Taikai project page** — Demo as a YouTube/Vimeo link in the **Gallery**, Tech Video as a link in the **Description** (`SCORING-CRITERIA.md §C7`) — and **two hackathon models at 10,000,000 tokens a day each** end the token-scarcity problem (`Autism-Visual-Supports/TOKEN-BUDGET.md §2d`) |

| Source | Grade | What came of it |
|---|---|---|
| **`2026 Hackathon Kick-off Presentation.pdf`** (19 slides), **`…Technical Evaluation - Google Docs.pdf`** and **`2026 Hackathon Resources - Google Docs.pdf`**, added 11:38 ET | **Authoritative — the organisers' own documents.** The Resources file is the *"enablement resources"* promised in answer to T7 | Read in full and written up in **`RESOURCES-AND-CRITERIA-NOV-2.md`**. They are **more specific than the photographed slides**: the tech criteria have **five** sections, not four; **DataFabric means AWS/Microsoft infrastructure**; **Logic Isolation means ODC Libraries**; **Observability names token consumption and cost**; **HITL means pausing agent execution**. They name **Agent Guardrails**, **Agent Evaluations** and **OutSystems MCP** as platform features. Four unphotographed slides: the **Innovation criteria**, the **four-person jury**, the **MS-or-AWS category** and two special awards, and **prescriptive shot lists** for both videos. The final slide lists **Autism Speaks** as a featured nonprofit |

| Source | Grade | What came of it |
|---|---|---|
| **`makeadifference@outsystems.com`, "2026 hackathon kick-off session", 2 Nov 16:34 UTC** — read from Gmail | **Authoritative — the organiser's own email** | Closes T7: the promised *"enablement resources"* is the Resources document already read. Carries the **recording link**, the deck as an attachment, and **live Google Docs** for the technical criteria and the resources — so the three PDFs are a *snapshot* of 11:38 ET and the Docs can change under them; re-check before submitting. Restates `#help` as the support route. `RESOURCES-AND-CRITERIA-NOV-2.md §6.1` |
| **The Zoom AI meeting summary** of the kickoff, same thread, 2 Nov 15:59 UTC | **SECOND-HAND.** Machine-generated, stamped *"AI can make mistakes"*, and it misnames Kris Lande, Jennifer Forman and Haiku 5.5 in the text it is being quoted for | **It is the only record of the question period**, and three answers matter: **Data Fabric is "optional, with mock integrations also being acceptable"** (which would defuse the 20% Connectivity hole — flagged against `SCORING-CRITERIA.md §A4` but not acted on until confirmed in `#help`), **"no limits on mentor usage"** (`TOKEN-BUDGET.md §8` q6), and **Twilio is unsponsored rather than banned**, with a 2027 partnership planned. Also: the category may be **AWS, Microsoft or both**; the two-day extension was for **Diwali**; support tickets must carry *"Hackathon"* in the title. `RESOURCES-AND-CRITERIA-NOV-2.md §6.2` and `§6.3` (the verification is now `§6.4`) |

---

## Added 7 November 2026 — the Australian practitioner video and its transcript

| Source | Grade | What came of it |
|---|---|---|
| **`Communication Tips & Strategies- 'First and Then' Boards (via DW YouTube Downloader).mp4`** — 48.6 MB, ~2:50, a speech-pathology service's "Communication Toolbox" episode presented by a clinician named Danielle | **Not readable here.** No ASR tooling exists in this environment and `ffmpeg`/`ffprobe` are not on the sandbox PATH, so the audio could not be transcribed locally. **A.J. transcribed it himself** rather than have the attempt made | Superseded by the transcript below. Keep the .mp4 as the primary record; it is **not** repo material (48 MB, third-party content) |
| **`First-then-board-transcript-from-australia.txt`** — A.J.'s transcript, 2,468 bytes, 11 timestamped blocks, complete from the greeting to the sign-off | **SECOND-TIER, but the best second-tier source we have.** A practising speech pathologist demonstrating the technique, not a vendor article selling a programme — so it is a cleaner read on *mechanics* than `sources-web/autism360-first-then/`. It is still **not a citation source**: no study, no standards body, and the service is a commercial provider. The two citable sources stay the TRIAD toolkit and the National Standards Report | **Confirms four things we already do and names two we do not.** See the two rows below |

**What it confirms** — each already in the build, so no change: move to the Then *quickly* once the First is done (Reviewer Q1 already bounds this at sixty seconds); pick a First at the child's level and not too hard; keep the board **in the child's sight** so they can work independently (Reviewer Q7 placement); and offer a **choice board** for the Then rather than always choosing it for the child (`Choice` is already a card Role, `choice` already a technique under Antecedent Package, and SPEC.md §7 already carries the Choice-board row).

**Gap 1 — the board never tells the parent what to do with the cards.** The transcript states the hand mechanic twice: *"Once the first activity is completed, remove the symbol from the board and then show the child the then activity."* Our contract covers what to **say** (`script`, four phases including `OnCompletion`), where to **put it** (`plan.placement`) and how to **prompt** (`plan.promptHierarchy`) — but nothing in `$defs/plan` or in `prompts/composer.md` says to clear the First card and reveal the Then. A parent following our board exactly would leave both cards up, which is the state that teaches the child the two pictures are simultaneous rather than sequential. **FIXED 7 November 2026**, commit `db04aeb`: a new `plan.boardAction`, required only for `FirstThenBoard` and `VisualSchedule` via the schema's `if`/`then` pattern, plus Composer rule 13, Reviewer question 10 `BOARD_NOT_OPERABLE`, and 12 records backfilled. **Decided at the same time, because the transcript is ambiguous and it changes every board: both cards stay visible from the start and the FIRST card comes off on completion** — a covered reward is not a motivator. Three eval cases test it (`c12`, `c13`, `c14`).

**Gap 2 — no graduated step between First–Then and a full schedule.** *"If they find the first then activity easy to complete, you can make it a little bit harder… by adding in an additional then. So then your visual becomes first, then, then."* Our four `supportType` values jump straight from `FirstThenBoard` to `VisualSchedule`. The optional `plan.generalization` field is the nearest home for it, and nothing currently names it. **Candidate fix: name the first→then→then step in `plan.generalization` guidance** rather than adding a fifth support type, which would cost a layout template. **STILL OPEN** — A.J. has decided gap 1 and the eval cases but not this one, so do not apply it without him.

## Added 7 November 2026 — the First–Then failure-mode article

| Source | Grade | What came of it |
|---|---|---|
| **`First-then-board-possible-problems.pdf`** — A.J.'s *Microsoft: Print To PDF* capture of the Autism 360 article, 27 pages, 6.7 MB | **UNUSABLE AS A FILE.** It has **no text layer at all**: `pdftotext` returns 27 characters for the whole document, `pdffonts` lists **zero** embedded fonts, and `pypdf` finds 0 characters and 4–10 images per page. It is 27 page *pictures*. This is exactly the check `ODC-GROUNDING.md §2` says to run on any new source, firing for the first time | **Do not upload it to the knowledge base.** No OCR tool is installed here (`tesseract`, `ocrmypdf`, `pdfimages`, ImageMagick all absent), so the text cannot be recovered locally. It did not need recovering — the live page was fetched instead. **Keep the PDF only as a visual record**, or delete it |
| **The article itself**, fetched from the live site, HTTP 200, 316,687 bytes → `sources-web/autism360-first-then/` as `page.html` plus `article.md` (4,135 words) | **SECOND-TIER — commercial, not clinical.** Autism 360 sells a paid programme and the article body carries three promotions for it. **It must not become a third citation source** beside the TRIAD toolkit and the National Standards Report; a board citing a vendor blog is worse than one citing nothing. Full reasoning: `sources-web/autism360-first-then/PROVENANCE.md` | **Its value is failure modes, which need no citation.** Six ways a First–Then board fails in a real house, of which **two are not covered anywhere in our design**: the board sliding into *bribery* when the reward is offered after distress has already started, and the child who does not yet understand the first→then *sequence* and needs two preferred activities first. Both are Reviewer questions we do not ask. It also names the underlying theory — **Premack's principle** — which is independently citable and maps to `Antecedent Package` |
