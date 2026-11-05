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
    "Vertrieb": WIKI + "Vertrieb",
    "Strategisches Management": WIKI + "Strategisches_Management",
    "Marketing": WIKI + "Marketing",
    "Konfliktmanagement": WIKI + "Konfliktmanagement",
}

META = {
    "/": {
        "og_image": "/assets/img/og-verbindet.jpg", "og_kicker": "STRATEGIE · FÜHRUNG · FINANCE", "og_line1": "Personalentwicklung,", "og_line2": "die verbindet.",
        "og_sub": "Strategie, Führungsklarheit und Finanzverständnis.",
        "og_alt": "THE GAP Lab: Personalentwicklung, die verbindet. Strategie, Führungsklarheit und Finanzverständnis.",
        "title": "Personalentwicklung Nürnberg für Führungskräfte | THE GAP Lab",
        "description": "Personalentwicklung für Führungskräfte: Strategie, Vertrieb, Leadership und Finanzverständnis, von Konzeption bis Durchführung. Kostenloses Erstgespräch.",
        "keywords": "Personalentwicklung, Führungskräfteentwicklung, Vertriebstraining, Verhandlungstraining, Leadership, Finanzverständnis, Nürnberg",
        "topics": ["Personalentwicklung", "Führung", "Verhandlung"],
    },
    "/leistungen": {
        "title": "Personalentwicklung: Konzeption bis Durchführung | THE GAP Lab",
        "description": "Vier Stufen für Ihre Personalentwicklung: Konzeption, Entwicklung, Durchführung und Vermarktung. Einzeln oder als Kette buchbar, mit Ergebnissen je Stufe.",
        "keywords": "Personalentwicklung, Konzeption, Workshop, Training, Vermarktung",
        "topics": ["Personalentwicklung"],
        "og_sub": "Konzeption · Entwicklung · Durchführung · Vermarktung", "og_image": "/assets/img/og-leistungen.jpg", "og_kicker": "LEISTUNGEN", "og_line1": "Vier Stufen von der Idee", "og_line2": "zur Maßnahme.",
    },
    "/fokusfelder": {
        "title": "Fokusfelder: Strategie, Führung, Finance | THE GAP Lab",
        "description": "Strategie, Vertrieb & Innovation, Leadership & Organisation, Finance & Transformation: drei Fokusfelder der Personalentwicklung mit je eigenem Ansprechpartner.",
        "keywords": "Strategie, Vertrieb, Innovation, Leadership, Finance, Fokusfelder, Personalentwicklung",
        "topics": ["Verhandlung", "Führung", "Kennzahl"],
        "og_sub": "Strategie · Leadership · Finance", "og_image": "/assets/img/og-fokusfelder.jpg", "og_kicker": "FOKUSFELDER", "og_line1": "Gestalten, Führen,", "og_line2": "Wirtschaften.",
    },
    "/fokusfelder/strategie-vertrieb-innovation": {
        "title": "Strategie, Vertrieb & Innovation: Training | THE GAP Lab",
        "description": "Strategie, Vertriebstraining, Verhandlung und Innovation: Marketing- und Sales-Management, Change Management und Rhetorik mit Dr. Oliver Meschkat.",
        "keywords": "Strategie, Vertriebstraining, Verkaufstraining, Verhandlungstraining, Innovationsmanagement, Change Management, BATNA, ZOPA",
        "topics": ["Strategisches Management", "Vertrieb", "Marketing", "Innovation", "Veränderungsmanagement", "Verhandlung", "Konfliktmanagement"], "reviewer": "oliver-meschkat",
        "og_sub": "Dr. Oliver Meschkat · Vertrieb · Innovation · Change", "og_image": "/assets/img/og-strategie-vertrieb.jpg", "og_kicker": "FOKUSFELD GESTALTEN", "og_line1": "Strategie festlegen,", "og_line2": "Kunden überzeugen.",
    },
    "/fokusfelder/leadership-organisation": {
        "title": "Führungskräfteentwicklung & Leadership | THE GAP Lab",
        "description": "Führungskräfteentwicklung für klare Rollen, Entscheidungsrechte und Führungskultur: damit Strategie im Arbeitsalltag ankommt. Mit Prof. Dr. Constantin Schubart.",
        "keywords": "Führungskräfteentwicklung, Leadership, Führungskultur, Rollenklarheit, Entscheidungsrechte, Umsetzungslücke",
        "topics": ["Führung", "Personalentwicklung", "Veränderungsmanagement"], "reviewer": "constantin-schubart",
        "og_sub": "Prof. Dr. Constantin Schubart · Rollen · Führungskultur", "og_image": "/assets/img/og-leadership.jpg", "og_kicker": "FOKUSFELD FÜHREN", "og_line1": "Von der Strategie", "og_line2": "in den Alltag.",
    },
    "/fokusfelder/finance-transformation": {
        "title": "Finanzverständnis für Führungskräfte | THE GAP Lab",
        "description": "Finance für Nicht-Finanzer: GuV, Bilanz, Cashflow, Kennzahlen und Business Case verständlich vermittelt. Maßnahmen mit Prof. Dr. Marcel Dulgeridis.",
        "keywords": "Finanzverständnis, Kennzahlen, Business Case, Cashflow, GuV, Bilanz",
        "topics": ["Cashflow", "Gewinn- und Verlustrechnung", "Kennzahl"], "reviewer": "marcel-dulgeridis",
        "og_sub": "Prof. Dr. Marcel Dulgeridis · GuV · Bilanz · Cashflow", "og_image": "/assets/img/og-finance.jpg", "og_kicker": "FOKUSFELD WIRTSCHAFTEN", "og_line1": "Finanzverständnis für", "og_line2": "wirtschaftliche Veränderung.",
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
        "og_sub": "Drei Partner · Verbund mit Schubart & Dulgeridis", "og_image": "/assets/img/og-ueber-uns.jpg", "og_kicker": "ÜBER UNS", "og_line1": "Drei Partner,", "og_line2": "eine Gesellschaft.",
    },
    "/kontakt": {
        "title": "Kontakt & kostenloses Erstgespräch | THE GAP Lab",
        "description": "Kostenloses Erstgespräch (20–30 Min.) mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis buchen oder per E-Mail anfragen. Altdorf bei Nürnberg.",
        "keywords": "Erstgespräch, Kontakt, Termin buchen, Altdorf bei Nürnberg",
        "topics": ["Personalentwicklung"],
        "og_sub": "Microsoft Teams · kostenlos · unverbindlich", "og_image": "/assets/img/og-kontakt.jpg", "og_kicker": "KONTAKT", "og_line1": "Kostenloses Erstgespräch,", "og_line2": "20 bis 30 Minuten.",
    },
    "/faq": {
        "title": "FAQ: {faq} Antworten zu Personalentwicklung | THE GAP Lab",
        "keywords": "FAQ, Personalentwicklung, Strategie, InnoLab, KI-Readiness Check, Zusammenarbeit",
        "topics": ["Personalentwicklung"],
        "og_sub": "Angebot · Fokusfelder · InnoLab · Datenschutz", "og_image": "/assets/img/og-faq.jpg", "og_kicker": "FAQ", "og_line1": "{faq} Antworten zu", "og_line2": "Personalentwicklung.",
    },
    "/glossar": {
        "title": "Glossar: BATNA, ZOPA, Cashflow, KI-Gap erklärt | THE GAP Lab",
        "keywords": "Glossar, BATNA, ZOPA, Cashflow, Business Case, Rollenklarheit, KI-Gap",
        "topics": ["Verhandlung", "Cashflow", "Führung"],
        "og_sub": "BATNA · ZOPA · Cashflow · Business Case · KI-Gap", "og_image": "/assets/img/og-glossar.jpg", "og_kicker": "GLOSSAR", "og_line1": "{glossar} Begriffe", "og_line2": "kurz erklärt.",
    },
}


def _counts():
    import pages_faq
    import pages_glossar
    return {"faq": len(pages_faq.ALL), "glossar": len(pages_glossar.terms())}


def resolve(m):
    c = _counts()
    return {k: (v.format(**c) if isinstance(v, str) else v) for k, v in m.items()}


def apply(pages):
    for p in pages:
        m = META.get(p["path"])
        if not m:
            continue
        m = resolve(m)
        for k in ("title", "description"):
            if k in m:
                p[k] = m[k]
        for k in ("keywords", "topics", "reviewer", "og_kicker", "og_line1", "og_line2"):
            if k in m:
                p["seo_" + k] = m[k]
        if "og_image" in m:
            p["og_image"] = m["og_image"]
            p["og_image_height"] = 630
            p["og_alt"] = m.get("og_alt") or f"{m['og_kicker'].capitalize()}: {m['og_line1']} {m['og_line2']} THE GAP Lab"
    return pages
