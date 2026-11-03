# Autism Visual Supports — OutSystems hackathon

First→Then boards for autistic children, built for the OutSystems *Build for the Future*
Hackathon 2026. A.J.'s daughter is autistic; his wife is the first test user.

**This file loads every session. The conversation gets compacted; this does not.** Twice
already a compaction summary has carried a fact that was stale by days — "no PIL" and
"eight idle days" were both wrong when acted on. If something matters past today, it goes
in a file.

**A.J. adds files to `hackathon-future/` without announcing them** — course transcripts,
documentation exports, screenshots. Run `ls -lt` early in a session and compare against
`SOURCE-MATERIAL.md`, which records what each file is and whether it has been read.

**Two directories, one project.** `hackathon-future/` holds the source material, the
emails and the hackathon rules; `Autism-Visual-Supports/` is the public git repo and the
submission. **The working directory flips between them without warning — always use
absolute paths.** This file lives in the parent so it loads from either, and so it stays
out of the public repo.

---

## 1. The boundary that decides almost everything

**The submission is built in OutSystems Developer Cloud. It is not built on AWS.**

There is no `aws odc`. ODC is provisioned and operated by OutSystems inside accounts we do
not hold. Scoring criterion one is *"application of the ODC features presented during the
kick-off"*; the prizes are ODC licences. An AWS-CLI build would be a different,
non-qualifying project. `PRE-BUILD-LAB.md` §1 settles this and `CODE-PLAN.md` §7
distinguishes the three things that get called "rolling out to AWS".

What follows from it, and keeps being re-derived the hard way:

- **The AWS surface is one service.** Amazon Bedrock, reached from our code.
  `AWS-ARCHITECTURE.md` §1.4 is titled "the one AWS service our code reaches out to".
- **AWS Trusted Advisor cannot be run against the submission** — it is an account-level
  inspector and we hold no account in the ODC tenant. It *can* run against the personal
  lab account, which is a different thing and not what is being judged.
- **One row is ours on either architecture: token metering.** It used to be two — webhook
  authentication was the other, because a managed platform does not authenticate a third
  party's callback — but **the only third party calling in was Twilio, withdrawn 2
  November** (§2). If the SMS path is cut, that row goes with it, along with trust
  boundaries B3 and B6 and open item 1. **Corrected 30
  October:** there *is* a console — the **Trial Model details** page in the ODC Portal
  shows trial-model limits and consumption. The `TokenUsage` entity is still needed, for a
  different reason: that page is for a human to read, not a feed the circuit breaker can
  query, and it cannot attribute cost to a board.
- The personal AWS account is a **lab bench**, not the build. Every call on it is billed to
  A.J.'s card. `PRE-BUILD-LAB.md` §3 sets a $25 budget first, deliberately low.
- **Nothing in that account exists yet — measured 2 November, not assumed.** `aws-cli
  2.38.5` is installed; `aws configure list` returns `<not set>` for access key, secret and
  region; `aws configure list-profiles` is empty; `~/.aws/` holds no credentials file. So
  **all of `PRE-BUILD-LAB.md §7` steps 1–6 are undone**: no IAM user, no key, no region,
  no `sts get-caller-identity`, **no Bedrock model access** (a fresh account has none, and
  §7 flags this as the step most often mistaken for a broken credential) and no budget.
  `tools/token-log.csv` holds only its header, so **no lab call has ever run**, and
  `aws-lab-signin.json` does not exist, so that ten-step page was never saved past step 1.
  `aws configure agent-toolkit` on 31 Oct installed 24 skills — **it does not sign you in**,
  and that is why this felt done.
- **Do not stand any of it up yet.** The reason to need it changed twice in one day: the
  written criteria made a Data Fabric connection to AWS the direct route to a 20% bucket
  (`RESOURCES-AND-CRITERIA-NOV-2.md §1.1`), and the kickoff Q&A then said Data Fabric is
  *"optional, with mock integrations also being acceptable"* — second-hand, from the Zoom
  AI summary (§6.2 of the same file). **`QUESTIONS-consolidated.txt` GROUP A questions A1
  and A2 settle whether any AWS account work happens this week**, and a billable data
  source created before they are answered is work in the wrong order. Note also that the
  $25 budget is sized for Bedrock *text calls*; anything hosted bills by the hour.

## 2. Claims that must stay true

Everything shipped has to survive a reviewer, a clinician, or a parent reading it.

- **No diagnosis, no clinical advice.** Self-injury, aggression or escalation in a parent's
  text surfaces referral guidance instead of a board. This is guardrail 5 in `SPEC.md` §6
  and the only guardrail with a safety cost if it is wrong.
