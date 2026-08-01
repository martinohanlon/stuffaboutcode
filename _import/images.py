#!/usr/bin/env python3
"""
Bring remote images into the repo.

Sources, in preference order (runbook step 03):
  1. The Takeout Albums/ folder -- the uploaded originals at full resolution.
     192 of 207 Blogger URLs match one by filename, so most of this needs no
     network at all.
  2. Direct download for the rest, using the /s1600/ variant already recorded in
     the Markdown rather than a thumbnail.

Writes assets/img/YYYY/MM/<name> plus _import/image-map.tsv. convert.py reads
that map and rewrites the URLs, which keeps the rewrite inside the reproducible
pipeline instead of being a one-off edit to _posts.

Re-runnable: files already present and correctly sized are left alone.

Usage:
  python _import/images.py            # localise everything
  python _import/images.py --dry-run  # plan only, no writes or downloads
  python _import/images.py --offline   # Albums only, skip downloads
"""

import io
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import defaultdict

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, "archive", "takeout-stuffaboutcode.zip")
MAP = os.path.join(ROOT, "_import", "image-map.tsv")
ASSETS = os.path.join(ROOT, "assets", "img")

DRY = "--dry-run" in sys.argv
OFFLINE = "--offline" in sys.argv

MAX_WIDTH = 1600
UA = "Mozilla/5.0 (compatible; stuffaboutcode-migration/1.0)"

# Affiliate and ad artwork: the runbook says drop these entirely.
DROP = re.compile(r"amazon-adsystem|adsbygoogle|googlesyndication|doubleclick", re.I)

MD_IMAGE = re.compile(r"!\[[^\]]*\]\((https?://[^)\s]+)\)")


def safe_name(url):
    """Filename for a URL, kept meaningful but safe in a path and a URL.

    Lowercased so a case-insensitive Windows checkout cannot collide two files
    that differ only in case, which a case-sensitive Pages host would serve as
    two distinct assets.
    """
    base = url.rstrip("/").rsplit("/", 1)[-1].split("?")[0]
    base = urllib.parse.unquote(base).lower()
    base = re.sub(r"[^a-z0-9._-]+", "-", base).strip("-.")
    if not os.path.splitext(base)[1]:
        base += ".jpg"
    return base or "image.jpg"


def collect_refs():
    """url -> earliest YYYY/MM it is referenced from."""
    refs = defaultdict(set)
    for d in ("_posts", "_drafts", "_pages"):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for n in sorted(os.listdir(p)):
            if not n.endswith(".md"):
                continue
            text = open(os.path.join(p, n), encoding="utf-8").read()
            m = re.match(r"^(\d{4})-(\d{2})-", n)
            if m:
                ym = f"{m.group(1)}/{m.group(2)}"
            else:
                fm = re.search(r"^date: (\d{4})-(\d{2})-", text, re.M)
                ym = f"{fm.group(1)}/{fm.group(2)}" if fm else "undated"
            for url in MD_IMAGE.findall(text):
                refs[url].add(ym)
    return {u: sorted(v)[0] for u, v in refs.items()}


def album_index():
    if not os.path.exists(ZIP):
        return {}, None
    z = zipfile.ZipFile(ZIP)
    idx = {}
    for n in z.namelist():
        if "/Albums/" in n and not n.endswith("/") and not n.endswith(".json"):
            idx.setdefault(os.path.basename(n).lower(), n)
    return idx, z


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def shrink(data, name):
    """Cap width at MAX_WIDTH. GIFs are left alone (animation)."""
    if name.endswith(".gif"):
        return data, None
    try:
        im = Image.open(io.BytesIO(data))
        w, h = im.size
    except Exception:
        return data, None
    if w <= MAX_WIDTH:
        return data, (w, h)
    nh = max(1, round(h * MAX_WIDTH / w))
    im = im.convert("RGB") if im.mode in ("P", "CMYK") and not name.endswith(".png") else im
    im = im.resize((MAX_WIDTH, nh), Image.LANCZOS)
    buf = io.BytesIO()
    if name.endswith((".jpg", ".jpeg")):
        im.save(buf, "JPEG", quality=85, optimize=True, progressive=True)
    elif name.endswith(".png"):
        im.save(buf, "PNG", optimize=True)
    else:
        return data, (w, h)
    return buf.getvalue(), (MAX_WIDTH, nh)


