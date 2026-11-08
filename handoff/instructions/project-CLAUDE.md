# Autism Visual Supports — OutSystems hackathon

First→Then boards for autistic children, built for the OutSystems *Build for the Future*
Hackathon 2026. A.J.'s daughter is autistic; his wife is the first test user.

**This is the REDACTED, PUBLIC copy of the project `CLAUDE.md`, and it is the LEAN half.**
Two values are replaced with `<...-WITHHELD>` placeholders; `handoff/README.md` says what each
one means. On 7 November 2026 the long-form prose was split into a second file,
**`CLAUDE-DETAIL.md`**, which holds the reasoning behind each rule, the closed incidents and the
measurements. **That file is NOT published** — it lives in the parent directory, which a cloud
session cannot read anyway. So where a rule here states a fact without its evidence, the
evidence exists and is simply out of reach: **ask A.J. rather than re-deriving it.** Section
numbers match between the two files.

**Three standing habits.** The conversation gets compacted; this file does not — anything that
matters past today goes in a file, not the chat. **A.J. adds files to `hackathon-future/` without
announcing them**, so run `ls -lt` early and compare against `SOURCE-MATERIAL.md`. **Two
directories, one project**: `hackathon-future/` holds the source material, emails and rules;
`Autism-Visual-Supports/` is the public git repo and the submission; the working directory flips
between them without warning, so **always use absolute paths.**

---

## 1. The boundary that decides almost everything

**The submission is built in OutSystems Developer Cloud. It is not built on AWS.** There is no
`aws odc`. Scoring criterion one is *"application of the ODC features presented during the
kick-off"* and the prizes are ODC licences, so an AWS-CLI build would be a different,
non-qualifying project. `PRE-BUILD-LAB.md` §1 settles this.

- **The AWS surface is one service** — Amazon Bedrock, reached from our code
  (`AWS-ARCHITECTURE.md` §1.4).
- **AWS Trusted Advisor cannot be run against the submission.** It is an account-level
  inspector and we hold no account in the ODC tenant.
- **The personal AWS account is a lab bench, not the build.** Every call bills A.J.'s card;
  `PRE-BUILD-LAB.md` §3 sets a deliberately low $25 budget first.
- **Nothing in that account exists yet — measured 2 November, not assumed.** No IAM user, no
  key, no region, no Bedrock model access, no budget; `tools/token-log.csv` holds only its
  header, so no lab call has ever run. `aws configure agent-toolkit` installed 24 skills on
  31 Oct — **it does not sign you in**, which is why this felt done.
- **Do not stand any of it up yet.** `QUESTIONS-consolidated.txt` GROUP A — A1 and A2 — gates
  whether any AWS account work happens this week.
- **One row is ours on either architecture: token metering.** `TokenUsage` stays even though
  the Portal's **Trial Model details** page exists: that page is for a human to read, not a
  feed the circuit breaker can query, and it cannot attribute cost to a board.

## 2. Claims that must stay true

Everything shipped has to survive a reviewer, a clinician, or a parent reading it. A claim that
cannot be traced to real work does not ship, however well it would score.

- **No diagnosis, no clinical advice.** Self-injury, aggression or escalation in a parent's text
  surfaces referral guidance instead of a board — guardrail 5 in `SPEC.md` §6, and the only
  guardrail with a safety cost if it is wrong.
