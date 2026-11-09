# What an ODC agent actually looks like

Read 30 October from the *Build the intake agent* exercise in the **Build your first
agentic-powered app** journey. That exercise builds a loan-intake agent; nothing here is
about loans. It is the first material we have seen that shows the **shape** of an ODC
agentic app rather than describing it, and it settles four things we had open and changes
two decisions.

Companion to [`ODC-GROUNDING.md`](ODC-GROUNDING.md) and [`CODE-PLAN.md`](CODE-PLAN.md).

---

## 1. The four nested actions, and their real names

The naming question in `ODC-GROUNDING.md §1` — `AgentTask` or `AgentFlow` or
`AgenticFlow` — is settled. **It is `AgentFlow`**, a server action in an `AgentFlows`
folder, and the scaffold nests like this:

```
Call<AgentName>            service action — the entry point, called from outside the app
  └── AgentFlow            server action, in the AgentFlows folder
        ├── GetGroundingData   server action — retrieval
        ├── BuildMessages      server action — assembles the model request
        ├── LoadMemory         server action — scaffolded, deletable
        └── StoreMemory        server action — scaffolded, deletable
```

An agentic app is created in ODC Studio from **Create → Agentic app**, and **the AI model
is chosen at creation**. The exercise's choice is `TrialClaudeHaiku4_5` — the same model
[`TOKEN-BUDGET.md §3`](TOKEN-BUDGET.md) picked on cost and rate limits, which is a useful
independent confirmation.

Memory is opt-out. The exercise deletes `LoadMemory`, `StoreMemory` and
`AppendMemoryToMessages` for a stateless agent, with a reason that applies to us exactly:
*"we don't want the data uploaded from the intake agent contaminated by previous
memory."* Our Composer must not carry one child's routine into another child's board, so
all three come out.

## 2. Open item 10 is answered, and the answer is better than any of our three options

[`CODE-PLAN.md §8`](CODE-PLAN.md) worried that the Web app and the Agentic app would
depend on each other. In the exercise **they do not**, and the mechanism is the part we
had not accounted for:

| Direction | How | What it means |
|---|---|---|
| Agentic **→** Web | `Add public elements`, selecting the consumer app's entities *and* its `SetIntakeAgentDecision` service action | A normal one-way weak dependency |
| Web **→** Agentic | **It does not exist.** The Web app raises an **Event** (`NewCustomerLoan`) and knows nothing about any agent | No cycle to permit |
| The join | An **ODC Workflow** listens for the Event and calls `Call<AgentName>` | The orchestrator is a third thing |

**So the architecture is: consumer app raises an event → Workflow orchestrates → agentic
app writes results back through a service action the consumer app exposes.** The consumer
app never references the agent. That is event-driven decoupling, and it is strictly better
than options A, B and C in `CODE-PLAN.md §8`, all three of which assumed a direct call.

### Workflows are a component we did not have

Created from ODC Studio (**Create → Workflow**), which opens the **ODC Portal** to edit
them. The nodes in the exercise:

- **Start** — bound to an *Asset* (the consumer app) and one of its *Events*.
- **Automatic Activity** — bound to an Asset and an Action, with input parameters mapped
  from the Start payload (`Start.NewCustomerLoan.CustomerLoanId`).
- **Decision** — branches with renamed outcomes and a condition on the activity's output.
- Published separately, and instances are visible under **Workflows** in the Portal.

Two consequences. **Workflow instances are observable in the Portal**, which is a demo
asset: a judge can watch a board request move through the pipeline. And a Workflow is
where **human-in-the-loop** belongs — the exercise says *"There is no human in the loop at
this stage"*, which places HITL in the later exercises as a workflow activity, not as
something we hand-build. Our parent approving a board before printing is exactly that.

## 3. Grounding is a serialized aggregate, not necessarily a knowledge base

`GetGroundingData` in the exercise is three nodes: an **Aggregate** over the app's own
entity, a **JSON Serialize** of its result, and an assign to the `GroundingData` output.
`BuildMessages` then injects it into the system message:

