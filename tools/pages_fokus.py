"""Die drei Fokusfeld-Seiten. Inhalte: allgemeines Fachwissen, belegte Personenangaben, keine erfundenen Kennzahlen."""
from siteinfo import SITE, PARTNERS
import visuals as V
from helpers import (esc, url_of, ARROW, faq_block, faq_more, cta_band, page_hero, section, head, answer_box, partner_wide)

SD = SITE["parent_url"]


def defs(items):
    return '<dl class="defs">' + "".join(f"<div><dt>{esc(t)}</dt><dd>{d}</dd></div>" for t, d in items) + "</dl>"


def feature(items):
    return '<ul class="feature-list">' + "".join(f"<li><strong>{esc(t)}</strong><span>{d}</span></li>" for t, d in items) + "</ul>"


def related(current):
    cards = []
    allf = [
        ("/fokusfelder/strategie-vertrieb-innovation", "Strategie, Vertrieb &amp; Innovation", "Strategie festlegen, Kunden überzeugen, Neues einführen."),
        ("/fokusfelder/leadership-organisation", "Leadership &amp; Organisation", "Rollen, Entscheidungswege und Erwartungen klären."),
        ("/fokusfelder/finance-transformation", "Finance &amp; Transformation", "Kennzahlen verstehen und Veränderung wirtschaftlich fundiert umsetzen."),
    ]
    for path, title, text in allf:
        if path == current:
            continue
        cards.append(f'<a class="card card-link" href="{path}"><span class="tag">Fokusfeld</span><h3>{title}</h3><p>{text}</p><span class="more">Fokusfeld ansehen</span></a>')
    return '<div class="grid grid-2">' + "".join(cards) + "</div>"


def fokus_page(cfg):
    page = {
        "path": cfg["path"], "short": cfg["short"], "title": cfg["title"], "description": cfg["description"],
        "crumbs": [("Fokusfelder", "/fokusfelder")], "priority": "0.8", "llms_group": "Fokusfelder",
        "faqs": cfg["faqs"], "styles": ["/assets/visual.css"], "journey": "/fokusfelder", "speakable": True,
        "schema_nodes": [{
            "@type": "Service", "@id": url_of(cfg["path"]) + "#service",
            "name": cfg["service_name"], "serviceType": "Personalentwicklung",
            "provider": {"@id": f"{SITE['domain']}/#organization"},
            "description": cfg["service_desc"],
            "audience": {"@type": "Audience", "audienceType": cfg["audience_type"]},
            "url": url_of(cfg["path"]),
        }],
    }
    p = PARTNERS[cfg["partner"]]
    faqs_html = faq_block(cfg["faqs"]) + faq_more()
    sources = "".join(f"<li>{s}</li>" for s in cfg["sources"])
    page["body"] = (
        page_hero(page, cfg["h1"], cfg["lead"])
        + section(V.facts_strip([
            ("Ansprechpartner", f'<a href="/ueber-uns#{cfg["partner"]}">{esc(p["name"])}</a>, {esc(p["role"])}'),
            ("Für wen", cfg["zielgruppe"]),
            ("Einstieg", "Kostenloses Erstgespräch, 20 bis 30 Minuten"),
        ], cfg["color"]), "v-tight", "")
        + section(answer_box(cfg["answer_label"], cfg["answer"]), "v-tight", "")
        + section(head(cfg.get("model_eyebrow", "Zentrale Begriffe"), cfg["model_title"], "") + cfg["model"] + defs(cfg["begriffe"]), "section-white", "")
        + section(head("Typische Ausgangslagen", "Wann dieses Fokusfeld relevant wird", "") + V.situations(cfg["ausgangslagen"], cfg["color"]), "", "")
        + section(
            head("Mögliche Bausteine", "Drei Phasen einer Maßnahme", "")
            + V.phases(cfg["color"], cfg["phases"]), "section-white", "")
        + section(head("Weiterführend", "Passende Formate und Begriffe", "") + V.related_formats(cfg["related"]), "", "")
        + section(V.partner_compact(cfg["partner"]), "section-cream v-tight", "")
        + section(head("Häufige Fragen", "Fragen zu diesem Fokusfeld") + faqs_html, "", "")
        + section('<div class="sources"><h2 class="h2">Quellen</h2><ul>' + sources + "</ul></div>", "section-white v-tight", "")
        + cta_band(cfg["cta_title"], "20 bis 30 Minuten, kostenlos und unverbindlich.")
    )
    return page


