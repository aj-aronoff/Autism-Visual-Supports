# CORRECTIONS — what HANDOFF.md got wrong, measured 3 November 2026

**Written from inside a cloud container (`anthropic_cloud`), by running the commands rather than
predicting their results.** `HANDOFF.md` §6 was written before any cloud session had run. Five of
its claims are wrong. Three further corrections follow from checking the repo's state instead of
carrying it over from the previous session's notes.

This file is a standalone record. The same corrections exist as section-by-section edits to
`HANDOFF.md` in commit `04af29f`; **take one or the other, not both**, or the two will drift.

---

## 1. The pattern, which matters more than any single line

Every one of the five §6 errors runs the same direction: it **understated** what a cloud container
can do. The practical cost was not inaccuracy but misrouting — image regeneration, the deck, schema
validation and the organiser mail were all marked as A.J.'s work when four of them are doable by an
agent.

§14 of `HANDOFF.md` already states the rule this breaks: *measure rather than estimate, and when a
measured number contradicts a prediction, say so and find out why.* The file was exempting itself
from its own instruction.

---

## 2. §6 — five capability claims, corrected

Each row was checked by running something. The Chrome row was proven by **rendering the committed
diagram**, not by finding a binary: a present binary that cannot rasterize would be worse than an
absent one.

| §6 as written | Measured in the container, 3 Nov |
|---|---|
| "No Windows Chrome, so **SVG cannot be rasterized**" | **Wrong. Chrome is present and rasterizing works.** `/usr/bin/google-chrome`, Chrome for Testing 153.0.8010.12, plus Playwright's Chromium at `/opt/pw-browsers/chromium`. Rendering the committed `assets/trust-boundaries.svg` headless wrote a 1600×1200 RGBA PNG, 203,237 bytes. The Windows path in `ASSETS.md` is A.J.'s machine, not a requirement |
| "No `soffice`, so the deck cannot be re-exported to PDF" | **Wrong.** `/usr/bin/soffice` and `/usr/bin/libreoffice` are both present |
| "`python-pptx` … not installed" | **Wrong. Present, 1.0.2.** So the deck's `.pptx` source can be read and edited here — which matters, because §9 item 8 says the deck's content is still 28 October |
| "`jsonschema` … not installed" | **Wrong. Present, 4.26.0.** The board contract validates in the cloud; see §4 below |
| "No Gmail, Notion or Docs MCP, so the organiser mail cannot be re-read" | **Wrong. Gmail and Claude Docs MCP were both connected in this session.** The organiser mail can be re-read from the cloud when those connectors are attached. Check what the session actually has rather than assuming |

**What §6 got right, and what the real boundary is:**

- **No ODC Studio and no ODC Portal session.** Studio is a desktop application and the tenant needs
  an interactive login. This is the one real boundary, and the whole reason §12 exists.
- **No Google Tasks** — it needs `../google-tasks/tasks.py` with that directory's own
  `.venv/bin/python`, outside the repo.
- **No `boto3`** — measured absent, so no Bedrock call from the cloud even if credentials existed,
  which they do not.
- **The AWS lab account has nothing in it**, as measured 2 Nov. Unchanged.

So the corrected split is: **what does not travel to the cloud is ODC Studio, the ODC Portal,
Google Tasks, and anything that must reach Bedrock.** Everything else in this repo travels,
including every image regeneration and raster, the deck's PPTX and PDF, and the organiser mail.

---

## 3. §4 — the repo state was stale, and the push gap was unstated

**The commit it named was two commits behind.** §4 said `main = 832d563 … level with origin/main`.
The published tip is **`3813f83`**, measured with `git ls-remote origin main`, not carried over from
notes. `9382397` (the handoff snapshot) and `3813f83` (removing the unlisted concept-video URL from
the tracked tree) were both missing from the list.

**The cloud checkout has no remote and cannot push.** Nothing in `HANDOFF.md` mentioned this, and it
is the first thing a cloud session hits. In the starting checkout `git remote -v` is empty:

```
$ git ls-remote origin
fatal: 'origin' does not appear to be a git repository
```

So a cloud session can commit, report success, and **lose the work when the container is reclaimed.**
Attaching the repo (`add_repo`, push access) gives a second clone that does have `origin` and fetches
fine — but **attaching and pushing are separate permissions.** Push from this session was refused:

```
remote: Claude doesn't have GitHub access to aj-aronoff/autism-visual-supports
        for your organization
fatal: … The requested URL returned error: 403
```

**The rule: confirm push works before doing work in a cloud session that has to leave the
container.** The fix is to install the Claude GitHub App on the repository, or reconnect GitHub, at
`https://claude.ai/connect-github`.

---

## 4. §4 — one verification command should be two

`HANDOFF.md` offers a single check. Since `jsonschema` is present, the board contract can be verified
too, and it is the thing the three agents are judged against:

```
$ python3 tools/test_guardrails.py
Ran 19 tests in 0.003s

OK
```

Validate `schema/examples/*.json` with `Draft202012Validator` against `schema/board.schema.json`:

```
first-then-shoes-swing.json      VALID
INVALID-four-word-label.json     rejected — label pattern
INVALID-invented-practice.json   rejected — evidenceBasis enum
INVALID-no-then-card.json        rejected — cards contract
```

Each invalid example fails **for the reason its filename claims**, which is the part worth checking:
a schema that rejected all three for the same reason would pass a naive count and still be broken.
Use plain `python3` for the guardrail suite — **not `python3 -I`**, which drops the script's own
directory from `sys.path` and breaks `import guardrails`.

---

## 5. §9 item 1 — the scoring gap is wider than stated

§9 called the Inclusivity section "close to unwritten". It is **absent**:

```
$ grep -niE "inclusiv|contrast|touch target|WCAG|accessib" SPEC.md
$
```

Zero occurrences. The eight headings run from "The finding that shapes the build" to "Build order"
with no accessibility section among them. Against a **40% User Centered Design bucket** whose other
half — User Needs — is this project's strongest ground anywhere, it is the cheapest point available,
and it is pure document work, so a cloud session can close it.

---

## 6. What this unblocks

- **§9 item 8 — the deck's content is still 28 October.** With `python-pptx` and `soffice` both
  present, the deck can be edited and re-exported to PDF from the cloud.
- **§9 item 1 — Inclusivity.** Document work, no platform needed.
- **§9 item 7 — the Twilio box in the diagram: excluded from scope** as of 3 Nov. The Chrome finding
  still stands on its own; it simply no longer has that job to do.

Still genuinely A.J.'s: anything in ODC Studio or the Portal, the Google Tasks list, and anything
that must reach Bedrock. §12 is unchanged.

---

## 7. Provenance

Every figure above was produced by running a command in the container on 3 November 2026. The
guardrail suite, the schema validation, the SVG render, the `ls-remote`, the `grep` and the 403 are
all reproducible. Nothing here is estimated.

An HTML rendering of this record, in the house style of `handoff/next-steps/*.html`, is published at
`https://claude.ai/artifact/JbjuhH6CKXdYU5YCCKSGLS` (private to the repo owner's account).
