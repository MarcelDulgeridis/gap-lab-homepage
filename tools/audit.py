#!/usr/bin/env python3
"""QA-Audit der erzeugten Seiten. Exit-Code 1 bei Fehlern."""
import glob, html, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOMAIN = "https://gap-lab.de"
files = [f for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True) if "/tools/" not in f and "/node_modules/" not in f]


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.imgs, self.heads, self.styleattr, self.inline_scripts = set(), [], [], [], 0, 0
        self.text, self._in_script, self._script_type, self.words = [], False, None, 0
        self._skip = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if "style" in a: self.styleattr += 1
        if tag == "a" and "href" in a: self.hrefs.append(a["href"])
        if tag == "img": self.imgs.append(a)
        if tag in ("h1", "h2", "h3", "h4"): self.heads.append(int(tag[1]))
        if tag == "script":
            self._in_script, self._script_type = True, a.get("type")
            if "src" not in a and a.get("type") != "application/ld+json": self.inline_scripts += 1
        if tag in ("style",): self._skip = True

    def handle_endtag(self, tag):
        if tag == "script": self._in_script = False
        if tag == "style": self._skip = False

    def handle_data(self, d):
        if not self._in_script and not self._skip:
            self.words += len(d.split())


def route_to_file(path):
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"): return os.path.join(ROOT, "index.html")
    p = path.lstrip("/")
    for cand in (p, p + ".html", p + "/index.html"):
        full = os.path.join(ROOT, cand)
        if os.path.isfile(full): return full
    return None


errors, warns = [], []
pages = {}
titles, descs = {}, {}
for f in sorted(files):
    rel = os.path.relpath(f, ROOT)
    txt = open(f, encoding="utf-8").read()
    p = P(); p.feed(txt); pages[f] = (txt, p)
    is404 = rel == "404.html"
    t = re.search(r"<title>(.*?)</title>", txt, re.S); t = html.unescape(t.group(1)) if t else ""
    d = re.search(r'<meta name="description" content="(.*?)">', txt); d = html.unescape(d.group(1)) if d else ""
    if not t or len(t) > 62: errors.append(f"{rel}: Title-Länge {len(t)}")
    if not (100 <= len(d) <= 165): errors.append(f"{rel}: Description-Länge {len(d)}")
    titles.setdefault(t, []).append(rel); descs.setdefault(d, []).append(rel)
    if len(re.findall(r"<h1[ >]", txt)) != 1: errors.append(f"{rel}: H1-Anzahl")
    if not is404 and f'<link rel="canonical" href="{DOMAIN}' not in txt: errors.append(f"{rel}: canonical")
    for need in ('property="og:title"', 'property="og:description"', 'property="og:image"', 'name="twitter:card"', 'hreflang="de"', 'lang="de"'):
        if need not in txt: errors.append(f"{rel}: fehlt {need}")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S):
        try: json.loads(m.group(1))
        except Exception as e: errors.append(f"{rel}: JSON-LD ungültig {e}")
    if p.styleattr: errors.append(f"{rel}: {p.styleattr} style-Attribute (CSP)")
    if p.inline_scripts: errors.append(f"{rel}: Inline-Skript (CSP)")
    for img in p.imgs:
        if "alt" not in img: errors.append(f"{rel}: img ohne alt")
        if "width" not in img or "height" not in img: warns.append(f"{rel}: img ohne width/height {img.get('src')}")
    # Überschriften nicht überspringen
    last = 0
    for h in p.heads:
        if last and h > last + 1: errors.append(f"{rel}: Überschriftensprung h{last}->h{h}")
        last = h
    # interne Links
    for href in p.hrefs:
        if href.startswith(("mailto:", "tel:")): continue
        if href.startswith("http"):
            if href.startswith(DOMAIN):
                href = href[len(DOMAIN):] or "/"
            else:
                continue
        if href.startswith("#"):
            if href[1:] not in p.ids: errors.append(f"{rel}: Anker {href} fehlt")
            continue
        target = route_to_file(href)
        if not target: errors.append(f"{rel}: Link {href} nicht auflösbar"); continue
        if "#" in href:
            frag = href.split("#")[1]
            tp = pages.get(target) or None
            ttxt = open(target, encoding="utf-8").read()
            if f'id="{frag}"' not in ttxt: errors.append(f"{rel}: Anker {href} fehlt im Ziel")
    # Asset-Referenzen
    for m in re.finditer(r'(?:src|href)="(/assets/[^"?]+|/favicon\.svg|/site\.webmanifest)', txt):
        if not os.path.isfile(os.path.join(ROOT, m.group(1).lstrip("/"))): errors.append(f"{rel}: Asset fehlt {m.group(1)}")
    # Fremde Hosts (CSP)
    for m in re.finditer(r'(?:src|href)="(https?://[^"]+)"', txt):
        u = m.group(1)
        if m.group(0).startswith("src=") and not u.startswith(DOMAIN): errors.append(f"{rel}: externes src {u}")
        if "stylesheet" in txt[max(0, m.start()-40):m.start()] and not u.startswith(DOMAIN): errors.append(f"{rel}: externes CSS {u}")
    print(f"{rel:48s} words={p.words:4d} title={len(t):2d} desc={len(d):3d}")

