---
name: crosspost-graphacademy
description: Cross-post a Neo4j GraphAcademy blog post to stuffaboutcode.com. Use when given a graphacademy.neo4j.com/blog URL (and usually the monorepo source folder) to bring across. Converts the MDX source to a dated Jekyll draft with the canonical pointing back at GraphAcademy, self-hosts the images, and leaves a review list of judgement calls.
---

# Cross-posting from GraphAcademy

Martin publishes on `graphacademy.neo4j.com/blog` and keeps a copy here. GraphAcademy
is the original: the copy carries `canonical_url` back to it and ends with an
"Originally published on" line. For Medium sources use `crosspost-medium` instead.

## Inputs

- **Blog URL**: `https://graphacademy.neo4j.com/blog/<slug>`. This becomes the
  `canonical_url` and the credit link. The page may 404 for a while after release, so
  don't rely on fetching it.
- **Source folder** (usually given): `https://github.com/neo4j-graphacademy/monorepo/tree/development/packages/internal/content/posts/<slug>`.
  If it is not given, that path with the blog slug is the first guess.

The repo is private. Use `gh`, not WebFetch or raw URLs:

```bash
P=repos/neo4j-graphacademy/monorepo/contents/packages/internal/content/posts/<slug>
gh api "$P?ref=development" --jq '.[] | "\(.name) \(.type)"'
gh api "$P/post.mdx?ref=development" -H "Accept: application/vnd.github.raw"
gh api "$P/post.yml?ref=development" -H "Accept: application/vnd.github.raw"
gh api "$P/images/<file>?ref=development" -H "Accept: application/vnd.github.raw" > <dest>
```

## Mapping

The folder holds `post.mdx` (body), `post.yml` (metadata) and `images/`.

| Source | Here |
|---|---|
| `title` | `title`, single-quoted |
| `publishedAt` (a date) | `date: YYYY-MM-DD 10:00:00 +01:00`. No time is given, so use 10:00 and the Europe/London offset for that date (`+01:00` BST, `+00:00` GMT) |
| `tags` (yml) | not copied: they are GraphAcademy's taxonomy. Pick 2 or 3 site slugs from existing posts (`neo4j`, `cypher`, `graphrag`, `ai`, …) |
| blog URL | `canonical_url` and the closing credit line |
| `excerpt`, `coverImage`, `categories`, `courses`, `brand`, `author`, `featured`, `commentsEnabled` | dropped. The cover is not used on posts here |

Output goes in `_drafts/YYYY-MM-DD-slug.md`, where the slug comes from the title the way
other posts do it, and **not** from the blog URL, which differs. Images go in
`assets/img/YYYY/MM/<slug>-<n>.<ext>`, referenced as `/assets/img/YYYY/MM/…`.

Front matter, matching the existing cross-posts:

```yaml
---
title: '...'
date: 2026-07-03 10:00:00 +01:00
tags: [neo4j, cypher]
canonical_url: https://graphacademy.neo4j.com/blog/<slug>
---
```

No `redirect_from`.

End the body with a rule and the credit, in this form:

```markdown
---

*Originally published on [Neo4j GraphAcademy](<blog-url>) on 9 October 2026.*
```

## MDX components

The body is MDX. Plain Markdown and fenced code come across untouched. The components do not:

- `![alt](images/x.png)`: download it, rewrite the path, keep the alt text.
- `<CourseCallout slug="…" />`: becomes a blockquote link, as in the other cross-posts:
  `> **[Course Title](https://graphacademy.neo4j.com/courses/<slug>/)**`.
  Get the title from `…/content/courses/<slug>/course.yml` (`title:`) and don't guess it.
- `<Console label="…" />`: a Create-AuraDB button. Becomes a link with the same label to
  `https://console.neo4j.io?attribution=graphacademy`.
- `<Graph nodes={…} relationships={…} />`: an interactive graph with no static
  equivalent here, because the site has no JS embeds. **Remove it and flag it** in the report.
  Offer a screenshot saved to `assets/img/…` as the replacement. Don't redraw it as text.
- Any other component: leave nothing half-converted. Remove it and flag it.

Check every fence has a language tag (`verify.py` fails otherwise). GraphAcademy uses
`cypher`, which Rouge handles; use `text` for output and transcripts.

## Words are Martin's

Same rule as `crosspost-medium`: **never reword, rewrite, expand, condense or add
sentences.** The conversion may delete whole components and fix damage it caused, and
nothing else. Awkward lines, thin opening paragraphs, or stray trailing whitespace that
the source carries go into the report as observations and stay as they are.

## Verify

```bash
python _import/verify.py                       # expect "problems: none"
bundle exec jekyll build --drafts --quiet
grep -o '<link rel="canonical"[^>]*>' _site/posts/<slug>/index.html
```

The canonical must be the GraphAcademy URL, while `og:url` stays on this site.
Then look at the page in a browser. Automated checks don't see what a page looks like.

## Stop

**Leave the draft and its images uncommitted.** Martin edits before it goes in. Report:
what was converted, what was removed (especially any `<Graph>`), the tags chosen and
anything you noticed but didn't touch. Then wait.

Publishing, when he says so, is `git mv _drafts/<file> _posts/<file>`. Commits are made
as Martin only, with no `Co-Authored-By` trailer.