STRATEGIE = {
    "path": "/fokusfelder/strategie-vertrieb-innovation", "short": "Strategie, Vertrieb & Innovation",
    "title": "Strategie, Vertrieb & Innovation: Training | THE GAP Lab",
    "description": "Marketing- und Sales-Management, strategisches Management, Verhandlungsführung sowie Innovations- und Change Management, mit Dr. Oliver Meschkat.",
    "h1": "Strategie, Vertrieb und Innovation: Richtung festlegen, Kunden überzeugen, Neues einführen",
    "lead": "Strategie, Vertrieb und Innovation entscheiden, ob ein Angebot den Markt erreicht. Verhandlung und Kommunikation tragen es.",
    "partner": "oliver-meschkat", "color": "f1",
    "model_eyebrow": "Themen und Begriffe",
    "model_title": "Vier Themenblöcke, ein Fokusfeld",
    "model": V.topics([
        ("Strategie &amp; Management", ["Strategisches Management", "Zielbild, Prioritäten, Ressourcen", "Entscheidungsvorlagen"]),
        ("Marketing &amp; Vertrieb", ["Marketing- und Sales-Management", "Verkaufstraining", "Kundengespräche und Angebote"]),
        ("Verhandlung &amp; Kommunikation", ["Verhandlungsführung", "Rhetorik und Moderation", "Konfliktmanagement"]),
        ("Innovation &amp; Change", ["Innovationsmanagement, Produktneu- und -weiterentwicklung", "Change Management", "Teambuilding im Wandel"]),
    ]) + V.zopa(),
    "phases": [("Ausrichten", ["Ausgangslage und Zielbild klären", "Strategie, Zielkunden und Prioritäten festlegen"]),
               ("Anwenden", ["Verkaufs- und Verhandlungsgespräche trainieren", "Rhetorik, Moderation und Konfliktmanagement üben", "Innovation und Change am eigenen Vorhaben entwickeln"]),
               ("Verankern", ["Auswertung und Transfer in den Alltag"])],
    "answer_label": "Kurzantwort: Was umfasst Strategie, Vertrieb & Innovation?",
    "answer": "Marketing- und Sales-Management, strategisches Management sowie Innovations- und Change Management, ergänzt um Verhandlungsführung, Rhetorik, Moderation und Konfliktmanagement. Ziel: Strategie, Angebot und Auftritt greifen so ineinander, dass sie beim Kunden und im Team ankommen.",
    "begriffe": [
        ("Strategisches Management", "Ziele, Prioritäten und Ressourcen festlegen und die Ausrichtung eines Unternehmens oder Bereichs steuern."),
        ("Sales-Management", "Planung und Steuerung des Vertriebs: Ziele, Zielkunden, Prozesse und Verkaufsgespräche."),
        ("Interessen und Positionen", "Die Position ist die Forderung, das Interesse der Grund dahinter. Wer Interessen kennt, findet mehr Lösungen."),
        ("Alternative zum Verhandlungsergebnis (BATNA)", "Die beste Alternative ohne Einigung (Best Alternative to a Negotiated Agreement). Sie bestimmt, bis wann ein Angebot akzeptabel ist."),
        ("Verhandlungsspielraum (ZOPA)", "Der Bereich, in dem beide Seiten zustimmen könnten (Zone of Possible Agreement). Ohne Überschneidung ist eine Einigung unwahrscheinlich."),
        ("Anker", "Die erste konkrete Zahl im Gespräch. Sie prägt häufig den weiteren Verlauf."),
        ("Argumentationsaufbau", "Behauptung, Begründung und Beleg, sodass Zuhörende sie nachvollziehen können."),
        ("Change Management", "Planung und Begleitung von Veränderung: Haltung, Kommunikation und Umgang mit Widerständen."),
    ],
    "ausgangslagen": [
        ("Neues Angebot oder Produkt", "Produktneu- oder -weiterentwicklung braucht Prototypen, Tests und Entscheidungen."),
        ("Vertrieb unter Druck", "Ziele, Zielkunden und Gespräche sind nicht aufeinander abgestimmt."),
        ("Verhandlungen und Konflikte", "Preise, Verträge und Budgets, dazu Einwände, Eskalation und ungleiche Machtverteilung."),
        ("Veränderung im Team", "Wandel stockt, die Strategie kommt im Alltag nicht an."),
    ],
    "zielgruppe": "Geschäftsleitungen, Vertriebs- und Marketingverantwortliche, Führungskräfte und Projektteams, die Strategie, Kundenauftritt oder Innovation voranbringen.",
    "related": [("/innolab#sprint", "InnoLab", "InnoLab Sprint", "Produktneu- und -weiterentwicklung: Prototyp und Pitch in fünf Tagen."),
                ("/innolab#change-leadership", "InnoLab", "Change Leadership", "Führungskräftetraining: Wandel kommunizieren und umsetzen."),
                ("/glossar#alternative-zum-verhandlungsergebnis-batna", "Glossar", "BATNA und ZOPA", "Die Begriffe hinter Verhandlungsspielraum und Alternative nachlesen.")],
    "faqs": [
        ("Was umfasst das Fokusfeld Strategie, Vertrieb & Innovation?",
         "<p>Marketing- und Sales-Management, strategisches Management, Verhandlungsführung, Rhetorik, Moderation, Konfliktmanagement, Teambuilding sowie Innovations- und Change Management, etwa als <a href=\"/innolab\">InnoLab</a> für Produktneu- oder -weiterentwicklung.</p>"),
        ("Gibt es Verkaufstraining?",
         "<p>Ja. Verkaufstraining und Sales-Management gehören zum Fokusfeld: Gesprächsführung, Verhandlung, Angebot und Steuerung. Den Umfang legen wir nach dem Erstgespräch im Angebot fest.</p>"),
        ("Worin unterscheiden sich Verhandlungsführung und Rhetorik?",
         "<p>Verhandlungsführung betrifft Strategie und Vorbereitung: Ziele, Alternativen, Spielräume und Gesprächsverlauf. Rhetorik betrifft die Wirkung: Aufbau von Argumenten, Wortwahl und Auftreten. Beides ergänzt sich.</p>"),
        ("Kann eine Maßnahme an eigenen Fällen ansetzen?",
         "<p>Ja. Eigene Verhandlungs-, Vertriebs- oder Innovationsfälle lassen sich in Übungen aufgreifen, auch anonymisiert.</p>"),
        ("Wer ist Ansprechpartner?",
         "<p>Dr. Oliver Meschkat, Partner der The Gap Lab GmbH, mit Schwerpunkt Marketing- und Sales-Management, Personalentwicklung sowie Innovations- und Change Management. Termin: <a href=\"/kontakt\">Kontakt</a>.</p>"),
    ],
    "sources": [
        "Fisher, R., Ury, W.: <em>Getting to Yes</em> (1981); deutsch: <em>Das Harvard-Konzept</em>. Grundlage der Unterscheidung von Positionen und Interessen sowie des Begriffs BATNA. Überblick: <a href=\"https://de.wikipedia.org/wiki/Harvard-Konzept\" rel=\"noopener\">Harvard-Konzept (Wikipedia)</a>.",
        "Raiffa, H.: <em>The Art and Science of Negotiation</em> (1982). Grundlage des Begriffs der Zone of Possible Agreement.",
        "Tversky, A., Kahneman, D.: Judgment under Uncertainty: Heuristics and Biases. <em>Science</em> 185 (1974). Beschreibt den Ankereffekt. <a href=\"https://doi.org/10.1126/science.185.4157.1124\" rel=\"noopener\">DOI 10.1126/science.185.4157.1124</a>.",
    ],
    "cta_title": "Strategie, die beim Kunden ankommt.",
    "service_name": "Strategie, Vertrieb & Innovation: Maßnahmen der Personalentwicklung",
    "service_desc": "Konzeption, Entwicklung und Durchführung von Maßnahmen zu Marketing- und Sales-Management, strategischem Management, Verhandlungsführung, Rhetorik sowie Innovations- und Change Management.",
    "audience_type": "Geschäftsleitungen, Vertriebs- und Marketingverantwortliche, Führungskräfte, Projektteams",
}


