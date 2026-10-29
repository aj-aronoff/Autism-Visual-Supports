#!/usr/bin/env python3
"""Build the Gemini Gem paste-and-save page from prompts/gemini-gems.md.

The markdown is the source of truth. Editing the prompts there and re-running
this is the only supported way to change the page, so the two cannot drift.
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "prompts", "gemini-gems.md")
OUT = os.path.join(ROOT, "docs", "gemini-gems.html")
LOCAL = os.path.join(ROOT, "gemini-gems.html")


def parse(md):
    """Each '## N. Title' section carries one blockquote: the meta-prompt."""
    out = []
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        head, _, rest = block.partition("\n")
        m = re.match(r"(\d+)\.\s+(.*)", head.strip())
        if not m:
            continue
        quote = [ln[2:] if ln.startswith("> ") else "" for ln in rest.splitlines()
                 if ln.startswith(">")]
        text = "\n".join(quote).strip()
        text = re.sub(r"\n{3,}", "\n\n", text)
        out.append({"n": int(m.group(1)), "slug": "gem%s" % m.group(1),
                    "title": m.group(2).strip(), "prompt": text})
    return out


CSS = """
:root{
  --bg:#F7FBFF; --surface:#FFFFFF; --surface-2:#EEF5FB; --line:#D4E4F2;
  --fg:#1F2B3A; --fg-2:#4A5D73; --muted:#73879C;
  --accent:#2E7CB8; --accent-2:#1B5C8F; --warm:#A8600C; --warm-bg:#FDF6EC;
  --ok:#2F8559; --ok-bg:#EBF7F0; --shadow:0 1px 2px rgba(31,43,58,.06),0 6px 20px rgba(31,43,58,.06);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0E1821; --surface:#16242F; --surface-2:#1C303E; --line:#2A4356;
  --fg:#E6EFF6; --fg-2:#B2C6D6; --muted:#7D96AA;
  --accent:#6FB6E4; --accent-2:#9CCDF0; --warm:#E0A64E; --warm-bg:#2A2015;
  --ok:#5CBF8C; --ok-bg:#12291E; --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.28);
  color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0E1821; --surface:#16242F; --surface-2:#1C303E; --line:#2A4356;
  --fg:#E6EFF6; --fg-2:#B2C6D6; --muted:#7D96AA;
  --accent:#6FB6E4; --accent-2:#9CCDF0; --warm:#E0A64E; --warm-bg:#2A2015;
  --ok:#5CBF8C; --ok-bg:#12291E; --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.28);
  color-scheme:dark}

*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);
  font-family:Lexend,"Segoe UI",system-ui,sans-serif;font-size:16px;line-height:1.6;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:62rem;margin:0 auto;
  padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px));
  padding-block:0 5rem}

header{padding-block:2.4rem 1.4rem;border-bottom:1px solid var(--line)}
.eyebrow{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);font-weight:600;margin:0 0 .5rem}
h1{font-size:clamp(1.7rem,4.6vw,2.5rem);line-height:1.15;margin:0 0 .6rem;
  letter-spacing:-.02em;text-wrap:balance}
.lede{color:var(--fg-2);margin:0;max-width:44rem}

.rule{margin:1.6rem 0 0;padding:1rem 1.15rem;background:var(--warm-bg);
  border-left:3px solid var(--warm);border-radius:0 8px 8px 0;font-size:.93rem;
  color:var(--fg-2)}
.rule strong{color:var(--fg)}

.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;
  background:var(--bg);border-bottom:1px solid var(--line);
  padding-block:.7rem;margin-bottom:1.6rem;
  display:flex;gap:.8rem;align-items:center;flex-wrap:wrap}
.count{font-size:.86rem;color:var(--muted);min-width:0}
.count b{color:var(--fg);font-weight:600}
.spacer{flex:1 1 auto}
button{font:inherit;font-size:.88rem;border-radius:8px;border:1px solid var(--line);
  background:var(--surface);color:var(--fg);padding:.48rem .9rem;cursor:pointer;
  transition:border-color .12s,background .12s}
