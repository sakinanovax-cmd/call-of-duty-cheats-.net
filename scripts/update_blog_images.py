# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
urls = [
    u.strip()
    for u in (root / "scripts" / "ign_ok_urls.txt").read_text(encoding="utf-8").splitlines()
    if u.strip()
][:30]

alts = [
    "Call of Duty Warzone gameplay screenshot from IGN",
    "Warzone combat gameplay image via IGN",
    "COD Warzone gunfight screenshot from IGN",
    "Warzone battlefield gameplay from IGN",
    "Call of Duty Warzone action screenshot via IGN",
    "Warzone tactical gameplay image from IGN",
    "COD Warzone street fight screenshot via IGN",
    "Warzone operator gameplay from IGN",
    "Call of Duty Warzone map combat via IGN",
    "Warzone close-quarters gameplay from IGN",
    "COD Warzone outdoor fight screenshot via IGN",
    "Warzone vehicle combat gameplay from IGN",
    "Call of Duty Warzone rooftop fight via IGN",
    "Warzone subway zone gameplay from IGN",
    "COD Warzone underground combat via IGN",
    "Warzone tunnel fight screenshot from IGN",
    "Call of Duty Warzone metro gameplay via IGN",
    "Warzone interior combat image from IGN",
    "COD Warzone close combat screenshot via IGN",
    "Warzone objective fight gameplay from IGN",
    "Call of Duty Warzone corridor fight via IGN",
    "Warzone station combat screenshot from IGN",
    "COD Warzone underground map via IGN",
    "Warzone Verdansk subway gameplay from IGN",
    "Call of Duty trench combat screenshot via IGN",
    "Warzone / Modern Warfare trench fight from IGN",
    "COD scrapyard combat gameplay via IGN",
    "Call of Duty Price trench screenshot from IGN",
    "Warzone promenade combat gameplay via IGN",
    "COD train station fight screenshot from IGN",
]

path = root / "blog.html"
html = path.read_text(encoding="utf-8")

img_re = re.compile(
    r'<img class="blog-card-img" src="[^"]+" alt="[^"]+" loading="lazy" width="640" height="400">'
)
matches = list(img_re.finditer(html))
if len(matches) != 30:
    raise SystemExit(f"expected 30 card images, found {len(matches)}")

parts = []
last = 0
for i, m in enumerate(matches):
    parts.append(html[last:m.start()])
    parts.append(
        f'<img class="blog-card-img" src="{urls[i]}" alt="{alts[i]}" loading="lazy" width="640" height="400">'
    )
    last = m.end()
parts.append(html[last:])
new_html = "".join(parts)

found = re.findall(r'<img class="blog-card-img" src="([^"]+)"', new_html)
assert len(found) == 30 and len(set(found)) == 30, (len(found), len(set(found)))

path.write_text(new_html, encoding="utf-8")
print("Updated blog.html with 30 unique IGN gameplay images")
for i, u in enumerate(found, 1):
    print(f"{i:02d}", u.split("/")[-1][:70])
