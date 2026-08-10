---
name: crosspost-medium
description: Cross-post something published on Medium to stuffaboutcode.com. Use when given a Medium URL to bring across, with or without a separate canonical URL. Converts the post to a dated Jekyll draft, self-hosts the images, and leaves a review list of the judgement calls.
---

# Cross-posting from Medium

Martin publishes on Medium (usually under a Neo4j publication) and keeps a copy
here. The copy is not the original: the canonical link goes to whoever should get
the credit, and this site keeps the post alive for the day the original 404s.

You need **two URLs**, and they are usually different:

| | |
|---|---|
| **Medium URL** | the source to convert *from* |
| **Canonical URL** | the page search engines should credit |

The canonical is often a third site — a Medium post can itself be the copy, with
the original on `graphacademy.neo4j.com` or `neo4j.com`. Do not assume the Medium
URL is canonical; getting this wrong tells Google that Martin's copy competes with
the original.

**Both arrive as loose text**, in whatever wording Martin used:

```
/crosspost-medium https://medium.com/neo4j/some-post-c969ae5f4230 canonical link - https://graphacademy.neo4j.com/blog/some-post
```

Pick them apart by host, not by position or by the words around them: the
`medium.com` URL (or `*.medium.com`) is the source, the other is the canonical.
**If only one URL is given, ask** — unless it is a Medium URL and he has said it
is the original, in which case pass no `--canonical` and it defaults to Medium's
own.

## 1. Convert

```bash
python .claude/skills/crosspost-medium/medium_to_md.py <medium-url> \
    --canonical <canonical-url> --tags graphrag,neo4j
```

Writes `_drafts/YYYY-MM-DD-slug.md`, downloads the images to
`assets/img/YYYY/MM/`, and prints a report plus a numbered review list.

Useful flags: `--dry-run` prints the markdown and writes nothing, `--force`
overwrites an existing draft, `--credit-name 'Neo4j GraphAcademy'` labels the
credit link, `--no-credit` drops it, `--self-test` runs the offline checks.

It reads Medium's own JSON payload (`medium.com/p/<id>?format=json`), not the
article HTML. **Don't be tempted to scrape the page instead** — it is rendered
client-side, so every `<img>` arrives with an empty `src` and code blocks have no
`<pre>` at all. The JSON has the images, the code, the tags, the publish
timestamp and the offsets of every inline-code span.

## 2. Work the review list

The script does the mechanical conversion and refuses to guess at the rest. Every
line it prints needs a decision.

**Check every fence language.** It prints all of them, not just the doubtful
ones, because a wrong language is visible on the page — it drives the
highlighting *and* the label in the block's header bar. Medium's own language
label is unreliable: it tags Cypher as `sql`, `scss` or `php`, and has called a
prompt transcript `javascript`. The script prefers what the content looks like
and flags every disagreement, but the last word is yours. Rouge (4.7) handles
`cypher`; use `text` for transcripts, console output and prompts.

**Write the alt text.** Medium captions come across as alt text, but most images
have no caption, and those arrive as `![]`. Describe them.

**Prune the tags.** Medium posts usually carry five; this site runs two or three.
They must be slugs (`raspberry-pi`, not `Raspberry Pi`). Nothing else is needed:
the tag page, the sidebar entry and the count are all generated. Only add an entry
to `_data/tags.yml` if the slug is a poor display name, the way `csharp` needs to
read as `c#`. The script still lists tags with no entry — treat that as a prompt to
consider a display name, not a chore.

**Resolve any TODO embeds.** YouTube is converted to
`{% include youtube.html id="…" %}` automatically. Anything else is left as
`<!-- TODO embed: url -->`, which `verify.py` reports as an unconverted embed.
Gists in particular should become a fenced code block — there are no JS embeds on
this site, and a gist can rot like any other remote content.

**Deal with the link cards.** Medium's link cards become a blockquote link. They
read like platform furniture. Delete them, or leave them and say so — do not
rewrite one into a sentence of your own.

## 3. Read it as prose — but do not write any

**The words are Martin's. Never reword, rewrite, expand, condense, or add a
sentence.** Not to improve an excerpt, not to fix an awkward line, not to smooth
a transition. If a sentence reads badly, that is his to fix, and a draft that
comes back in his own voice is worth more than a better-written one that doesn't.
Say what you noticed in the report and leave the text alone.

What you *may* remove — whole blocks of Medium's platform furniture, deleted
outright, never reworded:

- clap, follow and subscribe prompts
- newsletter and membership CTAs
- "originally published" lines Medium added itself (the script writes the
  credit line at the end; a second one is Medium's)
- boilerplate publication footers, the "What Is …?" section that ends every
  post in a publication
- `?ref=medium` and other tracking params on links that survive

And what the conversion itself broke — damage, not wording — fix silently and
list it in the report:

- missing spaces where an inline-code span met the next word
  (`` `execute`method ``, `` `GraphDatabase.driver`class ``)
- mangled punctuation and entities the conversion left behind

The test is whether the fix changes what Martin wrote or restores it. Closing up
`` `execute`method `` restores it. Anything that alters a sentence he actually
typed does not, however small the improvement — including a first paragraph too
thin to carry the home-page excerpt and meta description. That one is still worth
checking, and it is why the credit line goes at the *end*: at the top it would
become the description. **Report it and leave it.**

## 4. Verify

```bash
python _import/verify.py                       # expect "problems: none"
bundle exec jekyll build --drafts --quiet
grep -o '<link rel="canonical"[^>]*>' _site/posts/<slug>/index.html
```

`verify.py` is the repo's content linter and it catches the failure modes that
matter here: a remote image, a fence with no language, a leftover HTML tag, a
non-breaking space, an unresolved entity, an unconverted embed.

The canonical must point at the **canonical URL**, while `og:url` stays on
*this* site — that is deliberate, so a share of Martin's copy lands on his copy.

Then read the built page in a browser. The last migration shipped 124 passing
checks alongside a completely unstyled site; automated checks do not see what a
page looks like.

## 5. Stop

**Leave the draft uncommitted.** Martin edits the wording before it goes in — the
drafting is useful, the wording is his, first draft to last. Report what changed,
that it is uncommitted, and wait.

The report is where everything you noticed but did not touch goes: the awkward
line, the thin opening paragraph. List them as observations, not as edits you
made.

Publishing, when he says so, is a plain move — the draft is already dated, so
there is no rename to get wrong:

```bash
git mv _drafts/YYYY-MM-DD-slug.md _posts/YYYY-MM-DD-slug.md
```

## Notes

- **No `redirect_from`.** That is for the 136 posts carried off Blogger, whose old
  URLs must keep working. A cross-post is new here and never had another URL on
  this site. `verify.py` only expects `redirect_from` on posts dated before
  2026-08-01.
- **Images** are fetched at 1600px (or the original width, if smaller) and named
  `<slug>-<n>.<ext>`. Nothing may point at a Medium URL — `miro.medium.com` is
  someone else's server, and the last thing this site did was spend a fortnight
  recovering from exactly that.
- **The date** keeps Medium's first-published time, converted to Europe/London,
  and carries an explicit offset (`+01:00` BST, `+00:00` GMT). Without the offset
  a post can land on the wrong day.
- **Dated draft filenames** are deliberate here, and differ from the convention in
  `README.md` for ordinary drafts. It makes publishing a straight `git mv`, and
  Jekyll reads the date off the filename either way, so the preview URL is the
  final URL.
- **Member-only posts** are flagged in the review list. Check the body is complete
  and not a truncated preview.
