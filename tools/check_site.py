#!/usr/bin/env python3
"""Inhaltliche Vollprüfung der gebauten Seiten: Links/Anker, IDs, Überschriften, Bilder, JSON-LD, Preisregel, Wortwiederholungen."""
import glob, json, os, re, sys, collections, html
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pages = {}
for f in glob.glob(ROOT + "/*.html") + glob.glob(ROOT + "/fokusfelder/*.html"):
    rel = os.path.relpath(f, ROOT)[:-5]
    url = "/" if rel == "index" else "/" + rel
    pages[url] = open(f, encoding="utf-8").read()

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.ids = []; s.links = []; s.heads = []; s.imgs = []; s.ld = []; s._h = None; s._ld = False; s.buf = ""
        s.text = []; s.skip = 0
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.append(a["id"])
        if t == "a" and "href" in a: s.links.append(a["href"])
        if t in ("h1", "h2", "h3", "h4"): s._h = t; s.buf = ""
        if t == "img": s.imgs.append(a)
        if t == "script" and a.get("type") == "application/ld+json": s._ld = True; s.buf = ""
        if t in ("script", "style"): s.skip += 1
    def handle_endtag(s, t):
        if t == s._h: s.heads.append((t, re.sub(r"\s+", " ", s.buf).strip())); s._h = None
        if t == "script" and s._ld: s.ld.append(s.buf); s._ld = False
        if t in ("script", "style"): s.skip -= 1
    def handle_data(s, d):
        if s._h or s._ld: s.buf += d
        if not s.skip: s.text.append(d)

info = {}
for u, h in pages.items():
    p = P(); p.feed(h); info[u] = p

errs, warns = [], []
def E(u, m): errs.append(f"{u}: {m}")
def W(u, m): warns.append(f"{u}: {m}")

for u, p in info.items():
    # IDs
    dup = [i for i, n in collections.Counter(p.ids).items() if n > 1]
    if dup: E(u, f"doppelte IDs {dup}")
    # Überschriften
    hs = [t for t, _ in p.heads]
    if hs.count("h1") != 1: E(u, f"{hs.count('h1')} H1")
    last = 0
    for t, txt in p.heads:
        lv = int(t[1])
        if last and lv > last + 1: W(u, f"Überschriftensprung h{last}->h{lv}: {txt[:40]}")
        last = lv
    # Bilder
    for a in p.imgs:
        if not a.get("alt") and a.get("alt") != "": E(u, f"img ohne alt {a.get('src')}")
        if not a.get("width") or not a.get("height"): W(u, f"img ohne width/height {a.get('src')}")
    # JSON-LD
    for b in p.ld:
        try: json.loads(b)
        except Exception as e: E(u, f"JSON-LD ungültig: {e}")
    # Links
    for href in p.links:
        if href.startswith(("mailto:", "tel:", "http://", "https://")):
            if href.startswith("http://"): W(u, f"http-Link {href}")
            continue
        path, _, frag = href.partition("#")
        tgt = u if path == "" else path.split("?")[0]
        if tgt not in pages and not os.path.isfile(ROOT + tgt):
            E(u, f"toter Link {href}"); continue
        if frag and tgt in info and frag not in info[tgt].ids: E(u, f"Anker fehlt {href}")
    # Preisregel
    txt = " ".join(p.text)
    if u != "/innolab" and re.search(r"€|\bEUR\b|Festpreis|netto|zzgl\. ?USt", txt) and u not in ("/impressum", "/datenschutz"):
        W(u, "Preisbegriff außerhalb InnoLab: " + ", ".join(sorted(set(re.findall(r"€|EUR|Festpreis|netto|zzgl\. ?USt", txt)))))
    # Überschriften-Regeln: Frage/Imperativ
    for t, txt in p.heads:
        if t in ("h1", "h2") and "?" in txt and u not in ("/faq",): W(u, f"Frage in {t}: {txt}")
    # Title/Description
    m = re.search(r"<title>(.*?)</title>", pages[u]); d = re.search(r'name="description" content="(.*?)"', pages[u])
    if not m or not (20 <= len(html.unescape(m.group(1))) <= 65): W(u, f"Title-Länge {len(m.group(1)) if m else 0}")
    if not d or not (70 <= len(html.unescape(d.group(1))) <= 165): W(u, f"Description-Länge {len(d.group(1)) if d else 0}")
    if 'rel="canonical"' not in pages[u]: E(u, "canonical fehlt")
    # Doppelte Wörter, Doppelleerzeichen, typische Tippfehler
    flat = re.sub(r"\s+", " ", txt)
    for m in re.finditer(r"\b(\w{3,}) \1\b", flat, re.I):
        W(u, f"Wortdopplung: „{m.group(0)}“")
    for bad in ["  ", " ,", " .", "..", "ae ", "ue ", "oe "]:
        pass
    if "&amp;amp;" in pages[u] or "&amp;#" in pages[u]: E(u, "doppelt escapte Entität im HTML")
    for pat, why in [(r"\bGap Lab\b", "Markenschreibweise „Gap Lab“ (THE GAP Lab)"), (r"\bInnolab\b", "„Innolab“ statt InnoLab"), (r"\bfuer\b|\bueber\b|\bGroesse\b", "ersetzte Umlaute"), (r"\s[,.;:](?=\s|$)", "Leerzeichen vor Satzzeichen"), (r"(?<!\d)\.\.(?!\.)", "Doppelpunkt-Punkt"), (r"\bdass dass\b|\bdie die\b", "Wortdopplung")]:
        for m in re.finditer(pat, flat):
            W(u, f"{why}: …{flat[max(0,m.start()-25):m.end()+25]}…")
            break


