#!/usr/bin/env python3
"""جای‌گذاری تصاویر شکل‌ها در فایل‌های فصل‌ها (html/ و markdown/).

HTML — هر <figure> که figcaption آن با «شکل N-M.» آغاز می‌شود، به این ساختار تبدیل می‌شود:
    <figure …>
      <img src="../figures/chapter-NN/figure-N-M.png" alt="…">
      <figcaption …><b>شکل N-M.</b> …</figcaption>
    </figure>
Markdown — پیش از هر سطر «> **شکل N-M.** عنوان» یک سطر تصویر افزوده می‌شود:
    ![شکل N-M. عنوان](../figures/chapter-NN/figure-N-M.png)
اجرای دوباره بی‌خطر است (idempotent).

Usage (از ریشهٔ مخزن):
    python3 insert_figures.py            # html/chapter-*.html، html/appendix.html و markdown/chapter-*.md
    python3 insert_figures.py --check    # فقط گزارش، بدون نوشتن
پس از آن، book.md و book.html را با build_book.py دوباره بسازید.
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
    """Path relative to html/ and markdown/ (figures/ sits at the repository root)."""
    return f"../figures/chapter-{ch:02d}/figure-{ch}-{n}.png"


def img_file(ch: int, n: int) -> Path:
    return HERE / "figures" / f"chapter-{ch:02d}" / f"figure-{ch}-{n}.png"


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
        if not img_file(ch, n).exists():
            missing.append(f"{ch}-{n}")
            return m.group(0)
        count += 1
        ind = m.group("indent")
        return (f'{ind}<figure{m.group("attrs")}>\n'
                f'{ind}  {img_tag(ch, n, cap)}\n'
                f'{ind}  {cap}\n'
                f'{ind}</figure>')

    return FIG_RE.sub(rep, text), count


MD_CAP_RE = re.compile(r"^> \*\*(شکل ([۰-۹0-9]+)-([۰-۹0-9]+)\.)\*\* ?(.*)$")


def process_md(text: str, missing: list):
    out, count = [], 0
    for line in text.split("\n"):
        m = MD_CAP_RE.match(line)
        if m:
            ch, n = int(m.group(2).translate(FA2EN)), int(m.group(3).translate(FA2EN))
            if not img_file(ch, n).exists():
                missing.append(f"{ch}-{n}")
            else:
                count += 1
                alt = re.sub(r"[\[\]*`]", "", f"{m.group(1)} {m.group(4)}").strip()
                img = f"![{alt}]({img_src(ch, n)})"
                has_img = len(out) >= 2 and out[-2].lstrip("> ").startswith("![") and out[-1] in ("", ">")
                if has_img:
                    del out[-2:]
                # inside a sidebox (previous line quoted) the image must stay inside the blockquote
                quoted = bool(out) and out[-1].startswith(">")
                out += [f"> {img}", ">"] if quoted else [img, ""]
        out.append(line)
    return "\n".join(out), count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    files = [Path(f) for f in a.files] or sorted(
        list((HERE / "html").glob("chapter-*.html")) + [HERE / "html" / "appendix.html"]
        + list((HERE / "markdown").glob("chapter-*.md")))
    total, missing = 0, []
    for f in files:
        t = f.read_text(encoding="utf-8")
        new, c = (process_md if f.suffix == ".md" else process)(t, missing)
        total += c
        if new != t and not a.check:
            f.write_text(new, encoding="utf-8")
    print(f"figures with images: {total} (HTML + Markdown); missing image files: {missing or 'none'}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
