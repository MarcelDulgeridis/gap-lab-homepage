#!/usr/bin/env python3
"""Statischer Seitengenerator für gap-lab.de.

Aufruf:  python3 tools/build.py
Erzeugt alle HTML-Seiten, sitemap.xml, robots.txt und llms.txt im Projektroot.
Inhalte stehen in tools/pages_*.py, Stammdaten in tools/site.py.
"""
import hashlib
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))

from siteinfo import SITE, PARTNERS, NAV, FOOTER_LINKS  # noqa: E402
from helpers import esc, strip_tags, url_of, ARROW  # noqa: E402
from schema_nodes import person_node  # noqa: E402
import pages_core  # noqa: E402
import pages_fokus  # noqa: E402
import pages_glossar  # noqa: E402
import pages_innolab  # noqa: E402
import pages_ki  # noqa: E402
import pages_legal  # noqa: E402
import seo_meta  # noqa: E402
import datetime  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOMAIN = SITE["domain"]


def asset_hash(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:8]


CSS_V = asset_hash("assets/site.css")
JS_V = asset_hash("assets/site.js")


def versioned(path):
    return f"{path}?v={asset_hash(path.lstrip('/'))}"


def out_file(path):
    return "index.html" if path == "/" else path.lstrip("/") + ".html"


# ---------------------------------------------------------------- Schema.org
def org_node():
    return {
        "@type": "Organization",
        "@id": f"{DOMAIN}/#organization",
        "name": SITE["brand"],
        "legalName": SITE["legal_name"],
        "url": f"{DOMAIN}/",
        "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/icon-512.png", "width": 512, "height": 512},
        "image": f"{DOMAIN}/assets/img/og-the-gap-lab.jpg",
        "description": SITE["org_description"],
        "email": SITE["email"],
        "telephone": SITE["phone_e164"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE["street"],
            "postalCode": SITE["zip"],
            "addressLocality": SITE["city"],
            "addressCountry": "DE",
        },
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "Handelsregister",
            "value": f"{SITE['hrb']}, {SITE['court']}",
        },
        "parentOrganization": {"@id": SITE["parent_id"]},
        "employee": [person_node(k, full=False) for k in PARTNERS],
        "knowsAbout": SITE["knows_about"],
        "slogan": "Personalentwicklung, die im Arbeitsalltag ankommt.",
        "areaServed": {"@type": "Country", "name": "Deutschland"},
        "sameAs": [SITE["parent_url"]],
        "alternateName": ["The Gap Lab", "The Gap Lab GmbH"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Leistungen von THE GAP Lab",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@id": f"{DOMAIN}/leistungen#service"}},
                {"@type": "Offer", "itemOffered": {"@id": f"{DOMAIN}/fokusfelder/verhandlungsfuehrung#service"}},
                {"@type": "Offer", "itemOffered": {"@id": f"{DOMAIN}/fokusfelder/leadership-organisation#service"}},
                {"@type": "Offer", "itemOffered": {"@id": f"{DOMAIN}/fokusfelder/finance-transformation#service"}},
            ],
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "Anfragen und Erstgespräch",
            "email": SITE["email"],
            "telephone": SITE["phone_e164"],
            "availableLanguage": "de",
        },
    }


def breadcrumb_node(page):
    items = [("Start", "/")] + list(page.get("crumbs", []))
    if page["path"] != "/" and not page.get("crumbs"):
        items.append((page["short"], page["path"]))
    elif page["path"] != "/":
        items.append((page["short"], page["path"]))
    return {
        "@type": "BreadcrumbList",
        "@id": url_of(page["path"]) + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": url_of(p)}
            for i, (n, p) in enumerate(items)
        ],
    }


def faq_node(page_url, faqs, node_id=None):
    return {
        "@type": "FAQPage",
        "@id": node_id or page_url + "#faq",
        "isPartOf": {"@id": page_url + "#webpage"},
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)},
            }
            for q, a in faqs
        ],
    }


