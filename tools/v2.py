"""Redesign-Schicht (v2): Icon-Sprite, Markup-Anreicherung, neuer Start-Hero, Vorschau-Links.

Alles ohne Inline-Styles und ohne Inline-Skripte (strikte CSP).
Wird nur von `python3 tools/build.py --preview` bzw. `--live-v2` verwendet.
"""
import re

ICONS = {
 'gap': '<path d="M4 5v14M20 5v14"/><path d="M9.5 12h5" stroke-dasharray="1.2 2.4"/><path d="M8.5 12l2-2M8.5 12l2 2M15.5 12l-2-2M15.5 12l-2 2"/>',
 'compass': '<circle class="a" cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="9"/><path d="M15.6 8.4l-2 5.2-5.2 2 2-5.2z"/>',
 'nav': '<path class="a" d="M12 3l7 17-7-4-7 4z"/><path d="M12 3l7 17-7-4-7 4z"/>',
 'target': '<circle class="a" cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
 'coins': '<ellipse class="a" cx="12" cy="6.5" rx="7" ry="3"/><ellipse cx="12" cy="6.5" rx="7" ry="3"/><path d="M5 6.5v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5M5 11.5v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5"/>',
 'layers': '<path class="a" d="M12 3l9 5-9 5-9-5z"/><path d="M12 3l9 5-9 5-9-5z"/><path d="M3 12.5l9 5 9-5M3 16.5l9 5 9-5"/>',
 'users': '<circle class="a" cx="9" cy="8" r="3.2"/><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17.5 14.2c2.4.3 4.5 2.3 4.5 5.3"/>',
 'pencil': '<path class="a" d="M4 20l1-4.5L16.5 4a2 2 0 0 1 3 3L8 18.5z"/><path d="M4 20l1-4.5L16.5 4a2 2 0 0 1 3 3L8 18.5zM14 6.5l3.5 3.5"/>',
 'megaphone': '<path class="a" d="M4 10v4a1 1 0 0 0 1 1h3l8 4V5L8 9H5a1 1 0 0 0-1 1z"/><path d="M4 10v4a1 1 0 0 0 1 1h3l8 4V5L8 9H5a1 1 0 0 0-1 1zM19 9.5a4 4 0 0 1 0 5M8 15l1 5h3"/>',
 'bulb': '<path class="a" d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2V17h5v-1.1c0-.8.4-1.5 1-2A6 6 0 0 0 12 3z"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2V17h5v-1.1c0-.8.4-1.5 1-2A6 6 0 0 0 12 3zM9.5 20.5h5"/>',
 'cpu': '<rect class="a" x="6" y="6" width="12" height="12" rx="2.5"/><rect x="6" y="6" width="12" height="12" rx="2.5"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
 'clock': '<circle class="a" cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'arrow': '<path d="M4.5 12h15M13.5 6l6 6-6 6"/>',
 'spark': '<path class="a" d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/><path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/>',
 'mail': '<rect class="a" x="3" y="5.5" width="18" height="13" rx="2.5"/><rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3.5 7.5l8.5 6 8.5-6"/>',
 'phone': '<path class="a" d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2z"/><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
 'book': '<path class="a" d="M4 5.5C4 4.7 4.7 4 5.5 4H12v16H5.5A1.5 1.5 0 0 1 4 18.5z"/><path d="M12 4H18.5c.8 0 1.5.7 1.5 1.5v13c0 .8-.7 1.5-1.5 1.5H12M12 4v16M4 18.5V5.5C4 4.7 4.7 4 5.5 4H12"/>',
 'scale': '<path d="M12 4v16M7.5 20h9M5 8h14"/><path class="a" d="M5 8l-3 6.5h6z"/><path d="M5 8l-3 6.5h6zM19 8l-3 6.5h6z"/><path class="a" d="M19 8l-3 6.5h6z"/>',
 'building': '<path class="a" d="M5 21V5.5A1.5 1.5 0 0 1 6.5 4h7A1.5 1.5 0 0 1 15 5.5V21z"/><path d="M5 21V5.5A1.5 1.5 0 0 1 6.5 4h7A1.5 1.5 0 0 1 15 5.5V21M15 10h3.5a1.5 1.5 0 0 1 1.5 1.5V21M3 21h18M8.5 8h3M8.5 12h3M8.5 16h3"/>',
 'pin': '<path class="a" d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'calendar': '<rect class="a" x="3.5" y="5" width="17" height="15.5" rx="3"/><rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4M8 14h2M14 14h2"/>',
 'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
 'chat': '<path class="a" d="M4 5.5h16v11H9.5L5 20.5v-4H4z"/><path d="M4 5.5h16v11H9.5L5 20.5v-4H4z"/><path d="M8 10h8M8 13h5"/>',
 'trend': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 'up': '<path d="M12 19.5v-15M6 10.5l6-6 6 6"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def sprite():
    out = ['<svg width="0" height="0" class="sprite" aria-hidden="true" focusable="false"><defs>']
    for k, v in ICONS.items():
        out.append(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>')
    out.append('</defs></svg>')
    return ''.join(out)


def ic(name, cls=''):
    c = f' {cls}' if cls else ''
    return f'<svg class="ico{c}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


# ----------------------------------------------------------------- Start-Hero
def hero_home(arrow):
    lines = ["Beschlossenes kommt im Alltag an.", "Einzeln buchbar oder als Kette.",
             "Erstgespräch kostenlos, 20 bis 30 Minuten.", "Konzeption, Entwicklung, Durchführung, Vermarktung."]
    planks = "".join("<i></i>" for _ in range(7))
    return f"""
<section class="hero hero-home hero-v2"><div class="container hv-wrap">
  <div class="hv-copy">
    <p class="eyebrow">Personalentwicklung · Altdorf bei Nürnberg</p>
    <h1>Personal&shy;entwicklung, die <span class="accent">verbindet.</span></h1>
    <p class="lead">THE GAP Lab verbindet Strategie, Führungsklarheit und Finanzverständnis in Maßnahmen, die im Arbeitsalltag ankommen.</p>
    <div class="hero-actions">
      <a class="btn" href="/kontakt">Erstgespräch vereinbaren {arrow}</a>
      <a class="link-arrow" href="/leistungen">Leistungen ansehen {arrow}</a>
    </div>
    <p class="ticker"><span class="tk-dot">{ic('spark')}</span><span class="tk-t" data-lines="{'|'.join(lines)}">{lines[0]}</span></p>
  </div>
  <div class="hv-stage">
    <a class="hv-chip hv-c1" href="/ki-readiness">{ic('cpu')}<span>KI-Readiness Check<small>kostenlos</small></span></a>
    <a class="hv-chip hv-c2" href="/innolab">{ic('bulb')}<span>InnoLab<small>fünf Formate vor Ort</small></span></a>
    <figure class="hv-card" aria-labelledby="hv-cap">
      <div class="hv-top"><span class="hv-brand">{ic('gap')}THE GAP</span><span class="hv-badge">Schema</span></div>
      <div class="hv-scene" role="img" aria-label="Zwei Blöcke, Beschlossen und Im Alltag, verbunden durch eine Brücke, die sich schließen lässt.">
        <div class="hv-block hv-l"><b>Beschlossen</b><span>Strategie · Konzept</span></div>
        <div class="hv-bridge" data-planks="7">{planks}</div>
        <div class="hv-block hv-r"><b>Im Alltag</b><span>Verhalten · Ergebnis</span></div>
      </div>
      <div class="hv-ctl"><label for="hv-range">Maßnahme</label><input id="hv-range" class="hv-range" type="range" min="0" max="100" value="12"></div>
      <p class="hv-read" id="hv-cap"><span class="hv-state" data-s0="Die Lücke ist offen." data-s1="Die Brücke entsteht." data-s2="Beschlossenes kommt im Alltag an.">Die Lücke ist offen.</span></p>
    </figure>
  </div>
</div></section>
"""


# ------------------------------------------------------- Anreicherung des HTML
BREAK_ICON = {'/leistungen#konzeption': 'compass', '/fokusfelder/leadership-organisation': 'nav',
              '/fokusfelder/strategie-vertrieb-innovation': 'target', '/fokusfelder/finance-transformation': 'coins'}
STAGE_ICON = {'konzeption': 'pencil', 'entwicklung': 'layers', 'durchfuehrung': 'users', 'vermarktung': 'megaphone'}


def enhance(html, page, preview_prefix=None):
    # Icons in die Problem-Karten
    def brk(m):
        block = m.group(0)
        href = re.search(r'<h3><a href="([^"]+)"', block)
        icon = BREAK_ICON.get(href.group(1)) if href else None
        return block.replace('<span class="v-bigno"', f'<span class="v-ic">{ic(icon)}</span><span class="v-bigno"', 1) if icon else block
    html = re.sub(r'<li class="v-break[^>]*>.*?</li>', brk, html, flags=re.S)

    if page["path"] == "/":
        html = re.sub(r'<section class="hero hero-home">.*?</section>\n?', lambda m: hero_home(
            '<svg class="icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'), html, count=1, flags=re.S)

    html = add_hero_visual(html, page["path"])
    if preview_prefix:
        html = rewrite_links(html, preview_prefix)
    return html


KEEP = ("/assets/", "/favicon", "/site.webmanifest", "/llms")


def rewrite_links(html, prefix):
    """Vorschau: interne Seitenlinks zeigen auf /preview/..., damit der Klon vollständig durchklickbar ist."""
    def fix(m):
        url = m.group(2)
        if url.startswith("//") or url.startswith(KEEP):
            return m.group(0)
        if url == "/":
            return f'{m.group(1)}{prefix}/"'
        return f'{m.group(1)}{prefix}{url}"'
    return re.sub(r'(\shref=")(/[^"]*)"', fix, html)


# ----------------------------------------------------------- Kopf und Leisten
def _anchors(body):
    out = []
    for m in re.finditer(r'<p class="x?-?eyebrow">([^<]*)</p>\s*<h2 id="([^"]+)"', body):
        lab = re.sub(r"<[^>]+>", "", m.group(1))
        lab = re.sub(r"^\s*\d+\s*·\s*", "", lab).split("·")[0].strip()
        if lab and m.group(2) and all(lab != a for a, _ in out):
            out.append((lab, m.group(2)))
    return out[:6]


def header(page, nav, body, esc):
    items = []
    for label, path, is_cta in nav:
        cur = ' aria-current="page"' if (path == page["path"] or (path != "/" and page["path"].startswith(path + "/"))) else ""
        cls = ' class="btn"' if is_cta else ""
        items.append(f'<li><a{cls} href="{esc(path)}"{cur}>{esc(label)}</a></li>')
    anchors = _anchors(body)
    sub = ""
    if len(anchors) >= 2:
        title = "THE GAP Lab" if page["path"] == "/" else esc(page["short"])
        links = "".join(f'<a href="#{a}">{lab}</a>' for lab, a in anchors)
        sub = (f'<div class="snav"><div class="container snav-in"><span class="snav-t">{ic("gap")}{title}</span>'
               f'<nav class="snav-links" aria-label="Auf dieser Seite">{links}</nav>'
               f'<a class="btn snav-cta" href="/kontakt">Erstgespräch</a></div></div>')
    return (
        '<header class="site-header v2-header" data-open="false"><div class="gnav"><div class="container header-inner">'
        '<a class="brand" href="/" aria-label="THE GAP Lab — Startseite">THE GAP <span>Lab</span></a>'
        '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menü</button>'
        f'<nav class="site-nav" id="site-nav" aria-label="Hauptnavigation"><ul>{"".join(items)}</ul></nav>'
        f'</div></div>{sub}</header>'
    )


def sticky_bar():
    return (f'<div class="x-fbar" aria-hidden="true"><span class="x-fbar-t">{ic("calendar")}<b>Erstgespräch</b><span>kostenlos, 20 bis 30 Minuten</span></span>'
            '<a class="btn" href="/kontakt" tabindex="-1">Termin wählen</a>'
            f'<button class="x-top" type="button" tabindex="-1" aria-label="Zum Seitenanfang">{ic("up")}</button></div>')


# ----------------------------------------------------------- Seiten-Hero-Visuals
def _portrait(key, cls=""):
    from siteinfo import PARTNERS
    p = PARTNERS[key]
    return f'<img class="{cls}" src="{p["img_sm"]}" alt="" width="72" height="72" loading="eager" decoding="async">'


def hero_visual(path):
    from siteinfo import PARTNERS
    if path == "/leistungen":
        st = [("pencil", "Konzeption"), ("layers", "Entwicklung"), ("users", "Durchführung"), ("megaphone", "Vermarktung")]
        lis = "".join(f'<li><span class="x-v-no">0{k+1}</span>{ic(i)}<b>{n}</b></li>' for k, (i, n) in enumerate(st))
        return f'<div class="x-phv x-phv-chain" aria-hidden="true"><ol>{lis}</ol><p>Einzeln buchbar oder als Kette.</p></div>'
    if path == "/fokusfelder":
        return ('<div class="x-phv x-phv-venn" aria-hidden="true"><svg viewBox="0 0 300 280"><circle class="f1" cx="105" cy="105" r="82"/><circle class="f2" cx="195" cy="105" r="82"/>'
                '<circle class="f3" cx="150" cy="182" r="82"/><text x="80" y="92">Gestalten</text><text x="222" y="92">Führen</text><text x="150" y="232">Wirtschaften</text>'
                '<text class="c" x="150" y="138">Entscheidung</text><text class="c" x="150" y="154">im Alltag</text></svg></div>')
    fok = {"/fokusfelder/strategie-vertrieb-innovation": ("oliver-meschkat", "f1", "target", "Gestalten"),
           "/fokusfelder/leadership-organisation": ("constantin-schubart", "f2", "nav", "Führen"),
           "/fokusfelder/finance-transformation": ("marcel-dulgeridis", "f3", "coins", "Wirtschaften")}
    if path in fok:
        k, c, i, verb = fok[path]
        p = PARTNERS[k]
        return (f'<div class="x-phv x-phv-fokus {c}" aria-hidden="true"><div class="x-pf-ring"><img src="{p["img"]}" alt="" width="220" height="220" decoding="async"></div>'
                f'<span class="x-pf-verb">{ic(i)}{verb}</span><span class="x-pf-name"><b>{p["name"]}</b>{p["role"]} · {p["focus"].replace("&", "&amp;")}</span></div>')
    if path == "/ueber-uns":
        av = "".join(_portrait(k) for k in ("oliver-meschkat", "constantin-schubart", "marcel-dulgeridis"))
        return (f'<div class="x-phv x-phv-org" aria-hidden="true"><span class="x-o x-o1">Schubart &amp; Dulgeridis GmbH<small>Muttergesellschaft</small></span>'
                f'<i class="x-o-line"></i><span class="x-o x-o2">The Gap Lab GmbH<small>Altdorf bei Nürnberg</small></span><i class="x-o-line"></i><span class="x-o-av">{av}</span></div>')
    if path == "/kontakt":
        av = "".join(_portrait(k) for k in ("constantin-schubart", "oliver-meschkat", "marcel-dulgeridis"))
        return (f'<div class="x-phv x-phv-contact" aria-hidden="true"><span class="x-o-av">{av}</span>'
                f'<ul><li>{ic("clock")}20 bis 30 Minuten</li><li>{ic("chat")}Microsoft Teams</li><li>{ic("check")}Kostenlos und unverbindlich</li></ul></div>')
    if path == "/faq":
        import pages_faq
        n = len(pages_faq.ALL)
        qs = [q for _c, q, _a in pages_faq.ALL][:3]
        cards = "".join(f'<span class="x-qc x-qc{k}"><i>?</i>{q}</span>' for k, q in enumerate(qs))
        return f'<div class="x-phv x-phv-faq" aria-hidden="true">{cards}<span class="x-big">{n}<small>Antworten</small></span></div>'
    if path == "/glossar":
        import pages_glossar
        t = pages_glossar.terms()
        letters = sorted({x[0][0].upper() for x in t})
        tiles = "".join(f"<i>{l}</i>" for l in letters)
        return f'<div class="x-phv x-phv-gloss" aria-hidden="true"><span class="x-az">{tiles}</span><span class="x-big">{len(t)}<small>Begriffe</small></span></div>'
    return ""


def add_hero_visual(html, path):
    vis = hero_visual(path)
    if not vis:
        return html
    return re.sub(r'<section class="page-hero"><div class="container">(.*?)</div></section>',
                  lambda m: f'<section class="page-hero x-ph"><div class="container x-ph-grid"><div class="x-ph-copy">{m.group(1)}</div>{vis}</div></section>',
                  html, count=1, flags=re.S)
