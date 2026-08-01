---
title: 'Python - Create RSS / Podcast of MP3 files'
date: 2012-09-07 15:32:00 +01:00
tags: [python, rss, xml]
redirect_from:
  - /2012/09/python-create-rss-podcast-of-mp3-files.html
---

Anyway, a nice guy called [Dan Goff](http://www.blogger.com/profile/14848795091299473717) left a comment on my post about creating a [RSS / podcast file using Python](http://www.stuffaboutcode.com/2012/06/raspberry-pi-python-create-podcast-rss.html) letting me know that he had taken my code template and modified it to use the Mutagen library to pick up certain values from the ID3 tags inside MP3 files.

*Dan says:*

- *I'm populating the title for each entry and the description directly from the ID3 tags provided using the Mutagen library.*
- *I ran into an issue with my podcatching software, because the files are only tagged with the year and not a full date, so part of the code is to take a fully-formatted date string and write it back to the file so that it is listed correctly when my software "downloads" the file from the feed.*
- *Also, I ran into an issue with some Unicode characters in the description (mostly an ellipsis), so I took the quick-and-dirty (and probably not exactly correct) route and just converted everything in the description field to ASCII before writing it out to the feed.*

Dan has also kindly agreed to let me share his code:

```python
# update
environment to handle Unicode

PYTHONIOENCODING="utf-8"

# import libraries

import os

import sys

import datetime

import time

# import constants from stat library

from stat import * # ST_SIZE ST_MTIME

# import ID3 tag reader

from mutagen.id3 import ID3, ID3TimeStamp, TDRC

from time import strptime, strftime

# format date method

def formatDate(dt):

    return dt.strftime("%a, %d %b %Y
%H:%M:%S +0000")

# get the item/@type based on file extension

def getItemType(fileExtension):

    if fileExtension ==
"aac":

         mediaType =
"audio/mpeg"

    elif fileExtension ==
"mp4":

         mediaType =
"video/mpeg"

    else:

         mediaType =
"audio/mpeg"

    return mediaType

# constants

# the podcast name

rssTitle = "The podcast title"

# the podcast description

rssDescription = "The podcast description"

# the url where the podcast items will be hosted

rssSiteURL = http://xxx.xxx.xxx.xxx

# the url of the folder where the items will be stored

rssItemURL = rssSiteURL + "/Podcasts"

# the url to the podcast html file

rssLink = rssSiteURL #+ ""

# url to the podcast image

rssImageUrl = rssSiteURL #+ "/logo.jpg"

# the time to live (in minutes)

rssTtl = "60"

# contact details of the web master

rssWebMaster = "me@me.com"

#record datetime started

now = datetime.datetime.now()

# command line options

#    - python createRSFeed.py
/path/to/podcast/files /path/to/output/rss

# directory passed in

rootdir = sys.argv[1]

# output RSS filename

outputFilename = sys.argv[2]

# Main program

# open rss file

outputFile = open(outputFilename, "w")

# write rss header

outputFile.write("<?xml version=\"1.0\"
encoding=\"UTF-8\" ?>\n")

outputFile.write("<rss version=\"2.0\">\n")

outputFile.write("<channel>\n")

outputFile.write("<title>" + rssTitle +
"</title>\n")

outputFile.write("<description>" + rssDescription +
"</description>\n")

outputFile.write("<link>" + rssLink +
"</link>\n")

outputFile.write("<ttl>" + rssTtl +
"</ttl>\n")

outputFile.write("<image><url>" + rssImageUrl +
"</url><title>" + rssTitle +
"</title><link>" + rssLink +
"</link></image>\n")

outputFile.write("<copyright>mart
2012</copyright>\n")

outputFile.write("<lastBuildDate>" + formatDate(now) +
"</lastBuildDate>\n")

outputFile.write("<pubDate>" + formatDate(now) +
"</pubDate>\n")

outputFile.write("<webMaster>" + rssWebMaster +
"</webMaster>\n")

# walk through all files and subfolders

for path, subFolders, files in os.walk(rootdir):

    for file in files:

        # split the file based on
"." we use the first part as the title and the extension to work out
the media type

        fileNameBits =
file.split(".")

        # get the full path of the
file

        fullPath = os.path.join(path,
file)

        # get the stats for the
file

        fileStat =
os.stat(fullPath)

        # find the path relative to the
starting folder, e.g. /subFolder/file

        relativePath =
fullPath[len(rootdir):]

      # Extract ID3 info

      #title

      audio = ID3(fullPath)

      fileTitle =
audio["TIT2"].text[0]

      #date

      datePos =
fileTitle.find(":")

      fileDate =
fileTitle[(datePos+2):]

      fileDate = time.strptime(fileDate,
"%B %d, %Y")

      #correct date format in the file's
ID3 tag

      fileTS =
ID3TimeStamp(time.strftime("%Y-%m-%d", fileDate))

      audio['TDRC'] = TDRC(0,
[fileTS])

      #description

      fileDesc =
audio["COMM::'eng'"].text[0]

      fileDesc = fileDesc.encode('ascii',
'ignore') #converts everything to ASCII prior to writing out

      audio.save()

        # write rss item

outputFile.write("<item>\n")

        #outputFile.write("<title>"
+ fileNameBits[0].replace("_", " ") +
"</title>\n")

      outputFile.write("<title>"
+ fileTitle + "</title>\n")

#outputFile.write("<description>A
description</description>\n")

outputFile.write("<description>" + fileDesc + "</description>\n")

outputFile.write("<link>" + rssItemURL + relativePath +
"</link>\n")

outputFile.write("<guid>" + rssItemURL + relativePath +
"</guid>\n")

#outputFile.write("<pubDate>" +
formatDate(datetime.datetime.fromtimestamp(fileStat[ST_MTIME])) +
"</pubDate>\n")

      outputFile.write("<pubDate>"
+ time.strftime("%Y-%m-%d", fileDate) +
"</pubDate>\n")

outputFile.write("<enclosure url=\"" + rssItemURL +
relativePath + "\" length=\"" + str(fileStat[ST_SIZE]) +
"\" type=\"" +
getItemType(fileNameBits[len(fileNameBits)-1]) + "\"
/>\n")

outputFile.write("</item>\n")

# write rss footer

outputFile.write("</channel>\n")

outputFile.write("</rss>")

outputFile.close()

print "complete"
```

Thanks again to Dan.
