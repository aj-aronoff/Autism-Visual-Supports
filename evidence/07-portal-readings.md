# Portal readings, 9 November 2026

Everything here was read off the ODC Portal, not inferred.

## The agentic app
`Autism Visual Supports` · Development · **Revision 5, published Nov 09 2026 04:23 PM**, by
Avram (A.J.) Aronoff. Later publishes followed for the seed fix, the Setting defaults and the
grounding fixes.

Tabs: `Configuration` · `Consumers` · `Producers` · `Settings 15` · `Timers 1` ·
`Monitoring & Troubleshooting`. **The app's Settings are edited on the `Configuration` tab, per
stage** — nothing in this project had recorded where they lived.

## The generated test app
`Autism Visual Supports test app` · Development · **Revision 1, published Nov 09 2026 04:24 PM**.
*"A web app optimized for agent testing."* It calls `CallAutismVisualSupports`, so **it runs the
whole `AgentFlow`, including both knowledge-base searches** — which earlier project notes denied.
The proof: the agent's own inputs are `Messages` and `ChildId` with **no `BoardId`**, yet the test
app's chat shows a `BoardId` field, and only `AgentFlow` and `CallAutismVisualSupports` have one.

## `BedrockHaiku5_5`
Provider **Amazon Bedrock** · Configuration **Development AND Production** · Endpoints
**Priority 1 · Haiku 5.5 · Active** · **Usage limit `0 of 10,000,000 tokens`** ·
last modified **Nov 01 2026 01:34 PM by Miguel Amado** — the organiser, which is why his Slack
instruction to swap the model was safe advice.

**Reached through `Add public elements` → All sources → search → tick all → Add.** Nothing to
provision, no AWS account. The same dialog is how a second app would consume
`CallAutismVisualSupports`.

## The trial model, for contrast
**1,000 REQUESTS**, not tokens — `0 of 1000` on 1 Nov, GPT-5's equivalent is 100.
Source: `QUESTIONS-consolidated.txt`. **The two meters use different units**, which is why
switching to Bedrock did not only raise the ceiling: `TOKEN-BUDGET.md` is written in tokens, and
`LogTokenUsage` still writes `0`, so this Portal page is the only cost instrument that exists.

## Knowledge bases
`VisualSupportClinical` → `triad-visual-supports-p1-3` · **`Indexed files 1 of 1`** · ≈16 chunks,
16 vectors · 8.17 KB · chunking **Smart** · 0 indexing, 0 failed to index, 0 failed uploads.
`VisualSupportsTreatments` → `nsp-established-treatments-p11-19` · the same, 7.92 KB.

**Both read `0 of 0` when created.** That was a not-yet-indexed state, not a failed upload;
indexing is asynchronous with no status API and completed on its own.

## The 15 Settings
Four are the app's own: `DebugShowPassages`, `DemoChildNickname` (`Daughter`), `KBMinimumScore`,
`KBTopK` (3).

**Eleven carry a `Library` owner and belong to the agentic app TEMPLATE**, not to this build:
**Eleven settings belong to libraries that arrived with the agentic app template** — embedding
endpoints, model names, two page-extraction limits, and **two masked third-party API keys we did
not enter**. Endpoints and key names are withheld here. None of those libraries is called by this
application; every outside call it makes was enumerated and is listed above..

**Mentor enumerated every external action call this app makes**, and the complete list is:
the two knowledge-base searches, `Regex_Search` from the Text library, the built-in list actions,
and the Bedrock model call. **Nothing in `ImageVectorLibrary`, `SemanticEngineV2Library`,
`SemanticEngineV2`, `MultimodalEmbeddingLibrary`, `AWSBedrockRuntime`, `AWSBedrockModelInvocations`
or `Xml` is called.**

**UPDATED 10 Nov 00:15 — the category is BOTH, and proven.** A clone rebound to Azure OpenAI in four edits composes and reviews successfully, so the app runs on either provider unchanged (`evidence/15`). The enumeration below still holds and is what made that swap a four-edit change: the only live AI dependency is one model connection, and it was
Amazon Bedrock.** Mentor's caveat, kept: the check covered action *steps* only, not outside
functions inside expressions, nor the libraries' internal dependencies — *"please don't take that
as proven."*

**Not yet known: whether `APIKey` and `EmbeddingAPIKey` hold values.** A masked field looks
identical when empty. **Until that is known, do not publish a screenshot of that Settings page.**

## Validation, unchanged all day
**0 errors, 13 warnings** = 7 *"action is never used"* (`AddCard`, `AddSensorySupport`,
`BuildReviewerMessages`, `CheckReviewVerdict`, `SaveDraftBoard`, `SetPlan`, `SetScript` — the
Reviewer chain and the save steps) + 6 *"set Update Behavior to Changed Attributes"* scalability
suggestions on `Board`, `Card`, `CardLibrary`, `Child`, `TokenUsage`, `UsageLog`.

## One ODC constraint worth recording
**Every service action is public by nature in this version.** Trying to make one private raised
*"The app uses 'Public Property of a Service Action within an App', which is not supported on this
version."* So *"keep the entities private and expose only service actions"* does **not** produce a
private surface. The accurate sentence is: **the entities are private, and every entry point is a
service action that enforces its own rules.**
