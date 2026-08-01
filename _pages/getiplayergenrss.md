---
title: 'get_iplayer_genrss'
date: 2012-11-08 22:47:00 +00:00
redirect_from:
  - /p/getiplayergenrss.html
---

get_iplayer_genrss is an open source utility for creating rss (podcast) feeds from your [get_iplayer](http://www.infradead.org/get_iplayer/html/get_iplayer.html) download history.

get_iplayer is a really powerful BBC iPlayer search and download program, which also has some great PVR functionality.

Used together, they can automatically push your favourite BBC tv or radio programs to your phone, tablet, browser, media centre, iTunes or anything else than can read rss feeds!

get_iplayer_genrss reads the get_iplayer download_history file and by using parameters passed in such as URL where downloads are e.g. "http://server/path/to/downloads" creates an RSS file based on its contents.

It supports functions such as:

- Days in the past - only include in the RSS, downloads from the past \[so many\] days
- Media type - only include downloads with a specific media type (tv, radio, etc)
- Alternative directories - search alternative directories for the download, useful if the download has been copied to a different location

The code is being managed at [github](https://github.com/martinohanlon/get_iplayer_genrss.git), the repository [https://github.com/martinohanlon/get_iplayer_genrss.git](https://github.com/martinohanlon/get_iplayer_genrss.git) and I would welcome any contributions, comments or feedback.

**Install**

```bash
wget https://github.com/downloads/martinohanlon/get_iplayer_genrss/get_iplayer_genrss-0.2.tar.gz

tar -xf get_iplayer_genrss-0.2.tar.gz

cd get_iplayer_genrss
```

**Usage:**

```text
python get_iplayer_genrss.py -h

usage: get_iplayer_genrss.py [-h]
                             [-a ALTDOWNLOADDIR]
                             [-m MEDIATYPE]
                             [-v]
                             outputRSSFilename
                             numberOfPastDays
                             rssTitle
                             rssDescription
                             rssHTMLPageURL
                             rssDownloadsURL
                             rssImageURL
                             rssTTL
                             rssWebMaster

Create RSS feed (podcast) from get_iplayer's download history

positional arguments:
  outputRSSFilename     The location to output the RSS file
  numberOfPastDays      The number of days in the past to
                        include in the RSS
  rssTitle              Title of the rss feed
  rssDescription        Description of the rss feed
  rssHTMLPageURL        URL to the rss feed HTML page
                        www.example.com/rss/index.html
  rssDownloadsURL       URL where the downloads will be
                        located,
                        wwww.example.com/rss/downloads/
  rssImageURL           URL of the rss image
  rssTTL                Time to live in minutes for the rss
                        feed e.g 60 minutes
  rssWebMaster          RSS feed web master contact details
                        e.g. me@me.com

optional arguments:
  -h, --help            show this help message and exit
  -a ALTDOWNLOADDIR, --altDownloadDir ALTDOWNLOADDIR
                        An alternative download directory as
                        apposed to that in the download_history,
                        useful if the downloads have been copied
                        to another location; specify multiple by
                        seperating with a comma /path1,path2
  -m MEDIATYPE, --mediaType MEDIATYPE
                        Filter by get_iplayer media type (tv,
                        radio) ; specify multile values by
                        seperating with a comma tv,radio
  -v, --verbose         Output verbose statements
```

get_iplayer_genrss needs to be run as the same user which is used to run get_iplayer as get_iplayer creates download histories per user.

**Example:**

If your webserver is on IP address http://192.168.1.100 and your iplayer downloads are in the virtual directory http://192.168.1.100/iPlayerDownloads and you want to create and RSS file in the /var/www directory of the last 30 days downloads:

```bash
./get_iplayer_genrss.py -v /var/www/get_iplayer_feed.rss 30 "The rss feed title" "A description of the rss feed" "http://192.168.1.100/rss_feed_html_file.html" "http://192.168.1.100/iPlayerDownloads/" "http://192.168.1.100/rss_feed_logo.jpg" 60 "me@myemail.com (Mr My Name)"
```

**Alternative directories**

If you have moved the downloads from the original get_iplayer download directory you can specify an alternative directory using the -a option:

```bash
./get_iplayer_genrss.py -v -a /path/where/downloads/are /var/www/get_iplayer_feed.rss 30 "The rss feed title" "A description of the rss feed" "http://192.168.1.100/rss_feed_html_file.html" "http://192.168.1.100/iPlayerDownloads/" "http://192.168.1.100/rss_feed_logo.jpg" 60 "me@myemail.com (Mr My Name)"
```

Multiple alternative directories can be specified by separating them with a comma:

```text
-a /path/where/downloads/are1,/path/where/downloads/are2
```

**Media Types**

If you only want to include tv program's in the RSS feed you can specify a media type using the -m option:

```bash
./get_iplayer_genrss.py -v -m tv /var/www/get_iplayer_feed.rss 30 "The rss feed title" "A description of the rss feed" "http://192.168.1.100/rss_feed_html_file.html" "http://192.168.1.100/iPlayerDownloads/" "http://192.168.1.100/rss_feed_logo.jpg" 60 "me@myemail.com (Mr My Name)"
```

Multiple media types can be specified by separating them with a comma:

```text
-m tv,radio
```

**Currently in Alpha...**

So far get_iplayer_genrss has been tested on debian linux and get_iplayer 2.82.

Please let me know if you have used and tested the program on a different setup or if you have problems.
