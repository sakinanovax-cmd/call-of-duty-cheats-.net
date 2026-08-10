# -*- coding: utf-8 -*-
from pathlib import Path
import re
import json

root = Path(__file__).resolve().parents[1]
html = list(root.glob("*.html"))
sm = (root / "sitemap.xml").read_text(encoding="utf-8")
locs = re.findall(r"<loc>(.*?)</loc>", sm)

issues = []
for p in html:
    t = p.read_text(encoding="utf-8", errors="ignore")
    title = re.search(r"<title>(.*?)</title>", t)
    desc = re.search(r'name="description" content="(.*?)"', t)
    canon = re.search(r'rel="canonical" href="(.*?)"', t)
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.I | re.S)
    schema = len(re.findall(r"application/ld\+json", t))
    imgs = re.findall(r"<img[^>]+>", t)
    noalt = [i for i in imgs if "alt=" not in i]
    h1_clean = [re.sub(r"<[^>]+>", "", h).strip() for h in h1s]
    body_txt = re.sub(r"<script.*?</script>", "", t, flags=re.S | re.I)
    body_txt = re.sub(r"<[^>]+>", " ", body_txt)
    title_text = title.group(1).replace("&amp;", "&") if title else ""
    issues.append(
        {
            "file": p.name,
            "title": title_text or None,
            "title_len": len(title_text),
            "desc_len": len(desc.group(1)) if desc else 0,
            "desc": desc.group(1) if desc else None,
            "canon": canon.group(1) if canon else None,
            "h1_count": len(h1_clean),
            "h1": h1_clean,
            "og": bool(re.search(r'property="og:title"', t)),
            "schema": schema,
            "img_no_alt": len(noalt),
            "zadeyo": bool(re.search(r"zadeyo", t, re.I)),
            "lang": bool(re.search(r"<html[^>]+lang=", t)),
            "internal_buy": "call-of-duty-cheats.html" in t,
            "words": len(re.findall(r"[A-Za-z0-9']+", body_txt)),
            "hotlink_ign": "sm.ign.com" in t,
            "autoplay_video": bool(re.search(r"<video[^>]+autoplay", t, re.I)),
            "lazy_video": "video-poster-play" in t or 'preload="none"' in t,
        }
    )

sm_names = set()
for loc in locs:
    name = loc.rstrip("/").split("/")[-1]
    sm_names.add(name if name else "index.html")
    if loc.rstrip("/").endswith("codcheats.net"):
        sm_names.add("index.html")
html_set = {p.name for p in html}

bad_h1 = [(x["file"], x["h1_count"], x["h1"]) for x in issues if x["h1_count"] != 1]
long_title = [(x["file"], x["title_len"], x["title"]) for x in issues if x["title_len"] > 65]
long_desc = [(x["file"], x["desc_len"]) for x in issues if x["desc_len"] > 165]
short_desc = [(x["file"], x["desc_len"]) for x in issues if x["desc_len"] and x["desc_len"] < 70]
thin = [(x["file"], x["words"]) for x in issues if x["words"] < 300]
hotlink = [x["file"] for x in issues if x["hotlink_ign"]]
autoplay = [x["file"] for x in issues if x["autoplay_video"]]

broken = []
link_re = re.compile(r'href="([^"]+)"')
for p in html:
    t = p.read_text(encoding="utf-8", errors="ignore")
    for href in link_re.findall(t):
        if href.startswith(("http", "mailto", "#", "//")):
            continue
        href2 = href.split("#")[0].split("?")[0]
        if not href2:
            continue
        if not (root / href2).exists():
            broken.append((p.name, href2))

checks = {
    "unique_titles": len({x["title"] for x in issues}) == len(issues),
    "unique_desc": len({x["desc"] for x in issues}) == len(issues),
    "all_titles": all(x["title"] for x in issues),
    "all_desc": all(x["desc_len"] for x in issues),
    "all_canon": all((x["canon"] or "").startswith("https://codcheats.net") for x in issues),
    "sitemap_complete": not (html_set - sm_names),
    "schema_all": all(x["schema"] >= 1 for x in issues),
    "alts": sum(x["img_no_alt"] for x in issues) == 0,
    "no_broken": len(set(broken)) == 0,
    "single_h1": len(bad_h1) == 0,
    "title_len_ok": len(long_title) == 0,
    "desc_len_ok": len(long_desc) == 0 and len(short_desc) == 0,
    "trust_depth": len(thin) == 0,
    "no_hotlink_ign": len(hotlink) == 0,
    "no_autoplay_heavy": len(autoplay) == 0,
    "blogs_30": sum(1 for x in issues if x["file"].startswith("blog-")) >= 30,
    "blogs_link_buy": all(x["internal_buy"] for x in issues if x["file"].startswith("blog-")),
    "lang_all": all(x["lang"] for x in issues),
    "no_zadeyo": all(not x["zadeyo"] for x in issues),
}

passed = sum(1 for v in checks.values() if v)
total = len(checks)
score = round(100 * passed / total)

out = {
    "score": score,
    "checks_passed": passed,
    "checks_total": total,
    "checks": checks,
    "bad_h1": bad_h1,
    "long_title": long_title,
    "long_desc": long_desc,
    "short_desc": short_desc,
    "thin": thin,
    "hotlink_ign": hotlink,
    "autoplay_video": autoplay,
    "broken": sorted(set(broken)),
    "html_files": len(html),
    "blog_posts": sum(1 for x in issues if x["file"].startswith("blog-")),
    "sitemap_urls": len(locs),
    "home_words": next(x["words"] for x in issues if x["file"] == "index.html"),
    "home_title_len": next(x["title_len"] for x in issues if x["file"] == "index.html"),
    "home_desc_len": next(x["desc_len"] for x in issues if x["file"] == "index.html"),
}

(root / "scripts" / "seo_audit_result.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
if score < 100:
    fails = [k for k, v in checks.items() if not v]
    print("FAILING:", fails)
