# The board page — what the child actually uses

**The agent composes the board; this is what the board becomes.** A single self-contained HTML
file on a tablet, with the two cards, the sentence to say, and four buttons for the next morning.

| File | What it does |
|---|---|
| `first-then-board.html` | The page itself. Open it in a browser — it works offline and **makes no network calls of any kind** |
| `make-board-page.py` | Stamps a new page from a validated board JSON. The only thing that writes a board page, so the board key is derived in one place and the three-word rule is checked in one place |
| `emit-board-json-prompt.txt` | **The other half, in OutSystems.** The prompt that adds an `EmitBoardJson` Setting, default `False`, and makes the app append one compact `BOARD-JSON:` line to its reply **only when a board was saved** — never on a refusal, a parse failure or a failed save. With this and the two scripts, the join is reproducible end to end |
| `board-from-reply.py` | Takes the **whole** reply pasted out of the agent app, finds the `BOARD-JSON:` line, and hands the object to the generator. **Refuses and names the reason** rather than writing half a board |

## Three things worth knowing

**It makes no network calls.** Grepped for `fetch(`, `XMLHttpRequest`, `sendBeacon`, remote
`src`/`href`, `@import` and `WebSocket` — all zero. A photograph a parent adds cannot reach the
agent, the platform or anyone else, because there is no code path that could carry it.

**Photographs stay on the device.** They live in the browser's own storage and are stripped when
the page saves a copy of itself. One button embeds them deliberately, for moving a board between
your own devices, and it says so.

**Two keys, not one.** A board key, written once and never recomputed from the card labels, plus
a fresh session id for every run — because the same board can run twice before lunch, and
editing a label must not split one board's history in two.

## Try it without any of the above

The repository carries a validated board, so the generator runs with no ODC access, no
account and no key:

```
python3 board-page/make-board-page.py schema/examples/first-then-shoes-swing.json
```

That writes a working board page you can open, tap and save.

## The join, stated plainly

The agent composes in OutSystems. The board is its own page, because what a parent keeps is a
sheet of paper. **The link between them today is a copy and a paste**, and we would rather show
that than pretend it is not there. The same page taking the same JSON could later be fed by a
service call, and nothing about the page would change.
