---
title: 'Raspberry Pi - Google Drive & Grive'
date: 2013-03-04 16:25:00 +00:00
tags: [raspberry-pi]
redirect_from:
  - /2013/03/raspberry-pi-google-drive-grive.html
---

I use [google drive](http://drive.google.com/) a lot and I wanted to use my raspberry pi to automatically backup some of my more important files (i.e. documents and pictures) to google's cloud.

Now google hasn't released a [google drive client for linux](http://productforums.google.com/forum/#!topic/drive/j_SmC6bMsEo%5B1-25-false%5D), as yet, but there is a really good open source linux client called grive which allows you to sync with google drive.

**Install grive**
 I got most of this info from, [http://www.lbreda.com/grive/installation](http://www.lbreda.com/grive/installation).

***Install dependencies***
 Use apt-get to install grive's dependencies, I already had some of these installed, but it won't hurt to re-run if your not sure.

```bash
sudo apt-get install git cmake build-essential libgcrypt11-dev libjson0-dev libcurl4-openssl-dev libexpat1-dev libboost1.50-all libboost-filesystem-dev libboost-program-options-dev binutils-dev libyajl-dev
```

***Get the grive source code***

```bash
cd ~
git clone git://github.com/Grive/grive.git
```

***Compile grive***

```bash
cd grive
cmake .
make
```

Wait a while for it to compile (10-20 mins)

***Setup your google drive folder and authenticate***
 You need to create a directory which grive will sync Google Drive with; anything in Google Drive will be synced into this folder and anything in this folder will be synced to Google Drive.

```bash
mkdir ~/googleDrive
```

In order to make grive work it needs to be in your google drive, so copy the grive executable to the google drive directory:

```bash
cp ~/grive/grive/grive ~/googleDrive
```

Authenticate grive to work with your Google Drive account.

```bash
cd ~/googleDrive
./grive -a
```

Grive will now give you a URL and ask you to provide an access code. Cut and paste the URL into a browser, if your not logged in to google, login, and it will present you with an access code, cut and paste this access code into grive.

NOTE - In order to run grive, you must be in the google drive directory, for some reason if you are not, grive doesn't work and moans about having to authenticate even if you have!

**Test**
 Grive can be run in a test mode, which will do everything other than uploading / downloading.

```bash
./grive --dry-run
```

**Run**

```bash
./grive
```

Once completed, your ~/googleDrive directory should now hold a copy of everything which is in your google drive. Also any files you put in your googleDrive directory will also get synced to google drive.

**Backup other files and folders**
 I wanted to backup other files and folders and didn't want to put them in my ~/googleDrive folder so I did this by using symbolic links. Using symbolic links we can make it appear that a file or folder from a different location is in the google drive folder and as such will get synced to google drive. I used this technique to create a link to my Pictures folder which is stored on my NAS drive, that way all my pictures are backed up to google drive.

```text
ln -s /path/to/my/pictures ~/googleDrive/pictures
```

For more [information on ln command](http://linux.about.com/od/commands/l/blcmdl1_ln.htm).

**Restricting bandwidth using trickle**
 One of the challenges I found in backing up my files to google drive was a simple one of bandwidth, or more accurately a lack of bandwidth. When grive first ran, it uploaded a LOT of data to google drive and totally saturated by broadband (particularly as upload speeds are generally a lot less than download).

I came across a great utility called "trickle" which allows you to specify a maximum upload and download speed for any command, see [http://www.tuxradar.com/content/control-your-bandwidth-trickle](http://www.tuxradar.com/content/control-your-bandwidth-trickle) for more info.

***Install trickle***

```bash
sudo apt-get install trickle
```

***Run grive using trickle***
 The following command will specify a maximum download (-d) and upload (-u) limit for grive of 50k.

```bash
cd ~/googleDrive
trickle -d 50 -u 50 ./grive
```

**Schedule**
 I then chose to schedule grive to run once a week, using cron, thereby automating my file backup to google drive.
