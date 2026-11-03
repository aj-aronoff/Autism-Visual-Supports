# Grounding, and the two ODC features that provide it

Read 29 October 2026 against the ODC documentation. Companion to
[`SPEC.md §5`](SPEC.md) and [`AWS-ARCHITECTURE.md §1.4`](AWS-ARCHITECTURE.md).

---

## 1. Two features, two different jobs

[`SPEC.md §5`](SPEC.md) has used the phrase *"knowledge source"* since the spec was
written, as a placeholder for however ODC turns out to do retrieval. It turns out to do
it two ways, and the design needs **both**, for two unrelated reasons.

| Feature | Indexes | Serves | Our use |
|---|---|---|---|
| **Knowledge bases in ODC** | Documents you upload in the ODC Portal | The Composer's clinical grounding | The TRIAD toolkit, as a PDF |
| **Semantic search in ODC apps** | Attributes of your own entities | The Illustrator's reuse check | `CardLibrary.Label`, searched by meaning |

Both are **Beta**. Both say the same thing: *contact your OutSystems account team* to
enable them. That is §4 below, and it is the only part of this document that is a risk
rather than a plan.

In the agent itself the retrieval step has a name: **`GetGroundingData`**. The
documentation says it can draw on internal aggregates, search services for RAG, or
external tools — so the box labelled *knowledge source* in our architecture diagram is
this one named step, and the two features above are two things it can be pointed at.

### The four documented grounding sources

Read 30 October against the *AI integration* overview, which is where ODC states the
full list. It is four, not two, and the two features above are only the first and second:

| Source | What it is | Us |
|---|---|---|
| Your app's **entities** | Aggregates over your own data | `CardLibrary`, via semantic search |
| An **AI search service** | An external index, connected in Data Fabric | The §4 fallback, now documented rather than inferred |
| An **MCP server** | Documented under *Tools and connectors* | Not needed — our tools are ODC server actions |
| An external **REST API** | Any endpoint | Not needed |

The AI search service being named here, as one of four first-class grounding sources,
is what moves the §4 fallback from *a phrase we read into* to *a supported path*. The
sidebar carries a whole page on *Adding search services* alongside *Adding AI models*.

**The naming is settled: it is `AgentFlow`.** This page says `AgenticFlow` and our 29
October reading said `AgentTask`; the course exercise shows the actual scaffold, and
`GetGroundingData` and `BuildMessages` are server actions inside an `AgentFlow` server
action in an `AgentFlows` folder, entered through a `Call<AgentName>` service action. See
[`ODC-AGENT-ANATOMY.md §1`](ODC-AGENT-ANATOMY.md).

**And grounding turns out to be simpler than this document assumed.** The documented
pattern is an Aggregate over your own entities, a **JSON Serialize**, and the result
pasted into the system message. That makes passing `CardLibrary` rows as JSON the
*canonical* approach rather than a fallback, which lowers the stakes on open item 9
considerably — see [`ODC-AGENT-ANATOMY.md §3`](ODC-AGENT-ANATOMY.md).

The same page names **Amazon Bedrock, Azure OpenAI and Databricks** as example model
providers. Bedrock being first on that list is weak evidence for open item 3, not an
answer to it.

### Serialize a projection, not the entity

The *Ground data for AI agent* lesson (watched 30 October) gives three rules and calls the
second one *"a critical optimization problem that directly affects your budget"*: assign
**only the essential attributes** into a structure and serialize that. The exercise then
breaks its own rule by serializing a whole aggregate result.

For us the rule has teeth. A `Child` carries a routine history; a board needs one routine.
**Every `GetGroundingData` we write serializes a purpose-built projection structure**, and
the review question in `CODE-PLAN.md` §5 for stage A is simply: name every attribute in the
projection and say why the model needs it. The other two rules are stick to the facts, and
re-read the record at agent time rather than passing a copy forward — which matters here
because the Workflow hands an identifier between agents, not a payload, so each agent
re-reads. That is the right default and we should not optimize it away.

