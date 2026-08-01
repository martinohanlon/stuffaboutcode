#!/usr/bin/env python3
"""
Blogger (Google Takeout 2018 schema) -> Jekyll Markdown.

Reads _import/blog.xml (Takeout/Blogger/Blogs/<blog>/feed.atom) and writes
_posts/, _drafts/ and _pages/.

Why this exists instead of jekyll-import: the Takeout export uses the 2018
Blogger schema (xmlns:blogger="http://schemas.google.com/blogger/2018", with
<blogger:type>POST</blogger:type> instead of the old GData
<category scheme=".../g/2005#kind">). jekyll-import's Blogger importer parses
the old format only and aborts on this file with
"only <title type=\"text\"></title> is supported".

Re-runnable: always regenerates from blog.xml, so it is safe to iterate on.

Usage:  python _import/convert.py [--report]
"""

import ast
import html
import io
import os
import re
import shutil
import sys
import tokenize
import unicodedata
import warnings
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup, NavigableString, Tag

# reindent_python() compiles the posts' own code to check its rewrite. 2012-era
# regex strings contain invalid escapes like "\*", which warn on every parse.
# That is the published code, not a conversion problem.
warnings.filterwarnings("ignore", category=SyntaxWarning)

A = "{http://www.w3.org/2005/Atom}"
B = "{http://schemas.google.com/blogger/2018}"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_import", "blog.xml")
LONDON = ZoneInfo("Europe/London")

# ---------------------------------------------------------------- labels

# Blogger label -> (slug, display name). Slugs per the runbook: lowercase,
# hyphenated, no punctuation that needs escaping in a URL.
LABELS = {
    "raspberry pi": ("raspberry-pi", "raspberry pi"),
    "Python": ("python", "python"),
    "minecraft": ("minecraft", "minecraft"),
    "games": ("games", "games"),
    "gpio": ("gpio", "gpio"),
    "social networking": ("social-networking", "social networking"),
    "camera": ("camera", "camera"),
    "microbit": ("microbit", "microbit"),
    "Adventures in Minecraft": ("adventures-in-minecraft", "adventures in minecraft"),
    "get_iplayer": ("get-iplayer", "get_iplayer"),
    "c": ("c", "c"),
    "c#": ("csharp", "c#"),
    ".net": ("dotnet", ".net"),
    "RSS": ("rss", "rss"),
    "gps": ("gps", "gps"),
    "raspbmc / xbmc": ("raspbmc-xbmc", "raspbmc / xbmc"),
    "Car": ("car", "car"),
    "robot": ("robot", "robot"),
    "asp": ("asp", "asp"),
    "html": ("html", "html"),
    "xml": ("xml", "xml"),
    "scratch": ("scratch", "scratch"),
}

# Labels that hint at a fence language when the code itself is ambiguous.
LABEL_LANG = {
    "python": "python",
    "csharp": "csharp",
    "dotnet": "csharp",
    "c": "c",
    "asp": "asp",
    "html": "html",
    "xml": "xml",
}


def slug_label(term):
    if term in LABELS:
        return LABELS[term][0]
    s = unicodedata.normalize("NFKD", term).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "misc"


# ---------------------------------------------------------------- code detection

MONO_RE = re.compile(r"courier|monospace|consolas|monaco", re.I)

PY_HINT = re.compile(
    r"^\s*(import \w|from \w+ import |def \w|class \w|print\(|print |if __name__|"
    r"@[A-Za-z_]\w*\s*[(\n]|#!.*python)",
    re.M,
)

# Something that actually reads as Python, used to gate the label-based
# fallback: a post labelled "Python" also contains sensor dumps and config
# snippets, and those should not land in a python fence.
PY_TOKENS = re.compile(
    r"\b(import|def|class|return|elif|lambda|None|True|False|self|len|range|str|int)\b"
    r"|^\s*(for|while|if|try|except|print)\b",
    re.M,
)
SH_HINT = re.compile(
    r"^\s*(\$ |sudo |apt-get |apt |pip |pip3 |git |cd |ls |chmod |chown |wget |curl |mkdir |"
    r"nano |vi |python |python3 |make |\./|gem |bundle |raspi-config|modprobe|echo |cp |mv |"
    r"rm |tar |unzip |gunzip |mount |umount |service |systemctl |startx |java |javac |gcc |"
    r"ifconfig|iwconfig|crontab|reboot|shutdown|dpkg |update-rc\.d|scp |ssh |touch |cat |"
    r"grep |raspistill|raspivid|omxplayer|mkfs|dd |df |top|kill |killall )",
    re.M,
)

# Console output / error text rather than source.
OUT_HINT = re.compile(r"^\w[\w .-]*: (invalid|command not found|No such file|error|cannot)", re.I)

