#!/usr/bin/env python3
"""ساخت نسخهٔ یکپارچهٔ کل کتاب → markdown/book.md و html/book.html

ترتیب: صفحهٔ عنوان، فهرست مطالب (با گروه‌بندی بخش‌ها)، «حمایت از پروژه»، فصل‌های ۱ تا ۲۷ (chapter-NN)،
پیوست (appendix) و در پایان واژه‌نامهٔ اصلی (markdown/glossary.md، دو ستون، مرتب‌شده بر پایهٔ واژهٔ انگلیسی).

Usage (از ریشهٔ مخزن):
    python3 build_book.py
"""
import html as htmllib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MD_DIR = HERE / "markdown"
HTML_DIR = HERE / "html"
# بخش‌های پیش از متن که در آغاز فایل یک فصل، پیش از تیتر H1، آمده‌اند:
# فصل ۱ ← markdown/support.md و html/support.html («حمایت از پروژه»)
FRONT = {1: ["support"]}
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

TITLE_FA = "مبانی معماری نرم‌افزار: رویکردی مهندسی و مدرن"
TITLE_EN = "Fundamentals of Software Architecture: A Modern Engineering Approach"
SUBTITLE = "ویرایش دوم — Mark Richards و Neal Ford (O’Reilly، ۲۰۲۵)"
VERSION = "2.2.0"
VERSION_DATE = "آبان ۱۴۰۵ (اکتبر ۲۰۲۶)"
VERSION_NOTE = f"نسخهٔ ترجمه: {VERSION} — ویرایش بازبینی‌شده با تصویر جلد و صفحهٔ عنوان ({VERSION_DATE})"
COVER_IMG = "figures/fundamentals-of-software-architecture-persian.jpeg"
NOTE = "ترجمهٔ فارسی؛ تصاویر شکل‌ها از کتاب اصلی برداشته شده و عنوان‌هایشان ترجمه شده است."
PARTS = {2: "بخش اول: مبانی", 9: "بخش دوم: سبک‌های معماری", 21: "بخش سوم: تکنیک‌ها و مهارت‌های نرم"}
MASTER_H = "واژه‌نامهٔ اصلی کتاب"

ART = ("font-family:'Vazirmatn','IRANSans','Tahoma',sans-serif;line-height:2;max-width:46rem;"
       "margin:0 auto 2rem;color:#1a1a1a;background:#fff;padding:1.5rem;border:1px solid #e5e5e5;border-radius:8px;")
H1 = "font-size:1.7rem;margin:0 0 1rem;border-bottom:3px solid #2c5f8a;padding-bottom:.5rem;"
A = "color:#2c5f8a;text-decoration:none;"
BACK = (f'  <p style="text-align:left;margin:1rem 0 0;font-size:.9rem;">'
        f'<a href="#toc" style="{A}">↑ بازگشت به فهرست مطالب</a></p>\n')


def gloss_html(rows, title=MASTER_H, col2="معادل مصوب"):
    """Two-column glossary table (same markup as the chapter glossaries)."""
    trs = "\n".join(
        '        <tr><td dir="ltr" style="border:1px solid #ccc;padding:.4rem .7rem;'
        'text-align:left;font-family:Consolas,Monaco,monospace;background:#f7f9fb;">'
        f"{htmllib.escape(en)}</td>"
        '<td style="border:1px solid #ccc;padding:.4rem .7rem;">'
        f"{htmllib.escape(fa)}</td></tr>"
        for en, fa in rows
    )
    return (
        "  <section>\n"
        f'    <h3 style="font-size:1.35rem;color:#2c5f8a;margin:0 0 .8rem;">{title}</h3>\n'
        '    <table dir="rtl" style="width:100%;border-collapse:collapse;font-size:.95rem;">\n'
        "      <thead>\n"
        '        <tr style="background:#2c5f8a;color:#fff;">\n'
        '          <th style="border:1px solid #ccc;padding:.5rem .7rem;text-align:right;">واژهٔ انگلیسی</th>\n'
        f'          <th style="border:1px solid #ccc;padding:.5rem .7rem;text-align:right;">{col2}</th>\n'
        "        </tr>\n"
        "      </thead>\n"
        "      <tbody>\n"
        f"{trs}\n"
        "      </tbody>\n"
        "    </table>\n"
        "  </section>"
    )


