"""Visuelle Bausteine für THE GAP Lab: Modelle und Diagramme statt Textlisten.
Alle Inhalte stammen aus den bestehenden Seitentexten; Schemata sind als solche beschriftet, es gibt keine erfundenen Zahlen.
Keine Inline-Styles (CSP): Farben und Maße kommen aus assets/visual.css."""
from siteinfo import SITE, PARTNERS
from helpers import esc, ARROW

SD = SITE["parent_url"]
FIELDS = [
    ("f1", "/fokusfelder/verhandlungsfuehrung", "Verhandlungsführung &amp; Rhetorik", "Verhandeln", "oliver-meschkat",
     "Verhandlungen vorbereiten und überzeugend führen."),
    ("f2", "/fokusfelder/leadership-organisation", "Leadership &amp; Organisation", "Führen", "constantin-schubart",
     "Rollen, Erwartungen und Entscheidungswege klären."),
    ("f3", "/fokusfelder/finance-transformation", "Finance &amp; Transformation", "Wirtschaften", "marcel-dulgeridis",
     "Finanzwirkung verstehen, Veränderung wirtschaftlich umsetzen."),
]
STAGES = [
    ("konzeption", "Konzeption", "Was soll die Maßnahme bewirken, und für wen?",
     "Zielbild, Konzeptpapier mit Lernzielen und Ablauf, Format- und Zeitplan, Erfolgskriterien"),
    ("entwicklung", "Entwicklung", "Wie wird aus dem Konzept Praxis für die Teilnehmenden?",
     "Unterlagen, Übungen und Fallbeispiele, Leitfäden und Checklisten für den Transfer"),
    ("durchfuehrung", "Durchführung", "In welchem Format wirkt die Maßnahme am besten?",
     "Durchgeführte Maßnahme, Unterlagen, kurze Auswertung mit Empfehlungen"),
    ("vermarktung", "Vermarktung", "Wie werden Nutzen und Zielgruppe verständlich?",
     "Angebotsbeschreibung, Zielgruppenansprache, Informationsmaterial"),
]


def gap_bridge():
    breaks = [
        ("f1", "Verhandlungsführung", "Verhandlungen laufen ohne Strategie", "Ziele, Alternativen und Spielräume bleiben offen.", "/fokusfelder/verhandlungsfuehrung"),
        ("f2", "Leadership &amp; Organisation", "Führung bleibt unscharf", "Rollen und Entscheidungsrechte sind unklar.", "/fokusfelder/leadership-organisation"),
        ("f3", "Finance &amp; Transformation", "Zahlen werden nicht verstanden", "Entscheidungen ohne Bild der Finanzwirkung.", "/fokusfelder/finance-transformation"),
        ("f4", "Konzeption", "Maßnahmen passen nicht zur Zielgruppe", "Standardformate treffen die Zielgruppe nicht.", "/leistungen#konzeption"),
    ]
    cols = "".join(
        f'<li class="v-break {c}"><span class="v-bigno" aria-hidden="true">{i:02d}</span><span class="v-tagline">{t}</span>'
        f'<h3><a href="{href}">{h}</a></h3><p>{p}</p></li>'
        for i, (c, t, h, p, href) in enumerate(breaks, 1)
    )
    return (
        '<div class="v-gap">'
        f'<ol class="v-breaks">{cols}</ol></div>'
    )


def value_chain(with_links=True, results=True):
    lis = []
    for i, (aid, name, q, res) in enumerate(STAGES, 1):
        title = f'<a href="/leistungen#{aid}">{name}</a>' if with_links else name
        lis.append(
            f'<li class="v-stage s{i}"><div class="v-chev"><span>{i:02d} · Stufe</span><strong>{title}</strong></div>'
            f'<div class="v-stage-body"><div><span class="v-lab">Leitfrage</span><p>{q}</p></div>'
            + (f'<div><span class="v-lab">Ergebnis</span><p>{res}</p></div>' if results else "") + '</div></li>'
        )
    return '<ol class="v-chain">' + "".join(lis) + "</ol>"


