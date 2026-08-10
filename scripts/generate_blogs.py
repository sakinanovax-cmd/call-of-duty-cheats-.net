# -*- coding: utf-8 -*-
"""Generate 30 COD blog posts with IGN images + internal links."""
from pathlib import Path
import xml.sax.saxutils as xu

ROOT = Path(__file__).resolve().parents[1]
BUY = "call-of-duty-cheats.html"
HOME = "index.html"
GUIDE = "guide.html"
BLOG = "blog.html"
PURCHASE = "https://zadeyo.com/go/SAKINA?to=%2Fproducts%2Fwarzone"
SUPPORT = "https://zadeyo.com/support"
LOGO = "https://zadeyo.com/_next/image?url=%2Frt-removebg-preview.png&w=64&q=75"

IGN = [
    {
        "src": "https://sm.ign.com/t/ign_sr/photo/default/call-of-duty-20241125160517-1732552253056_hnbr.1280.jpg",
        "alt": "Call of Duty Warzone gameplay scene",
        "credit": "https://www.ign.com/games/call-of-duty-warzone",
    },
    {
        "src": "https://sm.ign.com/t/ign_sr/photo/default/call-of-duty-20241125160601-1732552253057_mayy.1280.jpg",
        "alt": "Call of Duty Warzone operator action",
        "credit": "https://www.ign.com/games/call-of-duty-warzone",
    },
    {
        "src": "https://sm.ign.com/t/ign_sr/photo/default/call-of-duty-20241125160623-1732552253057_ne8z.1280.jpg",
        "alt": "Call of Duty Warzone combat screenshot",
        "credit": "https://www.ign.com/games/call-of-duty-warzone",
    },
    {
        "src": "https://sm.ign.com/t/ign_sr/photo/default/call-of-duty-20241125160633-1732552253058_ma7x.1280.jpg",
        "alt": "Call of Duty Warzone map fight",
        "credit": "https://www.ign.com/games/call-of-duty-warzone",
    },
    {
        "src": "https://sm.ign.com/t/ign_ap/gallery/c/call-of-du/call-of-duty-black-ops-6-terminator-crossover-images_stcv.1400.jpg",
        "alt": "Call of Duty Black Ops 6 promotional art from IGN",
        "credit": "https://www.ign.com/games/call-of-duty-black-ops-6",
    },
    {
        "src": "https://sm.ign.com/t/ign_ap/photo/default/bo6-season-02-announcement-072-1737572808944_994k.1280.jpg",
        "alt": "Black Ops 6 season announcement image",
        "credit": "https://www.ign.com/games/call-of-duty-black-ops-6",
    },
    {
        "src": "https://sm.ign.com/t/ign_ap/photo/default/bo6-season-02-announcement-070-1737572811068_q53v.1280.jpg",
        "alt": "Black Ops 6 season artwork",
        "credit": "https://www.ign.com/games/call-of-duty-black-ops-6",
    },
    {
        "src": "https://sm.ign.com/t/ign_sr/gallery/c/call-of-du/call-of-duty-black-ops-6-and-warzones-bloke-biter-shark-skin_yz96.1400.jpg",
        "alt": "Black Ops 6 and Warzone cosmetic screenshot",
        "credit": "https://www.ign.com/games/call-of-duty-black-ops-6",
    },
]

# slug, category, date, title, meta_title, meta_desc, h1, desc_card, keywords, related, body_html
POSTS = []


def p(*paras):
    return "\n".join(f"<p>{x}</p>" for x in paras)


def section(h2, *paras, h3=None, h3_paras=None, ul=None):
    parts = [f"<h2>{h2}</h2>"]
    parts.extend(f"<p>{x}</p>" for x in paras)
    if h3:
        parts.append(f"<h3>{h3}</h3>")
        parts.extend(f"<p>{x}</p>" for x in (h3_paras or []))
    if ul:
        parts.append("<ul>" + "".join(f"<li>{i}</li>" for i in ul) + "</ul>")
    return "\n".join(parts)


def add(slug, cat, date, title, meta_title, meta_desc, h1, card, keywords, related, body):
    POSTS.append(
        {
            "slug": slug,
            "cat": cat,
            "date": date,
            "title": title,
            "meta_title": meta_title,
            "meta_desc": meta_desc,
            "h1": h1,
            "card": card,
            "keywords": keywords,
            "related": related,
            "body": body,
        }
    )


# --- 30 posts with natural copy ---

add(
    "blog-aimbot",
    "aimbot",
    "Mar 12, 2026",
    "Call of Duty Aimbot Explained",
    "Call of Duty Aimbot Explained (Warzone Guide)",
    "A plain look at Call of Duty aimbot tools for Warzone: Aim Lock, Prediction, Visible Check, FOV, Smooth, and Humanizer.",
    "Call of Duty Aimbot Explained",
    "How Aim Lock, Prediction, Visible Check, and Humanizer work in real Warzone fights.",
    "cod aimbot, warzone aimbot, call of duty hacks",
    ["blog-aimbot-settings.html", "blog-working-aimbot-warzone.html", BUY],
    section(
        "What people mean by “cod aimbot”",
        "When someone says they want a call of duty aimbot, they usually mean help tracking players in messy gunfights — not a magic “win button.” In Warzone that means slides, knocks, third parties, and a lot of movement.",
        "Our Aimbot suite on the <a href='" + BUY + "'>Call of Duty cheats</a> page is built around control: Aim Priority, Aim Keys, Aim Lock, Prediction, Ignore Knocked, Visible Check, Draw FOV, FOV, Smooth, Max Distance, Target Bone, plus Humanizer tools.",
    )
    + section(
        "The settings that actually matter",
        "FOV decides how wide the aimbot looks. Smooth decides how hard it snaps. Prediction helps on moving targets. Visible Check keeps you from locking through full cover when you want cleaner fights.",
        "Humanizer is the quiet hero. Humanize Min/Max, Miss Factor, and Humanize Smooth add small natural misses so tracking does not look robotic on a killcam.",
        h3="Want presets?",
        h3_paras=[
            "Use our <a href='blog-aimbot-settings.html'>aimbot settings guide</a> next. Then pair it with <a href='blog-esp.html'>ESP</a> so you know who to shoot before you commit."
        ],
    ),
)