def first_h1(path):
    """Title of a chapter file = its first H1 (front matter such as «حمایت از پروژه» may precede it)."""
    for l in path.read_text(encoding="utf-8").split("\n"):
        if l.startswith("# "):
            return l[2:].strip()
    raise ValueError(f"no H1 in {path}")


def front_items(n):
    """[(id, title)] of the front-matter blocks placed before chapter n (see build_chapter.FRONT)."""
    out = []
    for name in FRONT.get(n, []):
        head = (MD_DIR / f"{name}.md").read_text(encoding="utf-8").split("\n", 1)[0]
        out.append((name, re.sub(r"^#+\s*", "", head).strip()))
    return out


def units():
    """(anchor, base filename, title, chapter number or None)"""
    out = []
    for n in range(1, 28):
        f = MD_DIR / f"chapter-{n:02d}.md"
        title = first_h1(f)
        out.append((f"chapter-{n:02d}", f"chapter-{n:02d}", title, n))
    title = first_h1(MD_DIR / "appendix.md")
    out.append(("appendix", "appendix", title, None))
    return out


def master_rows():
    rows = []
    for l in (MD_DIR / "glossary.md").read_text(encoding="utf-8").split("\n"):
        if l.startswith("| ") and not l.startswith("| واژهٔ") and not l.startswith("| English"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) >= 2 and c[0] and not set(c[0]) <= set("-"):
                rows.append((c[0], c[1]))
    return sorted(rows, key=lambda r: r[0].lower())


def build_md(us, rows):
    md = [f"![روی جلد کتاب مبانی معماری نرم‌افزار](../{COVER_IMG})", "",
          f"# {TITLE_FA}", "", f"**{TITLE_EN}**", "", SUBTITLE, "", f"> {NOTE}", "",
          f"> **{VERSION_NOTE}**", "",
          '<a id="toc"></a>', "", "## فهرست مطالب", ""]
    for anchor, _, title, n in us:
        if n in PARTS:
            md += ["", f"**{PARTS[n]}**", ""]
        if n is None:
            md += [""]
        md += [f"- [{ft}](#{fid})" for fid, ft in front_items(n)]
        md.append(f"- [{title}](#{anchor})")
    md.append(f"- [{MASTER_H}](#glossary)")
    for anchor, base, _, _n in us:
        body = (MD_DIR / f"{base}.md").read_text(encoding="utf-8").strip()
        if not body.startswith("# "):                     # front matter before the H1 gets its own anchor
            front, body = body.split("\n# ", 1)
            body = "# " + body
            front = re.sub(r"\n+---\s*$", "", front.strip())
            fid = front_items(_n)[0][0] if front_items(_n) else f"{anchor}-front"
            md += ["", "---", "", f'<a id="{fid}"></a>', "", front]
        md += ["", "---", "", f'<a id="{anchor}"></a>', "", body]
    md += ["", "---", "", '<a id="glossary"></a>', "", f"# {MASTER_H}", "",
           f"این واژه‌نامه همهٔ {str(len(rows)).translate(FA)} معادل مصوبِ به‌کاررفته در ترجمه را "
           "به ترتیب الفبایی واژهٔ انگلیسی در بر دارد.", "",
           "| واژهٔ انگلیسی | معادل مصوب |", "|---|---|"]
    md += [f"| {en} | {fa} |" for en, fa in rows]
    return "\n".join(md) + "\n"