def venn(with_links=True):
    svg = """<svg class="v-venn" viewBox="0 0 520 440" role="img" aria-labelledby="venn-t venn-d">
<title id="venn-t">Drei Disziplinen überschneiden sich in der Entscheidung</title>
<desc id="venn-d">Venn-Diagramm: Verhandeln, Führen und Wirtschaften überschneiden sich in der Entscheidung im Alltag.</desc>
<circle class="vn vn1" cx="190" cy="165" r="140"/><circle class="vn vn2" cx="330" cy="165" r="140"/><circle class="vn vn3" cx="260" cy="285" r="140"/>
<text class="vt" x="140" y="118" text-anchor="middle">Verhandeln</text>
<text class="vt" x="382" y="118" text-anchor="middle">Führen</text>
<text class="vt" x="260" y="378" text-anchor="middle">Wirtschaften</text>
<text class="vt vc" x="260" y="205" text-anchor="middle">Entscheidung</text><text class="vt vc" x="260" y="230" text-anchor="middle">im Alltag</text>
</svg>"""
    rows = []
    for c, path, name, short, key, text in FIELDS:
        p = PARTNERS[key]
        inner = (f'<span class="v-swatch {c}" aria-hidden="true"></span><img class="v-port" src="{esc(p["img"])}" alt="" width="72" height="72" loading="lazy" decoding="async"><span><strong>{name}</strong>'
                 f'<em>{esc(p["name"])}</em></span>')
        rows.append(f'<li><a class="v-frow {c}" href="{path}">{inner}</a></li>' if with_links else f'<li><div class="v-frow {c}">{inner}</div></li>')
    return f'<div class="v-venn-wrap">{svg}<ul class="v-flist">{"".join(rows)}</ul></div>'


def statements():
    items = [
        ("3", "Disziplinen, eine Gesellschaft", "Verhandlung, Führung und Finanzen greifen ineinander, statt in getrennten Projekten zu laufen."),
        ("3", "Partner mit Namen", "Zwei Professoren für BWL an der IU, ein promovierter Verhandlungsexperte."),
        ("1", "Verbund mit Beratung", f'Tochter der <a href="{SD}">Schubart &amp; Dulgeridis GmbH</a> mit forschungsbasierter Beratung und Diagnostik (THE GAP).'),
    ]
    return '<div class="v-statements">' + "".join(
        f'<div class="v-st"><span class="v-bignum">{n}</span><h3>{h}</h3><p>{p}</p></div>' for n, h, p in items) + "</div>"


def timeline(steps):
    lis = "".join(
        f'<li><span class="v-node" aria-hidden="true"></span><span class="v-when">{w}</span><strong>{h}</strong><p>{p}</p>'
        f'<span class="v-out"><b>Ergebnis</b> {o}</span></li>' for w, h, p, o in steps)
    return f'<ol class="v-timeline">{lis}</ol>'


def teasers():
    from pages_innolab import FORMATS, eur
    rows = "".join(
        f'<li><a href="/innolab#{f["id"]}"><span class="v-days" role="img" aria-label="{f["days"]} Tage">'
        + "".join('<i></i>' for _ in range(f["days"])) +
        f'</span><span class="v-fn">{esc(f["name"])}<small>{esc(f["kind"])}</small></span><span class="v-fp">{esc(f["dur"].replace(" vor Ort",""))}</span></a></li>'
        for f in FORMATS)
    demo = ('<div class="v-gapdemo" role="img" aria-label="Beispiel: Management bewertet 82, Mitarbeitende bewerten 41, Gap 41 Punkte">'
            '<div><span>Management</span><svg viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true"><rect class="tr" width="100" height="8"/><rect class="b1" width="82" height="8"/></svg><b>82</b></div>'
            '<div><span>Mitarbeitende</span><svg viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true"><rect class="tr" width="100" height="8"/><rect class="b2" width="41" height="8"/></svg><b>41</b></div>'
            '<p><strong>41 Punkte KI-Gap</strong> zwischen Führungs- und Teamsicht. Illustratives Beispiel, keine Kundendaten.</p></div>')
    return (
        '<div class="v-duo">'
        '<article class="v-panel"><p class="v-kick">InnoLab · Innovation, Change, Personalentwicklung</p>'
        '<h3>Fünf Formate vor Ort.</h3>'
        f'<ul class="v-minilist" aria-label="Formate mit Dauer und Preis">{rows}</ul>'
        f'<a class="btn btn-gold" href="/innolab">InnoLab ansehen {ARROW}</a></article>'
        '<article class="v-panel v-panel-dark"><p class="v-kick">KI-Readiness Check · kostenlos</p>'
        '<h3>Die KI-Lücke in drei Minuten sichtbar.</h3>'
        + demo
        + '<ol class="v-mini3" aria-label="So funktioniert der Check"><li><b>1</b>Acht Aussagen bewerten</li><li><b>2</b>Zwei Sichten angeben</li><li><b>3</b>KI-Gap erhalten</li></ol>'
        + f'<a class="btn btn-gold" href="/ki-readiness">KI-Gap messen {ARROW}</a></article></div>')


