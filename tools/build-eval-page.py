#!/usr/bin/env python3
"""Build the A/B review page from eval/cases.json.

Every case carries two candidate boards. The page asks one question per case —
which one, and why — because the "why" is the part that generalises to the prompt.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "eval", "cases.json")
OUT = os.path.join(ROOT, "docs", "eval-review.html")

e = lambda s: html.escape(str(s), quote=True)

CSS = """
:root{
  --bg:#F7FBFF; --surface:#FFFFFF; --surface-2:#EEF5FB; --line:#D4E4F2; --line-2:#B9D4E8;
  --fg:#1F2B3A; --fg-2:#4A5D73; --muted:#73879C;
  --accent:#2E7CB8; --accent-2:#1B5C8F;
  --a:#2E7CB8; --a-bg:#E8F2FA; --b:#2F8559; --b-bg:#E9F5EE;
  --warm:#A8600C; --warm-bg:#FDF6EC;
  --shadow:0 1px 2px rgba(31,43,58,.06),0 6px 20px rgba(31,43,58,.06);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0E1821; --surface:#16242F; --surface-2:#1C303E; --line:#2A4356; --line-2:#36566E;
  --fg:#E6EFF6; --fg-2:#B2C6D6; --muted:#7D96AA;
  --accent:#6FB6E4; --accent-2:#9CCDF0;
  --a:#6FB6E4; --a-bg:#152836; --b:#5CBF8C; --b-bg:#12291E;
  --warm:#E0A64E; --warm-bg:#2A2015;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.28);
  color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0E1821; --surface:#16242F; --surface-2:#1C303E; --line:#2A4356; --line-2:#36566E;
  --fg:#E6EFF6; --fg-2:#B2C6D6; --muted:#7D96AA;
  --accent:#6FB6E4; --accent-2:#9CCDF0;
  --a:#6FB6E4; --a-bg:#152836; --b:#5CBF8C; --b-bg:#12291E;
  --warm:#E0A64E; --warm-bg:#2A2015;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.28);
  color-scheme:dark}

*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);
  font-family:Lexend,"Segoe UI",system-ui,sans-serif;font-size:15px;line-height:1.6;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:74rem;margin:0 auto;
  padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px));
  padding-block:0 5rem}
header{padding-block:2.4rem 1.3rem;border-bottom:1px solid var(--line)}
.eyebrow{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);font-weight:600;margin:0 0 .5rem}
h1{font-size:clamp(1.7rem,4.6vw,2.5rem);line-height:1.15;margin:0 0 .6rem;
  letter-spacing:-.02em;text-wrap:balance}
.lede{color:var(--fg-2);margin:0;max-width:46rem}
.rule{margin:1.5rem 0 0;padding:1rem 1.15rem;background:var(--warm-bg);
  border-left:3px solid var(--warm);border-radius:0 8px 8px 0;font-size:.92rem;color:var(--fg-2)}
.rule strong{color:var(--fg)}

.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;background:var(--bg);
  border-bottom:1px solid var(--line);padding-block:.7rem;margin-bottom:1.6rem;
  display:flex;gap:.8rem;align-items:center;flex-wrap:wrap}
.count{font-size:.85rem;color:var(--muted)}
.count b{color:var(--fg);font-weight:600}
.spacer{flex:1 1 auto}
button{font:inherit;font-size:.87rem;border-radius:8px;border:1px solid var(--line);
  background:var(--surface);color:var(--fg);padding:.46rem .9rem;cursor:pointer}
button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
button.primary:hover{background:var(--accent-2);border-color:var(--accent-2)}
button:disabled{opacity:.5;cursor:default}

.case{background:var(--surface);border:1px solid var(--line);border-radius:13px;
  box-shadow:var(--shadow);margin-bottom:2rem;overflow:hidden}
.case-head{padding:1.1rem 1.25rem 1rem;border-bottom:1px solid var(--line)}
.case-head h2{font-size:1.14rem;margin:0 0 .25rem;letter-spacing:-.01em}
.case-head h2 .cn{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.78rem;
  color:#fff;background:var(--accent);border-radius:6px;padding:.1rem .45rem;
  margin-right:.5rem;font-weight:600;vertical-align:.12em}
.tests{font-size:.87rem;color:var(--muted);margin:0 0 .8rem}
.quote{font-size:.93rem;color:var(--fg-2);background:var(--surface-2);
  border-left:3px solid var(--line-2);border-radius:0 8px 8px 0;padding:.65rem .85rem;margin:0 0 .7rem}
.prof{display:flex;flex-wrap:wrap;gap:.35rem}
.chip{font-size:.74rem;background:var(--surface-2);border:1px solid var(--line);
  border-radius:20px;padding:.12rem .6rem;color:var(--fg-2)}
