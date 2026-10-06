"""Kernseiten: Start, Leistungen, Fokusfelder-Übersicht, Über uns, Kontakt."""
from siteinfo import SITE, PARTNERS
from schema_nodes import person_nodes
from helpers import (esc, url_of, ARROW, btn, link_arrow, faq_block, partner_card, cta_band,
                     page_hero, section, head, answer_box)

SD = SITE["parent_url"]
BOOKING = SITE["booking_url"]
MAIL = f'<a href="mailto:{SITE["email"]}?subject=Anfrage%20THE%20GAP%20Lab">{SITE["email"]}</a>'
TEL = f'<a href="tel:{SITE["phone_e164"]}">{SITE["phone"]}</a>'

# ------------------------------------------------------------------ FAQ-Daten
FAQ_COMPANY = [
    ("Was macht die The Gap Lab GmbH?",
     "<p>The Gap Lab GmbH konzipiert, entwickelt und führt Maßnahmen der Personalentwicklung durch und vermarktet sie. "
     "Die Schwerpunkte sind <a href=\"/fokusfelder/verhandlungsfuehrung\">Verhandlungsführung &amp; Rhetorik</a>, "
     "<a href=\"/fokusfelder/leadership-organisation\">Leadership &amp; Organisation</a> sowie "
     "<a href=\"/fokusfelder/finance-transformation\">Finance &amp; Transformation</a>. Sitz der Gesellschaft ist Altdorf bei Nürnberg.</p>"),
    ("Wer steht hinter THE GAP Lab?",
     "<p>Geschäftsführer ist Prof. Dr. Constantin Schubart (laut Handelsregister einzelvertretungsberechtigt). "
     "Partner sind Dr. Oliver Meschkat (Verhandlungsführung &amp; Rhetorik) und Prof. Dr. Marcel Dulgeridis (Finance &amp; Transformation). "
     "THE GAP Lab ist eine Tochtergesellschaft der Schubart &amp; Dulgeridis GmbH. Mehr dazu auf <a href=\"/ueber-uns\">Über uns</a>.</p>"),
    ("Wie unterscheiden sich THE GAP Lab und die Schubart & Dulgeridis GmbH?",
     "<p>Die Schubart &amp; Dulgeridis GmbH ist auf forschungsbasierte Beratung und Diagnostik spezialisiert, zum Beispiel mit THE GAP, dem Pulse-Check, "
     "Re- und Upskilling-Programmen und Coaching. THE GAP Lab ist eine eigene Gesellschaft für Maßnahmen der Personalentwicklung mit den drei Fokusfeldern "
     "Verhandlungsführung, Leadership und Finance. Beide stehen im Verbund; Angebote der Muttergesellschaft finden Sie auf "
     f"<a href=\"{SD}\">schubart-dulgeridis.de</a>.</p>"),
    ("Für wen ist das Angebot gedacht?",
     "<p>Für Geschäftsleitungen, Personalverantwortliche und Führungskräfte, die Entwicklungsmaßnahmen gezielt planen, durchführen oder einkaufen möchten, "
     "etwa um Verhandlungskompetenz, Führungsklarheit oder Finanzverständnis in ihrer Organisation zu stärken.</p>"),
    ("Wo ist die Gesellschaft eingetragen?",
     f"<p>The Gap Lab GmbH hat ihren Sitz in {SITE['city']} (Geschäftsanschrift: {SITE['street']}, {SITE['zip']} Altdorf) und ist im Handelsregister B des "
     f"{SITE['court']} unter {SITE['hrb']} eingetragen. Tag der Eintragung: {SITE['registered']}.</p>"),
]

FAQ_COOPERATION = [
    ("Wie kommt eine Zusammenarbeit zustande?",
     "<p>Am Anfang steht ein kostenloses Erstgespräch von 20 bis 30 Minuten per Microsoft Teams. Dort klären wir Anlass, Ziel und Zielgruppe. "
     "Danach erhalten Sie ein Angebot mit klar beschriebenem Leistungsumfang. Den Termin buchen Sie auf der Seite <a href=\"/kontakt\">Kontakt</a>.</p>"),
    ("Was kostet eine Zusammenarbeit?",
     "<p>Wir nennen keine Pauschalpreise, weil Zielgruppe, Umfang und Format sehr unterschiedlich sein können. "
     "Nach dem Erstgespräch erhalten Sie ein individuelles Angebot nach Umfang.</p>"),
    ("Kann ich einzelne Leistungsstufen beauftragen?",
     "<p>Die Gesellschaft ist auf vier Stufen ausgerichtet: Konzeption, Entwicklung, Durchführung und Vermarktung von Maßnahmen. "
     "Ob Sie eine einzelne Stufe oder mehrere Stufen benötigen, klären wir im Erstgespräch anhand Ihrer Ausgangslage.</p>"),
    ("Wie läuft eine Maßnahme typischerweise ab?",
     "<p>Typisch ist ein Ablauf in vier Schritten: Ausgangslage klären, Konzept entwickeln, Maßnahme umsetzen, Wirkung gemeinsam auswerten. "
     "Umfang und Taktung richten sich nach Ziel und Zielgruppe. Details stehen auf der Seite <a href=\"/leistungen\">Leistungen</a>.</p>"),
]