# pydoc / man output and argparse usage text: prose in a code box, not source.
DOC_HINT = re.compile(
    r"^(NAME|SYNOPSIS|DESCRIPTION|usage:)\s*$|^(NAME|usage:)\s", re.M
)


def guess_lang(code, label_slugs):
    c = code.strip()
    low = c.lower()

    # Output/doc text first: pydoc dumps contain lines like "class GpioRap",
    # which otherwise reads as Python source.
    if OUT_HINT.search(c) or DOC_HINT.search(c):
        return "text"
    if low.startswith("<?xml") or re.search(r"</(project|configuration|settings)>", low):
        return "xml"
    if re.search(r"<%|%>", c):
        return "asp"
    # A block that opens with a tag is markup. Requiring a closing </div> or
    # </html> misses `<meta ... />` (html) and `<advancedsettings>` (xml).
    if re.match(r"^\s*<[a-zA-Z!]", c):
        if re.search(
            r"<!doctype html|</html>|</body>|</div>|<div\b|<script\b|<meta\b|<link\b"
            r"|<img\b|<a\s|<span\b|<iframe\b|<p\b|<br",
            low,
        ):
            return "html"
        if re.search(r"</[\w:.-]+>", c):
            return "xml"
        return "html"
    if re.search(r"^\s*#include\b", c, re.M):
        return "c"
    if re.search(r"\busing System\b|\bnamespace \w+|\bpublic (class|static void)\b", c):
        return "csharp"
    if PY_HINT.search(c):
        return "python"
    if re.search(r"\bfunction\s*\(|\bvar \w+\s*=|=>|console\.log", c):
        return "javascript"
    if OUT_HINT.search(c) or DOC_HINT.search(c):
        return "text"
    if SH_HINT.search(c):
        return "bash"
    if is_yaml(c):
        return "yaml"
    # Indentation after a colon is a Python tell, but only alongside something
    # that reads as Python -- YAML and `screen -ls` output match it too.
    if re.search(r":\s*\n\s+\S", c) and PY_TOKENS.search(c):
        return "python"
    # Fall back to the post's labels only for something that actually looks like
    # a listing. A bare one-liner tagged python purely because the post is
    # labelled "Python" is how shell commands ended up in python fences.
    if "\n" in c.strip():
        for s in label_slugs:
            lang = LABEL_LANG.get(s)
            if lang == "python" and not PY_TOKENS.search(c):
                continue
            if lang:
                return lang
    return "text"


YAML_LINE = re.compile(r"^\s*(#|-\s|[\w.-]+:(\s|$))")


def is_yaml(code):
    """A config block (Bukkit server.properties style YAML) rather than source."""
    lines = [l for l in code.split("\n") if l.strip()]
    if len(lines) < 2 or PY_TOKENS.search(code):
        return False
    return all(YAML_LINE.match(l) for l in lines)


def is_mono(tag):
    """A span/div/font that renders its content as code."""
    if not isinstance(tag, Tag):
        return False
    if tag.name == "code":
        return True
    if tag.name not in ("span", "div", "font", "p"):
        return False
    if MONO_RE.search(tag.get("style") or ""):
        return True
    if tag.name == "font" and MONO_RE.search(tag.get("face") or ""):
        return True
    cls = " ".join(tag.get("class") or [])
    if re.search(r"prettyprint|pretty_print", cls):
        return True
    return False


def mono_text(tag):
    """Text of a mono element, with <br> as newline. Tabs already substituted."""
    out = []

    def walk(node):
        for ch in node.children:
            if isinstance(ch, NavigableString):
                out.append(str(ch))
            elif ch.name == "br":
                out.append("\n")
            else:
                walk(ch)

    walk(tag)
    return "".join(out)


# ---------------------------------------------------------------- inline markdown

MD_ESCAPE = re.compile(r"([\\`*\[\]])")
# Only underscores that could open or close emphasis need escaping; GFM ignores
# intra-word ones, so leave mcpi_protocol_spec.txt readable for hand-editing.
MD_ESCAPE_US = re.compile(r"(?<![A-Za-z0-9])_|_(?![A-Za-z0-9])")
# A tag-shaped "<" in prose is literal text, not markup. The blog's own name is
# `<Stuff about="code" />`, and kramdown otherwise swallows it as raw HTML --
# which silently deleted the site name from the About page. Backslash-escaped
# rather than turned into &lt;, so the source stays readable and the
# unresolved-entity check in verify.py keeps meaning something.
MD_ESCAPE_LT = re.compile(r"<(?=[A-Za-z/!?])")


def esc(text):
    text = text.replace(" ", " ")
    text = MD_ESCAPE.sub(r"\\\1", text)
    text = MD_ESCAPE_US.sub(r"\\_", text)
    return MD_ESCAPE_LT.sub(r"\\<", text)


