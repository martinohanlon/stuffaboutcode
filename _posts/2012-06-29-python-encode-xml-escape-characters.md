---
title: 'Python - encode XML escape characters'
date: 2012-06-29 08:26:00 +01:00
tags: [python, xml]
redirect_from:
  - /2012/06/python-encode-xml-escape-characters.html
---

Anyway as part of my [iPlayer podcast project](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-bbc-iplayer-personal.html) I need to [create an RSS feed](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-python-create-podcast-rss.html),which is nothing more complicated than a XML file which conforms to a specific schema. Its a pretty simple schema so I decided rather than using an XML parser, I would just write strings to a file - this created a problem, I need to encode any escape characters which appeared in the text, o

therwise the xml created was invalid and most RSS readers wouldn't accept it.

There are 5 escape characters which need to be encoded:

```xml
"      ->     &quot;
'      ->     &apos;
<      ->     &lt;
>      ->     &gt;
&      ->     &amp;
```

So I created a really simple python function which I added to my create RSS feed program.

```python
# encode xml escape characters
def encodeXMLText(text):
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text
```

Which is called by passing the text I need to make xml safe:

```text
xmlText = encodeXMLText("Some text with escape characters & " ' < > you want to make xml safe")
```
