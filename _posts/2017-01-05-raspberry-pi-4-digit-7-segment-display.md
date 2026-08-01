---
title: 'Raspberry Pi - 4 digit 7 Segment display, gpiozero'
date: 2017-01-05 21:44:00 +00:00
tags: [gpio, raspberry-pi]
redirect_from:
  - /2017/01/raspberry-pi-4-digit-7-segment-display.html
---

I recently picked up some '[retro 4 digit LED displays](https://shop.pimoroni.com/products/retro-4-digit-led-display)' from [pimoroni](https://www.pimoroni.com/), noticing there was no support in [gpiozero](http://gpiozero.readthedocs.io/) for 7 segment displays (either [single](http://www.stuffaboutcode.com/2016/10/raspberry-pi-7-segment-display-gpiozero.html) or multi digit) I decided to add them and create a [pull request](https://github.com/RPi-Distro/python-gpiozero/pull/488).

This builds on the code I created for driving [single 7 segment displays](http://www.stuffaboutcode.com/2016/10/raspberry-pi-7-segment-display-gpiozero.html).

![](/assets/img/2017/01/7seg_leds.png)

Hopefully the PR will get added into a gpiozero release soon, but until then add this [code](https://gist.github.com/martinohanlon/23a8a67bc3c68988fbb492b3d5d42ca5) to your project and use the following to drive your display.

```text
#setup the pins

#these are the pins the LED are connected too
# (in the order A, B, C, D, E, F, G, decimal point)
LED_PINS = (7, 22, 25, 17, 8, 27, 4, 24)
#these are the pins the digits are connected too
DIGIT_PINS = (23, 18, 15, 14)

#create the multi seven segment display
# use active_high=True when digit pins are cathode (ground)
multi_sev = MultiSevenSegmentDisplay(LED_PINS, DIGIT_PINS,
                                     active_high=True)

#display your message
multi_sev.display("LEDS")

#turn off the display using
multi_sev.off()
```

The display function works by plexing the display, turning the LEDs on one at a time, so quickly it tricks the eye into thinking the display is showing 1 message.

{% include youtube.html id="jeg5sjdHCYM" %}
