"""Englische Fassung: erzeugt aus jeder fertigen deutschen Seite die englische Seite.

Prinzip: Die deutschen Seiten bleiben die Quelle. Übersetzt wird über einen Katalog (tools/i18n/en.json),
Schlüssel ist der deutsche Text eines Textblocks. Inline-Markup (Links, Hervorhebungen, Icons) steht im
Schlüssel als Platzhalter <g0>…</g0> bzw. <x0/>, damit Übersetzungen unabhängig von Link-Zielen und Icons sind.

    python3 tools/build.py              erzeugt auch /en/... und meldet fehlende Übersetzungen
    python3 tools/build.py --i18n-todo  schreibt fehlende Schlüssel nach tools/i18n/todo_en.json

Keine Abhängigkeiten außer der Standardbibliothek.
"""
import html
import json
import os
import re
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAT_PATH = os.path.join(ROOT, "tools", "i18n", "en.json")
DOMAIN = "https://www.gap-lab.de"

# Deutsche Pfade -> englische Pfade
SLUGS = {
    "/": "/en",
    "/leistungen": "/en/services",
    "/fokusfelder": "/en/focus-areas",
    "/fokusfelder/strategie-vertrieb-innovation": "/en/focus-areas/strategy-sales-innovation",
    "/fokusfelder/leadership-organisation": "/en/focus-areas/leadership-organisation",
    "/fokusfelder/finance-transformation": "/en/focus-areas/finance-transformation",
    "/innolab": "/en/innolab",
    "/ki-readiness": "/en/ai-readiness",
    "/ueber-uns": "/en/about-us",
    "/kontakt": "/en/contact",
    "/faq": "/en/faq",
    "/glossar": "/en/glossary",
    "/impressum": "/en/legal-notice",
    "/datenschutz": "/en/privacy",
}
EN_TO_DE = {v: k for k, v in SLUGS.items()}

# Skripte mit deutschen Texten: englische Kopie assets/<name>.en.js wird erzeugt
JS_I18N = ["site.js", "v2.js", "faq.js", "innolab.js", "ki-readiness.js"]

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "dt", "dd", "summary", "figcaption", "td", "th", "label",
         "button", "option", "title", "blockquote", "caption", "legend", "text", "desc", "output", "textPath"}
INLINE = {"a", "strong", "em", "b", "i", "span", "small", "br", "abbr", "sup", "sub", "code", "wbr", "mark", "q", "s", "u",
          "time", "img", "svg", "del", "ins", "cite"}
VOID = {"br", "img", "input", "meta", "link", "hr", "wbr", "source", "area", "base", "col", "embed", "param", "track"}
RAW = {"script", "style"}
ATTRS = {"alt", "title", "aria-label", "placeholder", "data-lines", "data-s0", "data-s2", "data-names", "data-label-open",
         "data-label-close", "data-step", "data-of", "data-q", "data-all-open", "data-all-close"}
META_CONTENT = {"description", "og:title", "og:description", "og:image:alt", "twitter:title", "twitter:description"}

MONTHS_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DATE_RX = re.compile(r"\b(\d{1,2})\. (" + "|".join(MONTHS_DE) + r") (\d{4})\b")


def en_path(path):
    path = path.rstrip("/") or "/"
    return SLUGS.get(path)


def de_date_to_en(m):
    return f"{int(m.group(1))} {MONTHS_EN[MONTHS_DE.index(m.group(2))]} {m.group(3)}"


def has_words(s):
    return bool(re.search(r"[A-Za-zÄÖÜäöüß]{2,}", s))


def norm(s):
    s = s.replace("­", "").replace(" ", " ")
    s = DATE_RX.sub("{date}", s)
    return re.sub(r"\s+", " ", s).strip()


def brand_nbsp(s):
    return s.replace("THE GAP Lab", "THE GAP Lab")


