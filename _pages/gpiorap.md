---
title: 'gpioRap'
date: 2012-12-18 20:59:00 +00:00
redirect_from:
  - /p/gpiorap.html
---

Whilst building a few apps that use the Raspberry Pi's GPIO, see my [previous post](http://www.stuffaboutcode.com/2012/11/raspberry-pi-getting-led-to-flash.html) about [getting an led to flash](http://www.stuffaboutcode.com/2012/11/raspberry-pi-getting-led-to-flash.html),I kept getting frustrated with **writing the same code over and over again**, like:

- turning an led on
- toggling an led from on to off or vice versa
- making an led flash
- waiting for a button to be pressed
- working out if a button had been pressed, or it was still held down

and this was just for simple stuff, what was it going to be like when I needed to be more complicated things.

I decided to create a wrapper class, gpioRap, which I could use to manage common components (initially buttons and led) and then that would leave me to only worry about the code needed to link components together and make the application work.

gpioRap is essentially a class of classes, a main class, GpioRap which allows you to setup the gpio and create components (Button, LED) which are sub-classes within GpioRap.

The structure of classes within a class also makes sure it is extendable, as I start to use new components, I simply create a new class (e.g. Relay, TemperatureSensor, etc).

So, say I want to create a program which waits for a button to be pressed and turns an led on or off:

```python
import gpioRap as gpioRap
import RPi.GPIO as GPIO
print "An example of gpioRap, when the button is pressed it will light the led, and pressed again it will turn off the led"
#Create GpioRap class using BCM pin numbers
gpioRapper = gpioRap.GpioRap(GPIO.BCM)
#Create an LED, which should be attached to pin 17
led = gpioRapper.createLED(17)
#Create a button, which should be monitored by pin 4, where False is read when the button is pressed
button = gpioRapper.createButton(4, False)
try:
    #Loop until ctrl c is pressed
    while True:
        #Wait for the button to be pressed
        if button.waitForPress() == True:
            led.toggle()
except KeyboardInterrupt:
    #Cleanup
    gpioRapper.cleanup()
```

The code for gpioRap is managed on github at [https://github.com/martinohanlon/gpioRap](https://github.com/martinohanlon/gpioRap)

**Installing gpioRap**

***Install git-core***
 In order to get the code from github you need to install git-core tools.

```bash
sudo apt-get install git-core
```

***Get the code from git***

```bash
git clone https://github.com/martinohanlon/gpioRap.git
```

***Install distribute***
 If you have never installed python modules before you are going to need to install the python setuptools module (aka distribute), see blog post, [python - installing modules](http://www.stuffaboutcode.com/2012/10/raspberry-pi-python-installing-modules.html), for info on how to do this.

***Install the module***

```bash
cd gpioRap
sudo python setup.py install
```

I would love some help is extending gpioRap, so if you have the gpio code for managing a specific component or would like to get your hands dirty and improve the class, let me know and we can work together.

**Class Documentation**

```text
NAME
    gpioRap

FILE
    /usr/local/lib/python2.7/dist-packages/gpioRap.py

DESCRIPTION
    gpioRap - A wrapper class for the RPi.GPIO module
    Author - Martin O'Hanlon
    Website - www.stuffaboutcode.com

CLASSES
    GpioRap

    class GpioRap
     |  A wrapper class for the RPi.GPIO module
     |
     |  Methods defined here:
     |
     |  __init__(self, gpioSetMode=None)
     |      Constructor can be passed the gpio set mode, GPIO.BCM / GPIO.Board, if None is passed GPIO.BCM is default
     |
     |  cleanup(self)
     |      Cleans up the GPIO, in effect resetting all values to default and closes
     |
     |  createButton(self, gpioPin, pressedState)
     |      Creates a button, gpioPin is the pin where the button is connected, pressedState is a boolean (True, False) which represents the value at the GPIO when the button is pressed
     |
     |  createLED(self, gpioPin)
     |      Creates an LED, gpioPin is the pin which is LED is connected to
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  Button = <class gpioRap.Button>
     |
     |  LED = <class gpioRap.LED>

        class Button
         |  A wrapper class for managing a single button
         |
         |  Methods defined here:
         |
         |  __init__(self, gpioPin, pressedState)
         |      Constructor must be passed gpioPin (the pin where the button is connected) and pressedState (a boolean [True, False] which represents the value at the GPIO when the button is pressed
         |
         |  get(self)
         |      Gets the current value of the gpio
         |
         |  pressed(self)
         |      Returns a boolean representing whether the button is pressed
         |
         |  waitForPress(self, timeOut=None)
         |      Waits for the button to be pressed (or an optional time out expires) and returns for a boolean representing whether the button is pressed

        class LED
         |  A wrapper class for managing an LED
         |
         |  Methods defined here:
         |
         |  __init__(self, gpioPin)
         |      Constructor must be bassed gpioPin (the pin where the LED is connected)
         |
         |  flash(self, times, delay)
         |      Flashes the LED, a number of times with a delay (in seconds) inbetween
         |
         |  get(self)
         |      Gets the value of the led
         |
         |  off(self)
         |      Turns the LED off
         |
         |  on(self)
         |      Turns the LED on
         |
         |  set(self, ledValue)
         |      Sets the value of the LED [True / False]
         |
         |  toggle(self)
         |      Toggles the LED, if its on, turns it off and vice versa
```