```
"Here is the customer loan information in JSON format: " + NewLine() +
GroundingData + NewLine() +
"Only answer based on the context." + NewLine() +
SystemMessageContent.ContentText
```

**That is the documented grounding pattern: serialize your own rows to JSON and put them
in the system message.** It reframes `ODC-GROUNDING.md`:

- **Open item 9 (semantic search) drops in severity.** Passing `CardLibrary` candidates as
  serialized JSON is not a degraded fallback — it is the canonical pattern. Semantic
  search becomes an upgrade to *which* rows we select, not a prerequisite for grounding.
- **Open item 8 (knowledge bases) keeps its weight**, because the TRIAD toolkit is a PDF
  rather than entity rows. But see §4: a PDF can also go in as binary content.
- **`prompts/composer.md` was already the right artifact.** It becomes the `SystemPrompt`
  value, and the layout rules travel in the prompt as they always did.

## 4. Multimodal input, concretely — and this is our photo-upload path

`UserMessage.Content` is a **list of content items, each holding exactly one type**. The
exercise appends two items per document inside a `ForEach`:

| Item | Attributes |
|---|---|
| The label | `ContentType = Entities.AIContentType.TextContent`, `ContentText = "This Document is a " + Documents.Current.DocumentLabel` |
| The file | `ContentType = Entities.AIContentType.ImageBinary`, `ContentBinaryData = Documents.Current.FileContent`, `FileFormat = Documents.Current.FileFormat` |

Carried by a structure the exercise defines as `SimpleDocument`: `FileContent` (Binary
Data), `DocumentLabel` (Text), `FileFormat` (Text), none mandatory.

**AI models ingest images *and PDFs* directly as binary content.** Two things follow. The
parent photo upload in `SPEC.md §4a` has a documented mechanism, and it is this one. And
for other file types there is a Forge component, **OmniDoc2MD (ODC)**, that converts a
binary to Markdown for appending as `TextContent`.

## 5. Two features that change how we write the code

**Prompts belong in Settings, not in the flow.** The exercise puts both prompts in
**Settings** (`SystemPrompt`, `UserPrompt`) for one stated reason: *"allows us to modify
them in the ODC Portal without the need to republish the app."* For a seven-day build with
an eval set to tune against, that is the single most valuable mechanical fact in the
exercise — prompt iteration stops costing a publish cycle.

Its rule for which prompt gets what is worth adopting verbatim: *if removing the
instruction would cause the agent to misbehave on **any** call — wrong format, DB error,
wrong tone — it belongs in the SystemPrompt. If it only applies to the current input, it
belongs in the UserPrompt.* For us: the twelve guardrails, the three-word limit and the
JSON shape are SystemPrompt; the child's profile and the obstacle are UserPrompt.

**There is a structured-output feature.** The exercise decides approval by
`Index(Response, "Approved") <> -1`, then documents its own bug — *"Not Approved"* matches
— and names the real answer: later exercises *"use the structured output feature to map
the agent's response directly into a structure, avoiding the need for a Regex action."*

So [`CODE-PLAN.md §3.1`](CODE-PLAN.md)'s output contract should be mapped by the platform,
not parsed by us. **Do not hand-write a JSON parser**, and do not decide anything by
searching for a word in free text — which is a trap our Reviewer's pass/fail would have
walked straight into.

## 6. Four gotchas that each cost an hour

1. **Raise the Default Timeout to 60 seconds** — on the agentic app *and* the consumer
   app, or the agent fails on a slow model response and the workflow never fires.
2. **Model responses overflow database columns.** The exercise names the errors
   (`OS-BERT-60400`, `22001: value too long`) and uses two defences together: a hard
   length rule in the SystemPrompt, and a truncation guard in the logic —
   `If(Length(Response) > 1000, Substr(Response, 0, 997) + "...", Response)`. Our board
   JSON is far longer than the exercise's 200-character summary, so **size the attributes
   deliberately and keep the truncation guard.**
3. **Cross-entity mappings through a joined entity** (`DocumentType.Label` on a `Document`
   aggregate) have to be set by hand; Mentor Studio does not resolve them.
