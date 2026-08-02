---
title: 'Raspberry Pi GPS Helmet Cam'
date: 2014-01-27 22:32:00 +00:00
tags: [camera, python, raspberry-pi]
redirect_from:
  - /2014/01/raspberry-pi-gps-helmet-cam.html
---

![](/assets/img/2014/01/20140126_222809-1.jpg)I've been snowboarding for the past 20 years, and for most of that time I've been video'ing mine and my buddies adventures with a helmet cam. [An old video of me snowboarding in Morzine, France](http://youtu.be/rfFMad5Qit4).

I wanted to make my own helmet cam which would also show data about what was going on (e.g. speed, altitude, temperature).

{% include youtube.html id="wChI6VVYDUc" %}

*Raspberry Pi GPS Helmet Cam*

The starting point was my [Raspberry Pi GPS Tracking Car Dash Cam](/posts/raspberry-pi-car-cam-gps-data-map/), this gave me some code for gathering GPS data, recording video and generating data overlay video's.

I came up with a 1 led, 1 button design; the led flashes when the cam is 'ready' (quickly when there isn't a GPS fix, slowly when there is GPS fix), the led comes on when the camera is recording, a short button press starts / stops the camera and a long button press shutdowns the helmet cam.

I set about writing the code which would run at start-up of the Pi and control the camera, waiting for the button to be pressed, controlling the led, reading the [GPS data](/posts/raspberry-pi-gps-setup-and-python/) and [temperature data](/posts/raspberry-pi-python-temp-sensor-ds18b20/) and start / stop the camera.

The program is multi-threaded and simply starts up a thread for each 'thing' (led, button, GPS, temperature sensor) that needs to be 'controlled', the main program then polls these controllers asking them if anything has changed and acts accordingly (e.g. starting / stopping the camera, shutting down the pi).

When the camera is started , the program uses the excellent python module, [picamera](/posts/raspberry-pi-camera-python-picamera/), to start the video capture and writes the gps and temperature data to a file while the video is recording. I made a change to the picamera module (which has since been [introduced](https://github.com/waveform80/picamera/issues/34)), this gave me a function to read the current frame number while the video was being recorded, allowing me to sync the data I have read to an exact position in the video.

I then use the data file to create a data video which I ultimately overly on top of the video taken from the helmet cam. The data video is created in exactly the same way as my [Raspberry Pi GPS Car Dash Cam](/posts/raspberry-pi-car-cam-gps-data-map/), by creating individual images for each frame using PIL (python imaging library).

![](/assets/img/2014/01/000716.jpg)

*A single frame image from a data video*

I then use mencoder to join the images together into a single video.

**Hardware**
 The helmet cam is a Raspberry Pi model A inside a small sandwich box, a control box and a Raspberry Pi camera board on the end of a long ribbon cable.

![](/assets/img/2014/01/20140107_214450.jpg)

The control box houses an [Adafruit Ultimate GPS breakout board](https://www.adafruit.com/products/746), a waterproof led and button, a temperature sensor and a very badly soldered piece of strip board which ties it all together.

It was my first time using stripboard, so moving my breadboard build to something more robust was a big job for me, but armed with a piece of paper and a set of crayons I came up with a design!

![](/assets/img/2014/01/20131228_163726.jpg)

![](/assets/img/2014/01/20131228_172940.jpg)

The camera is mounted on a small piece of wood, cut so when its mounted on my helmet, it, roughly, points in the right direction.

I got a 1m cable for the camera which I shielded with tin foil, as without it, it caused the GPS unit to loose fix when it was recording and then wrapped it in a polyester braided sheath.

![](/assets/img/2014/01/20140101_172353.jpg)

The camera, mount and cable are then attached using sticky backed velcro to my helmet, so I could take it off when not in use.

The whole set-up was powered by a usb power bank.

**Code**
[https://github.com/martinohanlon/pelmetcam](https://github.com/martinohanlon/pelmetcam)

There are a number of python modules which make up the helmet cam code:
 - [pelmetcam.py](https://github.com/martinohanlon/pelmetcam/blob/master/pelmetcam.py) - this is the main program which controls the helmet cam
 - [tempSensorController.py](https://github.com/martinohanlon/pelmetcam/blob/master/tempSensorController.py) - module which continually reads from the temperature sensor
 - [GPSController.py](https://github.com/martinohanlon/pelmetcam/blob/master/GPSController.py) - module which continually reads from the GPS sensor
 - [createDataOverlay.py](https://github.com/martinohanlon/pelmetcam/blob/master/createDataOverlay.py) - module which creates the data overlay images

I also created a few bash scripts to make things easier to manage:
 - [runPelmetcam.sh](https://github.com/martinohanlon/pelmetcam/blob/master/runPelmetcam.sh) - this is run when the pi boots and starts up the helmet cam, including the GPS daemon, temp sensor modules and shuts down the pi when the program finishes
 - [runPelmetcam.init](https://github.com/martinohanlon/pelmetcam/blob/master/runPelmetcam.init) - init.d script to make runPelmetcam.sh run at boot, see this [post](/posts/raspberry-pi-run-program-at-start-up/) for information on running commands at boot
 - [createVideos.sh](https://github.com/martinohanlon/pelmetcam/blob/master/createVideos.sh) - runs the commands to make the main video into an MP4, creating the data overlay images and encoding them into a video file

**Challenges**
 Before I went away I wanted to make sure it would operate in cold weather and test simple things, like my code would work if temperatures went negative, unfortunately an unusually mild winter in the UK mean't the only thing I could do was stick it in the freezer! It performed perfectly for the 20 minutes I left it in there. I can also confirm that the light does go off when you close the freezer door!

![](/assets/img/2014/01/20140109_112836.jpg)

After the unit had been on for a while I started to notice that the temperature sensor was reporting temperatures much higher than expected (i.e. +9 C when it was -5 outside), I don't know for sure but I'm pretty sure the GPS unit generates a little bit of heat, which obviously when trapped inside a small sealed box warmed it up a bit!

If I was to do it again I wouldn't bother putting the GPS unit in the control box; it seemed like a good idea due to the interference the camera creates and a desire to have it 'outside' to get a better GPS fix, but with the shielding on the camera cable and the sensitivity of the GPS Unit, I didn't need to worry.

There is a current [bug in the raspberry pi firmware](https://github.com/raspberrypi/linux/issues/435) which means if you try to use the raspberry pi camera at the same time as using a 1-wire sensor (like my temperature one) the camera will fail to start up. There are several reported workarounds, in the end I ended up reverting to an old firmware which didn't suffer from this bug.

**Stability**
 I wasn't expecting my Pi powered helmet cam to be very robust, I was secretly only expecting to get 1 or 2 runs out of it. I thought the combination of wet conditions, very cold temperatures, dodgy wiring / soldering and some pretty aggressive snowboarding would mean that it just self destructed.

However, it proved to be very robust, I used it all week and recorded hours of footage with the camera.

The only component which failed was a cheap micro usb power cable which split and caused the pi to boot and reboot continuously as it shorted out, ultimately leading to a corrupt file system.

**Full Length Videos**
 You can watch the unabridged videos taken using the helmet cam on my [youtube channel](http://www.youtube.com/user/martin26071976):

[Les Deux Alpes 2014 - Snowboarding "Vallee Blanche Off The Side"](http://www.youtube.com/watch?v=EN9MqABjAZ8)
[Les Deux Alpes 2014 - Snowboarding - "Boarder Cross Lee Wins"](http://www.youtube.com/watch?v=dk_os-_hhzo)
[Les Deux Alpes 2014 - Snowboarding "Under the Vandri Lift into the Trees"](http://www.youtube.com/watch?v=MWXi7HCI-MU)
[Les Deux Alpes 2014 - Snowboarding "Piste Down To Lac Noir Lift"](http://www.youtube.com/watch?v=iJMjbsSNnjg)

**Shopping List**
 I was asked what 'bits' you need to create your own helmet cam. A lot of these bits I already had, but I think this is a complete shopping list:
 - Raspberry Pi - Model A
 - Raspberry Pi - Camera Board
 - Sandisk Class 10 32GB SD Card
 - Adafruit Ultimate GPS Breakout Board ([UK](https://www.blogger.com/%22http://www.amazon.co.uk/gp/product/B008FZIZUE/ref=as_li_ss_tl?ie=UTF8&camp=1634&creative=19450&creativeASIN=B008FZIZUE&linkCode=as2&tag=stuabocod-21), [US](https://www.blogger.com/%22http://www.amazon.com/gp/product/B00GLW4016/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00GLW4016&linkCode=as2&tag=stuabocod-20&linkId=QSMKZJYEJC6HSW2U))
 - Waterproof Push Button
 - Waterproof Ultrabright Red LED
 - Electronic Project Enclosure
 - 1m ribbon camera cable
 - Tin Foil (for shielding camera cable)
 - Portable Battery Charger USB Power Bank
 - 15mm Polyester Braiding
 - 8m Polyester Braiding
 - DS18B20 Temperature Sensor ([UK](http://www.amazon.co.uk/gp/product/B00CN43OTK/ref=as_li_ss_tl?ie=UTF8&camp=1634&creative=19450&creativeASIN=B00CN43OTK&linkCode=as2&tag=stuabocod-21), [US](https://www.blogger.com/%22http://www.amazon.com/gp/product/B004G53D54/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B004G53D54&linkCode=as2&tag=stuabocod-20&linkId=LSUEUGSIZMJEWQFF))
 - 4.7k resistor (for temperature sensor)
 - 10k resistor (pull down for button)
 - ?k resistor (appropriate for your LED)
 - Stripboard
 - Plenty of wire
