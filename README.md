# stuffaboutcode.com

Martin O'Hanlon's project blog — Python, Raspberry Pi and Minecraft how-tos.
A Jekyll site hosted on GitHub Pages.

---

## Project structure

```
├── _config.yml            site config, permalinks, plugins, pagination
├── index.html             the home list (paginated, 7 per page)
├── search.json            build-time search index (title, url, date, tags, first 200 words)
│
├── _posts/                one file per post — YYYY-MM-DD-slug.md
├── _pages/                standalone pages — about, raspberry-pi, minecraft, …
├── _drafts/               unpublished work, no date in the filename
│
├── _layouts/
│   ├── default.html       header, content/sidebar grid, footer
│   ├── home.html          the post list — also serves the tag pages
│   ├── post.html          single post
│   ├── page.html          standalone page
│   └── tag.html           generated per label at /tags/:slug/
│
├── _includes/
│   ├── head.html          meta, fonts, stylesheet, theme bootstrap
│   ├── header.html        wordmark, nav, theme toggle
│   ├── sidebar.html       search, labels, pages, "writing again" card
│   ├── footer.html
│   ├── list-screen.html   list heading + rows + pager (home and tag pages)
│   ├── post-list.html     the post rows themselves
│   ├── youtube.html       {% include youtube.html id="…" %}
│   └── embed.html         {% include embed.html src="…" title="…" %}
│
├── _data/
│   ├── tags.yml           label slug → display name and count (drives the sidebar)
│   └── about_links.yml    the link cards on /about/
│
├── assets/
│   ├── css/main.css       the whole stylesheet
│   ├── js/site.js         theme toggle, copy buttons, search
│   ├── img/YYYY/MM/       post images, self-hosted
│   └── favicon.ico
│
├── _import/               one-off tooling from the Blogger migration
└── archive/               the original Blogger export
```

> **`_import/` is finished work, not part of running the site.** Its scripts
> regenerate `_posts/`, `_pages/` and `_drafts/` from the old Blogger export,
> **deleting whatever is there first**. Once you have written a new post, never
> run them — you would lose it. Nothing in normal use needs that directory.

---

## Installation

You need **Ruby** (3.3 or newer) and **Bundler**. That is all — the site has no
Node or npm dependency.

```bash
bundle install
```

Currently building against Ruby 3.3.5, Bundler 2.5.16, Jekyll 4.4.1.

Plugins, all from the `Gemfile`: `jekyll-redirect-from`, `jekyll-feed`,
`jekyll-sitemap`, `jekyll-paginate-v2`. Don't add more without a good reason —
the build runs on GitHub Actions precisely so the plugin list stays ours.

---

## Development

### Run the dev server

```bash
bundle exec jekyll serve --livereload --drafts
```

Then open <http://localhost:4000>. `--drafts` includes `_drafts/`;
`--livereload` refreshes the browser on save.

Useful flags:

| Flag | Why |
|---|---|
| `--drafts` | show unpublished posts from `_drafts/` |
| `--livereload` | reload the browser on save |
| `--incremental` | faster rebuilds while writing (can miss changes; restart if something looks stale) |
| `--future` | show posts dated in the future |
| `--port 4001` | if 4000 is taken |

**On Windows, `--detach` does not work** — Jekyll uses `fork()`, which Windows
lacks. Leave the server running in its own terminal.

### Build

```bash
bundle exec jekyll build
```

Output goes to `_site/`, which is generated and git-ignored — never edit it.

To preview a finished build without Jekyll:

```bash
cd _site
python -m http.server 4001
```

