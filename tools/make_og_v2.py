#!/usr/bin/env python3
"""Social-Bilder (Open Graph, 1200x630) im Redesign v2.

Links Kapitelzeile, Headline und Unterzeile aus tools/seo_meta.py, rechts die Grafik der jeweiligen Seite
(Brücke, Stufenkette, Venn, Partner, Organigramm, KI-Ringe ...). Schriften, Icons und Porträts kommen aus dem Repo.

Aufruf:  python3 tools/make_og_v2.py          (benötigt Node + Playwright: npm i playwright)
         python3 tools/make_og_v2.py --all    (alle Bilder neu, auch ohne Textänderung)
"""
import hashlib, html, json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(__file__))
import seo_meta  # noqa: E402
from siteinfo import PARTNERS  # noqa: E402
import v2  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATE = os.path.join(ROOT, "tools", "og_state.json")
VERSION = "v2-2"  # bei Gestaltungsänderungen erhöhen, dann werden alle Bilder neu erzeugt
A = "file://" + ROOT


def img(key, sm=False):
    return A + PARTNERS[key]["img_sm" if sm else "img"]


def ic(name):
    return f'<svg class="ico"><use href="#i-{name}"/></svg>'


# ------------------------------------------------------------ Grafiken rechts
def vis_home():
    planks = "".join(f'<i>{ic(n)}</i>' for n in ("pencil", "layers", "users", "megaphone"))
    return f'''<div class="plate"><div class="gapmark"><b>THE GAP</b><span></span></div>
<div class="bridge"><div class="pier l"><b>Beschlossen</b><small>Strategie · Konzept</small></div>
<div class="planks">{planks}</div><div class="pier r"><b>Im Alltag</b><small>Verhalten · Ergebnis</small></div></div>
<p class="cap">Vier Stufen schließen die Lücke.</p></div>'''


def vis_chain():
    st = [("pencil", "Konzeption", "#101D33"), ("layers", "Entwicklung", "#1b2f4d"), ("users", "Durchführung", "#515966"), ("megaphone", "Vermarktung", "#6a4e20")]
    lis = "".join(f'<li style="background:{c};margin-left:{k*26}px"><span>0{k+1}</span>{ic(i)}<b>{n}</b></li>' for k, (i, n, c) in enumerate(st))
    return f'<div class="chain"><ol>{lis}</ol><p>Einzeln buchbar oder als Kette.</p></div>'


def vis_venn():
    return '''<svg class="venn" viewBox="0 0 360 340"><circle cx="125" cy="125" r="100" fill="#85642C"/><circle cx="235" cy="125" r="100" fill="#101D33"/>
<circle cx="180" cy="220" r="100" fill="#515966"/><text x="98" y="110">Gestalten</text><text x="262" y="110">Führen</text><text x="180" y="282">Wirtschaften</text>
<text class="c" x="180" y="158">Entscheidung</text><text class="c" x="180" y="178">im Alltag</text></svg>'''


def vis_partner(key, color, icon, verb):
    p = PARTNERS[key]
    return f'''<div class="partner" style="--c:{color}"><div class="ring"><img src="{img(key)}"></div>
<span class="verb">{ic(icon)}{verb}</span><b>{html.escape(p["name"])}</b><small>{html.escape(p["role"])} · {html.escape(p["focus"])}</small></div>'''


def vis_org():
    av = "".join(f'<img src="{img(k, True)}">' for k in ("oliver-meschkat", "constantin-schubart", "marcel-dulgeridis"))
    return f'''<div class="org"><div class="o"><small>Muttergesellschaft</small>Schubart &amp; Dulgeridis GmbH</div><i></i>
<div class="o dark"><small>Tochtergesellschaft · Altdorf bei Nürnberg</small>The Gap Lab GmbH</div><i></i><div class="av">{av}</div></div>'''


def vis_contact():
    av = "".join(f'<img src="{img(k, True)}">' for k in ("constantin-schubart", "oliver-meschkat", "marcel-dulgeridis"))
    rows = "".join(f"<li>{ic(i)}{t}</li>" for i, t in (("clock", "20 bis 30 Minuten"), ("chat", "Microsoft Teams"), ("check", "Kostenlos und unverbindlich")))
    return f'<div class="contact"><div class="av">{av}</div><ul>{rows}</ul></div>'


def vis_faq(n):
    import pages_faq
    qs = [html.unescape(q) for _c, q, _a in pages_faq.ALL][:3]
    cards = "".join(f'<div class="qc" style="margin-left:{k*26}px"><i>?</i>{html.escape(q)}</div>' for k, q in enumerate(qs))
    return f'<div class="faq">{cards}<div class="big">{n}<small>Antworten</small></div></div>'


