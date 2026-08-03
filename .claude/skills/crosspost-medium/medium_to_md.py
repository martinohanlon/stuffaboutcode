#!/usr/bin/env python3
"""
Convert a Medium post into a stuffaboutcode.com draft.

Reads Medium's own structured payload -- `https://medium.com/p/<id>?format=json`
-- NOT the article HTML. The rendered page is built client-side: every <img>
arrives with an empty src and code blocks have no <pre> at all, so scraping it
loses the images and the code. The JSON carries the real thing, including each
code block's language and the character offsets of every inline-code span.

Writes a draft to _drafts/, downloads the images to assets/img/YYYY/MM/, and
prints a review list of the decisions it could not make on its own -- unlabelled
code fences, missing alt text, embeds it could not resolve, new tags.

Nothing here is authoritative about wording. It gets the mechanical conversion
right so the writing is the only thing left to do.

Usage:
  python .claude/skills/crosspost-medium/medium_to_md.py <medium-url> \
      --canonical <original-url> [--tags a,b] [--credit-name 'Name'] [--force]

  --canonical    the URL search engines should credit. Often NOT the Medium one
                 -- a post can go Medium + your own site from a third original.
                 Defaults to Medium's own canonicalUrl.
  --tags         override the tags; comma separated. Default: Medium's tags,
                 slugified (usually 5 of them, and usually needs pruning).
  --credit-name  label for the closing credit link. Default: from the host.
  --no-credit    omit the closing credit line.
  --dry-run      print the markdown, write nothing, download nothing.
  --force        overwrite an existing draft and re-download existing images.
"""

import argparse
import html
import json
import os
import re
import sys
import unicodedata
import urllib.parse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

try:
    import requests
except ImportError:
    sys.exit("needs requests:  pip install requests tzdata")

# Windows consoles default to cp1252, which cannot print an em dash or a smart
# quote -- and Medium prose is full of both. Without this, --dry-run output is
# unreadable and looks like a conversion fault.
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# .../<repo>/.claude/skills/crosspost-medium/medium_to_md.py -> <repo>
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TZ = ZoneInfo("Europe/London")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Medium's paragraph type enum. Anything not listed is passed through as prose
# with a warning rather than silently dropped.
P, H2, H3, IMG, BQ, PQ, PRE, ULI, OLI, IFRAME, H4, MIXTAPE = 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 13, 14
HEADINGS = (H2, H3, H4)

# Medium's inline markup enum.
MK_STRONG, MK_EM, MK_A, MK_CODE = 1, 2, 3, 10

# Credit-line labels that a hostname cannot be cased into automatically.
SITE_NAMES = {
    "medium.com": "Medium",
    "graphacademy.neo4j.com": "Neo4j GraphAcademy",
    "neo4j.com": "Neo4j",
    "dev.to": "DEV",
    "github.com": "GitHub",
}

REVIEW = []  # things a human has to decide, printed at the end


def review(msg):
    if msg not in REVIEW:  # the same rule can fire on many paragraphs
        REVIEW.append(msg)


# ---------------------------------------------------------------- fetch


def post_id(url):
    """Medium's post id -- the hex suffix on the slug, or /p/<id>."""
    clean = url.split("?")[0].rstrip("/")
    m = re.search(r"/p/([0-9a-f]{6,})$", clean) or re.search(r"-([0-9a-f]{8,})$", clean)
    return m.group(1) if m else None


def fetch_payload(url):
    pid = post_id(url)
    target = f"https://medium.com/p/{pid}?format=json" if pid else f"{url.split('?')[0]}?format=json"
    r = requests.get(target, timeout=60, headers=UA)
    if r.status_code != 200:
        sys.exit(f"Medium returned HTTP {r.status_code} for {target}")
    body = r.text
    if "</x>" in body[:40]:  # ])}while(1);</x> anti-JSON-hijack prefix
        body = body.split("</x>", 1)[1]
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        sys.exit(f"{target} did not return Medium's JSON payload -- is the URL a Medium post?")
    if not data.get("success"):
        sys.exit(f"Medium reported failure for {target}")
    return data["payload"]["value"]


# ---------------------------------------------------------------- text