# ------------------------------------------------------------------ Mini-DOM
class Node:
    __slots__ = ("tag", "attrs", "children", "selfclose", "raw")

    def __init__(self, tag, attrs=None, selfclose=False, raw=None):
        self.tag, self.attrs, self.children, self.selfclose, self.raw = tag, attrs or [], [], selfclose, raw


class Text:
    __slots__ = ("raw",)

    def __init__(self, raw):
        self.raw = raw


class Raw:
    __slots__ = ("raw",)

    def __init__(self, raw):
        self.raw = raw


ATTR_NAME = re.compile(r"""\s([^\s=/>"']+)(?=\s*=|\s|/?>)""")


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node("#root")
        self.stack = [self.root]

    def handle_decl(self, d): self.stack[-1].children.append(Raw(f"<!{d}>"))
    def handle_comment(self, d): self.stack[-1].children.append(Raw(f"<!--{d}-->"))
    def handle_pi(self, d): self.stack[-1].children.append(Raw(f"<?{d}>"))
    def handle_data(self, d): self.stack[-1].children.append(Text(d))
    def handle_entityref(self, n): self.stack[-1].children.append(Text(f"&{n};"))
    def handle_charref(self, n): self.stack[-1].children.append(Text(f"&#{n};"))

    def handle_starttag(self, tag, attrs):
        tag = self._case(tag)
        n = Node(tag, self._attr_case(attrs))
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(self._case(tag), self._attr_case(attrs), selfclose=True))

    def _attr_case(self, attrs):
        """HTMLParser schreibt Attributnamen klein; SVG-Attribute (viewBox) behalten ihre Schreibweise aus dem Original."""
        raw = self.get_starttag_text() or ""
        if not any(ch.isupper() for ch in raw):
            return attrs
        names = {m.lower(): m for m in ATTR_NAME.findall(re.sub(r"\"[^\"]*\"|'[^']*'", '""', raw))}
        return [(names.get(k, k), v) for k, v in attrs]

    def handle_endtag(self, tag):
        tag = self._case(tag)
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    @staticmethod
    def _case(tag):
        return {"textpath": "textPath", "lineargradient": "linearGradient", "clippath": "clipPath"}.get(tag, tag)


def parse(doc):
    b = Builder()
    b.feed(doc)
    b.close()
    return b.root


def start_tag(n):
    parts = [n.tag]
    for k, v in n.attrs:
        parts.append(k if v is None else f'{k}="{html.escape(v, quote=True)}"')
    return "<" + " ".join(parts) + ("/>" if n.selfclose else ">")


def serialize(n):
    if isinstance(n, (Text, Raw)):
        return n.raw
    if n.tag == "#root":
        return "".join(serialize(c) for c in n.children)
    inner = "".join(c.raw if (n.tag in RAW and isinstance(c, Text)) else serialize(c) for c in n.children)
    if n.selfclose or n.tag in VOID:
        return start_tag(n)
    return start_tag(n) + inner + f"</{n.tag}>"


DONE = object()  # Markierung in Node.raw: Knoten ist bereits übersetzt


def svgs_in(n):
    for c in n.children:
        if isinstance(c, Node):
            if c.tag == "svg":
                yield c
            else:
                yield from svgs_in(c)


def text_of(n):
    if isinstance(n, Text):
        return html.unescape(n.raw)
    if isinstance(n, Raw):
        return ""
    return "".join(text_of(c) for c in n.children)


def inline_only(n):
    for c in n.children:
        if isinstance(c, Node):
            if c.tag == "svg":
                continue
            if c.tag not in INLINE:
                return False
            if not inline_only(c):
                return False
    return True


