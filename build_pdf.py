#!/usr/bin/env python3
"""ساخت PDF از فایل‌های HTML ترجمه.

خروجی‌ها:
  pdf/book.pdf                  کل کتاب: صفحهٔ عنوان، فهرست مطالب (با شمارهٔ صفحه و پیوند قابل کلیک)،
                                فصل‌های ۱ تا ۲۷، پیوست و واژه‌نامهٔ اصلی + نشانک‌های (Bookmarks) PDF
  pdf/chapters/chapter-NN.pdf   PDF جداگانهٔ هر فصل (با نشانک بخش‌های همان فصل)
  pdf/chapters/appendix.pdf     PDF پیوست

موتور تبدیل: Chromium (از راه Playwright) برای چیدمان درست راست‌به‌چپ و شکل‌دهی حروف فارسی،
و PyMuPDF برای نشانک‌ها، شمارهٔ صفحه‌های فهرست و فشرده‌سازی. فونت‌ها از pdf/fonts بارگذاری می‌شوند
(Vazirmatn برای متن، DejaVu Sans Mono برای کد) و به نصب فونت روی سیستم نیازی نیست.

پیش‌نیازها (یک بار):
    pip install playwright pymupdf
    playwright install chromium

اجرا (از ریشهٔ مخزن):
    python3 build_pdf.py                      # کتاب + همهٔ فصل‌ها و پیوست
    python3 build_pdf.py --book-only          # فقط pdf/book.pdf
    python3 build_pdf.py --chapters-only      # فقط PDF فصل‌ها
    python3 build_pdf.py --chapters 1 15 27   # فقط فصل‌های مشخص (0 = پیوست)
    python3 build_pdf.py --chromium /path/to/chrome   # استفاده از Chromium/Chrome دیگر
    python3 build_pdf.py --page-size Letter --font-size 12
    python3 build_pdf.py --out-dir /tmp/pdf-test   # خروجی در پوشهٔ دیگر (برای آزمایش)

ورودی: فایل‌های html/chapter-NN.html، html/appendix.html و واژه‌نامهٔ markdown/glossary.md؛
تصاویر از figures/ خوانده می‌شوند. اگر HTMLها را ویرایش کردید، پیش از اجرا insert_figures.py را اجرا کنید.
"""
import argparse
import html as htmllib
import os
import re
import sys
import shutil
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_book import (HTML_DIR, MASTER_H, NOTE, PARTS, SUBTITLE, TITLE_EN, TITLE_FA,  # noqa: E402
                        VERSION, VERSION_DATE, VERSION_NOTE,
                        front_items, gloss_html, master_rows, units)

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
OUT = HERE / "pdf"
FONTS = HERE / "pdf" / "fonts"
GLOSS_CHAPTER_H = "واژه‌نامهٔ اختصاصی این فصل"
PLACEHOLDER = "۸۸۸"          # جای شمارهٔ صفحه در گذر نخست (پهن‌ترین حالت سه‌رقمی)


def default_chromium():
    if os.environ.get("CHROMIUM_PATH"):
        return os.environ.get("CHROMIUM_PATH")
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        p = shutil.which(name)
        if p:
            return p
    return None


