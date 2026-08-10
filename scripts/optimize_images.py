"""Convert gameplay JPGs to resized WebP for Lighthouse image delivery."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GP = ROOT / "images" / "gameplay"
MAX_W = 960
QUALITY = 72


def convert_one(src: Path) -> Path:
    out = src.with_suffix(".webp")
    im = Image.open(src).convert("RGB")
    if im.width > MAX_W:
        h = int(im.height * (MAX_W / im.width))
        im = im.resize((MAX_W, h), Image.Resampling.LANCZOS)
    im.save(out, "WEBP", quality=QUALITY, method=6)
    print(f"{src.name} -> {out.name} ({out.stat().st_size // 1024} KiB)")
    return out


def main():
    files = sorted(GP.glob("cod-*.jpg"))
    if not files:
        raise SystemExit("no gameplay jpgs found")
    for src in files:
        convert_one(src)
    # keep a slightly smaller hero if helpful
    hero = ROOT / "images" / "hero-bg.webp"
    if hero.exists():
        im = Image.open(hero).convert("RGB")
        if im.width > 1400:
            h = int(im.height * (1400 / im.width))
            im = im.resize((1400, h), Image.Resampling.LANCZOS)
        im.save(hero, "WEBP", quality=78, method=6)
        print(f"hero-bg.webp ({hero.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
