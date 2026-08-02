---
title: 'PiAware - Aircraft Overhead Indicator LED'
date: 2015-10-04 09:34:00 +01:00
tags: [gps, python, raspberry-pi]
redirect_from:
  - /2015/10/piaware-aircraft-overhead-led.html
---

I've been using the [PiAware](http://flightaware.com/adsb/piaware/) software to track aircraft flying near me and I liked the idea of turning an LED on when a plane was overhead (or at least near by!).

![](/assets/img/2015/10/12039693_10205647410799461_8669976234796368359_n.jpg)

The first step was creating a way of [reading data from PiAware using Python 3](/posts/read-piaware-flight-data-with-python/), so I created a module called [flightdata.py](/posts/read-piaware-flight-data-with-python/).

Once I had the data it was simply a case of looping through each of the aircraft signals found, calculating the distance between my gps co-ordinates and the gps position of the aircraft. If the distance was less than 10km I turned the led on!

I 'reused' the code to calculate the distance between 2 GPS co-ords from [codecodex](http://www.codecodex.com/wiki/Calculate_distance_between_two_points_on_a_globe#Python).

**Setting up**

You'll need [PiAware](http://flightaware.com/adsb/piaware) installed on your Raspberry Pi, up and running and tracking aircraft.

You'll need an LED, appropriate resistor, breadboard and a couple of Male/Female jumper cables to connect it togther.

The LED is connected to ground and pin 17 with the resistor in between.

![](/assets/img/2015/10/flightlight_bb.png)

**Install**

```bash
cd ~
git clone https://github.com/martinohanlon/flightlight
```

**Usage**
 Launch the flightlight program passing the latitude (lat) and longitude (lon) of your PiAware station (use [www.whatsmygps.com](http://www.whatsmygps.com/) to find your gps location) and the range that should be used to detect if an aircraft is overhead.

```text
usage: flightlight.py [-h] lat lon range
```

e.g. using GPS coords of 52.4539, -1.7481 (Birmingham, UK Airport) with a range of 10km

```bash
cd ~/flightlight/flightlight
sudo python3 flightlight.py 52.4539 -1.7481 10
```

**Code**

```python
import RPi.GPIO as GPIO
import argparse

from flightdata import FlightData
from haversine import points2distance
from time import sleep

#pin of the LED to light
LEDPIN = 17

class LED():
    def __init__(self, ledPin):
        self.ledPin = ledPin
        GPIO.setup(ledPin, GPIO.OUT)

    def on(self):
        GPIO.output(self.ledPin, True)

    def off(self):
        GPIO.output(self.ledPin, False)

#read command line options
parser = argparse.ArgumentParser(description="PiAware Flight Light")
parser.add_argument("lat", type=float, help="The latitude of the receiver")
parser.add_argument("lon", type=float, help="The longitude of the receiver")
parser.add_argument("range", type=int, help="The range in km for how close an aircraft should be to turn on the led")
args = parser.parse_args()

#get the flight data
myflights = FlightData()

#set GPIO mode
GPIO.setmode(GPIO.BCM)

try:

    #create LED
    led = LED(LEDPIN)

    #loop forever
    while True:

        plane_in_range = False

        #loop through the aircraft and see if one is in range
        for aircraft in myflights.aircraft:
            if aircraft.validposition == 1:
                startpos = ((args.lat, 0, 0), (args.lon, 0, 0))
                endpos = ((aircraft.lat, 0, 0), (aircraft.lon, 0, 0))
                distance = points2distance(startpos, endpos)
                #debug
                #print(distance)
                if distance <= args.range:
                    plane_in_range = True

        #turn the led on / off
        if plane_in_range:
            led.on()
        #print("on")
        else:
            led.off()
        #print("off")

        sleep(1)

        #refresh the data
        myflights.refresh()

finally:
    #tidy up GPIO
    GPIO.cleanup()
```