LEADERSHIP = {
    "path": "/fokusfelder/leadership-organisation", "short": "Leadership & Organisation",
    "title": "Leadership & Organisation — THE GAP Lab",
    "description": "Leadership & Organisation: Begriffe, typische Ausgangslagen und mögliche Bausteine für Führungsklarheit — mit Prof. Dr. Constantin Schubart als Ansprechpartner.",
    "h1": "Leadership und Organisation: Führung im Zusammenspiel von Strategie, Kultur und Rollen",
    "lead": "Führung funktioniert selten durch einzelne Personen allein. Entscheidend ist, wie Strategie, Kultur, Rollen und Entscheidungswege zusammenpassen.",
    "partner": "constantin-schubart", "color": "f2",
    "model_title": "Von der Strategie in den Alltag",
    "model": V.impl_stack(),
    "phases": [("Klären", ["Klärung von Rollen und Erwartungen", "Entscheidungswege und Verantwortlichkeiten"]),
               ("Anwenden", ["Führungsgespräche", "Umgang mit Veränderung", "Zusammenarbeit im Team"]),
               ("Verankern", ["Reflexion an eigenen Führungssituationen"])],
    "answer_label": "Kurzantwort: Was bedeutet Leadership & Organisation?",
    "answer": "Der Ansatz betrachtet Führung nicht als Eigenschaft einzelner Personen, sondern als Zusammenspiel aus Strategie, Kultur, Rollen und Entscheidungswegen. Ziel ist, dass Erwartungen klar sind und Entscheidungen im Alltag ankommen.",
    "why": (
        "<h2>Warum Rollen nie isoliert zu betrachten sind</h2>"
        "<p>Eine Führungskraft kann fachlich stark sein und trotzdem scheitern, wenn Rolle, Entscheidungsrechte und Erwartungen unklar sind. Umgekehrt bleibt eine klare Strategie wirkungslos, wenn die gelebte Kultur etwas anderes belohnt. Deshalb schaut dieses Fokusfeld auf das Zusammenspiel.</p>"
        f"<p>Der Abstand zwischen beschlossener Strategie und gelebtem Alltag ist ein häufiges Muster. Wer diesen Abstand zunächst messen möchte, findet die Diagnostik bei der Muttergesellschaft: <a href=\"{SD}the-gap\">THE GAP</a> der Schubart &amp; Dulgeridis GmbH.</p>"
    ),
    "begriffe": [
        ("Rollenklarheit", "Alle Beteiligten wissen, welche Aufgaben, Verantwortung und Erwartungen mit einer Rolle verbunden sind."),
        ("Entscheidungsrechte", "Die Festlegung, wer worüber entscheidet, wer einbezogen und wer lediglich informiert wird."),
        ("Führungskultur", "Die im Alltag tatsächlich gelebten Normen: Was wird belohnt, was toleriert, worüber wird gesprochen?"),
        ("Umsetzungslücke", "Der Abstand zwischen beschlossener Strategie und dem, was im Arbeitsalltag geschieht."),
        ("Führungsgespräch", "Ein strukturiertes Gespräch zwischen Führungskraft und Mitarbeitenden über Ziele, Erwartungen und Entwicklung."),
    ],
    "ausgangslagen": [
        ("Neue Führungsrolle", "Eine Fachkraft wird Führungskraft oder eine Führungskraft übernimmt einen größeren Verantwortungsbereich."),
        ("Strategie wird beschlossen, aber nicht gelebt", "Ziele sind kommuniziert, doch im Alltag bleiben alte Abläufe bestehen."),
        ("Unklare Zuständigkeiten", "Entscheidungen verzögern sich, weil nicht eindeutig ist, wer entscheidet."),
        ("Veränderungsvorhaben stocken", "Widerstand und Unsicherheit bremsen die Umsetzung."),
    ],
    "bausteine": [
        "Klärung von Rollen und Erwartungen",
        "Entscheidungswege und Verantwortlichkeiten",
        "Führungsgespräche",
        "Umgang mit Veränderung",
        "Zusammenarbeit im Team",
        "Reflexion an eigenen Führungssituationen",
    ],
    "zielgruppe": "Geschäftsleitungen, Bereichsleitungen und Teamleitungen sowie Personalverantwortliche, die Führung gezielt entwickeln möchten.",
    "related": [("/innolab#change-leadership", "InnoLab", "Change Leadership", "Führungskräftetraining, 2 + 1 Tage: Widerstände erkennen, Wandel kommunizieren, am eigenen Vorhaben arbeiten."),
                ("/innolab#scorecard", "InnoLab", "Innovation Scorecard", "Strategieworkshop für Geschäftsführung: Ausrichtung, Kennzahlen und Entscheidungsvorlage."),
                ("/glossar#umsetzungsluecke", "Glossar", "Umsetzungslücke", "Der Abstand zwischen beschlossener Strategie und Arbeitsalltag."),
                ("/ki-readiness", "Werkzeug", "KI-Readiness Check", "Kostenlos: Wie groß ist der Abstand zwischen Führungs- und Teamsicht bei KI?")],
    "faqs": [
        ("Worin unterscheiden sich Führungskräfteentwicklung und Organisationsentwicklung?",
         "<p>Führungskräfteentwicklung stärkt Personen in ihrer Rolle. Organisationsentwicklung verändert Strukturen, Abläufe und Kultur. Beides greift ineinander, deshalb betrachtet dieses Fokusfeld beide Seiten.</p>"),
        ("Brauche ich vorab eine Diagnostik?",
         f"<p>Nicht zwingend. Wenn Sie den Abstand zwischen Führungsanspruch und Arbeitsalltag zuerst messen möchten, bietet die Schubart &amp; Dulgeridis GmbH dafür <a href=\"{SD}the-gap\">THE GAP</a> an. Maßnahmen lassen sich aber auch ohne vorherige Diagnostik konzipieren.</p>"),
        ("Für welche Führungsebenen eignet sich das?",
         "<p>Für Geschäftsleitungen, Bereichsleitungen und Teamleitungen. Das Konzept richtet sich nach der jeweiligen Zielgruppe.</p>"),
        ("Wer ist Ansprechpartner für Leadership & Organisation?",
         "<p>Prof. Dr. Constantin Schubart, Geschäftsführer der The Gap Lab GmbH und Professor für Betriebswirtschaftslehre an der IU Internationalen Hochschule. Einen Termin buchen Sie auf der Seite <a href=\"/kontakt\">Kontakt</a>.</p>"),
    ],
    "sources": [
        f"THE GAP — Diagnostik der Differenz zwischen Führungserwartung und Arbeitsrealität (Schubart &amp; Dulgeridis GmbH): <a href=\"{SD}the-gap\">schubart-dulgeridis.de/the-gap</a>.",
    ],
    "cta_title": "Anspruch und Alltag zusammenbringen.",
    "service_name": "Leadership & Organisation: Maßnahmen der Personalentwicklung",
    "service_desc": "Konzeption, Entwicklung und Durchführung von Maßnahmen zu Führung, Rollenklarheit, Entscheidungswegen und Organisation.",
    "audience_type": "Geschäftsleitungen, Bereichsleitungen, Teamleitungen, Personalverantwortliche",
}

