"""Stammdaten. Quelle für Registerangaben: Mitteilung über die Eintragung im Handelsregister B Nürnberg
vom 23.09.2026 (HRB 46649). Personenangaben: veröffentlichte Profile auf schubart-dulgeridis.de.
Nichts hier ist erfunden; fehlende Registerangaben (Stammkapital, vollständiger Unternehmensgegenstand,
USt-IdNr.) stehen bewusst NICHT in den öffentlichen Texten."""

import re

SITE = {
    "domain": "https://www.gap-lab.de",
    "brand": "THE GAP Lab",
    "legal_name": "The Gap Lab GmbH",
    "street": "Hessenstraße 28",
    "zip": "90518",
    "city": "Altdorf bei Nürnberg",
    "hrb": "HRB 46649",
    "court": "Amtsgericht Nürnberg",
    "court_gen": "Amtsgerichts Nürnberg",
    "registered": "23.09.2026",
    "articles_date": "16.09.2026",
    "email": "info@schubart-dulgeridis.de",
    "phone": "+49 30 695 19 779",
    "phone_e164": "+493069519779",
    "parent_name": "Schubart & Dulgeridis GmbH",
    "parent_url": "https://www.schubart-dulgeridis.de/",
    "parent_id": "https://www.schubart-dulgeridis.de/#organization",
    "booking_url": "https://www.schubart-dulgeridis.de/kontakt",
    "published": "2026-10-06",
    "modified": "2026-11-10",
    "modified_de": "10. November 2026",
    "org_description": (
        "The Gap Lab GmbH (THE GAP Lab) mit Sitz in Altdorf bei Nürnberg konzipiert, entwickelt, führt durch und "
        "vermarktet Maßnahmen der Personalentwicklung. Schwerpunkte: Strategie, Vertrieb & Innovation, "
        "Leadership & Organisation sowie Finance & Transformation. Tochtergesellschaft der Schubart & Dulgeridis GmbH."
    ),
    "llms_summary": (
        "THE GAP Lab ist die Marke der The Gap Lab GmbH (Altdorf bei Nürnberg, HRB 46649, Amtsgericht Nürnberg). "
        "Die Gesellschaft konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung "
        "mit drei Fokusfeldern: Strategie, Vertrieb & Innovation, Leadership & Organisation, Finance & Transformation. "
        "Tochtergesellschaft der Schubart & Dulgeridis GmbH."
    ),
    "knows_about": [
        "Personalentwicklung",
        "Strategie, Vertrieb und Innovation",
        "Verhandlungsführung und Rhetorik",
        "Leadership und Organisation",
        "Finance und Transformation",
    ],
}

