#!/usr/bin/env python3
"""تبدیل Markdownِ یک بسته به کامپوننت HTMLِ راست‌به‌چپ (سبکِ یکسان با بسته‌های پیشین).

Usage:
    python3 md2html.py chunk-10.md chunk-10.html --terms source/chunk-10.terms --num ۱۰

Supported blocks: H1 / H2(→h3) / H3(→h4) / paragraphs (inline **bold**) /
fenced code (any language, LTR <pre>) / "- " lists (consecutive → one <ul>) /
"> **شکل …**" figures / "> … > — Name" aphorisms / "> **title** …" sideboxes /
"---" separators (rendered as <hr> between top-level sections) / final glossary.

English wrapping: parenthesised Latin-only content → one <bdi>(…)</bdi>; mixed
parentheses keep "(" ")" and bare-wrap inside; bare terms come from the --terms
file (one per line) and are matched in ONE combined regex pass (no nesting).
"""
import argparse
import html as htmllib
import re
from pathlib import Path

ART = ('<article dir="rtl" lang="fa" style="font-family:\'Vazirmatn\',\'IRANSans\',\'Tahoma\',sans-serif;'
       'line-height:2;max-width:46rem;margin:0 auto;color:#1a1a1a;background:#fff;padding:1.5rem;'
       'border:1px solid #e5e5e5;border-radius:8px;">')
H1 = 'font-size:1.7rem;margin:0 0 1rem;border-bottom:3px solid #2c5f8a;padding-bottom:.5rem;'
H3 = "font-size:1.35rem;color:#2c5f8a;margin:0 0 .8rem;"
H4 = "font-size:1.15rem;color:#2c5f8a;margin:1.2rem 0 .6rem;"
PAD = ("display:inline-block;unicode-bidi:isolate;font-family:Consolas,Monaco,monospace;"
       "background:#f4f6f8;border:1px solid #dde3e8;border-radius:3px;padding:0 .35em;direction:ltr;")
PAD92 = PAD.replace("monospace;", "monospace;font-size:.92em;")
ISO = "display:inline-block;unicode-bidi:isolate;direction:ltr;"
QUOTA = ('margin:1rem 0;padding:1rem 1.2rem;background:#eef4fa;border-right:5px solid #2c5f8a;'
         'border-radius:4px;font-size:1.05rem;font-weight:bold;text-align:center;')
SIDEBAR = ('margin:1.2rem 0;padding:1rem 1.2rem;background:#f7f9fb;border:1px solid #dde3e8;'
           'border-right:4px solid #2c5f8a;border-radius:4px;font-size:.98rem;text-align:justify;')
FOOTER = 'display:block;margin-top:.6rem;font-size:.9rem;font-weight:normal;color:#555;'
FIG = 'margin:1rem 0;padding:.7rem 1rem;background:#f9f9f9;border-right:4px solid #2c5f8a;border-radius:4px;'
PRE = ('direction:ltr;text-align:left;unicode-bidi:isolate;margin:.8rem 0;padding:.8rem 1rem;'
       'background:#f4f6f8;border:1px solid #dde3e8;border-radius:4px;overflow-x:auto;'
       'font-family:Consolas,Monaco,monospace;font-size:.92rem;line-height:1.6;')
UL = "margin:.6rem 1.2rem;padding:0;line-height:1.9;"
HR = '<hr style="border:none;border-top:1px dashed #bbb;margin:1.4rem 0;">'
FIGNOTE = '(تصویر شکل در پی‌دی‌اف اصلی کتاب موجود است؛ عنوان عیناً ترجمه شده است.)'