def measure_develop():
    return (
        '<div class="v-m2d"><div class="v-m2d-a"><span class="v-lab">Messen und beraten</span><h3>Diagnostik und Beratung</h3>'
        f'<p class="v-who">Schubart &amp; Dulgeridis GmbH</p><ul><li>THE GAP und Pulse-Check</li><li>Upskilling, Coaching, Recruiting</li></ul>'
        f'<a class="link-arrow" href="{SD}">Zur Muttergesellschaft {ARROW}</a></div>'
        '<div class="v-m2d-arrow" aria-hidden="true">' + ARROW + '</div>'
        '<div class="v-m2d-b"><span class="v-lab">Entwickeln</span><h3>Maßnahmen der Personalentwicklung</h3>'
        '<p class="v-who">The Gap Lab GmbH</p><ul><li>Konzeption bis Vermarktung</li><li>Verhandlung, Leadership, Finance</li></ul>'
        '<a class="link-arrow" href="/kontakt">Erstgespräch vereinbaren ' + ARROW + '</a></div></div>')


def decision_help():
    rows = [
        ("Noch unklar, was die Maßnahme bewirken soll und für wen", "konzeption", "Konzeption"),
        ("Konzept steht, aber Inhalte und Materialien fehlen oder passen nicht", "entwicklung", "Entwicklung"),
        ("Alles liegt vor, die Maßnahme soll mit hoher Qualität umgesetzt werden", "durchfuehrung", "Durchführung"),
        ("Gutes Angebot, aber Nutzen und Zielgruppe sind nicht verständlich beschrieben", "vermarktung", "Vermarktung"),
    ]
    lis = "".join(f'<li><span class="v-if">Wenn</span><span class="v-cond">{c}</span><span class="v-then" aria-hidden="true">{ARROW}</span>'
                  f'<a href="/leistungen#{a}"><span class="v-lab">Stufe {i}</span>{n}</a></li>' for i, (c, a, n) in enumerate(rows, 1))
    return f'<ul class="v-decide">{lis}</ul>'


def fokus_compare():
    cfg = {
        "f1": ("Wie gehe ich vorbereitet und überzeugend in das Gespräch?",
               ["Preis- und Konditionengespräche", "Vertragsverhandlungen", "Gespräche unter Druck"], ["Interessen", "BATNA", "ZOPA", "Anker"]),
        "f2": ("Wer entscheidet was, und wie kommt Strategie im Alltag an?",
               ["Neue Führungsrolle", "Strategie wird nicht gelebt", "Unklare Zuständigkeiten"], ["Rollenklarheit", "Entscheidungsrechte", "Führungskultur"]),
        "f3": ("Was bewirkt das Vorhaben finanziell, und trägt der Business Case?",
               ["Budgetverantwortung", "Veränderung ohne Business Case", "Zahlen ohne Entscheidung"], ["GuV", "Bilanz", "Cashflow", "Business Case"]),
    }
    cols = []
    for c, path, name, short, key, text in FIELDS:
        q, situ, terms = cfg[c]
        p = PARTNERS[key]
        cols.append(
            f'<article class="v-fc {c}"><header><span class="v-fc-n">{short}</span><h3><a href="{path}">{name}</a></h3></header>'
            f'<div><span class="v-lab">Leitfrage</span><p class="v-q">{q}</p></div>'
            f'<div><span class="v-lab">Zentrale Begriffe</span><ul class="v-terms">{"".join(f"<li>{t}</li>" for t in terms)}</ul></div>'
            f'<footer><img src="{esc(p["img"])}" alt="" width="56" height="56" loading="lazy" decoding="async"><span><strong>{esc(p["name"])}</strong><small>{esc(p["role"])}</small></span></footer></article>')
    return '<div class="v-fcmp">' + "".join(cols) + "</div>"


