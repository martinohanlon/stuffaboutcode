#!/usr/bin/env python3
"""
Audit every converted code block against the source HTML.

The runbook says to diff each fenced block against the live Blogger page. The
Atom export is what Blogger renders those pages from, so comparing against
blog.xml covers all 635 blocks instead of a handful, and needs no network.

Two independent checks, because they fail differently:

  content  -- tokenise the code text in the source and the code text in the
              generated Markdown, then report tokens the source has and the
              output lost (or gained). Whitespace-insensitive, so it catches
              dropped/duplicated code, not indentation.
  hygiene  -- HTML entities left raw in a fence (&lt; instead of <), stray
              markup, and tabs that never got expanded.

Indentation is covered separately by verify.py, which compiles every python
fence.

Usage:  python _import/audit.py [-v] [--post SLUG]
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter

from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert as C  # noqa: E402  reuse the exact same parsing rules

ROOT = C.ROOT
VERBOSE = "-v" in sys.argv
ONLY = None
if "--post" in sys.argv:
    ONLY = sys.argv[sys.argv.index("--post") + 1]

INLINE_CODE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}|\d{3,}")
ENTITY = re.compile(r"&(lt|gt|amp|quot|apos|nbsp|#\d+|#x[0-9a-fA-F]+);")


def source_code_text(html_str):
    """Every character the source renders as code, using convert.py's rules."""
    html_str = C.TAB_SPAN_RE.sub(lambda m: m.group(1) or " ", html_str)
    soup = BeautifulSoup(html_str, "html.parser")
    for p in soup.find_all("param"):
        p.decompose()
    for bad in soup.find_all(["script", "style", "noscript", "ins"]):
        bad.decompose()

    chunks = []
    for tag in soup.find_all(True):
        if tag.name != "pre" and not C.is_mono(tag):
            continue
        # convert.py treats a mono wrapper holding real prose blocks as prose
        if tag.name != "pre" and tag.find(
            ["p", "ul", "ol", "table", "h1", "h2", "h3", "pre"]
        ):
            continue
        # only the outermost code element, so nested spans aren't counted twice
        parent = tag.parent
        skip = False
        while parent is not None:
            if parent.name == "pre" or C.is_mono(parent):
                skip = True
                break
            parent = parent.parent
        if skip:
            continue
        chunks.append(C.mono_text(tag))
    return "\n".join(chunks)


def output_code_text(md):
    body = md.split("\n---\n", 1)[-1] if md.startswith("---\n") else md
    fences = [code for _, code, _ in C.iter_fences(body)]
    inline = INLINE_CODE.findall(C.strip_fences(body))
    return "\n".join(fences + inline), fences


def tokens(text):
    return Counter(TOKEN.findall(text))


def main():
    root = ET.parse(C.SRC).getroot()
    A, B = C.A, C.B

    # map slug -> generated file
    files = {}
    for d in ("_posts", "_drafts", "_pages"):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for n in os.listdir(p):
            if not n.endswith(".md"):
                continue
            slug = n[:-3]
            if d == "_posts":
                slug = slug[11:]
            files[slug] = os.path.join(p, n)

    checked = 0
    lost_posts = []
    gained_posts = []
    entity_hits = []
    tab_hits = []
    markup_hits = []
    fence_total = 0

    for e in root.findall(A + "entry"):
        etype = e.findtext(B + "type")
        if etype not in ("POST", "PAGE"):
            continue
        filename = (e.findtext(B + "filename") or "").strip()
        slug = re.sub(r"\.html?$", "", filename.rsplit("/", 1)[-1]) if filename else ""
        path = files.get(slug)
        if path is None:
            continue
        if ONLY and ONLY not in slug:
            continue
        checked += 1

        src = source_code_text(e.findtext(A + "content") or "")
        md = open(path, encoding="utf-8").read()
        out, fences = output_code_text(md)
        fence_total += len(fences)

        st, ot = tokens(src), tokens(out)
        lost = st - ot
        gained = ot - st
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if sum(lost.values()):
            lost_posts.append((rel, sum(lost.values()), lost.most_common(6)))
        if sum(gained.values()):
            gained_posts.append((rel, sum(gained.values()), gained.most_common(6)))

        for f in fences:
            if ENTITY.search(f):
                entity_hits.append((rel, ENTITY.search(f).group(0)))
            if "\t" in f:
                tab_hits.append(rel)
            if re.search(r"</(div|span|font|br)\b|<(div|span|font)\b", f):
                markup_hits.append(rel)

    print(f"entries checked: {checked}   fenced blocks: {fence_total}\n")

    def report(title, rows, note):
        print(f"=== {title}: {len(rows)} ===")
        if not rows:
            print("  none\n")
            return
        print(f"  ({note})")
        for rel, n, common in sorted(rows, key=lambda r: -r[1])[: (None if VERBOSE else 12)]:
            words = ", ".join(f"{w}x{c}" if c > 1 else w for w, c in common)
            print(f"  {n:5}  {rel}\n           {words}")
        print()

    report("posts where code tokens went MISSING", lost_posts, "source had them, output does not")
    report("posts where code tokens were ADDED", gained_posts, "output has them, source code did not")

    print(f"=== raw HTML entities left inside fences: {len(entity_hits)} ===")
    for rel, ent in entity_hits[:12]:
        print(f"  {rel}  {ent}")
    if not entity_hits:
        print("  none")
    print(f"\n=== unexpanded tabs in fences: {len(set(tab_hits))} ===")
    for rel in sorted(set(tab_hits))[:10]:
        print(f"  {rel}")
    if not tab_hits:
        print("  none")
    print(f"\n=== leftover markup inside fences: {len(set(markup_hits))} ===")
    for rel in sorted(set(markup_hits))[:10]:
        print(f"  {rel}")
    if not markup_hits:
        print("  none")


if __name__ == "__main__":
    main()