# ------------------------------------------------------------------ Segmente
def skeleton(n):
    """Inline-Inhalt -> (Schlüssel mit Platzhaltern, Zuordnung Platzhalter->Knoten, Datumswerte)."""
    tags, xs, dates = [], [], []
    out = []

    def walk(node):
        for c in node.children:
            if isinstance(c, Text):
                t = html.unescape(c.raw)
                for m in DATE_RX.finditer(t.replace(" ", " ")):
                    dates.append(m)
                out.append(t)
            elif isinstance(c, Raw):
                continue
            elif c.tag in ("svg", "img", "br", "wbr") or c.selfclose:
                xs.append(c)
                out.append(f"<x{len(xs) - 1}/>")
            else:
                tags.append(c)
                i = len(tags) - 1
                out.append(f"<g{i}>")
                walk(c)
                out.append(f"</g{i}>")
    walk(n)
    return norm("".join(out)), tags, xs, dates


PH = re.compile(r"<(/?)g(\d+)>|<x(\d+)/>")


def rebuild(translation, tags, xs, dates):
    """Übersetzung mit Platzhaltern -> HTML mit den Original-Tags."""
    pos, out = 0, []
    dates = list(dates)

    def esc(t):
        if "{date}" in t:
            t = t.replace("{date}", de_date_to_en(dates.pop(0)) if dates else "")
        return html.escape(brand_nbsp(t), quote=False)
    for m in PH.finditer(translation):
        out.append(esc(translation[pos:m.start()]))
        if m.group(3) is not None:
            out.append(serialize(xs[int(m.group(3))]))
        elif m.group(1):
            out.append(f"</{tags[int(m.group(2))].tag}>")
        else:
            out.append(start_tag(tags[int(m.group(2))]))
        pos = m.end()
    out.append(esc(translation[pos:]))
    return "".join(out)


def placeholders(s):
    return sorted(m.group(0) for m in PH.finditer(s))


class Translator:
    def __init__(self, cat):
        self.cat = cat
        self.missing = {}
        self.plain = {}  # Klartext-Fassung (für JSON-LD)
        for k, v in cat.items():
            if isinstance(v, str):
                self.plain.setdefault(PH.sub("", k).strip(), PH.sub("", v).strip())

    def t(self, key, where):
        if not has_words(PH.sub("", key)):
            return None
        v = self.cat.get(key)
        if v is None:
            self.missing.setdefault(key, where)
            return None
        if placeholders(v) != placeholders(key):
            self.missing.setdefault(key, where + " [Platzhalter passen nicht]")
            return None
        return v

    def tplain(self, s, where):
        k = norm(s)
        if not has_words(k):
            return s
        if k in self.cat and not PH.search(self.cat[k]):
            v = self.cat[k]
        elif k in self.plain:
            v = self.plain[k]
        else:
            self.missing.setdefault(k, where)
            return s
        if "{date}" in v:
            m = DATE_RX.search(s.replace(" ", " "))
            v = v.replace("{date}", de_date_to_en(m) if m else "")
        return brand_nbsp(v)

    # ---------- Baum übersetzen
    def node(self, n, where):
        if isinstance(n, (Text, Raw)) or n.raw is DONE:
            return
        if any(k == "data-keep" for k, _ in n.attrs):  # Sprachumschalter: bewusst in der Zielsprache, nicht übersetzen
            return
        if n.tag in RAW:
            return
        self.attrs(n, where)
        if n.tag != "svg" and n.children and inline_only(n):
            # Grafiken im Segment werden zum Platzhalter; ihre Texte (title, text) vorher übersetzen
            for s in svgs_in(n):
                self.node(s, where)
                s.raw = DONE
        if n.tag != "svg" and n.children and inline_only(n) and has_words(text_of(n)):
            key, tags, xs, dates = skeleton(n)
            # Attribute (aria-label, alt, title) aller Knoten im Segment vor dem Neuaufbau übersetzen
            for tg in tags + xs:
                if tg.raw is not DONE:
                    self.attrs(tg, where)
            if key:
                v = self.t(key, where)
                if v is not None:
                    n.children = [Raw(rebuild(v, tags, xs, dates))]
            return
        for i, c in enumerate(n.children):
            if isinstance(c, Text) and has_words(c.raw):
                raw = html.unescape(c.raw)
                k = norm(raw)
                v = self.t(k, where)
                if v is not None:
                    lead = raw[:len(raw) - len(raw.lstrip())]
                    trail = raw[len(raw.rstrip()):]
                    dates = list(DATE_RX.finditer(raw.replace(" ", " ")))
                    n.children[i] = Raw(lead + rebuild(v, [], [], dates) + trail)
            elif isinstance(c, Node):
                self.node(c, where)

    def attrs(self, n, where):
        if any(k == "data-keep" for k, _ in n.attrs):
            return
        new = []
        is_meta = n.tag == "meta" and any(k in ("name", "property") and v in META_CONTENT for k, v in n.attrs)
        for k, v in n.attrs:
            if v and (k in ATTRS or (k == "content" and is_meta)):
                if k in ("data-lines", "data-names"):
                    v = "|".join(self.tplain(x, where) for x in v.split("|"))
                else:
                    v = self.tplain(v, where)
            new.append((k, v))
        n.attrs = new


