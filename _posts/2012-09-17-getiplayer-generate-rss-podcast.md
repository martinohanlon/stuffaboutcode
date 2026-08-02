---
title: 'get_iplayer - generate an RSS / podcast'
date: 2012-09-17 21:44:00 +01:00
tags: [get-iplayer, python, raspberry-pi, rss]
redirect_from:
  - /2012/09/getiplayer-generate-rss-podcast.html
---

Anyway, Ive been improving the [BBC iPlayer custom podcast](/posts/raspberry-pi-bbc-iplayer-personal/) solution I created for the Raspberry Pi by making it more robust and re-factoring the code to introduce some 're-usability' and future proofing.

A big area of change is the python program I originally created which creates an RSS (podcast) feed; this program recursed a directory path and created the xml file based on some hard-coded constants in the code such as "rssURL".

So I created a re-usable component for creating RSS feeds from [get_iplayer](http://www.infradead.org/get_iplayer/html/get_iplayer.html) which I have dubbed "[get_iplayer_genrss](/getiplayergenrss/)" which reads the [get_iplayer](http://www.infradead.org/get_iplayer/html/get_iplayer.html) download_history file and by using parameters passed in such as URL where downloads are e.g. "http://server/path/to/downloads" creates an RSS file based on its contents.

It supports functions such as:

- Days in the past - only include in the RSS, downloads from the past \[so many\] days
- Media type - only include downloads with a specific media type (tv, radio, etc)
- Alternative directories - search alternative directories for the download, useful if the download has been copied to a different location

I have 'open sourced' the project and the code is being managed [github](https://github.com/martinohanlon/get_iplayer_genrss.git)[https://github.com/martinohanlon/get_iplayer_genrss.git](https://github.com/martinohanlon/get_iplayer_genrss.git) and would welcome any contributions, comments or feedback.

I am currently using get_iplayer_genrss to create rss feeds for radio shows which I download to my mobile phone and for tv shows which I use in XBMC.

For instructions on [installation and usage](/getiplayergenrss/) see this [page](/getiplayergenrss/).
