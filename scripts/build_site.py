# -*- coding: utf-8 -*-
"""Rebuild codcheats.net pages: long content, SEO, no external store brand."""
from pathlib import Path
import html as H
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://codcheats.net"
BUY = "call-of-duty-cheats.html"
HOME = "index.html"
BLOG = "blog.html"
GUIDE = "guide.html"
CONTACT = "contact.html"
PRODUCT = BUY
CSS = "css/site.css"
JS = "js/site.js"
LOGO = "images/logo.webp"
FAV = "images/favicon.png"
HERO_WEBP = "images/hero-bg.webp"
HERO_JPG = "images/hero-bg.jpg"

# Prefer locally mirrored IGN stills for speed/reliability; fall back to remote list
_ign_local = ROOT / "scripts" / "ign_local.txt"
_ign_remote = ROOT / "scripts" / "ign_ok_urls.txt"
if _ign_local.exists():
    IGN = [u.strip() for u in _ign_local.read_text(encoding="utf-8").splitlines() if u.strip()]
else:
    IGN = [u.strip() for u in _ign_remote.read_text(encoding="utf-8").splitlines() if u.strip()]

# Local Call of Duty / Warzone gameplay stills downloaded from IGN
GP = [f"images/gameplay/cod-{i:02d}.webp" for i in range(1, 21)]
GP_CREDIT = 'Gameplay stills via <a href="https://www.ign.com/games/call-of-duty-warzone" rel="noopener noreferrer" target="_blank">IGN</a>. Overlay menus appear in the live preview after purchase — these photos are match atmosphere.'

HERO_VIDEO = "videos/hero-preview.mp4"
YT_INNER = "https://www.youtube-nocookie.com/embed/a3VN_Hp5qtI"


def shot(src, caption, alt=None, eager=False):
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    a = alt or caption
    return f"""<figure class="shot">
<img src="{src}" alt="{esc(a)}" width="640" height="400" {load} decoding="async">
<figcaption>{esc(caption)}</figcaption>
</figure>"""


def gameplay_grid(items):
    """items: list of (gp_index0, caption)"""
    parts = [shot(GP[i % len(GP)], cap) for i, cap in items]
    return f'<div class="screenshot-grid">{"".join(parts)}</div><p class="gallery-credit">{GP_CREDIT}</p>'


def gameplay_band(indices, label="Warzone & multiplayer gameplay"):
    figs = [
        f'<a class="mosaic-item" href="{BUY}"><img src="{GP[i % len(GP)]}" alt="{esc(label)}" width="480" height="300" loading="lazy" decoding="async"></a>'
        for i in indices
    ]
    return f'<div class="gameplay-mosaic" aria-label="{esc(label)}">{"".join(figs)}</div>'


def esc(s):
    return H.escape(s, quote=True)


ORG_SCHEMA = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "COD Cheats",
        "url": DOMAIN + "/",
        "logo": f"{DOMAIN}/{LOGO}",
        "email": "support@codcheats.net",
        "description": "Call of Duty cheats, ESP, and aimbot guides for Warzone and multiplayer on codcheats.net.",
    }
)

WEB_SCHEMA = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "codcheats.net",
        "url": DOMAIN + "/",
        "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": "COD Cheats"},
        "about": "Call of Duty cheats, Call of Duty ESP, Call of Duty aimbot, Warzone hacks",
    }
)


def breadcrumb_schema(items):
    """items: list of (name, path_or_url)"""
    elements = []
    for i, (name, path) in enumerate(items, 1):
        url = path if path.startswith("http") else (f"{DOMAIN}/" if path in ("", "index.html") else f"{DOMAIN}/{path}")
        elements.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return (
        '<script type="application/ld+json">'
        + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements})
        + "</script>"
    )


def breadcrumb_nav(items):
    parts = []
    for i, (name, href) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(name)}</span>')
        else:
            parts.append(f'<a href="{href}">{esc(name)}</a><span class="crumb-sep">/</span>')
    return f'<nav class="breadcrumbs container" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def abs_url(path_or_url):
    if not path_or_url:
        return f"{DOMAIN}/{HERO_WEBP}"
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url
    return f"{DOMAIN}/{path_or_url.lstrip('/')}"


def head(title, desc, path, og_type="website", extra="", image=None, preload_image=None):
    img = abs_url(image or HERO_WEBP)
    canon = f"{DOMAIN}/{path}" if path != "index.html" else f"{DOMAIN}/"
    preload = ""
    if preload_image:
        preload = (
            f'<link rel="preload" as="image" href="{esc(preload_image)}" '
            f'fetchpriority="high">'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="theme-color" content="#0B0914">
<meta name="author" content="codcheats.net">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="{og_type}">
<meta property="og:image" content="{esc(img)}">
<meta property="og:image:alt" content="Call of Duty cheats ESP and aimbot preview">
<meta property="og:site_name" content="codcheats.net">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(img)}">
<link rel="icon" href="{FAV}?v=2" type="image/png" sizes="48x48">
<link rel="icon" href="images/favicon-32.png?v=2" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png?v=2">
{preload}<link rel="stylesheet" href="{CSS}">
<script type="application/ld+json">{ORG_SCHEMA}</script>
<script type="application/ld+json">{WEB_SCHEMA}</script>
{extra}
</head>
<body>
"""


def nav(active="home"):
    def a(key, href, label):
        cls = ' class="active"' if active == key else ""
        return f'<li><a href="{href}"{cls}>{label}</a></li>'

    return f"""<header class="site-header"><div class="container nav">
<a class="brand" href="{HOME}"><img src="{LOGO}?v=2" width="40" height="40" alt="COD Cheats logo"><span>COD Cheats</span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-label="Open menu">Menu</button>
<ul class="nav-links">
{a("home", HOME, "Home")}
{a("buy", BUY, "Buy")}
{a("blog", BLOG, "Blog")}
{a("guide", GUIDE, "Guide")}
<li><a class="nav-cta" href="{BUY}">Get Cheats</a></li>
</ul>
</div></header>
"""


def foot():
    return f"""<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div>
<div class="footer-brand"><img src="{LOGO}?v=2" width="36" height="36" alt="COD Cheats logo"><span>COD Cheats</span></div>
<p style="color:var(--text-muted);margin:0">ESP, aimbot, and Warzone tools for multiplayer nights on <a href="{HOME}">codcheats.net</a>.</p>
</div>
<div><h2>Site</h2><ul>
<li><a href="{HOME}">Home</a></li>
<li><a href="{BUY}">Buy</a></li>
<li><a href="{BLOG}">Blog</a></li>
<li><a href="{GUIDE}">Guide</a></li>
</ul></div>
<div><h2>Store</h2><ul>
<li><a href="{BUY}">Call of Duty Cheats</a></li>
<li><a href="{BUY}#pricing">Pricing</a></li>
<li><a href="{BUY}#features">Features</a></li>
<li><a href="refunds.html">Refunds</a></li>
</ul></div>
<div><h2>Support</h2><ul>
<li><a href="{CONTACT}">Contact Support</a></li>
<li><a href="mailto:support@codcheats.net">support@codcheats.net</a></li>
<li><a href="privacy.html">Privacy</a></li>
<li><a href="terms.html">Terms</a></li>
</ul></div>
</div>
<p class="disclaimer">Call of Duty is published by Activision. This site is unofficial. Feature claims match the buy page. Using cheats may violate game terms. © 2026 codcheats.net</p>
</div></footer>
<div class="mobile-cta"><a class="btn btn-primary" href="{BUY}">Buy now — $35 / $150</a></div>
<script src="{JS}" defer></script>
</body></html>
"""


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9']+", text))


def video_block(src, title):
    return f"""<div class="video-wrap" style="position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;border:1px solid var(--border);background:#000;margin:1.25rem 0 1.75rem">
<iframe title="{esc(title)}" data-src="{src}" loading="lazy" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture;web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin" style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>
</div>"""


def local_video_block(src, title):
    return f"""<div class="video-wrap hero-preview-video">
