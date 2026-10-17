#!/usr/bin/env python3
"""QA gate: well-formed HTML, MD↔HTML content match (prose, quotes, lists, code), headings,
glossary rows, footer artifacts, typo guard, master-glossary duplicates."""
import re, pathlib, html as H
from html.parser import HTMLParser
from collections import Counter
VOID = {"br","hr","img","meta","link","input","area","base","col","embed","source","track","wbr"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack, self.err = [], []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack or self.stack[-1] != tag: self.err.append(f"</{tag}> vs {self.stack[-3:]}")
        else: self.stack.pop()
def norm(s): return re.sub(r"\s+", " ", s.replace("\u200e","").replace("\u200f","").replace("**","")).strip()
total = 0
here = pathlib.Path(".")
htmls = sorted(here.glob("*.html"))
for f in htmls:
    p = P(); p.feed(f.read_text(encoding="utf-8"))
    errs = p.err + ([f"unclosed {p.stack}"] if p.stack else [])
    total += len(errs)
    if errs: print(f"{f.name}: {errs}")
print(f"HTML well-formed: {len(htmls)} files, errors {total}")
for md in sorted(list(here.glob("chunk-*.md")) + list(here.glob("chapter-*.md"))):
    ht = md.with_suffix(".html").read_text(encoding="utf-8")
    text = norm(H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", ht, flags=re.S))))
    text_tight = norm(H.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<!--.*?-->", "", ht, flags=re.S))))
    src = md.read_text(encoding="utf-8").split("\n")
    blocks, fence = [], False
    for line in src:
        s = line.strip()
        if s.startswith("```"): fence = not fence; continue
        if fence:
            if s: blocks.append(norm(s))
            continue
        if not s or s == "---" or s.startswith(("#", "|", "<!--")): continue
        if s.startswith(">"): s = re.sub(r"^(?:>\s*)+", "", s).strip()   # nested "> >" too
        if not s or s.startswith("```"): continue                      # fence markers inside sideboxes
        if s.startswith("- "): s = s[2:]
        s = re.sub(r"^[0-9۰-۹]+\. ", "", s)                       # numbered-list markers
        blocks.append(norm(s.replace("`", "")))          # inline-code markers (prose only)
    miss = [b for b in blocks if b not in text_tight and b not in text]
    heads = [norm(re.sub(r"^#+\s*", "", l)) for l in src if l.startswith("##")]
    hmiss = [h for h in heads if h not in text_tight]
    rows = [l for l in src if l.startswith("| ") and not l.startswith("| واژهٔ")]
    rmiss = []
    for l in rows:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 2 and (c[0] not in text_tight or c[1] not in text_tight): rmiss.append(c[0])
    n = len(miss) + len(hmiss) + len(rmiss); total += n
    print(f"{'OK ' if not n else 'FAIL'} {md.name}: {len(blocks)}b/{len(heads)}h/{len(rows)}r miss {len(miss)}/{len(hmiss)}/{len(rmiss)}")
    for x in (miss + hmiss + rmiss)[:6]: print("    MISS:", x[:150])
bad_bt = [h.name for h in here.glob("*.html") if "`" in re.sub(r"<pre.*?</pre>", "", h.read_text(encoding="utf-8"), flags=re.S)]
total += len(bad_bt); print("leaked backticks:", bad_bt or "none")
foot = re.compile(r"(?m)^(\d+\s*\|\s*Chapter|Chapter \d+:|[A-Z][A-Za-z ]+\s*\|\s*\d+\s*$)")
bad_f = [str(f) for f in here.rglob("*") if f.is_file() and f.suffix in (".md", ".html") and foot.search(f.read_text(encoding="utf-8"))]
total += len(bad_f); print("footers:", bad_f or "clean")
bad_t = []
for f in here.rglob("*.md"):
    t = f.read_text(encoding="utf-8")
    for w in ["مصالححه", "میشود", "میگیرد", "ه‌اي", "كة", "تمرکزبر"]:
        if w in t: bad_t.append((str(f), w))
    if "ي" in t: bad_t.append((str(f), "arabic-yeh"))
    if "ك" in t: bad_t.append((str(f), "arabic-kaf"))
total += len(bad_t); print("typos:", bad_t or "clean")
nested = [f.name for f in htmls if re.search(r"<bdi[^>]*><bdi", f.read_text(encoding="utf-8"))]
print("nested bdi:", nested or "none (all files)")
lines = [l for l in open("glossary.md", encoding="utf-8") if l.startswith("| ")]
keys = [l.split("|")[1].strip() for l in lines[1:]]
dups = [k for k, c in Counter(keys).items() if c > 1]; total += len(dups)
print(f"glossary: {len(lines)-1} rows, dups {dups or 'none'}, non-approved {sum(1 for l in lines[1:] if 'مصوب' not in l)}")
print("TOTAL ISSUES:", total)