# ------------------------------------------------------------------ Seiten
def link_map(href):
    if not href.startswith("/") or href.startswith("//"):
        return href
    path, sep, rest = href.partition("#")
    p = path.rstrip("/") or "/"
    e = SLUGS.get(p)
    return (e + (sep + rest if sep else "")) if e else href


def json_ld(tr, txt, where):
    data = json.loads(txt)
    page_types = {"WebPage", "AboutPage", "ContactPage", "CollectionPage", "FAQPage", "BreadcrumbList", "HowTo", "ItemList", "WebApplication"}
    keep_text = {"@type", "@id", "@context", "url", "item", "email", "telephone", "propertyID", "value", "sameAs", "logo", "image",
                 "inLanguage", "datePublished", "dateModified", "lastReviewed", "addressCountry", "postalCode", "streetAddress",
                 "addressLocality", "cssSelector", "applicationCategory", "operatingSystem", "priceCurrency", "price", "termCode",
                 "legalName", "alternateName", "contentUrl", "encodingFormat"}

    def url(u):
        if isinstance(u, str) and u.startswith(DOMAIN):
            rest = u[len(DOMAIN):] or "/"
            path, sep, frag = rest.partition("#")
            e = SLUGS.get(path.rstrip("/") or "/")
            if e:
                return DOMAIN + e + (sep + frag if sep else "")
        return u

    def walk(o, ctx_type=None, key=None):
        if isinstance(o, dict):
            t = o.get("@type")
            t = t if isinstance(t, str) else (t[0] if isinstance(t, list) and t else ctx_type)
            out = {}
            for k, v in o.items():
                if k == "inLanguage":
                    out[k] = "en-GB"
                elif k == "url" and t == "ImageObject" and isinstance(v, str) and re.search(r"/assets/img/og-[a-z0-9\-]+\.jpg$", v) \
                        and key == "primaryImageOfPage" and os.path.exists(os.path.join(ROOT, v[len(DOMAIN):].lstrip("/")[:-4] + ".en.jpg")):
                    out[k] = v[:-4] + ".en.jpg"
                elif k in ("url", "item") and t not in ("Organization", "WebSite"):
                    out[k] = url(v)
                elif k == "@id" and isinstance(v, str) and re.search(r"#(webpage|breadcrumb|faq|vorgehen|stufen|service|app|termset)", v):
                    out[k] = url(v)
                elif k == "name" and t in ("Organization", "Person", "CollegeOrUniversity", "WebSite", "PostalAddress"):
                    out[k] = v
                elif k in keep_text:
                    out[k] = walk(v, t, k) if isinstance(v, (dict, list)) else v
                else:
                    out[k] = walk(v, t, k)
            return out
        if isinstance(o, list):
            return [walk(x, ctx_type, key) for x in o]
        if isinstance(o, str):
            if o.startswith(("http://", "https://", "mailto:", "tel:", "#", "/")) or re.fullmatch(r"[\d\-:+ T.]+", o):
                return url(o)
            return tr.tplain(o, where + " [JSON-LD]")
        return o
    return json.dumps(walk(data), ensure_ascii=False, separators=(",", ":"))


