#!/usr/bin/env python3
"""
Post-import checks on _posts / _drafts / _pages.

The important one is PYTHON SYNTAX: the runbook calls flattened indentation the
single highest-risk item in the migration, and a Python block that no longer
parses is exactly what that looks like. Compiling every python fence turns
"looks fine to me" into a number.

Usage:  python _import/verify.py [-v]
"""

import ast
import io
import os
import re
import sys
import tokenize
import warnings
from collections import Counter

# Compiling the posts' own code raises SyntaxWarning for invalid escapes like
# "\*" in 2012-era regex strings. That is the published code, not a conversion
# problem, and it drowns out the actual report.
warnings.filterwarnings("ignore", category=SyntaxWarning)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert as C  # noqa: E402  share one fence parser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERBOSE = "-v" in sys.argv
HTML_LEFTOVER = re.compile(r"</(div|span|br|font|pre|table|td|tr|b|i|a)\b|<(div|span|font)\b", re.I)
INLINE_CODE = re.compile(r"`[^`\n]+`")

# Posts dated before this are Blogger imports and must keep their old URL in
# redirect_from. Posts written since are native and never had one.
MIGRATION_DATE = "2026-08-01"


def files():
    for d in ("_posts", "_drafts", "_pages"):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for n in sorted(os.listdir(p)):
            if n.endswith(".md"):
                yield os.path.join(p, n)


def tokenizes_cleanly(code):
    """True if Python can resolve the block's indentation structure.

    Version-independent: tokenize maintains the indent stack but does not check
    grammar, so a Python 2 listing tokenizes fine while still failing ast.parse.
    An IndentationError here means the indentation itself is inconsistent.
    """
    try:
        list(tokenize.generate_tokens(io.StringIO(code + "\n").readline))
        return True
    except IndentationError:
        return False
    except (tokenize.TokenError, SyntaxError):
        return True  # unterminated fragment, not an indentation fault


PY2_PRINT = re.compile(r"^\s*print\s+[\"'a-zA-Z_(]", re.M)
PY2_OTHER = re.compile(r"\bexcept\s+\w+\s*,\s*\w+:|\braw_input\s*\(|\bunicode\s*\(|<>")


def classify(code, err):
    """Why did this python block fail to parse?

    Only 'indentation' implicates the migration. Python 2 syntax and truncated
    fragments are faithful reproductions of what was published in 2012-2013.
    """
    # Check indentation FIRST, with tokenize rather than ast. tokenize does not
    # check grammar, so it works on the Python 2 listings too -- classifying on
    # ast alone let "python2" mask real indentation faults in the same block.
    if not tokenizes_cleanly(code):
        return "indentation"
    msg = str(err.msg).lower()
    if "print" in msg and "parentheses" in msg:
        return "python2"
    if PY2_PRINT.search(code) or PY2_OTHER.search(code):
        return "python2"
    lines = [l for l in code.split("\n") if l.strip()]
    # An excerpt lifted from inside a function starts indented; that is faithful,
    # not damage. Check before blaming indentation.
    if lines and re.match(r"^[ \t]+\S", lines[0]):
        return "fragment/truncated"
    # A snippet that opens a block and stops -- "while gameover == False:" quoted
    # on its own to explain it -- is an excerpt, not broken indentation.
    if lines and lines[-1].rstrip().endswith(":"):
        return "fragment/truncated"
    if "indent" in msg:
        return "indentation"
    if "unterminated string" in msg or "was never closed" in msg or "eof" in msg:
        return "fragment/truncated"
    first = code.strip().split("\n")[0]
    if re.match(r"^\s+\S", code.split("\n")[0]) or re.match(
        r"^\s*(else|elif|except|finally)\b", first
    ):
        return "fragment/truncated"
    return "other"


BINARY_EXT = (".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".zip")


def check_built_assets(problems, issues):
    """No asset in _site may be an HTML document.

    A stylesheet needs front matter for Jekyll to process it, which also makes it
    a Page -- and a `type: "pages"` default then wraps it in a layout. The result
    serves the whole stylesheet as HTML: correct URL, HTTP 200, plausible byte
    count, and not one rule applied. Cheap to check, invisible otherwise.
    """
    site = os.path.join(ROOT, "_site")
    if not os.path.isdir(site):
        return
    for dp, _, fs in os.walk(site):
        for f in fs:
            if f.endswith(".html") or f.endswith(BINARY_EXT):
                continue
            p = os.path.join(dp, f)
            try:
                head = open(p, encoding="utf-8", errors="replace").read(200).lstrip()
            except OSError:
                continue
            if head.lower().startswith(("<!doctype html", "<html")):
                rel = os.path.relpath(p, ROOT).replace("\\", "/")
                problems["ASSET SERVED AS HTML -- layout leaked in"] += 1
                issues.append(f"{rel}: wrapped in a layout")


def split_front_matter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 3)
    if end < 0:
        return None, text
    return text[4:end], text[end + 5 :]


