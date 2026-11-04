"""KI-Readiness Check: Werkzeug aus dem Prototyp (Markup in ki_readiness_body.html, Stil in assets/ki-readiness.css,
Logik in assets/ki-readiness.js). Die FAQ kommt aus ki_readiness_faq.json, damit sichtbarer Text und Schema identisch sind."""
import json
import os

from helpers import esc

HERE = os.path.dirname(__file__)

TITLE = "KI-Readiness Check — Ihr KI-Gap in 3 Minuten | THE GAP Lab"
DESC = ("Kostenloser KI-Readiness Check in 3 Minuten: Acht Signale, Management- und Mitarbeitendensicht "
        "und Ihr KI-Gap, ohne Login und mit sofortigem Ergebnis.")


def _read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


def ki_readiness():
    faqs = [(q, f"<p>{esc(a)}</p>") for q, a in json.loads(_read("ki_readiness_faq.json"))]
    faq_html = '<div class="k-faq">' + "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>"
        for q, a in json.loads(_read("ki_readiness_faq.json"))
    ) + "</div>"
    body = _read("ki_readiness_body.html").replace("{{FAQ}}", faq_html)
    return {
        "path": "/ki-readiness", "short": "KI-Readiness",
        "title": TITLE, "og_title": "Ihre KI-Strategie steht. Steht Ihre Organisation auch?",
        "description": DESC,
        "priority": "0.8", "llms_group": "Werkzeuge", "faqs": faqs,
        "show_stand": False, "modified": "2026-11-04",
        "og_image": "/assets/img/og-ki-readiness.jpg", "og_image_height": 627,
        "og_alt": "KI-Readiness Check von THE GAP Lab: Management- und Mitarbeitendensicht im Vergleich",
        "styles": ["/assets/ki-readiness.css"], "scripts": ["/assets/ki-readiness.js"], "speakable": False,
        "schema_nodes": [{
            "@type": "WebApplication", "@id": "https://www.gap-lab.de/ki-readiness#app", "name": "KI-Readiness Check",
            "url": "https://www.gap-lab.de/ki-readiness", "applicationCategory": "BusinessApplication", "operatingSystem": "Browser",
            "inLanguage": "de-DE", "isAccessibleForFree": True,
            "description": "Kostenloser Check in drei Minuten: acht Signale zur KI-Reife einer Organisation, Management- und Mitarbeitendensicht, KI-Gap und Handlungsfeld.",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
            "provider": {"@id": "https://www.gap-lab.de/#organization"},
        }],
        "body": '<div class="kic">' + body + "</div>",
    }


def build():
    return [ki_readiness()]