.chip.warn{background:var(--warm-bg);border-color:var(--warm);color:var(--warm)}

.tries{display:grid;grid-template-columns:1fr 1fr;gap:0}
.try{padding:1.05rem 1.25rem 1.3rem;min-width:0}
.try + .try{border-left:1px solid var(--line)}
.try.A{background:linear-gradient(var(--a-bg),transparent 120px)}
.try.B{background:linear-gradient(var(--b-bg),transparent 120px)}
.pick{display:flex;align-items:center;gap:.5rem;margin-bottom:.7rem;cursor:pointer;
  border:1px solid var(--line);border-radius:9px;padding:.5rem .7rem;background:var(--surface)}
.pick:hover{border-color:var(--accent)}
.pick input{accent-color:var(--accent);width:1.05rem;height:1.05rem;margin:0;flex:0 0 auto}
.pick b{font-size:.95rem}
.try.A .pick:has(input:checked){border-color:var(--a);box-shadow:inset 0 0 0 1px var(--a)}
.try.B .pick:has(input:checked){border-color:var(--b);box-shadow:inset 0 0 0 1px var(--b)}
.bet{font-size:.88rem;color:var(--fg-2);margin:0 0 .9rem}
.type{font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;font-weight:600;
  color:var(--accent);margin:0 0 .15rem}
.btitle{font-size:1rem;font-weight:600;margin:0 0 .15rem}
.theme{font-size:.8rem;color:var(--muted);margin:0 0 .8rem}
h4{font-size:.72rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);
  font-weight:600;margin:1rem 0 .4rem}
.cards{display:flex;flex-direction:column;gap:.4rem;margin:0;padding:0;list-style:none}
.cardrow{display:flex;gap:.55rem;align-items:baseline;font-size:.88rem;
  background:var(--surface-2);border:1px solid var(--line);border-radius:8px;padding:.4rem .6rem}
.role{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.68rem;
  text-transform:uppercase;color:var(--fg-2);background:var(--surface);
  border:1px solid var(--line);border-radius:5px;padding:.05rem .35rem;flex:0 0 auto}
.lab{font-weight:600}
.alt{color:var(--muted);font-size:.8rem}
dl.script{margin:0;display:grid;grid-template-columns:auto 1fr;gap:.25rem .7rem;font-size:.88rem}
dl.script dt{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;
  color:var(--muted);text-transform:uppercase;padding-top:.15rem}
dl.script dd{margin:0;color:var(--fg-2)}
ul.plan{margin:0;padding:0;list-style:none;font-size:.86rem;display:flex;
  flex-direction:column;gap:.4rem}
ul.plan b{display:block;font-size:.7rem;letter-spacing:.07em;text-transform:uppercase;
  color:var(--muted);font-weight:600}
ul.plan span{color:var(--fg-2)}
ol.hier{margin:0;padding-left:1.15rem;font-size:.85rem;color:var(--fg-2)}
ol.hier em{font-style:normal;font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:.72rem;color:var(--muted)}
.ev{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.5rem}
.note{margin-top:.9rem;font-size:.84rem;color:var(--fg-2);background:var(--warm-bg);
  border-left:3px solid var(--warm);border-radius:0 7px 7px 0;padding:.55rem .75rem}
.note b{color:var(--warm)}
.narr{margin:.3rem 0 0;padding-left:1.1rem;font-size:.85rem;color:var(--fg-2)}
.ref{font-size:.89rem;color:var(--fg-2);display:flex;flex-direction:column;gap:.55rem}
.ref b{display:block;font-size:.7rem;letter-spacing:.07em;text-transform:uppercase;
  color:var(--muted);font-weight:600}
.none{color:var(--muted);font-style:italic}

.foot{padding:1rem 1.25rem 1.2rem;border-top:1px solid var(--line);background:var(--surface-2)}
.foot label{display:block;font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);font-weight:600;margin-bottom:.35rem}
textarea{width:100%;min-height:4.6rem;resize:vertical;font:inherit;font-size:.89rem;
  color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:9px;
  padding:.6rem .75rem}
textarea:focus{outline:2px solid var(--accent);outline-offset:-1px;border-color:var(--accent)}
.saved{font-size:.74rem;color:var(--b);opacity:0;transition:opacity .2s;margin-left:.5rem}
.saved.on{opacity:1}
footer{margin-top:2.4rem;padding-top:1.3rem;border-top:1px solid var(--line);
  color:var(--muted);font-size:.85rem}
footer a{color:var(--accent)}
.off{padding:.8rem 1rem;background:var(--warm-bg);border:1px solid var(--warm);
  border-radius:9px;color:var(--fg-2);font-size:.88rem;margin-bottom:1.2rem}
