---
title: 'Raspberry Pi - Python - create podcast / RSS'
date: 2012-06-08 21:01:00 +01:00
tags: [python, raspberry-pi, rss]
redirect_from:
  - /2012/06/raspberry-pi-python-create-podcast-rss.html
---

Anyway as part of my [iPlayer personal podcast](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-bbc-iplayer-personal.html) solution I needed a way of creating an RSS feed. Python seemed like a logical choice given its a flexible and powerful scripting language and it comes ready on the Pi Debian distro. Even though I had never written a python script before!

**Create a podcast from a directory**
 I chose a really simple implementation, a python program that re-cursed the directory where the media files are stored and created an RSS xml file based on the content.

It only implements the base RSS specification, there are a number of tags for providing additional meta data, particularly for use with iTunes, but for my purposes this wasn't required. For more information about the RSS standard and podcasts see [http://www.podcast411.com/howto_1.html](http://www.podcast411.com/howto_1.html).

I also chose to output the xml as strings rather than using an XML parser, simply because it seemed like a significant overhead (mainly in terms of learning how) just to output a simple structure.

This script has only been tested for my requirements and its not really designed to have a tremendous amount of re-use, but feel free to adapt it to your needs.

**Python script - createRSSFeed.py**

```python
# import libraries
import os
import sys
import datetime
import time

# import constants from stat library
from stat import * # ST_SIZE ST_MTIME

# format date method
def formatDate(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

# get the item/@type based on file extension
def getItemType(fileExtension):
    if fileExtension == "aac":
        mediaType = "audio/mpeg"
    elif fileExtension == "mp4":
        mediaType = "video/mpeg"
    else:
        mediaType = "audio/mpeg"
    return mediaType

# constants
# the podcast name
rssTitle = "Podcast title"
# the podcast description
rssDescription = "Podcast description"
# the url where the podcast items will be hosted
rssSiteURL = "http://www.myurl.com/mypodcast"
# the url of the folder where the items will be stored
rssItemURL = rssSiteURL + "/iPlayerRadioDownloads"
# the url to the podcast html file
rssLink = rssSiteURL + "/index.html"
# url to the podcast image
rssImageUrl = rssSiteURL + "/logo.jpg"
# the time to live (in minutes)
rssTtl = "60"
# contact details of the web master
rssWebMaster = "me@me.com"

#record datetime started
now = datetime.datetime.now()

# command line options
#    - python createRSFeed.py /path/to/podcast/files /path/to/output/rss
# directory passed in
rootdir = sys.argv[1]
# output RSS filename
outputFilename = sys.argv[2]

# Main program

# open rss file
outputFile = open(outputFilename, "w")

# write rss header
outputFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
outputFile.write("<rss version=\"2.0\">\n")
outputFile.write("<channel>\n")
outputFile.write("<title>" + rssTitle + "</title>\n")
outputFile.write("<description>" + rssDescription + "</description>\n")
outputFile.write("<link>" + rssLink + "</link>\n")
outputFile.write("<ttl>" + rssTtl + "</ttl>\n")
outputFile.write("<image><url>" + rssImageUrl + "</url><title>" + rssTitle + "</title><link>" + rssLink + "</link></image>\n")
outputFile.write("<copyright>mart 2012</copyright>\n")
outputFile.write("<lastBuildDate>" + formatDate(now) + "</lastBuildDate>\n")
outputFile.write("<pubDate>" + formatDate(now) + "</pubDate>\n")
outputFile.write("<webMaster>" + rssWebMaster + "</webMaster>\n")

# walk through all files and subfolders
for path, subFolders, files in os.walk(rootdir):

    for file in files:

        # split the file based on "." we use the first part as the title and the extension to work out the media type
        fileNameBits = file.split(".")
            # get the full path of the file
            fullPath = os.path.join(path, file)
            # get the stats for the file
            fileStat = os.stat(fullPath)
            # find the path relative to the starting folder, e.g. /subFolder/file
            relativePath = fullPath[len(rootdir):]

        # write rss item
        outputFile.write("<item>\n")
        outputFile.write("<title>" + fileNameBits[0].replace("_", " ") + "</title>\n")
        outputFile.write("<description>A description</description>\n")
        outputFile.write("<link>" + rssItemURL + relativePath + "</link>\n")
        outputFile.write("<guid>" + rssItemURL + relativePath + "</guid>\n")
        outputFile.write("<pubDate>" + formatDate(datetime.datetime.fromtimestamp(fileStat[ST_MTIME])) + "</pubDate>\n")
        outputFile.write("<enclosure url=\"" + rssItemURL + relativePath + "\" length=\"" + str(fileStat[ST_SIZE]) + "\" type=\"" + getItemType(fileNameBits[len(fileNameBits)-1]) + "\" />\n")
        outputFile.write("</item>\n")

# write rss footer
outputFile.write("</channel>\n")
outputFile.write("</rss>")
outputFile.close()
print "complete"
```

**Running the script**
 The script expects 2 parameters:

- The path where the media files are stored
- The path of the output rss file

```bash
python createRSSFeed.py /path/to/media/files /path/to/output/RSSFile.rss
```

Update - I came across some problems when there was escape characters in the xml, so had to write a function to [encode text to make it xml safe](http://stuffaboutcode.blogspot.co.uk/2012/06/python-encode-xml-escape-characters.html).

Update - Dan Goff sent me on a [modified version of this program](http://www.stuffaboutcode.com/2012/09/python-create-rss-podcast-of-mp3-files.html) which uses the mutagen library to include data from ID3 tags in mp3 files