FAQ_CONTACT = [
    ("Wie erreiche ich THE GAP Lab?",
     f"<p>Per E-Mail an {MAIL} oder telefonisch unter {TEL}. Während der Aufbauphase werden E-Mail und Telefon gemeinsam mit der Muttergesellschaft genutzt. "
     "Direkt buchbare Termine mit den Partnern finden Sie auf der Seite <a href=\"/kontakt\">Kontakt</a>.</p>"),
    ("Mit wem kann ich ein Erstgespräch führen?",
     "<p>Mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis. Die Terminbuchung läuft über die Kalender der Partner bei der Schubart &amp; Dulgeridis GmbH; "
     "freie Zeiten werden live angezeigt.</p>"),
]

FAQ_ALL = FAQ_COMPANY + FAQ_COOPERATION + FAQ_CONTACT
FAQ_HOME = [FAQ_COMPANY[0], FAQ_COMPANY[1], FAQ_COMPANY[2], FAQ_COOPERATION[0], FAQ_COOPERATION[1], FAQ_COMPANY[4]]


def home():
    page = {
        "path": "/", "short": "Start",
        "title": "THE GAP Lab — Personalentwicklung | Altdorf bei Nürnberg",
        "description": "The Gap Lab GmbH konzipiert, entwickelt und führt Maßnahmen der Personalentwicklung durch — mit Fokus auf Verhandlungsführung, Leadership und Finance.",
        "og_title": "THE GAP Lab — Personalentwicklung mit Verhandlungsstärke, Führungsklarheit und Finanzverständnis",
        "priority": "1.0", "changefreq": "weekly", "llms_group": "Unternehmen",
        "faqs": FAQ_HOME, "faq_schema": False, "show_stand": False,
    }

    hero = f"""
<section class="hero"><div class="container"><div class="hero-grid">
  <div>
    <p class="eyebrow">Personalentwicklung · Altdorf bei Nürnberg</p>
    <h1>Personalentwicklung, die <span class="accent">Verhandlungsstärke, Führungsklarheit und Finanzverständnis</span> verbindet.</h1>
    <p class="lead">The Gap Lab GmbH konzipiert, entwickelt und führt Maßnahmen der Personalentwicklung durch. Dahinter stehen drei Partner: zwei Professoren für Betriebswirtschaftslehre und ein promovierter Verhandlungsexperte.</p>
    <div class="hero-actions">
      <a class="btn" href="/kontakt">Erstgespräch vereinbaren {ARROW}</a>
      {link_arrow("/leistungen", "Leistungen ansehen")}
    </div>
    <p class="hero-note">Für Geschäftsleitungen, Personalverantwortliche und Führungskräfte, die Entwicklung gezielt steuern wollen. Das Erstgespräch ist kostenlos.</p>
  </div>
  <aside class="flow-card" aria-labelledby="flow-title">
    <h2 id="flow-title">Vom Konzept zur Maßnahme</h2>
    <ol class="flow-list">
      <li><div><strong>Konzeption</strong><span>Ziele, Zielgruppe und Rahmen klären.</span></div></li>
      <li><div><strong>Entwicklung</strong><span>Inhalte, Materialien und Übungen erarbeiten.</span></div></li>
      <li><div><strong>Durchführung</strong><span>Maßnahmen umsetzen und begleiten.</span></div></li>
      <li><div><strong>Vermarktung</strong><span>Angebote klar beschreiben und in den Markt bringen.</span></div></li>
    </ol>
    <div class="flow-foot"><strong>Vier Stufen, eine Gesellschaft.</strong>So ist der Unternehmensgegenstand im Handelsregister formuliert ({SITE['hrb']}, {SITE['court']}).</div>
  </aside>
</div></div></section>
"""

    trust = f"""
<section class="trust" aria-label="Fakten zur Gesellschaft"><div class="container"><div class="trust-grid">
  <div class="trust-item"><strong>{SITE['hrb']}</strong><span>{SITE['court']}, eingetragen am {SITE['registered']}</span></div>
  <div class="trust-item"><strong>{SITE['city']}</strong><span>Sitz und Geschäftsanschrift der Gesellschaft</span></div>
  <div class="trust-item"><strong>Drei Partner</strong><span>Zwei Professoren (BWL) und ein promovierter Verhandlungsexperte</span></div>
  <div class="trust-item"><strong>Im Verbund mit S&amp;D</strong><span>Tochtergesellschaft der Schubart &amp; Dulgeridis GmbH</span></div>
</div></div></section>
"""

    problem = section(
        head("Ausgangslage", "Wenn Entwicklung im Arbeitsalltag nicht ankommt",
             "Viele Organisationen investieren in Trainings und Programme und sehen im Alltag wenig davon. Typische Muster:", "problem-title")
        + """<ul class="feature-list">
  <li><strong>Verhandlungen laufen ohne Strategie</strong><span>Entscheider verhandeln mit Kunden, Lieferanten oder intern, ohne Ziele, Alternativen und Spielräume vorab zu klären. Das Ergebnis sind Zugeständnisse, die vermeidbar gewesen wären.</span></li>
  <li><strong>Führung bleibt unscharf</strong><span>Rollen, Entscheidungsrechte und Erwartungen sind nicht eindeutig. Beschlossene Strategie und gelebte Kultur laufen auseinander.</span></li>
  <li><strong>Zahlen werden nicht verstanden</strong><span>Führungskräfte entscheiden über Budgets und Veränderungen, ohne die finanzielle Wirkung belastbar einschätzen zu können.</span></li>
  <li><strong>Maßnahmen passen nicht zur Zielgruppe</strong><span>Standardformate treffen nicht die Situation der Teilnehmenden und bleiben deshalb ohne Wirkung im Alltag.</span></li>
</ul>""", "", "problem-title")

    leistungen = section(
        head("Leistungen", "Vier Stufen von der Konzeption bis zur Vermarktung",
             "Jede Stufe beantwortet eine andere Frage. Sie können sie einzeln oder verbunden betrachten.", "leistungen-title")
        + """<div class="grid grid-4">
  <a class="card card-link" href="/leistungen#konzeption"><span class="tag">Stufe 1</span><h3>Konzeption</h3><p>Was soll die Maßnahme bewirken, und für wen? Ergebnis: ein Konzept mit Zielen, Zielgruppe, Format und Erfolgskriterien.</p><span class="more">Mehr erfahren</span></a>
  <a class="card card-link" href="/leistungen#entwicklung"><span class="tag">Stufe 2</span><h3>Entwicklung</h3><p>Aus dem Konzept werden Inhalte, Materialien und Übungen, abgestimmt auf die Praxis der Teilnehmenden.</p><span class="more">Mehr erfahren</span></a>
  <a class="card card-link" href="/leistungen#durchfuehrung"><span class="tag">Stufe 3</span><h3>Durchführung</h3><p>Die Maßnahme wird in dem Format umgesetzt, das zu Ausgangslage und Ziel passt.</p><span class="more">Mehr erfahren</span></a>
  <a class="card card-link" href="/leistungen#vermarktung"><span class="tag">Stufe 4</span><h3>Vermarktung</h3><p>Maßnahmen werden als verständliches Angebot beschrieben, damit Zielgruppe und Nutzen klar sind.</p><span class="more">Mehr erfahren</span></a>
</div>""", "section-white", "leistungen-title")

    fokus = section(
        head("Fokusfelder", "Drei Disziplinen, die im Alltag zusammenhängen",
             "Verhandeln, Führen und Wirtschaften treffen bei Entscheidern in denselben Situationen aufeinander. Jedes Fokusfeld hat einen klar benannten Ansprechpartner.", "fokus-title")
        + f"""<div class="grid grid-3">
  <a class="card card-link" href="/fokusfelder/verhandlungsfuehrung"><span class="tag">Fokusfeld</span><h3>Verhandlungsführung &amp; Rhetorik</h3><p>Verhandlungen vorbereiten, führen und überzeugend argumentieren, auch in kritischen Gesprächen.</p><p class="small"><strong>{esc(PARTNERS['oliver-meschkat']['name'])}</strong></p><span class="more">Fokusfeld ansehen</span></a>
  <a class="card card-link" href="/fokusfelder/leadership-organisation"><span class="tag">Fokusfeld</span><h3>Leadership &amp; Organisation</h3><p>Rollen, Erwartungen und Entscheidungswege klären, im Zusammenspiel von Strategie, Kultur und Führung.</p><p class="small"><strong>{esc(PARTNERS['constantin-schubart']['name'])}</strong></p><span class="more">Fokusfeld ansehen</span></a>
  <a class="card card-link" href="/fokusfelder/finance-transformation"><span class="tag">Fokusfeld</span><h3>Finance &amp; Transformation</h3><p>Finanzielle Zusammenhänge verstehen und Veränderung wirtschaftlich fundiert umsetzen.</p><p class="small"><strong>{esc(PARTNERS['marcel-dulgeridis']['name'])}</strong></p><span class="more">Fokusfeld ansehen</span></a>
</div>""", "", "fokus-title")

    warum = section(
        head("Warum THE GAP Lab", "Was die Gesellschaft von einer Einzelmaßnahme unterscheidet", "", "warum-title")
        + f"""<ul class="feature-list">
  <li><strong>Drei Disziplinen in einer Gesellschaft</strong><span>Verhandlung, Führung und Finanzen greifen in einer Gesellschaft ineinander, statt in getrennten Projekten mit getrennten Ansprechpartnern behandelt zu werden.</span></li>
  <li><strong>Namentlich bekannte Verantwortliche</strong><span>Die Partner sind öffentlich benannt. Zwei sind Professoren für Betriebswirtschaftslehre an der IU Internationalen Hochschule, einer ist promoviert und auf Verhandlungsführung spezialisiert.</span></li>
  <li><strong>Verbund mit forschungsbasierter Beratung</strong><span>Als Tochtergesellschaft steht THE GAP Lab im Verbund mit der <a href="{SD}">Schubart &amp; Dulgeridis GmbH</a>, die forschungsbasierte Beratung und Diagnostik anbietet (THE GAP).</span></li>
</ul>""", "section-white", "warum-title")

    vorgehen = section(
        head("Vorgehen", "So läuft eine Zusammenarbeit typischerweise ab",
             "Umfang und Taktung richten sich nach Ihrer Ausgangslage. Der Ablauf bleibt in der Struktur gleich.", "vorgehen-title")
        + """<ol class="steps">
  <li><strong>Erstgespräch</strong><span>20 bis 30 Minuten: Anlass, Ziel und Zielgruppe klären. Kostenlos und unverbindlich.</span></li>
  <li><strong>Konzept</strong><span>Wir leiten ein Konzept mit Zielen, Inhalten, Format und Erfolgskriterien ab und stimmen es mit Ihnen ab.</span></li>
  <li><strong>Umsetzung</strong><span>Inhalte werden entwickelt und die Maßnahme wird durchgeführt, entlang der Fokusfelder der Partner.</span></li>
  <li><strong>Auswertung</strong><span>Gemeinsam prüfen wir, was die Maßnahme bewirkt hat und welche nächsten Schritte sinnvoll sind.</span></li>
</ol>""", "", "vorgehen-title")

    partner = section(
        head("Partner", "Drei Partner, ein Ansprechkreis",
             "Constantin Schubart ist Geschäftsführer der Gesellschaft. Oliver Meschkat und Marcel Dulgeridis sind Partner.", "partner-title")
        + '<div class="grid grid-3">'
        + partner_card("constantin-schubart") + partner_card("oliver-meschkat") + partner_card("marcel-dulgeridis")
        + "</div>", "section-cream", "partner-title")

    faq = section(
        head("Häufige Fragen", "Antworten auf die wichtigsten Fragen", "", "faq-title")
        + faq_block(FAQ_HOME)
        + f'<p class="small">Weitere Antworten finden Sie in den <a href="/faq">FAQ</a>.</p>', "", "faq-title")

    cta = cta_band("Welche Entwicklung soll in Ihrer Organisation ankommen?",
                   "Sprechen Sie 20 bis 30 Minuten mit einem der Partner: kostenlos, unverbindlich, per Microsoft Teams.",
                   secondary="Die Terminbuchung läuft über die Kalender der Partner bei der Schubart &amp; Dulgeridis GmbH.")

    page["body"] = hero + trust + problem + leistungen + fokus + warum + vorgehen + partner + faq + cta
    return page