add(
    "blog-esp",
    "esp",
    "Mar 14, 2026",
    "Call of Duty ESP / Wallhack Explained",
    "Call of Duty ESP Explained — Cod Wallhack Basics",
    "Learn Call of Duty ESP the simple way: boxes, skeletons, health bars, snap lines, nicknames, weapons, and distance.",
    "Call of Duty ESP / Wallhack Explained",
    "Box, Skeleton, Health Bar, Snap Lines — what call of duty esp actually shows you.",
    "call of duty esp, cod wallhack, warzone hacks",
    ["blog-esp-config.html", "blog-loot-esp.html", BUY],
    section(
        "ESP in plain English",
        "Call of duty esp (people also search cod wallhack) draws enemy info through walls. You see where players are before you peek. That is it. No mystery.",
        "The live module includes Box, Filled Box, Skeleton, Health Bar, Snap Lines, Nicknames, Distance, Weapons, Show Team, thickness controls, and Max Distance. Full list sits on the <a href='" + BUY + "'>buy page</a>.",
    )
    + section(
        "Why Warzone players rely on it",
        "Warzone punishes bad information. Health bars tell you who is one shot. Weapons tell you if that push is stupid. Distance tells you whether to challenge or rotate.",
        "Keep Show Team set right in trios/quads so your squad does not look like enemies. Then fine-tune overlays in the <a href='blog-esp-config.html'>ESP config guide</a>.",
    ),
)

add(
    "blog-loot-esp",
    "esp",
    "Mar 18, 2026",
    "Warzone Loot ESP Explained",
    "Warzone Loot ESP Explained — Find Plates Fast",
    "Warzone loot ESP covers armor plates, heavy armor, ammo, gas masks, weapons, money, kill streaks, and crates.",
    "Warzone Loot ESP Explained",
    "Armor, ammo, gas masks, crates — loot faster in BR and Resurgence.",
    "warzone loot esp, warzone hacks, call of duty cheats",
    ["blog-esp.html", "blog-resurgence-hacks.html", BUY],
    section(
        "Loot ESP is a time saver",
        "Most Warzone deaths after a win streak happen because you looted slow. Loot ESP highlights Armor Plate, Heavy Armor, Ammo, Gas Mask, Weapon, Money, Kill Streak, and Crates.",
        "Limit Distance and Custom Colors keep the screen readable. Same options are listed under Loot ESP on our <a href='" + BUY + "'>Call of Duty cheats</a> plans.",
    )
    + section(
        "Where it shines",
        "Resurgence and hot drops. You land, grab plates, swap guns, and leave. Pair it with <a href='blog-radar-compass.html'>radar/compass</a> so you are not looting while a team holds high ground.",
    ),
)

add(
    "blog-radar-compass",
    "esp",
    "Mar 20, 2026",
    "Warzone Radar & Compass Overlay Explained",
    "Warzone Radar Hack Style Overlay Explained",
    "Compass FOV, radius sync, team filters, distance, and size settings for a cleaner Warzone radar overlay.",
    "Warzone Radar & Compass Overlay Explained",
    "A cleaner warzone radar hack style overlay for rotates and third parties.",
    "warzone radar hack, call of duty radar overlay, warzone cheats",
    ["blog-esp.html", "blog-warzone-solos.html", BUY],
    section(
        "Why compass beats a busy screen",
        "Full ESP is great. Sometimes you just want direction. Radar/Compass gives Enable, Enable Compass, Compass Radius Sync, Compass FOV, Show Team, Show Distance, Compass Size, and Max Distance.",
        "That is the warzone radar hack style info people want — without covering the whole HUD.",
    )
    + section(
        "Simple setup tip",
        "Start small on Compass Size. Turn Show Distance on. Cap Max Distance so far noise disappears. More detail lives on <a href='" + BUY + "'>codcheats.net pricing</a> and the <a href='blog-esp-config.html'>ESP guide</a>.",
    ),
)

add(
    "blog-aimbot-settings",
    "aimbot",
    "Mar 24, 2026",
    "Aimbot Settings Guide for Warzone & COD",
    "Warzone Aimbot Settings Guide — FOV & Humanizer",
    "Practical Warzone aimbot settings: FOV, Smooth, Target Bone, Visible Check, Ignore Knocked, and Humanizer presets.",
    "Aimbot Settings Guide for Warzone & COD",
    "FOV, Smooth, Humanizer, and bone presets that do not look ridiculous.",
    "how to get aimbot on call of duty, warzone aimbot, cod silent aim",
    ["blog-aimbot.html", "blog-humanizer-aim.html", BUY],
    section(
        "Start boring. Then tune.",
        "Turn Aimbot on. Bind Aim Keys. Enable Draw FOV so you can see the circle. Keep FOV medium. Raise Smooth until tracking feels calm.",
        "Target Bone on chest is safer than head for long sprays. Visible Check on. Ignore Knocked on in battle royale. On Team off when you only want enemies.",
    )
    + section(
        "Humanizer preset that feels human",
        "Enable Humanizer. Keep Humanize Min/Max close together. Add a light Miss Factor. Leave Humanize Smooth above zero.",
        "Gamepad players: Misc includes Gamepad Support. Use a bit more Smooth on stick aim. Full option names are on the <a href='" + BUY + "'>feature list</a>.",
        ul=[
            "Read <a href='blog-aimbot.html'>Aimbot Explained</a> if terms feel new",
            "Add <a href='blog-esp-config.html'>ESP presets</a> after aim feels right",
            "Use <a href='blog-cloud-dma.html'>Cloud DMA</a> notes before first load",
        ],
    ),
)

add(
    "blog-esp-config",
    "esp",
    "Mar 26, 2026",
    "ESP Configuration Guide — Box, Skeleton & Distances",
    "COD ESP Config Guide — Clean Warzone Overlays",
    "Configure Call of Duty ESP with box, skeleton, health bars, snap lines, thickness, and max distance for clean overlays.",
    "ESP Configuration Guide — Box, Skeleton & Distances",
    "Readable Warzone overlays without turning your screen into soup.",
    "cod external esp, call of duty esp, warzone cheats",
    ["blog-esp.html", "blog-loot-esp.html", BUY],
    section(
        "Pick one main shape",
        "Box or Skeleton. Not both at max thickness. Add Health Bar. Turn Distance and Weapons on. Nicknames help in sweaty lobbies.",
        "Show Team matters in squads. Max Distance should match the mode — short for small maps, longer for big BR rotates.",
    )
    + section(
        "Thickness tip",
        "If the overlay feels loud, drop Box Thickness, Line Thickness, and Skeleton Thickness. Snap Lines help in buildings; turn them off if they stress you out.",
        "When you are happy with player ESP, layer <a href='blog-loot-esp.html'>Loot ESP</a> and check plans on <a href='" + BUY + "'>Call of Duty cheats</a>.",
    ),
)

add(
    "blog-cloud-dma",
    "safety",
    "Apr 2, 2026",
    "How Cloud DMA & AWS Work for COD Cheats",
    "Warzone DMA Cheats — Cloud DMA on AWS Explained",
    "Cloud DMA for Call of Duty cheats explained simply: AWS hosting, why full features need it, and how it fits RICOCHET-era PC setups.",
    "How Cloud DMA & AWS Work for COD Cheats",
    "Why full Warzone features need Cloud DMA hosted on AWS — one path, not two random products.",
    "warzone dma cheats, cod bypass anti cheat, undetected warzone cheats 2026",
    ["guide.html", "blog-dma-cheats.html", BUY],
    section(
        "One delivery path",
        "You will see CLOUD-DMA and AWS on the product page. That is the same hosted delivery path. Cloud DMA runs the heavy work on AWS. It is not two separate cheats.",
        "Full Aimbot, ESP, Loot ESP, and Radar need that connection. We say that clearly on the <a href='" + BUY + "'>system requirements</a>.",
    )
    + section(
        "Still turn Windows security on",
        "HVCI, Core Isolation, TPM, Secure Boot — keep them ON. Cloud DMA does not replace those checks.",
        "For anti-cheat context, read <a href='" + GUIDE + "'>what anti-cheat Call of Duty uses</a>. For hardware bans, see the <a href='blog-hwid-spoofer.html'>HWID spoofer article</a>.",
    ),
)