## 2. The Composer's grounding: a knowledge base

**The corpus is two PDFs we already hold.** No extraction, no retyping, no reformatting.

| File | Size | Limit | Text layer | Fit for RAG |
|---|---|---|---|---|
| `Visual_Supports_Tool_Kit.pdf` | 1.1 MB | 20 MB | Yes — 15,899 characters in the first three pages | **Good.** Dense prose, discrete layout definitions |
| `Coaches Strategies Autism.pdf` | 8.8 MB | 20 MB | Yes — but only 1,046 characters in three pages | **Thin.** A slide deck; chunks will be mostly headings |

So the TRIAD toolkit is the knowledge base. The National Standards Report material
arrives better as the `EvidencePractice` static entity it already is in
[`SPEC.md §3`](SPEC.md) — eleven rows with citations is a lookup, not a retrieval
problem, and a static entity cannot hallucinate a twelfth practice.

Supported types are PDF, `.docx`, `.pptx`, `.html`/`.htm`, `.txt`, `.md` and `.csv`;
files cannot exceed **20 MB**, and the documentation states no limit on how many.
Scanned, image-only pages are supported for English and Chinese only — ours is English
and has a real text layer, so this does not apply, but it is the check to run on any
source we add later.

### Three facts that would each cost a day

**Chunking is set at creation and cannot be changed afterwards.** The knowledge base is
therefore a one-way decision, which is exactly the kind of decision not to make in a
hurry on day 3. Mitigation: files are unlimited in number, so create **two** knowledge
bases over the same toolkit with different chunking, run the
[`eval/cases.json`](eval/cases.json) set against both, and keep the one that retrieves
the right layout definition. Reconfiguring costs a rebuild; comparing costs an hour.

**~~Every stage has its own files, its own storage and its own index.~~ Corrected 1
November, from the Create knowledge base wizard itself**, which states: *"Each knowledge
base is scoped to **all the stages** in the organization."* That is the opposite of what
this section said, and it removes what was described here as the one trap that bites
silently.

Two things keep it from being a free pass. The wizard's wording is UI text from one
release, and the failure it would mask is silent — an ungrounded Composer does not error,
it answers plausibly and the board comes back looking fine. So **run one retrieval in the
demo stage and read the chunk that comes back** regardless; it costs a minute and it is
the only way to tell grounded from fluent. And the point is largely moot for this
submission anyway: this environment has exactly **two stages, Development and
Production** (confirmed 1 Nov, both US East (N. Virginia)), and **trial models exist only
in the Development stage** — so the demo runs from Development, and nothing has to cross
a stage boundary.

**Search quality is best in English**, which is what we have.

## 3. The Illustrator's reuse check: semantic search

This is the one that changes a design decision rather than confirming one.

`SearchCardLibrary` in [`SPEC.md §5`](SPEC.md) was going to be a label match. A label
match fails precisely where the feature matters: a parent who types *sneakers* does not
hit the existing **Shoes** card, so a second image is generated for the same activity.
That is a clinical failure before it is a cost one — [`SPEC.md §3`](SPEC.md) keeps
`CardLibrary` so that *a given activity keeps the same picture forever*, and a child who
is shown two different pictures for shoes has been given two different cards.

Semantic search over `CardLibrary.Label` is the fix: *sneakers*, *trainers* and *shoes*
are near each other by meaning, which is the whole point of vector retrieval. It is also
the cheapest possible win against the image budget in
[`TOKEN-BUDGET.md`](TOKEN-BUDGET.md), because every hit is an image not generated.

**How it indexes, and the two consequences:**

- **At publish**, publishing creates the embedding schema and the database triggers.
  Indexing time grows with the volume of data.
- **At runtime**, a create, update or delete on a searchable entity updates its
  embeddings **asynchronously**. Changes appear in search results once processing
  finishes — not immediately.
- **A full reindex** fires when semantic search is first enabled on an attribute, and
  again whenever that attribute's chunking configuration changes.
- **Indexing requests are rate-limited per tenant.** The documentation's own advice is
  to load large datasets before production, so indexing completes before anyone
  searches.

