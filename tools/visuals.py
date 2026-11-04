"""Visuelle Bausteine für THE GAP Lab: Modelle und Diagramme statt Textlisten.
Alle Inhalte stammen aus den bestehenden Seitentexten; Schemata sind als solche beschriftet, es gibt keine erfundenen Zahlen.
Keine Inline-Styles (CSP): Farben und Maße kommen aus assets/visual.css."""
from siteinfo import SITE, PARTNERS
from helpers import esc, ARROW

SD = SITE["parent_url"]
FIELDS = [
    ("f1", "/fokusfelder/verhandlungsfuehrung", "Verhandlungsführung &amp; Rhetorik", "Verhandeln", "oliver-meschkat",
     "Verhandlungen vorbereiten, führen und überzeugend argumentieren, auch in kritischen Gesprächen."),
    ("f2", "/fokusfelder/leadership-organisation", "Leadership &amp; Organisation", "Führen", "constantin-schubart",
     "Rollen, Erwartungen und Entscheidungswege klären, im Zusammenspiel von Strategie, Kultur und Führung."),
    ("f3", "/fokusfelder/finance-transformation", "Finance &amp; Transformation", "Wirtschaften", "marcel-dulgeridis",
     "Finanzielle Zusammenhänge verstehen und Veränderung wirtschaftlich fundiert umsetzen."),
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
        ("f1", "Verhandlungsführung", "Verhandlungen laufen ohne Strategie", "Entscheider verhandeln mit Kunden, Lieferanten oder intern, ohne Ziele, Alternativen und Spielräume vorab zu klären. Das Ergebnis sind Zugeständnisse, die vermeidbar gewesen wären.", "/fokusfelder/verhandlungsfuehrung"),
        ("f2", "Leadership &amp; Organisation", "Führung bleibt unscharf", "Rollen, Entscheidungsrechte und Erwartungen sind nicht eindeutig. Beschlossene Strategie und gelebte Kultur laufen auseinander.", "/fokusfelder/leadership-organisation"),
        ("f3", "Finance &amp; Transformation", "Zahlen werden nicht verstanden", "Führungskräfte entscheiden über Budgets und Veränderungen, ohne die finanzielle Wirkung belastbar einschätzen zu können.", "/fokusfelder/finance-transformation"),
        ("f4", "Konzeption", "Maßnahmen passen nicht zur Zielgruppe", "Standardformate treffen nicht die Situation der Teilnehmenden und bleiben deshalb ohne Wirkung im Alltag.", "/leistungen#konzeption"),
    ]
    cols = "".join(
        f'<li class="v-break {c}"><span class="v-dot" aria-hidden="true"></span><span class="v-tagline">{t}</span>'
        f'<h3>{h}</h3><p>{p}</p><a class="link-arrow" href="{href}">Ansehen {ARROW}</a></li>'
        for c, t, h, p, href in breaks
    )
    return (
        '<div class="v-gap">'
        '<div class="v-gapline" aria-hidden="true"><span class="v-end">Beschlossen<small>Strategie, Konzept, Programm</small></span>'
        '<span class="v-bridge"><i>Hier geht Wirkung verloren</i></span>'
        '<span class="v-end v-end-r">Im Alltag<small>Verhalten, Entscheidungen, Ergebnisse</small></span></div>'
        f'<ol class="v-breaks">{cols}</ol></div>'
    )


def value_chain(with_links=True):
    lis = []
    for i, (aid, name, q, res) in enumerate(STAGES, 1):
        title = f'<a href="/leistungen#{aid}">{name}</a>' if with_links else name
        lis.append(
            f'<li class="v-stage s{i}"><div class="v-chev"><span>Stufe {i}</span><strong>{title}</strong></div>'
            f'<div class="v-stage-body"><div><span class="v-lab">Leitfrage</span><p>{q}</p></div>'
            f'<div><span class="v-lab">Ergebnis</span><p>{res}</p></div></div></li>'
        )
    return '<ol class="v-chain">' + "".join(lis) + "</ol>"


def venn(with_links=True):
    svg = """<svg class="v-venn" viewBox="0 0 520 440" role="img" aria-labelledby="venn-t venn-d">
<title id="venn-t">Drei Disziplinen überschneiden sich in der Entscheidung</title>
<desc id="venn-d">Venn-Diagramm: Verhandeln, Führen und Wirtschaften überschneiden sich in der Entscheidung im Alltag.</desc>
<circle class="vn vn1" cx="190" cy="165" r="140"/><circle class="vn vn2" cx="330" cy="165" r="140"/><circle class="vn vn3" cx="260" cy="285" r="140"/>
<text class="vt" x="128" y="120" text-anchor="middle">Verhandeln</text>
<text class="vt" x="392" y="120" text-anchor="middle">Führen</text>
<text class="vt" x="260" y="378" text-anchor="middle">Wirtschaften</text>
<text class="vt vc" x="260" y="205" text-anchor="middle">Entscheidung</text><text class="vt vc" x="260" y="230" text-anchor="middle">im Alltag</text>
</svg>"""
    rows = []
    for c, path, name, short, key, text in FIELDS:
        p = PARTNERS[key]
        inner = (f'<span class="v-swatch {c}" aria-hidden="true"></span><span><strong>{name}</strong>'
                 f'<small>{text}</small><em>{esc(p["name"])}</em></span>')
        rows.append(f'<li><a class="v-frow {c}" href="{path}">{inner}</a></li>' if with_links else f"<li>{inner}</li>")
    return f'<div class="v-venn-wrap">{svg}<ul class="v-flist">{"".join(rows)}</ul></div>'