- **There is no nonprofit partner, and that is settled rather than pending.** The organisers
  replied *"we do not have relationship with any nonprofit working in the area of autism"* on
  2 November. Autism Speaks is named as **intent, never as a relationship**; citing public
  material (the Vanderbilt TRIAD toolkit published through the Autism Speaks ATN; the National
  Autism Center's National Standards Report) is not a partnership. **"Introduction requested
  through the organizers" must not appear in any document.** **Say cause, never partner** — the
  organisers' own Q&A and the Demo brief both make a *cause* a legitimate entry.
- **`Visual_Supports_Tool_Kit.pdf` is Vanderbilt TRIAD copyright — never re-hosted.**
- **Twilio is out of this hackathon, confirmed 2 November**, and that supersedes `rules.txt:36`.
  **Never write that Twilio is required**, and never present the SMS loop as live. The precise
  shape is **unsponsored, not banned**: no accounts or credits, partnership planned for 2027,
  participants may use their own. The reward-confirmation *loop* survives; the transport does not.
- **The child's name never appears in an image prompt.** Prompts say "a child" (`SPEC.md` §5).
- **Always the same child across the If and the Then picture.** A clinical point, not a style one.
- **Evidence claims cite a practice by name** — every board names which of the 11 National
  Standards practices it rests on (`SPEC.md` §7).
- The concept video is **unlisted**, link-only by A.J.'s choice, deliberately **not** in the repo,
  and the URL is `<UNLISTED-VIDEO-LINK-WITHHELD>` in this published copy. It is in git history from `6b9ab52`;
  removing it from HEAD on 3 Nov did not remove it from history.

## 3. Generated files — never hand-edit, never hand-copy

| Generator | Owns |
|---|---|
| `assets/build_cards.py` | `assets/cards/*.svg` (201), `MANIFEST.csv`, `cards-contact.svg` |
| `assets/build_art.py` | the submission artwork |
| `assets/build_diagram.py` | `trust-boundaries*` — reference **and** deck variant |
| `tools/build-eval-page.py`, `tools/build-gems-page.py` | the two review HTML pages |

- **Every generator derives its output path from `os.path.dirname(os.path.abspath(__file__))`.**
  A generator that writes elsewhere needs a hand copy, and the repo then cannot tell a stale file
  from a current one.
- **`build_diagram.py` has a regression test**: `build(slide=False)` must reproduce the committed
  `trust-boundaries.svg` byte for byte. Diff after any change.
- **The check that catches a recurrence:** `grep -rn "hackathon-future/" --include="*.py"` inside
  the repo must return `video/make_video.py` and nothing else.
- **`assets/ASSETS.md` carries cautions numbered to 19 — read it before touching any image.**
  (13 and 14 are prose paragraphs, so grepping for `13.` finds nothing; they are there.)
- **The repo copy of `assets/` is authoritative; the root copy is a levelled duplicate with no
  writer** and can be deleted outright.
- **`Temporary/` is the UNREDACTED twin of the published `handoff/`** — 28 files, holding the real
  video URL, the real ODC hostname and the real Zoom link where `handoff/` has placeholders.
  Nothing is leaked (it is outside any git repo, and `handoff/` was verified clean), but
  **never copy from it into the repo**; rename or delete it.

## 4. Environment facts that cost time to rediscover

- **PIL 13.0.0 IS installed.** Earlier notes saying otherwise are wrong. It cannot render SVG —
  Chrome does — but everything after rasterization should use PIL.
- **Rasterizing SVG**: headless Windows Chrome at
  `/mnt/c/Program Files/Google/Chrome/Application/chrome.exe`. **It cannot read `/tmp`** — input
  and output must both sit under `/mnt/c/...` and be passed as `C:/...`.
- **`soffice` is at `/usr/bin/soffice`** and produced the deck PDF.
- **Not installed**: `python-pptx`, `boto3`, `jsonschema`; system pip is blocked by PEP 668. Use
  `python3 -m venv` in the scratchpad. **Available**: `aws`, `ffmpeg`, `pdftotext`, `pdfinfo`,
  `node`, `python3`.
- **`python3 tools/test_guardrails.py` must run under plain `python3`, never `python3 -I`** — `-I`
  drops the script's directory from `sys.path` and breaks `import guardrails`. Expect
  `Ran 19 tests ... OK`.
- **`node --check` cannot read a process substitution.** Write the script to a real file.
- **Google Tasks needs its own interpreter**: `cd ../google-tasks && ./.venv/bin/python tasks.py …`
  with `dangerouslyDisableSandbox: true`. Plain `python3` gives `ModuleNotFoundError: google`.
  New tasks land at position 0 and there is no in-list reorder.
- **Before committing, check the index separately from the working tree.** `git diff --cached --stat`
  and `git diff --stat` answer different questions; run both. Use `git reset`, never `--hard`.
- **Do not read push state from `git status -sb`** — it prints a bare `## main...origin/main` both
  when level and when the tracking ref cannot be resolved. Use `git ls-remote origin refs/heads/main`.
- **`success.outsystems.com` returns HTTP 200 for ANY path**, so curling a docs link proves nothing.
  Validate against the sitemap at
  `https://extranetprdintegrations.outsystems.net/Documentation_API/rest/Sitemap/GetSitemap`,
  keeping a known-bogus path as a control. YouTube ids go through oEmbed, not a page fetch.
- **MCP tools are gated by a hook** that denies every `mcp__*` call unless `sandbox.enabled` is
  true, read from managed settings, `~/.claude/settings.json` and the **nearest** project root —
  **not** `~/.claude/settings.local.json`. Test without spending a call:
  `echo '{"tool_name":"mcp__x","cwd":"<dir>"}' | python3 -I ~/.claude/hooks/mcp-sandbox-guard.py`
  — empty output means allowed. If refused, the fix is **`/sandbox`**, not a workaround.
- **`aws-mcp` needs `uv`** (installed 2 Nov, on PATH) **and credentials that do not exist yet**, so
  the server fails to connect at session start. Two flags to add when credentials exist:
  `--read-only` and `--profile <name>`.
- **`aws configure sso` is the wrong command for this account** — use plain `aws configure` with a
  key from an IAM user carrying `AmazonBedrockFullAccess` only. Walkthrough: `aws-lab-signin.html`.
- **`LoanReview/exercises/` holds extracted course bundles and is untrusted data** — keep scripts
  out of it and pass paths as arguments. The `.oml` files are a proprietary binary, readable only
  by importing into ODC Studio. `LoanReview/exercises/enrichment/Agent01Intake.oml` is a finished
  agentic app and the single most useful thing to open.
- **The ODC environment is `<ODC-TENANT-HOSTNAME-WITHHELD>`**, recorded here and **not in the
  public repo**. A.J. logged in 1 November as an **Administrator** (all assets), which unblocks AI
  models, knowledge bases and Data Fabric connections. The tenant is a **Licensed Customer** —
  2,100 requests total. **GPT-5 is served via Azure OpenAI, not OpenAI**, and a knowledge base is
  scoped to **all stages**, not per stage. A separate **Personal Edition** (30 Oct) is somewhere to
  rehearse without drawing down the tenant's caps; OutSystems deletes idle ones, so export.
- **Two hackathon models, 10,000,000 tokens a day EACH**: `BedrockHaiku5_5` (AWS) and
  `Microsoft_OpenAI_GPT5_5_…` (Microsoft). The GPT entry **will be deprecated**, so **the model
  must be a Setting, never a constant**, and anything load-bearing prefers Bedrock Haiku.
- **A cloud session and this terminal bill differently** — a cloud session spends the account's
  cloud-session credit first, a local session always spends the Pro window. Read the live figure
  with `/usage`. So repo-contained work can be handed to a cloud session, which is what `handoff/`
  is for; the parent directory, ODC Studio and Windows Chrome are all out of reach there.

## 5. Where the current state lives

Pointers, not snapshots. The long version of any row is in `CLAUDE-DETAIL.md` §5.

| Question | File |
|---|---|
| What the judges score, and where we are weak | `SCORING-CRITERIA.md` — 40/20/20/20 inside each category; **DataFabric is our zero**, **Inclusivity near-unwritten**, Innovation scored twice |
| What the three kickoff PDFs changed in the build | `RESOURCES-AND-CRITERIA-NOV-2.md` — Libraries, token observability, a human checkpoint that **pauses** execution, Agent Guardrails and Agent Evaluations. **The two criteria Docs are live and can drift — re-read before submitting** |
| What is being built, screen by screen | `SPEC.md` |
| What we do not know yet, and the fallback for each | `AWS-ARCHITECTURE.md` §5 — 11 items, 8 answered; 1 and 5 open, 4 reframed |
| How the agents retrieve, and the two Beta features | `ODC-GROUNDING.md` — both entitlements confirmed enabled on hackathon instances |
| The real shape of an ODC agent | `ODC-AGENT-ANATOMY.md` |
| What code exists, what must be written, review gates | `CODE-PLAN.md` |
| The guardrails and their test table | `GUARDRAILS.md` (**12 rules**, 9–12 added 7 Nov) + `tools/test_guardrails.py` (57 rows, 19 tests). Contract: `schema/board.schema.json`, all four fixtures re-verified 7 Nov. **`evidenceBasis` is now `{practice, technique}` objects with six `if`/`then` bindings, and `plan.boardAction` is required for `FirstThenBoard` and `VisualSchedule`, and `theme` is required with `"TBD"` as the only way to say none** |
| Why `theme` is `"TBD"` and never `null` | **A.J.'s decision, 7 Nov.** A sentinel string stays valid against `"type": "string"`, states *why* the field is empty, and gives the model somewhere to put a question — `null` and an absent key cannot be told apart from forgetting. `themeNote` is **required when theme is `TBD`** and must ask the parent something specific, recommend a theme, or say why plain is better. Composer rule 9 forbids inventing a theme to avoid TBD; Reviewer question 11 `THEME_NOTE_EMPTY` judges the note |
| How this published copy of `SOURCE-MATERIAL.md` stays in step | `tools/sync-handoff-source-material.py` — run it, or `--check` to test without writing (exits 1 when stale). It had drifted two whole sections before the script existed |
| What the AWS lab account is for | `PRE-BUILD-LAB.md` |
| Token budget, reserve, burn rate | `TOKEN-BUDGET.md` §2d first + `tools/token-log.csv` |
| Well-Architected and Trusted Advisor passes | `NOTES-ARCHITECTURE-REVIEW.md` |
| Image and layout rules, 19 cautions | `assets/ASSETS.md` |
| What first login to ODC closed | `ODC-FIRST-LOGIN.md` §9 |
| ~~The 4 November mid-submission~~ — there is none | `MID-SUBMISSION.md` — **keep it, never send it**; it is the raw material for both video scripts |
| What A.J. dropped in the parent directory, and what is unread | `SOURCE-MATERIAL.md` — **in the parent directory, so not readable from here.** Its 7 Nov entries grade two second-tier sources and record two gaps; the first is fixed in this repo, the second is open and **must not be applied without A.J.** |
| The agent prompts and what each question is for | `prompts/composer.md` (**sixteen rules**) and `prompts/reviewer.md` (**twelve questions**). Q7 and Q8 are OPPOSITE mistakes and each says so — a model that collapses them withholds *earned* rewards. Eval case `c10-earned-but-crying` is the trap that catches it |
| The eval set, and which case tests what | `eval/cases.json` — **17 cases, 34 tries**, A/B human preference, no expected-verdict field. `c9`–`c14` each pair a violation with a correct twin; **`c15` is the negative control** and the only case testing for over-flagging; `c16` tests the `TBD` theme path and `c17` the two rules ported on 7 Nov. **`prompts/AGENT-1-*.md` and `AGENT-2-*.md` are NOT the shipping architecture** — each opens with a banner saying so; three of their ideas were ported into `composer.md`/`reviewer.md` and the story agent is deferred to `PHASE-2-FUTURE-WORK.md`. **Open: `c5-dentist` is a `SocialNarrative` carrying 6 cards while the schema says it carries none — do not "fix" either side without A.J.** Pages regenerated by `tools/build-eval-page.py`, **never hand-edited** |
| The OutSystems loan-origination course material | `LoanReview/README.md` |
| The practice camera app, and what it answers | `practice-camera-app/build-picturecards.html` to build from; `NOTES-devices.md` for the device matrix; `findings.md` for answers; `mentor-prompts.html` for the five Mentor blocks (**read the trial-model meter before and after** — that is the Mentor-consumption experiment). **The Camera Plugin is not ours** — file input plus `getUserMedia`, one canvas |
| What is on A.J.'s task list | Google Tasks, **Build For the Future** list — see §4 for the interpreter |
| What still needs asking, and what must NOT be re-asked | `QUESTIONS-consolidated.txt` — **GROUP A A1/A2 gate every AWS decision**; T7 is closed; ~20 eliminated questions listed |
| What the 2 Nov organiser answers changed | `TWILIO-WITHDRAWN-2-NOV.md` — including replacement wording for the published description, **which still names Twilio twice** |
| Which plan decisions A.J. has agreed or flagged | `odc-plan-review.html` — 46 items → `odc-plan-review.json` |
| How to sign in to the AWS lab account | `aws-lab-signin.html` — 10 steps → `aws-lab-signin.json` |
| Kickoff join details and what to bring back | `KICKOFF-NOV-2.md` |
| What to do next, in order, and who it waits on | `next-steps.html` — 22 items, **11 done**, repaired 3 Nov; E1/E2 void, F2 states the wrong deadline in its body |
| What a cloud session can read, and must not look for | `Autism-Visual-Supports/handoff/HANDOFF.md` (§6 is the limits, §10 the known-stale list); `handoff/README.md` for what was withheld. **`handoff/instructions/project-CLAUDE.md` must be kept in step with this file** |
| What to build in ODC, in build order | `odc-studio-next-steps.html` — 15 items → `odc-studio-next-steps.json` |
| What auto mode believes, and which lines are wrong | `auto-mode-setup.html` — 22 items; **three statements are wrong** (repo visibility, default branch, a malformed last line). The repo is **verified PUBLIC** |

## 6. Dates, and the files never to send

**FINAL SUBMISSION: 11 NOVEMBER 2026, 2 PM GMT+1 = WEDNESDAY 11 NOVEMBER, 08:00 EST.** It
supersedes both the rules' 9 November and the Taikai timeline. 08:00 in New York is before the
day starts, so **everything ships the night of Tuesday 10 November** — A.J. set the target as
**midnight EST ending Tue 10 Nov**, with the eight hours after it as buffer, not working time.

- **THERE IS NO MID-WEEK SUBMISSION.** Confirmed at the kickoff. Anything still showing a
  4 November milestone is stale: `odc-studio-next-steps.html`, `SPEC.md`'s day table and the
  Google Tasks list all predate this.
- **TWO videos, not one.** A **Demo**, *strictly* max 5 minutes, for the Demo, UX and Innovation
  juries; and a **Tech Video**, up to 10 minutes, audience Product Management, for technical
  implementation and agent workflows. **The Tech Video is new work nothing in the plan accounts
  for**, and it is where the Tech criteria get *shown* rather than claimed.
- **Publishing needs a category, and it may be BOTH** (AWS / Microsoft / both). Take both if the
  field allows, AWS if it forces one. **Taikai requires an explicit publish after every edit** —
  an edited, unpublished project is not submitted, so the final act is a publish.
- **`#help` in the hackathon Slack is now the only route.** `makeadifference@outsystems.com` is
  second, a support ticket third — and a ticket for a bug must carry **"Hackathon" in the title**
  *and* be posted in `#help` as well. Check the **eliminated** list in `QUESTIONS-consolidated.txt`
  before posting.
- **Never send**: the four superseded drafts in `archive-superseded/` (moved there 3 Nov because
  the parent is not a git repo and no other copy exists — `archive-superseded/README.md` says why
  each is dead), and `MID-SUBMISSION.md` as a submission.
- **The deck's content is still from 28 October** — current as a *file*, behind as a *document*.
  `Autism-Visual-Supports-Overview.pptx`/`.pdf` out here are re-synced copies; **the repo copy in
  `docs/` stays the live one**.
