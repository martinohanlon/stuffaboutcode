---
title: 'Raspberry Pi - Auto Backups'
date: 2012-08-07 17:19:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/08/raspberry-pi-auto-backups.html
---

Anyway, I keep buggering my raspberry pi up, very annoying but inevitable when your experimenting, so I had to look at a way of backing up my Pi's SD card, so in the event of a failure I could restore from a stable copy. Im also a lazy toe rag (although I prefer the term busy), so something as difficult as shutting down the pi, pulling the SD card out, putting it into a PC and taking a copy just wasn't going to work; I needed an automatted backup process that I didn't have to think about.

This turned out to be surprisingly easy providing your Pi is connected to a NAS drive or has a usb disk hanging off it. If you want more info about [connecting to a NAS](http://stuffaboutcode.blogspot.co.uk/2012/05/raspberry-pi-connect-nas-windows-share.html), see this [post](http://stuffaboutcode.blogspot.co.uk/2012/05/raspberry-pi-connect-nas-windows-share.html).

I used the linux dd command to make an image of the SD card, which I then schedule to run using cron.

I took a backup of the SD card using dd referencing the physical disk directory /dev/mmcblk0 and a location on my NAS drive. I doesn't have to be a NAS drive but, obviously, it does need to be location not on the SD card, so an external USB drive should work just as well.

```bash
sudo dd if=/dev/mmcblk0 of=/path/to/NAS/drive/raspberryPiSDCardBackup.img
```

Caution - be careful using the dd command, make sure you get the right syntax, particularily the **if** and **of** options, get them the wrong way round and your gonna need the backup you haven't taken!

Depending on the size of your SD card and speed of the external drive you are connecting too, this will take a little time, but when complete it should have created a .img file which is the same size as the total size of your sd card e.g. if you have an 8gb sd card you will end up with an 8gb image regardless of how much capacity is actually used.

I also stop services which run in the background (for me these are lighttpd and noip) before starting the backup and restarted them when finished to minimise the risk of taking a backup mid way through an update to the SD card. As I also run other scheduled jobs using cron so I also suspend the cron service, so that other schedules jobs don't run while the backup is.

I created a script to do this called runSDCardBackup.sh

```bash
nano runSDCardBackup.sh
```

```bash
sudo /etc/init.d/lighttpd stop
sudo /etc/init.d/noip stop
sudo /etc/init.d/cron stop
sudo dd if=/dev/mmcblk0 of=/path/to/NAS/drive/raspberryPiSDCardBackup.img
sudo /etc/init.d/cron start
sudo /etc/init.d/lighttpd start
sudo /etc/init.d/noip start
```

Make the script executable:

```bash
sudo chmod +x runSDCardBackup.sh
```

I then scheduled this job using cron and that was it, it runs once a week on a monday morning at 2:30am.

Run crontab using the -e option for edit:

```bash
sudo crontab -e
```

Adding the following line to the bottom of the file, then using Ctrl X to save:

```text
30 2 * * 1 /home/pi/runSDCardBackup.sh > /home/pi/SDCardBackup.log 2>&1
```

The first part "30 2 \* \* 1" is in the format "minute hour dayOfMonth Month dayOfWeek" tells cron to run when the minutes on the internal clock equal 30, the hour equals 2, for any day in the month, for any month when the day of the week is Monday.

The second part is the command which outputs the results to a log file.

For more information of how to use cron, see [http://www.adminschoice.com/crontab-quick-reference](http://www.adminschoice.com/crontab-quick-reference).
