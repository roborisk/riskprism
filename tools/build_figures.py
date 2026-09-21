#!/usr/bin/env python3
"""Render the paper figure PDFs into web-sized images under assets/images/.

Usage:
    python tools/build_figures.py /path/to/figure/pdf/directory

Requires: pymupdf, pillow
"""

import io
import os
import shutil
import sys

import pymupdf
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(REPO, "assets", "images")
PDF_DIR = os.path.join(REPO, "assets", "pdf")

# (pdf stem in the source directory, output name, target pixel width, format)
# Photographic figures go to JPEG; plots and screenshots stay lossless.
FIGURES = [
    ("highlevelapproach", "teaser", 1700, "jpg"),
    ("mainapproach", "approach", 2400, "jpg"),
    ("autolabeltool", "benchmark-labeling-tool", 1600, "png"),
    ("benchmarkqualitative", "benchmark-hazards", 2200, "jpg"),
    ("challengingmultiview", "benchmark-multiview", 1900, "jpg"),
    ("benchmarkquantitative", "benchmark-statistics", 1200, "png"),
    ("benchmarkablations", "results-safety-frontier", 1250, "png"),
    ("benchmarkquantiative_misprediction", "results-misprediction", 1400, "png"),
    ("qualitativeofflineexamples", "results-qualitative", 2100, "jpg"),
    ("realworldscenarios", "realworld-scenarios", 2600, "jpg"),
]


def main(src):
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)

    for stem, name, width, fmt in FIGURES:
        path = os.path.join(src, stem + ".pdf")
        if not os.path.exists(path):
            print(f"skip   {stem}.pdf (not found)")
            continue

        page = pymupdf.open(path)[0]
        zoom = width / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("ppm"))).convert("RGB")

        dst = os.path.join(IMG_DIR, f"{name}.{fmt}")
        if fmt == "jpg":
            img.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
        else:
            img.quantize(colors=256, method=Image.MAXCOVERAGE).save(
                dst, "PNG", optimize=True
            )

        shutil.copyfile(path, os.path.join(PDF_DIR, f"{name}.pdf"))
        print(f"wrote  {name}.{fmt}  {img.size[0]}x{img.size[1]}  "
              f"{os.path.getsize(dst) / 1024:.0f} KB")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
