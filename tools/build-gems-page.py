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
let db = null, saving = false;

const $ = s => document.querySelector(s);
const el = id => document.getElementById(id);

function mark(slug, on){
  on ? dirty.add(slug) : dirty.delete(slug);
  const n = dirty.size;
  el('count').innerHTML = n ? '<b>'+n+'</b> unsaved' : 'All saved';
  el('save').disabled = !n || saving;
  const p = el('pin-'+slug);
  if (p) p.classList.toggle('on', !on && !!el('ta-'+slug).value.trim());
}

async function save(){
  if (!db || !dirty.size || saving) return;
  saving = true; el('save').disabled = true; el('save').textContent = 'Saving…';
  const ids = [...dirty];
  try{
    await Promise.all(ids.map(slug =>
      db.doc('gems/'+slug).set({ response: el('ta-'+slug).value,
                                 updatedAt: new Date().toISOString() })));
    ids.forEach(s => mark(s, false));
  }catch(e){ el('count').textContent = 'Could not save — try again'; }
  saving = false; el('save').textContent = 'Save';
  el('save').disabled = !dirty.size;
}

let t = null;
function queue(slug){
  mark(slug, true);
  clearTimeout(t); t = setTimeout(save, 1500);
}

function build(){
  const root = el('list');
  GEMS.forEach(g => {
    const c = document.createElement('section');
    c.className = 'gem';
    c.innerHTML =
      '<div class="gem-head"><span class="num">'+g.n+'</span>'+
      '<h2>'+g.title+'</h2>'+
      '<span class="pin" id="pin-'+g.slug+'">saved</span></div>'+
      '<div class="body">'+
      '<label class="lbl">The meta-prompt</label>'+
      '<pre class="prompt" id="p-'+g.slug+'"></pre>'+
      '<div class="acts">'+
      '<button data-copy="'+g.slug+'">Copy prompt</button>'+
      '<button data-exp="'+g.slug+'">Show all</button></div>'+
      '<label class="lbl" for="ta-'+g.slug+'">The prompt the Gem wrote</label>'+
      '<textarea id="ta-'+g.slug+'" placeholder="Paste Gemini’s answer here."></textarea>'+
      '</div>';
    c.querySelector('#p-'+g.slug).textContent = g.prompt;
    root.appendChild(c);
    el('ta-'+g.slug).addEventListener('input', () => queue(g.slug));
  });

  root.addEventListener('click', async ev => {
    const cp = ev.target.closest('[data-copy]');
    if (cp){
      const g = GEMS.find(x => x.slug === cp.dataset.copy);
      try{ await navigator.clipboard.writeText(g.prompt);
           cp.textContent = 'Copied'; setTimeout(()=>cp.textContent='Copy prompt',1400); }
      catch(e){ const r=document.createRange(); r.selectNode(el('p-'+g.slug));
                getSelection().removeAllRanges(); getSelection().addRange(r);
                cp.textContent = 'Selected — press Ctrl+C';
                setTimeout(()=>cp.textContent='Copy prompt',2200); }
      return;
    }
    const ex = ev.target.closest('[data-exp]');
    if (ex){
      const pre = el('p-'+ex.dataset.exp);
      const open = pre.classList.toggle('open');
      ex.textContent = open ? 'Show less' : 'Show all';
    }
  });
}

async function start(){
  build();
  el('save').addEventListener('click', save);
  addEventListener('beforeunload', e => { if (dirty.size){ e.preventDefault(); e.returnValue=''; } });

  db = await claude.use('db');
  if (!db){ el('offline').hidden = false; el('save').disabled = true;
            el('count').textContent = 'Not signed in — nothing will be saved'; return; }

  db.collection('gems').onSnapshot(snap => {
    snap.forEach(doc => {
      const slug = doc.id.split('/').pop();
      if (dirty.has(slug)) return;            // never clobber an unsaved edit
      const ta = el('ta-'+slug);
      if (ta && typeof doc.data.response === 'string'){
        ta.value = doc.data.response;
        const p = el('pin-'+slug);
        if (p) p.classList.toggle('on', !!doc.data.response.trim());
      }
    });
  }, () => {});
}
start();
"""


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
  <button class="primary" id="save" disabled>Save</button>
</div>

<div class="off" id="offline" hidden>Not signed in to claude.ai, so nothing on this page
can be saved. Open it while signed in and your text will persist.</div>

<div id="list">{cards}</div>

<footer>Generated from <code>prompts/gemini-gems.md</code> by
<code>tools/build-gems-page.py</code>. The markdown is the source of truth &mdash;
edit there and rebuild. Repo:
<a href="https://github.com/aj-aronoff/Autism-Visual-Supports">aj-aronoff/Autism-Visual-Supports</a>.</footer>
</div>
<script>{JS.replace("__DATA__", data)}</script>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote %s (%d gems, %.1f KB)" % (OUT, len(gems), os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