def graph_for(page):
    url = url_of(page["path"])
    web_type = page.get("schema_type", "WebPage")
    webpage = {
        "@type": web_type,
        "@id": url + "#webpage",
        "url": url,
        "name": page["title"],
        "description": page["description"],
        "inLanguage": "de-DE",
        "isPartOf": {"@id": f"{DOMAIN}/#website"},
        "about": {"@id": f"{DOMAIN}/#organization"},
        "datePublished": SITE["published"],
        "dateModified": page.get("modified", SITE["modified"]),
        "primaryImageOfPage": {"@type": "ImageObject", "url": DOMAIN + page.get("og_image", "/assets/img/og-the-gap-lab.jpg")},
    }
    if page.get("seo_keywords"):
        webpage["keywords"] = page["seo_keywords"]
    topics = page.get("seo_topics")
    if topics:
        webpage["about"] = [{"@id": f"{DOMAIN}/#organization"}] + [
            {"@type": "Thing", "name": t, "sameAs": seo_meta.TOPIC[t]} for t in topics]
    if page.get("seo_reviewer"):
        webpage["reviewedBy"] = person_node(page["seo_reviewer"], full=False)
        webpage["lastReviewed"] = page.get("modified", SITE["modified"])
    if page.get("speakable"):
        webpage["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": page.get("speakable_selector", [".answer p"])}
    graph = [org_node()]
    website = {
        "@type": "WebSite",
        "@id": f"{DOMAIN}/#website",
        "url": f"{DOMAIN}/",
        "name": SITE["brand"],
        "inLanguage": "de-DE",
        "publisher": {"@id": f"{DOMAIN}/#organization"},
    }
    graph.append(website)
    if page["path"] != "/":
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append(breadcrumb_node(page))
    graph.append(webpage)
    if page["path"] == "/":
        graph.append({
            "@type": "HowTo", "@id": url + "#vorgehen", "name": "So läuft die Zusammenarbeit mit THE GAP Lab ab",
            "description": "Vier Schritte vom kostenlosen Erstgespräch bis zur Auswertung einer Maßnahme der Personalentwicklung.",
            "inLanguage": "de-DE",
            "step": [
                {"@type": "HowToStep", "position": 1, "name": "Erstgespräch", "text": "Anlass, Ziel und Zielgruppe klären (20 bis 30 Minuten, kostenlos). Ergebnis: klarer Auftrag.", "url": url + "#vorgehen-title"},
                {"@type": "HowToStep", "position": 2, "name": "Konzept", "text": "Ziele, Inhalte, Format und Erfolgskriterien festlegen. Ergebnis: abgestimmtes Konzept.", "url": url + "#vorgehen-title"},
                {"@type": "HowToStep", "position": 3, "name": "Umsetzung", "text": "Entwicklung und Durchführung entlang der Fokusfelder. Ergebnis: durchgeführte Maßnahme.", "url": url + "#vorgehen-title"},
                {"@type": "HowToStep", "position": 4, "name": "Auswertung", "text": "Wirkung prüfen und nächste Schritte klären. Ergebnis: Wirkung und nächste Schritte.", "url": url + "#vorgehen-title"},
            ],
        })
        graph.append({
            "@type": "ItemList", "@id": url + "#stufen", "name": "Die vier Leistungsstufen von THE GAP Lab",
            "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "url": f"{DOMAIN}/leistungen#{a}"}
                                for i, (n, a) in enumerate([("Konzeption", "konzeption"), ("Entwicklung", "entwicklung"), ("Durchführung", "durchfuehrung"), ("Vermarktung", "vermarktung")], 1)],
        })
    for extra in page.get("schema_nodes", []):
        if extra.get("@type") == "Service":
            extra.setdefault("areaServed", {"@type": "Country", "name": "Deutschland"})
        graph.append(extra)
    if page.get("faqs") and page.get("faq_schema", True):
        graph.append(faq_node(url, page["faqs"]))
    return {"@context": "https://schema.org", "@graph": graph}


def header_html(page):
    items = []
    for label, path, is_cta in NAV:
        cur = ' aria-current="page"' if (path == page["path"] or (path != "/" and page["path"].startswith(path + "/"))) else ""
        cls = ' class="btn"' if is_cta else ""
        items.append(f'<li><a{cls} href="{esc(path)}"{cur}>{esc(label)}</a></li>')
    return (
        '<header class="site-header" data-open="false"><div class="container header-inner">'
        f'<a class="brand" href="/" aria-label="THE GAP Lab — Startseite">THE GAP <span>Lab</span><em class="brand-tagline">Personalentwicklung</em></a>'
        '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menü</button>'
        f'<nav class="site-nav" id="site-nav" aria-label="Hauptnavigation"><ul>{"".join(items)}</ul></nav>'
        "</div></header>"
    )


