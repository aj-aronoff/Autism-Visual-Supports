# First login to the ODC environment

The environment was created on **30 October 2026**, three days before the kickoff. That
matters more than it sounds: seven of the eleven open items in
[`AWS-ARCHITECTURE.md §5`](AWS-ARCHITECTURE.md) were filed as *"resolve at kickoff"*
only because there was nothing to look at. Now there is. Each one below is a thing to
look at, the item it closes, and the fallback that was already written in case the
answer is bad — so a bad answer costs an hour of re-planning, not a day of the build.

Companion to [`PRE-BUILD-LAB.md`](PRE-BUILD-LAB.md), which does the same job for the
personal AWS lab account. The environment hostname is not recorded in this repo; it is
in the project `CLAUDE.md`, which is deliberately outside it.

---

## 0. Finish the user setup first

The email gives five steps, and step 3 issues a **verification code that expires**. If
the code lapses, start again at *Configure Password* and request a new one — the account
itself is already created and does not need re-requesting.

Set a password that is in the password manager before it is typed anywhere. This is the
only credential for the submission; there is no second route in.

---

## 1. Nine things to look at, in this order

| # | Look at | Closes | Fallback if the answer is bad |
|---|---|---|---|
| 1 | **Whether you are an administrator** — Portal → **Management**, which holds organization, subscription, access and settings | gates 5, 6, 7 and the §6 fallback — *managing AI models uses the same permissions as managing connections* | A request to OutSystems — nothing in our control recovers it |
| 2 | **How many stages the environment has** — Portal → Environments | — | See §2 |
| 2a | **Whether the organization is multi-portfolio**, and whether we are in the **main** portfolio | **gates the trial models themselves** — see §8 — plus app reuse and the §6 connection | None. Without the main portfolio there are no models |
| 3 | **Which region it is provisioned in** | Item 7 | US region required; a non-US region also triggers §3 |
| 4 | **Whether `Agentic` is one of the app types** in Create App — the four are Web, Mobile, Agentic, Library | Item 2 | Three server actions against the JSON contract in `SPEC.md §5` |
| 5 | **`INTEGRATE > AI models`** — which are added, and whether the **Provider** tab is available as well as **Trial** | Item 4 | Cards + photo upload, which is now the plan either way |
| 6 | **That Knowledge bases exists as a section**, and that a file can be uploaded | Item 8 — **already answered yes**, so this is confirmation, not discovery | A Data Fabric AI search connection — see §6 — then a prompt digest |
| 7 | **The Trial Model details page** — which row applies to us, **Licensed Customers or Personal Edition**, plus consumption to date | Items 6 and 11 | Plan against the Licensed row, the tighter of the two |
| 8 | **Install ODC Studio** — downloaded from the top right of the Portal — **and sign in**, then check that **Create → Agentic app** and **Create → Workflow** both appear | Items 1, 9 | Secret path segment + body token (weaker) for item 1 |

Nothing here requires publishing anything. Do not publish to a Production stage during
these checks — see §2 for why.

**Check 1 first, because it gates three of the others.** Knowledge bases and Data Fabric
connections are both managed in the Portal, and connections need the *Configure
Connections* and *Connection Management* permissions, which by default only
administrators hold. If the hackathon issues developer-level users, the grounding story
needs a request to OutSystems rather than a workaround — and a request takes days, which
makes this a Friday question and not a Monday one.

## 2. The stage count is the one that bites silently

[`ODC-GROUNDING.md §2`](ODC-GROUNDING.md) records that **every stage has its own
knowledge base files, its own storage and its own index**, and that the data source
*configuration* carries between stages while the content does not. An ungrounded
Composer does not fail. It answers plausibly, out of the model's own weights, with no
error anywhere.

So the stage count decides how much care day 3 needs:

- **One stage (Development only).** The trap cannot fire. Upload once.
- **Two or three stages.** The toolkit PDF has to be uploaded into *the stage the demo
  runs from*, and the eval set has to be run against that stage. Pick the demo stage now
  and write it into the build order rather than discovering it on 8 November.

## 3. The region note that is easy to miss

Semantic search queries from Cape Town, Hong Kong, Jakarta, Singapore, Tel Aviv and the
UAE are routed through `eu-central-1` for retrieval. If the environment is provisioned in
one of those, the Illustrator's reuse check crosses a region boundary that the trust
diagram does not currently draw, and `AWS-ARCHITECTURE.md §B5` needs a row.

## 4. One item that looking cannot resolve