Consequence one: **the 40-card seed goes in early**, not on demo day.
[`assets/cards/MANIFEST.csv`](assets/cards) is ready with 201 rows, and loading it on day 3 means the
library is indexed long before the Illustrator first queries it.

Consequence two: **the demo must not create a card and then immediately search for it.**
Asynchronous indexing means that sequence can legitimately miss. The demo script
searches for cards that were seeded, which is also the honest story — reuse is a library
behaviour, not a within-the-minute one.

Chunking choices here are per attribute: **smart chunking** (the default; recursive with
default separators), **fixed-size** (maximum characters plus overlap), **sentence-based**
(sentences per chunk, plus a maximum and an overlap), and **recursive** (character limits
and overlaps, splitting on a hierarchy of delimiters). For a field validated to three
words, this is close to moot — smart chunking on a 20-character label produces one
chunk — which is worth knowing mainly so we do not spend time tuning it.

Indexing has no status API. The only visibility is **Logs** under **Monitor** in the ODC
Portal, searching for **`Embedding sync`**; full reindex start and completion are logged,
and runtime changes are not.

## 4. The risk that closed: both features are Beta, and both are on

**Answered 30 October 2026.** Asked in the hackathon Slack; OutSystems replied:

> *"Yes, both are enabled in the the hackathon instance automatically, you dont need to do
> anything"*

— Snezana Djurisic, OutSystems. That closes open items 8 and 9 in
[`AWS-ARCHITECTURE.md §5`](AWS-ARCHITECTURE.md), and it closes them in the one way we could
not close ourselves: these were entitlements, not puzzles.

**So the primary design is the design.** The Composer is grounded in a knowledge base over
the TRIAD toolkit (§2) and the Illustrator's reuse check uses semantic search over the card
library (§3). Nothing below is the plan any more. Two things survive from it:

1. **Verify on first login anyway.** A platform answer is about entitlement; it is not a
   guarantee that the Semantic Search node is in the toolbox of the release we get. The
   forum report below is why. Checks 6 and 8 in `ODC-FIRST-LOGIN.md` stay — they now take
   a minute and confirm rather than decide.
2. **Keep the fallbacks written down.** If either feature misbehaves mid-build, day 5 is
   the wrong time to design a replacement. They are recorded below, demoted to contingency.

The original risk assessment follows, kept because it is the reason the question got asked
at all rather than discovered on day 3.

### What the risk was


| | Knowledge bases | Semantic search |
|---|---|---|
| Status | Beta | Beta — released 9 March 2026 |
| How to get it | "Contact your OutSystems account team" | Same |
| Can we work around it in code? | No. It is an entitlement | No |

This was a different kind of unknown from open items 2–6 in
[`AWS-ARCHITECTURE.md §5`](AWS-ARCHITECTURE.md). Those are *how does this work*
questions, answerable by trying it. This one was a switch somebody else owned, and a
hackathon instance is exactly the sort of instance where Beta features may or may not be
turned on. **So it was a question to ask, not a thing to discover on day 3** — and asking
it on 29 October is what bought an answer overnight, three days before the kickoff.

One anecdotal caution, from the OutSystems forums rather than the documentation: a
developer reported the Semantic Search node vanishing from the ODC Studio toolbox
between releases. Treat it as unverified, and as a reason to confirm the feature is
present before building on it rather than after.

### The fallbacks — contingency now, not plan

**If knowledge bases are unavailable:** the Composer's grounding moves into its system
prompt as a condensed rules digest. [`prompts/composer.md`](prompts/composer.md) is
already most of that document — it was written to state the TRIAD layout rules
explicitly rather than to rely on retrieval. We lose citation-to-source traceability,
which is a scoring loss on the evidence story, not a functional one.

