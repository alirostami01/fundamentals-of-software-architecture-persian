#!/usr/bin/env python3
"""استخراج تصاویر شکل‌ها از PDF اصلی کتاب → figures/chapter-NN/figure-N-M.png

روش: هر عنوان «Figure N-M.» (قلم ایتالیک) در PDF پیدا می‌شود و نزدیک‌ترین تصویرِ
بالای آن در همان صفحه با وضوح 200dpi برش و ذخیره می‌شود (آیکون‌های کوچک نکته کنار گذاشته می‌شوند).

Usage (از ریشهٔ مخزن):
    .venv/bin/python translation/extract_figures.py [--dpi 200]
"""
import argparse
import glob
import re
from pathlib import Path

import pymupdf

OUT = Path(__file__).resolve().parent / "figures"
CAP_RE = re.compile(r"Figure (\d+)-(\d+)\. ")


def find_captions(doc):
    for p in range(doc.page_count):
        for b in doc[p].get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"])
                m = CAP_RE.match(t)
                if m and "It" in l["spans"][0]["font"]:
                    yield p, int(m.group(1)), int(m.group(2)), l["bbox"][1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=200)
    a = ap.parse_args()
    doc = pymupdf.open(glob.glob("*.pdf")[0])
    n = 0
    for page, ch, num, y in find_captions(doc):
        pg = doc[page]
        above = [i["bbox"] for i in pg.get_image_info()
                 if i["bbox"][3] <= y + 3 and i["bbox"][2] - i["bbox"][0] > 100]
        if not above:
            print(f"WARNING: no image for Figure {ch}-{num} (page {page})")
            continue
        box = max(above, key=lambda b: b[3])          # nearest image above the caption
        d = OUT / f"chapter-{ch:02d}"
        d.mkdir(parents=True, exist_ok=True)
        pg.get_pixmap(clip=pymupdf.Rect(box), dpi=a.dpi, alpha=False).save(d / f"figure-{ch}-{num}.png")
        n += 1
    print(f"{n} figures written to {OUT}")


if __name__ == "__main__":
    main()
