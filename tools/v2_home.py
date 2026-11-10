"""Redesign v2: komplett neu aufgebaute Startseite.

Alle Inhalte stammen aus den bestehenden Modulen (visuals, pages_core, pages_innolab, pages_glossar, siteinfo).
Keine erfundenen Zahlen, keine Preise (die stehen ausschließlich auf /innolab).
Keine Inline-Styles/-Skripte: Werte für Animationen stehen in data-Attributen und werden von assets/v2.js gesetzt.
"""
from siteinfo import SITE, PARTNERS
from helpers import esc, faq_block
from v2 import ic

ARROW = ('<svg class="icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def _head(eyebrow, title, intro="", tid="", center=False, dark=False):
    cls = "x-head" + (" x-center" if center else "")
    intro_html = f'<p class="x-lead">{intro}</p>' if intro else ""
    return f'<div class="{cls}"><p class="x-eyebrow">{eyebrow}</p><h2 id="{tid}">{title}</h2>{intro_html}</div>'


def _tile(cls, tid, inner, sid=""):
    sid_attr = f' id="{sid}"' if sid else ""
    return f'<section class="x-tile {cls}"{sid_attr} aria-labelledby="{tid}"><div class="container">{inner}</div></section>'


# ---------------------------------------------------------------- 1 · Hero
def hero():
    import visuals as V
    stages = [(n, i) for (_a, n, _q, _r), i in zip(V.STAGES, ["pencil", "layers", "users", "megaphone"])]
    planks = "".join(f'<li class="x-plank" data-i="{k}" title="{n}">{ic(i)}<span class="sr-only">{n}</span></li>' for k, (n, i) in enumerate(stages))
    names = "|".join(n for n, _ in stages)
    return f"""
<section class="hero hero-home x-hero2"><div class="container"><div class="hero-grid">
  <div>
    <p class="eyebrow">Personalentwicklung · Altdorf bei Nürnberg</p>
    <h1>Personal&shy;entwicklung, die <span class="accent">verbindet.</span></h1>
    <p class="lead">THE GAP Lab verbindet Strategie, Führungsklarheit und Finanzverständnis in Maßnahmen, die im Arbeitsalltag ankommen.</p>
    <div class="hero-actions">
      <a class="btn" href="/kontakt">Erstgespräch vereinbaren {ARROW}</a>
      <a class="link-arrow" href="/leistungen">Leistungen ansehen {ARROW}</a>
    </div>
  </div>
  <figure class="x-render" aria-labelledby="x-render-cap">
    <div class="x-gapmark" aria-hidden="true"><b>THE GAP</b><i></i></div>
    <div class="x-bridge-scene">
      <div class="x-pier x-pier-l"><b>Beschlossen</b><span>Strategie · Konzept</span></div>
      <ol class="x-planks" aria-label="Die vier Stufen als Brücke" data-names="{names}">{planks}</ol>
      <div class="x-pier x-pier-r"><b>Im Alltag</b><span>Verhalten · Ergebnis</span></div>
    </div>
    <div class="x-ctl"><label for="x-range">Stufen</label><input id="x-range" type="range" min="0" max="4" step="1" value="1" aria-describedby="x-render-cap"><output class="x-outv" for="x-range">1 / 4</output></div>
    <p class="x-state" data-s0="Die Lücke ist offen." data-s2="Beschlossenes kommt im Alltag an.">Stufe 1 · Konzeption</p>
    <figcaption id="x-render-cap">Hier setzt THE GAP Lab an: Beschlossenes kommt im Alltag an.</figcaption>
  </figure>
</div></div></section>"""


# ---------------------------------------------------------------- 2 · Zahlen
def numbers():
    venn = ('<svg class="x-mini" viewBox="0 0 64 56" aria-hidden="true"><circle class="m1" cx="22" cy="20" r="15"/><circle class="m2" cx="42" cy="20" r="15"/>'
            '<circle class="m3" cx="32" cy="36" r="15"/></svg>')
    av = "".join(f'<img src="{esc(PARTNERS[k]["img_sm"])}" alt="" width="40" height="40" loading="lazy" decoding="async">'
                 for k in ("oliver-meschkat", "constantin-schubart", "marcel-dulgeridis"))
    bars = '<span class="x-mini-bars" aria-hidden="true">' + "".join(f'<i class="d{d}"></i>' for d in (5, 3, 3, 3, 2)) + '</span>'
    # Uhr: Segment von Minute 20 bis 30
    import math
    def pt(m, r=22):
        a = math.radians(m * 6 - 90)
        return 28 + r * math.cos(a), 28 + r * math.sin(a)
    x1, y1 = pt(20); x2, y2 = pt(30)
    ticks = "".join(f'<path d="M{pt(m,24)[0]:.1f} {pt(m,24)[1]:.1f}L{pt(m,21)[0]:.1f} {pt(m,21)[1]:.1f}"/>' for m in range(0, 60, 5))
    clock = (f'<svg class="x-mini x-clock" viewBox="0 0 56 56" aria-hidden="true"><circle class="c0" cx="28" cy="28" r="26"/><g class="tk">{ticks}</g>'
             f'<path class="seg" d="M28 28L{x1:.1f} {y1:.1f}A22 22 0 0 1 {x2:.1f} {y2:.1f}Z"/><circle class="hub" cx="28" cy="28" r="2.5"/></svg>')
    items = [(venn, "3", "Disziplinen", "in einer Gesellschaft"), (f'<span class="x-mini-av" aria-hidden="true">{av}</span>', "3", "Partner", "mit Namen"),
             (bars, "5", "InnoLab-Formate", "vor Ort"), (clock, "20–30", "Minuten Erstgespräch", "kostenlos")]
    lis = "".join(f'<li class="x-rv"><span class="x-mini-wrap">{v}</span><b class="x-count">{n}</b><span>{a}<small>{b}</small></span></li>' for v, n, a, b in items)
    return f'<section class="x-nums" aria-label="Das Wichtigste auf einen Blick"><div class="container"><ul>{lis}</ul></div></section>'


# ---------------------------------------------------------------- 3 · Kurzantwort
def kurz():
    facts = [("building", "Wer", "The Gap Lab GmbH, Tochter der Schubart &amp; Dulgeridis GmbH"),
             ("target", "Für wen", "Geschäftsleitungen, Personalverantwortliche, Führungskräfte, Bildungsträger"),
             ("pin", "Wo", f"{SITE['street']}, {SITE['zip']} {SITE['city']}"),
             ("calendar", "Einstieg", "Kostenloses Erstgespräch, 20 bis 30 Minuten")]
    cards = "".join(f'<div class="x-fact x-rv">{ic(i)}<span class="x-k">{k}</span><span class="x-v">{v}</span></div>' for i, k, v in facts)
    inner = f"""<div class="x-answer x-rv"><p class="x-eyebrow">Kurzantwort: Was ist THE GAP Lab?</p>
<p class="x-statement">THE GAP Lab konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung in drei Fokusfeldern: <em>Strategie, Vertrieb &amp; Innovation</em>, <em>Leadership &amp; Organisation</em> sowie <em>Finance &amp; Transformation</em>. Konkrete Angebote sind fünf InnoLab-Workshops vor Ort und der kostenlose KI-Readiness Check.</p></div>
<div class="x-facts">{cards}</div>"""
    return f'<section class="x-tile x-parch x-tight" aria-label="Kurzantwort"><div class="container">{inner}</div></section>'


# ---------------------------------------------------------------- 4 · Problem (Leitung mit Lecks)
def problem():
    breaks = [("f4", "compass", "Konzeption", "Maßnahmen passen nicht zur Zielgruppe", "Standardformate gehen an der Zielgruppe vorbei.", "/leistungen#konzeption"),
              ("f2", "nav", "Leadership &amp; Organisation", "Führung bleibt unscharf", "Rollen und Entscheidungsrechte sind unklar.", "/fokusfelder/leadership-organisation"),
              ("f1", "target", "Strategie, Vertrieb &amp; Innovation", "Strategie erreicht den Kunden nicht", "Angebot, Vertrieb und Verhandlung folgen keiner gemeinsamen Linie.", "/fokusfelder/strategie-vertrieb-innovation"),
              ("f3", "coins", "Finance &amp; Transformation", "Zahlen werden nicht verstanden", "Entscheidungen ohne Bild der Finanzwirkung.", "/fokusfelder/finance-transformation")]
    xs = [190, 370, 550, 730]
    leaks = "".join(f'<g class="x-leak" data-i="{k}"><circle class="x-leak-ring" cx="{x}" cy="70" r="15"/><circle class="x-leak-dot" cx="{x}" cy="70" r="6"/>'
                    f'<path class="x-drip" d="M{x} 88v26"/><text x="{x}" y="140" text-anchor="middle">{k+1:02d}</text></g>' for k, x in enumerate(xs))
    svg = f"""<svg class="x-pipe" viewBox="0 0 920 160" role="img" aria-labelledby="x-pipe-t"><title id="x-pipe-t">Schema: Auf dem Weg vom Beschluss in den Alltag geht an vier Stellen Wirkung verloren.</title>
<rect class="x-pipe-end" x="0" y="44" width="96" height="52"/><text class="x-pipe-lab" x="48" y="75" text-anchor="middle">Beschluss</text>
<rect class="x-pipe-end x-pipe-end-r" x="824" y="44" width="96" height="52"/><text class="x-pipe-lab x-pipe-lab-r" x="872" y="75" text-anchor="middle">Alltag</text>
<path class="x-pipe-track" d="M96 70H824"/><path class="x-pipe-flow" d="M96 70H824"/>{leaks}</svg>"""
    cards = "".join(
        f'<li class="x-break {c} x-rv" data-i="{k}"><span class="x-break-ic">{ic(i)}</span><span class="x-break-no">{k+1:02d}</span>'
        f'<span class="x-tag">{t}</span><h3><a href="{href}">{h}</a></h3><p>{p}</p></li>'
        for k, (c, i, t, h, p, href) in enumerate(breaks))
    inner = (_head("01 · Das Problem", "Personalentwicklung verliert an vier Stellen ihre Wirkung.", "", "problem-title")
             + f'<div class="x-pipe-wrap x-rv" data-state="open">{svg}'
             + f'<button class="x-switch" type="button" aria-pressed="false">{ic("check")}<span class="x-sw-off">Lücken schließen</span><span class="x-sw-on">Lücken geschlossen</span></button></div>'
             + f'<ol class="x-breaks">{cards}</ol>')
    return _tile("x-light", "problem-title", inner, "problem")


# ---------------------------------------------------------------- 5 · Vier Stufen (Etagen)
def stages():
    import visuals as V
    icons = ["pencil", "layers", "users", "megaphone"]
    floors, panels = [], []
    for k, ((aid, name, q, res), i) in enumerate(zip(V.STAGES, icons)):
        floors.append(f'<button class="x-floor{" on" if k == 0 else ""}" type="button" role="tab" id="fl-{aid}" aria-controls="fp-{aid}" aria-selected="{"true" if k == 0 else "false"}" data-i="{k}">'
                      f'<span class="x-floor-no">{k+1:02d}</span>{ic(i)}<span class="x-floor-n">{name}</span></button>')
        items = "".join(f"<li>{ic('check')}{r.strip()}</li>" for r in res.split(","))
        panels.append(f'<div class="x-panel{" on" if k == 0 else ""}" role="tabpanel" id="fp-{aid}" aria-labelledby="fl-{aid}"{"" if k == 0 else " hidden"}>'
                      f'<span class="x-panel-ic">{ic(i)}</span><span class="x-seg" aria-hidden="true">{"".join(f'<i class="{"on" if n <= k else ""}"></i>' for n in range(4))}</span><p class="x-eyebrow">Stufe {k+1} von 4 · Leitfrage</p><h3>{q}</h3>'
                      f'<p class="x-k">Ergebnisse</p><ul class="x-checks">{items}</ul>'
                      f'<a class="link-arrow" href="/leistungen#{aid}">{name} im Detail {ARROW}</a></div>')
    # Etagen von unten nach oben: Konzeption ist das Fundament
    tower = f'<div class="x-tower" role="tablist" aria-label="Die vier Stufen" aria-orientation="vertical">{"".join(reversed(floors))}<span class="x-ground" aria-hidden="true"></span></div>'
    inner = (_head("02 · Die Lösung", "Vier Stufen der Personalentwicklung, jede mit eigenem Ergebnis.",
                   "Einzeln buchbar oder als Kette. Wählen Sie eine Stufe.", "leistungen-title")
             + f'<div class="x-stages">{tower}<div class="x-panels">{"".join(panels)}</div></div>'
             + f'<button class="x-chainbtn" type="button" aria-pressed="false">{ic("link")}<span>Als Kette anzeigen</span></button>')
    return _tile("x-dark", "leistungen-title", inner, "leistungen")


# ---------------------------------------------------------------- 6 · Fokusfelder (Venn + Perspektiven + Wegweiser)
def fokus():
    import visuals as V
    leit = {"f1": "Wie bringe ich Strategie, Angebot und Auftritt zum Kunden?",
            "f2": "Wer entscheidet was, und wie kommt Strategie im Alltag an?",
            "f3": "Was bewirkt das Vorhaben finanziell, und trägt der Business Case?"}
    terms = {"f1": ["Strategie", "Sales", "BATNA", "Change"], "f2": ["Rollenklarheit", "Entscheidungsrechte", "Führungskultur"],
             "f3": ["GuV", "Bilanz", "Cashflow", "Business Case"]}
    situ = {"f1": "Strategie, Vertrieb, Verhandlung oder Innovation brauchen Richtung",
            "f2": "Rollen, Entscheidungswege oder Führung sind unklar",
            "f3": "Zahlen sollen Entscheidungen und Vorhaben tragen"}
    icons = {"f1": "target", "f2": "nav", "f3": "coins"}
    tabs, panes, chips = [], [], []
    for k, (c, path, name, verb, pkey, claim) in enumerate(V.FIELDS):
        p = PARTNERS[pkey]
        sel = k == 0
        tabs.append(f'<button class="x-ptab {c}{" on" if sel else ""}" type="button" role="tab" id="pt-{c}" aria-controls="pp-{c}" aria-selected="{"true" if sel else "false"}" data-f="{c}">'
                    f'{ic(icons[c])}<span>{verb}</span></button>')
        chip_terms = "".join(f"<li>{t}</li>" for t in terms[c])
        panes.append(f'<div class="x-pane {c}{" on" if sel else ""}" role="tabpanel" id="pp-{c}" aria-labelledby="pt-{c}"{"" if sel else " hidden"}>'
                     f'<img src="{esc(p["img"])}" alt="{esc(p["name"])}" width="160" height="160" loading="lazy" decoding="async">'
                     f'<div><p class="x-eyebrow">{verb} · {name}</p><h3>{claim}</h3><p class="x-q">„{leit[c]}“</p>'
                     f'<ul class="x-terms">{chip_terms}</ul>'
                     f'<p class="x-who"><b>{esc(p["name"])}</b><span>{esc(p["role"])}</span></p>'
                     f'<a class="link-arrow" href="{path}">Fokusfeld ansehen {ARROW}</a></div></div>')
        chips.append(f'<button class="x-situ" type="button" data-f="{c}">{situ[c]}</button>')
    venn = """<svg class="x-venn" viewBox="0 0 400 380" role="img" aria-labelledby="x-venn-t"><title id="x-venn-t">Schema: Gestalten, Führen und Wirtschaften überschneiden sich in der Entscheidung im Alltag.</title>
<circle class="x-vc f1" data-f="f1" cx="140" cy="140" r="110"/><circle class="x-vc f2" data-f="f2" cx="260" cy="140" r="110"/><circle class="x-vc f3" data-f="f3" cx="200" cy="244" r="110"/>
<text class="x-vt" x="105" y="122" text-anchor="middle">Gestalten</text><text class="x-vt" x="295" y="122" text-anchor="middle">Führen</text><text class="x-vt" x="200" y="318" text-anchor="middle">Wirtschaften</text>
<text class="x-vt x-vt-c" x="200" y="178" text-anchor="middle">Entscheidung</text><text class="x-vt x-vt-c" x="200" y="198" text-anchor="middle">im Alltag</text></svg>"""
    inner = (_head("03 · Die Fokusfelder", "Gestalten, Führen und Wirtschaften treffen bei Entscheidern zusammen.", "", "fokus-title")
             + f'<div class="x-fokus"><div class="x-venn-wrap x-rv">{venn}</div>'
             + f'<div class="x-persp x-rv"><div class="x-ptabs" role="tablist" aria-label="Fokusfelder">{"".join(tabs)}</div>{"".join(panes)}</div></div>'
             + f'<div class="x-finder x-rv"><p class="x-finder-q">{ic("compass")}Welches Fokusfeld passt zu Ihrer Aufgabe?</p><div class="x-situs">{"".join(chips)}</div></div>')
    return _tile("x-light", "fokus-title", inner, "fokusfelder")


# ---------------------------------------------------------------- 7 · Vorher / Nachher (InnoLab)
def innolab():
    import pages_innolab as P
    fmt = {f["id"]: f for f in P.FORMATS}
    rows_a = "".join(f'<li>{ic("spark")}<span>{esc(v)}</span></li>' for v, _i, _z in P.PICK)
    rows_b = "".join(f'<li>{ic("check")}<span>{esc(z)}<small>{esc(fmt[i]["name"])} · {esc(fmt[i]["dur"])}</small></span></li>' for _v, i, z in P.PICK)
    zu = {i: z for _v, i, z in P.PICK}
    def cells(f):
        on = [1, 1, 0, 1, 0] if f["id"] == "change-leadership" else [1 if d < f["days"] else 0 for d in range(5)]
        return "".join(f'<i class="{"on" if o else ""}"></i>' for k, o in enumerate(on))
    head = '<div class="x-g-head" aria-hidden="true"><span></span>' + "".join(f"<span>Tag {d}</span>" for d in range(1, 6)) + '</div>'
    rows = "".join(f'<a class="x-g-row" href="/innolab#{f["id"]}"><span class="x-g-name"><b>{esc(f["name"])}</b><small>{esc(f["kind"])} · {esc(f["dur"])}</small></span>'
                   f'<span class="x-g-cells" aria-label="{esc(f["dur"])}">{cells(f)}</span><span class="x-g-out">{ic("check")}{esc(zu.get(f["id"], ""))}</span></a>' for f in P.FORMATS)
    days = f'<div class="x-gantt x-rv"><p class="x-g-cap">{ic("calendar")}Fünf Formate im Zeitraster</p>{head}{rows}</div>'
    inner = (_head("04 · Das Angebot", "Von der Absicht zum Ergebnis.",
                   "Fünf InnoLab-Formate vor Ort. Jedes endet mit einem Ergebnis, das Sie weiterverwenden.", "angebote-title")
             + f'''<div class="x-cmp x-rv show-a" data-p="0">
  <div class="x-cmp-pane x-cmp-a"><h3>{ic("spark")}Ausgangslage</h3><ul>{rows_a}</ul></div>
  <div class="x-cmp-pane x-cmp-b"><h3>{ic("check")}Nach dem InnoLab</h3><ul>{rows_b}</ul></div>
</div>
<div class="x-cmp-ctl x-rv"><button type="button" data-to="0">Ausgangslage</button><input id="x-cmp" type="range" min="0" max="100" value="0" aria-label="Ausgangslage oder Ergebnis anzeigen"><button type="button" data-to="100">Ergebnis</button></div>
{days}
<p class="x-more"><a class="btn" href="/innolab">InnoLab ansehen {ARROW}</a></p>''')
    return _tile("x-cream", "angebote-title", inner, "innolab")


# ---------------------------------------------------------------- 8 · KI-Readiness (Cockpit)
def ki():
    dims = [("target", "Strategie &amp; Zielbild"), ("bulb", "Anwendungsfälle"), ("cpu", "Daten &amp; Systeme"), ("scale", "Governance &amp; Recht"),
            ("book", "Kompetenzen"), ("nav", "Führung &amp; Change"), ("users", "Nutzung im Alltag"), ("coins", "Wirkung &amp; Business Case")]
    tiles = "".join(f'<li class="x-rv">{ic(i)}<span>{n}</span></li>' for i, n in dims)
    ring = lambda cls, v, lab: (f'<div class="x-ring-item"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="x-r-track" cx="60" cy="60" r="50"/>'
                                f'<circle class="x-r-val {cls}" cx="60" cy="60" r="50" data-v="{v}"/></svg><b>{v}</b><span>{lab}</span></div>')
    inner = (_head("KI-Readiness Check · kostenlos", "Die KI-Lücke in drei Minuten sichtbar.",
                   "Acht Aussagen bewerten, zwei Sichten angeben, KI-Gap erhalten.", "ki-title")
             + f'''<div class="x-cockpit">
  <div class="x-viz x-rv"><p class="x-viz-h">{ic("gap")}KI-Gap<span class="x-badge x-badge-d">Illustratives Beispiel</span></p>
    <div class="x-rings">{ring("m", 82, "Management")}{ring("t", 41, "Mitarbeitende")}</div>
    <div class="x-scale" aria-hidden="true"><div class="x-sc-track"><span class="x-sc-gap"></span><span class="x-sc-m t"><i></i><b>41</b></span><span class="x-sc-m m"><i></i><b>82</b></span></div>
      <div class="x-sc-ax"><span>0</span><span>25</span><span>50</span><span>75</span><span>100</span></div></div>
    <p class="x-gapline"><b>41 Punkte KI-Gap</b> zwischen Führungs- und Teamsicht. Illustratives Beispiel, keine Kundendaten.</p></div>
  <div class="x-viz x-rv"><p class="x-viz-h">{ic("layers")}Acht Signale</p><ul class="x-dims">{tiles}</ul>
    <ol class="x-steps3"><li><b>1</b>Acht Aussagen bewerten</li><li><b>2</b>Zwei Sichten angeben</li><li><b>3</b>KI-Gap erhalten</li></ol>
    <a class="btn btn-gold" href="/ki-readiness">KI-Gap messen {ARROW}</a></div>
</div>''')
    return _tile("x-dark x-dark2", "ki-title", inner, "ki")


# ---------------------------------------------------------------- 9 · Vorgehen
def vorgehen():
    steps = [("chat", "Schritt 1 · 20 bis 30 Minuten", "Erstgespräch", "Anlass, Ziel, Zielgruppe.", "Klarer Auftrag"),
             ("pencil", "Schritt 2", "Konzept", "Ziele, Inhalte, Format, Erfolgskriterien.", "Abgestimmtes Konzept"),
             ("users", "Schritt 3", "Umsetzung", "Entwicklung und Durchführung entlang der Fokusfelder.", "Durchgeführte Maßnahme"),
             ("trend", "Schritt 4", "Auswertung", "Wirkung prüfen, nächste Schritte klären.", "Wirkung und nächste Schritte")]
    lis = "".join(f'<li class="x-rv"><span class="x-node"><span>{ic(i)}</span></span><span class="x-when">{w}</span><h3>{t}</h3><p>{d}</p>'
                  f'<span class="x-out"><b>Ergebnis</b>{o}</span></li>' for i, w, t, d, o in steps)
    inner = _head("05 · Das Vorgehen", "Vier Schritte vom Gespräch zur Auswertung.", "", "vorgehen-title") + f'<ol class="x-time">{lis}</ol>'
    return _tile("x-light", "vorgehen-title", inner, "vorgehen")


# ---------------------------------------------------------------- 10 · Fachbegriffe (Definition per Klick)
def begriffe():
    import pages_glossar as G
    want = [("BATNA", "Alternative zum Verhandlungsergebnis (BATNA)"), ("ZOPA", "Verhandlungsspielraum (ZOPA)"), ("Anker", "Anker"),
            ("Rollenklarheit", "Rollenklarheit"), ("Entscheidungsrechte", "Entscheidungsrechte"), ("Umsetzungslücke", "Umsetzungslücke"),
            ("Cashflow", "Cashflow"), ("Business Case", "Business Case"), ("KI-Gap", "KI-Gap")]
    defs = {t[0]: t for t in G.terms()}
    chips, cards = [], []
    for k, (short, full) in enumerate(want):
        t = defs.get(full)
        if not t:
            continue
        sel = k == 0
        slug = G._slug(full)
        chips.append(f'<button class="x-term{" on" if sel else ""}" type="button" aria-pressed="{"true" if sel else "false"}" data-t="{k}">{short}</button>')
        cards.append(f'<div class="x-def{" on" if sel else ""}" data-t="{k}"{"" if sel else " hidden"}><p class="x-eyebrow">{t[3]}</p><h3>{esc(full)}</h3>'
                     f'<p>{esc(t[1])}</p><a class="link-arrow" href="/glossar#{slug}">Im Glossar {ARROW}</a></div>')
    inner = (_head("Fachbegriffe", "Neun Begriffe, die Entscheidungen tragen.", "Kurz erklärt, mit Link ins Glossar.", "begriffe-title")
             + f'<div class="x-gloss"><div class="x-terms-row x-rv">{"".join(chips)}</div><div class="x-defs x-rv" aria-live="polite">{"".join(cards)}</div></div>')
    return _tile("x-cream", "begriffe-title", inner, "begriffe")


# ---------------------------------------------------------------- 11 · FAQ
def faq(page):
    inner = (_head("Häufige Fragen", "Antworten in Kürze.", "", "faq-title")
             + f'<div class="x-faq x-rv">{faq_block(page["faqs"])}</div><p class="x-small">Weitere Antworten: <a href="/faq">FAQ</a>.</p>')
    return _tile("x-light", "faq-title", inner, "faq")


# ---------------------------------------------------------------- 12 · Abschluss
def closing():
    avatars = "".join(f'<a class="x-av" href="/kontakt"><img src="{esc(PARTNERS[k]["img_sm"])}" alt="" width="72" height="72" loading="lazy" decoding="async">'
                      f'<span><b>{esc(PARTNERS[k]["name"])}</b><small>{esc(PARTNERS[k]["focus"])}</small></span></a>'
                      for k in ("constantin-schubart", "oliver-meschkat", "marcel-dulgeridis"))
    return f"""<section class="x-close" aria-labelledby="close-title"><div class="container x-close-in">
<div class="x-rv"><p class="x-eyebrow">Der nächste Schritt</p><h2 id="close-title">Entwicklung, die in Ihrer Organisation ankommt.</h2>
<p class="x-lead">Kostenloses Erstgespräch, 20 bis 30 Minuten, per Microsoft Teams.</p>
<div class="x-ctas"><a class="btn btn-gold" href="/kontakt">Erstgespräch vereinbaren {ARROW}</a>
<a class="link-arrow x-on-dark" href="mailto:{SITE['email']}?subject=Anfrage%20THE%20GAP%20Lab">{ic('mail')}{SITE['email']}</a></div></div>
<div class="x-avs x-rv">{avatars}</div></div></section>"""


def home_body(page):
    return "".join([hero(), numbers(), kurz(), problem(), stages(), fokus(), innolab(), ki(), vorgehen(), begriffe(), faq(page), closing()])
