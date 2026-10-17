#!/usr/bin/env python3
"""تبدیل Markdownِ یک بسته به کامپوننت HTMLِ راست‌به‌چپ (سبکِ یکسان با بسته‌های پیشین).

Usage:
    python3 md2html.py chunk-10.md chunk-10.html --terms source/chunk-10.terms --num ۱۰

Supported blocks: H1 / H2(→h3) / H3(→h4) / H4(→h5) / plain "> …" quotes / paragraphs (inline **bold**) /
fenced code (any language, LTR <pre>) / "- " lists (consecutive → one <ul>) /
"> **شکل …**" figures / "**جدول …**" + body tables / "> **نکته:** …" tip callouts / "> … > — Name" aphorisms / "> **title** …" sideboxes /
"---" separators (rendered as <hr> between top-level sections) / final glossary.

English wrapping: parenthesised Latin-only content → one <bdi>(…)</bdi>; mixed
parentheses keep "(" ")" and bare-wrap inside; bare terms come from the --terms
file (one per line) and are matched in ONE combined regex pass (no nesting).
"""
import argparse
import html as htmllib
import re
from pathlib import Path
PERSIAN = re.compile(r"[\u0600-\u06FF]")

ART = ('<article dir="rtl" lang="fa" style="font-family:\'Vazirmatn\',\'IRANSans\',\'Tahoma\',sans-serif;'
       'line-height:2;max-width:46rem;margin:0 auto;color:#1a1a1a;background:#fff;padding:1.5rem;'
       'border:1px solid #e5e5e5;border-radius:8px;">')
H1 = 'font-size:1.7rem;margin:0 0 1rem;border-bottom:3px solid #2c5f8a;padding-bottom:.5rem;'
H3 = "font-size:1.35rem;color:#2c5f8a;margin:0 0 .8rem;"
H4 = "font-size:1.15rem;color:#2c5f8a;margin:1.2rem 0 .6rem;"
H5 = "font-size:1.05rem;color:#2c5f8a;margin:1rem 0 .5rem;"
PLAINQ = ('margin:1rem 0;padding:.6rem 1.2rem;background:#fafbfc;border-right:3px solid #9bb4cc;'
          'border-radius:4px;font-size:.98rem;text-align:justify;')
PAD = ("display:inline-block;unicode-bidi:isolate;font-family:Consolas,Monaco,monospace;"
       "background:#f4f6f8;border:1px solid #dde3e8;border-radius:3px;padding:0 .35em;direction:ltr;")
PAD92 = PAD.replace("monospace;", "monospace;font-size:.92em;")
ISO = "display:inline-block;unicode-bidi:isolate;direction:ltr;"
QUOTA = ('margin:1rem 0;padding:1rem 1.2rem;background:#eef4fa;border-right:5px solid #2c5f8a;'
         'border-radius:4px;font-size:1.05rem;font-weight:bold;text-align:center;')
SIDEBAR = ('margin:1.2rem 0;padding:1rem 1.2rem;background:#f7f9fb;border:1px solid #dde3e8;'
           'border-right:4px solid #2c5f8a;border-radius:4px;font-size:.98rem;text-align:justify;')