add(
    "blog-hwid-spoofer",
    "spoofing",
    "Apr 5, 2026",
    "What Is an HWID Spoofer? (COD / Warzone)",
    "HWID Spoofer for Warzone Explained Simply",
    "What an HWID spoofer does after a Warzone hardware ban, and why suite-level spoofing keeps Call of Duty cheats usable.",
    "What Is an HWID Spoofer? (COD / Warzone)",
    "Hardware bans, fingerprints, and why spoofing keeps a cheat from feeling useless.",
    "warzone spoofer free, how to avoid hwid ban warzone, warzone cleaner for ban evasion",
    ["blog-cloud-dma.html", "blog-shadow-ban.html", BUY],
    section(
        "HWID in normal words",
        "Games can remember more than your account. They can remember machine details. If those get flagged, a fresh account on the same PC may still bounce.",
        "An HWID spoofer refreshes those identifiers so the ban fingerprint is less sticky. People search “how to avoid hwid ban warzone” after that exact headache.",
    )
    + section(
        "Why the suite includes it",
        "A cheat with no recovery path feels dead after a hardware hit. Our suite provides spoofer support so access stays usable. Pair it with updates and <a href='blog-cloud-dma.html'>Cloud DMA</a>.",
        "Need help after purchase? Use the <a href='" + SUPPORT + "'>support channel</a>. Plans stay on <a href='" + BUY + "'>codcheats.net</a>.",
    ),
)

add(
    "blog-comparison",
    "comparison",
    "Apr 8, 2026",
    "Best Call of Duty Cheat Review & Comparison 2026",
    "Best Undetectable COD Warzone Cheats 2026 Review",
    "Premium Call of Duty cheats vs free Warzone hacks in 2026 — updates, Humanizer, StreamProof, Cloud DMA, support, and price.",
    "Best Call of Duty Cheat Review & Comparison 2026",
    "Paid suite vs free leaks vs generic tools — what still holds up in 2026.",
    "best undetectable cod warzone cheats, best warzone cheat providers, cheapest cod aimbot",
    ["blog-free-vs-paid.html", "blog-undetected-warzone-2026.html", BUY],
    section(
        "The real scorecard",
        "“Best” is not a logo. It is update speed, feature depth, StreamProof, support, and clear Cloud DMA delivery. Free warzone hacks fail that test fast when RICOCHET patches land.",
        "Our Monthly plan is $35. Lifetime is $150. Same features on both. Lifetime keeps permanent access and future updates. See the live list on <a href='" + BUY + "'>Call of Duty cheats</a>.",
    )
    + """
<table class="compare-table">
<thead><tr><th>Factor</th><th>This suite</th><th>Free leaks</th><th>Generic paid</th></tr></thead>
<tbody>
<tr><td>Updates</td><td>2–4h typical</td><td>Often dead</td><td>Hit or miss</td></tr>
<tr><td>Aimbot</td><td>Humanizer + Prediction + Visible Check</td><td>Basic/broken</td><td>Often shallow</td></tr>
<tr><td>Vision</td><td>ESP + Loot ESP + Radar</td><td>Partial</td><td>ESP only common</td></tr>
<tr><td>StreamProof</td><td>Yes</td><td>Rare</td><td>Maybe</td></tr>
<tr><td>Delivery</td><td>Cloud DMA on AWS</td><td>Risky cracks</td><td>Unclear loaders</td></tr>
<tr><td>Support</td><td>24/7 channel</td><td>None</td><td>Slow tickets</td></tr>
</tbody></table>
"""
    + section(
        "Next reads",
        "Also see <a href='blog-free-vs-paid.html'>free vs paid</a> and the <a href='blog-checklist-undetected.html'>undetected checklist</a>.",
    ),
)

add(
    "blog-how-to-get-aimbot",
    "aimbot",
    "Apr 10, 2026",
    "How to Get Aimbot on Call of Duty (PC)",
    "How to Get Aimbot on Call of Duty — PC Steps",
    "Simple PC steps for how to get aimbot on Call of Duty: buy access, set Windows security, connect Cloud DMA, then tune FOV and Humanizer.",
    "How to Get Aimbot on Call of Duty (PC)",
    "The actual PC path people mean when they Google how to get aimbot on call of duty.",
    "how to get aimbot on call of duty, call of duty hack download, warzone aimbot",
    ["blog-aimbot-settings.html", "blog-install-without-ban.html", BUY],
    section(
        "Skip the shady “free download” maze",
        "If your search was “how to get aimbot on call of duty,” you have seen a hundred fake download buttons. Most are malware. The clean path is a maintained private suite with a real loader and support.",
        "On <a href='" + HOME + "'>codcheats.net</a> you start from the <a href='" + BUY + "'>buy page</a>, pick Monthly or Lifetime, then finish checkout on the store redirect.",
    )
    + section(
        "After you pay",
        "Download the loader from your order page. Turn on HVCI, Core Isolation, TPM, and Secure Boot. Connect Cloud DMA. Launch Warzone or your COD title. Enable Aimbot and set Aim Keys.",
        "Tune with the <a href='blog-aimbot-settings.html'>settings guide</a>. If Windows blocks something, ping <a href='" + SUPPORT + "'>support</a> instead of random Discord “fixes.”",
    ),
)

add(
    "blog-undetected-warzone-2026",
    "safety",
    "Apr 12, 2026",
    "Undetected Warzone Cheats 2026 — What That Means",
    "Undetected Warzone Cheats 2026 — Honest Take",
    "What undetected Warzone cheats 2026 really means under RICOCHET: fast updates, Cloud DMA, Humanizer, and sane settings — not forever immunity.",
    "Undetected Warzone Cheats 2026 — What That Means",
    "No cheat is magic forever. Here is what “undetected” should mean this year.",
    "undetected warzone cheats 2026, safest call of duty hack, free warzone hacks undetected 2026",
    ["blog-comparison.html", "guide.html", BUY],
    section(
        "Let’s be straight",
        "“Undetected forever” is marketing fluff. RICOCHET changes. What you want in 2026 is a build that gets patched in a 2–4 hour window, uses Cloud DMA on AWS, and gives you Humanizer + Visible Check so you are not playing like a bot.",
        "That is the standard we publish on <a href='" + BUY + "'>Call of Duty cheats</a> and explain in the <a href='" + GUIDE + "'>RICOCHET guide</a>.",
    )
    + section(
        "Red flags on other sites",
        "Free warzone hacks undetected 2026 posts with 40 download mirrors. No system requirements. No feature list. No support. Walk away.",
        "Want a checklist? Use <a href='blog-checklist-undetected.html'>this undetected checklist</a>.",
    ),
)