def build_html(us, rows):
    toc = []
    for anchor, _, title, n in us:
        if n in PARTS:
            if toc: toc.append("      </ul>")
            toc.append(f'      <p style="font-weight:bold;margin:.8rem 0 .2rem;">{PARTS[n]}</p>')
            toc.append('      <ul style="margin:.2rem 1.2rem;padding:0;line-height:1.9;">')
        elif not toc or n is None:
            if toc: toc.append("      </ul>")
            toc.append('      <ul style="margin:.2rem 1.2rem;padding:0;line-height:1.9;">')
        toc += [f'        <li><a href="#{fid}" style="{A}">{htmllib.escape(ft)}</a></li>' for fid, ft in front_items(n)]
        toc.append(f'        <li><a href="#{anchor}" style="{A}">{htmllib.escape(title)}</a></li>')
    toc.append(f'        <li><a href="#glossary" style="{A}">{MASTER_H}</a></li>')
    toc.append("      </ul>")
    parts = [
        "<!-- خروجی HTML — نسخهٔ یکپارچهٔ کل کتاب (بدون html/head)؛ ساخته‌شده با build_book.py -->",
        '<div dir="rtl" lang="fa">',
        "",
        '  <figure style="text-align:center;margin:0 0 2rem;padding:0;">',
        f'    <img src="../{COVER_IMG}" alt="روی جلد کتاب مبانی معماری نرم‌افزار" style="max-width:100%;max-height:85vh;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,0.15);">',
        '  </figure>',
        "",
        f'<article id="toc" dir="rtl" lang="fa" style="{ART}">',
        f'  <h1 style="{H1}">{TITLE_FA}</h1>',
        f'  <p dir="ltr" style="text-align:left;font-weight:bold;margin:.2rem 0;">{TITLE_EN}</p>',
        f'  <p style="margin:.2rem 0;">{SUBTITLE}</p>',
        f'  <p style="color:#2c5f8a;font-weight:bold;margin:.3rem 0;font-size:.95rem;">{VERSION_NOTE}</p>',
        f'  <p style="color:#666;font-size:.92rem;">{NOTE}</p>',
        '  <nav aria-label="فهرست مطالب">',
        '    <h2 style="font-size:1.35rem;color:#2c5f8a;margin:1rem 0 .4rem;">فهرست مطالب</h2>',
        *toc,
        "  </nav>",
        "</article>",
    ]
    for anchor, base, _, _ in us:
        t = (HTML_DIR / f"{base}.html").read_text(encoding="utf-8")
        t = re.sub(r"^<!--.*?-->\s*", "", t, flags=re.S).strip()
        t = t.replace("<article ", f'<article id="{anchor}" ', 1)
        t = re.sub(r'(<article[^>]*style="[^"]*?)margin:0 auto;', r"\1margin:0 auto 2rem;", t, count=1)
        t = t[: t.rfind("</article>")] + BACK + "</article>"
        parts += ["", t]
    g = re.sub(r"\s*<h3[^>]*>.*?</h3>", "", gloss_html(rows), count=1)
    parts += ["", f'<article id="glossary" dir="rtl" lang="fa" style="{ART}">',
              f'  <h1 style="{H1}">{MASTER_H}</h1>',
              f'  <p style="text-align:justify;">این واژه‌نامه همهٔ {str(len(rows)).translate(FA)} معادل مصوبِ '
              "به‌کاررفته در ترجمه را به ترتیب الفبایی واژهٔ انگلیسی در بر دارد.</p>",
              g, BACK.rstrip("\n"), "</article>", "", "</div>", ""]
    return "\n".join(parts)


def main():
    us, rows = units(), master_rows()
    (MD_DIR / "book.md").write_text(build_md(us, rows), encoding="utf-8")
    (HTML_DIR / "book.html").write_text(build_html(us, rows), encoding="utf-8")
    print(f"markdown/book.md + html/book.html written: {len(us)} units, {len(rows)} master-glossary rows")


if __name__ == "__main__":
    main()
