---
title: 'Raspberry Pi Reading Car Diagnostics (OBD-II) Data'
date: 2013-07-09 22:08:00 +01:00
tags: [car, python, raspberry-pi]
redirect_from:
  - /2013/07/raspberry-pi-reading-car-obd-ii-data.html
---

I read about a guy called salgar on [pistonheads.com](http://pistonheads.com/) who had used a [raspberry pi to read data from his motorbike](http://www.pistonheads.com/gassing/topic.asp?t=1216528) via an OBD-II USB reader and I thought, I've got to have a go at that.

{% include youtube.html id="UdYVlgv5D3Q" %}

[OBD](http://en.wikipedia.org/wiki/On-board_diagnostics) or On Board Diagnostics and OBD-II is a standard for communicating and reading data from a car, its standard across most modern cars and the likelihood is you have a connector in your car which you can read all sorts of data about the car such as RPM, Speed, Temperature and a million other things you wouldn't guess a car was monitoring.

*Update - I've taken this prototype to the next stage and used the [OBD data to overlay mph, rpm, temperature and throttle position over video taken with the camera board](http://www.stuffaboutcode.com/2013/07/raspberry-pi-car-cam-overlaid-with-obd.html).*

{% include youtube.html id="5EPRbiP9uTw" %}

I got hold of a USB to OBD2 interface cable for about £10. Pick one up from [amazon.com](http://www.amazon.com/gp/product/B004B7PSA0/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B004B7PSA0&linkCode=as2&tag=stuabocod-20) or [amazon.co.uk](http://www.amazon.co.uk/gp/product/B00CWU3AAS/ref=as_li_tf_tl?ie=UTF8&camp=1634&creative=6738&creativeASIN=B00CWU3AAS&linkCode=as2&tag=stuabocod-21).

![](/assets/img/2013/07/usb-obd.jpg)

I then took a fork of salgar's software from his github repository, [https://github.com/roflson/pyobd](https://github.com/roflson/pyobd), as the basis for my program. salgar's software is a fork from a project called pyobd, [https://github.com/peterh/pyobd](https://github.com/peterh/pyobd), which is a GUI based application for reading OBD-II data.

I used this as the basis for a program which would connect through OBD-II interface, 'ask' the car which sensors it supported and then read the data sensors in a loop every 0.5 second and write them to the screen.

I see this as step one in a project to log data about a car for other uses.

**Download and run**

You can download the code direct from

[github](https://github.com/martinohanlon/pyobd)

,

[https://github.com/martinohanlon/pyobd](https://github.com/martinohanlon/pyobd)

, so open a terminal and follow the instructions:

```bash
sudo apt-get install python-serial
sudo apt-get install git-core
cd ~
git clone https://github.com/martinohanlon/pyobd
cd pyobd
python obd_capture.py
```