button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
button.primary:hover{background:var(--accent-2);border-color:var(--accent-2)}
button:disabled{opacity:.5;cursor:default}

.gem{background:var(--surface);border:1px solid var(--line);border-radius:12px;
  box-shadow:var(--shadow);margin-bottom:1.5rem;overflow:hidden}
.gem-head{display:flex;gap:.9rem;align-items:baseline;padding:1.05rem 1.2rem .3rem}
.num{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.82rem;
  color:#fff;background:var(--accent);border-radius:6px;padding:.1rem .45rem;
  flex:0 0 auto;font-weight:600}
.gem-head h2{font-size:1.08rem;margin:0;letter-spacing:-.01em}
.pin{margin-left:auto;font-size:.74rem;color:var(--ok);background:var(--ok-bg);
  border-radius:20px;padding:.15rem .6rem;opacity:0;transition:opacity .2s;flex:0 0 auto}
.pin.on{opacity:1}
.body{padding:.5rem 1.2rem 1.2rem}
pre.prompt{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.83rem;
  line-height:1.65;background:var(--surface-2);border:1px solid var(--line);
  border-radius:9px;padding:.95rem 1rem;margin:.4rem 0 .8rem;
  white-space:pre-wrap;overflow-wrap:anywhere;color:var(--fg-2);
  max-height:16rem;overflow-y:auto}
pre.prompt.open{max-height:none}
.acts{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.9rem}
label.lbl{display:block;font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);font-weight:600;margin-bottom:.35rem}
textarea{width:100%;min-height:8.5rem;resize:vertical;font:inherit;font-size:.9rem;
  line-height:1.6;color:var(--fg);background:var(--bg);border:1px solid var(--line);
  border-radius:9px;padding:.7rem .8rem}
textarea:focus{outline:2px solid var(--accent);outline-offset:-1px;border-color:var(--accent)}
footer{margin-top:2.5rem;padding-top:1.3rem;border-top:1px solid var(--line);
  color:var(--muted);font-size:.85rem}
footer a{color:var(--accent)}
.off{padding:.8rem 1rem;background:var(--warm-bg);border:1px solid var(--warm);
  border-radius:9px;color:var(--fg-2);font-size:.88rem;margin-bottom:1.2rem}
@media(max-width:560px){.gem-head{flex-wrap:wrap}.pin{margin-left:0}}
"""

JS = r"""
const GEMS = __DATA__;
const dirty = new Set();
let db = null, saving = false, t = null;
const el = id => document.getElementById(id);

function collect(){
  const o = { kind: KIND, savedAt: new Date().toISOString(), responses: {} };
  GEMS.forEach(g => { o.responses[g.slug] = el('ta-' + g.slug).value; });
  return o;
}
function apply(o){
  if (!o || !o.responses) return 0;
  let n = 0;
  GEMS.forEach(g => {
    const v = o.responses[g.slug];
    if (typeof v === 'string' && !dirty.has(g.slug)){
      el('ta-' + g.slug).value = v;
      if (v.trim()) n++;
      const p = el('pin-' + g.slug);
      if (p) p.classList.toggle('on', !!v.trim());
    }
  });
  return n;
}
function clearDirty(){ [...dirty].forEach(s => mark(s, false)); }
function refresh(){
  el('save').disabled = saving || (!!db && !dirty.size);
  GEMS.forEach(g => {
    const p = el('pin-' + g.slug);
    if (p) p.classList.toggle('on', !dirty.has(g.slug) && !!el('ta-' + g.slug).value.trim());
  });
}

