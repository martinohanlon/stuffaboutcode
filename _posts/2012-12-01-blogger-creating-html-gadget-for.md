---
title: 'Blogger - Creating a HTML Gadget for Movember'
date: 2012-12-01 13:30:00 +00:00
tags: [social-networking]
redirect_from:
  - /2012/12/blogger-creating-html-gadget-for.html
---

Anyway, I was growing a Mo for [Movember](http://uk.movember.com/), its a great charity which encourages Men to grow a Mo (moustache) during the month of November, the aim of which is to raise vital funds and awareness for men’s health, specifically prostate cancer and testicular cancer.

**My Mo's**

![](http://static.movember.com/uploads/2011/profiles/110/714/11071424db02a0397a6d37bd24b4fa24-50a795d03a0ed-hero.jpg)![](http://static.movember.com/uploads/2011/profiles/874/0c8/8740c8575fb641c9fe2f7f16aba43035-50b348209c834-hero.jpg)![](http://static.movember.com/uploads/2011/albums/640/464/6404647b55502fd6ae351d093fa337b9-50ba02d5bf3ff-hero.jpg)

I decided to see if I could get some extra donations through my blog, not ever so hopeful, but I thought it was worth a go, so I created a HTML gadget on my blog, which would show a picture of me and my Mo and provide a link to donate to Movember, on the top right.

Firstly a BIG thank you to those people who did donate, I really wasn't expecting any and those that did donate where fantastically generous.

So to create a HTML gadget in blogger:

- login to the admin bit of blogger
- click layout on the left hand menu
- click "Add a gadget" where you want the gadget to go
- Scroll down or search till you find "HTML / Javascript Gadget" - this allows you to insert you own HTML code and have it displayed in the blogger gadget

![](/assets/img/2012/12/movember-html-gadget.png)

- Click on the +
- Give your gadget a title, in my case "Movember"
- Insert your HTML or Javascript code (my Movember HTML is below)

```html
<div>
<a href="http://mobro.co/martinohanlon">
<img src="http://static.movember.com/uploads/2011/profiles/874/0c8/8740c8575fb641c9fe2f7f16aba43035-50b348209c834-hero.jpg" alt="My Mo" />
</a><div style="font-style:italic;">"Im not growing this for fun!"<br /></div>
<div><a href="http://mobro.co/martinohanlon">http://mobro.co/martinohanlon</a></div>
<br />
<div>If everyone who visited my blog in November donated 10p, we would raise over £1000<br /></div>
<br />
<div>So maybe if you have found something useful today, and maybe Ive helped you solve a problem, why not <a href="http://mobro.co/martinohanlon">donate 10p</a> to raise vital funds for men’s health</div>
</div>
```

- Click save and that's it, a lovely new custom made gadget on your blog

![](/assets/img/2012/12/movember-gadget.png)

Its never too late to donate to Movember - [http://mobro.co/martinohanlon](http://mobro.co/martinohanlon)
