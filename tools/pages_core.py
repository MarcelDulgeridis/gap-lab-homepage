"""Kernseiten: Start, Leistungen, Fokusfelder-Übersicht, Über uns, Kontakt.
Textprinzip (S&D): kurz, konkret, Aussagesätze; Details stehen in den Unterseiten und im Glossar.
Die ausführliche Textvariante liegt im Git-Tag archive/volltext-2026-11-04."""
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
     "<p>Sie konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung. Schwerpunkte: "
     "<a href=\"/fokusfelder/verhandlungsfuehrung\">Verhandlungsführung &amp; Rhetorik</a>, "
     "<a href=\"/fokusfelder/leadership-organisation\">Leadership &amp; Organisation</a> und "
     "<a href=\"/fokusfelder/finance-transformation\">Finance &amp; Transformation</a>. Sitz ist Altdorf bei Nürnberg.</p>"),
    ("Wer steht hinter THE GAP Lab?",
     "<p>Geschäftsführer ist Prof. Dr. Constantin Schubart, Partner sind Dr. Oliver Meschkat und Prof. Dr. Marcel Dulgeridis. "
     "THE GAP Lab ist Tochter der Schubart &amp; Dulgeridis GmbH. Mehr auf <a href=\"/ueber-uns\">Über uns</a>.</p>"),
    ("Wie unterscheiden sich THE GAP Lab und die Schubart & Dulgeridis GmbH?",
     "<p>Die Schubart &amp; Dulgeridis GmbH bietet forschungsbasierte Beratung und Diagnostik (THE GAP, Pulse-Check, Upskilling, Coaching). "
     f"THE GAP Lab entwickelt und führt Maßnahmen der Personalentwicklung durch. Beide stehen im Verbund: <a href=\"{SD}\">schubart-dulgeridis.de</a>.</p>"),
    ("Für wen ist das Angebot gedacht?",
     "<p>Für Geschäftsleitungen, Personalverantwortliche und Führungskräfte, die Entwicklung gezielt planen, durchführen oder einkaufen.</p>"),
    ("Wo sitzt THE GAP Lab?",
     f"<p>In {SITE['city']} ({SITE['street']}, {SITE['zip']}). Alle Angaben im <a href=\"/impressum\">Impressum</a>.</p>"),
]

FAQ_COOPERATION = [
    ("Wie kommt eine Zusammenarbeit zustande?",
     "<p>Am Anfang steht ein kostenloses Erstgespräch (20 bis 30 Minuten, Microsoft Teams) zu Anlass, Ziel und Zielgruppe. "
     "Danach erhalten Sie ein Angebot mit klarem Leistungsumfang. Termin: <a href=\"/kontakt\">Kontakt</a>.</p>"),
    ("Was kostet eine Zusammenarbeit?",
     "<p>Nach dem Erstgespräch erhalten Sie ein individuelles Angebot nach Umfang. Die Preise der <a href=\"/innolab#preise\">InnoLab-Formate</a> stehen auf der InnoLab-Seite.</p>"),
    ("Muss ich alle vier Stufen beauftragen?",
     "<p>Nein. Stufen lassen sich einzeln oder als Kette buchen. Das klären wir im Erstgespräch.</p>"),
    ("Wie läuft eine Maßnahme ab?",
     "<p>In vier Schritten: Ausgangslage klären, Konzept entwickeln, Maßnahme umsetzen, Wirkung auswerten. Details: <a href=\"/leistungen\">Leistungen</a>.</p>"),
]

FAQ_CONTACT = [
    ("Wie erreiche ich THE GAP Lab?",
     f"<p>Per E-Mail an {MAIL} oder telefonisch unter {TEL}. E-Mail und Telefon werden in der Aufbauphase gemeinsam mit der Muttergesellschaft genutzt.</p>"),
    ("Mit wem kann ich ein Erstgespräch führen?",
     "<p>Mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis. Gebucht wird über deren Kalender bei der Schubart &amp; Dulgeridis GmbH, freie Zeiten sind live sichtbar.</p>"),
]

FAQ_ALL = FAQ_COMPANY + FAQ_COOPERATION + FAQ_CONTACT
FAQ_HOME = [FAQ_COMPANY[0], FAQ_COMPANY[1], FAQ_COOPERATION[1]]


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
<section class="hero hero-home"><div class="container"><div class="hero-grid">
  <div>
    <p class="eyebrow">Personalentwicklung · Altdorf bei Nürnberg</p>
    <h1>Personal&shy;entwicklung, die <span class="accent">verbindet.</span></h1>
    <p class="lead">THE GAP Lab verbindet Verhandlungsstärke, Führungsklarheit und Finanzverständnis in Maßnahmen, die im Arbeitsalltag ankommen.</p>
    <div class="hero-actions">
      <a class="btn" href="/kontakt">Erstgespräch vereinbaren {ARROW}</a>
      {link_arrow("/leistungen", "Leistungen ansehen")}
    </div>
  </div>
  {V.hero_gap()}
