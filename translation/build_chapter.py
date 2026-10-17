#!/usr/bin/env python3
"""ادغام بسته‌های یک فصل (chunk-NN.md/.html) در فایل کامل فصل (chapter-NN.md/.html).

Usage:
    python3 build_chapter.py <chapter> <chunk> [chunk ...] [--drop "heading text"]

Example:
    python3 build_chapter.py 1 1 2 3 --drop "ادامهٔ قوانین معماری نرم‌افزار" \
                                   --drop "انتظارات از یک معمار (ادامه)"

Rules:
  - H1 هر بسته حذف می‌شود؛ H1 بستهٔ اول = تیتر فایل فصل.
  - عناوین داده‌شده با --drop از MD (## text) و HTML (<h3>text</h3>) حذف می‌شوند.
  - واژه‌نامهٔ بسته‌ها ادغام و بر اساس واژهٔ انگلیسی یکتا می‌شود
    (نخستین کاربرد ملاک)، با عنوان «واژه‌نامهٔ اختصاصی این فصل».
"""
import argparse
import html as htmllib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
HR = '<hr style="border:none;border-top:1px dashed #bbb;margin:1.4rem 0;">'
GLOSS_H = "واژه‌نامهٔ اختصاصی این فصل"
GLOSS_H_CHUNK = "واژه‌نامهٔ اختصاصی این بخش"


def _split_chunk_md(n: int):
    lines = (HERE / f"chunk-{n:02d}.md").read_text(encoding="utf-8").split("\n")
    gi = next(i for i, l in enumerate(lines) if l.startswith(f"## {GLOSS_H_CHUNK}"))
    return lines[:gi], lines[gi:]


def collect_rows(chunks):
    rows, seen = [], set()
    for n in chunks:
        _, gloss = _split_chunk_md(n)
        for l in gloss:
            if l.startswith("| ") and not l.startswith("| واژهٔ انگلیسی") and not l.startswith("|---"):
                cells = [c.strip() for c in l.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[0] not in seen:
                    seen.add(cells[0])
                    rows.append((cells[0], cells[1]))
    return rows


def merge_md(title, chunks, drops):
    bodies = []
    drop_lines = {f"## {d}" for d in drops} | {f"### {d}" for d in drops}   # H2 and H3 continuation headings
    for n in chunks:
        body, _ = _split_chunk_md(n)
        if body and body[0].startswith("# "):
            body = body[1:]
        body = [l for l in body if l not in drop_lines]
        while body and body[-1].strip() in ("", "---"):
            body.pop()
        while body and not body[0].strip():
            body.pop(0)
        bodies.append("\n".join(body).strip())
    rows = collect_rows(chunks)
    md = f"# {title}\n\n" + "\n\n---\n\n".join(bodies)
    md += f"\n\n---\n\n## {GLOSS_H}\n\n"
    md += "| واژهٔ انگلیسی | معادل مصوب/به‌کاررفته در این فصل |\n|---|---|\n"
    md += "".join(f"| {en} | {fa} |\n" for en, fa in rows)
    return md, rows


def gloss_html(rows):
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
        '    <h3 style="font-size:1.35rem;color:#2c5f8a;margin:0 0 .8rem;">'
        f"{GLOSS_H}</h3>\n"
        '    <table dir="rtl" style="width:100%;border-collapse:collapse;font-size:.95rem;">\n'
        "      <thead>\n"
        '        <tr style="background:#2c5f8a;color:#fff;">\n'
        '          <th style="border:1px solid #ccc;padding:.5rem .7rem;text-align:right;">واژهٔ انگلیسی</th>\n'
        '          <th style="border:1px solid #ccc;padding:.5rem .7rem;text-align:right;">'
        "معادل مصوب/به‌کاررفته در این فصل</th>\n"
        "        </tr>\n"
        "      </thead>\n"
        "      <tbody>\n"
        f"{trs}\n"
        "      </tbody>\n"
        "    </table>\n"
        "  </section>"
    )


def merge_html(chunks, drops, rows):
    first = (HERE / f"chunk-{chunks[0]:02d}.html").read_text(encoding="utf-8")
    art = re.search(r"<article[^>]*>", first).group(0)
    h1 = re.search(r"<h1[^>]*>.*?</h1>", first, re.S).group(0)
    bodies = []
    for n in chunks:
        t = (HERE / f"chunk-{n:02d}.html").read_text(encoding="utf-8")
        start = t.index("</h1>") + len("</h1>")
        gi = t.index(GLOSS_H_CHUNK)
        hr_pos = t.rfind("<hr ", 0, gi)
        body = t[start:hr_pos]
        for d in drops:
            body = re.sub(r"<(h[34])[^>]*>" + re.escape(d) + r"</\1>\n\s*", "", body)
        bodies.append(body.strip())
    sep = "\n\n  " + HR + "\n\n  "
    inner = "\n\n  " + sep.join(bodies)
    inner += "\n\n  " + HR + "\n\n  " + gloss_html(rows)
    listed = ", ".join(f"{c:02d}" for c in chunks)
    comment = (
        f"<!-- خروجی HTML — کامپوننت کامل فصل (بدون html/head)؛ "
        f"ادغام بسته‌های {listed} -->"
    )
    return f"{comment}\n{art}\n\n  {h1}{inner}\n\n</article>\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("chapter", type=int)
    p.add_argument("chunks", type=int, nargs="+")
    p.add_argument("--drop", action="append", default=[],
                   help="عنوان ادامه‌ای که باید از MD و HTML حذف شود")
    a = p.parse_args()
    first_line = (HERE / f"chunk-{a.chunks[0]:02d}.md").read_text(encoding="utf-8").split("\n")[0]
    assert first_line.startswith("# "), first_line
    title = first_line[2:].strip()
    rows = collect_rows(a.chunks)
    md, _ = merge_md(title, a.chunks, a.drop)
    htm = merge_html(a.chunks, a.drop, rows)
    (HERE / f"chapter-{a.chapter:02d}.md").write_text(md, encoding="utf-8")
    (HERE / f"chapter-{a.chapter:02d}.html").write_text(htm, encoding="utf-8")
    print(f"chapter-{a.chapter:02d}.md/html written; glossary rows: {len(rows)}")


if __name__ == "__main__":
    main()
