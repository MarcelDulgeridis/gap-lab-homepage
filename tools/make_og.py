#!/usr/bin/env python3
"""Erzeugt die Social-Bilder (1200x630) aller Seiten aus tools/seo_meta.py. Nur Bilder, deren Text sich geändert hat, werden neu gerendert
(Stand in tools/og_state.json). Aufruf: python3 tools/make_og.py  (macOS, Swift)."""
import hashlib, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import seo_meta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATE = os.path.join(ROOT, "tools", "og_state.json")
state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
done = 0
for path, raw in seo_meta.META.items():
    if "og_image" not in raw:
        continue
    m = seo_meta.resolve(raw)
    args = [m["og_kicker"], m["og_line1"], m["og_line2"], m.get("og_sub", "")]
    h = hashlib.sha1("|".join(args).encode()).hexdigest()[:12]
    dst = os.path.join(ROOT, m["og_image"].lstrip("/"))
    if state.get(m["og_image"]) == h and os.path.exists(dst):
        continue
    tmp = "/tmp/og_make.png"
    subprocess.run(["swift", os.path.join(ROOT, "tools", "og_page.swift"), tmp] + args, check=True, capture_output=True)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", tmp, "--out", dst], check=True, capture_output=True)
    state[m["og_image"]] = h
    done += 1
    print("neu:", m["og_image"], args[1:3])
json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1, sort_keys=True)
print(f"{done} Bild(er) neu erzeugt")
