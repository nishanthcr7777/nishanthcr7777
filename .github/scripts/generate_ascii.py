"""
generate_ascii.py
-----------------
Converts  assets/source.png  (or .jpg/.jpeg/.webp) into a styled ASCII-art
PNG saved as  assets/myself.png.

Run locally:
    pip install pillow ascii-magic
    python scripts/generate_ascii.py

Triggered automatically by .github/workflows/ascii-art.yml every Sunday.
"""

from pathlib import Path
from PIL import Image, ImageEnhance

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).resolve().parent.parent
ASSETS_DIR  = REPO_ROOT / "assets"
OUTPUT_PATH = ASSETS_DIR / "myself.png"

SOURCE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]
SOURCE_PATH = None
for ext in SOURCE_EXTENSIONS:
    candidate = ASSETS_DIR / f"source{ext}"
    if candidate.exists():
        SOURCE_PATH = candidate
        break


def generate(source: Path):
    import ascii_magic

    print(f"Source: {source}")

    img = Image.open(source).convert("RGB")
    w, h = img.size

    # Crop: focus on face + upper torso, trim sides slightly
    img = img.crop((int(w * 0.05), 0, int(w * 0.95), int(h * 0.80)))

    # Boost contrast, sharpness, brightness, saturation for crisper ASCII
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Sharpness(img).enhance(2.5)
    img = ImageEnhance.Brightness(img).enhance(1.15)
    img = ImageEnhance.Color(img).enhance(1.4)

    art = ascii_magic.AsciiArt.from_pillow_image(img)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    art.to_image_file(
        path=str(OUTPUT_PATH),
        columns=100,
        back="#0d1117",       # GitHub dark background
        monochrome=False,
        full_color=True,
        enhance_image=True,
        file_type="PNG",
        border_width=6,
    )
    print(f"Saved -> {OUTPUT_PATH}")


def placeholder():
    """Fallback: stylised NB initials on dark background."""
    from PIL import Image, ImageDraw, ImageFont

    W, H = 400, 450
    img = Image.new("RGB", (W, H), (13, 17, 23))
    draw = ImageDraw.Draw(img)
    draw.rectangle([4, 4, W-5, H-5], outline=(112, 165, 253), width=2)

    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 96)
        sub  = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
    except Exception:
        font = sub = ImageFont.load_default()

    text = "NB"
    bb = draw.textbbox((0,0), text, font=font)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text(((W-tw)//2, (H-th)//2 - 30), text, fill=(112,165,253), font=font)

    for label, y, color in [
        ("NISHANTH B",                (H//2)+55, (191,145,243)),
        ("BACKEND · AI-NATIVE SYSTEMS", (H//2)+78, (56,189,174)),
    ]:
        bb = draw.textbbox((0,0), label, font=sub)
        draw.text(((W-(bb[2]-bb[0]))//2, y), label, fill=color, font=sub)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT_PATH)
    print(f"Placeholder saved -> {OUTPUT_PATH}")


if __name__ == "__main__":
    if SOURCE_PATH:
        generate(SOURCE_PATH)
    else:
        print("No source image found - generating placeholder.")
        print("Add assets/source.png to use your own photo.")
        placeholder()
