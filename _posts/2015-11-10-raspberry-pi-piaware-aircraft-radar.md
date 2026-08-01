---
title: 'Raspberry Pi PiAware Aircraft Radar'
date: 2015-11-10 21:26:00 +00:00
tags: [gps, python, raspberry-pi]
redirect_from:
  - /2015/11/raspberry-pi-piaware-aircraft-radar.html
---

After creating the [PiAware Flight Indicator LED](http://www.stuffaboutcode.com/2015/10/piaware-aircraft-overhead-led.html) I was keen to see what else I could do with the aircraft data my [PiAware](https://uk.flightaware.com/adsb/piaware/) setup was retrieving for me.

I thought I would see if I could make an 'old fashioned' radar to show what aircraft were being picked up so I could have my own desk based radar.

![](/assets/img/2015/11/img_20151111_072831560.jpg)

{% include youtube.html id="riIjfNKr-SM" %}

I found an example of a [radar written in pygame](http://simpson.edu/computer-science/), which became the basis of my code (although I am pretty sure the original author wouldn't recognise it now) and created a [radar class](https://github.com/martinohanlon/PiAwareRadar/blob/master/piawareradar/radar.py).

I plugged in the GPS coordinates of the aircraft using the [PiAware flight data class](http://www.stuffaboutcode.com/2015/09/read-piaware-flight-data-with-python.html) I created to produce a pretty swanky, even if I say so myself, radar of all the aircraft I am picking up signals from.

**Setup PiAware**
 If you want to have a go, first you need to setup a [PiAware](https://uk.flightaware.com/adsb/piaware/) server to receive data - you don't need a lot of equipment and its really easy to do.

**Download my project**
 The code is on [github](https://github.com/martinohanlon/PiAwareRadar)at [github.com/martinohanlon/PiAwareRadar](https://github.com/martinohanlon/PiAwareRadar).

```bash
git clone https://github.com/martinohanlon/PiAwareRadar
```

**Run the program**
 The program expects a number of command line parameters, the mandatory being the latitude and longitude of your PiAware server, which will be the centre of the radar.

```bash
cd PiAwareRadar/piawareradar
python3 piawareradar.py mylat mylon
```

You can set other parameters for the IP address of the PiAware server, if your radar is running on a different machine, whether you want it to run full screen and the layout of your screen (normal or touch).

**Usage**

```text
    usage: piawareradar.py [-h] [--piawareip PIAWAREIP] [--screen SCREEN] [--fullscreen] lat lon

    PiAware Flight Radar

    positional arguments:
      lat                   The latitude of the receiver
      lon                   The longitude of the receiver

    optional arguments:
      -h, --help            show this help message and exit
      --piawareip PIAWAREIP The ip address of the piaware server
      --screen SCREEN       The screen config to use [normal / touch]
      --fullscreen          Fullscreen radar
```

The plus and minus buttons in the top right allow you to zoom in and out, if you click on a dot, the data about that flight will be display in the bottom right hand corner.

![](/assets/img/2015/11/radar.jpg)