4. **Mentor Studio can report success without applying the change**, cannot add public
   elements, and rewrites named function parameters as positional ones. The exercise's own
   guidance is to send one prompt at a time and verify each result in Studio. Usable for
   scaffolding, not trustworthy unreviewed.

Also named, and worth having before day 3: **Markdown Renderer (ODC)** on Forge, for
displaying model output that comes back as Markdown.

## 7. Action calling — the mechanism we were missing

*Source: the enrichment-agent exercise, 30 October, plus the* Get to know Agent Workbench
*lesson.*

The `Call Agent` element has an **Action calling** tab. You click **Add action**, pick a
server action, and the model may now decide to call it mid-reasoning. This is tool calling,
and it is the thing that separates "a prompt with context" from an agent.

Three mechanics matter, and all three are easy to get wrong:

1. **Descriptions are the interface, not the signature.** The model chooses which action to
   call from the action's **Description**, and sets the arguments from each **input
   parameter's** Description. Both are empty by default and the exercise flags this
   explicitly: *"Descriptions are very important for action calling."* A description set in
   the Logic tab propagates into the `Call Agent` element automatically.
2. **A parameter is either AI-set or fixed, and the mechanism for fixing one is an agent
   input parameter.** Leave a parameter at the default `Generated by AI` and the model fills
   it from the description. To pin it instead: **right-click the `Call Agent` element** in
   Automations › Agents, **add an Input Parameter** to the agent, and then in the Action
   calling tab pick that parameter from the tool argument's dropdown.

   **Confirmed by the communication-agent exercise, 31 October**, which pins the officer's
   decision exactly this way and gives the reason in its own words: *"By mapping this
   explicitly, we ensure the agent uses the actual decision made by the officer, rather than
   hallucinating a value."* For us, `ChildId` and anything that scopes a query to one family
   is pinned to an agent input parameter, never AI-generated — a security property, not a
   style choice, and now a documented pattern rather than our inference.
3. **Action calling settings carry a Call Condition**, and the documented example of one is
   **a token usage limit**. See `TOKEN-BUDGET.md` §6.2: this is a platform-level stop we did
   not know we had.

### Why this changes the Illustrator and the Reviewer

The exercise ends with a warning that is almost a gift:

> *"Depending on the AI model you used, the DTI calculation may be incorrect. If you want
> the enrichment agent to use the mathematical functions you define to calculate the DTI
> ratio, you can create a server action, customize the logic for the calculations, and call
> it in the Call Agent element using the Action calling feature."*

OutSystems is saying, in its own training material, that **the model gets arithmetic wrong
and the fix is to hand the arithmetic to code.** Everything numeric in a board — step
count, total duration, timer arithmetic, reading-level scoring — belongs in a server action
the model calls, not in the model's output. That was already the preference in
`CODE-PLAN.md` §3.1 on budget grounds; it is now the vendor's own instruction.

It also gives the card search a second possible shape. `ODC-GROUNDING.md` §4 has the Web app
searching the card library and passing candidates in. Action calling would let the
Illustrator call `SearchCards` itself. **We are keeping the retrieval-first design**, because
a model-initiated search is an extra model turn per attempt and `TOKEN-BUDGET.md` §3a has
no room for it. Worth saying out loud at the kickoff demo, though: the choice is deliberate,
not an absence.

## 8. Structured output — confirmed, and it is clean

*Rewritten 31 October from the underwriter-agent exercise, which is where the feature
actually appears.*

**There is a `Structured output` tab on the `Call Agent` element**, and it removes the
whole string-wrangling chain. Four steps:

1. In the **Data** tab, create a Structure with a **Description** on the structure *and* on
   every attribute. The descriptions are the schema the model is held to — the exercise's
   `Decision` attribute is described as *"A string value: either 'Approved' or 'Rejected'"*.
2. Automations › Agents → double-click the `Call<Model>` element → **Structured output**
   tab → **Add structure** → pick it.
3. Change the `AgentFlow` **`Response` output parameter's Data Type from Text to that
   Structure.**
