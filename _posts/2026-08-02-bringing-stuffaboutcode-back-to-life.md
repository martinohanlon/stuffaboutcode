---
title: 'Bringing stuffaboutcode.com back to life'
date: 2026-08-02 11:30:00 +01:00
tags: [blogging, ai]
---

This blog stopped in 2018. Not deliberately — I just drifted away from it.

Somewhere along the way I moved into a job where writing and communicating *is* the work, and it turns out that when you write for a living you have a finite amount of writing in you. Every post I might have put here went to the organisation paying me instead. That's a reasonable trade while it lasts, but eight years of it left me with a blog full of Raspberry Pi and Minecraft projects and nothing after 2018.

![The old stuffaboutcode.com, running on Blogger](/assets/img/2026/08/old-stuffaboutcode-blogger.png)

That's what it looked like. Blogger, a theme I'd picked in about 2012, and 136 posts slowly rotting — images hotlinked from other people's servers that had since disappeared, `goo.gl` short links pointing at a service Google has since switched off, and code blocks that had lost their indentation somewhere in Blogger's editor years ago.

## What I actually wanted

Two things.

Somewhere to put my own ideas again, obviously. But also somewhere I control, that I can **cross-post to**. A lot of what I write now lives on someone else's platform, and platforms go away — I've just spent a fortnight proving that by chasing down dead links from 2012. If I publish something elsewhere I want a copy here with a canonical link pointing back to the original, so the search engines credit the right place and I still have it in ten years when the original has 404'd.

Longevity, basically. Plain Markdown files in a git repo will outlive any CMS I could pick.

## The drudge work

Migrating 136 posts off Blogger is not interesting work. It is:

- exporting from Google Takeout and working out that the format changed in 2018, so the standard `jekyll-import` tool doesn't read it any more
- converting HTML-with-inline-styles into clean Markdown
- rescuing code blocks from `<span style="font-family: Courier New">` soup, with the indentation intact, because these are Python posts and indentation is the program
- pulling 208 images off Google's servers before they vanish too
- writing a redirect for every single old URL, because there are fourteen years of inbound links out there

That's a week of tedium, and it's exactly the kind of thing a coding agent is good at. So I used one — Claude Code — and spent my time on the parts that actually needed me: what the thing should look like, what to keep, what to throw away, and whether the output was any good.

## Keeping myself in the loop

The way I work with a coding agent is that I stay in the process. Not "generate a website" and hope — review every phase, and be the one who decides. A few examples from this migration, including the ones where I was the reason it worked.

**The brief was wrong and the agent said so.** I'd written "203 posts" in the plan. The export had 136. Rather than quietly building 136 and moving on, it cross-checked the label counts against the design spec — raspberry-pi 95, python 77, minecraft 43 — found they matched the export exactly, and told me the 203 figure couldn't be right. It was my mistake, from a stale note.

**I caught the thing the tests couldn't.** After the theme went in, 124 automated checks passed. I opened the page and it looked nothing like the design — completely unstyled. The stylesheet was being served as an HTML document, because Jekyll had wrapped it in a page layout. It returned HTTP 200 at the right URL with a plausible file size, so every automated check was happy. The checks were reading the source file, not the built one. It took me two seconds to see and it would have shipped otherwise.

**I vetoed a fix that was correct but wrong.** Images broke on the staging URL, and the agent fixed it by rewriting every image reference in all 92 affected posts:

```markdown
![]({% raw %}{{ '/assets/img/2012/04/responsivedesign-mobile.png' | relative_url }}{% endraw %})
```

That works. It's also a permanent tax on writing every future post, to solve a problem that only exists on a temporary URL. I said no, and it moved the fix into the build step instead. Posts stayed as plain Markdown.

**And the loop runs both ways.** Three posts had genuinely broken indentation — not from the migration, broken in the original since 2013. The agent normalised what it could prove and refused those three, because Python itself couldn't work out the nesting. I fixed them by hand. It re-checked, and found my fix had flattened two other blocks I hadn't noticed. Three rounds before it was clean. I'd have shipped mine.

None of that is the agent being clever or me being clever. It's just that the failure modes are different, so between us we caught things neither would alone.

## Open source

The last benefit, and the one I didn't expect to care about as much as I do: the whole site is now public at [github.com/martinohanlon/stuffaboutcode](https://github.com/martinohanlon/stuffaboutcode).

Every post is a Markdown file. The theme is one stylesheet and about 200 lines of vanilla JavaScript — no framework, no npm. Push to the repo and GitHub Actions builds and deploys it. If you want to see how something here is done, you can just go and look, which feels right for a blog that has always been about showing people how things work.

Now I've just got to write something.