def footer_html(page=None):
    cols = []
    for title, links in FOOTER_LINKS:
        lis = "".join(f'<li><a href="{esc(h)}">{esc(t)}</a></li>' for t, h in links)
        cols.append(f'<div><h2>{esc(title)}</h2><ul>{lis}</ul></div>')
    return (
        '<footer class="site-footer"><div class="container">'
        '<div class="footer-grid">'
        '<div><a class="brand" href="/">THE GAP <span>Lab</span></a>'
        f'<p>{esc(SITE["legal_name"])}<br>{esc(SITE["street"])}<br>{esc(SITE["zip"])} {esc(SITE["city"])}</p>'
        '<p class="footer-mission">THE GAP Lab entwickelt und führt Maßnahmen der Personalentwicklung durch, damit Strategie im Arbeitsalltag ankommt.</p>'
        '<p>Tochtergesellschaft der Schubart &amp; Dulgeridis GmbH</p></div>'
        + "".join(cols)
        + "</div>"
        f'<div class="footer-bottom"><span>© 2026 {esc(SITE["legal_name"])}</span>'
        f'<span>Sitz: {esc(SITE["city"])}' + (f' · Stand: {de_date(page.get("modified", SITE["modified"]))}' if page else "") + '</span></div>'
        "</div></footer>"
    )


def stopify(page, html_body):
    """S&D-Regel: Überschriften sind Aussagesätze mit Punkt (keine Fragen, keine Doppelpunkte am Ende)."""
    if page["path"] in ("/impressum", "/datenschutz", "/404", "/ki-readiness"):
        return html_body
    def fix(m):
        open_t, inner, close_t = m.group(1), m.group(2), m.group(3)
        if 'card-title' in open_t:
            return m.group(0)
        text = re.sub(r"<[^>]+>", "", inner).rstrip()
        if not text or text[-1] in ".!?:;·»)" or text.endswith("&amp;") :
            return m.group(0)
        return f"{open_t}{inner.rstrip()}.{close_t}"
    html_body = re.sub(r"(<h1[^>]*>)(.*?)(</h1>)", fix, html_body, flags=re.S)
    html_body = re.sub(r"(<h2(?![^>]*card-title)[^>]*>)(.*?)(</h2>)", fix, html_body, flags=re.S)
    html_body = re.sub(r'(<h3 class="(?:v-h3|il-h3)">)(.*?)(</h3>)', fix, html_body, flags=re.S)
    return html_body


def nbsp_brand(html_body):
    """Markenname darf nicht mitten im Namen umbrechen (nur in Textknoten, nie in Attributen, Skripten oder Stilen)."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", html_body, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace("THE GAP Lab", "THE\u00a0GAP\u00a0Lab").replace("THE GAP", "THE\u00a0GAP")
    return "".join(parts)


def with_journey(page):
    body = page["body"]
    if page.get("journey"):
        import visuals
        marker = '<section class="cta-band"'
        if marker in body:
            body = body.replace(marker, visuals.journey(page["journey"]) + marker, 1)
    return body


def render(page):
    url = url_of(page["path"])
    title = page["title"]
    desc = page["description"]
    robots = page.get("robots", "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")
    og_img = DOMAIN + page.get("og_image", "/assets/img/og-the-gap-lab.jpg")
    og_h = page.get("og_image_height", 630)
    og_alt = esc(page.get("og_alt", "THE GAP Lab — Personalentwicklung mit Verhandlungsstärke, Führungsklarheit und Finanzverständnis"))
    extra_css = "".join(f'<link rel="stylesheet" href="{versioned(c)}">\n' for c in page.get("styles", []))
    graph = json.dumps(graph_for(page), ensure_ascii=False, separators=(",", ":"))
    head = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="author" content="{esc(SITE["legal_name"])}">
<meta name="geo.region" content="DE-BY">
<meta name="geo.placename" content="{esc(SITE["city"])}">
<link rel="alternate" hreflang="de" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="THE GAP Lab">
<meta property="og:title" content="{esc(page.get("og_title", title))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="{og_h}">
<meta property="og:image:alt" content="{og_alt}">
<meta property="og:locale" content="de_DE">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page.get("og_title", title))}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#101D33">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/source-sans-3-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
{extra_css}<link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">
<script src="/assets/site.js?v={JS_V}" defer></script>
<script type="application/ld+json">{graph}</script>
</head>
"""
    stand = ""
    if page.get("show_stand", True) and page["path"] not in ("/",):
        stand = f'<p class="stand container">Stand: {SITE["modified_de"]}</p>'
    body = (
        "<body>"
        '<a class="skip-link" href="#main">Zum Inhalt springen</a>'
        '<div class="rule-top" aria-hidden="true"></div>'
        + header_html(page)
        + '<main id="main">'
        + nbsp_brand(stopify(page, with_journey(page)))
        + "</main>"
        + footer_html(page)
        + "".join(f'<script src="{versioned(j)}" defer></script>' for j in page.get("scripts", []))
        + "</body></html>\n"
    )
    return head + body


