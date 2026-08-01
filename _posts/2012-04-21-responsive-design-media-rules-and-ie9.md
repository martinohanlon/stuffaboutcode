---
title: 'Responsive design, Media queries and IE9'
date: 2012-04-21 12:07:00 +01:00
tags: [html]
redirect_from:
  - /2012/04/responsive-design-media-rules-and-ie9.html
---

## Getting media queries working with IE9!

Anyway... I have had a complete nightmare getting media queries with IE9 and its been something of a battle to get it working...

It all started when I was buying train tickets the other day on[www.firstgreatwestern.co.uk](http://http//www.firstgreatwestern.co.uk/)and noticed a really great implementation of [responsive web design](http://en.wikipedia.org/wiki/Responsive_Web_Design) (I'm paraphrasing but one website, different layouts for desktop, mobile, tablet changed dynamically using CSS3 media queries) and I thought I gotta find out how that works.

I created a really simple webpage with a banner, navigation, main content, additional content and footer layout, I then created a CSS to apply a style and typical desktop layout (fixed window, dual column, etc).

![](/assets/img/2012/04/responsivedesign-desktop.png)

I then created a second CSS which would apply a typical mobile layout (100% width, single column, left justified, key content only).

![](/assets/img/2012/04/responsivedesign-mobile.png)

So responsive design is all about making these transitions in real-time as the environment changed, and this was what I was impressive with on the first great western website, when I re-sized the browser it suddenly started showing a different view; this was my task, make the browser change between these view automatically using [CSS3 media queries](http://www.w3.org/TR/css3-mediaqueries/).

In order to do this I started by splitting my 2 CSS's into 3:

- base - the styles that where consist amongst the 2 layouts (fonts, colors, etc)
- desktop layout - the styles which made the page look like a desktop page (floats, text alignment, etc)
- mobile layout - as above but for mobile

I then changed my html page to use media queries to select the right layout CSS based on screen width.

```html
<link rel="stylesheet"

    href="base.css"

    type="text/css" />

<link rel="stylesheet"

    href="mobile-layout.css"

    type="text/css"

    media="all and (max-width:499px)" />

<link rel="stylesheet"

    href="desktop-layout.css"

    type="text/css"

    media="all and (min-width:500px)" />
```

The media queries are really simple and basically say for **all** media types (screen, print, etc) where the screen width is up to 499px apply the mobile-layout.css and where the screen width is over 500px apply the desktop-layout.css.

Success - I now had a webpage which dynamically changed its layout based on the screen size... As long as I used **Chrome**or **Firefox**.... Try as I might I could not get it working in **IE**; now I already knew media queries only worked in IE9 and that they wouldn't work if the browser was compatibility mode, but I was using IE9 and it wasn't in compatibility mode. Arghhhh.

It took me a VERY long time to work out what I had done wrong. To explain, I wrote this prototype on the train to London, using my netbook, which doesn't have a web editor or development environment installed so I hand crafted the code in notepad and opened the files direct in the browser, and I hadn't included a very important line at the top of my html.

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
```

I hadn't told Internet Explorer what type of document it was, and as it was getting the file from the file system, not a webserver its seems it wasn't prepared to decided what it was either; unlike Chrome of Firefox.

So the moral is, always include your doctype as it seem IE is becoming a stickler for standards!

The prototype can be viewed [here](http://www.gooffpiste.com/ideas/responsive-design/index.html) just open it and try re-sizing the browser.
