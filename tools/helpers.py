"""Wiederverwendbare HTML-Bausteine für die Seitenmodule."""
import html
import re

from siteinfo import SITE, PARTNERS

DOMAIN = SITE["domain"]


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def url_of(path):
    return DOMAIN + ("/" if path == "/" else path)


# --------------------------------------------------------------- Bausteine
ARROW = ('<svg class="icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def btn(href, text, cls=""):
    klass = ("btn " + cls).strip()
    return f'<a class="{klass}" href="{esc(href)}">{text}</a>'


def link_arrow(href, text):
    return f'<a class="link-arrow" href="{esc(href)}">{text} {ARROW}</a>'


def faq_more():
    return '<p class="small">Weitere Antworten: <a href="/faq">FAQ</a>.</p>'


def faq_block(items):
    rows = []
    for q, a in items:
        rows.append(
            f'<details><summary>{esc(q)}</summary><div class="answer-body">{a}</div></details>'
        )
    return '<div class="faq">' + "".join(rows) + "</div>"


def breadcrumb_html(page):
    if page["path"] == "/":
        return ""
    items = [("Start", "/")] + list(page.get("crumbs", []))
    lis = "".join(f'<li><a href="{esc(p)}">{esc(n)}</a></li>' for n, p in items)
    lis += f'<li aria-current="page">{esc(page["short"])}</li>'
    return f'<nav class="breadcrumb" aria-label="Brotkrumen"><ol>{lis}</ol></nav>'


def partner_card(key, with_fokus=True):
    p = PARTNERS[key]
    links = [f'<a href="{esc(p["fokus_path"])}">Fokusfeld ansehen</a>']
    return (
        '<article class="partner">'
        f'<div class="photo"><img src="{esc(p["img"])}" alt="{esc(p["name"])}" width="448" height="448" loading="lazy" decoding="async"></div>'
        '<div class="body">'
        f'<span class="role">{esc(p["role"])}</span>'
        f'<h3>{esc(p["name"])}</h3>'
        f'<p class="focus">{esc(p["focus"])}</p>'
        f'<div class="links">{"".join(links)}</div>'
        "</div></article>"
    )


def cta_band(title, text, primary_text="Erstgespräch vereinbaren", primary_href="/kontakt", secondary=None):
    sec = ""
    if secondary:
        sec = f'<p>{secondary}</p>'
    return (
        '<section class="cta-band" aria-labelledby="cta-title"><div class="container"><div class="cta-inner">'
        f'<div><h2 id="cta-title">{title}</h2><p>{text}</p>{sec}</div>'
        f'<a class="btn btn-gold" href="{esc(primary_href)}">{primary_text} {ARROW}</a>'
        "</div></div></section>"
    )




def page_hero(page, h1, lead=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return (
        '<section class="page-hero"><div class="container">'
        + breadcrumb_html(page)
        + f"<h1>{h1}</h1>{lead_html}"
        + "</div></section>"
    )


def section(inner, cls="", label_id=None, container=True):
    lab = f' aria-labelledby="{label_id}"' if label_id else ""
    c = f'<div class="container">{inner}</div>' if container else inner
    return f'<section class="section {cls}"{lab}>{c}</section>'


def head(eyebrow, title, intro="", title_id=None):
    tid = f' id="{title_id}"' if title_id else ""
    intro_html = f"<p>{intro}</p>" if intro else ""
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f'<div class="section-head">{eb}<h2{tid}>{title}</h2>{intro_html}</div>'


def answer_box(label, text):
    return f'<div class="answer"><span class="label">{label}</span><p>{text}</p></div>'


def partner_wide(key):
    p = PARTNERS[key]
    return f"""<article class="partner-wide" id="{key}">
  <div class="photo"><img src="{esc(p['img'])}" alt="{esc(p['name'])}" width="448" height="448" loading="lazy" decoding="async"></div>
  <div>
    <span class="role">{esc(p['role'])} · {esc(p['focus'])}</span>
    <h3>{esc(p['name'])}</h3>
    <p>{esc(p['long_bio'])}</p>
    <div class="hero-actions">
      <a class="link-arrow" href="{esc(p['sd_url'])}">Profil bei Schubart &amp; Dulgeridis</a>
      <a class="link-arrow" href="{esc(p['linkedin'])}" rel="noopener noreferrer">LinkedIn</a>
    </div>
  </div>
</article>"""