FINANCE = {
    "path": "/fokusfelder/finance-transformation", "short": "Finance & Transformation",
    "title": "Finance & Transformation — THE GAP Lab",
    "description": "Finance & Transformation: Finanzverständnis für Führungskräfte, Kennzahlen und wirtschaftliche Bewertung von Veränderung — mit Prof. Dr. Marcel Dulgeridis.",
    "h1": "Finance und Transformation: Finanzverständnis für wirtschaftlich fundierte Veränderung",
    "lead": "Veränderung kostet Geld und soll Wirkung erzielen. Dieses Fokusfeld verbindet finanzielles Verständnis mit der Umsetzung von Vorhaben.",
    "partner": "marcel-dulgeridis", "color": "f3",
    "model_title": "Drei Blickwinkel auf die Zahlen eines Unternehmens",
    "model": V.finance_lenses(),
    "phases": [("Verstehen", ["Jahresabschluss und Berichte lesen", "Kennzahlen deuten"]),
               ("Bewerten", ["Wirtschaftlichkeit von Vorhaben bewerten", "Business Case aufbauen", "Finanzielle Wirkung von Veränderungen abschätzen"]),
               ("Anwenden", ["Übung an Fallbeispielen"])],
    "answer_label": "Kurzantwort: Was bedeutet Finance & Transformation?",
    "answer": "Das Fokusfeld verbindet Finanzverständnis (Rechnungswesen, Kennzahlen, Wirtschaftlichkeit) mit der Umsetzung von Veränderung. So werden Entscheidungen nicht nur strategisch plausibel, sondern auch wirtschaftlich belastbar.",
    "why": (
        "<h2>Warum Finanzverständnis zur Führung gehört</h2>"
        "<p>Wer über Budgets, Investitionen oder Veränderungen entscheidet, muss die finanzielle Wirkung einschätzen können. Das setzt nicht voraus, Buchhalter zu sein, wohl aber, Jahresabschluss und Kennzahlen lesen und Annahmen hinterfragen zu können.</p>"
        "<p>Transformation ist dabei kein Selbstzweck. Sie braucht eine nachvollziehbare wirtschaftliche Begründung und eine Umsetzungslogik, die Ressourcen, Zeit und Risiken berücksichtigt.</p>"
    ),
    "begriffe": [
        ("Gewinn- und Verlustrechnung (GuV)", "Stellt Erträge und Aufwendungen eines Zeitraums gegenüber und zeigt, ob und wie ein Gewinn oder Verlust entstanden ist."),
        ("Bilanz", "Stichtagsbezogene Gegenüberstellung von Vermögen (Aktiva) und Kapital (Passiva)."),
        ("Cashflow", "Zu- und Abflüsse von Zahlungsmitteln in einem Zeitraum. Ein Unternehmen kann Gewinn ausweisen und trotzdem Liquiditätsprobleme haben."),
        ("Kennzahlen", "Verdichtete Messgrößen, etwa Marge oder Eigenkapitalquote, die Lage und Entwicklung vergleichbar machen. Sie brauchen Kontext, um richtig gedeutet zu werden."),
        ("Business Case", "Die wirtschaftliche Begründung eines Vorhabens: erwartete Kosten, Nutzen, Annahmen und Risiken."),
    ],
    "ausgangslagen": [
        ("Budgetverantwortung ohne Finanzbrille", "Führungskräfte tragen Verantwortung für Budgets, ohne Berichte sicher lesen zu können."),
        ("Veränderung ohne Business Case", "Vorhaben starten, ohne dass Kosten, Nutzen und Annahmen belastbar beschrieben sind."),
        ("Zahlen und Entscheidungen laufen auseinander", "Berichte liegen vor, werden aber nicht in Entscheidungen übersetzt."),
        ("Transformation stockt an der Wirtschaftlichkeit", "Vorhaben werden gestoppt, weil der Nutzen nicht nachvollziehbar belegt ist."),
    ],
    "bausteine": [
        "Jahresabschluss und Berichte lesen",
        "Kennzahlen deuten",
        "Wirtschaftlichkeit von Vorhaben bewerten",
        "Business Case aufbauen",
        "Finanzielle Wirkung von Veränderungen abschätzen",
        "Übung an Fallbeispielen",
    ],
    "zielgruppe": "Geschäftsleitungen, Führungskräfte und Projektverantwortliche, die Budgets, Investitionen oder Veränderungsvorhaben verantworten.",
    "related": [("/innolab#scorecard", "InnoLab", "Innovation Scorecard", "Kennzahlen, Kosten-Nutzen-Rechnung und Entscheidungsvorlage für Innovationsvorhaben."),
                ("/glossar#cashflow", "Glossar", "Cashflow, GuV und Bilanz", "Die drei Blickwinkel auf die Zahlen eines Unternehmens im Glossar."),
                ("/glossar#business-case", "Glossar", "Business Case", "Die wirtschaftliche Begründung eines Vorhabens: Kosten, Nutzen, Annahmen, Risiken.")],
    "faqs": [
        ("Brauchen Führungskräfte betriebswirtschaftliche Vorkenntnisse?",
         "<p>Nein. Maßnahmen lassen sich an das Vorwissen der Zielgruppe anpassen. Ziel ist Verständnis, nicht Buchführung.</p>"),
        ("Worin liegt der Unterschied zwischen Gewinn und Cashflow?",
         "<p>Der Gewinn ist das Ergebnis der Erfolgsrechnung eines Zeitraums, der Cashflow der Saldo tatsächlicher Zahlungen. Beide können stark voneinander abweichen, etwa wenn Rechnungen erst später bezahlt werden.</p>"),
        ("Ist das Fokusfeld nur für Finanzbereiche gedacht?",
         "<p>Nein. Es richtet sich an alle, die Budgets, Investitionen oder Veränderungen verantworten.</p>"),
        ("Wer ist Ansprechpartner für Finance & Transformation?",
         "<p>Prof. Dr. Marcel Dulgeridis, Partner der The Gap Lab GmbH und Professor für Betriebswirtschaftslehre an der IU Internationalen Hochschule mit Schwerpunkt Rechnungswesen und Finanzberichterstattung. Einen Termin buchen Sie auf der Seite <a href=\"/kontakt\">Kontakt</a>.</p>"),
    ],
    "sources": [
        "Handelsrechtlicher Jahresabschluss nach Handelsgesetzbuch (<a href=\"https://www.gesetze-im-internet.de/hgb/__242.html\" rel=\"noopener\">§§ 242 ff. HGB</a>) sowie internationale Rechnungslegung nach IFRS als Grundlage der genannten Begriffe.",
    ],
    "cta_title": "Vorhaben mit belastbarer Zahlenbasis.",
    "service_name": "Finance & Transformation: Maßnahmen der Personalentwicklung",
    "service_desc": "Konzeption, Entwicklung und Durchführung von Maßnahmen zu Finanzverständnis, Kennzahlen und wirtschaftlicher Bewertung von Veränderungsvorhaben.",
    "audience_type": "Geschäftsleitungen, Führungskräfte, Projektverantwortliche",
}