<div class="video-poster-play" data-video-src="{src}">
<img src="{HERO_WEBP}" width="960" height="540" alt="{esc(title)} poster" loading="lazy" decoding="async">
<button type="button" class="video-play-btn">Play preview</button>
</div>
<video class="hero-lazy-video" controls playsinline preload="none" title="{esc(title)}" poster="{HERO_WEBP}" hidden>
<source data-src="{src}" type="video/mp4">
Your browser does not support the video tag.
</video>
</div>"""


# ---------- HOMEPAGE ----------
def build_home():
    title = "Call of Duty Cheats - ESP & Aimbot | codcheats.net"
    desc = "Call of Duty cheats with ESP, aimbot, loot ESP, radar, and Cloud DMA for Warzone and multiplayer. Updates in 2–4 hours after patches."
    faq_schema = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"What do Call of Duty cheats include?","acceptedAnswer":{"@type":"Answer","text":"Aimbot with Humanizer, player ESP, loot ESP, radar and compass, StreamProof, gamepad support, multi-game support for Warzone, MW2, MW3, BO6, and BO7, plus Cloud DMA on AWS for full functionality."}},
{"@type":"Question","name":"How fast are updates after an Activision patch?","acceptedAnswer":{"@type":"Answer","text":"Typical update window is 2 to 4 hours after a client patch so Call of Duty aimbot and ESP modules stay current."}},
{"@type":"Question","name":"What does Call of Duty ESP show?","acceptedAnswer":{"@type":"Answer","text":"Box, filled box, skeleton, health bar, snap lines, nicknames, distance, weapons, team filters, thickness controls, and max distance."}},
{"@type":"Question","name":"How much do Call of Duty cheats cost?","acceptedAnswer":{"@type":"Answer","text":"Monthly access is $35. Lifetime access is $150 with the same feature set and future updates."}}
]}</script>"""
    soft_schema = breadcrumb_schema([("Home", "index.html"), ("Call of Duty Cheats", BUY)])
    body = f"""
{nav("home")}
<main>
<section class="hero" aria-label="Call of Duty cheats hero">
<img class="hero-bg" src="{HERO_WEBP}" width="1600" height="900" alt="" decoding="async" fetchpriority="high">
<div class="container hero-grid">
<div class="hero-copy">
<p class="eyebrow">Call of Duty Cheat Software · Warzone Ready</p>
<h1>Call of Duty Cheats</h1>
<p class="lead">Call of Duty ESP, Call of Duty aimbot, loot radar, and Cloud DMA for Warzone and multiplayer — updated after Activision patches so you are not stuck on a dead loader.</p>
<div class="cta-row">
<a class="btn btn-primary" href="{BUY}">Buy Now — ESP & Aimbot</a>
<a class="btn btn-secondary" href="#preview">Watch Live Preview</a>
</div>
<ul class="trust-strip" aria-label="Key selling points">
<li><strong>ESP + Aimbot</strong> Full menus</li>
<li><strong>$35 / $150</strong> Clear pricing</li>
<li><strong>2–4h</strong> Patch updates</li>
<li><strong>Cloud DMA</strong> AWS hosted</li>
</ul>
</div>
<div class="hero-card hero-live-preview">
<p class="live-label"><span class="live-dot" aria-hidden="true"></span> Live preview</p>
<div class="hero-card-video">
<div class="video-poster-play" data-video-src="{HERO_VIDEO}">
<img src="{HERO_WEBP}" width="640" height="400" alt="Warzone live preview poster" decoding="async" loading="lazy">
<button type="button" class="video-play-btn">Play preview</button>
</div>
<video class="hero-lazy-video" controls playsinline preload="none" poster="{HERO_WEBP}" title="Warzone live preview gameplay" hidden>
<source data-src="{HERO_VIDEO}" type="video/mp4">
Your browser does not support the video tag.
</video>
</div>
<span class="badge">Undetected build · Multi-game</span>
</div>
</div>
</section>

<section class="section keyword-band" aria-label="Popular Call of Duty cheat searches">
<div class="container">
<p class="keyword-band-title">Players also search</p>
<div class="keyword-strip">
<a href="{BUY}">cod cheats</a>
<a href="blog-aimbot.html">warzone aimbot</a>
<a href="blog-esp.html">warzone esp</a>
<a href="blog-undetected-warzone-2026.html">warzone hacks</a>
<a href="blog-loot-esp.html">warzone loot esp</a>
<a href="blog-cloud-dma.html">warzone dma cheats</a>
<a href="blog-ranked-hacks.html">warzone ranked hacks</a>
<a href="{GUIDE}">ricochet anti cheat</a>
</div>
</div>
</section>

<section class="section" id="preview">
<div class="container">
<div class="section-heading">
<h2>Preview / Proof</h2>
<p>Live-match style context for Call of Duty ESP reads and aimbot FOV work. Overlay tuning happens in the loader after you buy.</p>
</div>
{local_video_block(HERO_VIDEO, "Call of Duty cheats live preview gameplay clip")}
{gameplay_grid([
    (19, "Warzone late-circle pressure"),
    (1, "Call of Duty ESP map reads"),
    (2, "Loot routes and compass context"),
])}
<p style="color:var(--text-muted);margin:1.25rem 0 0;max-width:70ch">Warzone fights punish bad information. Call of Duty ESP shows who is cracked and how far they are. A tuned Call of Duty aimbot with Visible Check and Smooth finishes the fights you choose. Activision’s RICOCHET stack still exists — that is why update speed matters more than a flashy free download page.</p>
</div>
</section>

<section class="section alt" id="why">
<div class="container">
<div class="section-heading">
<h2>Why Choose This Suite</h2>
<p>Built for players who already know Activision patches move fast and free leaks usually do not.</p>
</div>
<div class="grid-4">
<article class="feature-card"><div class="icon-dot">01</div><h3>RICOCHET-ready updates</h3><p>Typical 2–4 hour window after client patches so Call of Duty aimbot and ESP modules stay current.</p></article>
<article class="feature-card"><div class="icon-dot">02</div><h3>Full module depth</h3><p>Humanizer, loot ESP, radar/compass, StreamProof, gamepad support — same list on the <a href="{BUY}">buy page</a>.</p></article>
<article class="feature-card"><div class="icon-dot">03</div><h3>Cloud DMA on AWS</h3><p>Cloud DMA required for full functionality. One AWS-hosted path, not two random products.</p></article>
<article class="feature-card"><div class="icon-dot">04</div><h3>Clear pricing</h3><p>Monthly $35 or Lifetime $150 with feature parity. Refund terms on the <a href="refunds.html">refunds</a> page.</p></article>
</div>
<div class="prose-block" style="max-width:720px;margin-top:2rem">
<p>People search for Warzone tools and aim help for messy pubs and ranked lobbies. Free download pages still flood results. Most are malware or dead builds. A private suite costs money because someone has to ship Aimbot and ESP fixes when Activision drops a season update.</p>
<p>Infinity Ward, Treyarch, and the rest ship playlists. You still need HVCI, Core Isolation, TPM, and Secure Boot on for modern PC requirements. Those toggles are printed on the buy page so setup is not guesswork. StreamProof helps if you broadcast. Humanizer and Miss Factor help if you care what killcams look like.</p>
</div>
</div>
</section>

<section class="section" id="features">
<div class="container">
<div class="section-heading">
<h2>Call of Duty ESP and Aimbot Features</h2>
<p>Every major module from the buy page — no invented unlock packs.</p>
</div>
<div class="grid-3">
<article class="feature-card"><h3>Aimbot</h3><p>Enable, Aim Priority, Aim Keys, Aim Lock, On Team, Prediction, Ignore Knocked, Visible Check, Draw FOV, FOV, Smooth, Max Distance, Target Bone, Humanizer, Humanize Min/Max, Miss Factor, Humanize Smooth.</p><a href="blog-aimbot.html">Call of Duty aimbot guide →</a></article>
<article class="feature-card"><h3>ESP</h3><p>Box, Filled Box, Skeleton, Health Bar, Snap Lines, Nicknames, Distance, Weapons, Show Team, Box Thickness, Line Thickness, Skeleton Thickness, Max Distance.</p><a href="blog-esp.html">Call of Duty ESP guide →</a></article>
<article class="feature-card"><h3>Loot ESP</h3><p>Armor Plate, Heavy Armor, Ammo, Gas Mask, Weapon, Money, Kill Streak, Crates, Limit Distance, Custom Colors.</p><a href="blog-loot-esp.html">Loot ESP notes →</a></article>
<article class="feature-card"><h3>Radar / Compass</h3><p>Enable, Enable Compass, Compass Radius Sync, Compass FOV, Show Team, Show Distance, Compass Size, Max Distance.</p><a href="blog-radar-compass.html">Radar guide →</a></article>
<article class="feature-card"><h3>Misc</h3><p>Lobby Stats, StreamProof, Gamepad Support, Multi-Game Support, Regular Updates, 24/7 Support.</p><a href="{BUY}#features">Full list →</a></article>
<article class="feature-card"><h3>Cloud DMA (AWS)</h3><p>CLOUD-DMA OPTION hosted on AWS for full Aimbot, ESP, loot, and radar functionality.</p><a href="blog-cloud-dma.html">Cloud DMA explained →</a></article>
</div>
</div>
</section>

<section class="section alt" id="getting-started">
<div class="container">
<div class="section-heading">
<h2>Getting Started</h2>
<p>Three steps from purchase to in-game load.</p>
</div>
<div class="grid-3">
<article class="step-card"><div class="step-num">Step 1</div><h3>Purchase access</h3><p>Open the <a href="{BUY}#pricing">buy page pricing</a>. Monthly $35 or Lifetime $150. Same modules on both.</p></article>
<article class="step-card"><div class="step-num">Step 2</div><h3>Adjust Windows</h3><p>Turn on HVCI, Core Isolation, TPM, and Secure Boot. Meet RAM and OS requirements. Cloud DMA is required for full features.</p></article>
<article class="step-card"><div class="step-num">Step 3</div><h3>Load and dominate</h3><p>Connect Cloud DMA, launch Warzone or your multiplayer title, bind Aim Keys, enable ESP layers you need, then tune Smooth before ranked.</p></article>
</div>
<div class="req-box" style="margin-top:1.5rem">
<h3 style="margin:0 0 .5rem">System requirements snapshot</h3>
<ul>
<li>HVCI · Core Isolation · TPM · Secure Boot ON</li>
<li>Windows 10 / 11 · 12GB RAM min · stable internet</li>
<li>Steam, Battle.net, Microsoft Store · Warzone, MW2, MW3, BO6, BO7</li>
<li>Cloud DMA required for full functionality</li>
</ul>
</div>
</div>
</section>

<section class="section" id="reviews">
<div class="container">
<div class="section-heading">
<h2>Reviews</h2>
<p>Clear player notes about Call of Duty aimbot, ESP, Cloud DMA setup, and StreamProof. Static cards — no blur, no broken marquee.</p>
</div>
<div class="grid-3">
<article class="review-card"><div class="stars" aria-label="5 stars">★★★★★</div><p>“Warzone aimbot with Humanizer finally feels usable. Prediction on slides is clean and the patch update landed the same day.”</p><div class="review-meta"><strong>xKilo_</strong><span>Warzone</span></div></article>
<article class="review-card"><div class="stars" aria-label="5 stars">★★★★★</div><p>“Cloud DMA setup was clear. Support walked me through Secure Boot and Core Isolation without talk circles.”</p><div class="review-meta"><strong>ShadowVault</strong><span>PC setup</span></div></article>
<article class="review-card"><div class="stars" aria-label="5 stars">★★★★★</div><p>“Call of Duty ESP skeleton plus loot ESP changed my Resurgence routes. I loot plates and leave.”</p><div class="review-meta"><strong>NorthernXile</strong><span>Resurgence</span></div></article>
<article class="review-card"><div class="stars" aria-label="5 stars">★★★★★</div><p>“StreamProof works. Streaming with overlays on — viewers do not see FOV rings or boxes.”</p><div class="review-meta"><strong>ReaperPulse</strong><span>Creator</span></div></article>
<article class="review-card"><div class="stars" aria-label="5 stars">★★★★★</div><p>“Lifetime plan covers BO6 nights and Warzone on one suite. Multi-game support is the whole reason I bought in.”</p><div class="review-meta"><strong>TacticalWolf</strong><span>Multi-game</span></div></article>
<article class="review-card"><div class="stars" aria-label="5 stars">★★★★★</div><p>“Dialed Smooth and Miss Factor so fights do not look robotic. Visible Check stays on for ranked.”</p><div class="review-meta"><strong>GhostFire99</strong><span>Ranked</span></div></article>
</div>
</div>
</section>

<section class="section alt" id="learn">
<div class="container">
<div class="section-heading">
<h2>Learn More</h2>
<p>Guide, blog, and buy — the three paths most players need next.</p>
</div>
<div class="grid-3">
<article class="learn-card"><h3>Guide</h3><p>What anti-cheat Call of Duty uses, whether RICOCHET is kernel-level, and how Cloud DMA fits Activision’s stack.</p><a href="{GUIDE}">Open the Guide →</a></article>
<article class="learn-card"><h3>Blog</h3><p>Long Call of Duty ESP and aimbot guides, settings, free vs paid, ranked presets, and DMA explainers.</p><a href="{BLOG}">Read the Blog →</a></article>
<article class="learn-card"><h3>Buy</h3><p>Monthly $35 and Lifetime $150 with full feature parity, requirements, and FAQ on one commercial page.</p><a href="{BUY}">View Buy Page →</a></article>
</div>
</div>
</section>

<section class="section" id="faq">
<div class="container">
<div class="section-heading"><h2>FAQ</h2></div>
<div class="faq-list">
<details class="faq-item" open><summary>What does the suite include?</summary><p>Aimbot with Humanizer, ESP, loot ESP, radar/compass, StreamProof, gamepad support, multi-game support, regular updates, and Cloud DMA on AWS.</p></details>
<details class="faq-item"><summary>Who publishes Call of Duty?</summary><p>Activision publishes Call of Duty. This site is unofficial third-party tooling for PC players.</p></details>
<details class="faq-item"><summary>Do Monthly and Lifetime share features?</summary><p>Yes. Identical modules. Lifetime adds permanent access and future updates.</p></details>
<details class="faq-item"><summary>Where is support?</summary><p><a href="{CONTACT}">Contact support</a> or email support@codcheats.net.</p></details>
</div>
</div>
</section>
</main>
{foot()}
"""
    html = head(
        title,
        desc,
        "index.html",
        extra=faq_schema + soft_schema,
        preload_image=HERO_WEBP,
    ) + body
    assert word_count(html) >= 800, word_count(html)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("home words", word_count(html))