def inline(node, ctx):
    """Inline markdown for a prose node."""
    return "".join(inline_one(ch, ctx) for ch in node.children)


def inline_one(ch, ctx):
    """Inline markdown for a single node."""
    if isinstance(ch, NavigableString):
        return esc(re.sub(r"\s+", " ", str(ch)))

    n = ch.name
    if n == "br":
        return "  \n"
    if n in ("b", "strong"):
        inner = inline(ch, ctx).strip()
        return f"**{inner}**" if inner else ""
    if n in ("i", "em"):
        inner = inline(ch, ctx).strip()
        return f"*{inner}*" if inner else ""
    if n == "code" or is_mono(ch):
        inner = mono_text(ch).strip()
        if not inner:
            return ""
        tick = "`" if "`" not in inner else "``"
        return f"{tick}{inner}{tick}"
    if n == "a":
        href = (ch.get("href") or "").strip()
        img = ch.find("img")
        if img is not None:
            # thumbnail linking to full size: keep the full-size target
            return image_md(img, ctx, prefer=href)
        txt = inline(ch, ctx).strip()
        if not href:
            return txt
        return f"[{txt}]({href})" if txt else ""
    if n == "img":
        return image_md(ch, ctx)
    if n in ("iframe", "object", "embed"):
        return embed_md(ch, ctx)
    return inline(ch, ctx)


def load_image_map():
    """remote url -> local path, written by _import/images.py.

    Applying the rewrite here rather than editing _posts keeps the whole
    pipeline reproducible: convert.py alone regenerates every file.
    """
    path = os.path.join(ROOT, "_import", "image-map.tsv")
    m = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if line.startswith("#") or "\t" not in line:
                continue
            u, _, p = line.rstrip("\n").partition("\t")
            m[u] = p
    return m


IMAGE_MAP = load_image_map()


def image_md(img, ctx, prefer=None):
    src = (img.get("src") or "").strip()
    if prefer and re.search(r"googleusercontent|blogspot|\.(png|jpe?g|gif)($|\?)", prefer, re.I):
        src = prefer
    if not src:
        return ""
    alt = (img.get("alt") or "").strip()
    if src in IMAGE_MAP:
        local = IMAGE_MAP[src]
        if not local:
            ctx["dropped_ads"] += 1  # affiliate / ad artwork
            return ""
        ctx["local_images"] = ctx.get("local_images", 0) + 1
        return f"![{alt}]({local})"
    ctx["images"].append(src)
    return f"![{alt}]({src})"


YT_RE = re.compile(
    r"(?:youtube(?:\.googleapis)?\.com/(?:v/|embed/|watch\?v=)|youtu\.be/)([\w-]{6,})"
)


def embed_md(tag, ctx):
    src = tag.get("src") or tag.get("data") or ""
    m = YT_RE.search(src)
    if m:
        ctx["youtube"].append(m.group(1))
        return f"\n\n{{% include youtube.html id=\"{m.group(1)}\" %}}\n\n"
    if re.search(r"amazon|adsbygoogle|googlesyndication|doubleclick", src, re.I):
        ctx["dropped_ads"] += 1
        return ""
    if not src or src.strip().lower().startswith(("javascript:", "about:", "#")):
        # a script-driven widget with no real source; nothing to migrate
        ctx["dropped_ads"] += 1
        return ""
    ctx["other_embeds"].append(src)
    title = "Google Slides presentation" if "docs.google.com" in src else "Embedded content"
    return f'\n\n{{% include embed.html src="{src}" title="{title}" %}}\n\n'


# ---------------------------------------------------------------- block markdown

BLOCK_SKIP = re.compile(r"adsbygoogle|googlesyndication|doubleclick|amazon-ad", re.I)

# Blogger's hand-rolled code boxes: a div with a visible border or fill.
BOX_STYLE = re.compile(r"border|background", re.I)

# Mono elements that are block-level, so each one is its own code line.
BLOCK_MONO = {"div", "p", "center", "section", "article", "li", "tr", "td"}


INLINE_TAGS = {
    "a", "b", "strong", "i", "em", "u", "small", "sub", "sup", "abbr", "s",
    "strike", "img", "code", "big", "tt", "cite", "q", "label",
}


