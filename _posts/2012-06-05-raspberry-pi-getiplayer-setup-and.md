---
title: 'Raspberry Pi - get_iplayer - setup and running'
date: 2012-06-05 21:56:00 +01:00
tags: [get-iplayer, raspberry-pi]
redirect_from:
  - /2012/06/raspberry-pi-getiplayer-setup-and.html
---

Anyway... Im using [get_iplayer](http://www.infradead.org/get_iplayer/html/get_iplayer.html) as part of my solution to get my [Raspberry Pi to create and distribute a podcast of the stuff I want to listen to / watch](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-bbc-iplayer-personal.html), but there are so many options, settings and modes I thought it a good idea to write them down not only for my benefit but for those that might want to re-create.

For instructions on how to install get_iplayer, check out this [blog](http://stuffaboutcode.blogspot.co.uk/2012/05/raspberry-pi-downloading-from-bbc.html).

**SWF Verification**
 In June 2013, BBC iPlayer changed to use SWF Verification (see this [post](http://makingtechnologyeasier.blogspot.co.uk/2013/06/getiplayer-rtmpreadpacket-failed-to.html) for more information), If you haven't already you need to setup the certificate by running.

```bash
./get_iplayer --prefs-add --rtmp-tv-opts="--swfVfy http://www.bbc.co.uk/emp/releases/iplayer/revisions/617463_618125_4/617463_618125_4_emp.swf"
```

**Options**
 get_iplayer has 2 methods of telling it what options you want to use:

Passing them on the command line

```bash
./get_iplayer --output="/path/to/output/to" --type=tv,radio --etc
```

Setting preferences which get_iplayer then uses as defaults using the -pref--add command

```bash
./get_iplayer --prefs-add --output="/path/to/output/to"
```

I found setting preferences to be really useful otherwise every time you want to run get_iplayer your command is going to be VERY long.

The options I set up were:

- set the default types to search as tv and radio
- set the cache expiry time to 1 hour (its 4 by default)
- output downloads to a specific directory
- output radio downloads to a specific directory
- output to series sub-directories (e.g. all episodes of one series in one sub-directory)
- format file-names to use a simpler naming structure and include the series and episode as S00E00

```bash
# set default type to tv & radio
./get_iplayer --prefs-add --type=tv,radio
# set cache expiry to 1 hour
./get_iplayer --add-prefs --expiry=3600
# set output directory
./get_iplayer --prefs-add --output="/default/output/path"
# set specific output directory for radio
./get_iplayer --prefs-add --outputradio="/output/path/for/radio"
# you can also set specific output directory for tv with
./get_iplayer --prefs-add --outputtv="/output/path/for/tv"
# set to use sub-directories
./get_iplayer --prefs-add --subdir
# set file name format
./get_iplayer --prefs-add --file-prefix="<nameshort>-<episodeshort>-<senum>-<pid>
```

Check out the [get_iplayer documentation](http://linuxcentre.net/getiplayer/documentation) for more info on settings.

NOTE - preferences are user specific, so if you use get_iplayer as root, remember to set preferences logged in as root or use sudo.

**Web User Interface**

I am using get_iplayer's web user interface which is really easy to use and can be run with a simple command, allowing you to search, queue and record programmes from a web browser.

```text
perl /installed/path/get_iplayer.cgi --port=1935 --get_iplayer=/installed/path/get_iplayer
```

If you are going to run the Web UI as a daemon (background task) you can do so by adding an & to the end of the command, but it would also be worth logging to a file as the applicatio produces a LOT of output messages.

```text
perl /installed/path/get_iplayer.cgi --port=1935 --get_iplayer=/installed/path/get_iplayer 2>> /logfile/path/logfile.log &
```

**Running PVR**

I am using get_iplayer's PVR functions to allow me to record complete series of programmes. Using the Web UI, I can search for a programme then use the 'queue' or 'add series' command, then when get_iplayer is called using the --pvr option is searches for all my series' or queued downloads and downloads them all at once and by scheduling this to run periodically I could automate the download process.

```text
/installed/path/get_iplayer --pvr
```