def load_map():
    """Previous run's url -> path, so re-runs skip work already done."""
    prev = {}
    if os.path.exists(MAP):
        for line in open(MAP, encoding="utf-8"):
            if line.startswith("#") or "\t" not in line:
                continue
            u, _, p = line.rstrip("\n").partition("\t")
            prev[u] = p
    return prev


def main():
    refs = collect_refs()
    idx, z = album_index()
    prev = load_map()
    print(f"image references: {len(refs)}   album originals indexed: {len(idx)}\n")

    mapping = {}
    used = {}          # relative path -> source url
    stats = defaultdict(int)
    failures = []
    thirdparty = []
    saved_bytes = 0

    for url in sorted(refs):
        if DROP.search(url):
            mapping[url] = ""
            stats["dropped (ad/affiliate)"] += 1
            continue

        ym = refs[url]
        name = safe_name(url)
        rel = f"/assets/img/{ym}/{name}"
        target = os.path.join(ASSETS, ym.replace("/", os.sep), name)

        host_local = "googleusercontent" in url
        if not host_local:
            thirdparty.append(url)

        # Already localised on a previous run? Only trust this when the *map*
        # says this URL owns that file. Trusting os.path.exists(target) alone
        # makes two different images that share a filename collapse onto one.
        done = prev.get(url)
        if done and os.path.exists(os.path.join(ROOT, done.lstrip("/").replace("/", os.sep))):
            mapping[url] = done
            used[done] = url
            stats["already present"] += 1
            continue

        data = None
        src = None
        key = os.path.basename(url.rstrip("/").split("?")[0]).lower()
        if key in idx and z is not None:
            data, src = z.read(idx[key]), "album"
        elif not OFFLINE:
            try:
                data, src = fetch(url), "download"
                time.sleep(0.2)
            except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
                failures.append((url, str(e)[:70]))
                stats["FAILED"] += 1
                continue
        else:
            stats["skipped (offline, not in albums)"] += 1
            continue

        if not data:
            failures.append((url, "empty response"))
            stats["FAILED"] += 1
            continue

        original = len(data)
        data, dims = shrink(data, name)
        if len(data) < original:
            saved_bytes += original - len(data)
            stats["resized"] += 1

        # Two different images sharing a filename in the same month. Compare
        # bytes rather than assuming, so an identical re-upload reuses the file
        # and only a genuinely different image gets a suffix.
        def taken(r, t):
            if used.get(r) not in (None, url):
                return True
            if os.path.exists(t):
                with open(t, "rb") as fh:
                    return fh.read() != data
            return False

        if taken(rel, target):
            stem, ext = os.path.splitext(name)
            i = 2
            while True:
                cand = f"{stem}-{i}{ext}"
                r = f"/assets/img/{ym}/{cand}"
                t = os.path.join(ASSETS, ym.replace("/", os.sep), cand)
                if not taken(r, t):
                    break
                i += 1
            name, rel, target = cand, r, t
            stats["renamed (collision)"] += 1

        used[rel] = url
        mapping[url] = rel
        stats[f"from {src}"] += 1

        if not DRY:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(data)

    if not DRY:
        with open(MAP, "w", encoding="utf-8", newline="\n") as f:
            f.write("# remote url\tlocal path (empty = drop). Generated by _import/images.py\n")
            for u in sorted(mapping):
                f.write(f"{u}\t{mapping[u]}\n")

    for k, v in sorted(stats.items(), key=lambda kv: -kv[1]):
        print(f"  {v:4}  {k}")
    if saved_bytes:
        print(f"\nresizing saved {saved_bytes / 1e6:.1f} MB")

    if thirdparty:
        print(f"\nthird-party hosts self-hosted ({len(thirdparty)}) -- review:")
        for u in thirdparty:
            print(f"  {u}")

    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for u, e in failures:
            print(f"  {u}\n      {e}")

    if not DRY:
        total = sum(
            os.path.getsize(os.path.join(dp, f))
            for dp, _, fs in os.walk(ASSETS)
            for f in fs
        )
        n = sum(len(fs) for _, _, fs in os.walk(ASSETS))
        print(f"\nassets/img: {n} files, {total / 1e6:.1f} MB")
        print(f"wrote {os.path.relpath(MAP, ROOT)}")


if __name__ == "__main__":
    main()
