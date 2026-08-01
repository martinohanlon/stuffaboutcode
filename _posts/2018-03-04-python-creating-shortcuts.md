---
title: 'Python - Creating shortcuts'
date: 2018-03-04 08:20:00 +00:00
tags: [python]
redirect_from:
  - /2018/03/python-creating-shortcuts.html
---

I was recently working on the [mu](https://mu.readthedocs.io/) project (a Python IDE for beginners), which is super easy to install using pip, but there is no way to automate the creation of desktop and menu shortcuts.

This seemed like a really big miss, shortcuts are the usual way for people (and certainly beginners to launch applications).

So I set to creating a really simple way of creating shortcuts for Python applications.

Enter [shortcut](http://shortcut.readthedocs.io/en/latest/), a X platform (Windows, MacOS, Linux, Raspberry Pi) Python module for automatically creating shortcuts.

Its really simple to [install](http://shortcut.readthedocs.io/en/latest/#install) and [use](http://shortcut.readthedocs.io/en/latest/app.html):

```bash
pip3 install shortcut
shortcut name_of_app
```

It will find the location of the app and create desktop and menu shortcuts for it.

There is also a [Python API](http://shortcut.readthedocs.io/en/latest/api.html) which can be used to do the same:

```python
from shortcut import ShortCutter
s = ShortCutter()
s.create_desktop_shortcut("python")
s.create_menu_shortcut("python")
```

You will find documentation at [shortcut.readthedocs.io](http://shortcut.readthedocs.io/en/latest) and code at [github.com/martinohanlon/shortcut](https://github.com/martinohanlon/shortcut).