def main():
    langs = Counter()
    buckets = Counter()
    py_other = []
    py_ok = py_fail = 0
    failures = []
    problems = Counter()
    issues = []
    no_lang = []
    total = 0

    for path in files():
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        text = open(path, encoding="utf-8").read()
        total += 1

        fm, body = split_front_matter(text)
        if fm is None:
            problems["missing front matter"] += 1
            issues.append(f"{rel}: no front matter")
            continue
        if "title:" not in fm:
            problems["missing title"] += 1
            issues.append(f"{rel}: no title")
        if rel.startswith("_posts/"):
            if "date:" not in fm:
                problems["missing date"] += 1
                issues.append(f"{rel}: no date")
            # Only posts carried over from Blogger have an old URL to preserve.
            # Anything written since the migration is native to this site and
            # has never lived anywhere else.
            migrated = os.path.basename(rel)[:10] < MIGRATION_DATE
            if migrated and "redirect_from:" not in fm:
                problems["missing redirect_from"] += 1
                issues.append(f"{rel}: no redirect_from")

        # Fences are read from the whole file rather than from `body`, so
        # first_line is a line number in the file. Reporting "line 23" of a
        # listing leaves you counting lines by hand to find it.
        for lang, code, first_line in C.iter_fences(text):
            langs[lang or "(none)"] += 1
            if not lang:
                no_lang.append(rel)
            if lang == "python":
                try:
                    ast.parse(code)
                    py_ok += 1
                except SyntaxError as e:
                    bucket = classify(code, e)
                    buckets[bucket] += 1
                    file_line = first_line + (e.lineno or 1) - 1
                    if bucket == "indentation":
                        py_fail += 1
                        failures.append((rel, file_line, str(e.msg), code))
                    else:
                        py_other.append((bucket, rel, file_line, str(e.msg)))

        # markdown hygiene
        # Strip inline `code` as well as fenced blocks: a post may legitimately
        # quote a tag, e.g. `<span style="font-family: Courier New">`.
        stripped = INLINE_CODE.sub("", C.strip_fences(body))
        if HTML_LEFTOVER.search(stripped):
            problems["leftover HTML in prose"] += 1
            issues.append(f"{rel}: leftover HTML tags outside code")
        if re.search(r"&(lt|gt|amp|quot|nbsp|#\d+);", stripped):
            problems["unresolved HTML entity"] += 1
            issues.append(f"{rel}: unresolved HTML entity")
        if "\xa0" in body:
            problems["non-breaking space"] += 1
        if "blogger.googleusercontent.com" in body or "bp.blogspot.com" in body:
            problems["BLOGGER-HOSTED IMAGE -- must be 0"] += 1
        # Any remaining remote image is a host we do not control. Checking only
        # for googleusercontent would let third-party hotlinks pass unnoticed.
        for m in re.finditer(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", body):
            problems["remote image on a third-party host"] += 1
            issues.append(f"{rel}: remote image {m.group(1)}")
        if "<!-- TODO embed:" in body:
            problems["unconverted embed"] += 1

    check_built_assets(problems, issues)

    print(f"files: {total}")
    print(f"\nfence languages ({sum(langs.values())} blocks):")
    for k, v in langs.most_common():
        print(f"  {k:12} {v}")

    tot_py = py_ok + sum(buckets.values())
    print(f"\npython blocks: {tot_py}")
    print(f"  parse OK (py3)          {py_ok}")
    for k, v in buckets.most_common():
        flag = "  <-- MIGRATION BUG" if k == "indentation" else ""
        print(f"  {k:23} {v}{flag}")
    benign = py_ok + buckets["python2"] + buckets["fragment/truncated"]
    if tot_py:
        print(f"  -> {100 * benign / tot_py:.1f}% accounted for (valid py3, py2, or excerpt)")

    print("\nproblems:")
    if not problems:
        print("  none")
    for k, v in problems.most_common():
        print(f"  {v:4}  {k}")

    if failures:
        print(f"\n--- python parse failures ({len(failures)}) ---")
        for rel, lineno, msg, code in failures if VERBOSE else failures[:15]:
            first = code.strip().split("\n")[0][:70]
            print(f"  {rel}\n      line {lineno}: {msg}   | starts: {first!r}")

    other = [o for o in py_other if o[0] == "other"]
    if other:
        print(f"\n--- python 'other' ({len(other)}) ---")
        for bucket, rel, lineno, msg in other:
            print(f"  {rel}:{lineno}  {msg}")

    if issues and VERBOSE:
        print(f"\n--- issues ({len(issues)}) ---")
        for i in issues:
            print("  " + i)

    if no_lang:
        print(f"\nfences with no language tag: {len(no_lang)}")


if __name__ == "__main__":
    main()