def blocks(node, ctx, depth=0):
    """Yield ('code'|'para'|'md'|'br'|'boundary', text) tokens for a container.

    Consecutive inline content accumulates into a buffer and is flushed as whole
    paragraphs, split on runs of <br>. Emitting each <a>/<b>/text node as its own
    token instead is what turned single sentences into a stack of one-line
    paragraphs on the first pass.
    """
    out = []
    buf = []

    def flush():
        if not buf:
            return
        raw = "".join(buf)
        del buf[:]
        for part in re.split(r"\n[ \t]*\n+", raw):
            part = re.sub(r"[ \t]+", " ", part).strip()
            if part:
                out.append(("para", part))

    for ch in node.children:
        if isinstance(ch, NavigableString):
            s = str(ch)
            if not s.strip():
                # Blogger separates adjacent code spans with a bare &nbsp;
                # (`update-rc.d -f` + nbsp + `NameOfYourScript`). Dropping it as
                # whitespace welds the two tokens together.
                if (
                    not buf
                    and out
                    and out[-1][0] == "code"
                    and re.search(r"[ \xa0]", s)
                    and not out[-1][1].endswith((" ", "\n"))
                ):
                    out.append(("code", " "))
                continue
            buf.append(esc(re.sub(r"[ \t\r\n]+", " ", s)))
            continue

        n = ch.name

        if n in INLINE_TAGS:
            buf.append(inline_one(ch, ctx))
            continue

        if n in ("script", "style", "noscript", "form", "ins"):
            if n == "ins" or BLOCK_SKIP.search(str(ch.get("class") or "")):
                ctx["dropped_ads"] += 1
            continue

        # --- code ------------------------------------------------------
        if n == "pre" or is_mono(ch):
            # a mono wrapper holding real prose blocks should not become code
            if n != "pre" and ch.find(["p", "ul", "ol", "table", "h1", "h2", "h3", "pre"]):
                flush()
                out.extend(blocks(ch, ctx, depth + 1))
                continue
            flush()
            txt = mono_text(ch)
            if n == "pre":
                out.append(("boundary", ""))
                out.append(("code", txt))
                out.append(("boundary", ""))
                continue
            if n in BLOCK_MONO:
                # A mono <div> is one code line. The leading newline is source
                # formatting from `<div>\ncode</div>`, not content.
                if txt.startswith("\n"):
                    txt = txt[1:]
                out.append(("code", txt))
                out.append(("nl", ""))
            else:
                out.append(("code", txt))
            continue

        if n == "br":
            # inside a code run a <br> ends a line; in prose it separates
            # paragraphs once doubled.
            if not buf and out and out[-1][0] == "code":
                out.append(("br", ""))
            else:
                buf.append("\n")
            continue

        # --- headings --------------------------------------------------
        if n in ("h1", "h2", "h3", "h4", "h5", "h6"):
            flush()
            # The post h1 is the title, so body headings start at h2. Blogger
            # templates used <h3> for section headings, so a flat +1 demotion
            # buried most of them at h4 -- and the theme's signature "##" marker
            # only applies to h2/h3. Shift per post so the shallowest heading
            # used becomes h2, which keeps any real nesting intact.
            lvl = min(6, max(2, int(n[1]) + ctx.get("h_offset", 1)))
            t = inline(ch, ctx).strip()
            if t:
                out.append(("md", f"{'#' * lvl} {t}"))
            continue

        # --- lists -----------------------------------------------------
        if n in ("ul", "ol"):
            flush()
            out.append(("md", list_md(ch, ctx)))
            continue

        if n == "blockquote":
            flush()
            inner = render(blocks(ch, ctx, depth + 1), ctx)
            q = "\n".join(("> " + ln).rstrip() for ln in inner.strip().split("\n"))
            out.append(("md", q))
            continue

        if n == "table":
            flush()
            # Blogger wraps a captioned image in a table, not a data table.
            if "tr-caption-container" in " ".join(ch.get("class") or []):
                out.extend(blocks(ch, ctx, depth + 1))
            else:
                out.append(("md", table_md(ch, ctx)))
            continue

        if n in ("iframe", "object", "embed"):
            flush()
            m = embed_md(ch, ctx).strip()
            if m:
                out.append(("md", m))
            continue

        if n == "hr":
            flush()
            out.append(("md", "---"))
            continue

        # --- containers ------------------------------------------------
        if n in (
            "div", "p", "center", "span", "font", "section", "article",
            "tbody", "thead", "tr", "td", "th", "colgroup",
        ):
            cls = " ".join(ch.get("class") or [])
            if "tr-caption" in cls and "tr-caption-container" not in cls:
                flush()
                cap = inline(ch, ctx).strip()
                if cap:
                    out.append(("md", f"*{cap}*"))
                continue
            flush()
            kids = blocks(ch, ctx, depth + 1)
            if n == "p" and kids:
                out.append(("para", render(kids, ctx)))
            else:
                # A bordered/shaded div holding code is one code box; the next
                # such div is a separate listing, so fence them apart.
                boxed = BOX_STYLE.search(ch.get("style") or "") and any(
                    k == "code" for k, _ in kids
                )
                if boxed:
                    out.append(("boundary", ""))
                out.extend(kids)
                # A closing block element ends the current line. Posts that put
                # each code line in its own <div> (with no <br>) rely on this;
                # without it the whole listing collapses onto one line.
                if kids and kids[-1][0] == "code":
                    out.append(("br", ""))
                if boxed:
                    out.append(("boundary", ""))
            continue

        # fallback: treat as inline, node included
        buf.append(inline_one(ch, ctx))

    flush()
    return out


