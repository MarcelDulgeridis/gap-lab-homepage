"""Kernseiten: Start, Leistungen, Fokusfelder-Übersicht, Über uns, Kontakt."""
from siteinfo import SITE, PARTNERS
from schema_nodes import person_nodes
import visuals as V
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
     "<p>Geschäftsführer ist Prof. Dr. Constantin Schubart. "
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
    ("Wo sitzt THE GAP Lab?",
     f"<p>Die The Gap Lab GmbH hat ihren Sitz in {SITE['city']} ({SITE['street']}, {SITE['zip']} Altdorf). Die vollständigen Firmenangaben stehen im <a href=\"/impressum\">Impressum</a>.</p>"),
]

FAQ_COOPERATION = [
    ("Wie kommt eine Zusammenarbeit zustande?",
     "<p>Am Anfang steht ein kostenloses Erstgespräch von 20 bis 30 Minuten per Microsoft Teams. Dort klären wir Anlass, Ziel und Zielgruppe. "
     "Danach erhalten Sie ein Angebot mit klar beschriebenem Leistungsumfang. Den Termin buchen Sie auf der Seite <a href=\"/kontakt\">Kontakt</a>.</p>"),
    ("Was kostet eine Zusammenarbeit?",
     "<p>Für die <a href=\"/innolab#preise\">InnoLab-Formate</a> nennen wir Festpreise ab 5.800 € netto. Für alle anderen Maßnahmen gibt es keine Pauschalpreise, weil Zielgruppe, Umfang und Format sehr unterschiedlich sein können. "
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
    <div class="flow-foot"><strong>Vier Stufen, eine Gesellschaft.</strong>Von der Idee bis zum fertigen Angebot für Maßnahmen der Personalentwicklung.</div>
  </aside>
</div></div></section>
"""

    kurz = section(answer_box("Kurz erklärt: Was ist THE GAP Lab?",
        f"THE GAP Lab ist die Marke der The Gap Lab GmbH mit Sitz in {SITE['city']}. Die Gesellschaft konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung, "
        "damit Strategie im Arbeitsalltag ankommt. Drei Fokusfelder tragen die Arbeit: Verhandlungsführung &amp; Rhetorik, Leadership &amp; Organisation sowie Finance &amp; Transformation. "
        'Konkret beauftragbar sind die fünf <a href="/innolab">InnoLab-Formate</a>; für den Einstieg gibt es das kostenlose Erstgespräch und den <a href="/ki-readiness">KI-Readiness Check</a>.'),
        "v-tight", "")
    trust = f"""
<section class="trust" aria-label="Fakten zur Gesellschaft"><div class="container"><div class="trust-grid">
  <div class="trust-item"><strong>Kostenloses Erstgespräch</strong><span>20 bis 30 Minuten per Microsoft Teams mit einem der Partner</span></div>
  <div class="trust-item"><strong>{SITE['city']}</strong><span>Sitz und Geschäftsanschrift der Gesellschaft</span></div>
  <div class="trust-item"><strong>Drei Partner</strong><span>Zwei Professoren (BWL) und ein promovierter Verhandlungsexperte</span></div>
  <div class="trust-item"><strong>Im Verbund mit S&amp;D</strong><span>Tochtergesellschaft der Schubart &amp; Dulgeridis GmbH</span></div>
</div></div></section>
"""

    problem = section(
        head("Ausgangslage", "Wirkung geht an vier Stellen verloren, bevor Entwicklung im Alltag ankommt",
             "Viele Organisationen investieren in Trainings und Programme und sehen im Alltag wenig davon. An vier Stellen geht die Wirkung typischerweise verloren:", "problem-title")
        + V.gap_bridge(), "", "problem-title")

    leistungen = section(
        head("Leistungen", "Vier Stufen, jede mit eigenem Ergebnis: von der Konzeption bis zur Vermarktung",
             "Jede Stufe beantwortet eine andere Frage und liefert ein eigenes Ergebnis. Sie können sie einzeln oder verbunden betrachten.", "leistungen-title")
        + V.value_chain()
        + '<p class="small"><a class="link-arrow" href="/leistungen">Alle Stufen im Detail ' + ARROW + "</a></p>", "section-white", "leistungen-title")

    fokus = section(
        head("Fokusfelder", "Verhandeln, Führen und Wirtschaften treffen bei Entscheidern zusammen",
             "Sie begegnen sich in denselben Situationen: Verhandeln, Führen und Wirtschaften treffen bei Entscheidern in denselben Situationen aufeinander. Jedes Fokusfeld hat einen klar benannten Ansprechpartner.", "fokus-title")
        + V.venn(), "", "fokus-title")

    angebote = section(
        head("Angebote im Fokus", "Zwei Einstiege, die Sie ohne Vorgespräch ansehen können",
             "Das Formatportfolio InnoLab und der KI-Readiness Check zeigen, wie THE GAP Lab Wirkung greifbar macht.", "angebote-title")
        + V.teasers(), "section-cream", "angebote-title")

    warum = section(
        head("Warum THE GAP Lab", "Drei Disziplinen, drei Partner, ein Verbund", "", "warum-title")
        + V.statements(), "v-dark", "warum-title")

    vorgehen = section(
        head("Vorgehen", "In vier Schritten vom Gespräch zur ausgewerteten Maßnahme",
             "Umfang und Taktung richten sich nach Ihrer Ausgangslage. Der Ablauf bleibt in der Struktur gleich.", "vorgehen-title")
        + V.timeline([
            ("Schritt 1 · 20 bis 30 Minuten", "Erstgespräch", "Anlass, Ziel und Zielgruppe klären. Kostenlos und unverbindlich.", "Klarer Anlass, Ziel und Zielgruppe"),
            ("Schritt 2", "Konzept", "Wir leiten ein Konzept mit Zielen, Inhalten, Format und Erfolgskriterien ab und stimmen es mit Ihnen ab.", "Abgestimmtes Konzept mit Erfolgskriterien"),
            ("Schritt 3", "Umsetzung", "Inhalte werden entwickelt und die Maßnahme wird durchgeführt, entlang der Fokusfelder der Partner.", "Entwickelte und durchgeführte Maßnahme"),
            ("Schritt 4", "Auswertung", "Gemeinsam prüfen wir, was die Maßnahme bewirkt hat und welche nächsten Schritte sinnvoll sind.", "Wirkung und nächste Schritte"),
        ]), "", "vorgehen-title")

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

    cta = cta_band("Entwicklung, die in Ihrer Organisation ankommt.",
                   "Sprechen Sie 20 bis 30 Minuten mit einem der Partner: kostenlos, unverbindlich, per Microsoft Teams.",
                   secondary="Die Terminbuchung läuft über die Kalender der Partner bei der Schubart &amp; Dulgeridis GmbH.")

    page["body"] = hero + trust + kurz + problem + leistungen + fokus + angebote + warum + vorgehen + partner + faq + cta
    page["styles"] = ["/assets/visual.css"]
    page["journey"] = "/"
    page["speakable"] = True
    return page


def leistungen():
    page = {
        "path": "/leistungen", "short": "Leistungen",
        "title": "Leistungen — Konzeption bis Vermarktung | THE GAP Lab",
        "description": "Vier Leistungsstufen für Maßnahmen der Personalentwicklung: Konzeption, Entwicklung, Durchführung und Vermarktung. Ablauf, mögliche Ergebnisse, FAQ.",
        "priority": "0.9", "llms_group": "Leistungen", "schema_type": "CollectionPage",
        "styles": ["/assets/visual.css"], "journey": "/leistungen", "speakable": True,
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
        return f"""<article class="v-service" id="{anchor}">
  <div class="v-shead"><span class="big" aria-hidden="true">{num:02d}</span><div><span>{num:02d} · Stufe</span><h2>{title}</h2></div></div>
  <div class="v-sflow">
    <div class="v-sbox"><span class="v-lab">Ausgangslage</span><p>{ausgang}</p></div>
    <div class="v-sarrow" aria-hidden="true">{ARROW}</div>
    <div class="v-sbox mid"><span class="v-lab">Was wir tun</span><p>{tun}</p></div>
    <div class="v-sarrow" aria-hidden="true">{ARROW}</div>
    <div class="v-sbox out"><span class="v-lab">Mögliche Ergebnisse</span><ul>{erg}</ul></div>
  </div>
  <p class="v-sfit"><b>Geeignet, wenn</b> {geeignet}</p>
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
            + head("Überblick", "Vier Stufen beantworten vier Leitfragen und liefern je ein Ergebnis", "Jede Stufe liefert ein eigenes Ergebnis. Die Stufen bauen aufeinander auf, lassen sich aber einzeln beauftragen.")
            + V.value_chain()
            + '<h3 class="v-h3">Die passende Stufe.</h3>' + V.decision_help()
            + services, "", "")
        + section(V.innolab_strip(), "section-white v-tight", "")
        + section(
            head("Fokusfelder", "Wo die Stufen inhaltlich ansetzen", "Jede Stufe lässt sich auf eines oder mehrere der drei Fokusfelder beziehen.")
            + '<ul class="chips"><li><a href="/fokusfelder/verhandlungsfuehrung">Verhandlungsführung &amp; Rhetorik</a></li>'
              '<li><a href="/fokusfelder/leadership-organisation">Leadership &amp; Organisation</a></li>'
              '<li><a href="/fokusfelder/finance-transformation">Finance &amp; Transformation</a></li></ul>', "section-white", "")
        + section(
            head("Abgrenzung", "Messen und Entwickeln: THE GAP Lab und die Muttergesellschaft",
                 f"Diagnostik wie THE GAP und der Pulse-Check, Re- und Upskilling-Programme, Coaching und Recruiting gehören zur <a href=\"{SD}\">Schubart &amp; Dulgeridis GmbH</a>. "
                 "THE GAP Lab konzentriert sich auf Maßnahmen der Personalentwicklung in den drei Fokusfeldern.") + V.measure_develop(), "", "")
        + section(
            head("Häufige Fragen", "Fragen zu den Leistungen") + faq_block(faqs), "section-white", "")
        + cta_band("Die passende Stufe klärt das Erstgespräch.", "Im Erstgespräch klären wir, wo Ihre Ausgangslage liegt und welche Stufen sinnvoll sind.")
    )
    page["body"] = body
    page["schema_nodes"] = [{
        "@type": "ItemList", "@id": url_of("/leistungen") + "#stufen", "name": "Vier Leistungsstufen von THE GAP Lab",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "url": url_of("/leistungen") + "#" + a}
                            for i, (a, n) in enumerate([("konzeption", "Konzeption"), ("entwicklung", "Entwicklung"), ("durchfuehrung", "Durchführung"), ("vermarktung", "Vermarktung")], 1)],
    }, {
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
        "styles": ["/assets/visual.css"], "journey": "/fokusfelder", "speakable": True,
    }
    page["schema_nodes"] = [{
        "@type": "ItemList", "@id": url_of("/fokusfelder") + "#felder", "name": "Die drei Fokusfelder von THE GAP Lab",
        "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "url": url_of(u)}
                            for i, (u, n) in enumerate([("/fokusfelder/verhandlungsfuehrung", "Verhandlungsführung & Rhetorik"), ("/fokusfelder/leadership-organisation", "Leadership & Organisation"), ("/fokusfelder/finance-transformation", "Finance & Transformation")], 1)],
    }]
    page["body"] = (
        page_hero(page, "Drei Fokusfelder, drei Ansprechpartner",
                  "Verhandeln, Führen und Wirtschaften hängen im Alltag von Entscheidern zusammen. THE GAP Lab behandelt sie in einer Gesellschaft, jeweils mit einem benannten Partner.")
        + section(
            answer_box("Kurzantwort: In welchen Themenfeldern arbeitet THE GAP Lab?",
                       "In drei Fokusfeldern: Verhandlungsführung &amp; Rhetorik (Dr. Oliver Meschkat), Leadership &amp; Organisation (Prof. Dr. Constantin Schubart) sowie Finance &amp; Transformation (Prof. Dr. Marcel Dulgeridis).")
            + V.venn(with_links=False), "", "")
        + section(head("Im Vergleich", "Drei Fokusfelder nebeneinander", "Leitfrage, typische Situationen, zentrale Begriffe und Ansprechpartner auf einen Blick.", "cmp-title") + V.fokus_compare(), "section-white", "cmp-title")
        + cta_band("Das passende Fokusfeld klärt das Erstgespräch.", "Im Erstgespräch ordnen wir Ihre Ausgangslage gemeinsam ein.")
    )
    return page