# Invisible characters Medium's editor sprinkles through its prose, by ordinal so
# that no literal zero-width character can sit in this source and get mangled by
# an editor. Every one maps to a single space: the offsets in the markup data
# index this string, so the substitution has to be length-preserving.
#   00A0 no-break space   -- verify.py flags it
#   200B zero-width space
#   2028/2029 line/paragraph separator -- a raw one breaks the YAML front matter
#   202F/2009 narrow and thin space
INVISIBLE = {0x00A0: " ", 0x200B: " ", 0x2028: " ", 0x2029: " ", 0x202F: " ", 0x2009: " "}
# Removed rather than replaced, after the offsets stop mattering.
ZERO_WIDTH = {0x200C: "", 0x200D: "", 0xFEFF: ""}


def clean(text):
    """Length-preserving cleanup only -- the markup offsets index this string."""
    out = text.translate(INVISIBLE)
    # A substitution that changed the length once shifted every bold, link and
    # code span after it, and the output still looked plausible enough to pass a
    # byte-level check. Cheap to assert, expensive to miss.
    assert len(out) == len(text), "clean() must not change the length of the text"
    return out


def u16_map(text):
    """UTF-16 offset -> Python index.

    Medium's start/end offsets are JavaScript string indices, so an emoji counts
    as two. Indexing the Python string directly shifts every span after one.
    """
    out, u = {}, 0
    for i, ch in enumerate(text):
        out[u] = i
        u += 2 if ord(ch) > 0xFFFF else 1
    out[u] = len(text)
    return out


TAG_IN_PROSE = re.compile(r"</?[A-Za-z][\w-]*(?:\s[^<>]*?)?/?>")
# chr(2) rather than an escape or a literal: no editor or formatter rewrites it.
HOLD = chr(2) + "%d" + chr(2)


def escape(s):
    """Escape what would otherwise change meaning as Markdown.

    Deliberately light. GFM does not treat intra-word * or _ as emphasis, so
    snake_case survives unescaped; escaping it would litter the prose with
    backslashes for no gain. Nothing is ever escaped as an HTML entity, because
    verify.py flags a literal &lt; in prose -- the fix for one of this repo's
    checks must not trip another.
    """
    # A whole HTML tag in prose becomes inline code. Backslash-escaping it to
    # `\<div>` renders correctly, but the text still contains "<div" and
    # verify.py reads that as leftover HTML, while it strips inline code before
    # it looks. Lifted out first so the escaping below cannot reach inside it.
    held = []

    def take(m):
        review(f"HTML tag in prose wrapped in backticks so it renders: {m.group(0)[:50]}")
        held.append(m.group(0))
        return HOLD % (len(held) - 1)

    s = TAG_IN_PROSE.sub(take, s)

    s = s.replace("\\", "\\\\")
    s = s.replace("`", "\\`")
    # A stray "<" that never formed a whole tag still needs escaping.
    s = re.sub(r"<(?=[A-Za-z/!])", r"\\<", s)
    s = re.sub(r"&(?=\w+;|#\d+;)", r"\\&", s)
    s = s.replace("[", "\\[").replace("]", "\\]")
    # emphasis only fires when the marker flanks a word, so escape only there
    s = re.sub(r"(?<![\w*])\*(?=\S)", r"\\*", s)
    s = re.sub(r"(?<![\w_])_(?=\S)", r"\\_", s)

    for n, tag in enumerate(held):
        s = s.replace(HOLD % n, f"`{tag}`")
    return s


def escape_leading(s):
    """Stop the first characters of a paragraph reading as a block marker."""
    return re.sub(r"^(\s*)([#>+\-]|\d+\.)(\s)", r"\1\\\2\3", s)