</div></div></section>
"""

    nums = V.numbers_band([("3", "Disziplinen<br>in einer Gesellschaft"), ("3", "Partner<br>mit Namen"), ("5", "InnoLab-Formate<br>vor Ort"), ("20–30", "Minuten Erstgespräch<br>kostenlos")])

    problem = section(
        head("01 · Das Problem", "Wirkung geht an vier Stellen verloren", "", "problem-title") + V.gap_bridge(), "", "problem-title")

    leistungen = section(
        head("02 · Die Lösung", "Vier Stufen, jede mit eigenem Ergebnis", "Einzeln buchbar oder als Kette.", "leistungen-title")
        + V.value_chain(results=False)
        + '<p class="small"><a class="link-arrow" href="/leistungen">Ergebnisse je Stufe ' + ARROW + "</a></p>", "section-white", "leistungen-title")

    fokus = section(
        head("03 · Die Fokusfelder", "Verhandeln, Führen und Wirtschaften treffen bei Entscheidern zusammen", "", "fokus-title")
        + V.venn(), "", "fokus-title")

    angebote = section(
        head("04 · Das Angebot", "Zwei Einstiege ohne Vorgespräch", "", "angebote-title") + V.teasers(), "section-cream", "angebote-title")

    vorgehen = section(
        head("05 · Das Vorgehen", "Vier Schritte vom Gespräch zur Auswertung", "", "vorgehen-title")
        + V.timeline([
            ("Schritt 1 · 20 bis 30 Minuten", "Erstgespräch", "Anlass, Ziel, Zielgruppe.", "Klarer Auftrag"),
            ("Schritt 2", "Konzept", "Ziele, Inhalte, Format, Erfolgskriterien.", "Abgestimmtes Konzept"),
            ("Schritt 3", "Umsetzung", "Entwicklung und Durchführung entlang der Fokusfelder.", "Durchgeführte Maßnahme"),
            ("Schritt 4", "Auswertung", "Wirkung prüfen, nächste Schritte klären.", "Wirkung und nächste Schritte"),
        ]), "", "vorgehen-title")

    partner = section(
        head("Das Team", "Drei Partner, ein Ansprechkreis", "", "partner-title")
        + '<div class="grid grid-3">'
        + partner_card("constantin-schubart") + partner_card("oliver-meschkat") + partner_card("marcel-dulgeridis")
        + "</div>", "section-cream", "partner-title")

    faq = section(
        head("Häufige Fragen", "Antworten in Kürze", "", "faq-title")
        + faq_block(FAQ_HOME)
        + '<p class="small">Weitere Antworten: <a href="/faq">FAQ</a>.</p>', "", "faq-title")

    cta = cta_band("Entwicklung, die in Ihrer Organisation ankommt.",
                   "Kostenloses Erstgespräch, 20 bis 30 Minuten.")

    page["body"] = hero + nums + problem + leistungen + fokus + angebote + vorgehen + faq + cta
    page["speakable_selector"] = [".hero .lead"]
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
         "<p>Konzeption, Entwicklung, Durchführung und Vermarktung von Maßnahmen der Personalentwicklung in drei Fokusfeldern: Verhandlungsführung &amp; Rhetorik, Leadership &amp; Organisation, Finance &amp; Transformation.</p>"),
        ("Muss ich alle vier Stufen beauftragen?",
         "<p>Nein. Einzeln oder als Kette, das klärt das Erstgespräch.</p>"),
        ("Bieten Sie auch Diagnostik an?",
         f"<p>Diagnostik wie THE GAP und der Pulse-Check gehört zur Schubart &amp; Dulgeridis GmbH: <a href=\"{SD}the-gap\">schubart-dulgeridis.de/the-gap</a>.</p>"),
    ]
    page["faqs"] = faqs

    body = (
        page_hero(page, "Leistungen von der Konzeption bis zur Vermarktung", "Vier Stufen von der Idee zur Maßnahme.")
        + section(
            answer_box("Kurzantwort: Was bietet The Gap Lab an?",
                       "Maßnahmen der Personalentwicklung: konzipiert, entwickelt, durchgeführt und vermarktet, in den Fokusfeldern Verhandlungsführung &amp; Rhetorik, Leadership &amp; Organisation sowie Finance &amp; Transformation.")
            + head("Die vier Stufen", "Von der Leitfrage zum Ergebnis", "")
            + V.stage_matrix(), "", "")
        + section(V.innolab_strip(), "section-white v-tight", "")
        + section(
            head("Abgrenzung", "Messen und Entwickeln",
                 "Diagnostik und Beratung liegen bei der Muttergesellschaft, Maßnahmen bei THE GAP Lab.") + V.measure_develop(), "", "")
        + section(
            head("Häufige Fragen", "Fragen zu den Leistungen") + faq_block(faqs), "section-white", "")
        + cta_band("Die passende Stufe klärt das Erstgespräch.", "Kostenlos, 20 bis 30 Minuten.")
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
        page_hero(page, "Drei Fokusfelder, drei Ansprechpartner", "Ein benannter Partner je Fokusfeld.")
        + section(
            answer_box("Kurzantwort: In welchen Feldern arbeitet THE GAP Lab?",
                       "Verhandlungsführung &amp; Rhetorik, Leadership &amp; Organisation sowie Finance &amp; Transformation, je mit einem benannten Partner.")
            + V.venn(with_links=False), "", "")
        + section(head("Im Vergleich", "Drei Fokusfelder nebeneinander", "", "cmp-title") + V.fokus_compare(), "section-white", "cmp-title")
        + cta_band("Das passende Fokusfeld klärt das Erstgespräch.", "Kostenlos, 20 bis 30 Minuten.")
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

    page["body"] = (
        page_hero(page, "Drei Partner, eine Gesellschaft für Personalentwicklung", "Tochter der Schubart &amp; Dulgeridis GmbH.")
        + V.numbers_band([("3", "Partner<br>mit Namen"), ("2", "Professoren für BWL<br>an der IU"), ("1", "Verbund mit der<br>Schubart &amp; Dulgeridis GmbH")], "n3")
        + section(
            answer_box("Kurzantwort: Wer ist THE GAP Lab?",
                       f"Die Marke der The Gap Lab GmbH in {SITE['city']}, Tochter der Schubart &amp; Dulgeridis GmbH. Geschäftsführer ist Prof. Dr. Constantin Schubart.")
            + head("Aufbau und Team", "Wer hinter THE GAP Lab steht", "", "aufbau-title") + V.org_people(), "", "aufbau-title")
        + cta_band("Wir lernen uns im Gespräch kennen.", "Kostenlos, 20 bis 30 Minuten.")
    )
    return page


def kontakt():
    page = {
        "path": "/kontakt", "short": "Kontakt",
        "title": "Kontakt & Erstgespräch | THE GAP Lab",
        "description": "Kostenloses Erstgespräch (20–30 Min.) mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis buchen — oder per E-Mail und Telefon anfragen.",
        "priority": "0.9", "llms_group": "Unternehmen", "schema_type": "ContactPage",
        "styles": ["/assets/visual.css"], "speakable": True,
    }

    def booking(key):
        p = PARTNERS[key]
        first = {"constantin-schubart": "Constantin", "oliver-meschkat": "Oliver", "marcel-dulgeridis": "Marcel"}[key]
        return f"""<article class="card">
  <span class="tag">{esc(p['focus'])}</span>
  <h3>Erstgespräch mit {first}</h3>
  <p>{esc(p['name'])}</p>
  <a class="btn" href="{BOOKING}">Termin wählen {ARROW}</a>