def zopa():
    return """<figure class="v-zopa"><figcaption><strong>Schema: Verhandlungsspielraum und Alternative</strong><span>Konzeptgrafik ohne Zahlenwerte, Beispiel: ein Preis zwischen Käufer- und Verkäuferseite.</span></figcaption>
<div class="v-zopa-grid">
<div class="v-zrow"><span class="v-zl">Käuferseite</span><div class="v-track"><i class="za"><b>bis zur Schmerzgrenze</b></i><em class="zm zma" title="BATNA Käuferseite"></em></div></div>
<div class="v-zrow"><span class="v-zl">Verkäuferseite</span><div class="v-track"><i class="zb"><b>ab der Schmerzgrenze</b></i><em class="zm zmb" title="BATNA Verkäuferseite"></em></div></div>
<div class="v-zband" aria-hidden="true"><span>Einigungsbereich (ZOPA)</span></div>
</div>
<div class="v-zaxis"><span>niedriger Preis</span><span>hoher Preis</span></div>
<p class="v-zleg"><em class="zm"></em> Die Marke zeigt die Alternative (BATNA): Wer eine gute Alternative hat, muss ein schlechtes Angebot nicht annehmen. Überschneiden sich die Spielräume nicht, ist eine Einigung unwahrscheinlich.</p></figure>"""


def impl_stack():
    layers = [("Strategie", "Das beschlossene Ziel und die Richtung."),
              ("Rollen und Entscheidungsrechte", "Wer welche Aufgaben, Verantwortung und Entscheidungen hat."),
              ("Führungskultur", "Was im Alltag tatsächlich belohnt, toleriert und besprochen wird."),
              ("Arbeitsalltag", "Was Teams tatsächlich tun und entscheiden.")]
    lis = "".join(f'<li class="l{i}"><strong>{t}</strong><span>{d}</span></li>' for i, (t, d) in enumerate(layers, 1))
    return (f'<figure class="v-stack"><figcaption><strong>Schema: Von der Strategie in den Alltag</strong><span>Konzeptgrafik: Je unschärfer die mittleren Ebenen, desto größer die Umsetzungslücke.</span></figcaption>'
            f'<div class="v-stack-in"><ol>{lis}</ol><div class="v-brace" aria-hidden="true"><span>Umsetzungslücke</span></div></div></figure>')


def finance_lenses():
    lenses = [("Gewinn- und Verlustrechnung", "Wurde im Zeitraum Gewinn oder Verlust erwirtschaftet?", "Zeitraum", "Erträge und Aufwendungen"),
              ("Bilanz", "Was besitzt das Unternehmen, und wie ist es finanziert?", "Stichtag", "Vermögen (Aktiva) und Kapital (Passiva)"),
              ("Cashflow", "Wie viel Geld ist tatsächlich zu- und abgeflossen?", "Zeitraum", "Zahlungsmittel, auch bei Gewinn ein möglicher Engpass")]
    cols = "".join(f'<div class="v-lens"><h3>{n}</h3><div><span class="v-lab">Leitfrage</span><p>{q}</p></div><div><span class="v-lab">Zeitbezug</span><p>{t}</p></div><div><span class="v-lab">Zeigt</span><p>{z}</p></div></div>' for n, q, t, z in lenses)
    eq = ('<div class="v-bc" role="group" aria-label="Aufbau eines Business Case"><span class="v-lab">Business Case</span><ul>'
          '<li>Kosten</li><li class="op" aria-hidden="true">+</li><li>Nutzen</li><li class="op" aria-hidden="true">+</li><li>Annahmen</li><li class="op" aria-hidden="true">+</li><li>Risiken</li>'
          '<li class="op" aria-hidden="true">=</li><li class="res">tragfähige Entscheidung</li></ul></div>')
    gc = ('<div class="v-gc" role="img" aria-label="Gewinn und Cashflow können zeitlich auseinanderfallen: Die Rechnung wird gestellt und erst später bezahlt">'
          '<span class="v-lab">Gewinn ist nicht gleich Cashflow</span><div><span class="e1"><b>Rechnung gestellt</b>Ertrag gebucht, Gewinn steigt</span><span class="gap">Zahlungsziel</span><span class="e2"><b>Zahlung eingegangen</b>Cashflow steigt</span></div>'
          '<p>Schema, keine Zahlen: Zwischen beiden Zeitpunkten kann ein Unternehmen Gewinn ausweisen und trotzdem Liquiditätsprobleme haben.</p></div>')
    return f'<div class="v-lenses">{cols}</div>{eq}{gc}'