# The closing run must be at least as long as the opening one (\2 back-reference
# plus any extra), per CommonMark. Accepting any 3+ run lets a ``` inside a
# ````-fenced block close it early, which silently splits one block into two.
FENCE_RE = re.compile(
    r"^([ \t]*)(`{3,})([\w+-]*)[ \t]*\n(.*?)^\1\2`*[ \t]*$", re.M | re.S
)


def iter_fences(markdown):
    """Yield (lang, code) for every fenced block, dedented.

    Handles fences indented inside a list item. A regex anchored hard at column
    zero silently skips those, which meant the audit reported their code as
    missing and verify.py never syntax-checked it.
    """
    for m in FENCE_RE.finditer(markdown):
        indent, lang, body = m.group(1), m.group(3), m.group(4)
        if indent:
            body = "\n".join(
                ln[len(indent) :] if ln.startswith(indent) else ln
                for ln in body.split("\n")
            )
        yield lang, body


def strip_fences(markdown):
    """Markdown with every fenced block removed."""
    return FENCE_RE.sub("", markdown)


def still_inside(tag, root):
    """False once an ancestor has been extracted from root."""
    p = tag
    while p is not None:
        if p is root:
            return True
        p = p.parent
    return False


def pop_code(el, ctx):
    """Remove block-level listings from a list node and return them fenced.

    Blogger puts step-by-step code either inside an <li> or -- more awkwardly --
    in a <div><pre> that is a *sibling* of the <li> elements. The sibling case
    was being dropped entirely, because walking only `li` children never visits
    it. The in-<li> case was rendered as inline backticks, collapsing a
    multi-line listing onto one line.
    """
    out = []
    for tag in list(el.find_all(True)):
        if not still_inside(tag, el):
            continue
        if tag.name == "pre" or (is_mono(tag) and "\n" in mono_text(tag)):
            if tag.find_parent("pre") is not None:
                continue
            txt = mono_text(tag)
            tag.extract()
            if txt.strip():
                out.append(fence(txt, ctx))
    return out


def list_md(node, ctx, indent=0):
    ordered = node.name == "ol"
    pad = "  " * indent
    lines = []
    i = 0

    def attach(block):
        # Indent the fence so it stays inside the current item and ordered
        # numbering keeps running instead of restarting at 1.
        lines.append("")
        for ln in block.split("\n"):
            lines.append(pad + "   " + ln if ln.strip() else "")
        lines.append("")

    for ch in list(node.children):
        if isinstance(ch, NavigableString):
            continue
        if ch.name == "li":
            i += 1
            nested = []
            for sub in ch.find_all(["ul", "ol"], recursive=False):
                nested.append(list_md(sub, ctx, indent + 1))
                sub.extract()
            codes = pop_code(ch, ctx)
            body = inline(ch, ctx).strip()
            marker = f"{i}." if ordered else "-"
            lines.append(f"{pad}{marker} {body}".rstrip())
            for c in codes:
                attach(c)
            lines.extend(nested)
        else:
            # a listing sitting between items: attach to the preceding one
            for c in pop_code(ch, ctx):
                attach(c)
    return "\n".join(lines)


def table_md(node, ctx):
    rows = []
    for tr in node.find_all("tr"):
        cells = [inline(td, ctx).strip().replace("\n", " ") or " " for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [" "] * (width - len(r)) for r in rows]
    head, *body = rows
    out = ["| " + " | ".join(head) + " |", "|" + "|".join([" --- "] * width) + "|"]
    for r in body:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


CONTINUES = (":", "\\", "(", ",", "[", "{", "+", "=")


def rejoin_split_listings(merged):
    """Heal one listing that the author split across two <pre>/code boxes.

    Some posts break a single program mid-statement, e.g. a <pre> ending
    `for note in notes:` followed by a second <pre> holding the loop body. Only
    rejoin when the first half is visibly unfinished or the second half starts
    indented -- otherwise two adjacent listings are two listings.
    """
    out = []
    i = 0
    while i < len(merged):
        cur = merged[i]
        if (
            cur[0] == "gap"
            and out
            and out[-1][0] == "code"
            and i + 1 < len(merged)
            and merged[i + 1][0] == "code"
        ):
            prev_lines = [l for l in out[-1][1].split("\n") if l.strip()]
            next_lines = [l for l in merged[i + 1][1].split("\n") if l.strip()]
            if prev_lines and next_lines and (
                prev_lines[-1].rstrip().endswith(CONTINUES)
                or re.match(r"^[ \t\xa0]+\S", next_lines[0])
            ):
                out[-1][1] += "\n" + merged[i + 1][1]
                i += 2
                continue
        out.append(cur)
        i += 1
    return out