add(
    "blog-free-vs-paid",
    "comparison",
    "Apr 14, 2026",
    "Free Warzone Hacks vs Paid Call of Duty Cheats",
    "Free Warzone Hacks vs Paid COD Cheats",
    "Free Warzone hacks vs paid Call of Duty cheats: malware risk, dead updates, missing Humanizer/StreamProof, and why price is not the only cost.",
    "Free Warzone Hacks vs Paid Call of Duty Cheats",
    "Why “free” often costs an account — and what paid suites actually buy you.",
    "free warzone hacks undetected 2026, warzone 2 cheats free, call of duty hack download",
    ["blog-comparison.html", "blog-how-to-get-aimbot.html", BUY],
    section(
        "Free usually means unfinished",
        "Free leaks miss updates. They miss StreamProof. They miss a real Cloud DMA path. They also love stuffing your PC with junk.",
        "Paid access on <a href='" + BUY + "'>codcheats.net</a> is $35 a month or $150 lifetime for the full Aimbot, ESP, Loot ESP, Radar, Misc, and Cloud DMA suite.",
    )
    + section(
        "When free searches make sense",
        "People type warzone 2 cheats free when they are broke or curious. Fair. Just know the failure rate is ugly. Read <a href='blog-comparison.html'>the 2026 comparison</a> before you gamble an Activision account.",
    ),
)

add(
    "blog-install-without-ban",
    "safety",
    "Apr 16, 2026",
    "How to Install Warzone Cheats Without Instant Trouble",
    "How to Install Warzone Cheats Without Ban Risk Spikes",
    "Practical setup tips for installing Warzone cheats: Windows trust settings, Cloud DMA, Humanizer, StreamProof, and update habits.",
    "How to Install Warzone Cheats Without Instant Trouble",
    "Setup habits that lower dumb mistakes when people ask how to install warzone cheats without ban.",
    "how to install warzone cheats without ban, safest call of duty hack, cod bypass anti cheat",
    ["blog-cloud-dma.html", "blog-aimbot-settings.html", BUY],
    section(
        "There is no “ban-proof” button",
        "Anyone promising zero risk is lying. What you can do is avoid obvious mistakes: outdated builds, max FOV rage settings, and skipping Windows requirements.",
    )
    + section(
        "Install habits that help",
        ul=[
            "Buy a maintained suite from the <a href='" + BUY + "'>official plans page</a>",
            "Enable HVCI, Core Isolation, TPM, Secure Boot",
            "Connect Cloud DMA before expecting full features — see <a href='blog-cloud-dma.html'>this guide</a>",
            "Use Humanizer + Visible Check from day one",
            "Turn StreamProof on if you broadcast",
            "Update after every COD patch (we target 2–4 hours)",
        ],
        h3="More reading",
        h3_paras=[
            "Shadowban confusion: <a href='blog-shadow-ban.html'>how to think about Warzone shadow bans</a>. Spoofing: <a href='blog-hwid-spoofer.html'>HWID basics</a>."
        ],
    ),
)

add(
    "blog-working-aimbot-warzone",
    "aimbot",
    "Apr 18, 2026",
    "Is There a Working Aimbot for Warzone Right Now?",
    "Is There a Working Aimbot for Warzone in 2026?",
    "Yes — maintained private suites still ship working Warzone aimbot tools with Humanizer, Prediction, and Cloud DMA after RICOCHET patches.",
    "Is There a Working Aimbot for Warzone Right Now?",
    "Short answer for anyone typing is there a working aimbot for warzone.",
    "is there a working aimbot for warzone, warzone aimbot, undetected warzone cheats 2026",
    ["blog-aimbot.html", "blog-undetected-warzone-2026.html", BUY],
    section(
        "Short answer",
        "Yes — if it is maintained. Public free aimbots die constantly. Private suites that update in a few hours after patches are the ones people keep using.",
        "Our current Aimbot module is listed live on <a href='" + BUY + "'>Call of Duty cheats</a>: Aim Lock, Prediction, Visible Check, Humanizer, the whole set.",
    )
    + section(
        "How to tell it is actually working",
        "Loader opens. Cloud DMA connects. Draw FOV shows. Tracking follows your Aim Keys. After a game update, wait for the 2–4 hour patch window instead of forcing an old build.",
        "Setup help: <a href='blog-how-to-get-aimbot.html'>how to get aimbot on Call of Duty</a>.",
    ),
)

add(
    "blog-how-much-cheats-cost",
    "comparison",
    "Apr 20, 2026",
    "How Much Do Warzone Cheats Cost in 2026?",
    "How Much Do Warzone Cheats Cost?",
    "Warzone cheat pricing in 2026: our Monthly plan is $35 and Lifetime is $150 with full feature parity — Aimbot, ESP, Loot ESP, Radar, Cloud DMA.",
    "How Much Do Warzone Cheats Cost in 2026?",
    "Clear numbers for how much do warzone cheats cost — no bait tiers.",
    "how much do warzone cheats cost, cheapest cod aimbot, best warzone cheat providers",
    ["blog-comparison.html", BUY, "blog-free-vs-paid.html"],
    section(
        "Our prices",
        "Monthly: <strong>$35</strong> for 31 days. Lifetime: <strong>$150</strong> once. Same features. Lifetime adds permanent access and future updates.",
        "That covers Aimbot, ESP, Loot ESP, Radar/Compass, Misc (including StreamProof and Gamepad Support), and Cloud DMA on AWS. Details: <a href='" + BUY + "'>pricing page</a>.",
    )
    + section(
        "What cheaper usually cuts",
        "Dirt-cheap “cheapest cod aimbot” ads often cut Humanizer, loot tools, compass, or support. You pay again when it breaks. Lifetime here exists so you are not renting forever if you play all year.",
    ),
)

add(
    "blog-shadow-ban",
    "safety",
    "Apr 22, 2026",
    "Warzone Shadow Ban — What Players Actually Mean",
    "How to Remove Shadow Ban Warzone — Clear Guide",
    "What a Warzone shadow ban feels like, why people search how to remove shadow ban warzone, and practical next steps around accounts and HWID.",
    "Warzone Shadow Ban — What Players Actually Mean",
    "Skill-based weird lobbies vs real restrictions — and what to do next.",
    "how to remove shadow ban warzone, why was i banned from warzone for no reason, how to report hackers in call of duty",
    ["blog-hwid-spoofer.html", "blog-report-hackers.html", GUIDE],
    section(
        "Shadow ban is a messy word",
        "Sometimes it means weird lobby quality. Sometimes it means restricted matchmaking after reports. Sometimes people say “banned for no reason” when a wave just hit.",
        "If your account is fully banned, that is different from a temporary matchmaking flag. Activision support paths and waiting out a restriction are still the official account routes.",
    )
    + section(
        "If hardware is involved",
        "Hardware-linked hits are why players read about spoofers. See <a href='blog-hwid-spoofer.html'>HWID spoofer explained</a>. For anti-cheat background, open the <a href='" + GUIDE + "'>RICOCHET guide</a>.",
        "If you still want private tools after you sort access, the suite lives on <a href='" + BUY + "'>codcheats.net/call-of-duty-cheats</a>.",
    ),
)