4. Assign `Response = Call<Model>.Response` — now a typed object, not a string.

`AgentFlow.Response.Decision` and `AgentFlow.Response.Text` are then ordinary attribute
reads in the consumer-facing service action. **This is the path we take**, and
`CODE-PLAN.md §3.1`'s instruction not to hand-write a JSON parser is now backed by a
mechanism rather than a preference.

### The hand-rolled fallback, kept

The enrichment exercise predates the feature and does it by hand, which is worth keeping
in case structured output is withheld or misbehaves:

```
AgentFlow.Response  ->  Regex_Replace  ->  JSON Deserialize  ->  Run Server Action
                        strips prose      into the Structure    writes it back
```

- `Regex_Replace` comes from the **Text** library and has to be added through **Add public
  elements** — Mentor Studio cannot do it.
- The pattern is `"^[^\[{]*|\s*[^}\]]*$"` with `NewString = ""`: it deletes everything
  before the first `[` or `{` and everything after the last `}` or `]`. It exists because
  models wrap JSON in conversational padding.
- The SystemPrompt must name the keys and their types, and the Structure's attributes must
  match.

A documentation wrinkle worth not copying: the underwriter exercise still tells you to add
`Regex_Replace` as a public element in its setup step, then never uses it. It is a leftover
from the enrichment exercise. Skip it.

### The bug that ships in the exercise, and must not ship in ours

The underwriter's own decision mapping is:

```
Decision = If(Index(AgentFlow.Response.Decision, "Approved", ...) <> -1,
              Entities.AgentStatus.Approved, Entities.AgentStatus.Rejected)
```

**`"Not Approved"` contains `"Approved"`.** A substring search for the positive case
silently approves the negative one, and a loan underwriter is a vivid place to find that
out. Structured output constrains the attribute *by description*, which is not enforcement.

**Our rule: compare for equality against a known value, or better, have the model return a
value we map through a static entity** — never `Index(...) <> -1` on a decision. This lands
on guardrail 5 in `SPEC.md §6`, the one with a safety cost if it is wrong: the escalation
path must not be reachable by a substring accident.

## 9. Grounding, with the lesson's own three rules

The *Ground data for AI agent* lesson opens by calling missing context *"the biggest
challenge for any agent"* and closes with three rules. The second one is a budget rule:

1. **Stick to the facts** — send only the record and its documents. "Sending unnecessary
   entities or entire histories introduces irrelevant context, which forces the agent to
   filter noise instead of analyzing only the relevant facts."
2. **Be concise** — *"a critical optimization problem that directly affects your budget."*
   The instruction is to **assign only the essential attributes into a structure** and
   serialize that, not the entity.
3. **Keep data current** — re-read the record at agent time, never pass a stale copy.

**The exercise violates its own rule 2.** It serializes `GetCustomerLoanById.List` whole.
For us that is the difference between sending a child's entire routine history and sending
one routine: we build a **projection structure** — the handful of attributes a board needs —
and serialize that. It is the cheapest single token saving in the design.

Note also that the lesson names **three** grounding sources (aggregate, REST API, AI search
service) where the documentation names four. The missing one is the MCP server; treat the
documentation's list as the complete one and the lesson's as the common ones.

## 10. We now hold a working reference implementation

The exercise bundles extracted to `../LoanReview/exercises/` carry importable ODC apps
(moved there from `../exercises/` on 1 November; `../LoanReview/README.md` is the index):

| File | What it is |
|---|---|
| `enrichment/Agent01Intake.oml` | a **finished agentic app** — the intake agent, complete |
| `underwriter/agent02-enrichment.oml` | the **finished enrichment agent**, with action calling wired |
| `underwriter/loan-origination-enrichment-response.oml` | the consumer app after the enrichment round trip |
| `intake/LoanOrigination.oml` | the consumer app: entities, events, service actions, UI |
| `intake/MarkdownRenderer.oml` | the Forge Markdown Renderer, as a module |
| `intake/DriversLicense.png`, `PayStub6.pdf`, `BankStatement202508.pdf`, `AndreaMcCarthy2024CompleteTaxReturn.pdf` | sample documents for testing multimodal input |