def leistungen():
    page = {
        "path": "/leistungen", "short": "Leistungen",
        "title": "Leistungen — Konzeption bis Vermarktung | THE GAP Lab",
        "description": "Vier Leistungsstufen für Maßnahmen der Personalentwicklung: Konzeption, Entwicklung, Durchführung und Vermarktung. Ablauf, mögliche Ergebnisse, FAQ.",
        "priority": "0.9", "llms_group": "Leistungen", "schema_type": "CollectionPage",
    }
    faqs = [
        ("Was bietet The Gap Lab GmbH an?",
         "<p>The Gap Lab GmbH konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung. Inhaltliche Schwerpunkte sind Verhandlungsführung &amp; Rhetorik, Leadership &amp; Organisation sowie Finance &amp; Transformation.</p>"),
        ("Muss ich alle vier Stufen beauftragen?",
         "<p>Nein. Ob Sie eine Stufe, mehrere Stufen oder die gesamte Kette benötigen, hängt von Ihrer Ausgangslage ab. Das klären wir im kostenlosen Erstgespräch.</p>"),
        ("Welche Ergebnisse erhalte ich?",
         "<p>Je nach Stufe zum Beispiel ein Konzept mit Zielen und Erfolgskriterien, Arbeitsmaterialien und Übungen, eine durchgeführte Maßnahme mit Auswertung oder eine verständliche Angebotsbeschreibung. Den genauen Umfang halten wir im Angebot fest.</p>"),
        ("Bieten Sie auch Diagnostik an?",
         f"<p>Diagnostik wie THE GAP und der Pulse-Check gehört zur Schubart &amp; Dulgeridis GmbH. THE GAP Lab konzentriert sich auf Maßnahmen der Personalentwicklung. Mehr zur Diagnostik: <a href=\"{SD}the-gap\">schubart-dulgeridis.de/the-gap</a>.</p>"),
    ]
    page["faqs"] = faqs

    def service(num, anchor, title, ausgang, tun, ergebnisse, geeignet):
        erg = "".join(f"<li>{e}</li>" for e in ergebnisse)
        return f"""<article class="service" id="{anchor}">
  <div><span class="num">Stufe {num}</span><h2>{title}</h2></div>
  <div class="service-body">
    <h3>Ausgangslage</h3><p>{ausgang}</p>
    <h3>Was wir tun</h3><p>{tun}</p>
    <h3>Mögliche Ergebnisse</h3><ul>{erg}</ul>
    <h3>Geeignet, wenn</h3><p>{geeignet}</p>
  </div>
</article>"""

    services = (
        service(1, "konzeption", "Konzeption",
                "Eine Entwicklungsmaßnahme soll etwas bewirken, aber niemand hat festgelegt, was genau und für wen.",
                "Wir klären Anlass, Ziel und Zielgruppe, sichten vorhandene Programme und leiten daraus ein Konzept ab: Lernziele, Inhalte, Format, Ablauf und Kriterien, an denen sich der Erfolg messen lässt.",
                ["Zielbild und Zielgruppenbeschreibung", "Konzeptpapier mit Lernzielen, Inhalten und Ablauf", "Format- und Zeitplan", "Erfolgskriterien"],
                "eine Maßnahme neu aufgesetzt oder eine bestehende überarbeitet werden soll.")
        + service(2, "entwicklung", "Entwicklung",
                  "Das Konzept steht, aber Inhalte und Materialien fehlen oder passen nicht zur Zielgruppe.",
                  "Wir erarbeiten Inhalte, Übungen, Fallbeispiele und Arbeitsmaterialien und schneiden sie auf die Praxis der Teilnehmenden zu. Die fachliche Tiefe kommt aus den Fokusfeldern der Partner.",
                  ["Unterlagen für Workshop oder Training", "Übungen und Fallbeispiele", "Leitfäden und Checklisten für den Transfer in den Alltag", "Ablaufplan für die Durchführung"],
                  "bisherige Materialien zu allgemein sind und nicht zur Situation Ihrer Zielgruppe passen.")
        + service(3, "durchfuehrung", "Durchführung",
                  "Die Maßnahme soll umgesetzt werden, mit hoher fachlicher Qualität und klarem Praxisbezug.",
                  "Wir führen die Maßnahme im vereinbarten Format durch, zum Beispiel als Workshop, Training oder Begleitung. Die Umsetzung übernehmen die Partner entlang ihrer Fokusfelder. Format, Dauer und Ort stimmen wir mit Ihnen ab.",
                  ["Durchgeführte Maßnahme", "Unterlagen für die Teilnehmenden", "Kurze Auswertung mit Empfehlungen für die nächsten Schritte"],
                  "Führungskräfte oder Teams in konkreten Situationen handlungsfähiger werden sollen.")
        + service(4, "vermarktung", "Vermarktung",
                  "Gute Maßnahmen bleiben unsichtbar, wenn Angebot, Nutzen und Zielgruppe nicht klar beschrieben sind.",
                  "Wir bereiten Maßnahmen als verständliches Angebot auf und bringen sie in den Markt: mit klarer Beschreibung von Nutzen, Zielgruppe und Ablauf.",
                  ["Angebotsbeschreibungen", "Zielgruppenansprache", "Informationsmaterial"],
                  "Sie ein Entwicklungsangebot verständlich beschreiben und platzieren möchten.")
    )

    body = (
        page_hero(page, "Leistungen von der Konzeption bis zur Vermarktung",
                  "The Gap Lab GmbH deckt vier Stufen ab, in denen Maßnahmen der Personalentwicklung entstehen und wirken.")
        + section(
            answer_box("Kurzantwort: Was bietet The Gap Lab an?",
                       "The Gap Lab GmbH konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung. Inhaltlich arbeiten die Partner in drei Fokusfeldern: Verhandlungsführung &amp; Rhetorik, Leadership &amp; Organisation sowie Finance &amp; Transformation.")
            + services, "", "")
        + section(
            head("Fokusfelder", "Wo die Stufen inhaltlich ansetzen", "Jede Stufe lässt sich auf eines oder mehrere der drei Fokusfelder beziehen.")
            + '<ul class="chips"><li><a href="/fokusfelder/verhandlungsfuehrung">Verhandlungsführung &amp; Rhetorik</a></li>'
              '<li><a href="/fokusfelder/leadership-organisation">Leadership &amp; Organisation</a></li>'
              '<li><a href="/fokusfelder/finance-transformation">Finance &amp; Transformation</a></li></ul>', "section-white", "")
        + section(
            head("Abgrenzung", "THE GAP Lab und die Muttergesellschaft",
                 f"Diagnostik wie THE GAP und der Pulse-Check, Re- und Upskilling-Programme, Coaching und Recruiting gehören zur <a href=\"{SD}\">Schubart &amp; Dulgeridis GmbH</a>. "
                 "THE GAP Lab konzentriert sich auf Maßnahmen der Personalentwicklung in den drei Fokusfeldern. Wenn Sie zuerst messen möchten, wo Anspruch und Alltag auseinanderliegen, ist die Diagnostik der Muttergesellschaft der passende Einstieg."), "", "")
        + section(
            head("Häufige Fragen", "Fragen zu den Leistungen") + faq_block(faqs), "section-white", "")
        + cta_band("Welche Stufe brauchen Sie?", "Im Erstgespräch klären wir, wo Ihre Ausgangslage liegt und welche Stufen sinnvoll sind.")
    )
    page["body"] = body
    page["schema_nodes"] = [{
        "@type": "Service", "@id": url_of("/leistungen") + "#service",
        "name": "Maßnahmen der Personalentwicklung: Konzeption, Entwicklung, Durchführung, Vermarktung",
        "serviceType": "Personalentwicklung",
        "provider": {"@id": f"{SITE['domain']}/#organization"},
        "description": "Konzeption, Entwicklung, Durchführung und Vermarktung von Maßnahmen der Personalentwicklung in den Fokusfeldern Verhandlungsführung & Rhetorik, Leadership & Organisation sowie Finance & Transformation.",
        "audience": {"@type": "Audience", "audienceType": "Geschäftsleitungen, Personalverantwortliche, Führungskräfte"},
        "url": url_of("/leistungen"),
    }]
    return page


