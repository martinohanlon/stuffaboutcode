# stuffaboutcode.com

A Jekyll rebuild of a Blogger blog (203 posts, 2012–2018, Python / Raspberry Pi / Minecraft how-tos), hosted on GitHub Pages. Active again — new posts are planned.

## Ground rules

- Jekyll 4 + kramdown + Rouge. Built by GitHub Actions, **not** Pages' built-in Jekyll — we want current Jekyll and unrestricted plugins.
- Plugins: `jekyll-redirect-from`, `jekyll-feed`, `jekyll-sitemap`, `jekyll-paginate-v2`. Don't add more without asking.
- Permalinks are `/posts/:slug/`. Every post keeps its original Blogger URL in `redirect_from`. **Never remove a `redirect_from` entry** — that's 14 years of inbound links.
- No comments. Not imported, not to be added.
- No JS framework, no build step beyond Jekyll, no npm dependency for the site itself. Search and the copy buttons are vanilla JS, tens of lines each.
- No icon library. Every glyph in the design is a text character.
- Two fonts only: JetBrains Mono (chrome, headings, code) and IBM Plex Sans (post prose). Nothing else.

## Content rules

- Post bodies are Markdown with **fenced code blocks that always carry a language tag**.
- Code is never wrapped — horizontal scroll only. Indentation is semantic in Python posts.
- Images live at `assets/img/YYYY/MM/`, self-hosted. Nothing may point at `blogger.googleusercontent.com`.
- Tags are slugs: `raspberry-pi`, not `raspberry pi`.
- `timezone: Europe/London` in config; keep the UTC offsets the importer wrote or posts shift a day.

## Local dev

```bash
bundle install
bundle exec jekyll serve --livereload --drafts
```

Drafts go in `_drafts/`. Push to `main` and Actions deploys.

## Don't

- Redesign anything. If something looks wrong, say so rather than changing it.
- Touch DNS, the `CNAME` file, or Pages settings without being asked.
- Delete the archived Blogger export from the repo — it's the source of truth for the whole migration.