def vis_gloss(n):
    import pages_glossar
    letters = sorted({t[0][0].upper() for t in pages_glossar.terms()})
    tiles = "".join(f'<i class="{"d" if k % 3 == 2 else ""}">{l}</i>' for k, l in enumerate(letters))
    return f'<div class="gloss"><div class="az">{tiles}</div><div class="big">{n}<small>Begriffe</small></div></div>'


def vis_innolab():
    import pages_innolab as P
    rows = ""
    for f in P.FORMATS:
        on = [1, 1, 0, 1, 0] if f["id"] == "change-leadership" else [1 if d < f["days"] else 0 for d in range(5)]
        cells = "".join(f'<i class="{"on" if o else ""}"></i>' for o in on)
        rows += f'<div class="gr"><b>{html.escape(f["name"])}</b><span>{cells}</span></div>'
    head = "".join(f"<em>Tag {d}</em>" for d in range(1, 6))
    return f'<div class="plate gantt"><div class="gh"><b></b><span>{head}</span></div>{rows}</div>'


def vis_ki():
    def ring(v, cls, lab):
        off = 314.16 * (1 - v / 100)
        return (f'<div class="ri"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="50" class="t"/>'
                f'<circle cx="60" cy="60" r="50" class="{cls}" stroke-dashoffset="{off:.1f}"/></svg><b>{v}</b><small>{lab}</small></div>')
    return f'''<div class="ki">{ring(82, "m", "Management")}{ring(41, "e", "Mitarbeitende")}
<div class="sc"><span class="gap"></span><span class="mk" style="left:41%">41</span><span class="mk g" style="left:82%">82</span></div>
<p>41 Punkte KI-Gap · Illustratives Beispiel</p></div>'''


VIS = {
    "/": vis_home, "/leistungen": vis_chain, "/fokusfelder": vis_venn,
    "/fokusfelder/strategie-vertrieb-innovation": lambda: vis_partner("oliver-meschkat", "#85642C", "target", "Gestalten"),
    "/fokusfelder/leadership-organisation": lambda: vis_partner("constantin-schubart", "#101D33", "nav", "Führen"),
    "/fokusfelder/finance-transformation": lambda: vis_partner("marcel-dulgeridis", "#515966", "coins", "Wirtschaften"),
    "/ueber-uns": vis_org, "/kontakt": vis_contact,
}

EXTRA = {  # Seiten, deren Social-Bild nicht in seo_meta.META steht
    "/innolab": {"og_image": "/assets/img/og-innolab.jpg", "og_kicker": "INNOLAB", "og_line1": "Innovation, die im", "og_line2": "Unternehmen ankommt.",
                 "og_sub": "Fünf Formate vor Ort · Festpreis ab 5.800 € netto"},
    "/ki-readiness": {"og_image": "/assets/img/og-ki-readiness.jpg", "og_kicker": "KI-READINESS CHECK", "og_line1": "Ihre KI-Strategie steht.",
                      "og_line2": "Steht Ihre Organisation auch?", "og_sub": "3 Minuten · kostenlos · ohne Login"},
}

