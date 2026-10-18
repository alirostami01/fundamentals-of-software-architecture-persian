#!/usr/bin/env python3
"""ساخت نسخهٔ یکپارچهٔ کل کتاب → book.md / book.html

ترتیب: صفحهٔ عنوان، فهرست مطالب (با گروه‌بندی بخش‌ها)، فصل‌های ۱ تا ۲۷ (chapter-NN)،
پیوست (appendix) و در پایان واژه‌نامهٔ اصلی (glossary.md، دو ستون، مرتب‌شده بر پایهٔ واژهٔ انگلیسی).

Usage (از درون پوشهٔ translation):
    python3 build_book.py
"""
import html as htmllib
import re
from pathlib import Path

from build_chapter import FRONT, gloss_html

HERE = Path(__file__).resolve().parent
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

TITLE_FA = "مبانی معماری نرم‌افزار: رویکردی مهندسی و مدرن"
TITLE_EN = "Fundamentals of Software Architecture: A Modern Engineering Approach"
SUBTITLE = "ویرایش دوم — Mark Richards و Neal Ford (O’Reilly، ۲۰۲۵)"
NOTE = "ترجمهٔ فارسی؛ تصاویر شکل‌ها از کتاب اصلی برداشته شده و عنوان‌هایشان ترجمه شده است."
PARTS = {2: "بخش اول: مبانی", 9: "بخش دوم: سبک‌های معماری", 21: "بخش سوم: تکنیک‌ها و مهارت‌های نرم"}
MASTER_H = "واژه‌نامهٔ اصلی کتاب"

ART = ("font-family:'Vazirmatn','IRANSans','Tahoma',sans-serif;line-height:2;max-width:46rem;"
       "margin:0 auto 2rem;color:#1a1a1a;background:#fff;padding:1.5rem;border:1px solid #e5e5e5;border-radius:8px;")
H1 = "font-size:1.7rem;margin:0 0 1rem;border-bottom:3px solid #2c5f8a;padding-bottom:.5rem;"
A = "color:#2c5f8a;text-decoration:none;"
BACK = (f'  <p style="text-align:left;margin:1rem 0 0;font-size:.9rem;">'
        f'<a href="#toc" style="{A}">↑ بازگشت به فهرست مطالب</a></p>\n')


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
        head = (HERE / "front" / f"{name}.md").read_text(encoding="utf-8").split("\n", 1)[0]
        out.append((name, re.sub(r"^#+\s*", "", head).strip()))
    return out


def units():
    """(anchor, base filename, title, chapter number or None)"""
    out = []
    for n in range(1, 28):
        f = HERE / f"chapter-{n:02d}.md"
        title = first_h1(f)
        out.append((f"chapter-{n:02d}", f"chapter-{n:02d}", title, n))
    title = first_h1(HERE / "appendix.md")
    out.append(("appendix", "appendix", title, None))
    return out


def master_rows():
    rows = []
    for l in (HERE / "glossary.md").read_text(encoding="utf-8").split("\n"):
        if l.startswith("| ") and not l.startswith("| واژهٔ") and not l.startswith("| English"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) >= 2 and c[0] and not set(c[0]) <= set("-"):
                rows.append((c[0], c[1]))
    return sorted(rows, key=lambda r: r[0].lower())


def build_md(us, rows):
    md = [f"# {TITLE_FA}", "", f"**{TITLE_EN}**", "", SUBTITLE, "", f"> {NOTE}", "",
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
        body = (HERE / f"{base}.md").read_text(encoding="utf-8").strip()
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
        f'<article id="toc" dir="rtl" lang="fa" style="{ART}">',
        f'  <h1 style="{H1}">{TITLE_FA}</h1>',
        f'  <p dir="ltr" style="text-align:left;font-weight:bold;margin:.2rem 0;">{TITLE_EN}</p>',
        f'  <p style="margin:.2rem 0;">{SUBTITLE}</p>',
        f'  <p style="color:#666;font-size:.92rem;">{NOTE}</p>',
        '  <nav aria-label="فهرست مطالب">',
        '    <h2 style="font-size:1.35rem;color:#2c5f8a;margin:1rem 0 .4rem;">فهرست مطالب</h2>',
        *toc,
        "  </nav>",
        "</article>",
    ]
    for anchor, base, _, _ in us:
        t = (HERE / f"{base}.html").read_text(encoding="utf-8")
        t = re.sub(r"^<!--.*?-->\s*", "", t, flags=re.S).strip()
        t = t.replace("<article ", f'<article id="{anchor}" ', 1)
        t = re.sub(r'(<article[^>]*style="[^"]*?)margin:0 auto;', r"\1margin:0 auto 2rem;", t, count=1)
        t = t[: t.rfind("</article>")] + BACK + "</article>"
        parts += ["", t]
    g = gloss_html(rows).replace("واژه‌نامهٔ اختصاصی این فصل", MASTER_H).replace(
        "معادل مصوب/به‌کاررفته در این فصل", "معادل مصوب")
    g = re.sub(r"\s*<h3[^>]*>.*?</h3>", "", g, count=1)
    parts += ["", f'<article id="glossary" dir="rtl" lang="fa" style="{ART}">',
              f'  <h1 style="{H1}">{MASTER_H}</h1>',
              f'  <p style="text-align:justify;">این واژه‌نامه همهٔ {str(len(rows)).translate(FA)} معادل مصوبِ '
              "به‌کاررفته در ترجمه را به ترتیب الفبایی واژهٔ انگلیسی در بر دارد.</p>",
              g, BACK.rstrip("\n"), "</article>", "", "</div>", ""]
    return "\n".join(parts)


def main():
    us, rows = units(), master_rows()
    (HERE / "book.md").write_text(build_md(us, rows), encoding="utf-8")
    (HERE / "book.html").write_text(build_html(us, rows), encoding="utf-8")
    print(f"book.md/html written: {len(us)} units, {len(rows)} master-glossary rows")


if __name__ == "__main__":
    main()