def fokusfelder_hub():
    page = {
        "path": "/fokusfelder", "short": "Fokusfelder",
        "title": "Fokusfelder — Verhandlung, Leadership, Finance | THE GAP Lab",
        "description": "Die drei Fokusfelder von THE GAP Lab: Verhandlungsführung & Rhetorik, Leadership & Organisation, Finance & Transformation — mit Ansprechpartnern.",
        "priority": "0.8", "llms_group": "Fokusfelder", "schema_type": "CollectionPage",
    }
    page["body"] = (
        page_hero(page, "Drei Fokusfelder, drei Ansprechpartner",
                  "Verhandeln, Führen und Wirtschaften hängen im Alltag von Entscheidern zusammen. THE GAP Lab behandelt sie in einer Gesellschaft, jeweils mit einem benannten Partner.")
        + section(
            answer_box("Kurzantwort: In welchen Themenfeldern arbeitet THE GAP Lab?",
                       "In drei Fokusfeldern: Verhandlungsführung &amp; Rhetorik (Dr. Oliver Meschkat), Leadership &amp; Organisation (Prof. Dr. Constantin Schubart) sowie Finance &amp; Transformation (Prof. Dr. Marcel Dulgeridis).")
            + f"""<div class="grid grid-3">
  <a class="card card-link" href="/fokusfelder/verhandlungsfuehrung"><span class="tag">Fokusfeld 1</span><h2 class="card-title">Verhandlungsführung &amp; Rhetorik</h2><p>Interessen klären, Alternativen kennen, Gespräche steuern und überzeugend argumentieren.</p><p class="small"><strong>Ansprechpartner:</strong> {esc(PARTNERS['oliver-meschkat']['name'])}</p><span class="more">Fokusfeld ansehen</span></a>
  <a class="card card-link" href="/fokusfelder/leadership-organisation"><span class="tag">Fokusfeld 2</span><h2 class="card-title">Leadership &amp; Organisation</h2><p>Rollen, Entscheidungswege und Erwartungen klären und Strategie im Alltag verankern.</p><p class="small"><strong>Ansprechpartner:</strong> {esc(PARTNERS['constantin-schubart']['name'])}</p><span class="more">Fokusfeld ansehen</span></a>
  <a class="card card-link" href="/fokusfelder/finance-transformation"><span class="tag">Fokusfeld 3</span><h2 class="card-title">Finance &amp; Transformation</h2><p>Kennzahlen verstehen, Wirtschaftlichkeit bewerten und Veränderung finanziell fundiert umsetzen.</p><p class="small"><strong>Ansprechpartner:</strong> {esc(PARTNERS['marcel-dulgeridis']['name'])}</p><span class="more">Fokusfeld ansehen</span></a>
</div>""", "", "")
        + cta_band("Nicht sicher, welches Fokusfeld passt?", "Im Erstgespräch ordnen wir Ihre Ausgangslage gemeinsam ein.")
    )
    return page