**A better fallback than the digest: a Data Fabric AI search connection.** Read 30
October against *Create connections to external data sources*. Data Fabric connections
are not only external databases — the provider list includes three **AI search
services**: **Azure AI Search**, **Amazon Kendra** and a generic **Custom search
service** (endpoint plus one header name and value). The `GetGroundingData` step is
documented as able to draw on *"search services for RAG"*, and this is what that phrase
points at. So if the knowledge base entitlement is off, retrieval does not have to
collapse into a prompt digest — it can move to an index we build ourselves.

| Option | Cost on a 7-day build | Verdict |
|---|---|---|
| **Azure AI Search, Free tier** | One free service per subscription, 50 MB storage, 3 indexes, 16 MB source-file cap. The toolkit PDF is 1.1 MB | **The one to try.** Free tier has **no semantic ranking**, which is the quality feature we would want, so test retrieval against `eval/cases.json` before committing |
| **Amazon Kendra** | 750 hours free in the first 30 days, then **$1.125/hour** for Basic Developer Edition — about $810 a month, **billed on a provisioned index even when it is empty and unqueried** | **No.** Against the deliberately-low $25 lab budget in `PRE-BUILD-LAB.md §3`, one index left running overnight is most of the budget. The Kendra documentation landing page also says it is no longer open to new customers, which contradicts the pricing page |
| **Custom search service** | Our own endpoint — a Lambda Function URL on the lab account | Possible, but it is new code in week one, and `CODE-PLAN.md §3` has no room for it |

Two caveats before treating Azure AI Search as settled. It needs somewhere to run: the
hackathon provides Microsoft AI services, but whether Azure AI Search counts as one of
them is not stated anywhere we have read, and a personal Azure free account's $200 credit
runs 30 days. And **creating any connection requires administrator rights** — see below.

**Connections are administrator-only.** Managing them needs the *Configure Connections*
and *Connection Management* permissions, and by default only administrators have them.
Knowledge bases are managed in the Portal too. So a single question — *am I an
administrator of my own hackathon environment?* — decides whether either the knowledge
base or this fallback is reachable at all. It is now check 1 in
[`ODC-FIRST-LOGIN.md`](ODC-FIRST-LOGIN.md).

**Connections confirm the per-stage rule from §2 above**, and sharpen it: a connection is
configured per stage, with an explicit **Apply to all stages** button, and the
documentation states that an app and its connection information must be in the same
stage. Configuration carries; content does not. The button is why the distinction is easy
to miss.

**If semantic search is unavailable:** `SearchCardLibrary` falls back to a normalised
label match — lowercase, stem, strip articles — plus a short hand-written synonym table
for the cases that actually recur in a child's life: shoes/sneakers/trainers,
car/van/auto, tablet/iPad. Thirty lines of static data recovers most of the hit rate at
the cost of being unable to generalise. The library-first *gate* survives either way,
which is the part the budget depends on.

## 5. One regional note for the architecture

In Cape Town, Hong Kong, Jakarta, Singapore, Tel Aviv and the UAE, both features route
search requests through the European region (`eu-central-1`) for processing, because the
embedding model is not deployed there. Storage stays in the local region.

For us this is a footnote and not a problem — we need a US region anyway, which is
already open item 7. But it is a boundary fact: in those regions, query text crosses a
region boundary on its way to the embedding model. Since the Composer's query is built
from the obstacle text a parent typed, that text is the thing crossing. Worth one line in
[`AWS-ARCHITECTURE.md`](AWS-ARCHITECTURE.md) §B5 rather than a decision, since the
provisioned region is not ours to choose.

## 6. What changes in the build order

| Day | Was | Now also |
|---|---|---|
| 3 | Entities and static entities | Create the knowledge base, upload the toolkit, enable semantic search on `CardLibrary.Label`, seed the 201 cards |
| 3–4 | Composer + Reviewer | Point `GetGroundingData` at the knowledge base; compare the two chunkings against the eval set |
| 5–6 | Illustrator, card library reuse | Reuse now means a semantic hit, so the test is *sneakers* finding **Shoes** |
| 8 | UX pass | Confirm the knowledge base exists **in the stage the demo is recorded in** |

---

*First → Then. Print it, post it, trust it.*