def render(tokens, ctx):
    """Merge adjacent code tokens, then join blocks with blank lines.

    Line breaks inside a code run come from <br> ONLY, never from token
    adjacency. Blogger's editor routinely splits a single line across two mono
    spans mid-word (`self.openJunctio` + `n()`), so adjacent code tokens with no
    <br> between them are one line and must concatenate directly.
    """
    merged = []
    for kind, text in tokens:
        if kind == "code":
            if merged and merged[-1][0] == "code":
                merged[-1][1] += text
            else:
                merged.append(["code", text])
        elif kind == "boundary":
            # a styled code box / <pre> edge: candidate split point
            if merged and merged[-1][0] == "code":
                merged.append(["gap", ""])
        elif kind == "nl":
            # soft line end: a block mono element closed. Don't double up if the
            # run already ends in a newline.
            if merged and merged[-1][0] == "code" and not merged[-1][1].endswith("\n"):
                merged[-1][1] += "\n"
        elif kind == "br":
            if merged and merged[-1][0] == "code":
                merged[-1][1] += "\n"
            elif merged and merged[-1][0] in ("md", "para"):
                merged[-1][1] += "  \n"
        else:
            if text.strip():
                merged.append([kind, text])

    merged = rejoin_split_listings(merged)

    parts = []
    for kind, text in merged:
        if kind == "gap":
            continue
        if kind == "code":
            parts.append(fence(text, ctx))
        else:
            parts.append(text.strip())
    return "\n\n".join(p for p in parts if p.strip())


def _sig_tokens(code):
    """Token stream with whitespace normalised away, but nesting preserved.

    INDENT/DEDENT are kept as bare markers so a rewrite that changed the block
    structure cannot pass as equivalent.
    """
    out = []
    for t in tokenize.generate_tokens(io.StringIO(code + "\n").readline):
        if t.type in (tokenize.INDENT, tokenize.DEDENT):
            out.append((tokenize.tok_name[t.type], ""))
        elif t.type == tokenize.NEWLINE:
            out.append(("NEWLINE", ""))
        elif t.type in (tokenize.NL, tokenize.ENDMARKER):
            continue
        else:
            out.append((tokenize.tok_name[t.type], t.string))
    return out


def reindent_python(code, width=4):
    """Re-indent a Python listing to `width` spaces per nesting level.

    Six posts indent 1-2 spaces per level, and mix Apple-tab-span (one literal
    space) with &nbsp; runs inside the same listing, so observed widths run
    [1, 2, 3, 4, 5, 8]. Scaling the leading whitespace by a factor, or ranking
    the distinct widths, both get this wrong -- different widths do not map
    monotonically onto depth once the styles are mixed.

    So let Python decide: tokenize maintains the real indent stack and emits
    INDENT/DEDENT, which gives the true depth of every logical line. This also
    works on the Python 2 listings, because tokenize does not check grammar.

    Returns the input unchanged unless the result is provably equivalent.
    """
    if "\n" not in code.strip():
        return code
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(code + "\n").readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return code

    depth = 0
    logical = {}   # physical line -> depth, for lines starting a statement
    comments = {}  # physical line -> depth where the comment was seen
    protected = set()  # lines inside a multi-line string: never touch
    fresh = True
    for t in toks:
        if t.type == tokenize.STRING and t.end[0] > t.start[0]:
            # Continuation lines of a triple-quoted string are string content.
            # Blanking or re-indenting them rewrites the literal.
            protected.update(range(t.start[0] + 1, t.end[0] + 1))
        if t.type == tokenize.INDENT:
            depth += 1
        elif t.type == tokenize.DEDENT:
            depth = max(0, depth - 1)
        elif t.type == tokenize.NEWLINE:
            fresh = True
        elif t.type == tokenize.NL:
            pass
        elif t.type == tokenize.COMMENT:
            if fresh and t.line.lstrip().startswith("#"):
                comments[t.start[0]] = depth
        elif t.type != tokenize.ENDMARKER:
            if fresh:
                logical[t.start[0]] = depth
                fresh = False

    if not logical:
        return code

    starts = sorted(logical)
    out = []
    for i, raw in enumerate(code.split("\n"), start=1):
        if i in protected:
            out.append(raw)
            continue
        if not raw.strip():
            out.append("")
            continue
        if i in logical:
            d = logical[i]
        elif i in comments:
            # A comment above an indented block is tokenised before the INDENT,
            # so it carries the outer depth. Attach it to the statement below.
            nxt = next((logical[s] for s in starts if s > i), None)
            d = nxt if nxt is not None else comments[i]
        else:
            # continuation line inside brackets or after a backslash: leave it
            out.append(raw.rstrip())
            continue
        out.append(" " * (width * d) + raw.strip())
    new = "\n".join(out)

    # Guards: identical token stream, and identical AST when it parses at all.
    try:
        if _sig_tokens(code) != _sig_tokens(new):
            return code
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return code
    try:
        before = ast.dump(ast.parse(code))
    except SyntaxError:
        return new  # Python 2 listing: token equivalence is all we can check
    try:
        if ast.dump(ast.parse(new)) != before:
            return code
    except SyntaxError:
        return code
    return new