def render_inline(text, markups):
    """Apply Medium's markups to a paragraph, honouring nesting.

    Sorted outermost-first and clamped to the parent, so a link containing bold
    or code comes out nested rather than interleaved. Text inside a CODE span is
    never escaped -- backticks handle it.
    """
    text = clean(text)
    if not markups:
        return escape(text)

    m16 = u16_map(text)

    def idx(u, default):
        if u in m16:
            return m16[u]
        return default

    spans = []
    for mk in markups:
        s = idx(mk.get("start", 0), 0)
        e = idx(mk.get("end", 0), len(text))
        if e <= s:
            continue
        spans.append((s, e, mk))
    spans.sort(key=lambda t: (t[0], -t[1]))

    def wrap(mk, inner):
        t = mk.get("type")
        if t == MK_CODE:
            return f"`{inner}`"
        if t == MK_STRONG:
            return f"**{inner}**"
        if t == MK_EM:
            return f"*{inner}*"
        if t == MK_A:
            href = mk.get("href")
            if not href and mk.get("userId"):
                href = f"https://medium.com/u/{mk['userId']}"
            if not href:
                review(f"link with no target, left as plain text: {inner[:60]!r}")
                return inner
            href = href.split("?source=")[0]
            return f"[{inner}]({href})"
        review(f"unknown inline markup type {t}, left as plain text")
        return inner

    def build(lo, hi, pool, in_code):
        """Render text[lo:hi] with the spans in pool applied."""
        out, cur = [], lo
        i = 0
        while i < len(pool):
            s, e, mk = pool[i]
            if s >= hi:
                break
            s, e = max(s, lo), min(e, hi)
            if s > cur:
                out.append(text[cur:s] if in_code else escape(text[cur:s]))
            # everything starting before this span ends is nested inside it
            child = []
            j = i + 1
            while j < len(pool) and pool[j][0] < e:
                if pool[j][1] > e:
                    review(
                        "overlapping bold/italic/link/code spans on Medium were nested "
                        f"to fit -- check the formatting around {text[s:e][:40]!r}"
                    )
                child.append(pool[j])
                j += 1
            code = in_code or mk.get("type") == MK_CODE
            out.append(wrap(mk, build(s, e, child, code)))
            cur, i = e, j
        if cur < hi:
            out.append(text[cur:hi] if in_code else escape(text[cur:hi]))
        return "".join(out)

    return build(0, len(text), spans, False)


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


# ---------------------------------------------------------------- code fences

# A prompt or a chat transcript is not a language, and it is what Medium's own
# detector goes most wrong on -- "Create a function which..." came back as
# javascript. Checked before anything else so prose in a code block stays text.
TRANSCRIPT = re.compile(
    r"(?im)^\s*(\[/?(human|ai|user|assistant|system|you|me)\]|(human|ai|user|assistant|system)\s*:)"
)

# Ordered: first match wins. Anchored at line starts, because a keyword loose in
# an English sentence inside a code block is not evidence of a language.
GUESSES = [
    # SQL before Cypher: both use an uppercase WITH, but only SQL has SELECT ...
    # FROM, so testing for it first stops a CTE being called Cypher.
    ("sql", r"(?im)^\s*(SELECT\b[\s\S]*\bFROM\b|INSERT INTO|CREATE TABLE|ALTER TABLE)"),
    # Case-SENSITIVE, deliberately. Cypher is written in uppercase and Python is
    # not: `(?i)RETURN` matched `    return x` and labelled Python as Cypher.
    ("cypher", r"(?m)^\s*(MATCH|OPTIONAL MATCH|MERGE|UNWIND|RETURN|WITH|LOAD CSV)\b|\)-\[|\]->|\)<-\["),
    ("python", r"(?m)^\s*(def \w+\s*\(|class \w+[\s(:]|import \w|from [\w.]+ import|print\()"),
    ("bash", r"(?m)^\s*(\$ |# ?sudo |sudo |pip install|apt(-get)? |cd |export \w+=|curl |git |npm |docker )"),
    ("html", r"(?is)<(!doctype|html|div|span|script|body|head)\b"),
    ("csharp", r"(?m)^\s*(using System|namespace \w|public (class|record|async|static)|Console\.Write)"),
    ("java", r"(?m)^\s*(package \w|public class \w+\s*\{|System\.out\.print)"),
    ("javascript", r"(?m)^\s*(const \w+\s*=|let \w+\s*=|function \w*\s*\(|import .* from |console\.log)"),
    ("css", r"(?m)^\s*[.#]?[\w-]+\s*\{\s*$"),
    ("yaml", r"(?m)^[a-z][\w-]*:(\s|$)"),
]


def guess_lang(code):
    """(language, confident). Confident means the content itself said so."""
    stripped = code.strip()
    if TRANSCRIPT.search(code):
        return "text", True
    if stripped[:1] in "{[":
        try:
            json.loads(stripped)
            return "json", True
        except ValueError:
            pass
    for lang, pat in GUESSES:
        if re.search(pat, code):
            return lang, True
    return "text", False