- **There is no nonprofit partner, and that is settled rather than pending.** Autism
  Speaks is named as *intent*, never as a relationship. The evidence base is public
  material (the Vanderbilt TRIAD toolkit published through the Autism Speaks ATN; the
  National Autism Center's National Standards Report) — citing it is not a partnership and
  must never be written as one. **Answered 2 November, after asking twice:** the
  organisers replied *"we do not have relationship with any nonprofit working in the area
  of autism"*. So no introduction is coming and **"introduction requested through the
  organizers" must not appear in any document** — it did in `MID-SUBMISSION.md` and was
  corrected. **But the kickoff deck's final slide lists `Autism Speaks (autismspeaks.org)`
  among 20 *Featured Nonprofits & Partner Organizations*.** That does not relax anything
  here — a featured organisation is not an introduction, and intent is still never written
  as a relationship — but it is a *different premise* from the question that was answered,
  so one question on their terms is fair: *"your deck lists Autism Speaks among featured
  nonprofits; is there a route to them?"* It also means the alignment is worth stating in
  the Demo, because our clinical source is the TRIAD toolkit published through the Autism
  Speaks ATN and both halves are facts. `RESOURCES-AND-CRITERIA-NOV-2.md §5`.
  **And the organisers framed the way out themselves, in the same Q&A:** nonprofit use
  cases from OutSystems are *limited this year due to previous challenges*, and *"teams can
  still develop solutions for non-profits or causes they support"*. With the Demo brief's
  *"the nonprofit **or community cause** you are supporting"*, that is two independent
  statements that **a cause is a legitimate entry**. Say cause, never partner.
- **Twilio is out of this hackathon, confirmed 2 November** — *"We will not use twilio for
  this hackathon."* That **supersedes `rules.txt:36`**, which still names Twilio use as a
  condition of a special prize and was the only evidence the project had for calling it
  required. Never write that Twilio is required, and never present the SMS loop as live.
  **The precise shape, from the kickoff Q&A: unsponsored, not banned.** *"Twilio is not
  participating… no Twilio accounts or credits will be provided"*, a partnership is planned
  **for 2027**, and *"participants can use their own Twilio services"*. So it is not
  forbidden — it is unfunded and unscored, which is a weaker claim than "out" and the one
  to make if it ever comes up. It does not change the recommendation to cut.
  The reward-confirmation *loop* survives without it; the transport does not.
  `TWILIO-WITHDRAWN-2-NOV.md` holds the consequences, the recommendation to cut, and the
  replacement wording for the published description — which still names Twilio twice.
- **The child's name never appears in an image prompt.** Prompts say "a child".
  `SPEC.md` §5.
- **Always the same child across the If and the Then picture** in any artwork. A.J. asked
  for this explicitly and it is a clinical point, not a style one.
- **Evidence claims cite a practice by name.** Every board names which of the 11 National
  Standards practices it rests on; `SPEC.md` §7 maps feature → practice.
- The concept video is **unlisted** (`<UNLISTED-VIDEO-LINK-WITHHELD>`), link-only by A.J.'s
  choice, and is deliberately **not** in the repo.

## 3. Generated files — never hand-edit, never hand-copy

Four generators own their output. Editing a generated file is erased by the next run, and
`cp`-ing one between directories is how a stale PNG survives for days.

| Generator | Owns |
|---|---|
| `assets/build_cards.py` | `assets/cards/*.svg` (201), `MANIFEST.csv`, `cards-contact.svg` |
| `assets/build_art.py` | the submission artwork |
| `assets/build_diagram.py` | `trust-boundaries*` — reference **and** deck variant |
| `tools/build-eval-page.py`, `tools/build-gems-page.py` | the two review HTML pages |

**Every generator derives its output path from `os.path.dirname(os.path.abspath(__file__))`.**
A generator that writes elsewhere needs a hand copy, and the repo then cannot tell a stale
file from a current one. `assets/ASSETS.md` cautions 11 and 15.

**`build_diagram.py` has a regression test: `build(slide=False)` must reproduce the
committed `trust-boundaries.svg` byte for byte.** Diff it after any change to that file.

**The root `assets/` exists because two repo generators used to write into it — fixed
1 November 2026.** `build_art.py` had `OUT` hardcoded to the parent directory and
`build_video.py` did `sys.path.insert(0, <that path>)` before `import build_art`, so the
repo's own generators wrote the asset set *outside* the repo and imported the parent's
copy of themselves. Both now derive their paths from `__file__`. Caution 19 in
`ASSETS.md` has the measurements.

**The repo copy is authoritative; the root copy is a levelled duplicate with no writer.**
Its three stale files were replaced on 1 Nov — `ASSETS.md` (was 182 lines, missing
cautions 12–18), `build_diagram.py` (carried the very `OUT` caution 11 forbids) and
`trust-boundaries-2x.png` (**was 3413×1920, caution 16's bug, live**). The root copy holds
nothing the repo lacks but `__pycache__`, and has no `cards/`. It can be deleted outright;
until it is, read asset rules from the repo.

**The check that catches a recurrence:** `grep -rn "hackathon-future/" --include="*.py"`
inside the repo must return `video/make_video.py` and nothing else. That one is a
deliberate exception, annotated in the file — the concept video is kept out of the repo on
purpose.

**Verified 1 Nov, in a scratch copy so the repo was never written to:** `build_art.py`
reproduces all **21** committed SVGs byte for byte, and `build_diagram.py` reproduces
`trust-boundaries.svg` *and* the slide variant byte for byte, with both 2x renders at
2560×1440.

`assets/ASSETS.md` carries cautions numbered to 19. Read it before touching any image.
(13 and 14 are written as prose paragraphs rather than list items, so grepping for `13.`
finds nothing — they are there.) The three that cost the most:

- **#14 — an icon that passes in the SVG can fail at card size.** Render
  `cards-contact.png` and *look at it*. At 201 cards the sheet is 2034×3372, too tall to
  read in one go: slice it into three bands.
- **#16 — Chrome multiplies `--window-size` by `--force-device-scale-factor`.** Asking for
  `2560,1440` with a 1.333 factor silently produces 3413×1920. Hold the window at the CSS
  size, vary only the factor, and **read the pixel dimensions back**.
- **#17 — a degenerate SVG path draws nothing and raises nothing.** The Night card shipped
  as four yellow dots because its crescent arc rendered empty.

## 4. Environment facts that cost time to rediscover

- **PIL 13.0.0 *is* installed.** Earlier notes in this project said it was not; that is
  wrong. PIL still cannot render SVG — Chrome does that — but anything after
  rasterization (crop, slice, measure, composite) should use PIL rather than another SVG
  trick.
- **Rasterizing SVG**: headless Windows Chrome at
  `/mnt/c/Program Files/Google/Chrome/Application/chrome.exe`.
  **Windows Chrome cannot read `/tmp`.** Input and output must both sit under `/mnt/c/...`
  and be passed as `C:/...`. The session scratchpad is under `/tmp`, so Chrome work needs a
  scratch directory on the C: side.
- **`soffice` is at `/usr/bin/soffice`** and is the same pipeline that produced the deck
  PDF. After re-exporting, render one unchanged page from the old and new PDFs and compare
  before replacing — that check is what proved the round-trip was lossless.
- **`python-pptx` and `boto3` are not installed**, and system pip is blocked by PEP 668.
  Use `python3 -m venv` in the scratchpad. `tools/lab-measure.py` calls the AWS CLI rather
  than boto3 on purpose.
- Available: `aws`, `ffmpeg`, `pdftotext`, `pdfinfo`, `node`.
- **`node --check` cannot read a process substitution.** Write the script to a real file.
- **`jsonschema` is not installed and system pip is blocked** (PEP 668). The schema
  fixtures are validated from a throwaway venv: `python3 -m venv … && …/bin/pip install
  jsonschema`. `tools/test_guardrails.py` deliberately has **no** dependencies, so it runs
  under plain `python3` — but not under `python3 -I`, which drops the script's own
  directory from `sys.path` and breaks `import guardrails`.
- **Google Tasks needs its own interpreter.** `../google-tasks/tasks.py` is the live task
  list, read/write, and it must be run as `./.venv/bin/python tasks.py …` from that
  directory. Plain `python3` gives `ModuleNotFoundError: google`. It has no in-list
  reorder — `move` is cross-list only — and new tasks land at position 0, so the way to
  raise a task's priority is to delete it and add it again.
- **Before committing, check the index separately from the working tree.** On 31 Oct the
  index held a two-day-old snapshot of eight files while newer edits sat unstaged on top,
  so a plain `git commit` would have captured the stale version and stranded the rest.
  `git diff --cached --stat` and `git diff --stat` answer different questions; run both,
  and `git reset` (never `--hard`) to clear a stale index before staging deliberately.
- **`aws-mcp` failed because `uv`/`uvx` was not installed at all** — not merely off PATH.
  **Fixed 2 Nov: `brew install uv` → uv/uvx 0.13.6** at
  `/home/linuxbrew/.linuxbrew/bin/{uv,uvx}`, already on PATH, no PATH edit needed. (Brew
  *is* reachable from the sandbox — Homebrew 7.0.10, with `pipx` and `pip3` beside it — so
  that directory is **not** wholly masked, whatever earlier notes implied.) Verified
  end to end: `uvx mcp-proxy-for-aws@latest --help` resolves, downloads and exits 0.
  **MCP servers connect at session start, so the server appears only after a restart.**
  Config is `~/.claude.json` → `command: uvx`, `args: ["mcp-proxy-for-aws@latest",
  "https://aws-mcp.us-east-1.api.aws/mcp", "--metadata", "INSTALL_SOURCE=aws-cli"]`.
  **It still cannot do anything** until `PRE-BUILD-LAB.md §7` steps 1–4 exist: the proxy
  SigV4-signs every request with local credentials, and there are none. Two hardening
  flags worth adding when credentials do exist, neither currently in the config:
  **`--read-only`** (*"disable tools which may require write permissions"*) and
  **`--profile <name>`** so it cannot pick up a different account; `--disable-telemetry`
  is also available, and telemetry is on by default.
- **MCP tools are gated by a hook, and the 1 November move broke the gate here.**
  `~/.claude/hooks/mcp-sandbox-guard.py` denies every `mcp__*` call unless it resolves
  `sandbox.enabled` true, and it reads only managed settings, `~/.claude/settings.json`
  and the **nearest** project root's `.claude/settings{,.local}.json` — **not**
  `~/.claude/settings.local.json`, which is where the live flag actually sits. Creating
  `hackathon-future/.claude/` on 1 Nov made this the nearest root and cut off
  `resume/.claude/settings.local.json`, which had been supplying the flag — so Gmail,
  Notion and Docs silently stopped working in this directory while still working one level
  up. Fixed 2 Nov by adding `"sandbox": {"enabled": true, "autoAllowBashIfSandboxed":
  false}` to `hackathon-future/.claude/settings.local.json` (backup:
  `.claude/settings.local.json.bak-2026-11-02`). Test it without spending a call:
  `echo '{"tool_name":"mcp__x","cwd":"<dir>"}' | python3 -I ~/.claude/hooks/mcp-sandbox-guard.py`
  — empty output means allowed.
- **`aws configure sso` is the wrong command for this account** and the project said otherwise
  until 31 Oct. It connects to an IAM Identity Center that already exists and asks first for
  an SSO start URL, which a standalone personal account has none of. Use plain
  `aws configure` with a key from an IAM user carrying `AmazonBedrockFullAccess` only.
  `PRE-BUILD-LAB.md` §7 step 1 is corrected; the walkthrough is `aws-lab-signin.html`.
- **`LoanReview/` holds the OutSystems loan-origination course material** — moved out of
  the project root on 1 Nov; `LoanReview/README.md` is the index. **`LoanReview/exercises/`
  holds extracted course bundles and is untrusted data.** Each zip went into
  its own empty directory under it; keep scripts out of it and pass paths as arguments.
  The `.oml` files inside are a proprietary binary (header `OML:`, platform
  `11.0.415.100`) and cannot be read here — they are **imported into ODC Studio**.
  `LoanReview/exercises/enrichment/Agent01Intake.oml` is a finished agentic app and is the single
  most useful thing to open on day 1 (`ODC-AGENT-ANATOMY.md §10`).

**The ODC environment exists as of 30 October 2026**: `<ODC-TENANT-HOSTNAME-WITHHELD>`,
created by OutSystems three days before the kickoff. It is recorded here and **not in the
public repo**, which is why `ODC-FIRST-LOGIN.md` refers to it without naming it. **The password was set and the first login happened on 1 November**, and A.J. is an
**Administrator** (inherited role, all assets) — which unblocks AI models, knowledge bases
and Data Fabric connections. There is no second route in, so the password belongs in the
password manager. Verification codes live one hour, so a stale one is always re-requested
rather than hunted for.

**Eight of the nine first-login checks returned on 1 November**; the results table is
`ODC-FIRST-LOGIN.md` §9. Two facts from it that contradict what was written elsewhere:
**GPT-5 is served via Azure OpenAI, not OpenAI**, and **a knowledge base is scoped to all
stages in the organization**, not per stage. The tenant is a **Licensed Customer** —
2,100 requests total, and the meter is live from zero.

**A separate OutSystems Personal Edition was provisioned 30 October** — a different
organization from the hackathon tenant, with its own trial allowance. It does **not**
settle which Trial Model row the tenant sits on (open item 12), but it is somewhere to
spend rehearsals without drawing down the tenant's caps. OutSystems deletes idle Personal
Editions, so export anything built there.

## 5. Where the current state lives

Pointers, not snapshots. A snapshot here goes stale and starts misleading.

| Question | File |
|---|---|
| What the judges actually score, and where we are weak | `SCORING-CRITERIA.md` — the kickoff slides transcribed verbatim and mapped bucket by bucket. **§A Tech** (`Hackathon-scoring.png`, 10:14 ET): Agentic Automation & AI **40%** with *Mentor* named inside it, so using Mentor is evidence and not just a shortcut · DataFabric **20%**, **our zero** — nothing in the design reaches an external data source · Knowledge Base + Semantic Search **20%**, our strongest, both entitled · Modular Architecture / Governance / Security **20%**, naming **Forge Acceleration** (so T8 is worth points) and **Real-time Observability**, which we have nothing for. **§B UX** (`UX Evaluation slide.png`, 10:18 ET): User Centered Design **40%** — User Needs is our strongest ground anywhere, but its other half, **Inclusivity, is close to unwritten** (one contrast caution in `ASSETS.md`, about artwork, is the only hit in the whole project) · Usability **20%**, where *"under two minutes" is a target and never a measurement* · Design **20%** · Innovation **20%**. **Both slides are 40/20/20/20 within their own category, and neither says what the category is worth overall** — a 20% gap in Tech is not 20% of the prize. **Innovation is scored twice** — it is a 20% bucket inside the UX slide *and* has a jury of its own, named on the submission slide. **§C is the submission itself**: due **11 Nov, 2 PM GMT+1**, as **two videos** — a strictly 5-minute **Demo** for the Demo, UX and Innovation juries, and a 10-minute **Tech Video** for Product Management, which is where the Tech criteria get *shown* instead of claimed. The Demo's focus names **"the nonprofit value"**, which §C5 handles without implying a partnership. **One caveat added 2 Nov evening**: §A4's DataFabric zero may be **possibly defused** — the kickoff Q&A called Data Fabric optional and mock integrations acceptable — but that is second-hand and *"accepted"* is not *"scores the same"*, so the section stands as written with the flag against it until `#help` answers GROUP A's A1 |
| What the three kickoff PDFs changed, and the four things they change in the build | `RESOURCES-AND-CRITERIA-NOV-2.md` — the written criteria are **more specific than the slides** and in four places they move the design: **DataFabric means AWS or Microsoft infrastructure**, not any external source · **Logic Isolation means ODC *Libraries*** specifically, which our Web/Agentic app split does not satisfy on its own · **Real-Time Observability names token consumption and cost**, so `TokenUsage` is scored rather than merely prudent · **Human-in-the-Loop means a checkpoint that PAUSES agent execution**, not a review of finished output. It also names two platform features we built by hand — **Agent Guardrails** and **Agent Evaluations** — plus **OutSystems MCP** for connecting AI coding tools, which sits in the 40% bucket. And four slides the photographs missed: the **Innovation criteria** (one of which asks whether the entry is *"just a digital version of an existing paper/Excel form"* — aimed squarely at a First→Then board, answered in §3.1), the **four-person jury**, the **MS-or-AWS category selector** and its two special awards, and the **prescriptive shot lists** for both videos. **§6, added 2 Nov evening**, is the organisers' wrap-up email and the Zoom AI summary of the call — the email closes T7 (the *"enablement resources"* is the Resources document we already have) and carries the recording link, and **the two criteria documents are live Google Docs, so the PDFs are a snapshot of 11:38 ET on 2 Nov and can drift — re-read the Docs before submitting**. The Zoom summary is **second-hand** (machine-generated, and it misnames two jurors and a model) but it is the **only record of the question period**, and three of its lines move the build: Data Fabric *"optional, with mock integrations also being acceptable"*, *"no limits on mentor usage"*, and Twilio unsponsored rather than banned |
| What is being built, screen by screen | `SPEC.md` |
| What we do not know yet, and the fallback for each | `AWS-ARCHITECTURE.md` §5 — eleven open items, **eight answered** and struck through: 3 and 10, then 8 and 9 from the Slack reply (30 Oct), then 6, 7 and 11 from the first ODC login, then **2 from the Create-app dialog in Studio** (1 Nov). Item **4 was reframed, not answered**; items 1 and 5 are the two still open |
| How the agents retrieve, and the two Beta features | `ODC-GROUNDING.md` |
| The real shape of an ODC agent — scaffold, Events, Workflows, Settings, **Action calling** | `ODC-AGENT-ANATOMY.md` |
| What code exists, what must be written, review gates | `CODE-PLAN.md` |
| The guardrails, and the test table they are checked against | `GUARDRAILS.md` — 57 rows, 19 tests, `python3 tools/test_guardrails.py`. The board contract is `schema/board.schema.json` |
| What the AWS lab account is for | `PRE-BUILD-LAB.md` |
| Token budget, reserve, burn rate | `TOKEN-BUDGET.md` + `tools/token-log.csv` — **read §2d first.** The kickoff (2 Nov, 10:27) announced **two hackathon models, `BedrockHaiku5_5` (Haiku 5.5, AWS) and `Microsoft_OpenAI_GPT5_5_…` (GPT-5.5, Microsoft), at 10,000,000 tokens a day EACH** — per day and refilling, additional to the request-capped trial entries. One day on one model is 2.6× the whole build, so the reserve, the spending plan and the circuit breaker are no longer load-bearing; `TokenUsage` still is, because the organisers adjust limits daily and we cannot read their console. **Two architectural riders**: the GPT entry *"will be deprecated soon and replaced"*, so **the model must be a Setting, never a constant**, and anything load-bearing prefers the Bedrock Haiku entry; and *"feel free to configure and use your own models"* makes the `PRE-BUILD-LAB.md` AWS bench optional. Note the names — **Haiku 5.5 and GPT-5.5**, not the Haiku 4.5 / GPT-5 the trial entries carry |
| Well-Architected and Trusted Advisor passes | `NOTES-ARCHITECTURE-REVIEW.md` |
| Image and layout rules, and 18 cautions | `assets/ASSETS.md` |
| What to check on first login to ODC, and what it closes | `ODC-FIRST-LOGIN.md` |
| ~~The 4 November mid-submission~~ — **there is none.** Confirmed at the kickoff, 2 Nov: the only submission is the final one | `MID-SUBMISSION.md` — **keep it, never send it.** Its problem statement, use case, AI services and integrations are the raw material for both video scripts, and the only place that content sits in one piece |
| What A.J. has dropped into the parent directory, and what is still unread | `SOURCE-MATERIAL.md` |
| The OutSystems loan-origination course material (four exercises, the `.oml` reference apps) | `LoanReview/README.md` — moved out of the project root 1 Nov. `LoanReview/exercises/enrichment/Agent01Intake.oml` is the finished agentic app to import |
| The practice camera app, and what it is meant to answer | `practice-camera-app/build-picturecards.html` is the page to work from while building (16 items, Copy buttons on the code, measured-size and privacy fields); `studio-build.md` is the same build with the reasoning. **The Camera Plugin is NOT ours** (it needs a native app or a PWA; our parent app is a Web app per `CODE-PLAN.md §8`), so capture is a file input with `capture="environment"` on a phone and `getUserMedia` on a laptop, both converging on one canvas that also solves HEIC and the downscale. `practice-camera-app/NOTES-devices.md` answers the phone→desktop handoff (one app, one database, same stage — it is free), the already-taken picture (the Upload widget without `capture`) and the iPad (works; `capture` may not skip Safari's action sheet), and carries a six-row device test matrix in which **the Windows-Chrome HEIC row is expected to fail**. Its **§6 (2 Nov)** settles the four iOS usage-description keys: they live in a native binary's `Info.plist`, so **they are not ours** — a Web app, and an installed PWA on iOS too, gets Safari's own camera prompt, which we cannot word. The consequence is a UI item, not a setting: our own explanation has to sit **above** the button that triggers the prompt. Only camera and photo-library read would ever apply even natively; we never write to the camera roll and record no audio. **The hand-build is the primary path**, because the intake exercise states Mentor cannot do scaffolding and this app is mostly scaffolding. `mentor-prompt.md` holds five Mentor Studio blocks for the logic and the 13 questions, and `mentor-prompts.html` is the same thing as a page with a Copy button per prompt, checkboxes and comment boxes, saving to `mentor-prompts.json`; answers go in `practice-camera-app/findings.md`. **Read the trial-model meter before and after** — whether Mentor spends the 2,100-request allowance is open question 6 in `TOKEN-BUDGET.md §8` and this is the only cheap experiment for it |
| What is on A.J.'s actual task list | Google Tasks, the **Build For the Future** list. Read it with `../google-tasks/tasks.py show --list Build` — see §4 for the interpreter |
| What still needs asking, and what must NOT be re-asked | `QUESTIONS-consolidated.txt` — **all five sent on 1 Nov came back on 2 Nov**, quoted verbatim in the status header. Two are genuinely closed (no nonprofit relationship; **Twilio is not used in this hackathon**), two were deferred to the kickoff (the 10M Bedrock entry; the submission format, which is *different this year*) and one was answered with a pointer rather than a figure (*"we will share enablement resources"* — Mentor's consumption is still unknown). **Three were never asked**: which stage judges evaluate, the eleven-hour deadline discrepancy, and Forge/External Logic on this tenant — all three carried into `KICKOFF-NOV-2.md`. The Twilio *prize* question died with the service, so it is withdrawn rather than outstanding. The file also carries an **eliminated** list of ~20 answered questions, and **T9, added 2 Nov**: is there any OutSystems-provided route to run a native mobile app on an iPad this week, or does iOS need A.J.'s own Apple Developer account? Everything about the four `NS*UsageDescription` keys hangs off that one answer. **GROUP A, added 2 Nov**, is six AWS questions for `#help` in ask-order; **A1 (does a mocked integration score the same as a real Data Fabric connection) and A2 (is the AWS category about the sponsored models or about our own account) gate every other AWS decision this week**, and A4 folds the stage question into the sponsored-model question. **A6 is marked "ask only if the Portal does not show it"** — the Data Fabric provider list is a ten-minute look and A.J. is an Administrator. **T7 is closed**: do not re-ask Mentor's consumption, run the meter experiment |
| What the 2 November organiser answers changed, and what is still A.J.'s to decide | `TWILIO-WITHDRAWN-2-NOV.md` — why Twilio was in the design at all (`rules.txt:36` and nothing else), what dies with it (boundaries B3 and B6, the HMAC webhook, open item 1), what survives (the reward loop, the usage log, the promises-kept streak), the recommendation to cut and reclaim day 7, the three follow-ups in order, and **drafted replacement wording for the published Taikai description**, which still names Twilio in the body and in the tagline |
| Which plan decisions A.J. has agreed or flagged | `odc-plan-review.html` — 46 items; answers save to `odc-plan-review.json` beside it |
| How to sign in to the AWS lab account, and how far A.J. got | `aws-lab-signin.html` — ten steps, checkbox and notes each; saves to `aws-lab-signin.json` beside it |
| Kickoff join details, and what to bring back from it | `KICKOFF-NOV-2.md` — Zoom link, ID and passcode, and the five things to capture |
| What to do next, in order, and who each item is waiting on | `next-steps.html` — 22 items across tonight / Monday / 4 Nov / 9 Nov; saves to `next-steps.json` beside it. **Its dates are stale as of 2 Nov**: there is no 4 Nov milestone and the final deadline moved to the 11th |
| What to build in ODC, in build order, now that Studio runs | `odc-studio-next-steps.html` — 15 items: 5 with Studio open (two close open items 1 and 2), 4 for day 3, 6 held until after the kickoff; saves to `odc-studio-next-steps.json` beside it |
| What auto mode believes about this environment, and which lines are wrong | `auto-mode-setup.html` — the 23 `autoMode.environment` statements, **moved on 1 Nov from `~/.claude/settings.json` to `hackathon-future/.claude/settings.local.json`** so they apply to this directory and `Autism-Visual-Supports/` only and not to the resume project (global backup: `~/.claude/settings.json.bak-2026-11-01`), plus the sandbox/permission keys that enforce them, as 22 thumbs-up/down items; saves to `auto-mode-setup.json`. **Three statements are wrong**: repository visibility, default branch and a malformed last line. `Autism-Visual-Supports` is **verified PUBLIC** (`gh repo view`, 1 Nov), remote `github.com/aj-aronoff/Autism-Visual-Supports`, `main` ahead 3 |

**Every open item in `AWS-ARCHITECTURE.md` §5 has a named fallback, so none blocks the
build.** Items 8 and 9 were different in kind — ODC knowledge bases and semantic search are
Beta *entitlements* somebody else switches on, so no amount of trying resolved them.
**Both were answered 30 October**: OutSystems confirmed in the hackathon Slack that both
are enabled automatically on hackathon instances. So the knowledge base and semantic
search are **the design**, not the hoped-for branch of it, and the fallbacks in
`ODC-GROUNDING.md §4` are contingency only.

**The repo is committed locally and pushed only when A.J. asks.** On 31 October three
commits (`eec5a24`, `2df2ed3`, `0578cbf`, 1,200 insertions) were made and deliberately
left unpushed — `main` is ahead of `origin/main`. Do not push to close that gap; being
ahead is the chosen state, not a mistake. The content was checked for the §2 not-public
list before being offered for push and was clean; re-check if it changes.

## 6. Dates, and two files never to send

Registration closed 28 October. **The kickoff happened 2 November, 10:00–11:00 ET.** What
it changed is written up in `SCORING-CRITERIA.md` and `RESOURCES-AND-CRITERIA-NOV-2.md`;
`KICKOFF-NOV-2.md` holds the item-by-item capture, and §6.1 of the resources file holds
the **recording link**, which the organisers emailed afterwards.
**THERE IS NO MID-WEEK SUBMISSION.** Confirmed at the kickoff, 2 November — the 4
November deliverable this project planned for does not exist, and the only submission is
the final one. `MID-SUBMISSION.md` is therefore **kept and never sent**: its content is
the raw material for the two video scripts. Anything still showing a 4 November milestone
is stale — `next-steps.html`, `odc-studio-next-steps.html`, `SPEC.md`'s day table and the
Google Tasks list all predate this.

**FINAL SUBMISSION: 11 NOVEMBER 2026, 2 PM GMT+1 = WEDNESDAY 11 NOVEMBER, 08:00 EST
IN NEW YORK.** Announced at the kickoff (`Subbmission-details.png`) and **it supersedes
both** the rules' 9 November 11:59 PM CET and the Taikai timeline — the eleven-hour
discrepancy that was L5 is answered by both being wrong. Converted with
`TZ=America/New_York date`, not estimated. **Two days more build time, and no final
morning**: 08:00 in New York is before the day starts, so everything ships the night of
**Tuesday 10 November**, and that is the date to plan against. `PRE-BUILD-LAB.md`
schedules deleting the AWS lab key on 10 Nov — move it. **Why it moved, from the Zoom
summary: the event "was extended by two days until November 11th to accommodate Diwali
celebrations in India"** — which is a second, independent source for the 11th and explains
the clash with `rules.txt`.

**Publishing the project needs a category chosen, and it may be BOTH.** The submission
slide has a *Select category MS or AWS* field; the Q&A says *"select the appropriate
category (AWS, Microsoft, **or both**)… to be eligible for partner awards"*. There are two
special awards (AWS: Arun Nallathambi; Microsoft: Roberto Arocha) and no stated cost to
entering, so **take both if the field allows it, and AWS if it forces one** — Bedrock
Haiku, `AWS-ARCHITECTURE.md`, the Well-Architected pass and the DataFabric route all point
that way. Whether the field accepts both is a look at the Taikai project page, not a
question. And **Taikai requires an explicit publish after every edit** — an edited,
unpublished project is not submitted.

**There are TWO videos, not one** (`SCORING-CRITERIA.md §C`): a **Demo**, *strictly* max
5 minutes, for the Demo, UX and Innovation juries — which is the one `SPEC.md` day 8–9
already plans — and a **Tech Video**, up to 10 minutes, audience *Product Management*,
for *"technical implementation, key architectural decisions, and agent workflows"*. The
Tech Video is **new work nothing in the plan accounts for**, and it is also where the
Tech criteria get *shown* rather than claimed, which is how the Mentor evidence problem
gets solved. The Demo's stated focus names **"the nonprofit value"** — handle per §2:
public nonprofit material, families as beneficiaries, MIT licence, **never an implied
partnership**.

**A `#help` channel appeared in the hackathon Slack on 2 November, and it is now the only
route.** The earlier rule — technical questions to `#help`, scoring and deadlines held for
the kickoff call — **expired with the call**. The organisers' own wrap-up email says
*"For all support and questions, please go to the hackathon Slack space and post them on
**#help channel**"*, so everything goes there now, with `makeadifference@outsystems.com`
second and a support ticket third. A ticket for a **bug or product friction** must carry
**"Hackathon" in the title** *and* be posted in `#help` as well, not instead. Before
posting, check the **eliminated** list in
`QUESTIONS-consolidated.txt`: a channel with limited OutSystems attention is spent badly
on a question the documentation already answers, which is exactly why the
usage-description question became T9 instead.

Superseded drafts that must not be sent by accident — **all four moved out of the project
root into `archive-superseded/` on 3 November 2026** at A.J.'s request, because they did not
belong in the working directory: `email-followup-charities.txt`,
`email-3-team-name-change.txt`, `email-4-kickoff-questions.txt` and the question blocks in
`next-slack-questions.txt`. The last two were **absorbed into `QUESTIONS-consolidated.txt` on
1 November** after most of their questions were answered by the first ODC login. Sending any
of them now would ask things we already know. They were moved rather than deleted because the
parent directory is **not a git repository** and no other copy exists —
`archive-superseded/README.md` says why each one is dead.

`Autism-Visual-Supports-Overview.pptx` and `.pdf` in this parent directory **were stale
duplicates (23 Oct) and were re-synced from the repo on 1 Nov** — both are now
byte-identical to `Autism-Visual-Supports/docs/`. **The repo copy stays the live one**; a
copy out here goes stale again the moment the deck is rebuilt, so rebuild in `docs/` and
re-copy, or delete these two.

**The deck's content is still from 28 October.** It predates the guardrails, the board
schema, the first ODC login and the Agentic confirmation, so it is current as a *file* and
behind as a *document*. Refreshing it is a separate job from syncing it.