def ueber_uns():
    page = {
        "path": "/ueber-uns", "short": "Über uns",
        "title": "Über uns — Drei Partner, eine Gesellschaft | THE GAP Lab",
        "description": "Die Menschen hinter THE GAP Lab: Geschäftsführer, Partner und der Verbund mit der Schubart & Dulgeridis GmbH. Profile und Fokusfelder.",
        "priority": "0.8", "llms_group": "Unternehmen", "schema_type": "AboutPage",
        "styles": ["/assets/visual.css"], "journey": "/ueber-uns", "speakable": True,
    }
    page["schema_nodes"] = person_nodes()

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
                       f"THE GAP Lab ist die Marke der The Gap Lab GmbH mit Sitz in {SITE['city']}. "
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
        + section(head("Aufbau", "Gesellschaft, Verbund und Fokusfelder", "Die Gesellschaft ist Tochter der Schubart &amp; Dulgeridis GmbH und ordnet jedem Fokusfeld einen Partner zu.", "aufbau-title") + V.org(), "section-white", "aufbau-title")
        + section(head("Die Partner", "Wer hinter THE GAP Lab steht",
                       "Alle Angaben entsprechen den veröffentlichten Profilen auf schubart-dulgeridis.de.", "partner-title")
                  + '<div class="grid">' + wide("constantin-schubart") + wide("oliver-meschkat") + wide("marcel-dulgeridis") + "</div>",
                  "section-cream", "partner-title")
        + cta_band("Wir lernen uns im Gespräch kennen.", "Das Erstgespräch dauert 20 bis 30 Minuten und ist kostenlos.")
    )
    return page


