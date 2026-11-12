# Tech judging — criterion by criterion, with where to look

**A map for a judge with limited time, and a self-audit we are willing to publish.**
Each row says what the criterion asks, what this project actually does, where to verify it, and
an honest status. **Where we do not meet a criterion it says so**, because a checklist that only
claims successes is not evidence of anything.

Criteria are quoted from the kickoff slide of 2 November 2026.

---

## 40% — Agentic Automation & AI Capabilities

### *Agent Experience & Mentor: optimize and accelerate the development process* — **MET**

The application was not hand-written. It was built through **27 Mentor prompts in five blocks**,
and **every block ends with a confirm prompt** that asks the agent to read the app back and say
where it looked.

**That pattern is the point, and it earned its keep.** Three defects came out of confirm prompts
and none from looking at a screen: a unique index never created, three missing fields on a
reference table, and a mandatory flag never set. They were in what the agent did *not* say.

Two lessons we would hand to anyone doing this:

- **"That cannot be done in ODC" is worth exactly one challenge.** Twice we were told something
  was impossible and twice it was not; the second time the agent found the answer itself.
- **A read-back is a second reading, not a test.** An expression was described to us, we
  reproduced it from the description, and our own importer rejected the result. The application
  was fine — the description had been shortened. **Nothing is verified until something runs.**

**Verify:** `../mentor-build-prompts.html` · `evidence/README.md`

### *Agent Workbench: AI-driven decisions, routing, and tasks* — **NOT MET**

We opened it and built nothing in it. Routing decisions in this app are flow logic, not Workbench
artefacts. **Stated rather than glossed.**

### Multi-agent, which the slide names here — **MET**

Two agents run on every request. The **Composer** drafts; the **Reviewer** asks fifteen questions
a validator cannot answer and **has no tools and cannot edit anything** — a reviewer that can edit
stops reporting. Its verdict gates the approve step, never the save.

**Verify:** `prompts/composer.md`, `prompts/reviewer.md` · `evidence/11`, `evidence/26`

---

## 20% — Enterprise Connectivity & Data Integration

### *DataFabric Integration* — **NOT MET**

**This application does not use DataFabric.** It holds its own data in ODC; there was no second
system to unify, so there was nothing to federate and we did not invent a reason to.

What we did instead is close the surface: **every entity is private, and the only way in is a
service action**, because an action can validate and an entity cannot. One caveat we would pass
on — in this version **every service action is public by nature**, and making one private raises a
validation error. So "expose only service actions" does not give you a private surface. The
accurate sentence is that the entities are private and every entry point enforces its own rules.

---

## 20% — Contextual Intelligence & Grounding

### *Knowledge Base: ingest / structure data* — **MET**

**Two knowledge bases, deliberately separate**, because chunking is immutable per base and the two
documents are different shapes: the Vanderbilt TRIAD toolkit for how a support is laid out, and a
National Standards extract for which practice it rests on.

**The ingestion is licensed, not assumed.** The TRIAD toolkit's own credits permit distribution as
an electronic file at no cost, which is what allows these documents to sit in a knowledge base at
all. The source documents themselves are **not** in this repository.

### *Semantic Search: agents retrieve accurate and nuanced information* — **MET, with one gap**

Both bases are queried on **every** call, before the prompt is built. **The agent never retrieves
— it is handed passages.** The two queries are different by design: the layout base is queried
from the parent's own words, the evidence base from a fixed practice vocabulary.

**That distinction is the finding worth your time.** Querying the evidence base with the parent's
paragraph scored **0.167** and was rejected, so a board named three practices with nothing behind
them. We did not lower the threshold — a reference table of treatment names will never match a
narrative. Changing the query took it to **0.737**. The minimum score ships at **0.25**, set from
scores observed rather than chosen.

**Not built:** semantic search over the card library, so that *sneakers* finds *Shoes*.

**Verify:** `evidence/05-retrieval-scores.md`, `evidence/06-retrieval-attributes.txt`

---

## 20% — Modular Architecture, Governance and Security

| Sub-point | Status | What is actually there |
|---|---|---|
| **Logic Isolation** | **MET** | The Web and Agentic apps are split; entities are private and reached only through service actions |
| **Multi-Agent** | **MET** | Composer and Reviewer, both running on every request |
| **Human-in-the-Loop** | **PARTIAL — and we are careful about this** | A board saves as a **Draft**. Nothing becomes an in-use board without a separate approve call, and that call is the **only** place in the application that sets the status, verified by inspecting every action. **But nothing pauses** — an ODC service action runs to the end. It is a checkpoint in two calls, not a paused workflow, and we will not describe it as one |
| **Real-time Observability** | **WEAK** | Token usage is logged per request but the counts currently write zero, so the provider's own usage meter is the instrument we actually read. Stated rather than dressed up |
| **Forge Acceleration** | **NOT CLAIMED** | Seven libraries arrived with the agentic app template and **none of them is called**. Claiming acceleration we did not get would be false |

### Governance that is code rather than prompt wording — **MET, and this is the strongest part**

- **The safety rule runs first.** Self-injury or escalation in a parent's text returns referral
  guidance instead of a board, before any retrieval and before the model is called. It costs zero
  model tokens, and it fired in production.
- **An ungrounded answer says so.** If either base returns nothing, the flow stops before the
  model is called. Rule seventeen is a step in the flow, not a line in a prompt.
- **Parsing refuses before it extracts.** Thirty-eight checks; on failure it writes nothing and
  names the check that failed.
- **Citations are assembled in code**, from each passage's own attributes, and the model copies
  them. A re-runnable audit shows **zero fabrication**.
- **Non-affirming language** is twelve phrases mapped to replacements, in code, before a save.
- **There is no gender field in the `Child` entity.** A theme cannot be keyed on a child's sex
  because the data model does not permit it — a schema guarantee, not a policy.
- **The referral text has its own unit test**, asserting it contains no "diagnos", no "disorder",
  no "you should", no "probably". A test that fails if the software starts sounding like a
  diagnosis.

**Verify:** `tools/guardrails.py`, `tools/test_guardrails.py`, `schema/board.schema.json`,
`evidence/02`, `evidence/08-audit.py`

---

## The two things we would want a technical judge to check

1. **Run the audit.** `python3 evidence/08-audit.py` is re-runnable and checks every citation in a
   board against the passages the model was actually given.
2. **Read what the directory says it does *not* prove.** `evidence/README.md` has a section for
   that, and it is the part we would read first if we were judging.
