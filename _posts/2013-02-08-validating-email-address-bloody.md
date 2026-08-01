---
title: 'Validating an email address (bloody apostrophe)'
date: 2013-02-08 08:49:00 +00:00
redirect_from:
  - /2013/02/validating-email-address-bloody.html
---

You know what really gets me angry, websites which don't validate email address properly! I have an apostrophe in my surname O'Hanlon and often employers will give me the email address similar to martin.o'hanlon@mycompany.com, all well and good a perfectly respectable email address, which is reflective of my name.

Then this happens:

![](/assets/img/2013/02/oracle-email.png)

*Oracle Account Registration*

This isn't just small company's and little custom website, this issue is prevalent on some BIG companies websites.

It all comes down to regular expressions, which are a standard way of defining and validating a format, and for years when you googled 'email address regular expression', and clearly a lot of people did because the problem is everywhere, you ended up with this:

```text
[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}
```

And its wrong! Its a simple email address regular expression which is missing all sorts of 'unusual' characters / & % and most annoying for me '.

If you want to be correct against the RFC definition of an email address you need this(!):

```text
(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08
```

```text
\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?
```

```text
:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-
```

```text
5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-
```

```text
z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0
```

```text
b\x0c\x0e-\x7f])+)\])
```

Although I would be happier, im sure a lot of the other Irish descendants, with this:

```text
[A-Z0-9.'_%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}
```

Bloody apostophe!

For more information and a lot more background about validating email addresses head over to [http://www.regular-expressions.info/email.html](http://www.regular-expressions.info/email.html)

28/2/2013 - Found another SiteCore

![](/assets/img/2013/02/sitecore-email.png)

14/06/2013 - And another, Prometric

![](/assets/img/2013/02/prometric.png)
