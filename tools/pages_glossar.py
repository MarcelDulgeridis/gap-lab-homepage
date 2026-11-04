"""Glossar: zentrale Begriffe der drei Fokusfelder und der Marke. Definitionen stammen aus den Fokusfeld-Seiten
und den Angebotsseiten; hier nur gebündelt, mit DefinedTermSet-Schema (GEO)."""
import re
import unicodedata

from siteinfo import SITE
from helpers import esc, url_of, ARROW, cta_band, page_hero, section, head, answer_box, strip_tags
import visuals as V

PATH = "/glossar"


def _slug(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def terms():
    import pages_fokus as F
    out = []
    groups = [("f1", "Verhandlungsführung", "/fokusfelder/verhandlungsfuehrung", F.VERHANDLUNG),
              ("f2", "Leadership &amp; Organisation", "/fokusfelder/leadership-organisation", F.LEADERSHIP),
              ("f3", "Finance &amp; Transformation", "/fokusfelder/finance-transformation", F.FINANCE)]
    for cls, label, path, cfg in groups:
        for name, text in cfg["begriffe"]:
            out.append((name, text, cls, label, path))
    out += [
        ("THE GAP Lab", "Marke der The Gap Lab GmbH mit Sitz in Altdorf bei Nürnberg. Die Gesellschaft konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung und ist eine Tochtergesellschaft der Schubart & Dulgeridis GmbH.", "f4", "THE GAP Lab", "/ueber-uns"),
        ("Fokusfeld", "Eines der drei inhaltlichen Schwerpunktgebiete von THE GAP Lab: Verhandlungsführung & Rhetorik, Leadership & Organisation sowie Finance & Transformation. Jedes Fokusfeld hat einen benannten Partner als Ansprechpartner.", "f4", "THE GAP Lab", "/fokusfelder"),
        ("InnoLab", "Portfolio aus fünf Formaten vor Ort für Innovation, Change und Personalentwicklung (InnoLab Sprint, InnoLab Design, Learning Design 4.0, Change Leadership, Innovation Scorecard), jeweils mit eigenem Ergebnis.", "f4", "THE GAP Lab", "/innolab"),
        ("KI-Gap", "Der Abstand zwischen der Einschätzung der Führung und der Einschätzung der Mitarbeitenden zur KI-Reife der eigenen Organisation. Der kostenlose KI-Readiness Check macht ihn in drei Minuten sichtbar.", "f4", "THE GAP Lab", "/ki-readiness"),
    ]
    return sorted(out, key=lambda t: t[0].lower().replace("ä", "a").replace("ö", "o").replace("ü", "u"))


def glossar():
    ts = terms()
    letters = sorted({t[0][0].upper() for t in ts})
    az = '<ul class="v-az" aria-label="Alphabet">' + "".join(f'<li><a href="#b-{l.lower()}">{l}</a></li>' for l in letters) + "</ul>"
    seen, rows = set(), []
    for name, text, cls, label, path in ts:
        l = name[0].upper()
        anchor = f' id="b-{l.lower()}"' if l not in seen else ""
        seen.add(l)
        rows.append(
            f'<div class="v-term {cls}"{anchor}><dt id="{_slug(name)}">{esc(name)}<span>{label}</span></dt>'
            f'<dd>{esc(text)} <a href="{path}">Mehr dazu {ARROW}</a></dd></div>')
    page = {
        "path": PATH, "short": "Glossar",
        "title": "Glossar — Begriffe der Personalentwicklung | THE GAP Lab",
        "description": f"{len(ts)} Begriffe kurz erklärt: BATNA, ZOPA, Cashflow, Business Case, Rollenklarheit, KI-Gap und mehr, mit Link zum passenden Fokusfeld.",
        "priority": "0.7", "llms_group": "Wissen", "show_stand": False, "speakable": True,
        "styles": ["/assets/visual.css"], "journey": None,
    }
    defined = [{
        "@type": "DefinedTerm", "@id": f"{url_of(PATH)}#{_slug(n)}", "name": n, "description": t,
        "url": f"{url_of(PATH)}#{_slug(n)}", "inDefinedTermSet": {"@id": url_of(PATH) + "#termset"},
    } for n, t, c, l, p in ts]
    page["schema_nodes"] = [{"@type": "DefinedTermSet", "@id": url_of(PATH) + "#termset", "name": "Glossar von THE GAP Lab",
                             "inLanguage": "de-DE", "hasDefinedTerm": [{"@id": d["@id"]} for d in defined]}] + defined
    page["body"] = (
        page_hero(page, "Glossar: die wichtigsten Begriffe verständlich erklärt",
                  "Von Verhandlung über Führung bis Finanzen: Diese Begriffe tragen die Fokusfelder von THE GAP Lab.")
        + section(
            answer_box("Kurz erklärt", f"Das Glossar erklärt {len(ts)} Begriffe aus Verhandlungsführung (zum Beispiel BATNA, ZOPA, Anker), Leadership &amp; Organisation (zum Beispiel Rollenklarheit, Umsetzungslücke) und Finance &amp; Transformation (zum Beispiel Cashflow, Business Case) sowie zentrale Begriffe von THE GAP Lab. Jeder Eintrag verweist auf die Seite, die ihn im Zusammenhang erklärt.")
            + az + f'<dl class="v-gloss">{"".join(rows)}</dl>', "", "")
        + cta_band("Begriffe, die in Ihrer Organisation geklärt sind.", "Im Erstgespräch ordnen wir ein, welcher Begriff und welches Fokusfeld für Ihre Ausgangslage zählt.")
    )
    return page


def build():
    return [glossar()]
