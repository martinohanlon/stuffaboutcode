---
title: 'Change Blogger''s "Cookie Consent" bar'
date: 2015-07-28 11:52:00 +01:00
tags: [html]
redirect_from:
  - /2015/07/change-bloggers-cookie-consent-bar.html
---

If like me you are a user of blogger you will have no doubt notice that Google have kindly added a cookie consent message to your blog.

![](/assets/img/2015/07/cookieconsent.jpg)

You may have also seen the announcement when signing into the blogger

![](/assets/img/2015/07/cookieannouncement.jpg)

Leading you to [here](https://support.google.com/blogger/answer/6253244?p=eu_cookies_notice&hl=en&rd=1) to find about more information, including details on how to change the cookie consent bar to be appropriate for your blog.

If you want to change the values in the pop-up bar you can do so by adding a \<script> tag into your templates \<head>.

Log into Blogger, select Template from the menu and choose "Edit HTML" under the template.

In between the \<head> and \</head> tags you need to add a script tag and set a variable called "cookieOptions" which contains a json data e.g.:

```html
<script>cookieOptions = {"msg": "This website uses cookies to ensure you get the best experience", "link": "http://www.stuffaboutcode.com/p/about.html", "close": "Ok", "learn": "More" };</script>
```

Will change the bar to:

![](/assets/img/2015/07/cookieconsentnew.jpg)

The tags all change particular elements of the bar:

- msg = the message displayed in the box
- link = the url which clicking "Learn More" will redirect too
- learn = the text in the "Learn More" button
- close = the text in the "Got it" button

Note - the official [page](https://support.google.com/blogger/answer/6253244?p=eu_cookies_notice&hl=en&rd=1) says the "msg" tag is actually "message", this is incorrect, changing "message" wont affect it.

You don't have to change all the elements, if you just wanted to change the message you could use:

```html
<script>cookieOptions = {"msg": "This website uses cookies to ensure you get the best experience"};</script>
```

and all the other elements would remain the same.

You can also disable the bar setting cookieChoices to a blank json document using:

```html
<script>cookieChoices = {};</script>
```
