"""SEO/GEO-Steuerung je Seite: Suchtitel, Beschreibung, Social-Bild, thematische Entitäten, fachlich Verantwortliche.
Wird in build.all_pages() auf die Seiten angewendet; Seitenmodule bleiben unberührt.
Wikipedia-Verweise (sameAs) wurden einzeln auf Existenz geprüft."""

WIKI = "https://de.wikipedia.org/wiki/"
TOPIC = {
    "Personalentwicklung": WIKI + "Personalentwicklung",
    "Verhandlung": WIKI + "Verhandlung",
    "Führung": WIKI + "F%C3%BChrung",
    "Cashflow": WIKI + "Cashflow",
    "Innovation": WIKI + "Innovation",
    "Veränderungsmanagement": WIKI + "Ver%C3%A4nderungsmanagement",
    "Künstliche Intelligenz": WIKI + "K%C3%BCnstliche_Intelligenz",
    "Harvard-Konzept": WIKI + "Harvard-Konzept",
    "Rhetorik": WIKI + "Rhetorik",
    "Gewinn- und Verlustrechnung": WIKI + "Gewinn-_und_Verlustrechnung",
    "Kennzahl": WIKI + "Kennzahl",
}

META = {
    "/": {
        "title": "Personalentwicklung Nürnberg für Führungskräfte | THE GAP Lab",
        "description": "Personalentwicklung für Führungskräfte: Verhandlungsführung, Leadership und Finanzverständnis, von Konzeption bis Durchführung. Kostenloses Erstgespräch.",
        "keywords": "Personalentwicklung, Führungskräfteentwicklung, Verhandlungstraining, Leadership, Finanzverständnis, Nürnberg",
        "topics": ["Personalentwicklung", "Führung", "Verhandlung"],
    },
    "/leistungen": {
        "title": "Personalentwicklung: Konzeption bis Durchführung | THE GAP Lab",
        "description": "Vier Stufen für Ihre Personalentwicklung: Konzeption, Entwicklung, Durchführung und Vermarktung. Einzeln oder als Kette buchbar, mit Ergebnissen je Stufe.",
        "keywords": "Personalentwicklung, Konzeption, Workshop, Training, Vermarktung",
        "topics": ["Personalentwicklung"],
        "og_image": "/assets/img/og-leistungen.jpg", "og_kicker": "LEISTUNGEN", "og_line1": "Vier Stufen von der Idee", "og_line2": "zur Maßnahme.",
    },
    "/fokusfelder": {
        "title": "Fokusfelder: Verhandlung, Führung, Finance | THE GAP Lab",
        "description": "Verhandlungsführung & Rhetorik, Leadership & Organisation, Finance & Transformation: drei Fokusfelder der Personalentwicklung mit je eigenem Ansprechpartner.",
        "keywords": "Verhandlungsführung, Leadership, Finance, Fokusfelder, Personalentwicklung",
        "topics": ["Verhandlung", "Führung", "Kennzahl"],
        "og_image": "/assets/img/og-fokusfelder.jpg", "og_kicker": "FOKUSFELDER", "og_line1": "Verhandeln, Führen,", "og_line2": "Wirtschaften.",
    },
    "/fokusfelder/verhandlungsfuehrung": {
        "title": "Verhandlungstraining & Rhetorik | THE GAP Lab",
        "description": "Verhandlungstraining und Rhetorik für Entscheider: BATNA, ZOPA, Anker, Argumentation. Maßnahmen an Ihren eigenen Verhandlungsfällen, mit Dr. Oliver Meschkat.",
        "keywords": "Verhandlungstraining, Verhandlungsführung, Rhetorik, BATNA, ZOPA, Harvard-Konzept, Preisverhandlungen",
        "topics": ["Verhandlung", "Rhetorik", "Harvard-Konzept"], "reviewer": "oliver-meschkat",
        "og_image": "/assets/img/og-verhandlungsfuehrung.jpg", "og_kicker": "FOKUSFELD VERHANDELN", "og_line1": "Vorbereitet verhandeln,", "og_line2": "überzeugend argumentieren.",
    },
    "/fokusfelder/leadership-organisation": {
        "title": "Führungskräfteentwicklung & Leadership | THE GAP Lab",
        "description": "Führungskräfteentwicklung für klare Rollen, Entscheidungsrechte und Führungskultur: damit Strategie im Arbeitsalltag ankommt. Mit Prof. Dr. Constantin Schubart.",
        "keywords": "Führungskräfteentwicklung, Leadership, Führungskultur, Rollenklarheit, Entscheidungsrechte, Umsetzungslücke",
        "topics": ["Führung", "Personalentwicklung", "Veränderungsmanagement"], "reviewer": "constantin-schubart",
        "og_image": "/assets/img/og-leadership.jpg", "og_kicker": "FOKUSFELD FÜHREN", "og_line1": "Von der Strategie", "og_line2": "in den Alltag.",
    },
    "/fokusfelder/finance-transformation": {
        "title": "Finanzverständnis für Führungskräfte | THE GAP Lab",
        "description": "Finance für Nicht-Finanzer: GuV, Bilanz, Cashflow, Kennzahlen und Business Case verständlich vermittelt. Maßnahmen mit Prof. Dr. Marcel Dulgeridis.",
        "keywords": "Finanzverständnis, Kennzahlen, Business Case, Cashflow, GuV, Bilanz",
        "topics": ["Cashflow", "Gewinn- und Verlustrechnung", "Kennzahl"], "reviewer": "marcel-dulgeridis",
        "og_image": "/assets/img/og-finance.jpg", "og_kicker": "FOKUSFELD WIRTSCHAFTEN", "og_line1": "Finanzverständnis für", "og_line2": "wirtschaftliche Veränderung.",
    },
    "/innolab": {
        "title": "InnoLab: Innovationsworkshops ab 5.800 € netto | THE GAP Lab",
        "description": "Fünf Innovationsworkshops vor Ort: Sprint, Lernraumberatung, Train the Trainer, Change Leadership und Innovation Scorecard. Festpreis ab 5.800 € netto.",
        "keywords": "Innovationsworkshop, InnoLab Sprint, Train the Trainer, Change Leadership, Innovation Scorecard, Innovation Lab",
        "topics": ["Innovation", "Veränderungsmanagement", "Personalentwicklung"], "reviewer": "oliver-meschkat",
    },
    "/ki-readiness": {
        "title": "KI-Readiness Check kostenlos: KI-Gap in 3 Min. | THE GAP Lab",
        "description": "Kostenloser KI-Readiness Check als Selbsttest: in 3 Minuten acht Signale, Management- und Mitarbeitendensicht und Ihr KI-Gap, ohne Login, mit Sofortergebnis.",
        "keywords": "KI-Readiness Check, KI-Reifegrad, KI-Gap, KI-Strategie, Schatten-KI, Selbsttest",
        "topics": ["Künstliche Intelligenz"],
    },
    "/ueber-uns": {
        "title": "Über uns: Team, Professoren und Partner | THE GAP Lab",
        "description": "Das Team hinter THE GAP Lab: Prof. Dr. Constantin Schubart, Dr. Oliver Meschkat und Prof. Dr. Marcel Dulgeridis, im Verbund mit Schubart & Dulgeridis.",
        "keywords": "Team, Geschäftsführer, Partner, Professoren, IU Internationale Hochschule, Schubart & Dulgeridis",
        "topics": ["Personalentwicklung"],
        "og_image": "/assets/img/og-ueber-uns.jpg", "og_kicker": "ÜBER UNS", "og_line1": "Drei Partner,", "og_line2": "eine Gesellschaft.",
    },
    "/kontakt": {
        "title": "Kontakt & kostenloses Erstgespräch | THE GAP Lab",
        "description": "Kostenloses Erstgespräch (20–30 Min.) mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis buchen oder per E-Mail anfragen. Altdorf bei Nürnberg.",
        "keywords": "Erstgespräch, Kontakt, Termin buchen, Altdorf bei Nürnberg",
        "topics": ["Personalentwicklung"],
        "og_image": "/assets/img/og-kontakt.jpg", "og_kicker": "KONTAKT", "og_line1": "Kostenloses Erstgespräch,", "og_line2": "20 bis 30 Minuten.",
    },
    "/faq": {
        "title": "FAQ: 38 Antworten zu Personalentwicklung | THE GAP Lab",
        "keywords": "FAQ, Personalentwicklung, Verhandlungsführung, InnoLab, KI-Readiness Check, Zusammenarbeit",
        "topics": ["Personalentwicklung"],
        "og_image": "/assets/img/og-faq.jpg", "og_kicker": "FAQ", "og_line1": "38 Antworten zu", "og_line2": "Personalentwicklung.",
    },
    "/glossar": {
        "title": "Glossar: BATNA, ZOPA, Cashflow, KI-Gap erklärt | THE GAP Lab",
        "keywords": "Glossar, BATNA, ZOPA, Cashflow, Business Case, Rollenklarheit, KI-Gap",
        "topics": ["Verhandlung", "Cashflow", "Führung"],
        "og_image": "/assets/img/og-glossar.jpg", "og_kicker": "GLOSSAR", "og_line1": "19 Begriffe", "og_line2": "kurz erklärt.",
    },
}


def apply(pages):
    for p in pages:
        m = META.get(p["path"])
        if not m:
            continue
        for k in ("title", "description"):
            if k in m:
                p[k] = m[k]
        for k in ("keywords", "topics", "reviewer", "og_kicker", "og_line1", "og_line2"):
            if k in m:
                p["seo_" + k] = m[k]
        if "og_image" in m:
            p["og_image"] = m["og_image"]
            p["og_image_height"] = 630
            p["og_alt"] = f"{m['og_kicker'].capitalize()}: {m['og_line1']} {m['og_line2']} THE GAP Lab"
    return pages