CSS = f"""
@font-face{{font-family:Archivo;src:url({A}/assets/fonts/archivo-latin.woff2) format("woff2");font-weight:400 900}}
@font-face{{font-family:"Source Sans 3";src:url({A}/assets/fonts/source-sans-3-latin.woff2) format("woff2");font-weight:400 900}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{position:relative;font-family:"Source Sans 3";color:#101D33;background:linear-gradient(150deg,#fffefa 0%,#f4ede2 70%,#fbf8f2 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(16,29,51,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(16,29,51,.035) 1px,transparent 1px);background-size:34px 34px}}
.ring0{{position:absolute;right:-120px;top:-150px;width:440px;height:440px;border-radius:50%;border:1.5px solid rgba(142,108,52,.45);box-shadow:0 0 0 30px rgba(142,108,52,.06),0 0 0 62px rgba(142,108,52,.035)}}
.rule{{position:absolute;left:0;right:0;top:0;height:10px;background:linear-gradient(90deg,#987238,#d7bd87,#9f793d)}}
.left{{position:absolute;left:72px;top:64px;width:536px;bottom:56px;display:flex;flex-direction:column;overflow:hidden}}
.brand{{font-family:Archivo;font-weight:900;font-size:24px;letter-spacing:.01em}}.brand span{{color:#7A5A27;font-weight:700}}
.brand em{{font-style:normal;font-family:"Source Sans 3";font-weight:700;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:#596578;margin-left:12px;padding-left:12px;border-left:1px solid rgba(142,108,52,.5)}}
.eyebrow{{margin-top:auto;display:flex;align-items:center;gap:16px;font-family:Archivo;font-weight:800;font-size:19px;letter-spacing:.14em;text-transform:uppercase;color:#7A5A27}}
.eyebrow:before{{content:"";width:52px;height:3px;background:#8E6C34}}
h1{{margin-top:22px;font-family:Archivo;font-weight:900;font-size:60px;line-height:1.04;letter-spacing:-.035em}}
h1 span{{display:block;white-space:nowrap}}h1 .l2{{color:#7A5A27}}
.sub{{margin-top:24px;font-size:24px;font-weight:600;color:#3d4a5e;line-height:1.35}}
.foot{{margin-top:auto;padding-top:22px;font-family:Archivo;font-weight:800;font-size:16px;letter-spacing:.06em;color:#101D33;display:flex;align-items:center;gap:10px}}
.foot i{{width:9px;height:9px;background:#8E6C34;transform:rotate(45deg)}}
.right{{position:absolute;left:650px;right:60px;top:70px;bottom:60px;display:flex;align-items:center;justify-content:center}}
.ico{{width:1em;height:1em;stroke:currentColor;fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.ico .a{{fill:currentColor;fill-opacity:.18;stroke:none}}
.plate{{width:100%;background:#fffefa;border:1px solid rgba(142,108,52,.38);border-top:4px solid #8E6C34;box-shadow:0 24px 50px rgba(16,29,51,.14);padding:28px}}
.gapmark{{display:flex;flex-direction:column;align-items:center;gap:8px;margin-bottom:22px}}.gapmark b{{font-family:Archivo;font-weight:900;font-size:30px}}
.gapmark span{{position:relative;width:52px;height:3px;background:#8E6C34}}.gapmark span:after{{content:"";position:absolute;left:50%;top:50%;width:11px;height:11px;background:#8E6C34;transform:translate(-50%,-50%) rotate(45deg)}}
.bridge{{display:grid;grid-template-columns:1fr auto 1fr;align-items:stretch;min-height:170px}}
.pier{{display:flex;flex-direction:column;justify-content:center;gap:6px;text-align:center;padding:12px}}.pier b{{font-family:Archivo;font-weight:800;font-size:18px}}.pier small{{font-size:14px}}
.pier.l{{background:#101D33;color:#fff}}.pier.l small{{color:#C9D0DA}}.pier.r{{border:3px solid #8E6C34;background:#F1E9DD}}.pier.r small{{color:#596578}}
.planks{{position:relative;display:flex;gap:5px;align-items:center;padding:0 8px}}.planks:before{{content:"";position:absolute;left:0;right:0;top:50%;border-top:3px solid #8E6C34}}
.planks i{{position:relative;width:38px;height:38px;display:grid;place-items:center;background:#8E6C34;color:#fff;font-size:20px}}
.cap{{margin-top:18px;font-family:Archivo;font-weight:800;font-size:19px}}
.chain{{width:100%}}.chain ol{{list-style:none;display:grid;gap:12px}}
.chain li{{display:grid;grid-template-columns:auto auto 1fr;gap:16px;align-items:center;padding:20px 24px;color:#fff;border-left:5px solid #CFAD6B;font-family:Archivo}}
.chain li span{{font-weight:900;font-size:22px;color:#E8D3A4}}.chain li .ico{{font-size:28px;color:#CFAD6B}}.chain li b{{font-weight:800;font-size:24px}}
.chain p{{margin:16px 0 0 78px;font-family:Archivo;font-weight:800;font-size:18px;color:#7A5A27}}
.venn{{width:440px}}.venn circle{{mix-blend-mode:multiply;fill-opacity:.88}}
.venn text{{font-family:Archivo;font-weight:800;font-size:21px;fill:#fff;text-anchor:middle}}.venn text.c{{font-size:16px}}
.partner{{display:flex;flex-direction:column;align-items:center;text-align:center}}
.partner .ring{{width:290px;height:290px;border-radius:50%;padding:12px;background:conic-gradient(var(--c) 0 72%,rgba(142,108,52,.2) 72% 100%)}}
.partner .ring img{{width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:50% 18%;border:6px solid #fffefa}}
.partner .verb{{margin-top:-28px;position:relative;display:inline-flex;align-items:center;gap:10px;padding:11px 20px;background:var(--c);color:#fff;font-family:Archivo;font-weight:900;font-size:22px;letter-spacing:.08em;text-transform:uppercase}}
.partner .verb .ico{{font-size:24px}}.partner b{{margin-top:16px;font-family:Archivo;font-weight:800;font-size:24px}}.partner small{{margin-top:4px;font-size:17px;color:#596578}}
.org{{width:100%;display:flex;flex-direction:column;align-items:center}}
.org .o{{width:100%;padding:18px;text-align:center;font-family:Archivo;font-weight:800;font-size:24px;background:#fffefa;border:1px solid rgba(142,108,52,.38);border-top:4px solid #8E6C34}}
.org .o small{{display:block;font-family:"Source Sans 3";font-weight:700;font-size:14px;letter-spacing:.1em;text-transform:uppercase;color:#7A5A27;margin-bottom:4px}}
.org .o.dark{{background:#101D33;color:#fff;border-color:#101D33;border-top-color:#CFAD6B}}.org .o.dark small{{color:#CFAD6B}}
.org>i{{width:3px;height:26px;background:#8E6C34}}
.av{{display:flex;justify-content:center}}.av img{{width:96px;height:96px;border-radius:50%;object-fit:cover;object-position:50% 18%;border:4px solid #fffefa;box-shadow:0 0 0 1px rgba(142,108,52,.5);margin-left:-16px}}.av img:first-child{{margin-left:0}}
.contact{{width:100%}}.contact .av{{justify-content:flex-start;margin-bottom:24px}}
.contact ul{{list-style:none;display:grid;gap:12px}}.contact li{{display:flex;align-items:center;gap:16px;padding:18px 22px;background:#fffefa;border:1px solid rgba(142,108,52,.38);border-left:5px solid #8E6C34;font-family:Archivo;font-weight:700;font-size:23px}}
.contact li .ico{{font-size:28px;color:#8E6C34}}
.faq{{width:100%;display:flex;flex-direction:column;gap:12px}}
.qc{{display:flex;align-items:center;gap:16px;padding:18px 20px;background:#fffefa;border:1px solid rgba(142,108,52,.38);border-top:4px solid #8E6C34;box-shadow:0 10px 24px rgba(16,29,51,.08);font-family:Archivo;font-weight:800;font-size:19px;line-height:1.25}}
.qc i{{flex:none;width:38px;height:38px;display:grid;place-items:center;background:#101D33;color:#CFAD6B;font-style:normal;font-weight:900;font-size:20px}}
.big{{font-family:Archivo;font-weight:900;font-size:76px;line-height:1;letter-spacing:-.04em;color:#7A5A27;display:flex;align-items:baseline;gap:12px;margin:8px 0 0 52px}}
.big small{{font-size:18px;letter-spacing:.14em;text-transform:uppercase}}
.gloss{{width:100%}}.az{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}
.az i{{aspect-ratio:1;display:grid;place-items:center;background:#fffefa;border:1px solid rgba(142,108,52,.38);font-style:normal;font-family:Archivo;font-weight:900;font-size:30px}}.az i.d{{background:#101D33;color:#CFAD6B;border-color:#101D33}}
.gloss .big{{margin-left:0}}
.gantt{{padding:24px 24px 18px}}.gh,.gr{{display:grid;grid-template-columns:178px 1fr;gap:12px;align-items:center}}
.gh span,.gr span{{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}}.gh em{{font-style:normal;font-family:Archivo;font-weight:800;font-size:12px;white-space:nowrap;color:#7A5A27;text-align:center}}
.gr{{padding:12px 0;border-top:1px solid rgba(142,108,52,.3)}}.gr b{{font-family:Archivo;font-weight:800;font-size:18px}}
.gr i{{height:28px;background:#F1E9DD;border:1px dashed rgba(142,108,52,.45)}}.gr i.on{{background:linear-gradient(150deg,#ead8b2,#cfad6b);border:1px solid #CFAD6B}}
.ki{{width:100%;background:#101D33;border-top:4px solid #CFAD6B;padding:28px;display:grid;grid-template-columns:1fr 1fr;gap:18px;color:#fff;box-shadow:0 24px 50px rgba(16,29,51,.2)}}
.ri{{position:relative;text-align:center}}.ri svg{{width:170px;transform:rotate(-90deg)}}.ri circle{{fill:none;stroke-width:11}}.ri .t{{stroke:rgba(255,255,255,.12)}}
.ri .m{{stroke:#CFAD6B;stroke-dasharray:314.16}}.ri .e{{stroke:#C9D0DA;stroke-dasharray:314.16}}
.ri b{{position:absolute;left:0;right:0;top:56px;font-family:Archivo;font-weight:900;font-size:46px}}.ri small{{display:block;margin-top:8px;font-family:Archivo;font-weight:800;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:#C9D0DA}}
.sc{{grid-column:1/-1;position:relative;height:12px;background:rgba(255,255,255,.12);margin-top:34px}}
.sc .gap{{position:absolute;top:0;bottom:0;left:41%;width:41%;background:repeating-linear-gradient(135deg,rgba(207,173,107,.7) 0 7px,rgba(207,173,107,.25) 7px 14px)}}
.sc .mk{{position:absolute;top:-32px;transform:translateX(-50%);font-family:Archivo;font-weight:900;font-size:18px}}.sc .mk:after{{content:"";display:block;width:3px;height:26px;margin:2px auto 0;background:#C9D0DA}}.sc .mk.g:after{{background:#CFAD6B}}
.ki p{{grid-column:1/-1;margin-top:6px;font-family:Archivo;font-weight:800;font-size:18px;color:#CFAD6B}}
"""


