---
title: 'Raspberry Pi - Error installing lighttpd - fixed!'
date: 2012-05-31 08:44:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/05/raspberry-pi-error-installing-lighttpd.html
---

Anyway... I want to serve up from simple content over the web from my Raspberry Pi, so I thought, I know the tool for that - [lighttpd](http://www.lighttpd.net/)(aka lighty)!

Unfortunately when I tried to install it I was faced with an error (pretty unusual in my experience of using apt-get) which stated:

```text
chown: invalid group: `www-data:www-data'

dpkg: error processing lighttpd (--configure):

subprocess installed post-installation script returned error exit status 1
```

How annoying, anyway a little bit of research suggested that the group www-data doesn't exist on the Raspberry Pi distro of Debian, and hence why it was failing. A pretty easy fix - add the group "www-data" and re-run the install.

```bash
sudo groupadd www-data

sudo apt-get install lighttpd
```

That was it, worked like a charm!