// ---- persistence ---------------------------------------------------------
// Two worlds. Published on claude.ai there is a db and saving is invisible.
// Opened as a local file there is no db, so state goes to a JSON file the
// browser writes for you. showSaveFilePicker lets you choose the folder once
// and then re-save to that same file silently; without it we fall back to an
// ordinary download, which lands in Downloads and cannot be aimed anywhere.
const LSKEY = 'avs-gems-v1', FILENAME = 'gemini-gems.json', KIND = 'gemini-gems';
let fileHandle = null;

function note(msg){ el('count').textContent = msg; }

function stash(){ try{ localStorage.setItem(LSKEY, JSON.stringify(collect())); }catch(e){} }
function unstash(){
  try{ const r = localStorage.getItem(LSKEY); return r ? JSON.parse(r) : null; }
  catch(e){ return null; }
}

async function writeFile(force){
  const text = JSON.stringify(collect(), null, 2);
  if (window.showSaveFilePicker){
    try{
      if (!fileHandle && force){
        fileHandle = await showSaveFilePicker({
          suggestedName: FILENAME,
          types: [{ description: 'JSON file', accept: { 'application/json': ['.json'] } }]
        });
      }
      if (fileHandle){
        const w = await fileHandle.createWritable();
        await w.write(text);
        await w.close();
        return { ok: true, how: 'file', name: fileHandle.name };
      }
    }catch(err){
      if (err && err.name === 'AbortError') return { ok: false, how: 'cancel' };
      fileHandle = null;            // picker unavailable here — use the fallback
    }
  }
  if (!force) return { ok: false, how: 'none' };
  const blob = new Blob([text], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = FILENAME;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
  return { ok: true, how: 'download', name: FILENAME };
}

function openFile(){
  const inp = document.createElement('input');
  inp.type = 'file'; inp.accept = '.json,application/json';
  inp.addEventListener('change', () => {
    const f = inp.files && inp.files[0];
    if (!f) return;
    const r = new FileReader();
    r.onload = () => {
      try{
        const o = JSON.parse(r.result);
        if (o && o.kind && o.kind !== KIND){ note('That file belongs to the other page.'); return; }
        const n = apply(o);
        stash(); refresh();
        note('Loaded ' + n + ' from ' + f.name);
      }catch(e){ note('Could not read that file.'); }
    };
    r.readAsText(f);
  });
  inp.click();
}

async function saveLocal(explicit){
  stash();
  const res = await writeFile(explicit);
  if (res.ok){
    clearDirty();
    note(res.how === 'download' ? 'Downloaded ' + res.name
                                : 'Saved to ' + res.name);
  } else if (res.how === 'cancel'){
    note('Save cancelled — still unsaved.');
  } else {
    note('Kept in this browser. Press Save to write ' + FILENAME + '.');
  }
  refresh();
}

function mark(slug, on){
  on ? dirty.add(slug) : dirty.delete(slug);
  const n = dirty.size;
  if (n) note(n + (n === 1 ? ' unsaved' : ' unsaved'));
  else note(db ? 'All saved' : 'All saved to ' + (fileHandle ? fileHandle.name : FILENAME));
  el('save').disabled = saving || (!!db && !n);
  const p = el('pin-' + slug);
  if (p) p.classList.toggle('on', !on && !!el('ta-' + slug).value.trim());
}

async function save(auto){
  if (saving || (auto && !dirty.size)) return;
  saving = true; el('save').disabled = true; el('save').textContent = 'Saving…';
  try{
    if (db){
      const ids = [...dirty];
      await Promise.all(ids.map(slug =>
        db.doc('gems/' + slug).set({ response: el('ta-' + slug).value,
                                     updatedAt: new Date().toISOString() })));
      ids.forEach(s => mark(s, false));
    } else {
      await saveLocal(!auto);
    }
  }catch(e){ note('Could not save — try again'); }
  saving = false; el('save').textContent = 'Save';
  refresh();
}

function queue(slug){
  mark(slug, true);
  clearTimeout(t); t = setTimeout(() => save(true), 1500);
}

function build(){
  const root = el('list');
  GEMS.forEach(g => {
    const c = document.createElement('section');
    c.className = 'gem';
    c.innerHTML =
      '<div class="gem-head"><span class="num">' + g.n + '</span>' +
      '<h2>' + g.title + '</h2>' +
      '<span class="pin" id="pin-' + g.slug + '">saved</span></div>' +
      '<div class="body">' +
      '<label class="lbl">The meta-prompt</label>' +
      '<pre class="prompt" id="p-' + g.slug + '"></pre>' +
      '<div class="acts">' +
      '<button data-copy="' + g.slug + '">Copy prompt</button>' +
      '<button data-exp="' + g.slug + '">Show all</button></div>' +
      '<label class="lbl" for="ta-' + g.slug + '">The prompt the Gem wrote</label>' +
      '<textarea id="ta-' + g.slug + '" placeholder="Paste Gemini\u2019s answer here."></textarea>' +
      '</div>';
    c.querySelector('#p-' + g.slug).textContent = g.prompt;
    root.appendChild(c);
    el('ta-' + g.slug).addEventListener('input', () => queue(g.slug));
  });

  root.addEventListener('click', async ev => {
    const cp = ev.target.closest('[data-copy]');
    if (cp){
      const g = GEMS.find(x => x.slug === cp.dataset.copy);
      try{
        await navigator.clipboard.writeText(g.prompt);
        cp.textContent = 'Copied'; setTimeout(() => cp.textContent = 'Copy prompt', 1400);
      }catch(e){
        const r = document.createRange(); r.selectNode(el('p-' + g.slug));
        getSelection().removeAllRanges(); getSelection().addRange(r);
        cp.textContent = 'Selected — press Ctrl+C';
        setTimeout(() => cp.textContent = 'Copy prompt', 2200);
      }
      return;
    }
    const ex = ev.target.closest('[data-exp]');
    if (ex){
      const pre = el('p-' + ex.dataset.exp);
      ex.textContent = pre.classList.toggle('open') ? 'Show less' : 'Show all';
    }
  });
}

async function start(){
  build();
  el('save').addEventListener('click', () => save(false));
  el('load').addEventListener('click', openFile);
  addEventListener('beforeunload', e => { if (dirty.size){ e.preventDefault(); e.returnValue = ''; } });

  // Three states, not two. Outside the claude.ai runtime there is no
  // window.claude at all, so this must not be a bare call: a ReferenceError
  // would skip local-file setup. Inside the runtime but without a db, the
  // viewer blocks downloads too, so offering the file buttons there would hand
  // over a button that silently does nothing.
  const inRuntime = typeof claude !== 'undefined' && !!claude.use;
  try{ db = inRuntime ? await claude.use('db') : null; }catch(e){ db = null; }

  if (!db && inRuntime){
    el('signin').hidden = false;
    el('save').disabled = true;
    note('Sign in to claude.ai to save');
    return;
  }

  if (!db){
    el('local').hidden = false;
    el('load').hidden = false;
    el('save').textContent = 'Save';
    const n = apply(unstash());
    note(n ? 'Restored ' + n + ' from this browser — press Save to write ' + FILENAME
           : 'Nothing saved yet');
    refresh();
    return;
  }

  db.collection('gems').onSnapshot(snap => {
    snap.forEach(doc => {
      const slug = doc.id.split('/').pop();
      if (dirty.has(slug)) return;              // never clobber an unsaved edit
      const ta = el('ta-' + slug);
      if (ta && typeof doc.data.response === 'string'){
        ta.value = doc.data.response;
        const p = el('pin-' + slug);
        if (p) p.classList.toggle('on', !!doc.data.response.trim());
      }
    });
  }, () => {});
}
start();
"""



# The Artifact runtime wraps a published page in its own skeleton, so docs/ holds
# the page body alone. A file opened from disk gets no such wrapper: with no
# doctype it renders in quirks mode and with no charset the em-dashes arrive as
# mojibake. So the standalone copy carries the skeleton, and the same reset the
# runtime supplies, and the builder writes both rather than leaving it to a cp.
SKELETON = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
__HEAD__
</head>
<body>
__BODY__
</body>
</html>
"""


def write_both(page, out_docs, out_local):
    """docs/ gets the artifact source; the repo root gets a standalone file."""
    head, _, rest = page.partition("<style>")
    style, _, body = rest.partition("</style>")
    os.makedirs(os.path.dirname(out_docs), exist_ok=True)
    with open(out_docs, "w", encoding="utf-8") as f:
        f.write(page)
    with open(out_local, "w", encoding="utf-8") as f:
        # .replace, not %: the reset itself contains max-width:100%
        f.write(SKELETON.replace("__HEAD__", head.rstrip() + "\n<style>" + style + "</style>")
                        .replace("__BODY__", body.strip()))
    return os.path.getsize(out_docs), os.path.getsize(out_local)

def main():
    gems = parse(open(SRC, encoding="utf-8").read())
    if len(gems) != 8:
        raise SystemExit("expected 8 meta-prompts, parsed %d" % len(gems))
    for g in gems:
        if not g["prompt"].lower().startswith("write a great prompt to"):
            raise SystemExit("gem %d does not open with the required phrase" % g["n"])

    import json
    data = json.dumps(gems, ensure_ascii=False)
    cards = ""
    body = f"""<title>Gemini Gem Prompts</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header>
  <p class="eyebrow">Autism Visual Supports &middot; prompt comparison</p>
  <h1>Eight prompts to write prompts</h1>
  <p class="lede">Run each one in a Gemini Gem. Paste what the Gem writes back into the
  box underneath it. I read the boxes, compare each against the prompt I wrote for the
  same agent, and take whatever the Gem got right.</p>
  <div class="rule"><strong>None of these contains my answer.</strong> Each one gives
  Gemini the same raw material I had &mdash; the job, who it is for, what the output
  feeds &mdash; and nothing about how I solved it. If a meta-prompt listed my rules,
  the Gem would hand them back in its own words and the comparison would prove nothing.
  So the constraints appear as facts about the problem, and the Gem has to derive the
  rules itself. What is worth copying is a rule I missed, or one of mine with a better
  reason behind it. A longer prompt is not a better one.</div>
</header>

<div class="bar">
  <span class="count" id="count">All saved</span>
  <span class="spacer"></span>
  <button id="load" hidden>Load JSON</button>
  <button class="primary" id="save" disabled>Save</button>
</div>

<div class="off" id="signin" hidden>Saving needs a claude.ai sign-in, and this view
does not have one. Everything on the page still works &mdash; but nothing typed here will
be kept. Sign in and reload, or open the copy in the project folder, which saves to a
JSON file instead.</div>

<div class="off" id="local" hidden><strong>Local file mode.</strong> This copy is not
talking to claude.ai, so <b>Save</b> writes a <code>gemini-gems.json</code> file instead.
Chrome and Edge will ask once where to put it &mdash; choose this folder &mdash; and every
later save goes to that same file without asking. Other browsers drop it in Downloads.
Your text is also kept in this browser between visits, and <b>Load JSON</b> brings a saved
file back.</div>

<div id="list">{cards}</div>

<footer>Generated from <code>prompts/gemini-gems.md</code> by
<code>tools/build-gems-page.py</code>. The markdown is the source of truth &mdash;
edit there and rebuild. Repo:
<a href="https://github.com/aj-aronoff/Autism-Visual-Supports">aj-aronoff/Autism-Visual-Supports</a>.</footer>
</div>
<script>{JS.replace("__DATA__", data)}</script>
"""
    a, b = write_both(body, OUT, LOCAL)
    print("wrote %s (%d gems, %.1f KB)" % (OUT, len(gems), a / 1024))
    print("wrote %s (standalone, %.1f KB)" % (LOCAL, b / 1024))


if __name__ == "__main__":
    main()