for k, v in titles.items():
    if len(v) > 1: errors.append(f"Doppelter Title: {k} -> {v}")
for k, v in descs.items():
    if len(v) > 1: errors.append(f"Doppelte Description: {v}")

sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
for loc in re.findall(r"<loc>(.*?)</loc>", sm):
    if not route_to_file(loc[len(DOMAIN):] or "/"): errors.append(f"Sitemap-URL ohne Seite: {loc}")


# ------------------------------------------------------------------ Tiefenprüfungen (GEO/SEO, Story, Kontrast)
def lum(hexc):
    h = hexc.lstrip("#"); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

for fg, bg, label, need in [
    ("#7A5A27", "#fbf8f2", "gold-text auf paper", 4.5), ("#7A5A27", "#f2eadf", "gold-text auf cream", 4.5), ("#7A5A27", "#fffefa", "gold-text auf white", 4.5),
    ("#85642C", "#fffefa", "f1 auf white", 4.5), ("#85642C", "#f4ebd8", "f1 auf f1-tint", 4.5),
    ("#2c5a8c", "#fffefa", "f2 auf white", 4.5), ("#2c5a8c", "#e3ecf6", "f2 auf f2-tint", 4.5),
    ("#2a6b5e", "#fffefa", "f3 auf white", 4.5), ("#2a6b5e", "#dcefe9", "f3 auf f3-tint", 4.5),
    ("#FDFCFA", "#101D33", "on-navy auf navy", 4.5), ("#C9D0DA", "#101D33", "on-navy-muted auf navy", 4.5), ("#CFAD6B", "#101D33", "gold-mid auf navy", 4.5),
    ("#4f5b6e", "#fbf8f2", "muted auf paper", 4.5), ("#4f5b6e", "#f2eadf", "muted auf cream", 4.5),
    ("#FFFFFF", "#85642C", "weiss auf f1", 4.5), ("#FFFFFF", "#2c5a8c", "weiss auf f2", 4.5), ("#FFFFFF", "#2a6b5e", "weiss auf f3", 4.5),
    ("#FFFFFF", "#4a79ab", "weiss auf Ebene 3", 3.0), ("#FFFFFF", "#7a5a27", "weiss auf Ebene 4", 4.5),
]:
    c = contrast(fg, bg)
    if c < need: errors.append(f"Kontrast {label}: {c:.2f} < {need}")

sm_urls = re.findall(r"<loc>(.*?)</loc>", sm)
llms = open(os.path.join(ROOT, "llms.txt"), encoding="utf-8").read()
for u in sm_urls:
    if u not in llms: errors.append(f"llms.txt ohne {u}")
if not os.path.isfile(os.path.join(ROOT, "llms-full.txt")): errors.append("llms-full.txt fehlt")

inbound = {}
for f, (txt, p) in pages.items():
    for href in set(p.hrefs):
        if href.startswith(("mailto:", "tel:", "#", "http")) and not href.startswith(DOMAIN): continue
        tgt = href.replace(DOMAIN, "").split("#")[0].split("?")[0] or "/"
        if os.path.relpath(f, ROOT) != (("index.html" if tgt == "/" else tgt.lstrip("/") + ".html")):
            inbound.setdefault(tgt, set()).add(os.path.relpath(f, ROOT))
for u in sm_urls:
    path = u.replace(DOMAIN, "") or "/"
    n = len(inbound.get(path, ()))
    if n < 4: errors.append(f"zu wenige interne Links auf {path}: {n}")

ALL_DEF = set()
for f, (txt, p) in pages.items():
    for m in re.finditer(r'"@id":"([^"]+)","@type"', txt): ALL_DEF.add(m.group(1))
for f, (txt, p) in pages.items():
    rel = os.path.relpath(f, ROOT)
    ids_defined, ids_ref = set(), set()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S):
        g = json.loads(m.group(1)).get("@graph", [])
        def walk(o, top):
            if isinstance(o, dict):
                if "@id" in o and len(o) == 1: ids_ref.add(o["@id"])
                elif "@id" in o and top: ids_defined.add(o["@id"])
                for v in o.values(): walk(v, False)
            elif isinstance(o, list):
                for v in o: walk(v, top)
        for n in g:
            if "@id" in n: ids_defined.add(n["@id"])
            walk({k: v for k, v in n.items() if k != "@id"}, False)
    for r in ids_ref:
        if r not in ids_defined and r not in ALL_DEF and not r.startswith("https://www.schubart-dulgeridis.de/"): errors.append(f"{rel}: Schema-Referenz {r} ohne Definition")
    if '"speakable"' in txt and 'class="answer"' not in txt: errors.append(f"{rel}: speakable ohne .answer")
    if rel not in ("404.html",) and "datePublished" in txt and not re.search(r'"dateModified":"2026-11-04"', txt) and rel in ("index.html","leistungen.html"): errors.append(f"{rel}: dateModified veraltet")

print()
for w in warns: print("WARN ", w)
for e in errors: print("FEHLER", e)
print(f"\n{len(files)} Dateien, {len(errors)} Fehler, {len(warns)} Warnungen")
sys.exit(1 if errors else 0)