add(
    "blog-ranked-hacks",
    "aimbot",
    "Apr 24, 2026",
    "Warzone Ranked Hacks — Play Smarter, Not Louder",
    "Warzone Ranked Hacks Guide for PC",
    "Warzone ranked hacks tips: smaller FOV, Humanizer, Visible Check, StreamProof, and why rage settings get you watched faster.",
    "Warzone Ranked Hacks — Play Smarter, Not Louder",
    "Ranked is sweaty. Your settings should be quieter than pubs.",
    "warzone ranked hacks, call of duty ranked play cheats, warzone aimbot",
    ["blog-aimbot-settings.html", "blog-stream-proof.html", BUY],
    section(
        "Ranked is where people watch demos",
        "If you run call of duty ranked play cheats like a rage cheat video, you will look loud. Keep FOV tighter. Keep Smooth higher. Keep Humanizer on. Visible Check on.",
        "StreamProof stays on if you stream ranked. Lobby Stats in Misc helps you read the lobby before the match gets stupid.",
    )
    + section(
        "Tools that help ranked decision-making",
        "ESP distance + weapons. Compass for flanks. Ignore Knocked so you finish the player still shooting. Loadouts and plans: <a href='" + BUY + "'>Call of Duty cheats</a>.",
    ),
)

add(
    "blog-multiplayer-cheats",
    "aimbot",
    "Apr 26, 2026",
    "Call of Duty Multiplayer Cheats (MW / BO)",
    "Call of Duty Multiplayer Cheats for PC",
    "Call of Duty multiplayer cheats for MW2, MW3, BO6, and BO7 on one multi-game suite with Aimbot, ESP, StreamProof, and Cloud DMA.",
    "Call of Duty Multiplayer Cheats (MW / BO)",
    "One suite for multiplayer nights — not only battle royale.",
    "call of duty multiplayer cheats, black ops 6 cheats xbox, cod cold war cheats pc",
    ["blog-black-ops-6-cheats.html", "blog-mw2-mw3-hacks.html", BUY],
    section(
        "Multiplayer is a different rhythm",
        "Maps are smaller. Spawns recycle. ESP Max Distance can stay shorter. Aimbot FOV can stay modest because fights are closer.",
        "Our Multi-Game Support covers Warzone, MW2, MW3, BO6, and BO7 on Steam, Battle.net, and Microsoft Store. That is listed on the <a href='" + BUY + "'>buy page</a>.",
    )
    + section(
        "Note on consoles",
        "This site is about PC software. Searches like black ops 6 cheats xbox or warzone hacks ps4 no jailbreak are common, but our loader path is Windows + Cloud DMA.",
    ),
)

add(
    "blog-resurgence-hacks",
    "esp",
    "Apr 28, 2026",
    "Warzone Resurgence Hacks — Loadout Speed Wins",
    "Warzone Resurgence Hacks Guide",
    "Warzone Resurgence hacks that matter: Loot ESP for plates, Compass for spawns, Aimbot Ignore Knocked, and fast rotates.",
    "Warzone Resurgence Hacks — Loadout Speed Wins",
    "Resurgence is pace. These modules match that pace.",
    "warzone resurgence hacks, warzone loot esp, warzone radar hack",
    ["blog-loot-esp.html", "blog-radar-compass.html", BUY],
    section(
        "Resurgence rewards info + speed",
        "You respawn a lot. Bad loot paths waste those lives. Turn on Armor Plate, Ammo, Weapon, and Crates in Loot ESP. Keep Limit Distance tight so the island stays readable.",
        "Compass helps when teams land on your building from the next gulag wave. Aimbot Ignore Knocked stops you wasting aim on downed bodies while a third party cracks you.",
    )
    + section(
        "Grab the suite",
        "Feature names and pricing: <a href='" + BUY + "'>codcheats.net</a>. More loot detail: <a href='blog-loot-esp.html'>Loot ESP explained</a>.",
    ),
)

add(
    "blog-silent-aim",
    "aimbot",
    "Apr 30, 2026",
    "COD Silent Aim vs Normal Aim Lock",
    "COD Silent Aim Explained in Simple Words",
    "What players mean by COD silent aim, how it differs from visible Aim Lock/FOV aimbot styles, and how Humanizer changes the feel.",
    "COD Silent Aim vs Normal Aim Lock",
    "People search cod silent aim — here is the practical difference in feel.",
    "cod silent aim, warzone aimbot, call of duty trigger bot",
    ["blog-aimbot.html", "blog-humanizer-aim.html", BUY],
    section(
        "What players are asking for",
        "“Silent aim” usually means bullets or targeting that does not show a huge obvious snap. Folks also confuse it with trigger bot searches. Our published suite focuses on Aim Lock, FOV, Smooth, Prediction, and Humanizer — the controls listed on <a href='" + BUY + "'>the feature page</a>.",
    )
    + section(
        "How to get a quieter feel anyway",
        "Lower FOV. Higher Smooth. Humanizer on. Miss Factor lightly on. Do not film rage clips if you care about reports. Read <a href='blog-aimbot-settings.html'>settings</a> next.",
    ),
)

add(
    "blog-stream-proof",
    "safety",
    "May 2, 2026",
    "StreamProof Warzone Cheats — Stream Without Flashing ESP",
    "Stream Proof Warzone Cheats Explained",
    "StreamProof hides Call of Duty cheat overlays from OBS and Discord capture so Warzone streams do not flash ESP or FOV rings.",
    "StreamProof Warzone Cheats — Stream Without Flashing ESP",
    "OBS-friendly overlay hiding for creators who still run tools.",
    "warzone hacks, stream proof, call of duty cheats",
    ["blog-ranked-hacks.html", "blog-esp-config.html", BUY],
    section(
        "Why StreamProof exists",
        "ESP boxes on stream are an instant report magnet. Misc on our suite includes StreamProof so overlays stay off OBS, Discord, and common capture tools.",
        "Turn it on before you go live. Test a private stream first. Then play. Feature sits with Lobby Stats, Gamepad Support, and Multi-Game Support on <a href='" + BUY + "'>the buy page</a>.",
    )
    + section(
        "Creator tip",
        "Even with StreamProof, keep aim settings human. Viewers may not see ESP, but crazy flicks still look wrong. Pair with <a href='blog-humanizer-aim.html'>Humanizer notes</a>.",
    ),
)