</article>"""

    page["body"] = (
        page_hero(page, "Kontakt und Erstgespräch", "20 bis 30 Minuten mit einem der Partner, kostenlos.")
        + section(answer_box("Kurzantwort: Wie komme ich zum Erstgespräch?", "Online einen Termin mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis wählen. Das Gespräch dauert 20 bis 30 Minuten, findet per Microsoft Teams statt und ist kostenlos."), "v-tight", "")
        + section(
            head("Termin buchen", "Drei Ansprechpartner, ein Termin",
                 "Buchung über die Kalender der Partner bei der Schubart &amp; Dulgeridis GmbH.", "termin-title")
            + '<div class="grid grid-3">' + booking("constantin-schubart") + booking("oliver-meschkat") + booking("marcel-dulgeridis") + "</div>"
            + '<p class="small">Mit dem Klick wechseln Sie zur Website der Muttergesellschaft, dort gilt deren <a href="' + SD + 'datenschutz">Datenschutzerklärung</a>.</p>',
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
</div><div>"""
            + head("Gut vorbereitet", "Vier Stichworte genügen", "", "prep-title")
            + V.checklist([
                "<strong>Anlass und Ziel</strong>",
                "<strong>Zielgruppe</strong> und ungefähre Zahl",
                "<strong>Zeitrahmen</strong> bis zur Wirkung",
                "<strong>Bisherige Erfahrungen</strong>",
            ]) + """
</div></div>""", "section-cream", "")
    )
    return page


def build():
    return [home(), leistungen(), fokusfelder_hub(), ueber_uns(), kontakt()]
