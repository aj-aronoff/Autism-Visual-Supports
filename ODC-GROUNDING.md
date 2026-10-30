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

In the agent itself the retrieval step has a name: **`GetGroundingData`**, part of the
`AgentTask` logic. The documentation says it can draw on internal aggregates, search
services for RAG, or external tools — so the box labelled *knowledge source* in our
architecture diagram is this one named step, and the two features above are two things
it can be pointed at.

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

**Every stage has its own files, its own storage and its own index.** Development, QA
and Production do not share uploads, and content does not carry over. The data source
*configuration* does. This is the one that bites silently: publish to the stage the
demo is recorded in, forget to upload there, and the Composer still answers — just
ungrounded, generically, and plausibly. **The board comes back looking fine.** So
uploading to the demo stage is a build-order item, and the check is to run one retrieval
in that stage and read the chunk that comes back.

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

## 4. The risk: both features are Beta

| | Knowledge bases | Semantic search |
|---|---|---|
| Status | Beta | Beta — released 9 March 2026 |
| How to get it | "Contact your OutSystems account team" | Same |
| Can we work around it in code? | No. It is an entitlement | No |

This is a different kind of unknown from open items 2–6 in
[`AWS-ARCHITECTURE.md §5`](AWS-ARCHITECTURE.md). Those are *how does this work*
questions, answerable by trying it. This one is a switch somebody else owns, and a
hackathon instance is exactly the sort of instance where Beta features may or may not be
turned on. **So it is a question to ask, not a thing to discover on day 3.**

One anecdotal caution, from the OutSystems forums rather than the documentation: a
developer reported the Semantic Search node vanishing from the ODC Studio toolbox
between releases. Treat it as unverified, and as a reason to confirm the feature is
present before building on it rather than after.

### The fallbacks, so neither answer stops the build

**If knowledge bases are unavailable:** the Composer's grounding moves into its system
prompt as a condensed rules digest. [`prompts/composer.md`](prompts/composer.md) is
already most of that document — it was written to state the TRIAD layout rules
explicitly rather than to rely on retrieval. We lose citation-to-source traceability,
which is a scoring loss on the evidence story, not a functional one.

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
