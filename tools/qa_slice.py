#!/usr/bin/env python3
"""Schneidet Vollseiten-Screenshots mit Chrome in lesbare Abschnitte (ohne PIL): qa_slice.py <ordner> <breite_px> <abschnitt_px> <dateien...>"""
import os, subprocess, sys
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
folder, outw, sech = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
for name in sys.argv[4:]:
    src = os.path.join(folder, name)
    info = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", src], capture_output=True, text=True).stdout
    w = int(info.split("pixelWidth:")[1].split()[0]); h = int(info.split("pixelHeight:")[1].split()[0])
    scaled_h = round(h * outw / w); n = -(-scaled_h // sech)
    os.makedirs(os.path.join(folder, "sl"), exist_ok=True)
    for i in range(n):
        wrap = os.path.join(folder, "sl", f"_w_{name}_{i}.html")
        open(wrap, "w").write(f'<html><body style="margin:0;background:#fff"><div style="width:{outw}px;height:{sech}px;overflow:hidden"><img src="file://{src}" style="width:{outw}px;display:block;margin-top:-{i*sech}px"></div></body></html>')
        out = os.path.join(folder, "sl", f"{name[:-4]}_{i:02d}.png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", f"--window-size={outw},{sech}", f"--screenshot={out}", "--virtual-time-budget=2000", "file://" + wrap], capture_output=True)
        os.remove(wrap)
    print(name, h, n)