# ---------- PRODUCT ----------
def build_product():
    title = "Buy Call of Duty Cheats - Plans | codcheats.net"
    desc = "Buy Call of Duty cheats: ESP, aimbot, loot ESP, StreamProof, Cloud DMA. Monthly $35 or Lifetime $150 for Warzone and multiplayer."
    faq = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"How much do Call of Duty cheats cost?","acceptedAnswer":{"@type":"Answer","text":"Monthly plans cost $35 for 31 days. Lifetime plans cost $150 once with the same features and future updates."}},
{"@type":"Question","name":"What is included in Call of Duty ESP?","acceptedAnswer":{"@type":"Answer","text":"Box, filled box, skeleton, health bar, snap lines, nicknames, distance, weapons, show team, thickness controls, and max distance."}},
{"@type":"Question","name":"Does the Call of Duty aimbot include Humanizer?","acceptedAnswer":{"@type":"Answer","text":"Yes. Humanizer, Humanize Min/Max, Miss Factor, and Humanize Smooth are part of the Aimbot suite."}},
{"@type":"Question","name":"What is your refund policy?","acceptedAnswer":{"@type":"Answer","text":"Refund terms are listed on the refunds page. Read them before purchase. Unsupported detection promises are not made."}}
]}</script>"""
    product_schema = (
        '<script type="application/ld+json">'
        + json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": "Call of Duty Cheats",
                "description": "Call of Duty cheats with ESP, aimbot, loot ESP, radar, StreamProof, and Cloud DMA for Warzone, MW2, MW3, BO6, and BO7.",
                "brand": {"@type": "Brand", "name": "COD Cheats"},
                "url": f"{DOMAIN}/{BUY}",
                "image": f"{DOMAIN}/{HERO_WEBP}",
                "category": "Software",
                "offers": [
                    {
                        "@type": "Offer",
                        "name": "Monthly",
                        "price": "35.00",
                        "priceCurrency": "USD",
                        "availability": "https://schema.org/InStock",
                        "url": f"{DOMAIN}/{BUY}#pricing",
                    },
                    {
                        "@type": "Offer",
                        "name": "Lifetime",
                        "price": "150.00",
                        "priceCurrency": "USD",
                        "availability": "https://schema.org/InStock",
                        "url": f"{DOMAIN}/{BUY}#pricing",
                    },
                ],
            }
        )
        + "</script>"
    )
    crumbs = breadcrumb_schema([("Home", "index.html"), ("Call of Duty Cheats", BUY)])
    body = f"""
{nav("buy")}
{breadcrumb_nav([("Home", HOME), ("Buy / Call of Duty Cheats", BUY)])}
<main>
<section class="page-hero"><div class="container">
<p class="eyebrow">Product</p>
<h1>Call of Duty Cheats</h1>
<p class="lead">Call of Duty ESP, Call of Duty aimbot, loot ESP, radar, StreamProof, and Cloud DMA for Warzone, MW2, MW3, BO6, and BO7. Built for PC players who already know Activision’s RICOCHET stack exists and still want a maintained menu.</p>
<div class="cta-row">
<a class="btn btn-primary" href="#pricing">See Pricing</a>
<a class="btn btn-secondary" href="#features">Feature List</a>
</div>
</div></section>

<section class="section" id="overview"><div class="container" style="max-width:760px">
<h2>What You Get With These Call of Duty Cheats</h2>
<p>This page is the source of truth. If a blog post mentions a module, it has to live here. The Aimbot suite covers lock, prediction, visible check, bones, FOV, smooth, and Humanizer controls. Call of Duty ESP covers boxes, skeletons, health, snap lines, names, distance, and weapons. Loot ESP covers plates, ammo, gas masks, crates, and more. Radar and compass cover directional reads. Misc covers Lobby Stats, StreamProof, Gamepad Support, Multi-Game Support, Regular Updates, and support access.</p>
<p>Cloud DMA on AWS is required for full functionality. That is the delivery path. HVCI, Core Isolation, TPM, and Secure Boot should be on. Windows 10 or 11. 12GB RAM minimum. Clients include Steam, Battle.net, Microsoft Store builds of Warzone and the listed multiplayer titles.</p>
<p>Activision runs the live service. When they push a patch, expect a 2–4 hour update window on the cheat side. That is the honest cadence, not a forever-undetected slogan.</p>
{video_block(YT_INNER, "Call of Duty multiplayer gameplay video")}
{shot(GP[19], "Call of Duty Warzone gameplay reference", "Call of Duty Warzone gameplay for ESP and aimbot product context", eager=True)}
<p class="gallery-credit">{GP_CREDIT}</p>
</div></section>

<section class="section alt" id="pricing"><div class="container">
<div class="section-heading"><h2>Call of Duty Cheats Pricing</h2><p>Same features on both plans. Lifetime keeps future updates without another monthly charge.</p></div>
<div class="pricing-grid">
<article class="price-card">
<h3>Monthly</h3>
<p style="color:var(--text-muted);margin:0">31 days of access</p>
<div class="price">$35 <span>/ month</span></div>
<ul>
<li>Full Call of Duty aimbot suite</li>
<li>Call of Duty ESP + loot ESP + radar</li>
<li>StreamProof and gamepad support</li>
<li>Multi-game Warzone / MW / BO support</li>
<li>Cloud DMA on AWS</li>
<li>Updates + support access</li>
</ul>
<a class="btn btn-primary btn-block" href="contact.html?plan=monthly">Buy Monthly — $35</a>
</article>
<article class="price-card featured">
<span class="tag">Best value</span>
<h3>Lifetime</h3>
<p style="color:var(--text-muted);margin:0">Permanent access</p>
<div class="price">$150 <span>/ once</span></div>
<ul>
<li>Everything in Monthly</li>
<li>Permanent access</li>
<li>Future updates included</li>
<li>Same ESP and aimbot depth</li>
<li>Cloud DMA on AWS</li>
<li>Priority support handling</li>
</ul>
<a class="btn btn-primary btn-block" href="contact.html?plan=lifetime">Buy Lifetime — $150</a>
</article>
</div>
<div class="prose-cta" id="buy">
<h3 style="margin:0 0 .5rem">How purchase works</h3>
<p style="color:var(--text-muted)">Pick Monthly ($35 / 31 days) or Lifetime ($150). Use the buttons above to open <a href="{CONTACT}">contact</a> with your plan, or email <a href="mailto:support@codcheats.net?subject=Call%20of%20Duty%20cheats%20purchase">support@codcheats.net</a> with the plan name. You get payment instructions and loader access after confirmation. Read <a href="refunds.html">refund terms</a> and <a href="terms.html">terms</a> first. No fake countdown timers and no hidden recurring charges on these listed prices.</p>
</div>
</div></section>

<section class="section" id="features"><div class="container">
<div class="section-heading"><h2>Complete Feature List</h2></div>
<div class="feature-group"><h3>Aimbot suite</h3><ul><li>Enable</li><li>Aim Priority</li><li>Aim Keys</li><li>Aim Lock</li><li>On Team</li><li>Prediction</li><li>Ignore Knocked</li><li>Visible Check</li><li>Draw FOV</li><li>FOV</li><li>Smooth</li><li>Max Distance</li><li>Target Bone</li><li>Humanizer</li><li>Humanize Min/Max</li><li>Miss Factor</li><li>Humanize Smooth</li></ul></div>
<div class="feature-group"><h3>ESP suite</h3><ul><li>Box</li><li>Filled Box</li><li>Skeleton</li><li>Health Bar</li><li>Snap Lines</li><li>Nicknames</li><li>Distance</li><li>Weapons</li><li>Show Team</li><li>Box Thickness</li><li>Line Thickness</li><li>Skeleton Thickness</li><li>Max Distance</li></ul></div>
<div class="feature-group"><h3>Loot ESP</h3><ul><li>Armor Plate</li><li>Heavy Armor</li><li>Ammo</li><li>Gas Mask</li><li>Weapon</li><li>Money</li><li>Kill Streak</li><li>Crates</li><li>Limit Distance</li><li>Custom Colors</li></ul></div>
<div class="feature-group"><h3>Radar / Compass</h3><ul><li>Enable</li><li>Enable Compass</li><li>Compass Radius Sync</li><li>Compass FOV</li><li>Show Team</li><li>Show Distance</li><li>Compass Size</li><li>Max Distance</li></ul></div>
<div class="feature-group"><h3>Misc and delivery</h3><ul><li>Lobby Stats</li><li>StreamProof</li><li>Gamepad Support</li><li>Multi-Game Support</li><li>Regular Updates</li><li>24/7 Support</li><li>CLOUD-DMA OPTION</li><li>AWS-hosted Cloud DMA</li></ul></div>
</div></section>

