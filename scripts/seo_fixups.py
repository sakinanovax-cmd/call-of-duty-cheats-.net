# -*- coding: utf-8 -*-
"""One-shot SEO fixups: shorten titles, localize IGN images for blogs."""
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

SUBS = {
    "Call of Duty ESP Guide - Boxes, Skeletons, Distance | codcheats.net": "Call of Duty ESP Guide | codcheats.net",
    "Call of Duty Aimbot Settings - FOV, Smooth, Humanizer | codcheats.net": "Call of Duty Aimbot Settings | codcheats.net",
    "Call of Duty ESP Config Guide for Clean Overlays | codcheats.net": "Call of Duty ESP Config Guide | codcheats.net",
    "Cloud DMA on AWS for Call of Duty Cheats | codcheats.net": "Cloud DMA for Call of Duty Cheats | codcheats.net",
    "Undetected Warzone Cheats 2026 - Honest Meaning | codcheats.net": "Undetected Warzone Cheats 2026 | codcheats.net",
    "Free Warzone Hacks vs Paid Call of Duty Cheats | codcheats.net": "Free vs Paid Call of Duty Cheats | codcheats.net",
    "Warzone Ranked Call of Duty Aimbot Tips | codcheats.net": "Warzone Ranked Aimbot Tips | codcheats.net",
    "Warzone Resurgence Call of Duty Cheats Guide | codcheats.net": "Warzone Resurgence Cheats Guide | codcheats.net",
    "StreamProof for Call of Duty Cheats & Warzone | codcheats.net": "StreamProof Call of Duty Cheats | codcheats.net",
    "Call of Duty Multiplayer Cheats for PC | codcheats.net": "Call of Duty Multiplayer Cheats | codcheats.net",
    "Warzone DMA Call of Duty Cheats Explained | codcheats.net": "Warzone DMA Cheats Explained | codcheats.net",
    "Warzone Solos Call of Duty ESP Tips | codcheats.net": "Warzone Solos ESP Tips | codcheats.net",
    "Best Call of Duty Cheats for Beginners | codcheats.net": "Call of Duty Cheats for Beginners | codcheats.net",
    "Warzone Wallhack vs Call of Duty ESP | codcheats.net": "Warzone Wallhack vs ESP | codcheats.net",
    "Call of Duty Controller Aimbot & Gamepad Guide | codcheats.net": "Call of Duty Controller Aimbot | codcheats.net",
    "How RICOCHET Affects Call of Duty Cheats | codcheats.net": "RICOCHET and Call of Duty Cheats | codcheats.net",
    "Warzone Loadouts With Call of Duty ESP | codcheats.net": "Warzone Loadouts With ESP | codcheats.net",
    "MW3 Cheats PC with Call of Duty Multi-Game Suite | codcheats.net": "MW3 Cheats PC Multi-Game Guide | codcheats.net",
    "Call of Duty Cheats Pricing - $35 Monthly vs $150 Lifetime | codcheats.net": "Call of Duty Cheats Pricing Guide | codcheats.net",
    "Safe Habits After Buying Call of Duty Cheats | codcheats.net": "Safe Habits for Call of Duty Cheats | codcheats.net",
    "codcheats.net Call of Duty Cheats Setup Checklist | codcheats.net": "Call of Duty Cheats Setup Checklist | codcheats.net",
    "Warzone Radar & Compass Overlay Guide | codcheats.net": "Warzone Radar and Compass Guide | codcheats.net",
    "Warzone Loot ESP Guide - Plates, Ammo, Crates | codcheats.net": "Warzone Loot ESP Guide | codcheats.net",
    "Call of Duty Aimbot Guide for Warzone & MP | codcheats.net": "Call of Duty Aimbot Guide | codcheats.net",
    "How to Get Aimbot on Call of Duty PC | codcheats.net": "How to Get Aimbot on Call of Duty | codcheats.net",
}


def shorten_titles():
    p = ROOT / "scripts" / "blog_content.py"
    t = p.read_text(encoding="utf-8")
    for a, b in SUBS.items():
        if a in t:
            t = t.replace(a, b)
            print("title", len(b), b)
        else:
            print("miss", a[:48])
    p.write_text(t, encoding="utf-8")
    for m in re.findall(r'"([^"]*codcheats\.net)"', t):
        if len(m) > 65:
            print("STILL LONG", len(m), m)


def localize_ign():
    urls = [
        u.strip()
        for u in (ROOT / "scripts" / "ign_ok_urls.txt").read_text(encoding="utf-8").splitlines()
        if u.strip()
    ]
    out_dir = ROOT / "images" / "blog"
    out_dir.mkdir(parents=True, exist_ok=True)
    local = []
    ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.ign.com/",
        "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
    }
    for i, u in enumerate(urls):
        path = out_dir / f"ign-{i + 1:02d}.jpg"
        if path.exists() and path.stat().st_size > 5000:
            local.append(f"images/blog/{path.name}")
            print("keep", path.name)
            continue
        try:
            req = urllib.request.Request(u, headers=ua)
            data = urllib.request.urlopen(req, timeout=30).read()
            if len(data) < 5000:
                raise ValueError("tiny")
            path.write_bytes(data)
            local.append(f"images/blog/{path.name}")
            print("dl", path.name, len(data))
        except Exception as e:
            print("fail", i + 1, e)
            # fallback to already-local gameplay image
            gp = ROOT / "images" / "gameplay" / f"cod-{(i % 20) + 1:02d}.jpg"
            if gp.exists():
                local.append(f"images/gameplay/{gp.name}")
    (ROOT / "scripts" / "ign_local.txt").write_text("\n".join(local) + "\n", encoding="utf-8")
    print("local images", len(local))


if __name__ == "__main__":
    shorten_titles()
    localize_ign()