def page_html(m, vis_html):
    k = html.escape(m["og_kicker"])
    l1, l2 = html.escape(m["og_line1"]), html.escape(m["og_line2"])
    sub = html.escape(m.get("og_sub", ""))
    return f"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
{v2.sprite()}<div class="grid"></div><div class="ring0"></div><div class="rule"></div>
<div class="left"><div class="brand">THE GAP <span>Lab</span><em>Personalentwicklung</em></div>
<p class="eyebrow">{k}</p><h1><span class="l1">{l1}</span><span class="l2">{l2}</span></h1><p class="sub">{sub}</p>
<div class="foot"><i></i>gap-lab.de · Altdorf bei Nürnberg</div></div>
<div class="right">{vis_html}</div>
<script>document.fonts.ready.then(function(){{var h=document.querySelector("h1"),L=document.querySelector(".left"),s=60;
function ok(){{return [].every.call(h.children,function(c){{return c.scrollWidth<=h.clientWidth}})&&L.scrollHeight<=L.clientHeight}}
while(!ok()&&s>34){{s-=2;h.style.fontSize=s+"px"}}window.__fit=true}});</script></body></html>"""


def jobs():
    c = seo_meta._counts()
    items = []
    for path, raw in list(seo_meta.META.items()) + list(EXTRA.items()):
        if "og_image" not in raw:
            continue
        m = seo_meta.resolve(raw)
        if path == "/faq":
            vis = vis_faq(c["faq"])
        elif path == "/glossar":
            vis = vis_gloss(c["glossar"])
        elif path == "/innolab":
            vis = vis_innolab()
        elif path == "/ki-readiness":
            vis = vis_ki()
        else:
            vis = VIS[path]()
        items.append((m, page_html(m, vis)))
    return items


def main():
    state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    force = "--all" in sys.argv
    tmp = tempfile.mkdtemp(prefix="og_v2_")
    todo = []
    import i18n
    tr = i18n.Translator(i18n.load_catalog())
    items = []
    for m, doc in jobs():
        items.append((m, doc))
        en = dict(m, og_image=m["og_image"].replace(".jpg", ".en.jpg"))
        items.append((en, i18n.translate_fragment(doc, tr, "OG " + m["og_image"])))
    if tr.missing:
        print(f"WARNUNG: {len(tr.missing)} Texte für englische Social-Bilder fehlen im Katalog:", list(tr.missing)[:8])
    for m, doc in items:
        h = hashlib.sha1((VERSION + doc).encode()).hexdigest()[:12]
        dst = os.path.join(ROOT, m["og_image"].lstrip("/"))
        if not force and state.get(m["og_image"]) == h and os.path.exists(dst):
            continue
        f = os.path.join(tmp, os.path.basename(dst).replace(".jpg", ".html"))
        open(f, "w", encoding="utf-8").write(doc)
        todo.append({"html": f, "out": dst})
        state[m["og_image"]] = h
    if todo:
        spec = os.path.join(tmp, "jobs.json")
        json.dump(todo, open(spec, "w"))
        subprocess.run(["node", os.path.join(ROOT, "tools", "og_render.js"), spec], check=True)
    json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(f"{len(todo)} Bild(er) neu erzeugt")


if __name__ == "__main__":
    main()