# ------------------------------------------------------------------ Kurzfassungen (Volltext: Git-Tag archive/volltext-2026-11-04)
LEADERSHIP.update({
    "h1": "Leadership und Organisation: Führung im Zusammenspiel von Strategie, Kultur und Rollen",
    "lead": "Führung wirkt dort, wo Strategie, Kultur, Rollen und Entscheidungswege zusammenpassen. Führungskräfteentwicklung setzt dort an.",
    "answer": "Führung ist kein Merkmal einzelner Personen, sondern das Zusammenspiel aus Strategie, Kultur, Rollen und Entscheidungswegen. Ziel: klare Erwartungen und Entscheidungen, die im Alltag ankommen.",
    "begriffe": [
        ("Rollenklarheit", "Alle wissen, welche Aufgaben, Verantwortung und Erwartungen zu einer Rolle gehören."),
        ("Entscheidungsrechte", "Wer entscheidet, wer wird einbezogen, wer nur informiert."),
        ("Führungskultur", "Die im Alltag gelebten Normen: Was wird belohnt, toleriert, besprochen?"),
        ("Umsetzungslücke", "Der Abstand zwischen beschlossener Strategie und Arbeitsalltag."),
        ("Führungsgespräch", "Strukturiertes Gespräch über Ziele, Erwartungen und Entwicklung."),
    ],
    "ausgangslagen": [
        ("Neue Führungsrolle", "Eine Fachkraft wird Führungskraft oder übernimmt mehr Verantwortung."),
        ("Strategie wird nicht gelebt", "Ziele sind kommuniziert, alte Abläufe bleiben."),
        ("Unklare Zuständigkeiten", "Entscheidungen verzögern sich."),
        ("Veränderungsvorhaben stocken", "Widerstand und Unsicherheit bremsen."),
    ],
    "faqs": [
        ("Brauche ich vorab eine Diagnostik?",
         f"<p>Nicht zwingend. Wer den Abstand zwischen Anspruch und Alltag zuerst messen möchte, findet <a href=\"{SD}the-gap\">THE GAP</a> bei der Schubart &amp; Dulgeridis GmbH.</p>"),
        ("Für welche Führungsebenen eignet sich das?",
         "<p>Für Geschäftsleitungen, Bereichsleitungen und Teamleitungen, jeweils angepasst an die Zielgruppe.</p>"),
    ],
})
FINANCE.update({
    "h1": "Finance und Transformation: Finanzverständnis für wirtschaftlich fundierte Veränderung",
    "lead": "Veränderung kostet Geld und soll wirken. Finanzverständnis macht Entscheidungen belastbar.",
    "answer": "Finanzverständnis (Rechnungswesen, Kennzahlen, Wirtschaftlichkeit) verbunden mit der Umsetzung von Veränderung. Entscheidungen werden strategisch plausibel und wirtschaftlich belastbar.",
    "begriffe": [
        ("Gewinn- und Verlustrechnung (GuV)", "Erträge und Aufwendungen eines Zeitraums im Vergleich."),
        ("Bilanz", "Vermögen (Aktiva) und Kapital (Passiva) zu einem Stichtag."),
        ("Cashflow", "Zu- und Abflüsse von Zahlungsmitteln. Gewinn und Liquidität können auseinanderfallen."),
        ("Kennzahlen", "Verdichtete Messgrößen wie Marge oder Eigenkapitalquote. Sie brauchen Kontext."),
        ("Business Case", "Wirtschaftliche Begründung eines Vorhabens: Kosten, Nutzen, Annahmen, Risiken."),
    ],
    "ausgangslagen": [
        ("Budgetverantwortung ohne Finanzbrille", "Berichte werden nicht sicher gelesen."),
        ("Veränderung ohne Business Case", "Kosten und Nutzen sind nicht belastbar beschrieben."),
        ("Zahlen ohne Entscheidung", "Berichte liegen vor, werden aber nicht umgesetzt."),
        ("Transformation stockt", "Der Nutzen ist nicht nachvollziehbar belegt."),
    ],
    "faqs": [
        ("Brauchen Führungskräfte betriebswirtschaftliche Vorkenntnisse?",
         "<p>Nein. Maßnahmen passen sich dem Vorwissen an. Ziel ist Verständnis, nicht Buchführung.</p>"),
        ("Worin unterscheiden sich Gewinn und Cashflow?",
         "<p>Gewinn ist das Ergebnis der Erfolgsrechnung, Cashflow der Saldo tatsächlicher Zahlungen. Beide können stark abweichen.</p>"),
    ],
})


def build():
    return [fokus_page(STRATEGIE), fokus_page(LEADERSHIP), fokus_page(FINANCE)]
