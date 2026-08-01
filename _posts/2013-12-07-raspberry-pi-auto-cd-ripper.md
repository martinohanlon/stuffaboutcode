---
title: 'Raspberry Pi - Auto CD Ripper'
date: 2013-12-07 00:34:00 +00:00
tags: [python, raspberry-pi]
redirect_from:
  - /2013/12/raspberry-pi-auto-cd-ripper.html
---

I've got a lot of CD's I have never got round to ripping to MP3. I didn't fancy sitting in front of a PC shovelling them in for hours, so I wrote I little program to automate the ripping using an raspberry pi and an old USB CD/DVD drive.

USB CD/DVD drives are pretty cheap nowadays, check out Amazon ([UK](http://www.amazon.co.uk/s/?_encoding=UTF8&camp=1634&creative=19450&field-keywords=usb%20cd%20drive&linkCode=ur2&rh=i%3Aaps%2Ck%3Ausb%20cd%20drive&sprefix=usb%20cd%20%2Caps&tag=stuabocod-21&url=search-alias%3Daps), [US](http://www.amazon.com/s/?_encoding=UTF8&camp=1789&creative=390957&linkCode=ur2&pageMinusResults=1&suo=1386403837217&tag=stuabocod-20&url=search-alias%3Daps#/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=usb%20cd%20drive&sprefix=usb+cd+%2Caps&rh=i%3Aaps%2Ck%3Ausb%20cd%20drive&sepatfbtf=true&tc=1386403840951)), if you get one without a separate power supply, you will also need a powered USB hub.

When my program runs, it opens the cd drawer and waits for a CD to be put in, when a CD is inserted it will rip the CD and when finished open the drawer so you can put in the next. The plan is to stick it in by the tv and just let it rip.

{% include youtube.html id="w7arOpX99VM" %}

Its a pretty simple python program which starts up a great command line cd ripper called [Ripit](http://www.suwald.com/ripit/news.php) plus an mp3 encoder called [lame](http://lame.sourceforge.net/).

If you want to have a go yourself.

**Install ripit, lame and eject**
 You will need a few utilities to do the CD ripping.

```bash
sudo apt-get install ripit lame eject
```

**Download my program**
 You can download my program from github, [github.com/martinohanlon/AutoRipper.git](https://github.com/martinohanlon/AutoRipper.git)

```bash
sudo apt-get install git-core
cd ~
git clone https://github.com/martinohanlon/AutoRipper.git
```

**Run it**
 You have to pass the program 2 parameters:

- an output directory of where the CD's will be ripped to
- a timeout in seconds which is the amount of time the program will wait in between CD rips before it quits

```bash
cd AutoRipper
python autoRipper.py /home/pi 60
```

**The code**

```python
#!/usr/bin/env python

import subprocess
import time
import pygame
import datetime
import argparse

RIPITDIRTEMPLATE = "'\"/$artist/$album\"'"

class AutoRipper():
    def __init__(self,cdDrive,outputPath,timeout):
        self.cdDrive = cdDrive
        self.outputPath = outputPath
        self.timeout = timeout
        self.cdDrive.init()

    def start(self):
        print "AutoRipper - Waiting for Audio Disk"
        #loop until a disk hasnt been inserted within the timeout
        lastTimeDiskFound = datetime.datetime.now()
        while (lastTimeDiskFound + datetime.timedelta(0,self.timeout)) > datetime.datetime.now():
            #is there a disk in the drive?
            if self.cdDrive.get_empty() == False:
                # Disk found
                # is it an audio cd?
                if self.cdDrive.get_track_audio(0) == True:
                    print "AutoRipper - Audio disk found, starting ripit."
                    #run ripit
                    # getting subprocess to run ripit was difficult
                    #  due to the quotes in the --dirtemplate option
                    #   this works though!
                    ripit = subprocess.Popen("ripit --outputdir " + self.outputPath + " --dirtemplate=" + RIPITDIRTEMPLATE + " --nointeraction", shell=True)
                    ripit.communicate()
                    # rip complete - eject disk
                    print "AutoRipper - rip complete, ejecting"
                    # use eject command rather than pygame.cd.eject as I had problems with my drive
                    subprocess.call(["eject"])
                else:
                    print "AutoRipper - Disk inserted isnt an audio disk."
                    subprocess.call(["eject"])
                lastTimeDiskFound = datetime.datetime.now()
                print "AutoRipper - Waiting for disk"
            else:
                # No disk - eject the tray
                subprocess.call(["eject"])
            # wait for a bit, before checking if there is a disk
            time.sleep(5)

        # timed out, a disk wasnt inserted
        print "AutoRipper - timed out waiting for a disk, quitting"
        # close the drawer
        subprocess.call(["eject", "-t"])
        #finished - cleanup
        self.cdDrive.quit()

if __name__ == "__main__":

    print "StuffAboutCode.com Raspberry Pi Auto CD Ripper"

    #Command line options
    parser = argparse.ArgumentParser(description="Auto CD Ripper")
    parser.add_argument("outputPath", help="The location to rip the CD to")
    parser.add_argument("timeout", help="The number of seconds to wait for the next CD")
    args = parser.parse_args()

    #Initialize the CDROM device
    pygame.cdrom.init()

    # make sure we can find a drive
    if pygame.cdrom.get_count() == 0:
        print "AutoRipper - No drives found!"
    elif pygame.cdrom.get_count() > 1:
        print "AutoRipper - More than 1 drive found - this isnt supported - sorry!"
    elif pygame.cdrom.get_count() == 1:
        print "AutoRipper - Drive found - Starting"
        autoRipper = AutoRipper(pygame.cdrom.CD(0),args.outputPath,int(args.timeout))
        autoRipper.start()

    #clean up
    pygame.cdrom.quit()
```

I had problems with my cd drive where occasionally it wouldn't open the drawer with the button on the front, if you have the same, just type the command eject and it'll pop right out.
