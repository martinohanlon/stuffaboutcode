---
title: 'Raspberry Pi - Raspbian Lighttpd Mime Types'
date: 2012-07-28 07:41:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/07/raspberry-pi-raspbian-lighttpd-mime.html
---

Anyway Ive been having a few problems with mime types and lighttpd, this has all come after I migrated my [Raspberry Pi - Personal Podcast](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-bbc-iplayer-personal.html) solution from Debian squeeze to Raspbian distributions and the 'differences' between the versions.

Mime types are assigned to file extensions (e.g. .html = text/html) and are loaded through the lighttpd's config file (sort of), specifically:

```text
/etc/lighttpd/lighttpd.conf
```

includes a script

```text
include_shell "/usr/share/lighttpd/create-mime.assign.pl"
```

which uses a file of mime types and file extensions

```text
/etc/mime.types
```

to make the associations!

All the mime types and associated file extensions are stored in this file as a table and if you need to create, modify or remove them its as simple as modifying this file.

```bash
sudo nano /etc/mime.types
```

The mime types are stored as text, with mime types to file extension(s):

```text
audio/mpeg                   mpga mpega mp2 mp3 m4a aac
text/html                    html htm shtml
video/mp4                    mp4
text/rtf
```

The issue I experienced was that Debian Squeeze and Raspbian distributions install different versions of the mime.types file.

I was specifically interested in the application/rss+xml mime type as without it browsers wouldn't recognise an rss (podcast) feed, in Debian Squeeze the mime mapping was as expected:

```text
application/rss+xml          rss
```

However in Raspbian it was:

```text
application/x-rss+xml        rss
```

[Wikipedia's page on mime types](http://en.wikipedia.org/wiki/Internet_media_type) told me that the **x** meant "Types or subtypes that begin with x- are non-standard (they are not registered with IANA)". Now the application/rss+xml isn't registered with IANA so it is technically correct that it should be x-rss+xml but not very helpful because all the browsers I tested only identify rss+xml and why this change was made between versions is a mystery.
