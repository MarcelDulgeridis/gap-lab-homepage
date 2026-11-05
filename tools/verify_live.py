#!/usr/bin/env python3
"""Prüft nach dem Deployment, ob die Live-Seite dem lokalen Stand entspricht (Weiterleitung, Titel, Bilder, Sitemap)."""
import re, sys, urllib.request, urllib.error, os


class R308(urllib.request.HTTPRedirectHandler):
    """Python 3.9 folgt 308 nicht von selbst."""
    def http_error_308(self, req, fp, code, msg, headers):
        return self.http_error_302(req, fp, 302, msg, headers)


urllib.request.install_opener(urllib.request.build_opener(R308))

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = "https://www.gap-lab.de"
ok = True


def get(path, follow=True):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "gap-lab-verify/1.0"})
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return r.status, r.geturl(), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, BASE + path, ""


def check(name, cond, detail=""):
    global ok
    print(("OK    " if cond else "FEHLT ") + name + (f"  ({detail})" if detail and not cond else ""))
    ok &= bool(cond)


s, url, _ = get("/fokusfelder/verhandlungsfuehrung")
check("alte Adresse leitet auf neue Seite weiter", s == 200 and url.endswith("/fokusfelder/strategie-vertrieb-innovation"), f"{s} {url}")
for rel in ["index", "leistungen", "fokusfelder", "fokusfelder/strategie-vertrieb-innovation", "innolab", "ueber-uns", "faq", "glossar", "kontakt"]:
    local = open(os.path.join(ROOT, rel + ".html"), encoding="utf-8").read()
    lt = re.search(r"<title>(.*?)</title>", local).group(1)
    path = "/" if rel == "index" else "/" + rel
    s, _, live = get(path)
    m = re.search(r"<title>(.*?)</title>", live)
    check(f"{path}: Titel live = lokal", s == 200 and m and m.group(1) == lt, f"{s} {m.group(1) if m else '-'}")
s, _, sm = get("/sitemap.xml")
check("Sitemap enthält neue Fokusfeld-Seite", "strategie-vertrieb-innovation" in sm and "verhandlungsfuehrung" not in sm)
for img in ["og-verbindet.jpg", "og-strategie-vertrieb.jpg", "og-fokusfelder.jpg"]:
    s, _, _ = get("/assets/img/" + img)
    check(f"Bild {img} erreichbar", s == 200, str(s))
print("\nALLES LIVE" if ok else "\nNOCH NICHT VOLLSTÄNDIG LIVE (Vercel braucht nach dem Push 1 bis 2 Minuten)")
sys.exit(0 if ok else 1)
