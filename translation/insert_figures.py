#!/usr/bin/env python3
"""جای‌گذاری تصاویر شکل‌ها در فایل‌های HTML (بسته‌ها، فصل‌ها و پیوست).

هر <figure> که figcaption آن با «شکل N-M.» آغاز می‌شود، به این ساختار تبدیل می‌شود:
    <figure …>
      <img src="figures/chapter-NN/figure-N-M.png" alt="…">
      <figcaption …><b>شکل N-M.</b> …</figcaption>
    </figure>
یادداشت جایگزین قدیمی («تصویر شکل در پی‌دی‌اف اصلی…») حذف می‌شود.
اجرای دوباره بی‌خطر است (idempotent).

Usage (از درون پوشهٔ translation):
    python3 insert_figures.py            # همهٔ chunk-*.html، chapter-*.html و appendix.html
    python3 insert_figures.py --check    # فقط گزارش، بدون نوشتن
"""
import argparse
import html as htmllib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FA2EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
IMG_STYLE = ("display:block;max-width:100%;height:auto;margin:0 auto .7rem;"
             "background:#fff;border:1px solid #e3e3e3;border-radius:3px;")
FIG_RE = re.compile(r'(?P<indent>[ \t]*)<figure(?P<attrs>[^>]*)>\s*'
                    r'(?:<img[^>]*>\s*)?'
                    r'(?P<cap><figcaption[^>]*>(?:(?!</figcaption>).)*</figcaption>)\s*'
                    r'(?:<small[^>]*>(?:(?!</small>).)*</small>\s*)?'
                    r'</figure>', re.S)
NUM_RE = re.compile(r'شکل\s*([۰-۹0-9]+)-([۰-۹0-9]+)')


def img_src(ch: int, n: int) -> str:
    return f"figures/chapter-{ch:02d}/figure-{ch}-{n}.png"


def img_tag(ch: int, n: int, caption_html: str) -> str:
    alt = re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", "", caption_html))).strip()
    return (f'<img src="{img_src(ch, n)}" alt="{htmllib.escape(alt)}" loading="lazy" '
            f'style="{IMG_STYLE}">')


def process(text: str, missing: list):
    count = 0

    def rep(m):
        nonlocal count
        cap = m.group("cap")
        num = NUM_RE.search(re.sub(r"<[^>]+>", "", cap)[:40])
        if not num:                                   # table-in-figure etc.
            return m.group(0)
        ch, n = int(num.group(1).translate(FA2EN)), int(num.group(2).translate(FA2EN))
        if not (HERE / img_src(ch, n)).exists():
            missing.append(f"{ch}-{n}")
            return m.group(0)
        count += 1
        ind = m.group("indent")
        return (f'{ind}<figure{m.group("attrs")}>\n'
                f'{ind}  {img_tag(ch, n, cap)}\n'
                f'{ind}  {cap}\n'
                f'{ind}</figure>')

    return FIG_RE.sub(rep, text), count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    files = [Path(f) for f in a.files] or sorted(
        list(HERE.glob("chunk-*.html")) + list(HERE.glob("chapter-*.html")) + list(HERE.glob("appendix.html")))
    total, missing = 0, []
    for f in files:
        t = f.read_text(encoding="utf-8")
        new, c = process(t, missing)
        total += c
        if new != t and not a.check:
            f.write_text(new, encoding="utf-8")
    print(f"figures with images: {total}; missing image files: {missing or 'none'}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