def ueber_uns():
    page = {
        "path": "/ueber-uns", "short": "Über uns",
        "title": "Über uns — Drei Partner, eine Gesellschaft | THE GAP Lab",
        "description": "Wer steht hinter THE GAP Lab? Gesellschaftsdaten, Geschäftsführer, die drei Partner und der Verbund mit der Schubart & Dulgeridis GmbH.",
        "priority": "0.8", "llms_group": "Unternehmen", "schema_type": "AboutPage",
    }
    page["schema_nodes"] = person_nodes()

    facts = f"""<div class="table-wrap"><table class="facts"><tbody>
<tr><th scope="row">Firma</th><td>{SITE['legal_name']} (Marke: THE GAP Lab)</td></tr>
<tr><th scope="row">Rechtsform</th><td>Gesellschaft mit beschränkter Haftung</td></tr>
<tr><th scope="row">Sitz</th><td>{SITE['city']}</td></tr>
<tr><th scope="row">Geschäftsanschrift</th><td>{SITE['street']}, {SITE['zip']} Altdorf</td></tr>
<tr><th scope="row">Handelsregister</th><td>{SITE['hrb']}, {SITE['court']}</td></tr>
<tr><th scope="row">Gesellschaftsvertrag</th><td>vom {SITE['articles_date']}</td></tr>
<tr><th scope="row">Eintragung</th><td>{SITE['registered']}</td></tr>
<tr><th scope="row">Geschäftsführer</th><td>Prof. Dr. Constantin Schubart (einzelvertretungsberechtigt)</td></tr>
<tr><th scope="row">Muttergesellschaft</th><td><a href="{SD}">{SITE['parent_name']}</a></td></tr>
</tbody></table></div>"""

    def wide(key):
        p = PARTNERS[key]
        return f"""<article class="partner-wide" id="{key}">
  <div class="photo"><img src="{esc(p['img'])}" alt="{esc(p['name'])}" width="448" height="448" loading="lazy" decoding="async"></div>
  <div>
    <span class="role">{esc(p['role'])} · {esc(p['focus'])}</span>
    <h3>{esc(p['name'])}</h3>
    <p>{esc(p['long_bio'])}</p>
    <div class="hero-actions">
      {link_arrow(p['fokus_path'], 'Fokusfeld ansehen')}
      <a class="link-arrow" href="{esc(p['sd_url'])}">Profil bei Schubart &amp; Dulgeridis</a>
      <a class="link-arrow" href="{esc(p['linkedin'])}" rel="noopener noreferrer">LinkedIn</a>
    </div>
  </div>
</article>"""

    page["body"] = (
        page_hero(page, "Drei Partner, eine Gesellschaft für Personalentwicklung",
                  "The Gap Lab GmbH ist eine Tochtergesellschaft der Schubart &amp; Dulgeridis GmbH. Hier steht, wer dahintersteht und wie die Gesellschaft aufgestellt ist.")
        + section(
            answer_box("Kurzantwort: Wer ist THE GAP Lab?",
                       f"THE GAP Lab ist die Marke der The Gap Lab GmbH mit Sitz in {SITE['city']}, eingetragen im Handelsregister B des {SITE['court_gen']} unter {SITE['hrb']}. "
                       "Die Gesellschaft konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung. Geschäftsführer ist Prof. Dr. Constantin Schubart; Partner sind Dr. Oliver Meschkat und Prof. Dr. Marcel Dulgeridis.")
            + '<div class="split"><div>' + head("Warum es die Gesellschaft gibt", "Ein eigenes Feld für Personalentwicklung", "", "warum-title")
            + '</div><div class="prose">'
              "<p>Der Gesellschaftszweck beschreibt eine Kette: Maßnahmen der Personalentwicklung werden konzipiert, entwickelt, durchgeführt und vermarktet. "
              "THE GAP Lab gibt dieser Kette eine eigene Gesellschaft.</p>"
              "<p>Inhaltlich stehen drei Disziplinen im Mittelpunkt, die in der Praxis von Entscheidern zusammenhängen: "
              "<strong>Verhandlungsführung &amp; Rhetorik</strong>, <strong>Leadership &amp; Organisation</strong> und <strong>Finance &amp; Transformation</strong>. "
              "Jede Disziplin hat einen Partner, der sie fachlich verantwortet.</p>"
              f"<p>Die Gesellschaft steht im Verbund mit der <a href=\"{SD}\">Schubart &amp; Dulgeridis GmbH</a>, die forschungsbasierte Beratung und Diagnostik anbietet.</p>"
              "</div></div>", "", "")
        + section(head("Die Partner", "Wer hinter THE GAP Lab steht",
                       "Alle Angaben entsprechen den veröffentlichten Profilen auf schubart-dulgeridis.de.", "partner-title")
                  + '<div class="grid">' + wide("constantin-schubart") + wide("oliver-meschkat") + wide("marcel-dulgeridis") + "</div>",
                  "section-cream", "partner-title")
        + section(head("Gesellschaftsdaten", "Auf einen Blick",
                       "Quelle: Mitteilung des Registergerichts über die Eintragung im Handelsregister B.", "daten-title") + facts, "section-white", "daten-title")
        + cta_band("Lernen Sie uns im Gespräch kennen", "Das Erstgespräch dauert 20 bis 30 Minuten und ist kostenlos.")
    )
    return page