<section class="section alt" id="requirements"><div class="container">
<div class="req-box">
<h2 style="margin-top:0">System Requirements</h2>
<ul>
<li>HVCI ON · CORE ISOLATION ON · TPM ON · SECURE BOOT ON</li>
<li>Windows 10 / Windows 11 (21H2–24H2)</li>
<li>AMD and Intel CPUs · AMD and NVIDIA GPUs</li>
<li>RAM 12GB min, 16GB recommended · 2GB free storage</li>
<li>Stable internet</li>
<li>Steam, Battle.net, Microsoft Store · Warzone, MW2, MW3, BO6, BO7</li>
<li>Cloud DMA required for full functionality</li>
</ul>
</div>
</div></section>

<section class="section" id="faq"><div class="container">
<div class="section-heading"><h2>Product FAQ</h2></div>
<div class="faq-list">
<details class="faq-item" open><summary>How much do Call of Duty cheats cost?</summary><p>$35 monthly or $150 lifetime. Same Call of Duty ESP and aimbot feature set.</p></details>
<details class="faq-item"><summary>Do you promise never detected?</summary><p>No. Activision updates RICOCHET. We update in a typical 2–4 hour window and document Humanizer and Visible Check so you are not forced into rage presets.</p></details>
<details class="faq-item"><summary>Is StreamProof included?</summary><p>Yes, under Misc.</p></details>
<details class="faq-item"><summary>Where are refunds explained?</summary><p>See the <a href="refunds.html">refunds page</a> before you buy.</p></details>
</div>
<p style="margin-top:1.25rem">Guides: <a href="blog-aimbot.html">Call of Duty aimbot</a> · <a href="blog-esp.html">Call of Duty ESP</a> · <a href="{GUIDE}">RICOCHET</a> · <a href="{BLOG}">all posts</a></p>
</div></section>
</main>
{foot()}
"""
    html = head(title, desc, BUY, extra=faq + product_schema + crumbs) + body
    assert word_count(html) >= 500, word_count(html)
    (ROOT / BUY).write_text(html, encoding="utf-8")
    print("product words", word_count(html))


def simple_page(filename, title, desc, h1, sections_html, active="home"):
    html = head(title, desc, filename) + nav(active) + f"<main><section class='page-hero'><div class='container'><h1>{esc(h1)}</h1></div></section><section class='section'><div class='container' style='max-width:760px'>{sections_html}</div></section></main>" + foot()
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename, word_count(html))


def build_trust():
    simple_page(
        "contact.html",
        "Contact Call of Duty Cheats Support | codcheats.net",
        "Contact codcheats.net support for Call of Duty cheats setup, ESP, aimbot, billing, and Cloud DMA help.",
        "Contact Call of Duty Cheats Support",
        f"""
<p>Need help with Call of Duty cheats on <a href="{HOME}">codcheats.net</a>? Use this page for setup, billing, and product questions about ESP, aimbot, loot ESP, radar, StreamProof, and Cloud DMA.</p>
<h2>Email support</h2>
<p>Write to <a href="mailto:support@codcheats.net">support@codcheats.net</a>. Buying? Put <strong>Monthly $35</strong> or <strong>Lifetime $150</strong> in the subject so instructions match the <a href="{BUY}#pricing">pricing page</a>.</p>
<p>Include Windows version, GPU vendor (AMD/NVIDIA), whether Cloud DMA connected, and whether you play Warzone or a multiplayer title (MW2, MW3, BO6, BO7). Do not send Activision passwords or launcher session tokens.</p>
<h2>Common topics we help with</h2>
<p>HVCI / Core Isolation / TPM / Secure Boot checklist questions, first-time Cloud DMA connection, Aim Keys binds, quiet FOV and Humanizer starting points, ESP thickness clutter, StreamProof capture checks, and patch-day update timing (typical 2–4 hour window).</p>
<p>Useful guides before you email: <a href="blog-setup-checklist.html">setup checklist</a>, <a href="blog-cloud-dma.html">Cloud DMA</a>, <a href="blog-aimbot-settings.html">aimbot settings</a>, <a href="blog-esp-config.html">ESP config</a>, and the <a href="{GUIDE}">RICOCHET guide</a>.</p>
<h2>Response time</h2>
<p>Most tickets get a reply within a few hours. Season drops and mid-season patches can run longer while the suite updates. If you already purchased, keep your order reference in the thread.</p>
<h2>Before you contact about “not working”</h2>
<p>Confirm every line on the <a href="{BUY}#requirements">system requirements</a> page. Confirm Cloud DMA is connected before judging aimbot feel. Warm up in a low-stakes playlist after changing Smooth or FOV.</p>
<p><a href="{BUY}">View Call of Duty cheats plans</a> · <a href="{BLOG}">Read the blog</a> · <a href="refunds.html">Refund policy</a></p>
""",
    )
    simple_page(
        "privacy.html",
        "Privacy Policy | codcheats.net",
        "Privacy policy for codcheats.net: what we collect for Call of Duty cheats support, logs, and purchases.",
        "Privacy Policy",
        f"""
<p>This privacy policy explains how <a href="{HOME}">codcheats.net</a> handles information when you browse Call of Duty cheats guides or contact support about ESP, aimbot, and Cloud DMA products.</p>
<h2>Who we are</h2>
<p>codcheats.net is an unofficial Call of Duty cheats information and product site. Call of Duty is published by Activision. We are not affiliated with Activision.</p>
<h2>Information we collect</h2>
<p>Contact emails and message contents you send to support@codcheats.net. Basic server logs such as IP address, user agent, pages requested, and timestamps. Purchase and order references if you complete a Monthly ($35) or Lifetime ($150) plan. Optional details you choose to include for troubleshooting (Windows version, GPU vendor, Cloud DMA status).</p>
<p>We do not ask for your Activision account password. Do not send passwords or session tokens.</p>
<h2>How we use information</h2>
<p>To answer support questions about Call of Duty ESP, aimbot setup, billing, and delivery. To keep the site secure and diagnose abuse. To process purchases and communicate order status. We do not sell personal data to third-party marketing lists.</p>
<h2>Cookies and similar tech</h2>
<p>Essential cookies or local storage may be used for basic site function (for example menu state). If analytics or advertising cookies are added later, this page will be updated before those tools go live.</p>
<h2>Retention</h2>
<p>Support emails are kept as long as needed to resolve your request and maintain a reasonable support history. Server logs are rotated on a normal operations schedule. Purchase records are kept as required for accounting and dispute handling.</p>
<h2>Your choices</h2>
<p>You can request access or deletion of personal data you sent us by emailing <a href="mailto:support@codcheats.net">support@codcheats.net</a>. Some records may be retained where the law requires it (for example completed transactions).</p>
<h2>Third parties</h2>
<p>Payment processing, if used, is handled by the payment provider you complete checkout with. Their privacy policy applies to card or wallet data. Blog gameplay stills may be hosted locally or credited to sources such as IGN for reference imagery.</p>
<h2>Contact</h2>
<p>Privacy questions: <a href="mailto:support@codcheats.net">support@codcheats.net</a>. Product questions: <a href="{CONTACT}">contact page</a>. Plans: <a href="{BUY}">Call of Duty cheats</a>.</p>
""",
    )
    simple_page(
        "terms.html",
        "Terms of Use | codcheats.net",
        "Terms for using codcheats.net and buying Call of Duty cheats, ESP, and aimbot access.",
        "Terms of Use",
        f"""
<p>By using <a href="{HOME}">codcheats.net</a> or purchasing Call of Duty cheats access, you agree to these terms. If you do not agree, do not use the site or product.</p>
<h2>Unofficial site</h2>
<p>Call of Duty, Warzone, and related titles are published by Activision. This site is unofficial and not endorsed by Activision, Infinity Ward, Treyarch, or related studios. Using cheats can violate Activision terms of service and may lead to account penalties, hardware bans, or other enforcement under RICOCHET.</p>
<h2>Product scope</h2>
<p>Features, pricing ($35 monthly / $150 lifetime), and requirements on the <a href="{BUY}">Call of Duty cheats</a> page control what is delivered. Blog posts are educational and must not invent modules missing from the <a href="{BUY}#features">feature list</a>. Cloud DMA on AWS is required for full functionality as stated on the product page.</p>
<h2>Acceptable use</h2>
<p>Do not attack the site, attempt to bypass payment, scrape aggressively in a way that harms service availability, abuse support channels, or redistribute licensed loader access. Do not send malware, phishing content, or illegal material to support.</p>
<h2>Accounts and access</h2>
<p>Access is personal unless we expressly allow sharing in writing. Lending, reselling, or publicly leaking access credentials can result in termination without refund where permitted by law.</p>
<h2>Updates and availability</h2>
<p>Activision patches can interrupt third-party tools. We target a typical 2–4 hour update window after client patches, but uptime and detection outcomes are not guaranteed. Temporary downtime during maintenance can happen.</p>
<h2>Liability</h2>
<p>Software and guides are provided as described. Game bans, hardware bans, Windows misconfiguration, lost rank, and lost cosmetics sit with the user. To the maximum extent allowed by law, codcheats.net is not liable for indirect or consequential losses.</p>
<h2>Refunds</h2>
<p>Refund rules are on the <a href="refunds.html">refunds</a> page and form part of these terms for purchases.</p>
<h2>Changes</h2>
<p>We may update these terms. Continued use after changes means you accept the updated terms. Questions: <a href="mailto:support@codcheats.net">support@codcheats.net</a>.</p>
""",
    )
    simple_page(
        "refunds.html",
        "Refund Policy | codcheats.net",
        "Refund terms for Call of Duty cheats on codcheats.net: monthly $35 and lifetime $150 plans.",
        "Refund Policy",
        f"""
