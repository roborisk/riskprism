#!/usr/bin/env python3
"""Derive the header logo and favicons from assets/images/riskprism-logo.jpg.

Keys out the white JPEG background, trims the surrounding margin, and writes:
    assets/images/riskprism-logo.png   header logo, transparent
    assets/favicon-32.png              browser tab
    assets/favicon-192.png             high-DPI tab / Android
    assets/apple-touch-icon.png        iOS home screen, on white

Usage:
    python tools/build_logo.py

Requires: pillow, numpy
"""

import os

import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(REPO, "assets", "images", "riskprism-logo.jpg")

# The artwork's palest fill bottoms out near 211 and the background sits at 254,
# so the alpha ramp between these two leaves the light blue face fully opaque.
OPAQUE_BELOW = 235
CLEAR_ABOVE = 251


def main():
    src = Image.open(SOURCE).convert("RGB")
    rgb = np.asarray(src).astype(np.float32)

    whiteness = rgb.min(axis=2)
    alpha = np.clip((CLEAR_ABOVE - whiteness) / (CLEAR_ABOVE - OPAQUE_BELOW), 0, 1) * 255
    img = Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), "RGBA")

    img = img.crop(img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    pad = max(img.size) // 40
    trimmed = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    trimmed.paste(img, (pad, pad))

    side = max(trimmed.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(trimmed, ((side - trimmed.width) // 2, (side - trimmed.height) // 2))

    logo = trimmed.resize((round(trimmed.width * 512 / trimmed.height), 512), Image.LANCZOS)
    logo.save(os.path.join(REPO, "assets", "images", "riskprism-logo.png"), optimize=True)

    for size in (32, 192):
        square.resize((size, size), Image.LANCZOS).save(
            os.path.join(REPO, "assets", f"favicon-{size}.png"), optimize=True
        )

    # iOS composites transparent touch icons onto black, so flatten onto white.
    touch = Image.new("RGB", (180, 180), (255, 255, 255))
    icon = square.resize((164, 164), Image.LANCZOS)
    touch.paste(icon, (8, 8), icon)
    touch.save(os.path.join(REPO, "assets", "apple-touch-icon.png"), optimize=True)

    print("wrote logo and favicons")


if __name__ == "__main__":
    main()