PARTNERS = {
    "constantin-schubart": {
        "name": "Prof. Dr. Constantin Schubart",
        "role": "Geschäftsführer",
        "focus": "Leadership & Organisation",
        "job_title": "Geschäftsführer, Leadership & Organisation",
        "short_bio": "Professor für BWL an der IU Internationalen Hochschule. Rollen im Zusammenspiel von Strategie, Kultur und Führung.",
        "long_bio": "Professor für Betriebswirtschaftslehre an der IU Internationalen Hochschule. Betrachtet Rollen im Zusammenspiel von Strategie, Kultur und Führung.",
        "schema_desc": "Professor für Betriebswirtschaftslehre an der IU Internationalen Hochschule und Geschäftsführer der The Gap Lab GmbH. Fokus: Leadership und Organisation.",
        "img": "/assets/img/portrait-constantin-schubart.webp",
        "sd_url": "https://www.schubart-dulgeridis.de/ueber-uns#constantin-schubart",
        "linkedin": "https://www.linkedin.com/in/constantin-schubart-384ab517/",
        "same_as": [
            "https://www.schubart-dulgeridis.de/ueber-uns#constantin-schubart",
            "https://www.linkedin.com/in/constantin-schubart-384ab517/",
        ],
        "fokus_path": "/fokusfelder/leadership-organisation",
        "knows_about": ["Leadership", "Organisation", "Betriebswirtschaftslehre"],
    },
    "oliver-meschkat": {
        "name": "Dr. Oliver Meschkat",
        "role": "Partner",
        "focus": "Strategie, Vertrieb & Innovation",
        "job_title": "Partner, Strategie, Vertrieb & Innovation",
        "short_bio": "Marketing- und Sales-Management, Personalentwicklung, Innovations- und Change Management.",
        "long_bio": "Marketing- und Sales-Management, Personalentwicklung, Innovations- und Change Management. Trainer und Berater seit 2010 zu Leadership, Teambuilding, Verhandlungsführung, Verkaufstraining, Konfliktmanagement, strategischem Management, Rhetorik, Moderation und Kommunikation.",
        "schema_desc": "Partner der The Gap Lab GmbH für Marketing- und Sales-Management, Personalentwicklung sowie Innovations- und Change Management. Trainer und Berater seit 2010.",
        "img": "/assets/img/portrait-oliver-meschkat.jpg",
        "sd_url": "https://www.schubart-dulgeridis.de/ueber-uns#oliver-meschkat",
        "linkedin": "https://www.linkedin.com/in/dr-oliver-meschkat-a8a80b58/",
        "same_as": [
            "https://www.schubart-dulgeridis.de/ueber-uns#oliver-meschkat",
            "https://www.linkedin.com/in/dr-oliver-meschkat-a8a80b58/",
        ],
        "fokus_path": "/fokusfelder/strategie-vertrieb-innovation",
        "knows_about": ["Marketing- und Sales-Management", "Personalentwicklung", "Innovationsmanagement", "Change Management", "Strategisches Management", "Verhandlungsführung", "Verkaufstraining", "Rhetorik", "Moderation", "Konfliktmanagement", "Teambuilding"],
    },
    "marcel-dulgeridis": {
        "name": "Prof. Dr. Marcel Dulgeridis",
        "role": "Partner",
        "focus": "Finance & Transformation",
        "job_title": "Partner, Finance & Transformation",
        "short_bio": "Professor für BWL an der IU Internationalen Hochschule. Schwerpunkt Rechnungswesen und Finanzberichterstattung.",
        "long_bio": "Professor für Betriebswirtschaftslehre an der IU Internationalen Hochschule (Campus Regensburg). Schwerpunkt Rechnungswesen und Finanzberichterstattung.",
        "schema_desc": "Professor für Betriebswirtschaftslehre an der IU Internationalen Hochschule mit Schwerpunkt Rechnungswesen und Finanzberichterstattung. Partner der The Gap Lab GmbH.",
        "img": "/assets/img/portrait-marcel-dulgeridis.webp",
        "sd_url": "https://www.schubart-dulgeridis.de/ueber-uns#marcel-dulgeridis",
        "linkedin": "https://www.linkedin.com/in/marceldulgeridis/",
        "same_as": [
            "https://www.schubart-dulgeridis.de/ueber-uns#marcel-dulgeridis",
            "https://www.linkedin.com/in/marceldulgeridis/",
            "https://www.iu.de/hochschule/lehrende/dulgeridis-marcel/",
        ],
        "fokus_path": "/fokusfelder/finance-transformation",
        "knows_about": ["Rechnungswesen", "Finanzberichterstattung", "Transformation"],
    },
}

# (Label, Pfad, ist_CTA)
NAV = [
    ("Leistungen", "/leistungen", False),
    ("Fokusfelder", "/fokusfelder", False),
    ("InnoLab", "/innolab", False),
    ("KI-Readiness", "/ki-readiness", False),
    ("Über uns", "/ueber-uns", False),
    ("FAQ", "/faq", False),
    ("Erstgespräch", "/kontakt", True),
]

FOOTER_LINKS = [
    ("Leistungen", [
        ("InnoLab", "/innolab"),
        ("Konzeption", "/leistungen#konzeption"),
        ("Entwicklung", "/leistungen#entwicklung"),
        ("Durchführung", "/leistungen#durchfuehrung"),
        ("Vermarktung", "/leistungen#vermarktung"),
    ]),
    ("Fokusfelder", [
        ("Strategie, Vertrieb & Innovation", "/fokusfelder/strategie-vertrieb-innovation"),
        ("Leadership & Organisation", "/fokusfelder/leadership-organisation"),
        ("Finance & Transformation", "/fokusfelder/finance-transformation"),
    ]),
    ("Unternehmen", [
        ("Über uns", "/ueber-uns"),
        ("KI-Readiness Check", "/ki-readiness"),
        ("Glossar", "/glossar"),
        ("FAQ", "/faq"),
        ("Kontakt", "/kontakt"),
        ("Impressum", "/impressum"),
        ("Datenschutz", "/datenschutz"),
        ("Schubart & Dulgeridis GmbH", "https://www.schubart-dulgeridis.de/"),
    ]),
]


for _p in PARTNERS.values():
    _p["img_sm"] = re.sub(r"\.(jpg|webp)$", "-sm.jpg", _p["img"])