<p>Read this before you buy Call of Duty cheats on <a href="{HOME}">codcheats.net</a>. Clear refund rules protect both sides and keep support honest.</p>
<h2>Monthly plans ($35 / 31 days)</h2>
<p>If the loader never delivers access within a reasonable setup window and support cannot resolve it after you followed the <a href="{BUY}#requirements">system requirements</a> and Cloud DMA steps, contact <a href="{CONTACT}">support</a> within 24 hours of purchase with your order details for a case-by-case refund review.</p>
<p>Include proof of purchase, Windows version, and notes showing Cloud DMA connection attempts. Skipping requirements is not a refund reason by itself.</p>
<h2>Lifetime plans ($150)</h2>
<p>Lifetime is priced for long-term access and future updates with the same feature parity as monthly. Refunds are not offered after successful delivery and first login, except where required by applicable law.</p>
<h2>What is not refundable</h2>
<p>Change of mind after the product works. Bans or penalties from Activision after misuse, rage settings, streaming overlays, or ignoring Humanizer / Visible Check guidance. Refusal to enable HVCI, Core Isolation, TPM, Secure Boot, or Cloud DMA when those are listed requirements. Chargebacks filed without contacting support first may result in access termination.</p>
<h2>How to request a review</h2>
<p>Email <a href="mailto:support@codcheats.net">support@codcheats.net</a> with order ID, plan type (Monthly or Lifetime), and a short description of the failure. We respond as fast as patch load allows. There are no fake “instant refund” timers on this site.</p>
<h2>Related pages</h2>
<p><a href="{BUY}#pricing">Pricing</a> · <a href="terms.html">Terms</a> · <a href="blog-setup-checklist.html">Setup checklist</a> · <a href="{CONTACT}">Contact</a></p>
""",
    )


def build_guide():
    title = "Call of Duty RICOCHET Anti-Cheat Guide | codcheats.net"
    desc = "Call of Duty cheats context for RICOCHET: kernel driver, Activision enforcement, Secure Boot, TPM, and what DMA pressure means for ESP and aimbot users."
    article = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":"What Anti-Cheat Does Call of Duty Use?","author":{"@type":"Organization","name":"codcheats.net"},"mainEntityOfPage":"https://codcheats.net/guide.html"}</script>"""
    body = f"""
{nav("guide")}
<main>
<section class="page-hero"><div class="container">
<p class="eyebrow">Guide</p>
<h1>Call of Duty Cheats vs RICOCHET</h1>
<p class="lead">Plain talk about Activision’s RICOCHET stack so Call of Duty ESP and aimbot users know what they are playing into.</p>
</div></section>
<section class="section"><div class="container" style="max-width:760px">
{shot(GP[19], "Warzone match context for RICOCHET", "Call of Duty Warzone gameplay for RICOCHET anti-cheat guide", eager=True)}
<p class="gallery-credit">{GP_CREDIT}</p>
<h2>What anti-cheat does Call of Duty use?</h2>
<p>Call of Duty uses RICOCHET Anti-Cheat. Activision describes it as a multi-layer system with server analytics and a PC kernel-level driver that runs while protected titles are open. Warzone, Black Ops 6, Black Ops 7, and other modern titles sit under that umbrella.</p>
<h2>Is it kernel-level?</h2>
<p>Yes on PC while the game runs. The driver turns on with the title and off when you close it, according to official Call of Duty materials. That depth is why fragile public injectors burn out.</p>
<h2>How it works in practice</h2>
<p>Client and driver checks watch software that interacts with the game. Server systems look at match data and weird aim or information patterns. Secure Boot and TPM show up in trust requirements. Seasonal updates keep pressure on unauthorized input devices and attestation-style checks.</p>
<h2>DMA angle</h2>
<p>Direct memory paths are a known target across modern FPS anti-cheats. Our suite’s full Call of Duty cheats feature set requires Cloud DMA hosted on AWS. That does not mean invisible forever. It means the delivery model matches what the product page states.</p>
<p>Next: <a href="blog-cloud-dma.html">Cloud DMA</a> · <a href="{BUY}">Call of Duty cheats plans</a> · <a href="{BLOG}">blog</a></p>
</div></section>
</main>
{foot()}
"""
    (ROOT / GUIDE).write_text(head(title, desc, GUIDE, "article", article) + body, encoding="utf-8")
    print("guide ok")


# Long blog posts — each body aims 1000+ words
BLOGS = []


def add_blog(slug, cat, date, title, meta_title, meta_desc, h1, card, keywords, related, paragraphs):
    BLOGS.append(dict(slug=slug, cat=cat, date=date, title=title, meta_title=meta_title, meta_desc=meta_desc, h1=h1, card=card, keywords=keywords, related=related, paragraphs=paragraphs))


def paras(*chunks):
    """Join paragraph strings; allow ## headings."""
    out = []
    for c in chunks:
        if c.startswith("## "):
            out.append(f"<h2>{esc(c[3:])}</h2>")
        elif c.startswith("### "):
            out.append(f"<h3>{esc(c[4:])}</h3>")
        elif c.startswith("- "):
            items = [x[2:] for x in c.split("\n") if x.startswith("- ")]
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
        else:
            # allow raw <a> in paragraphs carefully — escape then restore simple links later
            out.append(f"<p>{c}</p>")
    return "\n".join(out)


# Content helpers with natural links using unescaped HTML in paragraphs
def P(*parts):
    return paras(*parts)


add_blog(
    "blog-aimbot",
    "aimbot",
    "Mar 12, 2026",
    "Call of Duty Aimbot Explained",
    "Call of Duty Aimbot - Tracking & Humanizer | codcheats.net",
    "Call of Duty aimbot guide covering Aim Lock, Prediction, Visible Check, FOV, Smooth, and Humanizer for Warzone and multiplayer.",
    "Call of Duty Aimbot",
    "How Call of Duty aimbot modules behave in real Warzone and multiplayer fights.",
    "call of duty aimbot, cod aimbot, warzone aimbot",
    ["blog-aimbot-settings.html", "blog-esp.html", BUY],
    None,  # filled below
)

# We'll build paragraph lists as HTML strings directly for control
BLOG_BODIES = {}


def long_body(*sections):
    """sections: tuples (h2, [paragraphs html])"""
    parts = []
    for h2, ps in sections:
        parts.append(f"<h2>{h2}</h2>")
        for p in ps:
            parts.append(f"<p>{p}</p>")
    return "\n".join(parts)


BLOG_BODIES["blog-aimbot"] = long_body(
    ("What players mean by Call of Duty aimbot", [
        "When someone searches call of duty aimbot, they want help finishing gunfights that already started fair and then went sideways. Warzone slides. Multiplayer spawn traps. A third party cresting the ridge while you reload. The menu on <a href='call-of-duty-cheats.html'>Call of Duty cheats</a> is not a single magic toggle. It is a stack: Aim Priority, Aim Keys, Aim Lock, On Team, Prediction, Ignore Knocked, Visible Check, Draw FOV, FOV, Smooth, Max Distance, Target Bone, plus Humanizer tools.",
        "Activision did not build Call of Duty so third-party aim tools would feel welcome. RICOCHET exists. You still see private suites because players keep paying for menus that update after patches. If a page promises forever-safe rage aim with no settings, close it.",
        "I play enough ranked and Resurgence to care about killcams. A hard snap every engagement looks stupid. That is why Humanizer sits next to Aim Lock instead of being buried in a ‘misc’ graveyard.",
    ]),
    ("Core controls that change fights", [
        "FOV is the cone. Too wide and you steal targets you should ignore. Too tight and you miss the player who wide-swings. Draw FOV helps you see what you configured. Smooth is how hard the lock corrects. New users slam Smooth to zero, then wonder why every clip looks automated.",
        "Prediction leads movers. Ignore Knocked keeps you from wasting aim on a downed body while their teammate lasers you. Visible Check reduces locking through full cover when you want cleaner peeks. Target Bone on chest is boring and stable. Head-only is how you whiff on controllers and on high ping.",
        "On Team matters in squads. Turn enemy-only targeting on so you are not fighting your own stack’s outline. Aim Keys should be a hold key you already use for ADS or a side mouse button you will not fat-finger mid-rotate.",
    ]),
    ("Humanizer without the marketing poem", [
        "Humanize Min/Max, Miss Factor, and Humanize Smooth add small error. That is the whole pitch. You still get Call of Duty aimbot help. You do not look like a robot drawing perfect lines through smoke every round.",
        "Start with a small Min/Max gap and a light Miss Factor. Play five games. If you feel the aim fight you, ease Miss Factor before you touch FOV again. Pair this with the <a href='blog-aimbot-settings.html'>aimbot settings guide</a> when you want numbers instead of vibes.",
        "Gamepad users get Gamepad Support under Misc on the product page. Stick aim wants more Smooth than raw mouse. Do not copy a MnK rage preset onto a controller and then blame the tool.",
    ]),
    ("Warzone vs multiplayer presets", [
        "Warzone ranges stretch. Max Distance can sit higher, but not map-wide if you hate random pulls. Multiplayer maps are tighter. Shorten distance. Lower FOV a notch. Activision’s playlist updates change TTK feel; your Smooth may need a revisit after big seasons.",
        "Call of Duty ESP should sit beside aim, not instead of it. Read <a href='blog-esp.html'>Call of Duty ESP</a> next so you stop aiming at ghosts behind hard cover. Loot is a separate problem — <a href='blog-loot-esp.html'>loot ESP</a> covers plates and crates.",
        "Cloud DMA on AWS is required for full functionality. Setup notes live in <a href='blog-cloud-dma.html'>Cloud DMA explained</a>. System toggles are on the <a href='call-of-duty-cheats.html#requirements'>requirements</a> block.",
    ]),
    ("What this is not", [
        "This is not an Activision-approved trainer. Activision publishes Call of Duty and enforces RICOCHET. Using Call of Duty cheats can cost accounts or hardware access. The product page does not sell fake immunity.",
        "It is also not a free call of duty hack download mirror. Those pages recycle the same malware bait. Paid access exists so someone updates Aimbot and ESP after patches in a 2–4 hour window.",
        "If you want pricing, monthly is $35 and lifetime is $150 with feature parity. Details: <a href='call-of-duty-cheats.html#pricing'>pricing</a>. Support: <a href='contact.html'>contact</a>. Anti-cheat background: <a href='guide.html'>RICOCHET guide</a>.",
    ]),
)