def kontakt():
    page = {
        "path": "/kontakt", "short": "Kontakt",
        "title": "Kontakt & Erstgespräch | THE GAP Lab",
        "description": "Kostenloses Erstgespräch (20–30 Min.) mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis buchen — oder per E-Mail und Telefon anfragen.",
        "priority": "0.9", "llms_group": "Unternehmen", "schema_type": "ContactPage",
        "faqs": FAQ_CONTACT, "faq_schema": True, "styles": ["/assets/visual.css"],
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
            head("Termin buchen", "Drei Ansprechpartner, ein Termin",
                 "Die Buchung läuft über die Kalender der Partner bei der Schubart &amp; Dulgeridis GmbH. Dort wählen Sie die Person und sehen freie Zeiten live. Nach der Buchung erhalten Sie eine Outlook-Einladung mit Microsoft-Teams-Link.", "termin-title")
            + '<div class="grid grid-3">' + booking("constantin-schubart") + booking("oliver-meschkat") + booking("marcel-dulgeridis") + "</div>"
            + '<p class="small">Mit dem Klick verlassen Sie gap-lab.de und wechseln zur Website der Muttergesellschaft; dort gilt deren <a href="' + SD + 'datenschutz">Datenschutzerklärung</a>.</p>',
            "", "termin-title")
        + section(head("Ablauf", "So läuft das Erstgespräch ab", "", "ablauf-title") + V.contact_flow(), "section-white", "ablauf-title")
        + section(
            '<div class="contact-grid"><div>'
            + head("Direkt anfragen", "E-Mail und Telefon", "", "direkt-title")
            + f"""<ul class="contact-list">
  <li><span class="k">E-Mail</span>{MAIL}</li>
  <li><span class="k">Telefon</span>{TEL}</li>
  <li><span class="k">Anschrift</span>{SITE['legal_name']}<br>{SITE['street']}<br>{SITE['zip']} {SITE['city']}</li>
</ul>
<p class="small muted">Während der Aufbauphase werden E-Mail und Telefon gemeinsam mit der Muttergesellschaft genutzt.</p>
</div><div>"""
            + head("Gut vorbereitet", "Was Sie für das Gespräch mitbringen können", "", "prep-title")
            + V.checklist([
                "<strong>Anlass und Ziel:</strong> Was soll sich in Ihrer Organisation verändern?",
                "<strong>Zielgruppe:</strong> Wer soll teilnehmen, und wie viele Personen sind es ungefähr?",
                "<strong>Zeitrahmen:</strong> Bis wann soll die Maßnahme wirken?",
                "<strong>Bisherige Erfahrungen:</strong> Was wurde schon versucht, und was hat nicht funktioniert?",
            ]) + """<p class="muted">Nichts davon ist Pflicht. Auch ein erstes Stichwort genügt.</p>
</div></div>""", "section-cream", "")
        + section(head("Häufige Fragen", "Zum Kontakt") + faq_block(FAQ_CONTACT), "", "")
    )
    return page


def build():
    return [home(), leistungen(), fokusfelder_hub(), ueber_uns(), kontakt()]