@media(max-width:780px){
  .tries{grid-template-columns:1fr}
  .try + .try{border-left:0;border-top:1px solid var(--line)}
}
"""

JS = r"""
const CASES = __IDS__;
const dirty = new Set();
let db = null, saving = false, t = null;
const el = id => document.getElementById(id);

function state(id){
  const r = document.querySelector('input[name="pick-'+id+'"]:checked');
  return { pick: r ? r.value : null, comment: el('c-'+id).value };
}
function mark(id, on){
  on ? dirty.add(id) : dirty.delete(id);
  const n = dirty.size;
  el('count').innerHTML = n ? '<b>'+n+'</b> unsaved' : (done()+' of '+CASES.length+' decided');
  el('save').disabled = !n || saving;
  const s = el('s-'+id);
  if (s) s.classList.toggle('on', !on && !!state(id).pick);
}
function done(){ return CASES.filter(id => state(id).pick).length; }

async function save(){
  if (!db || !dirty.size || saving) return;
  saving = true; el('save').disabled = true; el('save').textContent = 'Saving…';
  const ids = [...dirty];
  try{
    await Promise.all(ids.map(id => {
      const s = state(id);
      return db.doc('eval/'+id).set({ pick: s.pick, comment: s.comment,
                                      updatedAt: new Date().toISOString() });
    }));
    ids.forEach(i => mark(i, false));
  }catch(err){ el('count').textContent = 'Could not save — try again'; }
  saving = false; el('save').textContent = 'Save';
  el('save').disabled = !dirty.size;
}
function queue(id){ mark(id, true); clearTimeout(t); t = setTimeout(save, 1500); }