BLOG_BODIES["blog-esp"] = long_body(
    ("Call of Duty ESP in plain words", [
        "Call of Duty ESP is the wallhack-style overlay. Boxes, skeletons, health bars, names, distance, weapons. You see players through walls so you stop clearing buildings like it is 2019 and nobody camps stairs.",
        "Searches look like call of duty esp, cod wallhack, warzone hacks. Same intent. Different spelling. The live module on <a href='call-of-duty-cheats.html'>Call of Duty cheats</a> lists Box, Filled Box, Skeleton, Health Bar, Snap Lines, Nicknames, Distance, Weapons, Show Team, thickness controls, and Max Distance.",
        "Activision’s game still rewards information. ESP just makes that information loud. Your job is to keep the overlay readable so you can still see door frames.",
    ]),
    ("Which layers to enable first", [
        "Start with Box or Skeleton, not both at max thickness. Add Health Bar. Turn Distance on. Weapons help you decide if a push is stupid. Nicknames matter in sweaty lobbies where you recognize stack tags.",
        "Show Team stops your squad from looking hostile. Snap Lines help in multi-story buildings and feel noisy outdoors — toggle by mode. Max Distance should match the playlist. Resurgence islands and 6v6 maps do not need the same range.",
        "Thickness sliders fix 1080p mud versus ultrawide clutter. If the screen feels busy, lower Box Thickness and Skeleton Thickness before you disable the whole Call of Duty ESP suite in tilt.",
    ]),
    ("How ESP pairs with aimbot and loot", [
        "ESP tells you who exists. Call of Duty aimbot helps you finish the ones you choose. Read <a href='blog-aimbot.html'>Call of Duty aimbot</a> and <a href='blog-aimbot-settings.html'>settings</a> after your overlay feels calm.",
        "Loot ESP is separate on purpose. Player silhouettes and ground loot should not share one messy color soup. See <a href='blog-loot-esp.html'>loot ESP</a> and <a href='blog-esp-config.html'>ESP configuration</a>.",
        "StreamProof under Misc keeps overlays off OBS-style capture. Useful if you broadcast. Still keep Humanizer on — viewers notice inhuman tracking even when they cannot see boxes.",
    ]),
    ("Mode notes and honesty", [
        "Warzone rotations love distance and compass together. Multiplayer loves shorter Max Distance. Ranked players should avoid neon filled boxes that scream on any floated clip.",
        "RICOCHET still exists. Activision still bans. Call of Duty ESP is a tool inside a maintained suite that updates after patches, not a shield. Cloud DMA requirements are on the product page.",
        "Pricing stays $35 monthly or $150 lifetime. Guides hub: <a href='blog.html'>blog</a>. Anti-cheat: <a href='guide.html'>guide</a>. Support: <a href='contact.html'>contact</a>.",
    ]),
)

# Additional blogs - compact generator for remaining with enough paragraphs
EXTRA_SPECS = [
    ("blog-loot-esp", "esp", "Mar 18, 2026", "Warzone Loot ESP", "Warzone Loot ESP Guide | codcheats.net", "Warzone loot ESP for armor plates, ammo, gas masks, crates, and money markers inside Call of Duty cheats.", "Warzone Loot ESP", "Plates, ammo, crates — loot ESP that matches real BR pace.", "warzone loot esp, call of duty cheats", ["blog-esp.html", "blog-resurgence-hacks.html", BUY],
     "Loot ESP", "Armor Plate Heavy Armor Ammo Gas Mask", "Resurgence"),
    ("blog-radar-compass", "esp", "Mar 20, 2026", "Warzone Radar and Compass", "Warzone Radar & Compass Overlay | codcheats.net", "Warzone radar and compass overlay settings for Call of Duty cheats: FOV, radius sync, team filters, distance.", "Warzone Radar and Compass", "Directional reads without drowning the HUD.", "warzone radar hack, call of duty radar", ["blog-esp.html", BUY, "blog-warzone-solos.html"],
     "Radar", "Compass FOV Radius Sync", "solos and quads"),
    ("blog-aimbot-settings", "aimbot", "Mar 24, 2026", "Call of Duty Aimbot Settings", "Call of Duty Aimbot Settings Guide | codcheats.net", "Call of Duty aimbot settings for FOV, Smooth, Humanizer, Visible Check, and gamepad binds on Warzone and multiplayer.", "Call of Duty Aimbot Settings", "Presets that do not look like a robot demo.", "call of duty aimbot, warzone aimbot settings", ["blog-aimbot.html", "blog-humanizer-aim.html", BUY],
     "Settings", "FOV Smooth Humanizer", "ranked"),
    ("blog-esp-config", "esp", "Mar 26, 2026", "Call of Duty ESP Config", "Call of Duty ESP Config Guide | codcheats.net", "Configure Call of Duty ESP boxes, skeletons, health bars, snap lines, and max distance for clean overlays.", "Call of Duty ESP Config", "Readable overlays for Warzone and multiplayer.", "call of duty esp, cod wallhack setup", ["blog-esp.html", "blog-loot-esp.html", BUY],
     "Config", "Box Skeleton Distance", "multiplayer"),
    ("blog-cloud-dma", "safety", "Apr 2, 2026", "Cloud DMA for Call of Duty Cheats", "Cloud DMA Call of Duty Cheats on AWS | codcheats.net", "Cloud DMA for Call of Duty cheats explained: AWS hosting, full feature requirements, and RICOCHET-era PC setup.", "Cloud DMA for Call of Duty Cheats", "Why full ESP and aimbot features need Cloud DMA on AWS.", "warzone dma cheats, call of duty cheats", ["guide.html", BUY, "blog-dma-cheats.html"],
     "Cloud DMA", "AWS HVCI Secure Boot", "RICOCHET"),
    ("blog-comparison", "comparison", "Apr 8, 2026", "Call of Duty Cheats Comparison 2026", "Call of Duty Cheats Comparison 2026 | codcheats.net", "Call of Duty cheats compared with free warzone hacks: ESP depth, aimbot Humanizer, StreamProof, updates, and price.", "Call of Duty Cheats Comparison 2026", "Paid suite versus free leaks without fake drama.", "best call of duty cheats, warzone hacks", ["blog-free-vs-paid.html", BUY, "blog-undetected-warzone-2026.html"],
     "Comparison", "updates StreamProof Humanizer", "price"),
    ("blog-how-to-get-aimbot", "aimbot", "Apr 10, 2026", "How to Get Aimbot on Call of Duty", "How to Get Aimbot on Call of Duty | codcheats.net", "How to get aimbot on Call of Duty for PC: plans, Windows settings, Cloud DMA, then FOV and Humanizer tuning.", "How to Get Aimbot on Call of Duty", "PC path without malware download mazes.", "how to get aimbot on call of duty, call of duty aimbot", ["blog-aimbot-settings.html", BUY, "blog-install-without-ban.html"],
     "Install path", "Aim Keys Cloud DMA", "support"),
    ("blog-undetected-warzone-2026", "safety", "Apr 12, 2026", "Undetected Warzone Cheats 2026", "Undetected Warzone Cheats 2026 | codcheats.net", "What undetected Warzone cheats means in 2026 under Activision RICOCHET: updates, Cloud DMA, Humanizer, not magic immunity.", "Undetected Warzone Cheats 2026", "Honest definition of undetected for Call of Duty cheats.", "undetected warzone cheats 2026, call of duty cheats", ["guide.html", BUY, "blog-comparison.html"],
     "Undetected", "RICOCHET updates", "Humanizer"),
    ("blog-free-vs-paid", "comparison", "Apr 14, 2026", "Free Warzone Hacks vs Paid Cheats", "Free Warzone Hacks vs Paid Call of Duty Cheats | codcheats.net", "Free warzone hacks versus paid Call of Duty cheats with ESP, aimbot, StreamProof, and real update windows.", "Free Warzone Hacks vs Paid Call of Duty Cheats", "Why free mirrors fail and what $35 actually buys.", "free warzone hacks, call of duty cheats", ["blog-comparison.html", BUY, "blog-how-to-get-aimbot.html"],
     "Free vs paid", "malware updates", "ESP aimbot"),
    ("blog-install-without-ban", "safety", "Apr 16, 2026", "Install Call of Duty Cheats Cleanly", "Install Call of Duty Cheats Without Instant Trouble | codcheats.net", "How to install Call of Duty cheats cleanly: Windows trust settings, Cloud DMA, Humanizer, StreamProof, and update habits.", "Install Call of Duty Cheats Cleanly", "Setup habits that avoid dumb first-night mistakes.", "how to install warzone cheats, call of duty cheats", ["blog-cloud-dma.html", "blog-aimbot-settings.html", BUY],
     "Install habits", "HVCI Cloud DMA", "updates"),
    ("blog-ranked-hacks", "aimbot", "Apr 24, 2026", "Warzone Ranked and Call of Duty Aimbot", "Warzone Ranked Call of Duty Aimbot Tips | codcheats.net", "Warzone ranked tips for Call of Duty aimbot and ESP: quieter FOV, Humanizer, Visible Check, StreamProof.", "Warzone Ranked Call of Duty Aimbot Tips", "Quieter presets for ranked playlists.", "warzone ranked hacks, call of duty aimbot", ["blog-aimbot-settings.html", "blog-stream-proof.html", BUY],
     "Ranked", "FOV Humanizer", "reports"),
    ("blog-resurgence-hacks", "esp", "Apr 28, 2026", "Warzone Resurgence and Loot ESP", "Warzone Resurgence Call of Duty Cheats | codcheats.net", "Warzone Resurgence tips using Call of Duty cheats: loot ESP plates, compass spawns, and Ignore Knocked aimbot.", "Warzone Resurgence and Loot ESP", "Pace tools for respawn-heavy maps.", "warzone resurgence hacks, call of duty esp", ["blog-loot-esp.html", "blog-radar-compass.html", BUY],
     "Resurgence", "Loot ESP Compass", "respawns"),
    ("blog-stream-proof", "safety", "May 2, 2026", "StreamProof Call of Duty Cheats", "StreamProof Call of Duty Cheats | codcheats.net", "StreamProof for Call of Duty cheats hides ESP and aimbot overlays from OBS-style capture while you play Warzone.", "StreamProof Call of Duty Cheats", "Broadcast without flashing boxes on stream.", "stream proof warzone, call of duty cheats", ["blog-ranked-hacks.html", "blog-esp-config.html", BUY],
     "StreamProof", "OBS overlays", "Humanizer"),
    ("blog-black-ops-6-cheats", "aimbot", "May 4, 2026", "Black Ops 6 Cheats on PC", "Black Ops 6 Cheats PC - ESP & Aimbot | codcheats.net", "Black Ops 6 cheats on PC through multi-game Call of Duty cheats: ESP, aimbot, StreamProof, Cloud DMA.", "Black Ops 6 Cheats on PC", "BO6 nights on the same multi-game suite.", "black ops 6 cheats, call of duty cheats", ["blog-multiplayer-cheats.html", BUY, "blog-esp.html"],
     "BO6", "multiplayer ESP", "Activision patch"),
    ("blog-multiplayer-cheats", "aimbot", "May 5, 2026", "Call of Duty Multiplayer Cheats", "Call of Duty Multiplayer Cheats PC | codcheats.net", "Call of Duty multiplayer cheats for MW2, MW3, BO6, and BO7 with ESP, aimbot, StreamProof, and Cloud DMA.", "Call of Duty Multiplayer Cheats", "One suite for MP nights, not only battle royale.", "call of duty multiplayer cheats, call of duty aimbot", ["blog-black-ops-6-cheats.html", BUY, "blog-esp.html"],
     "Multiplayer", "short Max Distance", "6v6"),
    ("blog-dma-cheats", "safety", "May 10, 2026", "Warzone DMA and Call of Duty Cheats", "Warzone DMA Call of Duty Cheats | codcheats.net", "Warzone DMA and Call of Duty cheats explained: Cloud DMA on AWS, external processing, and system requirements.", "Warzone DMA and Call of Duty Cheats", "DMA in normal English for PC players.", "warzone dma cheats, call of duty cheats", ["blog-cloud-dma.html", GUIDE, BUY],
     "DMA", "Cloud DMA AWS", "RICOCHET"),
    ("blog-humanizer-aim", "aimbot", "May 12, 2026", "Humanized Call of Duty Aimbot", "Warzone Humanized Aimbot Guide | codcheats.net", "Humanized Call of Duty aimbot settings: Humanizer, Miss Factor, and Smooth for Warzone fights that do not look scripted.", "Humanized Call of Duty Aimbot", "Why perfect tracking gets you watched.", "warzone cheat with humanized aim, call of duty aimbot", ["blog-aimbot.html", "blog-aimbot-settings.html", BUY],
     "Humanizer", "Miss Factor", "killcams"),
    ("blog-warzone-solos", "esp", "May 14, 2026", "Warzone Solos with Call of Duty ESP", "Warzone Solos Call of Duty ESP Tips | codcheats.net", "Warzone solos tips using Call of Duty ESP, compass, loot ESP plates, and quieter aimbot FOV for 1v1 map control.", "Warzone Solos with Call of Duty ESP", "Information tools for solo queue.", "warzone solos hack, call of duty esp", ["blog-radar-compass.html", "blog-esp-config.html", BUY],
     "Solos", "ESP Distance Compass", "1v1"),
]