# ───────────────────────────── CSS ─────────────────────────────
def css(page_size: str, font_pt: float) -> str:
    f = FONTS.as_uri()
    return f"""
@font-face {{ font-family: 'VazirPDF'; src: url('{f}/Vazirmatn-Regular.ttf'); font-weight: 400; }}
@font-face {{ font-family: 'VazirPDF'; src: url('{f}/Vazirmatn-Bold.ttf'); font-weight: 700; }}
@font-face {{ font-family: 'MonoPDF'; src: url('{f}/DejaVuSansMono.ttf'); font-weight: 400; }}
@font-face {{ font-family: 'MonoPDF'; src: url('{f}/DejaVuSansMono-Bold.ttf'); font-weight: 700; }}

@page {{
  size: {page_size};
  margin: 20mm 18mm 18mm 18mm;
  @bottom-center {{ content: counter(page, persian); font-family: 'VazirPDF'; font-size: 9pt; color: #666; }}
}}
@page cover {{ @bottom-center {{ content: none; }} }}
@page bookcover {{
  size: {page_size};
  margin: 0;
  @bottom-center {{ content: none; }}
}}

.book-cover-image {{
  page: bookcover;
  width: 100vw;
  height: 100vh;
  margin: 0 !important;
  padding: 0 !important;
  break-after: page;
  overflow: hidden;
  background: #0d1b2a;
}}
.book-cover-image img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}}

html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; font-family: 'VazirPDF', sans-serif; font-size: {font_pt}pt; line-height: 1.9; color: #1a1a1a; }}

/* کامپوننت‌های HTML برای صفحه نمایش طراحی شده‌اند؛ برای چاپ، قاب و عرض محدود حذف می‌شود */
article {{
  max-width: none !important; margin: 0 !important; padding: 0 !important;
  border: none !important; border-radius: 0 !important; box-shadow: none !important;
  font-family: 'VazirPDF', sans-serif !important; line-height: 1.9 !important;
}}
article.unit {{ break-before: page; }}
article.unit:first-child {{ break-before: auto; }}
article h1 {{ font-size: 20pt !important; }}
article h3 {{ font-size: 14.5pt !important; }}
article h4 {{ font-size: 12.5pt !important; }}

bdi[style*="monospace"], code, pre, pre *, td[style*="monospace"] {{ font-family: 'MonoPDF', monospace !important; }}
bdi[style*="monospace"] {{ font-size: .86em !important; display: inline !important;
  -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
pre {{ white-space: pre-wrap !important; overflow-wrap: anywhere; font-size: 8.3pt !important; line-height: 1.5 !important; }}

h1, h2, h3, h4, h5 {{ break-after: avoid; }}
p {{ orphans: 3; widows: 3; }}
figure, blockquote, aside, pre, tr {{ break-inside: avoid; }}
figure img {{ max-height: 195mm; object-fit: contain; }}
table {{ font-size: .92em !important; }}
thead {{ display: table-header-group; }}
a {{ color: inherit; text-decoration: none; }}
/* خط‌چین‌ها در PDF کروم برای هر صفحه به‌صورت هزاران مستطیل کوچک تکرار می‌شوند و حجم را چند برابر می‌کنند */
hr {{ border: none !important; border-top: .6pt solid #c8c8c8 !important; }}

/* واژه‌نامهٔ اصلی: جدول فشرده‌تر */
#glossary table {{ font-size: 9pt !important; line-height: 1.45 !important; }}
#glossary td, #glossary th {{ padding: 1.2mm 2.5mm !important; }}

/* بخش‌های پیش از متن (حمایت از پروژه) روی صفحهٔ جداگانه */
section.support {{ break-after: page; margin-top: 30mm !important; padding: 8mm 9mm !important; }}
section.support a {{ overflow-wrap: anywhere; }}

/* صفحهٔ عنوان */
.cover {{ page: cover; height: 245mm; display: flex; flex-direction: column; justify-content: center;
          text-align: center; break-after: page; }}
.cover .t {{ font-size: 28pt; font-weight: 700; color: #2c5f8a; line-height: 1.6; }}
.cover .en {{ direction: ltr; font-size: 14pt; font-weight: 700; margin-top: 8mm; color: #333; }}
.cover .sub {{ font-size: 13pt; margin-top: 6mm; }}
.cover .note {{ font-size: 10pt; color: #666; margin-top: 20mm; }}
.cover .bar {{ width: 60mm; height: 2mm; background: #2c5f8a; margin: 10mm auto 0; }}

/* فهرست مطالب */
.toc {{ page: cover; break-after: page; }}
.toc .h {{ font-size: 20pt; font-weight: 700; color: #2c5f8a; border-bottom: 3px solid #2c5f8a;
           padding-bottom: 2mm; margin-bottom: 4mm; }}
.toc .part {{ font-weight: 700; color: #2c5f8a; margin: 4mm 0 1mm; font-size: 1.02em; }}
.toc a.row {{ display: flex; align-items: baseline; gap: 2mm; color: inherit; break-inside: avoid; }}
.toc a.row .dots {{ flex: 1; height: 1pt; min-width: 6mm; transform: translateY(-1.2mm);
  background: radial-gradient(circle, #999 0.5pt, transparent 0.6pt) repeat-x left center / 3pt 1pt; }}
.toc a.row .pg {{ min-width: 9mm; text-align: left; }}
.toc a.l1 {{ font-weight: 700; margin-top: 2.2mm; }}
.toc a.l2 {{ padding-right: 7mm; font-size: .93em; color: #333; }}
"""


# ───────────────────────────── HTML assembly ─────────────────────────────
def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def chapter_no(anchor: str):
    m = re.fullmatch(r"chapter-(\d+)", anchor)
    return int(m.group(1)) if m else None