add(
    "blog-black-ops-6-cheats",
    "aimbot",
    "May 4, 2026",
    "Black Ops 6 Cheats for PC — Multi-Game Suite",
    "Black Ops 6 Cheats PC — Aimbot & ESP",
    "Black Ops 6 cheats on PC through a multi-game Call of Duty suite: Aimbot, ESP, StreamProof, Cloud DMA, shared with Warzone and BO7.",
    "Black Ops 6 Cheats for PC — Multi-Game Suite",
    "BO6 nights without buying a second random loader.",
    "black ops 6 cheats xbox, call of duty multiplayer cheats, cod aimbot",
    ["blog-multiplayer-cheats.html", "blog-mw2-mw3-hacks.html", BUY],
    section(
        "BO6 on the same build",
        "You do not need a sketchy “BO6 only” crack. Multi-Game Support on our Call of Duty suite includes Black Ops 6 with the same Aimbot and ESP modules.",
        "PC only here — Windows, Cloud DMA, the requirements on <a href='" + BUY + "'>codcheats.net</a>. Console searches are common; this software path is not for consoles.",
    )
    + section(
        "After a BO6 patch",
        "Wait for the update window. We aim for 2–4 hours. Forcing an old build is how people brick a night. Status help: <a href='" + SUPPORT + "'>support</a>.",
    ),
)

add(
    "blog-mw2-mw3-hacks",
    "aimbot",
    "May 6, 2026",
    "Modern Warfare 2 & MW3 Hacks on PC",
    "Call of Duty Modern Warfare 2 Hacks (PC)",
    "Call of Duty Modern Warfare 2 hacks and MW3 PC support inside one multi-game cheat suite with Aimbot, ESP, and Cloud DMA.",
    "Modern Warfare 2 & MW3 Hacks on PC",
    "Still hopping into MW2/MW3? Multi-game support has you.",
    "call of duty modern warfare 2 hacks, cod modern warfare 2 hacks ps4, warzone 2 hacks ps5",
    ["blog-multiplayer-cheats.html", "blog-black-ops-6-cheats.html", BUY],
    section(
        "Older modern titles still get playtime",
        "Not everyone lives in the newest battle pass. MW2 and MW3 are covered under Multi-Game Support with Warzone, BO6, and BO7.",
        "Same Aimbot suite. Same ESP suite. Same Cloud DMA requirement. See <a href='" + BUY + "'>plans</a>.",
    )
    + section(
        "PC vs console wording",
        "Search boxes show cod modern warfare 2 hacks ps4 and warzone 2 hacks ps5 a lot. Those are different platforms. Our guides and loader are for Windows PC.",
    ),
)

add(
    "blog-ricochet-players",
    "safety",
    "May 8, 2026",
    "RICOCHET Anti-Cheat for Normal Players",
    "Do Call of Duty Hacks Actually Work Under RICOCHET?",
    "Do Call of Duty hacks actually work under RICOCHET? A plain guide to the kernel driver, updates, and why maintained Cloud DMA suites matter.",
    "RICOCHET Anti-Cheat for Normal Players",
    "A non-robot explanation of RICOCHET — and the “do hacks still work?” question.",
    "do call of duty hacks actually work, cod bypass anti cheat, how to hack call of duty warzone",
    ["guide.html", "blog-undetected-warzone-2026.html", BUY],
    section(
        "What RICOCHET is",
        "RICOCHET is Call of Duty’s anti-cheat. On PC it includes a kernel-level driver while the game runs, plus server-side checks. We break that down properly on the <a href='" + GUIDE + "'>guide page</a>.",
    )
    + section(
        "So… do hacks still work?",
        "Maintained private tools still exist. Public junk usually does not last. Success depends on update speed, delivery (Cloud DMA on AWS for our suite), and how loud your settings are.",
        "If you came from “how to hack call of duty warzone,” start at <a href='" + HOME + "'>codcheats.net</a> and read <a href='blog-install-without-ban.html'>install habits</a> before you load anything.",
    ),
)

add(
    "blog-dma-cheats",
    "safety",
    "May 10, 2026",
    "Warzone DMA Cheats — Simple Explanation",
    "Warzone DMA Cheats Explained for Beginners",
    "Warzone DMA cheats explained without jargon overload: what DMA means, why Cloud DMA on AWS is our full-feature path, and who it is for.",
    "Warzone DMA Cheats — Simple Explanation",
    "DMA sounds scary. Here it is in normal English.",
    "warzone dma cheats, kernel level driver cod hack, external aimbot warzone undetected",
    ["blog-cloud-dma.html", "guide.html", BUY],
    section(
        "DMA = reading memory a different way",
        "DMA stands for Direct Memory Access. In cheat talk it means reading game data through a path that is not a basic free injector from 2018.",
        "Our product’s full functionality needs Cloud DMA hosted on AWS. Details: <a href='blog-cloud-dma.html'>Cloud DMA & AWS</a>.",
    )
    + section(
        "Is it “external”?",
        "People search external aimbot warzone undetected because they want less fragile setups. Cloud DMA is the external processing model we document. Requirements still include Secure Boot and friends on <a href='" + BUY + "'>the buy page</a>.",
    ),
)

add(
    "blog-humanizer-aim",
    "aimbot",
    "May 12, 2026",
    "Warzone Cheat With Humanized Aim — Why It Matters",
    "Warzone Cheat With Humanized Aim Explained",
    "Why a Warzone cheat with humanized aim matters: Humanizer, Humanize Min/Max, Miss Factor, and Humanize Smooth on our Aimbot suite.",
    "Warzone Cheat With Humanized Aim — Why It Matters",
    "Perfect tracking looks fake. Humanizer fixes the vibe.",
    "warzone cheat with humanized aim, cod aimbot, warzone aimbot",
    ["blog-aimbot.html", "blog-aimbot-settings.html", BUY],
    section(
        "Killcams tell on you",
        "Machine-perfect aim is obvious. Humanizer exists so Aim Lock can still help without looking like a script every time.",
        "Controls: Humanizer, Humanize Min/Max, Miss Factor, Humanize Smooth. Listed under Aimbot on <a href='" + BUY + "'>Call of Duty cheats</a>.",
    )
    + section(
        "A simple starting point",
        "Enable Humanizer. Small Min/Max gap. Low Miss Factor. Keep Humanize Smooth on. Then fight five games before you touch anything else. Full walkthrough: <a href='blog-aimbot-settings.html'>settings guide</a>.",
    ),
)