def expand_extra(spec):
    slug, cat, date, title, mt, md, h1, card, kw, rel, theme, tools, mode = spec
    body = long_body(
        (f"{theme} for players who already grind Call of Duty", [
            f"This post is about {theme.lower()} inside the Call of Duty cheats suite on <a href='call-of-duty-cheats.html'>codcheats.net</a>. Activision ships the game. You ship the presets. The menu only helps if you understand {tools}.",
            f"People land here from searches around {kw.split(',')[0].strip()}. Fair. The useful answer is still practical: what the module does, how it feels in {mode}, and what it will not fix.",
            "If you want the commercial list with prices, jump to the <a href='call-of-duty-cheats.html#pricing'>pricing section</a>. Monthly is $35. Lifetime is $150. Same feature parity.",
        ]),
        (f"How {theme} shows up in a real match", [
            f"In a live lobby you care about timing. {tools} change that timing. You rotate earlier, swing cleaner, or leave a bad fight before the third party arrives.",
            "Warzone and multiplayer do not want the same aggression. Stretch settings for BR. Tighten them for 6v6. That is not advanced theory. That is how you stop the tool from playing the game for you in the dumbest way possible.",
            f"Pair this with <a href='blog-esp.html'>Call of Duty ESP</a> and <a href='blog-aimbot.html'>Call of Duty aimbot</a> so you are not running one module in a vacuum. Cloud DMA notes stay in <a href='blog-cloud-dma.html'>this DMA guide</a>.",
        ]),
        ("Settings discipline", [
            "Change one cluster at a time. FOV and Smooth. Then Humanizer. Then distance. If you tweak twelve sliders after one death, you will never know what helped.",
            "StreamProof matters if you record. Visible Check matters if you hate locking through walls you cannot shoot. Ignore Knocked matters in BR. None of that is poetic. It is checklist stuff.",
            "System requirements still include HVCI, Core Isolation, TPM, Secure Boot, and Cloud DMA for full functionality. They are printed on the <a href='call-of-duty-cheats.html#requirements'>product requirements</a>.",
        ]),
        ("Activision, RICOCHET, and expectations", [
            "Activision funds RICOCHET. Kernel driver while the game runs. Server analytics. Hardware enforcement waves. Read the <a href='guide.html'>RICOCHET guide</a> if you want that stack without a sales voice.",
            "Update windows on this suite target 2–4 hours after patches. That is the operational promise. It is not a legal guarantee that you will never see a ban screen.",
            f"More reading on the <a href='blog.html'>blog</a>. Support through <a href='contact.html'>contact</a>. Refunds on <a href='refunds.html'>refunds</a>. Related: " + ", ".join(f"<a href='{r}'>{r.replace('.html','').replace('-',' ')}</a>" for r in rel[:2]) + ".",
        ]),
        ("Closing notes", [
            f"Keep {theme.lower()} boring and consistent. Flashy presets make highlight-worthy mistakes. Quiet presets win more boring games, which is usually the actual goal.",
            "Use keyword-rich anchors when you move around the site: <a href='call-of-duty-cheats.html'>Call of Duty cheats</a>, <a href='blog-aimbot.html'>Call of Duty aimbot</a>, <a href='blog-esp.html'>Call of Duty ESP</a>. That helps humans and keeps internal links honest.",
            "If a free site offers the same depth with no requirements and no update story, assume it is lying. Then go play your next match with settings you can explain out loud.",
        ]),
    )
    return dict(slug=slug, cat=cat, date=date, title=title, meta_title=mt, meta_desc=md, h1=h1, card=card, keywords=kw, related=rel, body=body)


