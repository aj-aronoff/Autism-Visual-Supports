# The imported board running on the child's own iPad — 11 November 2026, 17:01

**Board 100, composed by the agent in OutSystems, pasted through `board-from-reply.py`, served from
the laptop over the house WiFi, open in Safari on the iPad — with photographs of her own shoe and
her own light-up dinosaur on the two cards.**

Photo: `ipad-board-device.jpg` (and `-small.jpg`, 273 KB). The original is `HTML on IPAD.jpg`.
Processing was corrective only — deskewed by a **measured 0.70°**, flat-fielded to remove the
vignette, white-balanced (the page photographed as RGB 173,170,172 and was lifted to white), and
cropped to drop the address bar and the battery indicator. **Nothing in the page was altered.**

## What is visible, and what each thing is evidence of

| On screen | What it shows |
|---|---|
| `Shoes First, Then Dinosaur` · `FirstThenBoard` | The agent's own title and support type, unedited |
| `Theme: Dinosaur footprints` | The theme came from the child's recorded interest and resolved through the page's lookup to the dinosaur tint and the corner motif |
| `Antecedent Package — cueing and prompting/prompt fading` | The practice and technique, named on the board itself |
| Two cards, **real photographs** | Her actual shoe and her actual toy, added on the iPad from her own library |
| `First shoes, then dinosaur.` | The script line the Composer wrote |
| Four buttons, in the card's own words | `✓ Put on shoes`, `★ Dinosaur toy`, `Dinosaur toy — later`, `Dinosaur toy did not happen` |
| `This run — nothing yet.` | A run that has not started, which is what the next morning begins from |

## What it proves

1. **The whole chain reaches the child's device.** Parent's prose → two knowledge bases → Composer
   → Reviewer → one emitted line → a page → a real iPad. Nothing in that path is a mock-up.
2. **`Download with pictures` works.** The `PICS` block and its loader were written the same
   afternoon and unit-tested in node; this was their **first run in a browser**, and the downloaded
   file, reopened from Files on a different origin with no stored photographs, showed the correct
   pictures.
3. **The photographs never left the device.** The page makes zero network calls — grepped for
   `fetch(`, `XMLHttpRequest`, `sendBeacon`, remote `src`/`href`, `@import` and `WebSocket`, all
   zero — and `pageHTML()` strips photos unless that one button is pressed. The pictures went from
   her camera roll to her own iPad's storage and nowhere else.
4. **Every iPad browser is WebKit**, so no iPad can save a page in place; `Download with pictures`
   is the answer rather than a workaround. iPad Chrome and iPad Edge cannot open a local file at
   all.

## What it does NOT prove

- **Board 100 is not the Demo's board.** It was composed from the velcro-and-shelf message, not
  from the tie-shoes message the Demo types, and its Reviewer verdict was `pass` rather than
  `revise`. The two cannot be narrated as one run.
- **The page was served over HTTP from the laptop**, not installed on the iPad. That is a
  demonstration setup, and the honest description is a page on a device, not a deployed app.
- **One device, one session.** Nothing here is about a second iPad, a second child, or a board run
  twice in a morning.
- The `+ photo` buttons are visible because this is the parent's view. Board-only mode hides them.