def pick_lang(code, medium_lang):
    """Choose a fence language, preferring the content over Medium's label.

    Medium's codeBlockMetadata.lang comes from its own detector, and it is wrong
    often enough to matter: it labels Cypher as sql, scss or php. Every code
    block on this site carries a language that drives both the Rouge highlighting
    and the label in the block's header bar, so a wrong one is visible.

    Returns (lang, note) -- note is non-None when a human should confirm.
    """
    guess, confident = guess_lang(code)
    if confident:
        if medium_lang and medium_lang.lower() != guess:
            return guess, f"Medium labelled it `{medium_lang}`; the content says `{guess}`"
        if not medium_lang:
            return guess, f"no language on Medium, read as `{guess}` from the content"
        return guess, None  # Medium and the content agree
    if medium_lang:
        return medium_lang.lower(), f"using Medium's own label `{medium_lang}`, unverified"
    return "text", "no language on Medium and nothing identifiable -- fell back to `text`"


def fence(code, lang):
    """Fence a block, widening the delimiter if the code contains backticks."""
    ticks = "`" * max(3, max((len(m) for m in re.findall(r"`+", code)), default=0) + 1)
    return f"{ticks}{lang}\n{code.rstrip()}\n{ticks}"


# ---------------------------------------------------------------- media


def image_url(iid, original_width):
    """Medium serves any width; ask for 1600 unless the original is smaller."""
    width = min(1600, original_width) if original_width else 1600
    return f"https://miro.medium.com/v2/resize:fit:{width}/{iid}"


EXT_BY_TYPE = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp"}


def download_image(iid, original_width, dest_dir, stem, dry_run, force):
    m = re.search(r"\.(png|jpe?g|gif|webp)$", iid, re.I)
    ext = ("." + m.group(1).lower().replace("jpeg", "jpg")) if m else None
    url = image_url(iid, original_width)

    if dry_run:
        return f"{stem}{ext or '.png'}"

    os.makedirs(dest_dir, exist_ok=True)
    if ext:
        path = os.path.join(dest_dir, stem + ext)
        if os.path.exists(path) and not force:
            return stem + ext
    r = requests.get(url, timeout=90, headers=UA)
    if r.status_code != 200:
        review(f"image failed to download (HTTP {r.status_code}): {url}")
        return None
    if not ext:  # ids like 0*XJCKj2675Cc_B0Y9 carry no extension
        ext = EXT_BY_TYPE.get(r.headers.get("content-type", "").split(";")[0], ".png")
    name = stem + ext
    path = os.path.join(dest_dir, name)
    if os.path.exists(path) and not force:
        return name
    with open(path, "wb") as f:
        f.write(r.content)
    return name


YT = re.compile(r"(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=)|youtu\.be/)([A-Za-z0-9_-]{11})")


def resolve_embed(media_id):
    """Medium keeps embeds behind /media/<id>; resolve to something self-hosted.

    Returns (markdown, kind). YouTube becomes the site's own include; anything
    else is reported rather than guessed at.
    """
    try:
        r = requests.get(f"https://medium.com/media/{media_id}", timeout=60, headers=UA)
    except requests.RequestException as e:
        review(f"embed {media_id} could not be fetched ({e}) -- left as a TODO")
        return f"<!-- TODO embed: https://medium.com/media/{media_id} -->", "unresolved"
    if r.status_code != 200:
        review(f"embed {media_id} returned HTTP {r.status_code} -- left as a TODO")
        return f"<!-- TODO embed: https://medium.com/media/{media_id} -->", "unresolved"

    page = html.unescape(r.text)
    inner = urllib.parse.unquote(page)

    m = YT.search(inner)
    if m:
        return '{%% include youtube.html id="%s" %%}' % m.group(1), "youtube"

    if "gist.github.com" in inner:
        g = re.search(r"https://gist\.github\.com/[\w./-]+", inner)
        url = g.group(0).removesuffix(".js") if g else f"https://medium.com/media/{media_id}"
        review(
            f"GitHub gist embed: {url}\n"
            "      No JS embeds on this site -- paste the gist's code into a fenced block."
        )
        return f"<!-- TODO embed: {url} -->", "gist"

    src = re.search(r'src="(https?://[^"]+)"', page)
    if src:
        real = urllib.parse.parse_qs(urllib.parse.urlparse(html.unescape(src.group(1))).query).get("url")
        target = real[0] if real else html.unescape(src.group(1))
        review(
            f"embed points at {target}\n"
            "      Check it works in an iframe, then use {% include embed.html src=\"...\" title=\"...\" %}."
        )
        return f"<!-- TODO embed: {target} -->", "unresolved"

    review(f"embed {media_id} could not be identified -- left as a TODO")
    return f"<!-- TODO embed: https://medium.com/media/{media_id} -->", "unresolved"


