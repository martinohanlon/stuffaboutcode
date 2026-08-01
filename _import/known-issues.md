# Known issues carried over from Blogger

These are defects **in the original published posts**, reproduced faithfully by
the importer. Each was traced back to the raw HTML in `_import/blog.xml` before
being classified this way — none is a conversion artefact.

## Fixed by hand

The three posts whose Python would not parse have been corrected in `_posts/`.
`verify.py` now reports **zero** indentation failures.

| Post | Was |
|---|---|
| `2012-12-09-raspberry-pi-gpio-game-how-many-times.md` | Two separate defects: `binary = "1" + binary` indented ~20 where its siblings use 12 (that line mixes four `&nbsp;` pairs *and* two tab-spans), and `while True:` indented 8 inside a `try:` body indented 1. |
| `2013-02-01-raspberry-pi-minecraft-auto-bridge.md` | `if ((movementX < -0.2) ...):` had no indentation while its body was indented 12, so it broke the loop it sat in. |
| `2015-09-27-read-piaware-flight-data-with-python.md` | `sleep(1)` and the lines after it indented 3 where the enclosing block uses 8. |

> **`tokenize` reports one error at a time.** The GPIO post was recorded here as
> a single broken line for exactly that reason — the second defect only appeared
> once the first was fixed. If another post ever fails this way, re-run the check
> after each fix rather than assuming the first report is the whole story.

These fixes live only in `_posts/`. They are not in `_import/blog.xml`, so
re-running the importer would discard them — one more reason not to.

## Still present: not indentation

| Post | Problem | In the source? |
|---|---|---|
| `_posts/2014-05-21-minecraft-graphics-turtle.md` | `tell the turtle to go forward 25 blocks` is missing its leading `#`, so a comment parses as code. Every other comment in the listing has one. | Yes — the `#` was never typed. |
| `_posts/2015-05-12-astro-pi-getting-started.md` | `from sense-hat import AstroPi` — module is `sense_hat`, a hyphen is not valid in an import. | Yes — typo as published. |

## Indentation is normalised to 4 spaces

Several posts indented Python 1–2 spaces per level, because they carry
indentation two ways in the same listing: `Apple-tab-span` elements holding a
single literal space, and runs of `&nbsp;` four or more wide. Observed widths ran
`[1, 2, 3, 4, 5, 8]`.

`convert.reindent_python()` normalises every python fence to 4 spaces per level.
It does **not** scale the leading whitespace or rank the distinct widths — both
get this wrong, because once the two styles are mixed the widths no longer map
monotonically onto depth. Instead it uses `tokenize`, which maintains Python's
real indent stack and emits INDENT/DEDENT, giving the true depth of every logical
line. That works on the Python 2 listings too, since `tokenize` does not check
grammar.

Left untouched on purpose:

- lines inside triple-quoted strings (re-indenting rewrites the literal)
- continuation lines aligned inside brackets, where the alignment is the point

A rewrite is only accepted if the significant token stream is identical
(INDENT/DEDENT included, so nesting cannot change) and, when the block parses at
all, the AST matches exactly. Otherwise the original is kept.

Three posts could not be normalised automatically — their source indentation was
self-inconsistent, so `tokenize` raised `IndentationError` and there was no
reliable nesting to re-emit. Those have since been repaired by hand (see above),
and every Python fence in `_posts/` now indents in clean multiples of 4.

## Verified benign

Checked by hand against the raw HTML; `audit.py` flags them, and each is correct:

- `_posts/2012-06-29-python-encode-xml-escape-characters.md` keeps `&quot;` and
  `&amp;` as literal text inside fences. The post is *about* XML escaping and the
  source is double-escaped (`&amp;quot;`), so the entity text is the content.
- `_posts/2012-05-06-facebook-comments-and-aspnet.md` and
  `_posts/2012-12-01-blogger-creating-html-gadget-for.md` contain `<div>` inside
  fences. They are HTML/ASP listings; that is the code.
- Three posts show a code token "lost" and a matching one "added"
  (`inc`+`lude` -> `include`, `openJunctio`+`tore` -> `openJunction`,
  `fileNam`+`eBits` -> `fileNameBits`). Blogger's editor split those identifiers
  across two spans mid-word; rejoining them is the fix, not damage.

## Not defects

- **43 Python 2 blocks** (`print "..."`, `except X, e:`). Correct as published for
  2012–2013 Raspberry Pi posts; they are not modernised. `verify.py` buckets
  these separately so they do not mask real breakage.
- **Fragments/excerpts** that start mid-function and so do not parse standalone.
- **179 `text`-tagged blocks** holding console output, `pydoc` dumps, sensor
  readings, `screen -ls` listings, config fragments and single-line snippets with
  no reliable language tell. `text` is a real tag, so the "always tag a fence"
  rule holds. Guessing here would mis-highlight, which reads worse than plain.

## Images that were already broken before the migration

Six image references could not be brought local, and none of them is a
migration problem — every one is a third-party host that has rotted. They are
left pointing at their original URLs, which is no worse than the live blog
today, and flagged by `verify.py` as "remote image on a third-party host".

| Host | Refs | Status |
|---|---|---|
| `static.movember.com` | 3 | Domain no longer resolves (DNS failure). Gone for good. |
| `rosettacode.org` | 1 | `404 Not Found`. |
| `scratch.mit.edu` | 1 | `403 Forbidden` — hotlink protection. |
| `www.modmypi.com` | 1 | `403 Forbidden` — hotlink protection. |

The two 403s may still render in a browser, which sends a referer we do not.
Fetching them anyway would mean deliberately working around another site's
hotlink protection, so it has not been done.

Deciding what to do here is editorial: replace the images, or delete the
references and any surrounding text that points at them. Note the three
Movember images are on posts about a charity campaign from 2012.

`licensebuttons.net` (the CC BY-SA badge) fetched fine and is now self-hosted,
along with everything from `blogger.googleusercontent.com`.

## Still outstanding for later phases

- `goo.gl` short links need resolving while they still redirect (runbook 07).
- Figure captions are currently emitted as an italic paragraph after the image.
  The design calls for a bordered `<figure>` with a mono caption; wiring that up
  belongs with the theme (Phase 4).