`.oml` is a proprietary binary — header `OML:`, platform `11.0.415.100`, then compressed
sections — so it cannot be read here. **Importing `Agent01Intake.oml` into Studio on day 1
is worth more than any further documentation reading**, because it answers the questions
that only a working app answers: how the `Call Agent` element is really wired, what the
Action calling tab looks like populated, and what the default scaffold contains before we
delete the memory nodes.

**Arrived 31 October**: the underwriter bundle carries the finished enrichment app, which
this section previously recorded as missing. So we now hold working versions of agents 1
and 2 plus two states of the consumer app. The communication bundle is the PDF only — no
`.oml` — so agent 4 is the one we would build from the write-up rather than read.

## 11. The interactive agent is shaped differently, and one of its choices is wrong for us

*From the communication-agent exercise, 31 October. This is the fourth of four, and the
only conversational one — which makes it the closest match to a parent typing into our app.*

Four of its decisions are worth copying:

1. **Memory comes back, and it is keyed to the business record.** The first three agents
   delete `LoadMemory`, `AppendMemoryToMessages` and `StoreMemory`. This one keeps all
   three, and does something neat: it **changes `SessionId`'s data type** from Text to
   `CustomerLoan Identifier`. Conversation memory is therefore scoped to one loan, not one
   browser session. For us the equivalent key is a **child**, or a board — so a parent's
   follow-up *"make it shorter"* lands against the right routine and cannot leak across
   children. That scoping is a privacy property, not a convenience.
2. **No `UserPrompt` Setting.** The exercise says why: *"it uses the user's input
   directly."* The deterministic agents template their user message; the conversational one
   passes the parent's words through. Ours should do the same, with the guardrails in
   `SPEC.md §6` standing between the words and the model rather than a template.
3. **Intent routing lives in the SystemPrompt, pointing at a tool.** *"If the user
   explicitly asks you to draft, generate, write, compose, prepare, or create an email,
   message, or notification to the applicant, you MUST call the `GenerateEmailDraft`
   action."* A list of verbs, a named action, and `MUST`. That is the pattern for
   *"print this"*, *"text it to me"* and *"make it simpler"*.
4. **Policy as data, not as prompt text.** The underwriter agent grounds on **two**
   sources: it serializes the loan *and* a `BankPolicy` **entity**, labelling each in the
   system message (*"Here is the bank policy information in JSON format: "*). The bank's
   rules are rows, editable without republishing. **Our clinical rules should be an entity
   too**, serialized the same way — so a practice can be corrected by a clinician rather
   than by a developer, and so each board can cite which row it rested on
   (`SPEC.md §7`).

### The one to reject: chat through an event and a workflow

The exercise routes the officer's chat the same way as everything else. A `Send` click
raises a `NewUserPrompt` event; a second workflow, `WorkflowNewUserPrompt`, starts on it
and calls the agent; the screen finds out by **polling**. The exercise's own instructions
say *"Click the refresh icon"*, and the underwriter's say the response *"may take several
seconds"*.

For a bank officer at a desk that is fine. **For a parent with four minutes before the car,
it is not.** A board request that returns by refresh button is a worse product than one
that returns with a spinner, and the architecture allows the better one: the agentic app
exposes `Call<Agent>` as a **service action**, and the Web app can call it directly instead
of raising an event.

**Decision: the parent-facing path calls the service action directly and shows progress;
the event-and-workflow path is for anything that can be asynchronous** — the Illustrator
filling in artwork after the board is already usable, and the SMS send. That keeps the
Workflow in the submission, which scoring criterion one wants, without putting a refresh
button between a parent and the thing they need. `CODE-PLAN.md §4` carries it as a build
item; the latency budget belongs in `SPEC.md §4`.

One operational note from the same page: the Portal shows **logs, traces and running
workflow instances**, which is where a stuck board gets diagnosed.

---

*First → Then. Print it, post it, trust it.*