# ---------------------------------------------------------------- tags


def site_tags():
    path = os.path.join(ROOT, "_data", "tags.yml")
    if not os.path.exists(path):
        return set()
    return set(re.findall(r"^-\s*slug:\s*(\S+)", open(path, encoding="utf-8").read(), re.M))


# ---------------------------------------------------------------- convert


def convert(value, args):
    paragraphs = value["content"]["bodyModel"]["paragraphs"]
    title = clean(value.get("title") or "")
    slug = re.sub(r"-[0-9a-f]{8,}$", "", value.get("uniqueSlug") or slugify(title))

    published = datetime.fromtimestamp(
        (value.get("firstPublishedAt") or value.get("latestPublishedAt")) / 1000, tz=timezone.utc
    ).astimezone(TZ)

    img_dir = os.path.join(ROOT, "assets", "img", published.strftime("%Y"), published.strftime("%m"))
    img_web = f"/assets/img/{published.strftime('%Y/%m')}"

    # Map Medium's heading levels onto the site's, which start at ##. Whichever
    # levels the post actually uses are collapsed downward, so a post using only
    # "small title" still opens at ## rather than ####.
    used = sorted({p["type"] for p in paragraphs if p.get("type") in HEADINGS})
    level = {t: "#" * min(2 + i, 4) for i, t in enumerate(used)}

    out, stats = [], {"images": 0, "fences": [], "youtube": 0, "todo": 0}
    n_img, ol = 0, 0
    i = 0
    while i < len(paragraphs):
        p = paragraphs[i]
        t, text, markups = p.get("type"), p.get("text") or "", p.get("markups") or []

        # Medium repeats the title as the first body paragraph.
        if i == 0 and t in HEADINGS and clean(text).strip() == title.strip():
            i += 1
            continue

        if t in HEADINGS:
            out.append(f"{level[t]} {render_inline(text, markups)}")
            ol = 0

        elif t == P:
            out.append(escape_leading(render_inline(text, markups)))
            ol = 0

        elif t == PRE:
            # Consecutive PRE paragraphs are one logical listing -- Medium makes
            # a new paragraph per block, and pasted code often lands as several.
            block, lang = [], (p.get("codeBlockMetadata") or {}).get("lang")
            while i < len(paragraphs) and paragraphs[i].get("type") == PRE:
                q = paragraphs[i]
                if (q.get("codeBlockMetadata") or {}).get("lang") not in (lang, None):
                    break
                lang = lang or (q.get("codeBlockMetadata") or {}).get("lang")
                block.append(clean(q.get("text") or ""))
                i += 1
            i -= 1
            code = "\n".join(block)
            lang, note = pick_lang(code, lang)
            first = code.strip().split("\n")[0][:60]
            stats["fences"].append({"lang": lang, "first": first, "note": note})
            if note:
                review(f"fence #{len(stats['fences'])}: {note}\n      starts: {first!r}")
            out.append(fence(code, lang))
            ol = 0

        elif t == IMG:
            meta = p.get("metadata") or {}
            iid = meta.get("id")
            if not iid:
                review("image paragraph with no id -- skipped")
                i += 1
                continue
            n_img += 1
            name = download_image(
                iid, meta.get("originalWidth"), img_dir, f"{slug}-{n_img}", args.dry_run, args.force
            )
            if name:
                stats["images"] += 1
                caption = render_inline(text, markups).strip() if text.strip() else ""
                if not caption:
                    review(f"image {name} has no alt text -- describe it in the brackets")
                out.append(f"![{caption}]({img_web}/{name})")
            ol = 0

        elif t in (BQ, PQ):
            body = render_inline(text, markups)
            out.append("\n".join("> " + ln for ln in body.split("\n")))
            ol = 0

        elif t == ULI:
            items = []
            while i < len(paragraphs) and paragraphs[i].get("type") == ULI:
                q = paragraphs[i]
                items.append("- " + render_inline(q.get("text") or "", q.get("markups") or []))
                i += 1
            i -= 1
            out.append("\n".join(items))
            ol = 0

        elif t == OLI:
            items = []
            while i < len(paragraphs) and paragraphs[i].get("type") == OLI:
                q = paragraphs[i]
                ol += 1
                items.append(f"{ol}. " + render_inline(q.get("text") or "", q.get("markups") or []))
                i += 1
            i -= 1
            out.append("\n".join(items))

        elif t == IFRAME:
            mid = (p.get("iframe") or {}).get("mediaResourceId")
            if not mid:
                review("embed with no media id -- skipped")
                i += 1
                continue
            md, kind = resolve_embed(mid)
            if kind == "youtube":
                stats["youtube"] += 1
            else:
                stats["todo"] += 1
            out.append(md)
            ol = 0

        elif t == MIXTAPE:
            # A Medium link card. Its text run is title + description + the bare
            # hostname concatenated, so rendering the markups gives a link label
            # three lines long. Take the title and description from their spans
            # instead and drop the hostname.
            href = (p.get("mixtapeMetadata") or {}).get("href", "")
            whole = clean(text)
            m16 = u16_map(whole)
            picked = {}
            for mk in markups:
                if mk.get("type") in (MK_STRONG, MK_EM):
                    s = m16.get(mk.get("start", 0), 0)
                    e = m16.get(mk.get("end", 0), len(whole))
                    picked[mk["type"]] = whole[s:e].strip()
            title_txt = picked.get(MK_STRONG) or whole.split("\n")[0].strip()
            desc = picked.get(MK_EM, "")
            link = f"[{escape(title_txt)}]({href.split('?')[0]})" if href else escape(title_txt)
            out.append(f"> **{link}**" + (f" — {escape(desc)}" if desc else ""))
            review(
                "Medium link card became a blockquote link"
                + (f" -> {href.split('?')[0]}" if href else "")
                + "\n      Reword it as a sentence in your own voice, or drop it."
            )
            ol = 0

        else:
            review(f"unhandled Medium paragraph type {t}, kept as prose: {clean(text)[:60]!r}")
            out.append(escape_leading(render_inline(text, markups)))
            ol = 0

        i += 1

    body = "\n\n".join(b for b in out if b.strip())
    # Medium's editor leaves a space between a closing inline-code span and the
    # punctuation after it ("a `VectorRetriever` ."). Its own CSS hides that; a
    # markdown renderer does not.
    body = re.sub(r"` +(?=[.,;:!?)])", "`", body)
    # Zero-width and other invisible leftovers, now that offsets no longer matter.
    body = body.translate(ZERO_WIDTH)
    return title, slug, published, body, stats


