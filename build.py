#!/usr/bin/env python3
"""Ehitab äpi:
  docs/index.html      – valmis äpp GitHub Pagesi jaoks (üks fail + sw.js, manifest, ikoonid)
  docs/artifact.html   – sama claude.ai Artifacti jaoks (ilma <html>/<head> raamita)

Käivita:  python3 build.py
"""
import base64, json, pathlib, re, shutil

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
IMAGES = ROOT / "images"
OUT = ROOT / "docs"

app = (SRC / "app.html").read_text(encoding="utf-8")
data = (SRC / "data.js").read_text(encoding="utf-8")
config = (SRC / "config.js").read_text(encoding="utf-8")

keys = sorted(set(re.findall(r'src:\s*"([a-z_]+)"', data)))
images, missing = {}, []
for k in keys:
    p = IMAGES / f"{k}.jpg"
    if not p.exists():
        missing.append(k); continue
    images[k] = "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode("ascii")
credits = json.loads((IMAGES / "credits.json").read_text(encoding="utf-8")) if (IMAGES / "credits.json").exists() else {}
images_js = "window.IMAGES = " + json.dumps(images) + ";\nwindow.CREDITS = " + json.dumps(credits, ensure_ascii=False) + ";"

def render(cfg):
    return app.replace("__DATA__", data).replace("__CONFIG__", cfg).replace("__IMAGES__", images_js)

# Artifact: ilma Firebase'ita (välised skriptid on seal nagunii blokeeritud)
fragment = render("window.FIREBASE_CONFIG = null;")
full = ('<!doctype html>\n<html lang="et">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="color-scheme" content="light dark">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
        '<meta name="theme-color" content="#3A7A4B">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="icon" href="icon-192.png">\n'
        '<link rel="apple-touch-icon" href="icon-192.png">\n'
        '</head>\n<body>\n' + render(config) + '\n</body>\n</html>\n')

OUT.mkdir(exist_ok=True)
(OUT / "artifact.html").write_text(fragment, encoding="utf-8")
(OUT / "index.html").write_text(full, encoding="utf-8")
for f in (SRC / "static").iterdir():
    shutil.copy(f, OUT / f.name)
(OUT / ".nojekyll").write_text("")
print(f"OK: {len(images)} pilti, index.html {len(full)//1024} KB, Firebase {'SEES' if re.search(r'^window\.FIREBASE_CONFIG\s*=\s*\{', config, re.M) else 'väljas (config.js on null)'}")
if missing:
    print("PUUDU pildid:", ", ".join(missing))
