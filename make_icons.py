#!/usr/bin/env python3
"""Generate MOCE PWA icons with Pillow (no external converters needed)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "icons")
os.makedirs(OUT, exist_ok=True)

STEEL = (22, 33, 46, 255)      # #16212E
STEEL_D = (12, 20, 29, 255)
ORANGE = (255, 122, 24, 255)   # #FF7A18
WHITE = (255, 255, 255, 255)


def font(size):
    for p in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default(size)


def make(size, pad_ratio, path, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    pad = int(size * pad_ratio)
    # background rounded square (full bleed for maskable)
    r = 0 if maskable else int(size * 0.22)
    box = [0, 0, size - 1, size - 1] if maskable else [pad // 2, pad // 2, size - 1 - pad // 2, size - 1 - pad // 2]
    # steel gradient (two-stop, manual)
    top, bot = STEEL, STEEL_D
    grad = Image.new("RGBA", (size, size))
    gd = ImageDraw.Draw(grad)
    for y in range(size):
        t = y / max(1, size - 1)
        c = tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(4))
        gd.line([(0, y), (size, y)], fill=c)
    # rounded mask
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle(box, radius=r if r else size // 2 if maskable else r, fill=255)
    if maskable:
        md.rectangle([0, 0, size - 1, size - 1], fill=255)
    img.paste(grad, (0, 0), mask)

    d = ImageDraw.Draw(img)
    # orange accent swoosh (bottom-right)
    if not maskable:
        d.pieslice([int(size * 0.55), int(size * 0.55), int(size * 1.35), int(size * 1.35)],
                   180, 360, fill=ORANGE)
        img.paste(Image.composite(img, img, mask), (0, 0))
        d = ImageDraw.Draw(img)

    # big "M" monogram
    safe = int(size * (0.42 if maskable else 0.52))
    f = font(int(safe * 1.15))
    text = "M"
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cx = (size - tw) / 2 - bb[0]
    cy = (size - th) / 2 - bb[1] - int(size * 0.02)
    d.text((cx, cy), text, font=f, fill=ORANGE)

    img.save(path, "PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    make(512, 0.0, os.path.join(OUT, "icon-512.png"))
    make(192, 0.0, os.path.join(OUT, "icon-192.png"))
    make(512, 0.18, os.path.join(OUT, "maskable-512.png"), maskable=True)
    make(180, 0.0, os.path.join(OUT, "apple-touch-icon.png"))
    print("done")
