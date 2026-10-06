"""Die drei Fokusfeld-Seiten. Inhalte: allgemeines Fachwissen, belegte Personenangaben, keine erfundenen Kennzahlen."""
from siteinfo import SITE, PARTNERS
from helpers import (esc, url_of, ARROW, faq_block, cta_band, page_hero, section, head, answer_box, partner_wide)

SD = SITE["parent_url"]


def defs(items):
    return '<dl class="defs">' + "".join(f"<div><dt>{esc(t)}</dt><dd>{d}</dd></div>" for t, d in items) + "</dl>"


def feature(items):
    return '<ul class="feature-list">' + "".join(f"<li><strong>{esc(t)}</strong><span>{d}</span></li>" for t, d in items) + "</ul>"


def related(current):
    cards = []
    allf = [
        ("/fokusfelder/verhandlungsfuehrung", "Verhandlungsführung &amp; Rhetorik", "Verhandlungen vorbereiten, führen und überzeugend argumentieren."),
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
        "faqs": cfg["faqs"],
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
    faqs_html = faq_block(cfg["faqs"])
    sources = "".join(f"<li>{s}</li>" for s in cfg["sources"])
    page["body"] = (
        page_hero(page, cfg["h1"], cfg["lead"])
        + section(
            answer_box(cfg["answer_label"], cfg["answer"])
            + '<div class="prose">' + cfg["why"] + "</div>", "", "")
        + section(head("Zentrale Begriffe", "Die wichtigsten Begriffe im Überblick", "") + defs(cfg["begriffe"]), "section-white", "")
        + section(head("Typische Ausgangslagen", "Wann dieses Fokusfeld relevant wird", "") + feature(cfg["ausgangslagen"]), "", "")
        + section(
            '<div class="split"><div>'
            + head("Mögliche Bausteine", "Was eine Maßnahme enthalten kann", "")
            + '</div><div class="prose"><ul>' + "".join(f"<li>{b}</li>" for b in cfg["bausteine"]) + "</ul>"
            f'<p class="muted">Welche Bausteine sinnvoll sind, hängt von Ziel und Zielgruppe ab. Das Konzept entsteht nach dem Erstgespräch in der <a href="/leistungen#konzeption">Konzeption</a>.</p>'
            f'<p><strong>Für wen:</strong> {cfg["zielgruppe"]}</p></div></div>', "section-white", "")
        + section(head("Ansprechpartner", f"Ihr Ansprechpartner: {esc(p['name'])}", "") + partner_wide(cfg["partner"]), "section-cream", "")
        + section(head("Häufige Fragen", "Fragen zu diesem Fokusfeld") + faqs_html, "", "")
        + section(
            '<div class="sources"><h2 class="h2">Quellen und weiterführend</h2><ul>' + sources + "</ul></div>"
            + "<div>" + head("Weitere Fokusfelder", "Das könnte ebenfalls relevant sein", "") + related(cfg["path"]) + "</div>", "section-white", "")
        + cta_band(cfg["cta_title"], "Im kostenlosen Erstgespräch (20 bis 30 Minuten) ordnen wir Ihre Ausgangslage ein.")
    )
    return page


VERHANDLUNG = {
    "path": "/fokusfelder/verhandlungsfuehrung", "short": "Verhandlungsführung & Rhetorik",
    "title": "Verhandlungsführung & Rhetorik — THE GAP Lab",
    "description": "Verhandlungsführung und Rhetorik: Begriffe, typische Ausgangslagen und mögliche Bausteine einer Maßnahme — mit Dr. Oliver Meschkat als Ansprechpartner.",
    "h1": "Verhandlungsführung und Rhetorik: souverän verhandeln, überzeugend argumentieren",
    "lead": "Verhandlungen entscheiden über Preise, Konditionen, Budgets und Zusammenarbeit. Dieses Fokusfeld macht sie planbar.",
    "partner": "oliver-meschkat",
    "answer_label": "Kurzantwort: Was ist Verhandlungsführung?",
    "answer": "Verhandlungsführung ist die zielgerichtete Vorbereitung, Steuerung und Auswertung von Verhandlungen. Ziel sind Ergebnisse, die die eigenen Interessen wahren und für die Gegenseite tragfähig genug sind, dass sie auch umgesetzt werden.",
    "why": (
        "<h2>Warum Verhandlungsführung lernbar ist</h2>"
        "<p>Verhandeln wirkt oft wie Talent. In der Praxis ist es überwiegend Vorbereitung: Wer seine Interessen kennt, Alternativen in der Hand hat und die Gegenseite einschätzen kann, verhandelt anders als jemand, der spontan reagiert.</p>"
        "<p>Rhetorik ergänzt das. Sie sorgt dafür, dass Argumente verständlich aufgebaut sind und auch unter Druck ankommen. Verhandlungsführung entscheidet, was gesagt wird; Rhetorik, wie es wirkt.</p>"
    ),
    "begriffe": [
        ("Interessen und Positionen", "Eine Position ist die Forderung („Wir wollen zehn Prozent Rabatt“). Das Interesse ist der Grund dahinter („Wir müssen das Budget einhalten“). Wer Interessen kennt, findet mehr Lösungen als nur die ursprüngliche Forderung."),
        ("Alternative zum Verhandlungsergebnis (BATNA)", "Die beste Alternative, die Sie haben, wenn keine Einigung zustande kommt (englisch: Best Alternative to a Negotiated Agreement). Sie bestimmt, bis wann ein Angebot noch akzeptabel ist."),
        ("Verhandlungsspielraum (ZOPA)", "Der Bereich, in dem beide Seiten einer Einigung zustimmen könnten (englisch: Zone of Possible Agreement). Überschneiden sich die Spielräume nicht, ist eine Einigung unwahrscheinlich."),
        ("Anker", "Die erste konkrete Zahl oder Forderung im Gespräch. Sie prägt häufig den weiteren Verlauf, weil sich beide Seiten daran orientieren."),
        ("Argumentationsaufbau", "Eine Behauptung wird durch Begründung und Beleg gestützt, sodass Zuhörende sie nachvollziehen können."),
    ],
    "ausgangslagen": [
        ("Preis- und Konditionengespräche", "Verhandlungen mit Kunden oder Lieferanten, bei denen Spielräume vorab nicht abgesteckt sind."),
        ("Vertragsverhandlungen", "Mehrere Beteiligte, viele Details und der Druck, zeitnah abzuschließen."),
        ("Interne Verhandlungen", "Budgets, Ressourcen und Prioritäten zwischen Bereichen: Hier verhandeln Menschen, die danach weiter zusammenarbeiten."),
        ("Gespräche unter Druck", "Kritische Situationen mit Einwänden, Eskalation oder ungleicher Machtverteilung."),
    ],
    "bausteine": [
        "Vorbereitungsstruktur für Verhandlungen",
        "Analyse von Interessen und Alternativen",
        "Gesprächsführung und Fragetechnik",
        "Argumentationsaufbau und rhetorische Mittel",
        "Umgang mit Einwänden und Druck",
        "Übung an eigenen Verhandlungsfällen",
        "Auswertung und Transfer in den Alltag",
    ],
    "zielgruppe": "Geschäftsleitungen, Führungskräfte und Fachverantwortliche, die regelmäßig verhandeln oder überzeugen müssen.",
    "faqs": [
        ("Worin unterscheiden sich Verhandlungsführung und Rhetorik?",
         "<p>Verhandlungsführung betrifft Strategie und Vorbereitung: Ziele, Alternativen, Spielräume und Gesprächsverlauf. Rhetorik betrifft die Wirkung: Aufbau von Argumenten, Wortwahl und Auftreten. Beides ergänzt sich.</p>"),
        ("Kann eine Maßnahme an eigenen Verhandlungsfällen ansetzen?",
         "<p>Ja, das ist sinnvoll. Wenn Sie konkrete Fälle bereitstellen, können wir sie in Übungen aufgreifen. Vertrauliche Details bleiben bei Ihnen; Fälle lassen sich auch anonymisieren.</p>"),
        ("Wie lange dauert eine Maßnahme?",
         "<p>Das hängt von Ziel, Zielgruppe und Format ab. Wir legen den Umfang nach dem Erstgespräch im Angebot fest.</p>"),
        ("Wer ist Ansprechpartner für Verhandlungsführung?",
         "<p>Dr. Oliver Meschkat, Partner der The Gap Lab GmbH und Experte für Verhandlungsführung, Rhetorik und Argumentation. Einen Termin buchen Sie auf der Seite <a href=\"/kontakt\">Kontakt</a>.</p>"),
    ],
    "sources": [
        "Fisher, R., Ury, W.: <em>Getting to Yes</em> (1981); deutsch: <em>Das Harvard-Konzept</em>. Grundlage der Unterscheidung von Positionen und Interessen sowie des Begriffs BATNA.",
        "Raiffa, H.: <em>The Art and Science of Negotiation</em> (1982). Grundlage des Begriffs der Zone of Possible Agreement.",
        "Tversky, A., Kahneman, D.: Judgment under Uncertainty: Heuristics and Biases. <em>Science</em> 185 (1974). Beschreibt den Ankereffekt.",
    ],
    "cta_title": "Welche Verhandlung soll besser werden?",
    "service_name": "Verhandlungsführung & Rhetorik: Maßnahmen der Personalentwicklung",
    "service_desc": "Konzeption, Entwicklung und Durchführung von Maßnahmen zu Verhandlungsführung, Rhetorik und Argumentation für Entscheider und Führungskräfte.",
    "audience_type": "Geschäftsleitungen, Führungskräfte, Fachverantwortliche",
}

LEADERSHIP = {
    "path": "/fokusfelder/leadership-organisation", "short": "Leadership & Organisation",
    "title": "Leadership & Organisation — THE GAP Lab",
    "description": "Leadership & Organisation: Begriffe, typische Ausgangslagen und mögliche Bausteine für Führungsklarheit — mit Prof. Dr. Constantin Schubart als Ansprechpartner.",
    "h1": "Leadership und Organisation: Führung im Zusammenspiel von Strategie, Kultur und Rollen",
    "lead": "Führung funktioniert selten durch einzelne Personen allein. Entscheidend ist, wie Strategie, Kultur, Rollen und Entscheidungswege zusammenpassen.",
    "partner": "constantin-schubart",
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
    "cta_title": "Wo klemmt es zwischen Anspruch und Alltag?",
    "service_name": "Leadership & Organisation: Maßnahmen der Personalentwicklung",
    "service_desc": "Konzeption, Entwicklung und Durchführung von Maßnahmen zu Führung, Rollenklarheit, Entscheidungswegen und Organisation.",
    "audience_type": "Geschäftsleitungen, Bereichsleitungen, Teamleitungen, Personalverantwortliche",
}

FINANCE = {
    "path": "/fokusfelder/finance-transformation", "short": "Finance & Transformation",
    "title": "Finance & Transformation — THE GAP Lab",
    "description": "Finance & Transformation: Finanzverständnis für Führungskräfte, Kennzahlen und wirtschaftliche Bewertung von Veränderung — mit Prof. Dr. Marcel Dulgeridis.",
    "h1": "Finance und Transformation: Veränderung wirtschaftlich fundiert umsetzen",
    "lead": "Veränderung kostet Geld und soll Wirkung erzielen. Dieses Fokusfeld verbindet finanzielles Verständnis mit der Umsetzung von Vorhaben.",
    "partner": "marcel-dulgeridis",
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
        "Handelsrechtlicher Jahresabschluss nach Handelsgesetzbuch (§§ 242 ff. HGB) sowie internationale Rechnungslegung nach IFRS als Grundlage der genannten Begriffe.",
    ],
    "cta_title": "Welches Vorhaben braucht eine belastbare Zahlenbasis?",
    "service_name": "Finance & Transformation: Maßnahmen der Personalentwicklung",
    "service_desc": "Konzeption, Entwicklung und Durchführung von Maßnahmen zu Finanzverständnis, Kennzahlen und wirtschaftlicher Bewertung von Veränderungsvorhaben.",
    "audience_type": "Geschäftsleitungen, Führungskräfte, Projektverantwortliche",
}


def build():
    return [fokus_page(VERHANDLUNG), fokus_page(LEADERSHIP), fokus_page(FINANCE)]
