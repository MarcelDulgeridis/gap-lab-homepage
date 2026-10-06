#!/usr/bin/env python3
"""Lokaler Server mit Clean-URL-Verhalten und den Security-Headern aus vercel.json (zum Testen)."""
import http.server, json, os, sys, socketserver

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
cfg = json.load(open(os.path.join(ROOT, "vercel.json")))
HEADERS = []
for rule in cfg.get("headers", []):
    if rule["source"] == "/(.*)":
        HEADERS = [(h["key"], h["value"]) for h in rule["headers"]]


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def translate_path(self, path):
        p = path.split("?")[0].split("#")[0]
        rel = p.lstrip("/")
        for cand in (rel, rel + ".html", os.path.join(rel, "index.html")):
            full = os.path.join(ROOT, cand)
            if os.path.isfile(full):
                return full
        return os.path.join(ROOT, "404.html")

    def end_headers(self):
        for k, v in HEADERS:
            self.send_header(k, v)
        super().end_headers()

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", int(sys.argv[1]) if len(sys.argv) > 1 else 8960), H) as s:
    s.serve_forever()