# ---- SEO/GEO-Prüfung je Seite
titles, descs = {}, {}
for u, h in pages.items():
    if u == "/404": continue
    t = html.unescape(re.search(r"<title>(.*?)</title>", h).group(1)); d = html.unescape(re.search(r'name="description" content="(.*?)"', h).group(1))
    if t in titles: E(u, f"Title doppelt mit {titles[t]}")
    if d in descs: E(u, f"Description doppelt mit {descs[d]}")
    titles[t] = u; descs[d] = u
    if len(t) > 62: W(u, f"Title {len(t)} Zeichen (max. 62)")
    if len(d) > 160: W(u, f"Description {len(d)} Zeichen (max. 160)")
    img = re.search(r'og:image" content="https://www\.gap-lab\.de(/[^"]+)"', h)
    if not img or not os.path.isfile(ROOT + img.group(1)): E(u, "og:image-Datei fehlt")
    if u not in ("/", "/impressum", "/datenschutz", "/ki-readiness", "/innolab", "/404") and img and "og-verbindet" in img.group(1): W(u, "nutzt das Standard-Social-Bild")
    if '"dateModified"' not in h: E(u, "dateModified fehlt")
    # Haupt-Suchbegriff in H1 oder Title
    m1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S); h1t = html.unescape(re.sub(r"<[^>]+>", "", m1.group(1))).replace("\u00ad", "")
    if u not in ("/impressum", "/datenschutz", "/ki-readiness") and not set(re.findall(r"\w{6,}", t.lower())) & set(re.findall(r"\w{6,}", h1t.lower())): W(u, "Title und H1 teilen kein Schlüsselwort")

# Sitemap vs Seiten
sm = open(ROOT + "/sitemap.xml").read()
for blk in re.finditer(r"<loc>https://www\.gap-lab\.de(/[^<]*)</loc>\s*<lastmod>([^<]*)</lastmod>", sm):
    u, d = blk.group(1), blk.group(2)
    if u in pages and f'"dateModified":"{d}"' not in pages[u]: E(u, f"dateModified weicht von sitemap-lastmod {d} ab")
smu = set(re.findall(r"https://www.gap-lab\.de(/[^<]*)</loc>", sm))
for u in pages:
    if u == "/404": continue
    if u not in smu: E(u, "fehlt in sitemap.xml")
for u in smu:
    if u not in pages: E(u, "Sitemap-URL ohne Seite")
ll = open(ROOT + "/llms.txt").read()
for u in pages:
    if u in ("/404", "/impressum", "/datenschutz"): continue
    if ("https://www.gap-lab.de" + (u if u != "/" else "/")) not in ll: W(u, "fehlt in llms.txt")

print("\n".join(["FEHLER:"] + errs) if errs else "keine Fehler")
print("\n".join(["WARNUNGEN:"] + warns) if warns else "keine Warnungen")
sys.exit(1 if errs else 0)