def load_unit(anchor: str, base: str):
    """(article_html, [(level, id, title_html, title_text, heading_pos), ...], number of h1/h3 headings)."""
    t = (HTML_DIR / f"{base}.html").read_text(encoding="utf-8")
    t = re.sub(r"^<!--.*?-->\s*", "", t, flags=re.S).strip()
    t = t.replace("<article ", '<article class="unit" ', 1)
    entries = []
    # front matter before the H1 (e.g. «حمایت از پروژه» in chapter 1): own TOC entry/bookmark, own page
    for fid, ftitle in front_items(chapter_no(anchor)):
        if f'id="{fid}"' in t:
            entries.append((1, fid, ftitle, ftitle, None))
    # the unit anchor sits on the H1, so TOC page numbers point at the chapter title, not the front matter
    t = re.sub(r"<h1([^>]*)>", lambda m: f'<h1 id="{anchor}"{m.group(1)}>', t, count=1)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    entries.append((1, anchor, h1.group(1), strip_tags(h1.group(1)), 0))
    k = 0
    pos = 0

    def add_id(m):
        nonlocal k, pos
        inner = m.group(2)
        pos += 1
        if strip_tags(inner).startswith("واژه‌نامهٔ اختصاصی"):
            return m.group(0)          # chapter glossary: not listed in TOC/bookmarks
        k += 1
        sid = f"{anchor}-s{k}"
        entries.append((2, sid, inner, strip_tags(inner), pos))
        return f'<h3 id="{sid}"{m.group(1)}>{inner}</h3>'

    t = re.sub(r"<h3([^>]*)>(.*?)</h3>", add_id, t, flags=re.S)
    return t, entries, pos + 1


def glossary_article(rows):
    g = gloss_html(rows)
    g = re.sub(r"\s*<h3[^>]*>.*?</h3>", "", g, count=1)
    intro = (f'<p style="text-align:justify;">این واژه‌نامه همهٔ {str(len(rows)).translate(FA)} معادل مصوبِ '
             "به‌کاررفته در ترجمه را به ترتیب الفبایی واژهٔ انگلیسی در بر دارد.</p>")
    art = (f'<article id="glossary" class="unit" dir="rtl" lang="fa">\n'
           f'<h1 style="font-size:1.7rem;margin:0 0 1rem;border-bottom:3px solid #2c5f8a;padding-bottom:.5rem;">{MASTER_H}</h1>\n'
           f"{intro}\n{g}\n</article>")
    return art, [(1, "glossary", MASTER_H, MASTER_H, 0)]


def toc_html(entries, chapter_of, pages=None):
    rows = ['<nav class="toc" aria-label="فهرست مطالب"><div class="h">فهرست مطالب</div>']
    pg_done = []
    for lvl, eid, title_html, *_ in entries:
        n = chapter_of.get(eid)
        if lvl == 1 and n in PARTS:
            rows.append(f'<div class="part">{PARTS[n]}</div>')
        pg = PLACEHOLDER if pages is None else str(pages[len(pg_done)]).translate(FA)
        pg_done.append(eid)
        rows.append(f'<a class="row l{lvl}" href="#{eid}"><span class="t">{title_html}</span>'
                    f'<span class="dots"></span><span class="pg">{pg}</span></a>')
    rows.append("</nav>")
    return "\n".join(rows)


def cover_image_html():
    img_uri = (HERE / "figures" / "fundamentals-of-software-architecture-persian.jpeg").as_uri()
    return (f'<div class="book-cover-image">'
            f'<img src="{img_uri}" alt="روی جلد کتاب">'
            f'</div>')


def cover_html(version_str: str = None):
    v = version_str or VERSION_NOTE
    return (f'<section class="cover"><div class="t">{TITLE_FA}</div><div class="bar"></div>'
            f'<div class="en">{TITLE_EN}</div><div class="sub">{SUBTITLE}</div>'
            f'<div class="ver" style="margin-top:12mm;font-size:11.5pt;font-weight:700;color:#2c5f8a;">{v}</div>'
            f'<div class="note">{NOTE}</div></section>')


def document(body: str, title: str, args) -> str:
    return ("<!DOCTYPE html>\n"
            f'<html lang="fa" dir="rtl"><head><meta charset="utf-8"><base href="{HTML_DIR.as_uri()}/">'
            f"<title>{htmllib.escape(title)}</title><style>{css(args.page_size, args.font_size)}</style></head>"
            f'<body dir="rtl">\n{body}\n</body></html>')