LEGAL_NOTE = ('<p class="x-legal-note">This English version is provided for convenience. '
              'Only the <a href="{de}" hreflang="de" lang="de" data-keep>German version</a> is legally binding.</p>')


def to_en(doc, de_path, tr, js_versions):
    where = de_path
    en = SLUGS[de_path]
    url_de = DOMAIN + ("/" if de_path == "/" else de_path)
    url_en = DOMAIN + en
    # Kopf: Sprache, Canonical, hreflang, og:url, og:locale
    doc = doc.replace('<html lang="de">', '<html lang="en">', 1)
    doc = doc.replace(f'<link rel="canonical" href="{url_de}">', f'<link rel="canonical" href="{url_en}">', 1)
    doc = doc.replace(f'<meta property="og:url" content="{url_de}">', f'<meta property="og:url" content="{url_en}">', 1)
    doc = doc.replace('\n<meta property="og:locale:alternate" content="en_GB">', "")
    doc = doc.replace('<meta property="og:locale" content="de_DE">', '<meta property="og:locale" content="en_GB">\n<meta property="og:locale:alternate" content="de_DE">', 1)
    doc = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?', "", doc)
    doc = doc.replace(f'<link rel="canonical" href="{url_en}">',
                      f'<link rel="canonical" href="{url_en}">\n' + alternates(de_path).rstrip("\n"), 1)
    # Skripte: englische Kopien
    for name, ver in js_versions.items():
        base = name[:-3]
        doc = re.sub(r'/assets/' + re.escape(base) + r'\.js\?v=[0-9a-f]+', f"/assets/{base}.en.js?v={ver}", doc)
    # Social-Bilder: englische Fassung, falls vorhanden
    def og(m):
        en_img = m.group(1) + ".en.jpg"
        fp = os.path.join(ROOT, en_img.lstrip("/"))
        if not os.path.exists(fp):
            return m.group(0)
        import hashlib
        return en_img + "?v=" + hashlib.sha1(open(fp, "rb").read()).hexdigest()[:8]
    doc = re.sub(r'(/assets/img/og-[a-z0-9\-]+)\.jpg\?v=[0-9a-f]+', og, doc)
    # JSON-LD
    doc = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',
                 lambda m: m.group(1) + json_ld(tr, m.group(2), where) + m.group(3), doc, flags=re.S)
    # Sprachumschalter: auf der englischen Seite zur deutschen Seite
    doc = re.sub(r'<li class="lang">.*?</li>', lang_switch(de_path, "en"), doc, count=1, flags=re.S)
    doc = re.sub(r'<a class="lang-m".*?</a>', lang_mobile(de_path, "en"), doc, count=1, flags=re.S)
    root = parse(doc)
    # Links umschreiben (außer Sprachumschalter)
    def fix(n):
        if isinstance(n, Node):
            if n.tag == "a" and not any(k == "data-keep" for k, _ in n.attrs):
                n.attrs = [(k, link_map(v) if k == "href" and v else v) for k, v in n.attrs]
            for c in n.children:
                fix(c)
    fix(root)
    tr.node(root, where)
    if de_path in ("/impressum", "/datenschutz"):
        doc_tmp = serialize(root)
        doc_tmp = re.sub(r"(</h1>)", lambda m: m.group(1) + LEGAL_NOTE.format(de=de_path), doc_tmp, count=1)
        root = parse(doc_tmp)

    return serialize(root)


def alternates(de_path):
    url_de = DOMAIN + ("/" if de_path == "/" else de_path)
    e = SLUGS.get(de_path)
    out = f'<link rel="alternate" hreflang="de" href="{url_de}">\n'
    if e:
        out += f'<link rel="alternate" hreflang="en" href="{DOMAIN + e}">\n'
    out += f'<link rel="alternate" hreflang="x-default" href="{url_de}">\n'
    return out


