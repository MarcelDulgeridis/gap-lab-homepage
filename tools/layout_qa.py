#!/usr/bin/env python3
"""Layout-QA: lädt jede Seite in Headless-Chrome bei mehreren Breiten, injiziert layout_audit.js (nur lokal, ohne CSP)
und fasst Befunde zusammen. Optional --shots: Vollseiten-Screenshots in einen Ordner."""
import http.server, json, os, re, socketserver, subprocess, sys, threading, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAGES = ["/", "/leistungen", "/fokusfelder", "/fokusfelder/verhandlungsfuehrung", "/fokusfelder/leadership-organisation",
         "/fokusfelder/finance-transformation", "/innolab", "/ki-readiness", "/ueber-uns", "/kontakt", "/faq", "/glossar", "/impressum", "/datenschutz", "/404"]
WIDTHS = [int(w) for w in (sys.argv[sys.argv.index("--widths") + 1].split(",") if "--widths" in sys.argv else "360,414,768,1024,1280,1600".split(","))]
SHOTS = sys.argv[sys.argv.index("--shots") + 1] if "--shots" in sys.argv else None
PORT = 8977


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def do_GET(self):
        p = self.path.split("?")[0].split("#")[0]; rel = p.lstrip("/")
        full = None
        for cand in (rel, rel + ".html", os.path.join(rel, "index.html")):
            if rel != "" and os.path.isfile(os.path.join(ROOT, cand)): full = os.path.join(ROOT, cand); break
        if rel == "": full = os.path.join(ROOT, "index.html")
        if full is None: full = os.path.join(ROOT, "404.html")
        data = open(full, "rb").read()
        ctype = self.guess_type(full)
        if full.endswith(".html"):
            data = data.replace(b"</body>", b'<script src="/tools/layout_audit.js"></script></body>')
        self.send_response(200); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def log_message(self, *a): pass


socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()


if '--serve-only' in sys.argv:
    import time
    print('QA-Server auf', PORT, flush=True)
    while True: time.sleep(3600)


def chrome(args, timeout=60):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox", "--force-device-scale-factor=1", "--lang=de-DE"] + args,
                          capture_output=True, text=True, timeout=timeout)


results = collections.defaultdict(lambda: collections.defaultdict(list))
heights = {}
for w in WIDTHS:
    for pg in PAGES:
        r = chrome([f"--window-size={w},1000", "--virtual-time-budget=6000", "--dump-dom", f"http://127.0.0.1:{PORT}{pg}"])
        m = re.search(r'<pre id="qa-out">(.*?)</pre>', r.stdout, re.S)
        if not m: results[pg][w].append(("qa-fail", "kein Ergebnis")); continue
        d = json.loads(m.group(1).replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))
        heights[(pg, w)] = d["h"]
        seen = set()
        for k, v in d["issues"]:
            if (k, v) in seen: continue
            seen.add((k, v)); results[pg][w].append((k, v))
        if SHOTS:
            os.makedirs(SHOTS, exist_ok=True)
            name = (pg.strip("/").replace("/", "_") or "home") + f"_{w}.png"
            chrome([f"--window-size={w},{min(d['h'], 16000)}", "--virtual-time-budget=6000", f"--screenshot={os.path.join(SHOTS, name)}", f"http://127.0.0.1:{PORT}{pg}"])
total = 0
for pg in PAGES:
    grouped = collections.OrderedDict()
    for w in WIDTHS:
        for k, v in results[pg][w]:
            key = (k, re.sub(r"@y\d+", "", v)); grouped.setdefault(key, []).append(w)
    for (k, v), ws in grouped.items():
        total += 1; print(f"{pg:40s} {','.join(map(str, ws)):26s} {k:13s} {v}")
print(f"\n{total} Befunde (gruppiert)")