# ───────────────────────────── rendering ─────────────────────────────
class Renderer:
    def __init__(self, args):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        opts = {"args": ["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"]}
        if args.chromium:
            opts["executable_path"] = args.chromium
        try:
            self.browser = self._pw.chromium.launch(**opts)
        except Exception as e:  # pragma: no cover - environment specific
            self._pw.stop()
            sys.exit(f"Chromium اجرا نشد: {e}\n"
                     "راه‌حل: «playwright install chromium» را اجرا کنید یا با --chromium مسیر Chrome/Chromium را بدهید.")
        self.tmpdir = Path(tempfile.mkdtemp(prefix="pdfbuild-"))

    def render(self, html: str, name: str) -> bytes:
        f = self.tmpdir / f"{name}.html"
        f.write_text(html, encoding="utf-8")
        page = self.browser.new_page()
        try:
            page.goto(f.as_uri(), wait_until="load", timeout=600_000)
            page.evaluate("document.fonts.ready")
            return page.pdf(prefer_css_page_size=True, print_background=True, outline=True, tagged=True)
        finally:
            page.close()

    def close(self):
        self.browser.close()
        self._pw.stop()


def toc_link_pages(doc, toc_start: int, toc_pages: int, n_entries: int):
    """Target page (1-based) of every TOC row, read from the internal links Chromium wrote on the TOC pages."""
    rows = []
    for pno in range(toc_start, toc_start + toc_pages):
        links = [l for l in doc[pno].get_links() if l.get("page", -1) >= 0]
        links.sort(key=lambda l: (round(l["from"].y0, 0), -l["from"].x1))
        for l in links:
            key = (pno, round(l["from"].y0))
            if rows and rows[-1][0][0] == pno and abs(rows[-1][0][1] - key[1]) <= 2:
                continue                      # another fragment of the same row
            rows.append((key, l["page"] + 1))
    if len(rows) != n_entries:
        raise RuntimeError(f"TOC rows ({n_entries}) and links found ({len(rows)}) differ")
    return [p for _, p in rows]


def find_toc_pages(doc):
    """Cover image and title page have no TOC links. TOC pages have internal links."""
    start = None
    count = 0
    for pno in range(doc.page_count):
        forward_links = [l for l in doc[pno].get_links() if l.get("page", -1) > pno]
        if len(forward_links) >= 10:
            if start is None:
                start = pno
            count += 1
        elif start is not None:
            break
    if start is None:
        raise RuntimeError("TOC pages not found in rendered document")
    return start, count


def finalize(pdf_bytes: bytes, out: Path, title: str, toc, version: str = VERSION):
    import pymupdf
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    if toc is not None:
        doc.set_toc(toc)
    doc.set_metadata({"title": title, "author": "Mark Richards, Neal Ford — ترجمهٔ فارسی",
                      "subject": f"{TITLE_EN} (نسخهٔ {version})",
                      "creator": f"build_pdf.py v{version} (Chromium + PyMuPDF)"})
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out, garbage=3, deflate=True)
    pages = doc.page_count
    doc.close()
    return pages


def outline_from_chromium(pdf_bytes: bytes, entries, n_heads: int):
    """Bookmarks for a single chapter.

    Chromium writes a PDF outline from the h1/h3/h4… headings, but its titles can be bidi-scrambled
    (Persian mixed with digits). So only the page numbers are taken from it — matched by position
    against all h1/h3 headings of the file — and our own clean titles are used."""
    import pymupdf
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    raw = [it for it in doc.get_toc(simple=True) if it[0] <= 2]
    doc.close()
    if len(raw) != n_heads:
        print(f"    هشدار: سرفصل‌های Chromium ({len(raw)}) با فایل ({n_heads}) نمی‌خواند؛ فقط نشانک فصل ساخته شد")
        return [[1, e[3], 1] for e in entries if e[0] == 1]
    return [[lvl, txt, 1 if pos is None else raw[pos][2]] for lvl, _, _, txt, pos in entries]


# ───────────────────────────── builds ─────────────────────────────
def rel(p: Path) -> str:
    try:
        return str(p.relative_to(HERE))
    except ValueError:
        return str(p)