def situations(items, cls):
    lis = "".join(f'<li><span class="v-lab">Situation</span><strong>{t}</strong><p>{d}</p></li>' for t, d in items)
    return f'<ol class="v-situ {cls}">{lis}</ol>'


def phases(cls, groups):
    cols = "".join(
        f'<div class="v-ph"><span class="v-phn">{i}</span><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul></div>'
        for i, (t, xs) in enumerate(groups, 1))
    return f'<div class="v-phases {cls}">{cols}</div>'


def org():
    p = PARTNERS
    kids = "".join(
        f'<li class="{c}"><span class="v-lab">{short}</span><h3><a href="{path}">{name}</a></h3><p><strong>{esc(p[key]["name"])}</strong><br>{esc(p[key]["role"])}</p></li>'
        for c, path, name, short, key, text in FIELDS)
    return (f'<figure class="v-org"><figcaption class="sr-only">Struktur: Muttergesellschaft, Tochtergesellschaft und drei Fokusfelder mit Partnern</figcaption>'
            f'<div class="v-o1"><span class="v-lab">Muttergesellschaft</span><h3><a href="{SD}">Schubart &amp; Dulgeridis GmbH</a></h3><p>Forschungsbasierte Beratung und Diagnostik</p></div>'
            '<div class="v-oline" aria-hidden="true"></div>'
            '<div class="v-o2"><span class="v-lab">Tochtergesellschaft · Altdorf bei Nürnberg</span><h3>The Gap Lab GmbH</h3><p>Maßnahmen der Personalentwicklung</p></div>'
            '<div class="v-oline v-oline2" aria-hidden="true"></div>'
            f'<ul class="v-okids">{kids}</ul></figure>')


def contact_flow():
    steps = [("1", "Termin wählen", "Freie Zeiten live."),
             ("2", "Einladung erhalten", "Outlook mit Teams-Link."),
             ("3", "Gespräch", "20 bis 30 Minuten, kostenlos."),
             ("4", "Angebot", "Nach Umfang.")]
    lis = "".join(f'<li><span class="v-n">{n}</span><strong>{h}</strong><p>{p}</p></li>' for n, h, p in steps)
    return f'<ol class="v-cflow">{lis}</ol>'


def checklist(items):
    return '<ul class="v-check">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


JOURNEY = [("/", "Verstehen", "Start"), ("/leistungen", "Leistungen", "Vier Stufen"), ("/fokusfelder", "Fokusfelder", "Drei Disziplinen"),
           ("/innolab", "Angebote", "InnoLab"), ("/ueber-uns", "Team", "Über uns"), ("/kontakt", "Gespräch", "Kontakt")]


def journey(current):
    """Roter Faden: sichtbare Reise über die Seiten, mit hervorgehobenem nächsten Schritt."""
    idx = next((i for i, (p, _, _) in enumerate(JOURNEY) if p == current), 0)
    lis = []
    for i, (path, step, name) in enumerate(JOURNEY):
        state = "done" if i < idx else ("now" if i == idx else ("next" if i == idx + 1 else "todo"))
        cur = ' aria-current="page"' if i == idx else ""
        lis.append(f'<li class="j-{state}"><a href="{path}"{cur}><span class="v-jn">{i + 1}</span><span class="v-jt"><b>{step}</b><small>{name}</small></span></a></li>')
    nxt = JOURNEY[idx + 1] if idx + 1 < len(JOURNEY) else None
    more = (f'<a class="btn" href="{nxt[0]}">Weiter: {nxt[2]} {ARROW}</a>' if nxt else "")
    return ('<section class="v-journey" aria-label="Ihr Weg durch THE GAP Lab"><div class="container"><p class="v-lab">Ihr Weg durch THE GAP Lab</p>'
            f'<ol>{"".join(lis)}</ol>{more}</div></section>')