def de_date(iso):
    y, m, d = iso.split("-")
    months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    return f"{int(d)}. {months[int(m) - 1]} {y}"


def assign_lastmod(pages):
    """Änderungsdatum je Seite aus dem Inhalt: bleibt stehen, solange sich Titel, Beschreibung, Text und FAQ nicht ändern."""
    store_path = os.path.join(ROOT, "tools", "lastmod.json")
    try:
        with open(store_path, encoding="utf-8") as fh:
            store = json.load(fh)
    except (OSError, ValueError):
        store = {}
    today = datetime.date.today().isoformat()
    for p in pages:
        blob = json.dumps([p["title"], p["description"], p["body"], p.get("faqs", []), p.get("seo_keywords", "")], ensure_ascii=False)
        h = hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]
        old = store.get(p["path"])
        if old and old["hash"] == h:
            date = old["date"]
        else:
            date = today if old else p.get("modified", today)
            if old:
                date = today
        store[p["path"]] = {"hash": h, "date": date}
        p["modified"] = date
    with open(store_path, "w", encoding="utf-8") as fh:
        json.dump(store, fh, ensure_ascii=False, indent=1, sort_keys=True)
    return pages


def all_pages():
    pages = []
    pages += pages_core.build()
    pages += pages_fokus.build()
    pages += pages_ki.build()
    pages += pages_innolab.build()
    pages += pages_glossar.build()
    pages += pages_legal.build()
    seo_meta.apply(pages)
    return assign_lastmod(pages)


def write(rel, content):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def sitemap(pages):
    rows = []
    for p in pages:
        if not p.get("sitemap", True):
            continue
        rows.append(
            "  <url>\n"
            f"    <loc>{url_of(p['path'])}</loc>\n"
            f"    <lastmod>{p.get('modified', SITE['modified'])}</lastmod>\n"
            f"    <changefreq>{p.get('changefreq', 'monthly')}</changefreq>\n"
            f"    <priority>{p.get('priority', '0.6')}</priority>\n"
            "  </url>"
        )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")


def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot",
            "Google-Extended", "Applebot-Extended", "CCBot"]
    out = ["User-agent: *", "Allow: /", ""]
    out.append("# KI-Such- und Antwortsysteme sind ausdrücklich zugelassen, damit Unternehmen und Leistungen")
    out.append("# korrekt zitiert werden können.")
    for b in bots:
        out += [f"User-agent: {b}", "Allow: /", ""]
    out.append(f"Sitemap: {DOMAIN}/sitemap.xml")
    return "\n".join(out) + "\n"