def _en_target(de_path):
    """Englische Entsprechung; die 404-Seite führt zur englischen Startseite."""
    return SLUGS.get(de_path) or (SLUGS["/"] if de_path == "/404" else None)


def lang_mobile(de_path, current):
    """Handy/Tablet: immer sichtbarer Sprachknopf neben „Menü“, zeigt die jeweils andere Sprache."""
    e = _en_target(de_path)
    if not e:
        return ""
    if current == "de":
        return f'<a class="lang-m" href="{e}" hreflang="en" lang="en" data-keep aria-label="English version" title="English version">EN</a>'
    de_href = "/" if de_path == "/404" else de_path
    return f'<a class="lang-m" href="{de_href}" hreflang="de" lang="de" data-keep aria-label="Deutsche Fassung" title="Deutsche Fassung">DE</a>'


def lang_switch(de_path, current):
    e = _en_target(de_path)
    if not e:
        return ""
    de_href = de_path
    if current == "de":
        return (f'<li class="lang"><span class="lang-cur" aria-current="true">DE</span>'
                f'<a class="lang-alt" href="{e}" hreflang="en" lang="en" data-keep aria-label="English version">EN</a></li>')
    return (f'<li class="lang"><a class="lang-alt" href="{de_href}" hreflang="de" lang="de" data-keep aria-label="Deutsche Fassung">DE</a>'
            f'<span class="lang-cur" aria-current="true">EN</span></li>')


def add_de_alternates(doc, de_path):
    """Deutsche Seite: hreflang en ergänzen und og:locale:alternate setzen."""
    if de_path not in SLUGS:
        return doc
    doc = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?', "", doc)
    url_de = DOMAIN + ("/" if de_path == "/" else de_path)
    doc = doc.replace(f'<link rel="canonical" href="{url_de}">', f'<link rel="canonical" href="{url_de}">\n' + alternates(de_path).rstrip("\n"), 1)
    doc = doc.replace('<meta property="og:locale" content="de_DE">', '<meta property="og:locale" content="de_DE">\n<meta property="og:locale:alternate" content="en_GB">', 1)
    return doc


# ------------------------------------------------------------------ Skripte
STR_RX = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'')  # "…" oder '…', zeilenweise


def js_en(src, tr, name):
    """Deutsche String-Literale in einem Skript durch Übersetzungen ersetzen (Schlüssel: Literal-Inhalt)."""
    def rep(m):
        q = '"' if m.group(1) is not None else "'"
        s = m.group(1) if q == '"' else m.group(2)
        v = tr.cat.get("js:" + s)  # Katalogeintrag zuerst: auch Einzelwörter wie "Kompetenzen", die wie Bezeichner aussehen
        if v is None and (not re.search(r"[A-Za-zÄÖÜäöüß]{3,}", s) or re.fullmatch(r"[\w\-.#\[\]=:,> ]+", s) and not re.search(r"[äöüÄÖÜß ]", s)):
            return m.group(0)
        if v is None:
            if re.search(r"[äöüÄÖÜß]|\b(und|der|die|das|mit|von|für|nicht|Ihr|Sie|wir|ist|eine?)\b", s):
                tr.missing.setdefault("js:" + s, "assets/" + name)
            return m.group(0)
        return q + v.replace(q, "\\" + q) + q
    out = STR_RX.sub(rep, src)
    return out.replace('"de-DE"', '"en-GB"')


def translate_fragment(doc, tr, where):
    """Beliebiges HTML-Dokument übersetzen (z. B. Social-Bild-Motive)."""
    root = parse(doc)
    tr.node(root, where)
    return serialize(root).replace('<html lang="de">', '<html lang="en">', 1)


def load_catalog():
    if not os.path.exists(CAT_PATH):
        return {}
    return json.load(open(CAT_PATH, encoding="utf-8"))