def credit_line(canonical, published, name):
    host = urllib.parse.urlparse(canonical).netloc.lower().removeprefix("www.")
    label = name or SITE_NAMES.get(host, host)
    day = f"{published.day} {published:%B %Y}"
    return f"---\n\n*Originally published on [{label}]({canonical}) on {day}.*"


def front_matter(title, published, tags, canonical):
    offset = published.strftime("%z")
    stamp = f"{published:%Y-%m-%d %H:%M:%S} {offset[:3]}:{offset[3:]}"
    return "\n".join(
        [
            "---",
            "title: '%s'" % title.replace("'", "''"),
            f"date: {stamp}",
            "tags: [%s]" % ", ".join(tags),
            f"canonical_url: {canonical}",
            "---",
        ]
    )


def self_test():
    """Offline checks on the conversion rules. No network, writes nothing.

    Every case here is a bug this script actually shipped once.
    """
    fails = []

    def eq(got, want, label):
        if got != want:
            fails.append(f"{label}\n      got:  {got!r}\n      want: {want!r}")

    # A length-changing clean() silently shifted every markup offset after it.
    # Escapes, never literal invisibles: a literal one here is what VS Code
    # warns about as an "unusual line terminator", and what an editor mangles.
    # Escapes, never literal invisibles: VS Code reports a literal U+2028 as
    # an "unusual line terminator", and editors silently mangle them.
    # Built with chr() so the source file itself holds no invisible character
    # and no \u escape: both get rewritten by editors and formatters.
    nbsp, zwsp = chr(0x00A0), chr(0x200B)
    eq(clean(f"a{nbsp}b{zwsp}c"), "a b c", "clean() maps invisibles to one space each")
    seps = chr(0x2028) + chr(0x2029)
    eq(len(clean(f"R{seps}G")), 4, "clean() preserves length")
    eq(clean("RAG"), "RAG", "clean() leaves ordinary text untouched")

    # Medium offsets are UTF-16, so an emoji ahead of a span counts as two.
    eq(
        render_inline("hi code x", [{"type": MK_CODE, "start": 3, "end": 7}]),
        "hi `code` x",
        "inline code span",
    )
    eq(
        render_inline("🚀 code x", [{"type": MK_CODE, "start": 3, "end": 7}]),
        "🚀 `code` x",
        "span after an emoji uses UTF-16 offsets",
    )
    eq(
        render_inline("see docs now", [{"type": MK_A, "start": 4, "end": 8, "href": "https://x.dev"}]),
        "see [docs](https://x.dev) now",
        "link span",
    )
    eq(
        render_inline(
            "read the docs here",
            [
                {"type": MK_A, "start": 5, "end": 18, "href": "https://x.dev"},
                {"type": MK_STRONG, "start": 9, "end": 13},
            ],
        ),
        "read [the **docs** here](https://x.dev)",
        "bold nested inside a link",
    )
    # Markdown inside a code span must survive verbatim.
    eq(
        render_inline("use *args now", [{"type": MK_CODE, "start": 4, "end": 9}]),
        "use `*args` now",
        "no escaping inside code",
    )
    eq(escape("a <div> & b"), "a `<div>` & b", "HTML tag in prose becomes inline code")
    eq(escape("a < b"), "a < b", "a lone less-than is left alone")
    eq(escape("if a <b then"), "if a \\<b then", "half a tag is backslash-escaped")
    eq(escape("use &amp; here"), "use \\&amp; here", "entity escaped so verify.py stays quiet")
    eq(escape("snake_case stays"), "snake_case stays", "intra-word underscore left alone")

    # Medium's own detector labels Cypher as sql/scss/php, and calls prompt
    # transcripts javascript. The content has to win.
    eq(pick_lang("MATCH (m:Movie) RETURN m", "sql")[0], "cypher", "Cypher beats Medium's sql")
    eq(pick_lang("[Human]\nCreate a function which connects", None)[0], "text", "transcript is text")
    eq(pick_lang("def f(x):\n    return x", None)[0], "python", "python from content")
    eq(pick_lang("no idea what this is", None)[0], "text", "unknown falls back to text")
    eq(pick_lang("SELECT a FROM b", None)[0], "sql", "sql from content")
    # An unlabelled block whose language we cannot read must still be flagged.
    if pick_lang("no idea what this is", None)[1] is None:
        fails.append("an unreadable fence language must be flagged for review")
    if pick_lang("MATCH (n) RETURN n", "cypher")[1] is not None:
        fails.append("agreement between Medium and the content needs no review note")

    # A fence must not be closable by backticks in the code itself.
    eq(fence("a ``` b", "text"), "````text\na ``` b\n````", "fence widens past inner backticks")

    for label, want in [("2026-07-22T00:00:30Z", "+01:00"), ("2026-01-15T12:00:00Z", "+00:00")]:
        d = datetime.fromisoformat(label.replace("Z", "+00:00")).astimezone(TZ)
        fm = front_matter("t", d, ["a"], "https://x.dev")
        if want not in fm:
            fails.append(f"BST/GMT offset for {label}: expected {want} in\n      {fm}")

    eq(
        front_matter("Martin's post", datetime(2026, 7, 22, tzinfo=TZ), ["a"], "https://x.dev").split("\n")[1],
        "title: 'Martin''s post'",
        "apostrophe doubled for YAML",
    )
    eq(post_id("https://medium.com/neo4j/some-slug-c969ae5f4230?source=rss"), "c969ae5f4230", "post id")
    eq(post_id("https://medium.com/p/c969ae5f4230"), "c969ae5f4230", "post id from /p/")

    if fails:
        print(f"self-test: {len(fails)} FAILED", file=sys.stderr)
        for f in fails:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("self-test: all checks passed", file=sys.stderr)
    return 0