add(
    "blog-warzone-solos",
    "esp",
    "May 14, 2026",
    "Warzone Solos Hack Tips — Info Wins 1v1s",
    "Warzone Solos Hack Guide",
    "Warzone solos hack tips using ESP distance, Compass, Loot ESP plates, and quieter Aimbot FOV for 1v1 map control.",
    "Warzone Solos Hack Tips — Info Wins 1v1s",
    "Solos is information. These modules match that mode.",
    "warzone solos hack, warzone cheats, call of duty battle royale cheats",
    ["blog-radar-compass.html", "blog-esp-config.html", BUY],
    section(
        "Solos changes your overlay",
        "No teammates to cover a bad peek. ESP Distance and Weapons matter more. Compass helps you avoid walking into two separate players.",
        "Loot ESP for plates and gas masks keeps you alive through late circles. Keep Aimbot FOV smaller than quads — you do not need a huge magnet.",
    )
    + section(
        "Load the suite",
        "Everything named above is on <a href='" + BUY + "'>codcheats.net</a>. Config help: <a href='blog-esp-config.html'>ESP configuration</a>.",
    ),
)

add(
    "blog-plunder-hacks",
    "esp",
    "May 16, 2026",
    "Warzone Plunder Hacks — Money and Chaos",
    "Warzone Plunder Hacks Guide",
    "Warzone Plunder hacks focused on Loot ESP money markers, Compass pressure, and Aimbot settings for chaotic cash modes.",
    "Warzone Plunder Hacks — Money and Chaos",
    "Plunder is loud. Your loot filters should be louder for cash.",
    "warzone plunder hacks, warzone loot esp, call of duty battle royale cheats",
    ["blog-loot-esp.html", "blog-resurgence-hacks.html", BUY],
    section(
        "Play Plunder like a loot route",
        "Money and Weapon markers in Loot ESP matter more here. Crates too. Limit Distance so you are not tracking junk across the map.",
        "Compass helps when every contract turns into a third party. Aimbot Prediction helps on vehicles and sprinting targets.",
    )
    + section(
        "Same product page",
        "No special “Plunder only” myth product — it is the same <a href='" + BUY + "'>Call of Duty cheats</a> suite. Read <a href='blog-loot-esp.html'>Loot ESP</a> for filter detail.",
    ),
)

add(
    "blog-report-hackers",
    "safety",
    "May 18, 2026",
    "How to Report Hackers in Call of Duty",
    "How to Report Hackers in Call of Duty",
    "How to report hackers in Call of Duty from the in-game scoreboard, plus why report waves happen and how that ties to RICOCHET.",
    "How to Report Hackers in Call of Duty",
    "Legit report steps — and why this page still links our tool guides.",
    "how to report hackers in call of duty, why was i banned from warzone for no reason, do call of duty hacks actually work",
    ["guide.html", "blog-shadow-ban.html", "blog-ricochet-players.html"],
    section(
        "Reporting is simple",
        "Open the scoreboard, highlight the player, report, pick the cheating reason, send it. That is the normal Call of Duty path. You can also use Activision’s support site for account issues.",
        "Reports feed into RICOCHET systems. That is why loud cheat settings get people banned in waves. Background reading: <a href='" + GUIDE + "'>RICOCHET guide</a>.",
    )
    + section(
        "Why this is on a cheat blog",
        "Because both sides search the same keywords. If you are here for tools, stay on maintained builds and human settings. Start at <a href='" + HOME + "'>codcheats.net</a> and the <a href='" + BUY + "'>buy page</a>. If you got restricted and feel confused, read <a href='blog-shadow-ban.html'>shadow ban notes</a>.",
    ),
)

add(
    "blog-checklist-undetected",
    "comparison",
    "May 20, 2026",
    "Undetected COD Checklist Before You Buy",
    "Safest Call of Duty Hack Checklist 2026",
    "A practical safest Call of Duty hack checklist: feature list, update promise, Cloud DMA clarity, StreamProof, support, and real pricing.",
    "Undetected COD Checklist Before You Buy",
    "Use this list before you trust any Warzone cheat site.",
    "safest call of duty hack, best warzone cheat providers, most reliable warzone hack 2026",
    ["blog-comparison.html", "blog-undetected-warzone-2026.html", BUY],
    section(
        "Checklist",
        ul=[
            "Do they list exact features (Aimbot Humanizer, Loot ESP, Radar)?",
            "Do they say Cloud DMA on AWS clearly — not vague “DMA magic”?",
            "Is there a real update promise (we use 2–4 hours)?",
            "Is StreamProof included?",
            "Is support actually linked?",
            "Are prices clear ($35 / $150 here)?",
            "Do articles link to a real <a href='" + BUY + "'>buy page</a> on the same site?",
        ],
    )
    + section(
        "If a site fails the list",
        "Do not download. Come back to <a href='" + HOME + "'>codcheats.net</a>, read <a href='blog-comparison.html'>the comparison</a>, then decide.",
    ),
)


NAV = f"""  <div class="announcement"><div class="announcement-inner container"><span>Call of Duty guides · Updated for Warzone & multiplayer</span><a href="{PURCHASE}" rel="noopener sponsored">Buy Now</a></div></div>
  <header class="site-header"><div class="container nav">
    <a class="brand" href="{HOME}"><img src="{LOGO}" width="36" height="36" alt="Call of Duty Cheats"><span>COD Cheats</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-label="Open menu">Menu</button>
    <ul class="nav-links">
      <li><a href="{HOME}">Home</a></li><li><a href="{BUY}">Buy</a></li><li><a class="active" href="{BLOG}">Blog</a></li><li><a href="{GUIDE}">Guide</a></li>
      <li><a class="nav-cta" href="{PURCHASE}" rel="noopener sponsored">Get Access</a></li>
    </ul>
  </div></header>"""

FOOT = f"""  <footer class="site-footer"><div class="container"><div class="footer-grid">
    <div><div class="footer-brand"><img src="{LOGO}" width="32" height="32" alt="Call of Duty Cheats"><span>COD Cheats</span></div>
    <p style="color:var(--text-muted);margin:0;">Guides and tools for Call of Duty players on <a href="{HOME}">codcheats.net</a>.</p></div>
    <div><h4>Site</h4><ul><li><a href="{HOME}">Home</a></li><li><a href="{BUY}">Buy</a></li><li><a href="{BLOG}">Blog</a></li><li><a href="{GUIDE}">Guide</a></li></ul></div>
    <div><h4>Store</h4><ul><li><a href="{PURCHASE}" rel="noopener sponsored">Purchase Access</a></li><li><a href="{BUY}#pricing">Pricing</a></li></ul></div>
    <div><h4>Support</h4><ul><li><a href="{SUPPORT}" rel="noopener">Support Channel</a></li></ul></div>
  </div><p class="disclaimer">Game images credited to IGN where shown. Product features match the buy page. © 2026 codcheats.net</p></div></footer>
  <script src="js/main.js" defer></script>"""


