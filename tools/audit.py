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

print()
for w in warns: print("WARN ", w)
for e in errors: print("FEHLER", e)
print(f"\n{len(files)} Dateien, {len(errors)} Fehler, {len(warns)} Warnungen")
sys.exit(1 if errors else 0)