def build_wrapper(terms):
    terms = sorted({t for t in terms if t}, key=len, reverse=True)
    bare_re = re.compile(r"(?<![\w])(" + "|".join(re.escape(t) for t in terms) + r")(?![\w])") if terms else None
    paren_re = re.compile(r"\([^()]*\)")

    def bdi(inner, paren=False, iso=False):
        style = ISO if iso else (PAD92 if paren else PAD)
        return f'<bdi dir="ltr" style="{style}">{htmllib.escape(inner, quote=False)}</bdi>'

    def bare(seg):
        if bare_re is None:
            return htmllib.escape(seg, quote=False)
        out, last = [], 0
        for m in bare_re.finditer(seg):
            out.append(htmllib.escape(seg[last:m.start()], quote=False))
            out.append(bdi(m.group(0)))
            last = m.end()
        out.append(htmllib.escape(seg[last:], quote=False))
        return "".join(out)

    def plain(text):
        out, last = [], 0
        for m in paren_re.finditer(text):
            out.append(bare(text[last:m.start()]))
            inner = m.group(0)[1:-1]
            if re.search(r"[A-Za-z]", inner) and not re.search(r"[\u0600-\u06FF]", inner):
                out.append(bdi(f"({inner})", paren=True))
            else:
                out.append("(" + bare(inner) + ")")
            last = m.end()
        out.append(bare(text[last:]))
        return "".join(out)

    def inline(text):
        parts = text.split("**")
        return "".join(f"<b>{plain(p)}</b>" if i % 2 else plain(p) for i, p in enumerate(parts))

    return inline, bdi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("html")
    ap.add_argument("--terms", default=None)
    ap.add_argument("--num", required=True, help="Persian chunk number for the header comment")
    a = ap.parse_args()

    terms = []
    if a.terms:
        terms = [l.strip() for l in Path(a.terms).read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#")]
    inline, bdi = build_wrapper(terms)

    lines = Path(a.md).read_text(encoding="utf-8").split("\n")
    assert lines[0].startswith("# ")
    h1_text = lines[0][2:].strip()
    gi = next(i for i, l in enumerate(lines) if l.startswith("## واژه‌نامهٔ اختصاصی این بخش"))
    body, gloss_lines = lines[1:gi], lines[gi:]

    # ---- tokenize into blocks (fenced code kept intact) ----
    blocks, cur, fence = [], [], None
    for l in body:
        if fence is not None:
            cur.append(l)
            if l.strip() == "```":
                blocks.append(("code", cur)); cur, fence = [], None
            continue
        if l.startswith("```"):
            if cur: blocks.append(("text", cur)); cur = []
            fence = l[3:].strip() or "text"
            cur = [l]
            continue
        if not l.strip():
            if cur: blocks.append(("text", cur)); cur = []
            continue
        cur.append(l)
    if cur: blocks.append(("text", cur))
    assert fence is None, "unterminated code fence"

    sections, current = [], None
    pending_ul = []

    def close_ul():
        nonlocal pending_ul
        if pending_ul:
            current.append(f'    <ul style="{UL}">')
            current.extend(f"      <li>{inline(x)}</li>" for x in pending_ul)
            current.append("    </ul>")
            pending_ul = []

    def start_section(heading_html=None):
        nonlocal current
        if current is not None:
            close_ul()
            current.append("  </section>")
            sections.append("\n".join(current))
        current = ["  <section>"]
        if heading_html:
            current.append(heading_html)

    def ensure():
        if current is None:
            start_section()

    def quote(b):
        qs = [l[1:].strip() for l in b]
        paras, buf = [], []
        for q in qs:
            if q == "":
                if buf: paras.append(" ".join(buf)); buf = []
            else:
                buf.append(q)
        if buf: paras.append(" ".join(buf))
        first = paras[0]
        unb = lambda s: s[2:-2] if s.startswith("**") and s.endswith("**") else s
        if first.startswith("**شکل"):
            m = re.match(r"\*\*(.+?)\*\*\s*(.*)", first)
            return (f'    <figure style="{FIG}">\n'
                    f'      <figcaption style="font-size:.95rem;color:#333;"><b>{inline(m.group(1))}</b> {inline(m.group(2))}</figcaption>\n'
                    f'      <small style="color:#777;">{FIGNOTE}</small>\n'
                    f'    </figure>')
        attrib = next((p for p in paras if p.startswith("—")), None)
        if attrib:
            return (f'    <blockquote style="{QUOTA}">\n      {inline(unb(first))}\n'
                    f'      <footer style="{FOOTER}">— {bdi(attrib.lstrip("—").strip(), iso=True)}</footer>\n'
                    f'    </blockquote>')
        ps = [f'    <p style="font-weight:bold;text-align:center;margin:0 0 .7rem;">{inline(unb(first))}</p>']
        ps += [f'    <p style="text-align:justify;margin:.55rem 0;">{inline(p)}</p>' for p in paras[1:]]
        return f'    <blockquote style="{SIDEBAR}">\n' + "\n".join(ps) + "\n    </blockquote>"

    for kind, b in blocks:
        if kind == "code":
            ensure(); close_ul()
            lang = b[0][3:].strip() or "text"
            code = htmllib.escape("\n".join(b[1:-1]), quote=False)
            current.append(f'    <pre dir="ltr" style="{PRE}"><code class="language-{lang}">{code}</code></pre>')
            continue
        joined = "\n".join(b)
        if joined.strip() == "---":
            continue
        if b[0].startswith("### "):
            ensure(); close_ul()
            current.append(f'    <h4 style="{H4}">{inline(b[0][4:].strip())}</h4>')
        elif b[0].startswith("## "):
            start_section(f'    <h3 style="{H3}">{inline(b[0][3:].strip())}</h3>')
        elif b[0].startswith(">"):
            ensure(); close_ul()
            current.append(quote(b))
        elif all(l.startswith("- ") for l in b):
            ensure()
            pending_ul.extend(l[2:].strip() for l in b)
        else:
            ensure(); close_ul()
            current.append(f'    <p style="text-align:justify;">{inline(" ".join(x.strip() for x in b))}</p>')
    if current is not None:
        close_ul()
        current.append("  </section>")
        sections.append("\n".join(current))

    rows = []
    for l in gloss_lines:
        if l.startswith("| ") and not l.startswith("| واژهٔ") and not l.startswith("|---"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            rows.append((c[0], c[1]))
    trs = "\n".join(
        '        <tr><td dir="ltr" style="border:1px solid #ccc;padding:.4rem .7rem;text-align:left;'
        f'font-family:Consolas,Monaco,monospace;background:#f7f9fb;">{htmllib.escape(en)}</td>'
        f'<td style="border:1px solid #ccc;padding:.4rem .7rem;">{htmllib.escape(fa)}</td></tr>'
        for en, fa in rows)
    gloss = "\n".join([
        "  <section>", f'    <h3 style="{H3}">واژه‌نامهٔ اختصاصی این بخش</h3>',
        '    <table dir="rtl" style="width:100%;border-collapse:collapse;font-size:.95rem;">',
        "      <thead>", '        <tr style="background:#2c5f8a;color:#fff;">',
        '          <th style="border:1px solid #ccc;padding:.5rem .7rem;text-align:right;">واژهٔ انگلیسی</th>',
        '          <th style="border:1px solid #ccc;padding:.5rem .7rem;text-align:right;">معادل مصوب/به‌کاررفته در این بخش</th>',
        "        </tr>", "      </thead>", "      <tbody>", trs, "      </tbody>", "    </table>", "  </section>"])

    out = [f"<!-- بخش دوم: خروجی HTML — کامپوننت محتوای داخلی (بدون html/head) — بستهٔ {a.num} -->",
           ART, "", f'  <h1 style="{H1}">{htmllib.escape(h1_text, quote=False)}</h1>']
    for i, s in enumerate(sections):
        out.append("")
        if i:
            out += [f"  {HR}", ""]
        out.append(s)
    out += ["", f"  {HR}", "", gloss, "", "</article>"]
    text = "\n".join(out) + "\n"
    Path(a.html).write_text(text, encoding="utf-8")
    print(f"{a.html}: sections {len(sections)}, glossary rows {len(rows)}, "
          f"nested-bdi {bool(re.search(r'<bdi[^>]*><bdi', text))}")


if __name__ == "__main__":
    main()
