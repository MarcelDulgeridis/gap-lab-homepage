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
import pages_legal  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOMAIN = SITE["domain"]


def asset_hash(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:8]


CSS_V = asset_hash("assets/site.css")
JS_V = asset_hash("assets/site.js")


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
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/og-the-gap-lab.jpg"},
    }
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
    for extra in page.get("schema_nodes", []):
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
        f'<a class="brand" href="/" aria-label="THE GAP Lab — Startseite">THE GAP <span>Lab</span></a>'
        '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menü</button>'
        f'<nav class="site-nav" id="site-nav" aria-label="Hauptnavigation"><ul>{"".join(items)}</ul></nav>'
        "</div></header>"
    )


def footer_html():
    cols = []
    for title, links in FOOTER_LINKS:
        lis = "".join(f'<li><a href="{esc(h)}">{esc(t)}</a></li>' for t, h in links)
        cols.append(f'<div><h2>{esc(title)}</h2><ul>{lis}</ul></div>')
    return (
        '<footer class="site-footer"><div class="container">'
        '<div class="footer-grid">'
        '<div><a class="brand" href="/">THE GAP <span>Lab</span></a>'
        f'<p>{esc(SITE["legal_name"])}<br>{esc(SITE["street"])}<br>{esc(SITE["zip"])} {esc(SITE["city"])}</p>'
        '<p>Tochtergesellschaft der Schubart &amp; Dulgeridis GmbH</p></div>'
        + "".join(cols)
        + "</div>"
        f'<div class="footer-bottom"><span>© 2026 {esc(SITE["legal_name"])}</span>'
        f'<span>Sitz: {esc(SITE["city"])}</span></div>'
        "</div></footer>"
    )


def render(page):
    url = url_of(page["path"])
    title = page["title"]
    desc = page["description"]
    robots = page.get("robots", "index,follow,max-image-preview:large")
    og_img = f"{DOMAIN}/assets/img/og-the-gap-lab.jpg"
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
<link rel="alternate" hreflang="de" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="THE GAP Lab">
<meta property="og:title" content="{esc(page.get("og_title", title))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="THE GAP Lab — Personalentwicklung mit Verhandlungsstärke, Führungsklarheit und Finanzverständnis">
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
<script src="/assets/site.js?v={JS_V}"></script>
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
        + page["body"]
        + "</main>"
        + footer_html()
        + "</body></html>\n"
    )
    return head + body


def all_pages():
    pages = []
    pages += pages_core.build()
    pages += pages_fokus.build()
    pages += pages_legal.build()
    return pages


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
    lines.append("")
    groups = {}
    for p in pages:
        if p.get("llms_group"):
            groups.setdefault(p["llms_group"], []).append(p)
    for g, items in groups.items():
        lines.append(f"## {g}")
        for p in items:
            lines.append(f"- [{p['short']}]({url_of(p['path'])}): {p['description']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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
    print(f"{len(pages)} Seiten erzeugt (css v={CSS_V}, js v={JS_V}).")


if __name__ == "__main__":
    main()
