---
title: 'Raspberry Pi - gpioRap - A GPIO Wrapper'
date: 2012-12-05 13:30:00 +00:00
tags: [gpio, python, raspberry-pi]
redirect_from:
  - /2012/12/raspberry-pi-gpiorap-gpio-wrapper.html
---

Anyway, I've been playing around with the Raspberry Pi's GPIO for the past couple of weeks, see my [previous post](/posts/raspberry-pi-getting-led-to-flash/) about [getting an led to flash](/posts/raspberry-pi-getting-led-to-flash/) and I kept getting frustrated with **writing the same code over and over again**, like:

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
 If you have never installed python modules before you are going to need to install the python setuptools module (aka distribute), see blog post, [python - installing modules](/posts/raspberry-pi-python-installing-modules/), for info on how to do this.

***Install the module***

```bash
cd gpioRap
sudo python setup.py install
```

I would love some help is extending gpioRap, so if you have the gpio code for managing a specific component or would like to get your hands dirty and improve the class, let me know and we can work together.