def kontakt():
    page = {
        "path": "/kontakt", "short": "Kontakt",
        "title": "Kontakt & Erstgespräch | THE GAP Lab",
        "description": "Kostenloses Erstgespräch (20–30 Min.) mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis buchen — oder per E-Mail und Telefon anfragen.",
        "priority": "0.9", "llms_group": "Unternehmen", "schema_type": "ContactPage",
        "faqs": FAQ_CONTACT, "faq_schema": True,
    }

    def booking(key):
        p = PARTNERS[key]
        first = {"constantin-schubart": "Constantin", "oliver-meschkat": "Oliver", "marcel-dulgeridis": "Marcel"}[key]
        return f"""<article class="card">
  <span class="tag">{esc(p['focus'])}</span>
  <h3>Erstgespräch mit {first}</h3>
  <p>{esc(p['name'])} · {esc(p['role'])}. 20 bis 30 Minuten per Microsoft Teams, kostenlos.</p>
  <a class="btn" href="{BOOKING}">Termin wählen {ARROW}</a>
</article>"""

    page["body"] = (
        page_hero(page, "Kontakt und Erstgespräch",
                  "Sprechen Sie 20 bis 30 Minuten mit einem der Partner. Das Gespräch ist kostenlos und unverbindlich.")
        + section(
            head("Termin buchen", "Wählen Sie Ihren Ansprechpartner",
                 "Die Buchung läuft über die Kalender der Partner bei der Schubart &amp; Dulgeridis GmbH. Dort wählen Sie die Person und sehen freie Zeiten live. Nach der Buchung erhalten Sie eine Outlook-Einladung mit Microsoft-Teams-Link.", "termin-title")
            + '<div class="grid grid-3">' + booking("constantin-schubart") + booking("oliver-meschkat") + booking("marcel-dulgeridis") + "</div>"
            + '<p class="small">Mit dem Klick verlassen Sie gap-lab.de und wechseln zur Website der Muttergesellschaft; dort gilt deren <a href="' + SD + 'datenschutz">Datenschutzerklärung</a>.</p>',
            "", "termin-title")
        + section(
            '<div class="contact-grid"><div>'
            + head("Direkt anfragen", "E-Mail und Telefon", "", "direkt-title")
            + f"""<ul class="contact-list">
  <li><span class="k">E-Mail</span>{MAIL}</li>
  <li><span class="k">Telefon</span>{TEL}</li>
  <li><span class="k">Anschrift</span>{SITE['legal_name']}<br>{SITE['street']}<br>{SITE['zip']} {SITE['city']}</li>
  <li><span class="k">Handelsregister</span>{SITE['hrb']}, {SITE['court']}</li>
</ul>
<p class="small muted">Während der Aufbauphase werden E-Mail und Telefon gemeinsam mit der Muttergesellschaft genutzt.</p>
</div><div>"""
            + head("Gut vorbereitet", "Was Sie für das Gespräch mitbringen können", "", "prep-title")
            + """<ul>
  <li><strong>Anlass und Ziel:</strong> Was soll sich in Ihrer Organisation verändern?</li>
  <li><strong>Zielgruppe:</strong> Wer soll teilnehmen, und wie viele Personen sind es ungefähr?</li>
  <li><strong>Zeitrahmen:</strong> Bis wann soll die Maßnahme wirken?</li>
  <li><strong>Bisherige Erfahrungen:</strong> Was wurde schon versucht, und was hat nicht funktioniert?</li>
</ul>
<p class="muted">Nichts davon ist Pflicht. Auch ein erstes Stichwort genügt.</p>
</div></div>""", "section-white", "")
        + section(head("Häufige Fragen", "Zum Kontakt") + faq_block(FAQ_CONTACT), "", "")
    )
    return page


def build():
    return [home(), leistungen(), fokusfelder_hub(), ueber_uns(), kontakt()]