FOOTER = 'display:block;margin-top:.6rem;font-size:.9rem;font-weight:normal;color:#555;'
TIP = ('margin:1rem 0;padding:.8rem 1.1rem;background:#eef8f1;border:1px solid #cfe8d6;'
       'border-right:5px solid #2e8b57;border-radius:4px;font-size:1rem;text-align:justify;')
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
    paren_re = re.compile(r"\([^()]+\)")

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

    code_terms = [t for t in terms if "(" in t or ")" in t]   # e.g. main(), f(x, y): atomic
    code_re = re.compile("(" + "|".join(re.escape(t) for t in code_terms) + ")") if code_terms else None

    def plain(text):
        if "`" in text:                                   # inline code / inline LaTeX: `x`, `$CC = E - N + 2$`
            pieces = re.split(r"`([^`]+)`", text)
            if len(pieces) > 1:
                return "".join(bdi(x) if i % 2 else plain(x) for i, x in enumerate(pieces))
        if code_re is not None:
            pieces = code_re.split(text)
            if len(pieces) > 1:
                return "".join(bdi(x) if i % 2 else plain_parens(x) for i, x in enumerate(pieces))
        return plain_parens(text)

    def plain_parens(text):
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

    pending_kind = ["ul"]                             # "ul" or "ol" (numbered list)

    def close_ul():
        nonlocal pending_ul
        if pending_ul:
            tag = pending_kind[0]
            current.append(f'    <{tag} style="{UL}">')
            current.extend(f"      <li>{inline(x)}</li>" for x in pending_ul)
            current.append(f"    </{tag}>")
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
        raw = [l[2:] if l.startswith("> ") else l[1:] for l in b]   # keeps code indentation
        paras, buf, nested = [], [], {}
        i = 0
        while i < len(qs):
            q = qs[i]
            if q.startswith("```"):                   # fenced code inside a sidebox
                if buf: paras.append(" ".join(buf)); buf = []
                lang = q[3:].strip() or "text"
                j = i + 1
                while j < len(qs) and not qs[j].startswith("```"):
                    j += 1
                code = htmllib.escape("\n".join(raw[i + 1:j]), quote=False)
                key = f"\x00NEST{len(nested)}\x00"
                nested[key] = f'  <pre dir="ltr" style="{PRE}"><code class="language-{lang}">{code}</code></pre>'
                paras.append(key)
                i = j + 1
                continue
            if q.startswith(">"):                     # nested quote inside a sidebox ("> > …")
                if buf: paras.append(" ".join(buf)); buf = []
                nb = []
                while i < len(qs) and qs[i].startswith(">"):
                    nb.append(qs[i]); i += 1
                key = f"\x00NEST{len(nested)}\x00"
                nested[key] = quote(nb).replace("\n", "\n  ")
                paras.append(key)
                continue
            if q == "":
                if buf: paras.append(" ".join(buf)); buf = []
            else:
                buf.append(q)
            i += 1
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
            at = attrib.lstrip("—").strip()
            foot = inline(at) if PERSIAN.search(at) else bdi(at, iso=True)   # Persian attribution stays RTL
            return (f'    <blockquote style="{QUOTA}">\n      {inline(unb(first))}\n'
                    f'      <footer style="{FOOTER}">— {foot}</footer>\n'
                    f'    </blockquote>')
        if first.startswith("**نکته") and len(paras) == 1:   # tip callout (book's lemur/tip icon)
            return (f'    <aside role="note" style="{TIP}">\n      <p style="margin:0;">{inline(first)}</p>\n    </aside>')
        if not first.startswith("**"):                 # plain quotation (no title, no attribution)
            ps = [f'      <p style="margin:.35rem 0;">{inline(p)}</p>' for p in paras]
            return f'    <blockquote style="{PLAINQ}">\n' + "\n".join(ps) + "\n    </blockquote>"
        ps = [f'    <p style="font-weight:bold;text-align:center;margin:0 0 .7rem;">{inline(unb(first))}</p>']
        def body(p):
            if p in nested: return "  " + nested[p]
            if p.startswith("**شکل"): return "  " + quote(["> " + p]).replace("\n", "\n  ")   # figure inside a sidebox
            return f'    <p style="text-align:justify;margin:.55rem 0;">{inline(p)}</p>'
        ps += [body(p) for p in paras[1:]]
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
        if b[0].startswith("#### "):
            ensure(); close_ul()
            current.append(f'    <h5 style="{H5}">{inline(b[0][5:].strip())}</h5>')
        elif b[0].startswith("### "):
            ensure(); close_ul()
            current.append(f'    <h4 style="{H4}">{inline(b[0][4:].strip())}</h4>')
        elif b[0].startswith("## "):
            start_section(f'    <h3 style="{H3}">{inline(b[0][3:].strip())}</h3>')
        elif b[0].startswith(">"):
            ensure(); close_ul()
            current.append(quote(b))
        elif all(l.startswith("|") for l in b):        # body table (→ figure + figcaption)
            ensure(); close_ul()
            cap = ""
            if current and current[-1].startswith('    <p style="text-align:justify;"><b>جدول'):
                cap_html = current.pop()[len('    <p style="text-align:justify;">'):-len("</p>")]
                cap = (f'      <figcaption style="font-size:.95rem;color:#333;margin-bottom:.5rem;" dir="rtl">'
                       f'{cap_html}</figcaption>\n')
            cells = [[c.strip() for c in l.strip().strip("|").split("|")] for l in b if not re.match(r"^\|[-:| ]+\|$", l)]
            th = "".join(f'<th style="border:1px solid #ccc;padding:.45rem .6rem;">{inline(c)}</th>' for c in cells[0])
            trs = "\n".join("          <tr>" + "".join(
                f'<td style="border:1px solid #ccc;padding:.4rem .6rem;vertical-align:top;">{inline(c)}</td>' for c in r)
                + "</tr>" for r in cells[1:])
            current.append(
                f'    <figure style="{FIG}">\n{cap}'
                '      <table dir="rtl" style="width:100%;border-collapse:collapse;font-size:.95rem;text-align:right;">\n'
                f'        <thead>\n          <tr style="background:#2c5f8a;color:#fff;">{th}</tr>\n        </thead>\n'
                f'        <tbody>\n{trs}\n        </tbody>\n      </table>\n    </figure>')
        elif all(l.startswith("- ") for l in b):
            ensure()
            if pending_kind[0] != "ul": close_ul()
            pending_kind[0] = "ul"
            pending_ul.extend(l[2:].strip() for l in b)
        elif all(re.match(r"^[0-9۰-۹]+\. ", l) for l in b):   # numbered list item(s) → <ol>
            ensure()
            if pending_kind[0] != "ol": close_ul()
            pending_kind[0] = "ol"
            pending_ul.extend(re.sub(r"^[0-9۰-۹]+\. ", "", l).strip() for l in b)
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