def article_html(post, img):
    labels = []
    for r in post["related"]:
        if r == BUY:
            labels.append(f'<a href="{r}">Call of Duty cheats — pricing & features</a>')
        elif r == HOME:
            labels.append(f'<a href="{r}">codcheats.net home</a>')
        elif r == GUIDE:
            labels.append(f'<a href="{r}">RICOCHET anti-cheat guide</a>')
        else:
            slug = r.replace(".html", "")
            title = next((x["title"] for x in POSTS if x["slug"] == slug), slug)
            href = r if r.endswith(".html") else f"{r}.html"
            labels.append(f'<a href="{href}">{xu.escape(title)}</a>')
    related_links = "\n".join(labels)

    kw = post["keywords"]
    body = post["body"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{xu.escape(post["meta_title"])}</title>
  <meta name="description" content="{xu.escape(post["meta_desc"])}">
  <link rel="canonical" href="https://codcheats.net/{post["slug"]}.html">
  <meta name="robots" content="index,follow">
  <meta name="keywords" content="{xu.escape(kw)}">
  <meta property="og:title" content="{xu.escape(post["meta_title"])}">
  <meta property="og:description" content="{xu.escape(post["meta_desc"])}">
  <meta property="og:url" content="https://codcheats.net/{post["slug"]}.html">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{img["src"]}">
  <link rel="icon" href="{LOGO}">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/global.css">
  <link rel="stylesheet" href="css/blog.css">
</head>
<body>
{NAV}
  <article class="article-wrap">
    <div class="eyebrow">{post["cat"].title()}</div>
    <h1>{xu.escape(post["h1"])}</h1>
    <div class="article-meta">{post["date"]} · <a href="{BLOG}">COD blog</a> · <a href="{HOME}">codcheats.net</a></div>
    <img class="article-hero-img" src="{img["src"]}" width="1280" height="720" alt="{xu.escape(img["alt"])}" loading="lazy">
    <p class="article-img-credit">Image via <a href="{img["credit"]}" rel="noopener noreferrer" target="_blank">IGN</a> (Call of Duty coverage). All rights belong to their owners.</p>
    <div class="article-body">
{body}
      <p>Main site hub: <a href="{HOME}">codcheats.net</a> · Tools & pricing: <a href="{BUY}">Call of Duty cheats</a> · Education: <a href="{GUIDE}">anti-cheat guide</a>.</p>
      <div class="prose-cta">
        <h3 style="margin:0 0 0.5rem;">Ready for the full Warzone / COD suite?</h3>
        <p style="color:var(--text-muted);margin:0 0 1rem;">Aimbot, ESP, Loot ESP, Radar, StreamProof, Cloud DMA — Monthly $35 or Lifetime $150.</p>
        <a class="btn btn-primary" href="{PURCHASE}" rel="noopener sponsored">Get Access</a>
        <p class="redirect-note">Checkout opens on the main store. More info on <a href="{BUY}">the buy page</a>.</p>
      </div>
    </div>
    <div class="article-end">
      <h2>Keep reading on codcheats.net</h2>
      <div class="related-links">
{related_links}
        <a href="{BLOG}">All Call of Duty blog posts</a>
      </div>
    </div>
  </article>
{FOOT}
</body>
</html>
"""


def build_blog_index():
    cards = []
    for i, post in enumerate(POSTS):
        img = IGN[i % len(IGN)]
        cards.append(
            f"""          <article class="blog-card" data-category="{post["cat"]}">
            <img class="blog-card-img" src="{img["src"]}" alt="{xu.escape(img["alt"])}" loading="lazy" width="640" height="400">
            <span class="pill">{post["cat"].title()}</span>
            <h3>{xu.escape(post["title"])}</h3>
            <p>{xu.escape(post["card"])}</p>
            <div class="meta">{post["date"]}</div>
            <a class="btn btn-secondary" href="{post["slug"]}.html">Read Article</a>
          </article>"""
        )
    cards_html = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Call of Duty Cheats Blog — 30 Warzone Guides</title>
  <meta name="description" content="30 Call of Duty and Warzone cheat guides on codcheats.net: aimbot, ESP, DMA, ranked, Resurgence, RICOCHET, pricing, and setup tips.">
  <link rel="canonical" href="https://codcheats.net/blog.html">
  <meta name="robots" content="index,follow">
  <meta property="og:title" content="Call of Duty Cheats Blog — 30 Warzone Guides">
  <meta property="og:description" content="Aimbot, ESP, Cloud DMA, ranked, and safety guides for Call of Duty players.">
  <meta property="og:url" content="https://codcheats.net/blog.html">
  <meta property="og:type" content="website">
  <link rel="icon" href="{LOGO}">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/global.css">
  <link rel="stylesheet" href="css/blog.css">
</head>
<body>
{NAV}
  <main>
    <section class="page-hero">
      <div class="container">
        <div class="eyebrow">Blog · 30 guides</div>
        <h1>Call of Duty Blogs & Tips</h1>
        <p class="lead">Easy guides for warzone hacks, cod aimbot, ESP, Cloud DMA, and RICOCHET — written for real players, with internal links back to <a href="{HOME}">codcheats.net</a>.</p>
        <div class="filters" role="tablist" aria-label="Filter articles">
          <button class="filter-btn active" type="button" data-filter="all">All</button>
          <button class="filter-btn" type="button" data-filter="comparison">Comparison</button>
          <button class="filter-btn" type="button" data-filter="esp">ESP</button>
          <button class="filter-btn" type="button" data-filter="aimbot">Aimbot</button>
          <button class="filter-btn" type="button" data-filter="spoofing">Spoofing</button>
          <button class="filter-btn" type="button" data-filter="safety">Safety</button>
        </div>
      </div>
    </section>
    <section class="section" style="padding-top:0;">
      <div class="container">
        <div class="blog-grid">
{cards_html}
        </div>
      </div>
    </section>
  </main>
{FOOT}
</body>
</html>
"""


def build_sitemap():
    urls = [
        ("https://codcheats.net/", "1.0"),
        ("https://codcheats.net/call-of-duty-cheats.html", "0.95"),
        ("https://codcheats.net/guide.html", "0.85"),
        ("https://codcheats.net/blog.html", "0.9"),
    ]
    for post in POSTS:
        urls.append((f"https://codcheats.net/{post['slug']}.html", "0.7"))
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri in urls:
        body.append("  <url>")
        body.append(f"    <loc>{loc}</loc>")
        body.append("    <changefreq>weekly</changefreq>")
        body.append(f"    <priority>{pri}</priority>")
        body.append("  </url>")
    body.append("</urlset>")
    return "\n".join(body) + "\n"


def main():
    assert len(POSTS) == 30, len(POSTS)
    for i, post in enumerate(POSTS):
        img = IGN[i % len(IGN)]
        path = ROOT / f"{post['slug']}.html"
        path.write_text(article_html(post, img), encoding="utf-8")
        print("wrote", path.name)
    (ROOT / "blog.html").write_text(build_blog_index(), encoding="utf-8")
    print("wrote blog.html")
    (ROOT / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8")
    print("wrote sitemap.xml")
    print("DONE", len(POSTS), "posts")


if __name__ == "__main__":
    main()