async function start(){
  CASES.forEach(id => {
    document.querySelectorAll('input[name="pick-'+id+'"]')
      .forEach(r => r.addEventListener('change', () => queue(id)));
    el('c-'+id).addEventListener('input', () => queue(id));
  });
  el('save').addEventListener('click', save);
  addEventListener('beforeunload', ev => { if (dirty.size){ ev.preventDefault(); ev.returnValue=''; } });
  mark('__none__', false); dirty.delete('__none__');

  db = await claude.use('db');
  if (!db){ el('offline').hidden = false; el('save').disabled = true;
            el('count').textContent = 'Not signed in — nothing will be saved'; return; }

  db.collection('eval').onSnapshot(snap => {
    snap.forEach(doc => {
      const id = doc.id.split('/').pop();
      if (dirty.has(id)) return;              // never clobber an unsaved edit
      const d = doc.data || {};
      if (d.pick){
        const r = document.querySelector('input[name="pick-'+id+'"][value="'+d.pick+'"]');
        if (r) r.checked = true;
      }
      const c = el('c-'+id);
      if (c && typeof d.comment === 'string') c.value = d.comment;
      const s = el('s-'+id); if (s) s.classList.toggle('on', !!d.pick);
    });
    el('count').innerHTML = done()+' of '+CASES.length+' decided';
  }, () => {});
}
start();
"""


def render_board(t):
    p = t["plan"]
    cards = "".join(
        '<li class="cardrow"><span class="role">%s</span>'
        '<span><span class="lab">%s</span> <span class="alt">&mdash; %s</span></span></li>'
        % (e(c["role"]), e(c["label"]), e(c["altText"])) for c in t["cards"])
    script = "".join('<dt>%s</dt><dd>%s</dd>' % (e(s["phase"]), e(s["phrase"]))
                     for s in t["script"])
    plan = "".join('<li><b>%s</b><span>%s</span></li>' % (lbl, e(p[k]))
                   for k, lbl in (("placement", "Placement"),
                                  ("reinforcement", "Reinforcement"),
                                  ("ifChallengingBehavior", "If it goes wrong"),
                                  ("generalization", "Elsewhere")) if p.get(k))
    hier = "".join('<li><em>%s</em> &mdash; %s</li>' % (e(h["kind"]), e(h["instruction"]))
                   for h in p["promptHierarchy"])
    ev = "".join('<span class="chip">%s</span>' % e(x) for x in t.get("evidenceBasis", []))
    extra = ""
    if t.get("narrativeText"):
        extra += ('<h4>The words on the pages</h4><ol class="narr">%s</ol>'
                  % "".join("<li>%s</li>" % e(x) for x in t["narrativeText"]))
    if t.get("sensoryHandling"):
        extra += '<div class="note"><b>Sensory</b> &mdash; %s</div>' % e(t["sensoryHandling"])
    if t.get("specGap"):
        extra += '<div class="note"><b>Spec gap</b> &mdash; %s</div>' % e(t["specGap"])
    return ('<p class="type">%s</p><p class="btitle">%s</p><p class="theme">%s</p>'
            '<h4>Cards</h4><ul class="cards">%s</ul>'
            '<h4>What the parent says</h4><dl class="script">%s</dl>'
            '<h4>Plan</h4><ul class="plan">%s</ul>'
            '<h4>Prompt hierarchy</h4><ol class="hier">%s</ol>'
            '<div class="ev">%s</div>%s'
            % (e(t["supportType"]), e(t["title"]),
               e(t["theme"]) if t.get("theme") else "No theme",
               cards, script, plan, hier, ev, extra))


def render_referral(t):
    su = ('<span>%s</span>' % e(t["stillUseful"])) if t.get("stillUseful") \
         else '<span class="none">Nothing offered.</span>'
    return ('<p class="type">Referral &mdash; no board</p>'
            '<div class="ref">'
            '<div><b>Reason</b><span>%s</span></div>'
            '<div><b>What to do</b><span>%s</span></div>'
            '<div><b>Still useful</b>%s</div>'
            '<div><b>Deliberately absent</b><span>%s</span></div>'
            '</div>' % (e(t["reason"]), e(t["guidance"]), su, e(t["whatItDoesNotDo"])))


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    cases = data["cases"]
    out = []
    for i, c in enumerate(cases, 1):
        pr = c["profile"]
        chips = [e(pr["nickname"]), "%s years" % pr["ageYears"], e(pr["visualStyle"]),
                 e(pr["languageLevel"]), e(c["request"]["environment"])]
        chiphtml = "".join('<span class="chip">%s</span>' % x for x in chips)
        chiphtml += '<span class="chip warn">%s</span>' % e("Interests: " + pr["specialInterests"])
        chiphtml += '<span class="chip warn">%s</span>' % e("Sensory: " + pr["sensoryNotes"])
        chiphtml += '<span class="chip warn">%s</span>' % e("Triggers: " + pr["triggerNotes"])

        cols = ""
        for t in c["tries"]:
            inner = render_referral(t) if t.get("outcome") == "referral" else render_board(t)
            cols += (
                '<div class="try %s">'
                '<label class="pick"><input type="radio" name="pick-%s" value="%s">'
                '<b>Prefer %s</b></label>'
                '<p class="bet">%s</p>%s</div>'
                % (t["try"], c["id"], t["try"], t["try"], e(t["design"]), inner))

        out.append(
            '<section class="case">'
            '<div class="case-head"><h2><span class="cn">%d</span>%s</h2>'
            '<p class="tests">Tests: %s</p>'
            '<p class="quote">&ldquo;%s&rdquo;</p>'
            '<div class="prof">%s</div></div>'
            '<div class="tries">%s</div>'
            '<div class="foot"><label for="c-%s">Why &mdash; and what it means for the prompt'
            '<span class="saved" id="s-%s">saved</span></label>'
            '<textarea id="c-%s" placeholder="What made the difference? A rule I should add, '
            'or one I should drop?"></textarea></div>'
            '</section>'
            % (i, e(c["name"]), e(c["tests"]), e(c["request"]["obstacle"]), chiphtml, cols,
               c["id"], c["id"], c["id"]))

    ids = json.dumps([c["id"] for c in cases])
    page = f"""<title>Board Comparison</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header>
  <p class="eyebrow">Autism Visual Supports &middot; eval set v{e(data['version'])}</p>
  <h1>Eight cases, two boards each</h1>
  <p class="lede">For each case, pick the board you would actually put on a fridge, then
  say why. The one you pick becomes the reference answer for that case, and the set
  becomes how we tell whether a change to the Composer prompt made things better or
  only different.</p>
  <div class="rule"><strong>The comment matters more than the pick.</strong> The pick
  gives us a gold answer for one case. The reason generalises into a rule, and rules are
  what the prompt is made of. Two of these are deliberately close calls, one exposes a
  gap in the spec, and the last one has no board in it at all.</div>
</header>

<div class="bar">
  <span class="count" id="count">0 of {len(cases)} decided</span>
  <span class="spacer"></span>
  <button class="primary" id="save" disabled>Save</button>
</div>

<div class="off" id="offline" hidden>Not signed in to claude.ai, so nothing on this page
can be saved. Open it while signed in and your choices will persist.</div>

{''.join(out)}

<footer>Generated from <code>eval/cases.json</code> by <code>tools/build-eval-page.py</code>.
Repo: <a href="https://github.com/aj-aronoff/Autism-Visual-Supports">aj-aronoff/Autism-Visual-Supports</a>.</footer>
</div>
<script>{JS.replace('__IDS__', ids)}</script>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote %s (%d cases, %d tries, %.1f KB)"
          % (OUT, len(cases), sum(len(c["tries"]) for c in cases),
             os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