def llms(pages):
    lines = [f"# {SITE['brand']} ({SITE['legal_name']})", ""]
    lines.append(f"> {SITE['llms_summary']}")
    lines.append("")
    lines.append(f"Firmendaten: {SITE['legal_name']}, {SITE['street']}, {SITE['zip']} {SITE['city']}; "
                 f"{SITE['hrb']}, {SITE['court']}; Geschäftsführer: Prof. Dr. Constantin Schubart (einzelvertretungsberechtigt). "
                 f"Muttergesellschaft: Schubart & Dulgeridis GmbH (https://www.schubart-dulgeridis.de/).")
    lines.append("Kurzfassung: THE GAP Lab entwickelt und führt Maßnahmen der Personalentwicklung durch (Konzeption, Entwicklung, Durchführung, Vermarktung) in drei Fokusfeldern: Verhandlungsführung & Rhetorik, Leadership & Organisation, Finance & Transformation. Zielgruppe: Geschäftsleitungen, Personalverantwortliche, Führungskräfte. Konkrete Angebote: fünf InnoLab-Formate (Innovation, Change, Lernen) und der kostenlose KI-Readiness Check. Einstieg: kostenloses Erstgespräch (20 bis 30 Minuten).")
    lines.append("")
    lines.append(f"Vollständiger Inhalt aller Seiten als Text: {DOMAIN}/llms-full.txt")
    lines.append("")
    lines += [
        "## Fakten",
        f"- Name: {SITE['brand']} (Firma: {SITE['legal_name']}); Sitz: {SITE['street']}, {SITE['zip']} {SITE['city']}",
        "- Branche: Personalentwicklung, Weiterbildung, Beratung; Zielgruppe: Geschäftsleitungen, Personalverantwortliche, Führungskräfte, Bildungsträger",
        "- Leistungen: Konzeption, Entwicklung, Durchführung, Vermarktung von Maßnahmen der Personalentwicklung",
        "- Fokusfelder: Verhandlungsführung & Rhetorik (Dr. Oliver Meschkat), Leadership & Organisation (Prof. Dr. Constantin Schubart), Finance & Transformation (Prof. Dr. Marcel Dulgeridis)",
        "- Angebote: fünf InnoLab-Formate vor Ort (Preise ausschließlich auf der InnoLab-Seite), kostenloser KI-Readiness Check, kostenloses Erstgespräch (20 bis 30 Minuten, Microsoft Teams)",
        f"- Kontakt: {SITE['email']}, {SITE['phone']}; Termin: {DOMAIN}/kontakt",
        f"- Verbund: Tochtergesellschaft der {SITE['parent_name']} (Diagnostik und Beratung: THE GAP, Pulse-Check)",
        f"- Stand der Inhalte: {max(p.get('modified', SITE['modified']) for p in pages)}",
        "",
        "## Zitierhinweis",
        f"- Bitte als „{SITE['brand']} ({SITE['legal_name']})“ nennen und auf die jeweilige Seite unter {DOMAIN} verlinken.",
        "- Preise, Konditionen und Teilnehmerzahlen nur von /innolab übernehmen; Fachbegriffe (BATNA, ZOPA, Cashflow, KI-Gap u. a.) sind im Glossar definiert.",
        "",
    ]
    groups = {}
    for p in pages:
        if p.get("llms_group"):
            groups.setdefault(p["llms_group"], []).append(p)
    for g, items in groups.items():
        lines.append(f"## {g}")
        for p in items:
            lines.append(f"- [{p['short']}]({url_of(p['path'])}): {p['description']}")
        lines.append("")
    import pages_faq
    keep = ["Was macht THE GAP Lab?", "Wie unterscheiden sich THE GAP Lab und die Schubart &amp; Dulgeridis GmbH?", "Was ist InnoLab?",
            "Welche fünf Formate gibt es?", "Was bedeuten BATNA und ZOPA?", "Was ist der KI-Readiness Check?", "Wie kommt eine Zusammenarbeit zustande?"]
    lines.append("## Kurzantworten")
    for _c, q, a in pages_faq.ALL:
        if q in keep:
            text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"</?(?:a|strong|em|b|span)\b[^>]*>", "", a)))).strip()
            lines.append(f"- {html.unescape(q)} {text}")
    lines.append(f"- Weitere Antworten: {DOMAIN}/faq")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def llms_full(pages):
    from helpers import strip_tags
    out = [f"# {SITE['brand']} ({SITE['legal_name']}): vollständiger Inhalt als Text", "",
           f"> {SITE['llms_summary']}", "", f"Stand: {max(p.get('modified', SITE['modified']) for p in pages)}. Quelle: {DOMAIN}", ""]
    for p in pages:
        if not p.get("sitemap", True) or p["path"] in ("/ki-readiness",):
            continue
        out += [f"## {p['title']}", f"URL: {url_of(p['path'])}", ""]
        body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", p["body"], flags=re.S)
        body = re.sub(r"</(p|li|h[1-6]|div|section|dt|dd|tr|article|summary|span|strong|small|b|em|a)>\s*(?=<(?:p|li|h[1-6]|div|section|dt|dd|tr|article|details|summary|span|strong|small|b|em|a)\b)", " ", body)
        body = re.sub(r"</(p|li|h[1-6]|div|section|dt|dd|tr|article|summary|details|ul|ol|dl)>", "¶", body)
        text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)))
        out += [t.strip() for t in text.split("¶") if t.strip()]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    pages = all_pages()
    seen_paths = set()
    for p in pages:
        assert p["path"] not in seen_paths, p["path"]
        seen_paths.add(p["path"])
        write(out_file(p["path"]), render(p))
    write("sitemap.xml", sitemap(pages))
    write("robots.txt", robots())
    write("llms.txt", llms(pages))
    write("llms-full.txt", llms_full(pages))
    print(f"{len(pages)} Seiten erzeugt (css v={CSS_V}, js v={JS_V}).")


if __name__ == "__main__":
    main()