def main():
    if "--self-test" in sys.argv:
        sys.exit(self_test())

    ap = argparse.ArgumentParser(description="Convert a Medium post to a stuffaboutcode draft.")
    ap.add_argument("url", help="the Medium post URL")
    ap.add_argument("--canonical", help="URL to credit as the original (default: Medium's own)")
    ap.add_argument("--tags", help="comma-separated tag slugs (default: Medium's, slugified)")
    ap.add_argument("--credit-name", help="label for the closing credit link")
    ap.add_argument("--no-credit", action="store_true", help="omit the closing credit line")
    ap.add_argument("--dry-run", action="store_true", help="print only; write and download nothing")
    ap.add_argument("--force", action="store_true", help="overwrite the draft and re-download images")
    args = ap.parse_args()

    value = fetch_payload(args.url)

    if value.get("isSubscriptionLocked") or value.get("isMarkedPaywallOnly"):
        review("Medium says this post is member-only. Check the body is complete, not a preview.")

    canonical = args.canonical or value.get("canonicalUrl") or value.get("mediumUrl") or args.url
    canonical = canonical.split("?")[0]

    title, slug, published, body, stats = convert(value, args)

    medium_tags = [slugify(t["slug"]) for t in (value.get("virtuals") or {}).get("tags", [])]
    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else medium_tags
    known = site_tags()
    new = [t for t in tags if t not in known]

    parts = [front_matter(title, published, tags, canonical), body]
    if not args.no_credit:
        parts.append(credit_line(canonical, published, args.credit_name))
    doc = "\n\n".join(parts) + "\n"

    # Dated in _drafts/ too, against Jekyll's usual convention, so publishing is
    # a plain `git mv` to _posts/ with no rename to get wrong. Jekyll reads the
    # date off the filename either way, so the preview URL is the final one.
    name = f"{published:%Y-%m-%d}-{slug}.md"
    draft = os.path.join(ROOT, "_drafts", name)
    rel = os.path.relpath(draft, ROOT).replace("\\", "/")

    if args.dry_run:
        print(doc)
    else:
        if os.path.exists(draft) and not args.force:
            sys.exit(f"{rel} already exists -- pass --force to overwrite it")
        os.makedirs(os.path.dirname(draft), exist_ok=True)
        with open(draft, "w", encoding="utf-8", newline="\n") as f:
            f.write(doc)

    langs = ", ".join(sorted({f["lang"] for f in stats["fences"]})) or "none"
    print(f"\n{'would write' if args.dry_run else 'wrote'}: {rel}", file=sys.stderr)
    print(f"  title      {title}", file=sys.stderr)
    print(f"  date       {published:%Y-%m-%d %H:%M:%S %z}", file=sys.stderr)
    print(f"  canonical  {canonical}", file=sys.stderr)
    print(f"  tags       {', '.join(tags) or '(none)'}", file=sys.stderr)
    print(f"  images     {stats['images']} -> assets/img/{published:%Y/%m}/", file=sys.stderr)
    print(f"  fences     {len(stats['fences'])} ({langs})", file=sys.stderr)
    print(f"  youtube    {stats['youtube']}", file=sys.stderr)
    print(f"  TODO embeds {stats['todo']}", file=sys.stderr)
    print(f"  publish    git mv {rel} _posts/{name}", file=sys.stderr)

    # Every fence, not only the doubtful ones. A wrong language is visible on the
    # page -- it drives the highlighting and the label in the block's header bar.
    if stats["fences"]:
        print("\ncheck every fence language:", file=sys.stderr)
        for n, f in enumerate(stats["fences"], 1):
            mark = " <-- confirm" if f["note"] else ""
            print(f"  {n:2}. {f['lang']:11} {f['first']!r}{mark}", file=sys.stderr)

    if new:
        review(
            "new to this site, and will display as their own slug: "
            + ", ".join(new)
            + "\n      The sidebar entry and the count are generated, so nothing has to be"
            + "\n      added. Only give one a display name in _data/tags.yml if the slug"
            + "\n      reads badly, the way csharp has to read as c#:\n"
            + "\n".join(f"        - slug: {t}\n          name: '{t}'" for t in new)
        )
    if len(tags) > 3:
        review(f"{len(tags)} tags is more than this site usually carries -- prune to the 2-3 that matter.")

    if REVIEW:
        print(f"\nreview ({len(REVIEW)}):", file=sys.stderr)
        for r in REVIEW:
            print(f"  - {r}", file=sys.stderr)
    else:
        print("\nreview: nothing outstanding", file=sys.stderr)


if __name__ == "__main__":
    main()