def statements():
    items = [
        ("3", "Disziplinen in einer Gesellschaft", "Verhandlung, Führung und Finanzen greifen in einer Gesellschaft ineinander, statt in getrennten Projekten mit getrennten Ansprechpartnern behandelt zu werden."),
        ("3", "Partner mit Namen", "Die Partner sind öffentlich benannt. Zwei sind Professoren für Betriebswirtschaftslehre an der IU Internationalen Hochschule, einer ist promoviert und auf Verhandlungsführung spezialisiert."),
        ("1", "Verbund mit Beratung und Diagnostik", f'Als Tochtergesellschaft steht THE GAP Lab im Verbund mit der <a href="{SD}">Schubart &amp; Dulgeridis GmbH</a>, die forschungsbasierte Beratung und Diagnostik anbietet (THE GAP).'),
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
        f'</span><span class="v-fn">{esc(f["name"])}<small>{esc(f["kind"])}</small></span><span class="v-fp">{eur(f["price"])}</span></a></li>'
        for f in FORMATS)
    demo = ('<div class="v-gapdemo" role="img" aria-label="Beispiel: Management bewertet 82, Mitarbeitende bewerten 41, Gap 41 Punkte">'
            '<div><span>Management</span><svg viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true"><rect class="tr" width="100" height="8"/><rect class="b1" width="82" height="8"/></svg><b>82</b></div>'
            '<div><span>Mitarbeitende</span><svg viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true"><rect class="tr" width="100" height="8"/><rect class="b2" width="41" height="8"/></svg><b>41</b></div>'
            '<p><strong>41 Punkte KI-Gap</strong> zwischen Führungs- und Teamsicht. Illustratives Beispiel, keine Kundendaten.</p></div>')
    return (
        '<div class="v-duo">'
        '<article class="v-panel"><p class="v-kick">InnoLab · Innovation, Change, Personalentwicklung</p>'
        '<h3>Fünf Formate vor Ort, vom Sprint bis zur Scorecard.</h3>'
        '<p>Innovation, die im Unternehmen ankommt: zum Festpreis, mit konkreten Ergebnissen wie Prototyp, Entscheidungsvorlage oder Change-Fahrplan.</p>'
        f'<ul class="v-minilist" aria-label="Formate mit Dauer und Preis">{rows}</ul>'
        f'<a class="btn btn-gold" href="/innolab">InnoLab ansehen {ARROW}</a></article>'
        '<article class="v-panel v-panel-dark"><p class="v-kick">KI-Readiness Check · kostenlos</p>'
        '<h3>Ihre KI-Strategie steht. Steht Ihre Organisation auch?</h3>'
        '<p>In drei Minuten sehen Sie, wie groß die Lücke zwischen Führungsplan und Arbeitsalltag bei Ihrer KI-Einführung ist. Ohne Login, mit sofortigem Ergebnis.</p>'
        + demo + f'<a class="btn btn-gold" href="/ki-readiness">KI-Gap messen {ARROW}</a></article></div>')


def measure_develop():
    return (
        '<div class="v-m2d"><div class="v-m2d-a"><span class="v-lab">Messen und beraten</span><h3>Diagnostik und Beratung</h3>'
        f'<p class="v-who">Schubart &amp; Dulgeridis GmbH</p><ul><li>THE GAP und Pulse-Check</li><li>Re- und Upskilling-Programme</li><li>Coaching und Recruiting</li></ul>'
        f'<a class="link-arrow" href="{SD}">Zur Muttergesellschaft {ARROW}</a></div>'
        '<div class="v-m2d-arrow" aria-hidden="true">' + ARROW + '</div>'
        '<div class="v-m2d-b"><span class="v-lab">Entwickeln</span><h3>Maßnahmen der Personalentwicklung</h3>'
        '<p class="v-who">The Gap Lab GmbH</p><ul><li>Konzeption, Entwicklung, Durchführung, Vermarktung</li><li>Fokusfelder Verhandlung, Leadership, Finance</li><li>Format, Dauer und Ort nach Ihrer Ausgangslage</li></ul>'
        '<a class="link-arrow" href="/kontakt">Erstgespräch vereinbaren ' + ARROW + '</a></div></div>'
        '<p class="small muted">Wenn Sie zuerst messen möchten, wo Anspruch und Alltag auseinanderliegen, ist die Diagnostik der Muttergesellschaft der passende Einstieg.</p>')


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
            f'<div><span class="v-lab">Typische Situationen</span><ul>{"".join(f"<li>{s}</li>" for s in situ)}</ul></div>'
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
            '<div class="v-o2"><span class="v-lab">Tochtergesellschaft · Altdorf bei Nürnberg</span><h3>The Gap Lab GmbH</h3><p>Konzeption, Entwicklung, Durchführung und Vermarktung von Maßnahmen der Personalentwicklung. Geschäftsführer: Prof. Dr. Constantin Schubart.</p></div>'
            '<div class="v-oline v-oline2" aria-hidden="true"></div>'
            f'<ul class="v-okids">{kids}</ul></figure>')


def contact_flow():
    steps = [("1", "Partner und Termin wählen", "Freie Zeiten werden live angezeigt."),
             ("2", "Einladung erhalten", "Outlook-Einladung mit Microsoft-Teams-Link."),
             ("3", "Gespräch, 20 bis 30 Minuten", "Anlass, Ziel und Zielgruppe klären. Kostenlos und unverbindlich."),
             ("4", "Angebot", "Danach erhalten Sie ein Angebot nach Umfang.")]
    lis = "".join(f'<li><span class="v-n">{n}</span><strong>{h}</strong><p>{p}</p></li>' for n, h, p in steps)
    return f'<ol class="v-cflow">{lis}</ol>'


def checklist(items):
    return '<ul class="v-check">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
