---
title: 'Responsive web design example and source code'
date: 2012-04-24 22:38:00 +01:00
tags: [html]
redirect_from:
  - /2012/04/responsive-web-design-example-and-code.html
---

Anyway... I recently posted a blog about a building a single page website which used media queries to change layout in real-time between a desktop & mobile format. Click [here](http://stuffaboutcode.blogspot.co.uk/2012/04/responsive-design-media-rules-and-ie9.html) to read it.

I few people have contacted me to ask if I would provide a link & source code for the page, so here it is:

- [Webpage](http://www.gooffpiste.com/ideas/responsive-design/index.html)
- [Sourcecode](http://www.gooffpiste.com/ideas/responsive-design/responsive-design-sourcecode.zip)

Fyi - I've made a couple of changes in the last few days.

**Adding a meta tag to enable viewport in mobile browsers**

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

**Adding a condition to default the layout to desktop if the browser was IE8 or below**

```html
<!--[if lte IE 8]>
       <link rel="stylesheet"
            href="browser-layout.css"
            type="text/css" />
<![endif]-->
```