**Items 8 and 9 were the two that looking could not resolve, and they are now answered
without looking.** OutSystems confirmed in the hackathon Slack on 30 October that
knowledge bases *and* semantic search are **enabled automatically on hackathon
instances** — *"you dont need to do anything."* Both checks stay in §1, demoted to
confirmation: an entitlement being granted is not the same as the Semantic Search node
being present in the toolbox of the release we are given, and `ODC-GROUNDING.md §4`
records a forum report of exactly that node disappearing between releases.

**Semantic search is a setting on an entity attribute in ODC Studio**, not a section in
the Portal, so it is visible only once Studio is installed and a module is open — which
is why it rides along with check 8 rather than standing on its own.

**The token allocation itself** — the number, whether it is per team or per participant,
and what happens at exhaustion — is not discoverable from inside the environment. That
stays a question for a human, and it is question 5 in `email-4-kickoff-questions.txt`.

## 5. What the email itself already answered

Question 4 of the kickoff email asked *"when do credentials arrive?"* and argued that
half a day lost on 2 November is material with a seven-day window. ODC access, at least,
arrived early. The AWS and Microsoft AI tokens and Twilio are still unaccounted for, and
the Twilio one is the one with a lead time: a trial project can only send SMS to numbers
verified in advance, which is a thing to discover this week and not on 8 November.

The email came from a named Developer Advocate at OutSystems. That is a better-targeted
reader for *"is Agent Workbench enabled on the hackathon instances"* than a shared
mailbox, and replying in that thread does not require finding an address.

## 6. If knowledge bases are not entitled, check 6 is not the end of it

Data Fabric connections are not only external databases. The provider list includes three
**AI search services** — Azure AI Search, Amazon Kendra and a generic Custom search
service — and `GetGroundingData` is documented as able to draw on a search service for
RAG. So a missing knowledge base entitlement does not force the Composer back onto a
prompt digest. [`ODC-GROUNDING.md §4`](ODC-GROUNDING.md) compares the three on cost:
Azure AI Search's Free tier is the one to try, Kendra bills about $810 a month on a
provisioned index **even when it is empty and unqueried** and is ruled out, and a custom
endpoint is new code `CODE-PLAN.md` has no room for. Creating any of them needs check 1.

## 7. Two things the getting-started page settles, and one it opens

**Check 4 is now a yes-or-no on a menu.** ODC offers four app types at creation — Web,
Mobile, **Agentic**, Library — and the documentation carries a page called *Getting
started with an Agentic app*. Open item 2 is therefore answerable by opening the Create
App dialog, and the guide A.J. asked OutSystems for in question 4 of
`email-4-kickoff-questions.txt` exists; it is in the documentation rather than the
training catalog, which is where he looked.

**1-Click publish targets the Development stage by default**, which is the benign case
for §2: the stage that gets published is the stage to upload the knowledge base into,
unless we deliberately promote.

**The open one: Mentor.** Mentor Web generates an app from a prompt in the Portal and
Mentor Studio assists inside ODC Studio. Both would save real time in a seven-day solo
build, and both are ODC features, which scoring criterion one rewards. But both are
model-backed, and nothing we have read says whether they draw on the same metered
allocation as our three agents. If they do, scaffolding spends the board budget. That is
now question 6 in [`TOKEN-BUDGET.md §8`](TOKEN-BUDGET.md).


## 8. The trial models, and why check 2a outranks everything

ODC ships three ready-to-use **trial models** in every tenant, in the **development
stage**: GPT-5 via OpenAI, Claude Haiku 4.5 via Amazon Bedrock, Amazon Nova Pro via
Amazon Bedrock. That answers open item 3 — Bedrock is native, the Forge connector is off
the critical path — and it settles the image question: none of the three emits images.

**But in a multi-portfolio organization, trial models exist only in the main portfolio.**
If this organization is multi-portfolio and our apps are not in the main one, there are no
models available to us at all. Not a slower path or a smaller quota — none. Every other
check on this sheet has a fallback; that one does not, which is why it sits at 2a and why
it is worth two minutes before anything else.

The limits are a **total allowance, not a time window**, and reaching one *prevents
further use of the model*. The numbers are on the **Trial Model details** page, which is
also where consumption to date is shown — so check 7 is a page to read and screenshot,
not a yes-or-no. Those numbers are the input to `TOKEN-BUDGET.md §3`, whose ~3.8M-token
build estimate is currently sized against nothing.

---

*First → Then. Print it, post it, trust it.*
