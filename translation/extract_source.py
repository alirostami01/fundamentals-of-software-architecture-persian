#!/usr/bin/env python3
"""استخراج منبع انگلیسیِ بسته‌ها از PDF با PyMuPDF (بازسازی پاراگراف با فاصلهٔ عمودی خطوط).

Usage:
    python3 extract_source.py OUT.md --start-page 63 --stop-page 68 \
        --start-at "Measuring Modularity" --stop-at "Core Metrics"

Rules:
  - classification by (size, left, bold, italic): H2 (>=17), H3 (15.5-17 @72),
    sidebox title (14-15.5 bold), quote (9.3@~90), attribution (9.3 + em-dash),
    listing heads (10.0@72), bullets (10.5@~81), definition terms (full-italic@72),
    figure/equation captions (full-italic), box bodies (10.0@~80),
    equation pieces (<=10 @>86) are dropped (re-insert formulas manually).
  - paragraphs: same-class lines with top-gap <=15.5pt; across pages, continue
    only when the previous line does not end a sentence.
"""
import argparse
import html as H
import re
from pathlib import Path

import pymupdf
import glob

PDF = sorted(glob.glob("*.pdf"))[0]
PAT = re.compile(r'<p style="top:([\d.]+)pt;left:([\d.]+)pt;line-height:([\d.]+)pt">(.*?)</p>', re.S)
TERMINAL = ".!?”’\")"
H2_SIZE = 17.0
GAP_LIMIT = 15.5


def classify(top, left, size, bold, inner, txt):
    if size == 9.0 and top > 580:
        return None                                   # footer
    if top < 120 and size > 14 and left > 200:
        return None                                   # running banner
    full_ital = bool(re.match(r"^<i>.*</i>$", inner.strip(), re.S))
    if size >= H2_SIZE and bold and left < 200:
        return "H2"
    if 15.5 <= size < H2_SIZE and bold and left < 100:
        return "H3"
    if 14 <= size < 15.5 and bold:
        return "SIDEBOXTITLE"
    if txt.startswith("—"):
        return "ATTRIB"
    if size <= 9.5 and left >= 110:
        return "DROP"                                 # equation pieces (limits)
    if size <= 9.5:
        return "QUOTE"
    if full_ital and left < 80 and txt.startswith("Figure"):
        return "FIGCAP"
    if full_ital and 84 <= left <= 90:
        return "EQCAP"
    coh_types = ("Functional cohesion", "Sequential cohesion",
                 "Communicational cohesion", "Procedural cohesion",
                 "Temporal cohesion", "Logical cohesion", "Coincidental cohesion")
    if full_ital and left < 80 and txt.startswith(coh_types):
        return "DEFTERM"
    if size == 10.5 and left == 72.0:
        return "MAIN"
    if size == 10.0 and left == 72.0:
        return "LISTHEAD"
    if size == 10.5 and 76 <= left <= 86:
        return "BULLET"
    if size == 10.0 and 76 <= left <= 86:
        return "BOX"
    if size == 10.5 and 86 < left < 97:
        return "INDENT"                               # wrap of BULLET/DEFTERM
    return "DROP"                                     # equation pieces etc.


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--start-page", type=int, required=True)
    ap.add_argument("--stop-page", type=int, required=True, help="inclusive")
    ap.add_argument("--start-at", default=None, help="emit only from this heading")
    ap.add_argument("--stop-at", default=None, help="stop before this heading")
    a = ap.parse_args()

    doc = pymupdf.open(PDF)
    lines = []                                        # (page, top, size, cls, txt)
    started = a.start_at is None
    for pno in range(a.start_page, a.stop_page + 1):
        h = doc[pno].get_text("html")
        for m in PAT.finditer(h):
            top, left = float(m.group(1)), float(m.group(2))
            inner = m.group(4)
            bold = "<b>" in inner or "<strong>" in inner
            sz = re.search(r"font-size:([\d.]+)pt", inner)
            size = float(sz.group(1)) if sz else 0
            txt = H.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
            if not txt or txt == "•":
                continue
            cls = classify(top, left, size, bold, inner, txt)
            if cls is None:
                continue
            if not started:
                if cls in ("H2", "H3") and txt == a.start_at:
                    started = True
                else:
                    continue
            if a.stop_at and cls in ("H2", "H3") and txt == a.stop_at:
                break
            if cls == "DROP":
                continue
            lines.append([pno, top, size, cls, txt])
        else:
            continue
        break

    blocks, cur = [], None                            # (cls, [(page,top,txt), ...])
    last_top = last_page = last_cls = None

    def flush():
        nonlocal cur
        if cur:
            blocks.append((cur[0], [t for _, _, t in cur[1]]))
        cur = None

    for pg, top, size, cls, txt in lines:
        if cls == "INDENT" and last_cls in ("BULLET", "DEFTERM"):
            cls = last_cls                            # continuation inherits
        if cur is None:
            cur = (cls, [(pg, top, txt)])
        elif cls != last_cls:
            flush()
            cur = (cls, [(pg, top, txt)])
        else:
            prev = cur[1][-1][2]
            if pg != last_page:
                if prev and prev[-1] in TERMINAL:
                    flush()
                    cur = (cls, [(pg, top, txt)])
                else:
                    cur[1].append((pg, top, txt))
            elif top - last_top > GAP_LIMIT:
                flush()
                cur = (cls, [(pg, top, txt)])
            else:
                cur[1].append((pg, top, txt))
        last_top, last_page, last_cls = top, pg, cls
    flush()

    def join(ls):
        out = ls[0]
        for s in ls[1:]:
            if out and out[-1] in "\u2010\u2011-":
                out = out[:-1] + s
            else:
                out = out + " " + s
        return re.sub(r"[ \t]+", " ", out).strip()

    parts = []
    i = 0
    while i < len(blocks):
        cls, ls = blocks[i]
        if cls == "LISTHEAD":                          # listing head + its bullets
            merged = list(ls)
            while i + 1 < len(blocks) and blocks[i + 1][0] == "BULLET":
                i += 1
                merged += blocks[i][1]
            parts.append("```text\n" + "\n".join(merged) + "\n```")
        elif cls == "BULLET":                          # prose (question) bullets
            txt = join(ls)
            items = [x.strip() for x in re.split(r"(?=• )", txt) if x.strip()]
            parts.append("\n".join(
                "- " + (x[2:].strip() if x.startswith("• ") else x) for x in items))
        else:
            txt = join(ls).replace("GoTo", "Go To")
            if cls == "H2":
                parts.append(f"## {txt}")
            elif cls == "H3":
                parts.append(f"### {txt}")
            else:
                parts.append(txt)
        i += 1
    src = "\n\n".join(parts).strip() + "\n"
    Path(a.out).write_text(src, encoding="utf-8")
    words = len(re.findall(r"[A-Za-z][A-Za-z0-9'’().;/-]*", src))
    print(f"{a.out}: {len(blocks)} blocks, {words} words")
    for i, (c, ls) in enumerate(blocks):
        print(f"{i+1:2d} {c:11s} ({len(ls)}) {join(ls)[:66]}")


if __name__ == "__main__":
    main()
