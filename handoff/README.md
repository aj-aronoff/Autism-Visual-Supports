# handoff/ — a redacted snapshot for a cloud Claude Code session

Published **3 November 2026** so a session that only has this repo can take over. Start with
`HANDOFF.md`.

**This is a sanitized copy.** Six categories of value were stripped and replaced with visible
`<...-WITHHELD>` placeholders — the ODC tenant hostname, the unlisted concept-video link,
the kickoff Zoom joining details and recording link, and local filesystem paths. `HANDOFF.md`
§11 has the table. Ask A.J. for any value you actually need; never guess one, and never commit
one here.

## Withheld entirely, and why

| Not published | Reason |
|---|---|
| `KICKOFF-NOV-2.md` | Zoom link, meeting ID, passcode and a dial-in number. The kickoff is over and its outcomes are in `state/SCORING-CRITERIA.md` and `state/RESOURCES-AND-CRITERIA-NOV-2.md` |
| `DO-NOT-PUBLISH.md` | It is an index *of* the secrets. Its rules survive in `HANDOFF.md`; its values do not belong in a public repo |
| `global-CLAUDE.md` | A.J.'s personal machine preferences and local paths — not project material |
| `auto-mode-setup.html` | Describes the sandbox and permission configuration of A.J.'s machine |
| `aws-lab-signin.html` | A walkthrough for A.J.'s personal AWS account |
| `rules.txt`, `faq.txt`, `prizes.txt`, `Hackathon-announcement.txt` | Verbatim organiser-issued documents. Ours to read, not to republish — and they carry organiser contact addresses |
| `MID-SUBMISSION.md`, `project-description*.md` | Already in this repo at the root and in `docs/` — a second copy would drift |

## One pre-existing exposure, flagged not fixed

`MID-SUBMISSION.md` in the repo root carries the **unlisted** concept-video URL in plain text.
It was introduced by commit `6b9ab52` ("Add the 4 November mid-submission document"), well
before this handoff, and is not something this snapshot added — the copy here is redacted.
`CLAUDE.md` treats that video as link-only by choice, so the root file contradicts it.
**Removing it from the current file does not remove it from git history**, so the realistic
options are to accept it or to re-issue the video with a new URL. A.J.'s call.