def facts_strip(items, cls=""):
    return f'<dl class="v-facts {cls}">' + "".join(f"<div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in items) + "</dl>"


def innolab_strip():
    from pages_innolab import FORMATS, eur
    rows = "".join(
        f'<li><a href="/innolab#{f["id"]}"><span class="v-days" role="img" aria-label="{f["days"]} Tage">' + "".join("<i></i>" for _ in range(f["days"])) +
        f'</span><span class="v-fn">{esc(f["name"])}<small>{esc(f["kind"])} · {esc(f["people"])}</small></span><span class="v-fp">{esc(f["dur"].replace(" vor Ort",""))}</span></a></li>'
        for f in FORMATS)
    return ('<div class="v-iostrip"><div><p class="v-kick">InnoLab · konkret beauftragbar</p><h3>Fünf Formate vor Ort.</h3>'
            f'<a class="btn" href="/innolab">Alle Formate ansehen {ARROW}</a></div><ul class="v-minilist" aria-label="InnoLab-Formate">{rows}</ul></div>')


def related_formats(items):
    lis = "".join(f'<li><a href="{h}"><span class="v-lab">{k}</span><strong>{n}</strong></a></li>' for h, k, n, t in items)
    return f'<ul class="v-related">{lis}</ul>'


def partner_compact(key):
    p = PARTNERS[key]
    return (f'<div class="v-pc {FIELD_CLS.get(key, "f1")}"><img src="{esc(p["img"])}" alt="{esc(p["name"])}" width="96" height="96" loading="lazy" decoding="async">'
            f'<div><strong>{esc(p["name"])}</strong><span>{esc(p["role"])} · {esc(p["focus"])}</span>'
            f'<a class="link-arrow" href="/ueber-uns#{key}">Profil {ARROW}</a></div></div>')


FIELD_CLS = {"oliver-meschkat": "f1", "constantin-schubart": "f2", "marcel-dulgeridis": "f3"}


def hero_gap():
    """Hero-Grafik: Beschlossen und Im Alltag, dazwischen die Lücke, an der THE GAP Lab ansetzt."""
    return ('<figure class="v-hgap"><svg viewBox="0 0 480 360" role="img" aria-labelledby="hg-t hg-d">'
            '<title id="hg-t">Die Lücke zwischen Beschlossenem und Arbeitsalltag</title>'
            '<desc id="hg-d">Links der Block Beschlossen, rechts der Block Im Alltag, dazwischen eine unterbrochene Brücke mit der Marke THE GAP.</desc>'
            '<rect class="hg-l" x="14" y="120" width="176" height="210"/>'
            '<rect class="hg-r" x="290" y="120" width="176" height="210"/>'
            '<text class="hg-t1" x="102" y="215" text-anchor="middle">Beschlossen</text><text class="hg-t2" x="102" y="242" text-anchor="middle">Strategie · Konzept</text>'
            '<text class="hg-t3" x="378" y="215" text-anchor="middle">Im Alltag</text><text class="hg-t4" x="378" y="242" text-anchor="middle">Verhalten · Ergebnis</text>'
            '<path class="hg-b" d="M190 120H222M258 120H290"/>'
            '<path class="hg-tick" d="M222 106V134M258 106V134"/>'
            '<rect class="hg-d" x="233" y="107" width="14" height="14" transform="rotate(45 240 114)"/>'
            '<text class="hg-gap" x="240" y="70" text-anchor="middle">THE GAP</text>'
            '<rect class="hg-bar" x="218" y="82" width="44" height="3"/>'
            '</svg><figcaption>Hier setzt THE GAP Lab an: Beschlossenes kommt im Alltag an.</figcaption></figure>')


def numbers_band(items):
    return ('<section class="v-nums" aria-label="Das Wichtigste auf einen Blick"><div class="container"><ul>'
            + "".join(f'<li><b>{n}</b><span>{l}</span></li>' for n, l in items) + '</ul></div></section>')