Open [http://localhost:4001](http://localhost:4001).

### Deployment

Not wired up yet. The intent is a GitHub Actions workflow that builds on push
to `main` and publishes to Pages — that is why the build does not rely on Pages'
own Jekyll, which restricts plugins.

---

## How to

### Write a post

Create `_posts/YYYY-MM-DD-some-slug.md`:

`````markdown
---
title: 'Raspberry Pi - reading a DHT22 sensor'
date: 2026-08-01 20:15:00 +01:00
tags: [python, raspberry-pi]
---

Opening paragraph. This becomes the excerpt on the home page and the
description in search results, so make it say something.

## What you need

- a Raspberry Pi
- a DHT22 sensor

```python
import board
import adafruit_dht

sensor = adafruit_dht.DHT22(board.D4)
print(sensor.temperature)
```
`````

- The URL comes from the filename minus the date: `/posts/some-slug/`.
- No `layout:` needed — posts get it automatically.
- **The date needs a UTC offset**: `+01:00` for BST, `+00:00` for GMT. Without
  one the post can land on the wrong day.
- `tags` are lowercase slugs — `raspberry-pi`, not `Raspberry Pi`.
- Headings inside a post start at `##`. The theme prefixes every `h2` with a
  green `##` marker, which is a deliberate part of the design.

### Fence every code block with a language

```` ```python ````, ```` ```bash ````, ```` ```html ````, and so on. Never a
bare ```` ``` ````. The language drives both the syntax colours and the label in
the block's header bar. Use `text` for console output or anything that isn't a
real language.

Code is **never wrapped** — long lines scroll sideways. Indentation is meaning
in Python posts, so leave it alone.

### Add images

Put the file in `assets/img/YYYY/MM/` matching the post's date, then reference
it with an absolute path:

```markdown
![A DHT22 wired to a Pi](/assets/img/2026/08/dht22-wiring.jpg)
```

- Self-host everything. Don't hotlink — the old blog is full of images that have
  since rotted away on other people's servers.
- Resize to about **1600px wide** before committing. Anything larger is wasted.
- Lowercase filenames, hyphens not spaces.

### Embed a video

```liquid
{% include youtube.html id="dQw4w9WgXcQ" %}
```

Anything else that needs an iframe:

```liquid
{% include embed.html src="https://…/embed" title="What it is" %}
```

### Start a draft

Put it in `_drafts/` with **no date in the filename** — `_drafts/my-idea.md`.
It shows up under `jekyll serve --drafts` and is skipped by a normal build.
Publishing means moving it to `_posts/` and adding the date to the filename.

### Add a page

Create `_pages/thing.md`, which becomes `/thing/`:

```markdown
---
title: 'Thing'
---

Body copy.
```

To put it in the sidebar's **Pages** list, add a link in
`_includes/sidebar.html`. To add it to the top nav, edit
`_includes/header.html`.

### Use tags

Add slugs to a post's `tags:` and the tag page at `/tags/<slug>/` is generated
automatically, along with the chips under the post.

**A brand-new tag will not appear in the sidebar's Labels list.** That list is
driven by `_data/tags.yml`, which carries a display name and count per label —
it is how `/tags/csharp/` manages to display as `c#`. To list a new label, add
an entry:

```yaml
- slug: sensors
  name: 'sensors'
  count: 3
```

The `count` is not calculated, so it needs updating by hand. Keep the list in
count-descending order.

### Change the look

Everything is in `assets/css/main.css`. Colours are `oklch()` custom properties
defined twice at the top — once for dark, once under
`:root[data-theme="light"]`. Change a token there and it applies everywhere.

> **If you ever add a file to `assets/` that needs front matter**, give it
> `layout: null`. Front matter makes Jekyll treat a file as a page, and a page
> gets wrapped in a layout — which silently serves a stylesheet as an HTML
> document. `_config.yml` has a default guarding `assets/`; keep it.

---

## Things not to break

- **Never remove a `redirect_from` entry.** Each one keeps an old Blogger URL
  working, and some of those links are over a decade old.
- **Permalinks are `/posts/:slug/`.** Renaming a post file changes its URL.
- **Two fonts only** — JetBrains Mono for chrome, headings and code; IBM Plex
  Sans for post prose.
- **No icon library.** Every glyph in the design is a text character: `←` `→`
  `↗` `▍` `☀` `☾` `$` `/` `#`.

## Checking your work

```bash
python _import/verify.py
```

A content linter, safe to run any time — it reads files and writes nothing. It
reports untagged code fences, missing front matter, posts still pointing at
remote images, and assets accidentally wrapped in a layout. Needs
`pip install beautifulsoup4 tzdata`.