def build_book(r: Renderer, args):
    t0 = time.time()
    us = units()
    arts, entries, chapter_of = [], [], {}
    for anchor, base, _, n in us:
        a, e, _ = load_unit(anchor, base)
        arts.append(a)
        entries += e
        chapter_of[anchor] = n
    ga, ge = glossary_article(master_rows())
    arts.append(ga)
    entries += ge
    ver_note = f"نسخهٔ ترجمه: {args.version} — بازبینی جامع ۲۷ فصل و واژه‌نامه ({VERSION_DATE})"
    body = lambda pages: (cover_image_html() + "\n" + cover_html(ver_note) + "\n" + toc_html(entries, chapter_of, pages) + "\n" + "\n".join(arts))

    import pymupdf
    print("  گذر ۱: چیدمان و یافتن شمارهٔ صفحه‌ها…", flush=True)
    pdf1 = r.render(document(body(None), TITLE_FA, args), "book-pass1")
    d1 = pymupdf.open(stream=pdf1, filetype="pdf")
    toc_start, toc_pages = find_toc_pages(d1)
    pages = toc_link_pages(d1, toc_start, toc_pages, len(entries))
    d1.close()

    print("  گذر ۲: درج شمارهٔ صفحه‌ها در فهرست…", flush=True)
    pdf2 = r.render(document(body(pages), TITLE_FA, args), "book-pass2")
    d2 = pymupdf.open(stream=pdf2, filetype="pdf")
    d2_start, d2_pages = find_toc_pages(d2)
    if d2_start != toc_start or d2_pages != toc_pages or toc_link_pages(d2, d2_start, d2_pages, len(entries)) != pages:
        raise RuntimeError("page numbers shifted between passes")
    d2.close()

    toc = [
        [1, "روی جلد", 1],
        [1, "صفحهٔ عنوان و شناسنامه", 2],
        [1, "فهرست مطالب", toc_start + 1]
    ] + [[e[0], e[3], pages[i]] for i, e in enumerate(entries)]
    n = finalize(pdf2, OUT / "book.pdf", TITLE_FA, toc, version=args.version)
    print(f"  ✓ {rel(OUT / 'book.pdf')} — {n} صفحه، {len(entries)} سرفصل در فهرست "
          f"({(OUT / 'book.pdf').stat().st_size / 1e6:.1f} MB، {time.time() - t0:.0f} ثانیه)")


def build_chapters(r: Renderer, args):
    sel = set(args.chapters) if args.chapters else None
    for anchor, base, title, n in units():
        num = 0 if n is None else n
        if sel is not None and num not in sel:
            continue
        art, entries, n_heads = load_unit(anchor, base)
        art = art.replace('class="unit"', 'class="unit single"', 1)
        pdf = r.render(document(art, f"{title} — {TITLE_FA}", args), base)
        toc = outline_from_chromium(pdf, entries, n_heads)
        out = OUT / "chapters" / f"{base}.pdf"
        pages = finalize(pdf, out, f"{title} — {TITLE_FA}", toc, version=args.version)
        print(f"  ✓ {rel(out)} — {pages} صفحه ({out.stat().st_size / 1e6:.1f} MB)", flush=True)


def main():
    ap = argparse.ArgumentParser(description="ساخت PDF کتاب (با فهرست) و PDF جداگانهٔ هر فصل از فایل‌های HTML")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--book-only", action="store_true", help="فقط pdf/book.pdf")
    g.add_argument("--chapters-only", action="store_true", help="فقط PDF فصل‌ها")
    ap.add_argument("--chapters", type=int, nargs="+", metavar="N", help="فقط این فصل‌ها (0 = پیوست)")
    ap.add_argument("--version", default=VERSION, help=f"نسخهٔ کتاب در PDF (پیش‌فرض: {VERSION})")
    ap.add_argument("--chromium", default=default_chromium(),
                    help="مسیر Chrome/Chromium (پیش‌فرض: خودکار، متغیر CHROMIUM_PATH یا Chromium Playwright)")
    ap.add_argument("--page-size", default="A4", help="اندازهٔ صفحه، مانند A4، A5 یا Letter (پیش‌فرض A4)")
    ap.add_argument("--out-dir", type=Path, default=None, help="پوشهٔ خروجی (پیش‌فرض: pdf/)")
    ap.add_argument("--font-size", type=float, default=11, help="اندازهٔ قلم متن به pt (پیش‌فرض 11)")
    args = ap.parse_args()
    if args.chapters:
        args.chapters_only = True
    if args.out_dir:
        global OUT
        OUT = args.out_dir.resolve()

    missing = [f for f in ("Vazirmatn-Regular.ttf", "Vazirmatn-Bold.ttf", "DejaVuSansMono.ttf") if not (FONTS / f).exists()]
    if missing:
        sys.exit(f"فونت‌ها در {FONTS} پیدا نشدند: {missing}")

    r = Renderer(args)
    try:
        if not args.chapters_only:
            print("ساخت کتاب کامل:", flush=True)
            build_book(r, args)
        if not args.book_only:
            print("ساخت PDF فصل‌ها:", flush=True)
            build_chapters(r, args)
    finally:
        r.close()


if __name__ == "__main__":
    main()