def fence(code, ctx):
    code = code.replace("\r\n", "\n").replace("\r", "\n")
    code = code.replace(" ", " ")
    # Apple-tab-span markers became real tabs; Python posts want spaces.
    code = code.expandtabs(4)
    code = "\n".join(ln.rstrip() for ln in code.split("\n"))
    code = code.strip("\n")
    if not code.strip():
        return ""
    lang = guess_lang(code, ctx["labels"])
    if lang == "python":
        fixed = reindent_python(code)
        if fixed != code:
            ctx["reindented"] = ctx.get("reindented", 0) + 1
            code = fixed
    ctx["langs"][lang] += 1
    ctx["code_blocks"] += 1
    ticks = "```"
    while ticks in code:
        ticks += "`"
    return f"{ticks}{lang}\n{code}\n{ticks}"


# ---------------------------------------------------------------- entry -> file


TAB_SPAN_RE = re.compile(
    r'<span[^>]*class="[^"]*Apple-tab-span[^"]*"[^>]*>([\s ]*)</span>', re.I
)


def body_markdown(html_str, ctx):
    # Apple-tab-span holds indentation as literal whitespace under
    # white-space:pre, so emit its content verbatim -- that is exactly what the
    # browser rendered. (Do not expand each character to a tab stop: several
    # posts indent some lines with &nbsp; runs and others with tab-spans, and
    # scaling only one of them shears the two apart.) A literal tab inside the
    # span survives and is expanded once, at the end, in fence().
    #
    # This has to run on the raw string, before BeautifulSoup: bs4 collapses any
    # text node that is entirely whitespace to a single space, silently turning
    # a two-level indent into a one-level one and producing invalid Python.
    # (Whitespace inside <pre> lives in mixed text nodes and is unaffected.)
    html_str = TAB_SPAN_RE.sub(lambda m: m.group(1) or " ", html_str)

    soup = BeautifulSoup(html_str, "html.parser")

    # Blogger wraps YouTube in <object><param name="movie" value="..."><embed>.
    # Lift the movie URL onto the object before discarding the params, or the
    # video ID is lost and the embed converts to an empty TODO comment.
    for obj in soup.find_all("object"):
        if obj.get("data"):
            continue
        for p in obj.find_all("param"):
            if (p.get("name") or "").lower() in ("movie", "src", "url") and p.get("value"):
                obj["data"] = p["value"]
                break
    for p in soup.find_all("param"):
        p.decompose()

    levels = [int(h.name[1]) for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    ctx["h_offset"] = 2 - min(levels) if levels else 1

    md = render(blocks(soup, ctx), ctx)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    return md.strip() + "\n"


def yaml_str(s):
    return "'" + s.replace("'", "''") + "'"


def build(entry, ctx_totals):
    title = (entry.findtext(A + "title") or "").strip()
    content = entry.findtext(A + "content") or ""
    published = entry.findtext(A + "published") or entry.findtext(B + "created")
    filename = (entry.findtext(B + "filename") or "").strip()

    dt = datetime.strptime(published[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    local = dt.astimezone(LONDON)

    terms = [c.get("term") for c in entry.findall(A + "category") if c.get("term")]
    slugs = sorted({slug_label(t) for t in terms})

    if filename:
        slug = re.sub(r"\.html?$", "", filename.rsplit("/", 1)[-1])
    else:
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]

    ctx = {
        "labels": slugs,
        "langs": ctx_totals["langs"],
        "images": [],
        "youtube": [],
        "other_embeds": [],
        "dropped_ads": 0,
        "code_blocks": 0,
    }
    body = body_markdown(content, ctx)

    fm = ["---"]
    fm.append(f"title: {yaml_str(title)}")
    fm.append(f"date: {local.strftime('%Y-%m-%d %H:%M:%S %z')[:-2]}:{local.strftime('%z')[-2:]}")
    if slugs:
        fm.append("tags: [" + ", ".join(slugs) + "]")
    if filename:
        fm.append("redirect_from:")
        fm.append(f"  - {filename}")
    fm.append("---")

    return {
        "slug": slug,
        "date": local,
        "title": title,
        "front_matter": "\n".join(fm),
        "body": body,
        "ctx": ctx,
        "orig": filename,
        "tags": slugs,
    }


def main():
    if not os.path.exists(SRC):
        sys.exit(f"missing {SRC}")

    root = ET.parse(SRC).getroot()
    entries = root.findall(A + "entry")

    posts_dir = os.path.join(ROOT, "_posts")
    drafts_dir = os.path.join(ROOT, "_drafts")
    pages_dir = os.path.join(ROOT, "_pages")
    for d in (posts_dir, drafts_dir, pages_dir):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)

    totals = {"langs": Counter()}
    written = {"post": 0, "draft": 0, "page": 0}
    all_images, all_yt, all_other, ads = [], [], [], 0
    manifest = []
    tag_counts = Counter()
    seen_slugs = Counter()

    for e in entries:
        etype = e.findtext(B + "type")
        status = e.findtext(B + "status")
        if etype == "COMMENT":
            continue
        if etype not in ("POST", "PAGE"):
            continue

        rec = build(e, totals)

        # Posts live at /posts/:slug/ and pages at /:name/, so the two never
        # collide -- dedupe within each namespace, not across both, or a page
        # gets a spurious "-2" because some post shares its name.
        space = "page" if etype == "PAGE" else "post"
        key = (space, rec["slug"])
        seen_slugs[key] += 1
        if seen_slugs[key] > 1:
            rec["slug"] = f"{rec['slug']}-{seen_slugs[key]}"

        if etype == "PAGE":
            path = os.path.join(pages_dir, rec["slug"] + ".md")
            written["page"] += 1
        elif status == "DRAFT":
            path = os.path.join(drafts_dir, rec["slug"] + ".md")
            written["draft"] += 1
        else:
            path = os.path.join(posts_dir, f"{rec['date']:%Y-%m-%d}-{rec['slug']}.md")
            written["post"] += 1
            for t in rec["tags"]:
                tag_counts[t] += 1

        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(rec["front_matter"] + "\n\n" + rec["body"])

        all_images += rec["ctx"]["images"]
        all_yt += rec["ctx"]["youtube"]
        all_other += rec["ctx"]["other_embeds"]
        ads += rec["ctx"]["dropped_ads"]
        manifest.append(
            {
                "path": os.path.relpath(path, ROOT).replace("\\", "/"),
                "title": rec["title"],
                "orig": rec["orig"],
                "code": rec["ctx"]["code_blocks"],
                "imgs": len(rec["ctx"]["images"]),
            }
        )

    # _data/tags.yml — slug -> display name, for the sidebar
    data_dir = os.path.join(ROOT, "_data")
    os.makedirs(data_dir, exist_ok=True)
    # A sequence, not a mapping: Liquid can sort a list of hashes but cannot
    # order a mapping by a nested value, and the sidebar wants count-descending.
    with open(os.path.join(data_dir, "tags.yml"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# Label slug, display name and post count, most used first.\n")
        f.write("# Generated by _import/convert.py -- do not edit by hand.\n")
        for term, (s, disp) in sorted(
            LABELS.items(), key=lambda kv: (-tag_counts[kv[1][0]], kv[1][0])
        ):
            if not tag_counts[s]:
                continue
            f.write(f"- slug: {s}\n  name: {yaml_str(disp)}\n  count: {tag_counts[s]}\n")

    print(f"posts  {written['post']}")
    print(f"drafts {written['draft']}")
    print(f"pages  {written['page']}")
    print(f"code blocks {sum(totals['langs'].values())}  ->  {dict(totals['langs'])}")
    print(f"remote images {len(all_images)} ({len(set(all_images))} unique)")
    print(f"youtube {len(all_yt)}  other embeds {len(all_other)}  ad blocks dropped {ads}")

    if "--report" in sys.argv:
        rep = os.path.join(ROOT, "_import", "report")
        os.makedirs(rep, exist_ok=True)
        with open(os.path.join(rep, "images.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(set(all_images))))
        with open(os.path.join(rep, "embeds.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(set(all_other))))
        with open(os.path.join(rep, "manifest.tsv"), "w", encoding="utf-8") as f:
            f.write("path\tcode\timgs\torig\ttitle\n")
            for m in sorted(manifest, key=lambda m: m["path"]):
                f.write(f"{m['path']}\t{m['code']}\t{m['imgs']}\t{m['orig']}\t{m['title']}\n")
        print(f"wrote report to _import/report/")


if __name__ == "__main__":
    main()