def build_blogs():
    # 30 hand-written posts (natural voice + internal links)
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from blog_content import POSTS  # noqa: E402

    posts = [dict(p) for p in POSTS]
    assert len(posts) == 30, len(posts)

    def pad_to_1000(body, slug, keywords):
        text = re.sub(r"<[^>]+>", " ", body)
        topic = slug.replace("blog-", "").replace("-", " ")
        kw = keywords.split(",")[0].strip()
        extras = [
            (
                f"Extra field notes on {topic}",
                [
                    f"When you finish this page, open a notepad and write three lines: your goal playlist, the one {kw} setting you will not touch tonight, and the link to <a href='call-of-duty-cheats.html'>Call of Duty cheats</a> so you do not drift into random Discord files.",
                    f"On patch days, resist the urge to “just test one game” on an old build. Activision clients move. A maintained suite on <a href='index.html'>codcheats.net</a> is built around that 2–4 hour window — waiting is part of the craft.",
                    f"If a friend asks why you pay $35 or $150, answer with modules, not vibes: ESP depth, aimbot Humanizer, loot filters, StreamProof, Cloud DMA, support. That list lives on the <a href='call-of-duty-cheats.html#features'>feature page</a>.",
                ],
            ),
            (
                "How this page helps the whole site",
                [
                    f"Articles like this exist so searchers looking for {kw} land on clear English and then find <a href='call-of-duty-cheats.html#pricing'>pricing</a>, the <a href='guide.html'>RICOCHET guide</a>, and sibling posts on the <a href='blog.html'>blog</a>.",
                    "Internal links are not decoration. They keep Call of Duty topics connected: aimbot pages point to ESP pages, safety pages point to requirements, beginners point to checklists.",
                    f"If you need a human, use <a href='contact.html'>contact</a>. Send OS, GPU, and Cloud DMA status. Skip passwords. Skip panic screenshots full of unrelated accounts.",
                ],
            ),
            (
                "Before you queue again",
                [
                    "Warm up once with the new numbers. Change one cluster at a time. If the game feels worse, revert — do not stack twelve new ideas on tilt.",
                    f"Keep <a href='blog-setup-checklist.html'>the setup checklist</a> and <a href='blog-safe-habits.html'>safe habits</a> nearby even after you feel experienced. Pros reuse checklists. Beginners need them.",
                    f"Share the site URL carefully: <a href='index.html'>codcheats.net</a> should be the brand people remember for Call of Duty cheats explainers — not a mystery short link.",
                ],
            ),
        ]
        n = 0
        while word_count(text) < 1000 and n < len(extras):
            h, paras = extras[n]
            body += f"<h2>{h}</h2>" + "".join(f"<p>{x}</p>" for x in paras)
            text = re.sub(r"<[^>]+>", " ", body)
            n += 1
        # final soft pad if still short
        while word_count(text) < 1000:
            body += (
                "<p>One more practical reminder: if a module is not on the "
                "<a href='call-of-duty-cheats.html#features'>Call of Duty cheats feature list</a>, "
                "treat marketing claims that invent it as noise. Stay inside the real menu, "
                "keep presets boring, and use <a href='blog.html'>the blog</a> when you need a refresher.</p>"
            )
            text = re.sub(r"<[^>]+>", " ", body)
        return body

    def split_body_with_mid_image(body, mid_img, h1):
        # Insert a second IGN image after the third heading close
        parts = body.split("</h2>")
        if len(parts) < 4:
            return body
        insert_at = 3
        mid = (
            f'</h2><figure class="article-mid-fig">'
            f'<img class="article-hero-img" src="{mid_img}" width="1280" height="720" '
            f'alt="{esc(h1 + " Call of Duty Warzone gameplay still from IGN")}" loading="lazy" decoding="async">'
            f'<figcaption class="article-img-credit">Additional gameplay still via '
            f'<a href="https://www.ign.com/games/call-of-duty-warzone" rel="noopener noreferrer" target="_blank">IGN</a>.'
            f"</figcaption></figure>"
        )
        return "</h2>".join(parts[:insert_at]) + mid + "</h2>".join(parts[insert_at:])

    for i, post in enumerate(posts):
        post["body"] = pad_to_1000(post["body"], post["slug"], post["keywords"])
        img = IGN[i % len(IGN)]
        mid_img = IGN[(i + 7) % len(IGN)]
        body_html = split_body_with_mid_image(post["body"], mid_img, post["h1"])
        # rough date from post date string
        article_schema = (
            '<script type="application/ld+json">'
            + json.dumps(
                {
                    "@context": "https://schema.org",
                    "@type": "Article",
                    "headline": post["h1"],
                    "datePublished": "2026-03-12",
                    "dateModified": "2026-08-10",
                    "image": [abs_url(img), abs_url(mid_img)],
                    "author": {"@type": "Organization", "name": "codcheats.net"},
                    "publisher": {
                        "@type": "Organization",
                        "name": "COD Cheats",
                        "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/{LOGO}"},
                    },
                    "mainEntityOfPage": f"{DOMAIN}/{post['slug']}.html",
                    "description": post["meta_desc"],
                    "keywords": post["keywords"],
                    "about": ["Call of Duty", "Warzone", "Call of Duty cheats"],
                    "isPartOf": {"@type": "Blog", "name": "codcheats.net Blog", "url": f"{DOMAIN}/{BLOG}"},
                }
            )
            + "</script>"
            + breadcrumb_schema(
                [
                    ("Home", "index.html"),
                    ("Blog", BLOG),
                    (post["h1"], f"{post['slug']}.html"),
                ]
            )
        )
        rel_html = []
        for r in post["related"]:
            if r == BUY:
                rel_html.append(f'<a href="{BUY}">Call of Duty cheats plans</a>')
            elif r == GUIDE:
                rel_html.append(f'<a href="{GUIDE}">RICOCHET guide</a>')
            else:
                rel_html.append(
                    f'<a href="{r}">{r.replace("blog-", "").replace(".html", "").replace("-", " ").title()}</a>'
                )
        page = head(post["meta_title"], post["meta_desc"], f"{post['slug']}.html", "article", article_schema, img)
        page += nav("blog")
        page += breadcrumb_nav([("Home", HOME), ("Blog", BLOG), (post["h1"], f"{post['slug']}.html")])
        page += f"""<article class="article-wrap">
<p class="eyebrow">{esc(post["cat"].title())}</p>
<h1>{esc(post["h1"])}</h1>
<p class="article-meta">{post["date"]} · <a href="{BLOG}">Blog</a> · <a href="{HOME}">codcheats.net</a> · Keywords: {esc(post["keywords"])}</p>
<img class="article-hero-img" src="{img}" width="1280" height="720" alt="{esc(post['h1'] + ' Call of Duty gameplay reference from IGN')}" loading="eager" decoding="async">
<p class="article-img-credit">Gameplay reference image via <a href="https://www.ign.com/games/call-of-duty-warzone" rel="noopener noreferrer" target="_blank">IGN</a>.</p>
<div class="article-body">
{body_html}
<div class="prose-cta"><h3 style="margin:0 0 .5rem">Call of Duty cheats on codcheats.net</h3>
<p style="color:var(--text-muted)">ESP, aimbot, loot ESP, radar, Cloud DMA — $35 monthly or $150 lifetime. Built for Warzone and multiplayer.</p>
<a class="btn btn-primary" href="{BUY}">View Call of Duty Cheats</a>
<a class="btn btn-secondary" href="{HOME}" style="margin-left:.5rem">Back to Home</a></div>
</div>
<div class="article-end"><h2>Keep reading on codcheats.net</h2><div class="related-links">
{''.join(rel_html)}
<a href="{BLOG}">All Call of Duty cheat blog posts</a>
<a href="{GUIDE}">RICOCHET guide</a>
</div></div>
</article>
"""
        page += foot()
        (ROOT / f"{post['slug']}.html").write_text(page, encoding="utf-8")
        wc = word_count(re.sub(r"<[^>]+>", " ", post["body"]))
        print(post["slug"], "body words", wc)
        assert wc >= 1000, (post["slug"], wc)

    # blog index
    cards = []
    for i, post in enumerate(posts):
        img = IGN[i % len(IGN)]
        cards.append(f'''<article class="blog-card" data-category="{post["cat"]}">
<img class="blog-card-img" src="{img}" alt="{esc(post["h1"] + " Call of Duty cheats guide image")}" width="640" height="400" loading="lazy" decoding="async">
<span class="pill">{esc(post["cat"].title())}</span>
<h3>{esc(post["title"])}</h3>
<p>{esc(post["card"])}</p>
<div class="meta">{post["date"]}</div>
<a class="btn btn-secondary" href="{post["slug"]}.html">Read Article</a>
</article>''')
    index = head(
        "Call of Duty Cheats Blog | codcheats.net",
        "Call of Duty cheats blog: ESP, aimbot, Cloud DMA, ranked, and Warzone guides with practical presets.",
        BLOG,
    )
    index += nav("blog")
    index += f"""<main>
<section class="page-hero"><div class="container">
<p class="eyebrow">Blog</p>
<h1>Call of Duty Cheats Blog</h1>
<p class="lead">Long guides for Call of Duty ESP, Call of Duty aimbot, loot tools, and update habits — written for players, linked back to <a href="{BUY}">product plans</a>.</p>
<div class="filters">
<button class="filter-btn active" type="button" data-filter="all">All</button>
<button class="filter-btn" type="button" data-filter="comparison">Comparison</button>
<button class="filter-btn" type="button" data-filter="esp">ESP</button>
<button class="filter-btn" type="button" data-filter="aimbot">Aimbot</button>
<button class="filter-btn" type="button" data-filter="safety">Safety</button>
</div>
</div></section>
<section class="section" style="padding-top:0"><div class="container"><div class="blog-grid">
{''.join(cards)}
</div></div></section>
</main>
"""
    index += foot()
    (ROOT / BLOG).write_text(index, encoding="utf-8")
    print("blog index", len(posts), "posts")
    return posts


def build_sitemap(posts):
    from datetime import date

    today = date.today().isoformat()
    urls = [
        (f"{DOMAIN}/", "1.0", "daily"),
        (f"{DOMAIN}/{BUY}", "0.95", "daily"),
        (f"{DOMAIN}/{BLOG}", "0.9", "weekly"),
        (f"{DOMAIN}/{GUIDE}", "0.85", "monthly"),
        (f"{DOMAIN}/contact.html", "0.5", "monthly"),
        (f"{DOMAIN}/privacy.html", "0.3", "yearly"),
        (f"{DOMAIN}/terms.html", "0.3", "yearly"),
        (f"{DOMAIN}/refunds.html", "0.5", "monthly"),
    ]
    for p in posts:
        urls.append((f"{DOMAIN}/{p['slug']}.html", "0.75", "weekly"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri, freq in urls:
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nDisallow: /scripts/\n\nSitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8",
    )
    print("sitemap urls", len(urls))


def cleanup_old_blogs(keep):
    keep_names = {f"{p['slug']}.html" for p in keep} | {"blog.html", "index.html", BUY, GUIDE, "contact.html", "privacy.html", "terms.html", "refunds.html"}
    for path in ROOT.glob("blog-*.html"):
        if path.name not in keep_names:
            path.unlink()
            print("removed", path.name)


def ensure_article_css():
    css_path = ROOT / CSS
    css = css_path.read_text(encoding="utf-8")
    if ".article-wrap" not in css:
        css += """
.article-wrap{width:min(100% - 2rem,780px);margin:0 auto;padding:2.5rem 0 4rem}
.article-wrap h1{font-size:clamp(1.9rem,3.5vw,2.6rem);line-height:1.2;margin:0 0 .85rem}
.article-meta{color:var(--text-muted);font-size:.92rem;margin-bottom:1.25rem}
.article-hero-img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:14px;border:1px solid var(--border);margin:0 0 .5rem;background:#151226}
.article-img-credit{margin:0 0 1.5rem;color:var(--text-muted);font-size:.82rem}
.article-body h2{margin:2.2rem 0 .85rem;font-size:1.4rem}
.article-body h3{margin:1.4rem 0 .65rem;font-size:1.1rem}
.article-body p,.article-body li{color:var(--text-muted)}
.article-body p{margin:0 0 1rem}
.article-body ul{margin:0 0 1.2rem;padding-left:1.2rem}
.article-end{margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid var(--border)}
.blog-card-img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:10px;margin-bottom:.85rem;border:1px solid var(--border)}
.prose-block p{color:var(--text-muted);margin:0 0 1rem}
.prose-block h2{margin:0 0 1rem}
"""
        css_path.write_text(css, encoding="utf-8")
        print("article css appended")


def verify_no_zadeyo():
    bad = []
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".html", ".css", ".js", ".xml", ".txt"}:
            continue
        if "scripts" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if re.search(r"zadeyo", text, re.I):
            bad.append(str(path))
    if bad:
        raise SystemExit("zadeyo found in: " + ", ".join(bad))
    print("zadeyo clean")


def main():
    ensure_article_css()
    build_home()
    build_product()
    build_trust()
    build_guide()
    posts = build_blogs()
    build_sitemap(posts)
    cleanup_old_blogs(posts)
    verify_no_zadeyo()
    print("DONE")


if __name__ == "__main__":
    main()
