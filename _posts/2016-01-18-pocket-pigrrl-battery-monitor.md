---
title: 'Pocket PiGRRL - Battery Monitor'
date: 2016-01-18 00:19:00 +00:00
tags: [c, raspberry-pi]
redirect_from:
  - /2016/01/pocket-pigrrl-battery-monitor.html
---

I recently made myself an [Adafruit Pocket PiGRRL](https://learn.adafruit.com/pocket-pigrrl/overview) and I wanted to modify it so it would warn me when the battery was running low - there is a small red LED but its hidden inside the case!

![](/assets/img/2016/01/img_20160106_213746797.jpg)

The plan was to create a program which would sense the battery getting low and put a warning icon on the top left of screen giving me time to shutdown the Pi properly or plug it in.

![](/assets/img/2016/01/imgp4581.jpg)

![](/assets/img/2016/01/lowbatticon.jpg)

TLDR - just scroll down to install Grrl Battery Monitor.

I started with the software as I, foolishly, thought this would be the hardest part, the problem with creating an icon is that is has to go over the top of everything regardless of what is on the screen (command prompt, emulators, emulation station, everything) or what hardware was rendering it.

My first plan was that I could use [Picamera](http://picamera.readthedocs.org/en/release-1.10/)'s overlay function which I knew used the GPU to output directly to the screen, and with a bit of help from [Dave Jones](https://twitter.com/waveform80) who put together a [prototype](https://gist.github.com/waveform80/b13f7d78e6671c133984), it was looking good, but while the icon appeared on top of emulators and the command prompt, it didnt write over emulation station.

I came across [Low Level Graphics on Raspberry Pi](http://raspberrycompote.blogspot.co.uk/2012/12/low-level-graphics-on-raspberry-pi-part_9509.html) which walks you through writing graphics directly to the [Linux framebuffer](https://en.wikipedia.org/wiki/Linux_framebuffer) using C, this was a lot lower level than I hoped to get into but it would definitely write my icon over anything that was on the screen - using this I wrote a [program](https://github.com/martinohanlon/grrl-bat-monitor/blob/master/grrl_bat_mon.c) to create an icon on the screen when a GPIO pin was triggered.

Next I needed to be able to read from the [power booster](https://learn.adafruit.com/adafruit-powerboost-1000c-load-share-usb-charge-boost/overview) when the battery was running low, my original plan was to use the LBO (low battery output) pin, but this proved to be way more difficult than I expected, read this [post on Adafruit's forum](http://forums.adafruit.com/viewtopic.php?f=19&t=87713) if your really interested.

I ended up connecting a wire to the low battery warning led (red) on the power booster and using this to switch a transistor which connected a GPIO to ground.

![](/assets/img/2016/01/imgp4584.jpg)

Its been frustrating but I am really pleased with how it worked out - if you want to add the batter monitor to your own Pocket PiGRRL follow the instructions below.

**Install Grrl Battery Monitor**

You will need a few parts:

- Some wire
- 2N3904 NPN transistor
- 47k resistor
- Strip board

*Note - if you are doing this on a PiGRRL 2 with a Pi 3, be sure to check out Christian's comments about the [pin to use](http://www.stuffaboutcode.com/2016/01/pocket-pigrrl-battery-monitor.html?showComment=1473048626905#c1441985850678463142) and [wiring-pi install](http://www.stuffaboutcode.com/2016/01/pocket-pigrrl-battery-monitor.html?showComment=1472960188243#c2350592785972375454) before starting.*

1. Open up your Pi GRRL and connect a small length of wire to the red (low power) led on the power booster.

![](/assets/img/2016/01/redledsolderpoint.jpg)

![](/assets/img/2016/01/redledwire.jpg)

2. Solder the components to the strip board. including 2 lengths of wire which will connect to GPIO 19 and GND.

![](/assets/img/2016/01/stripboard2.jpg)

![](/assets/img/2016/01/stripboard.jpg)

![](/assets/img/2016/01/stripboard3.jpg)

3. Flip over your Pi and solder the GPIO and GND wires to the underside of the Pi's GPIO header.

![](/assets/img/2016/01/soldertopi.jpg)

![](/assets/img/2016/01/soldertopi2.jpg)

*The yellow wire is for my [mute / un-mute amp function](http://www.stuffaboutcode.com/2016/01/pocket-pigrrl-adding-mute.html).*

4, Solder the wire from the low power (red) led to the strip board.

![](/assets/img/2016/01/redledsolder.jpg)

5. Stick the strip board to the case in-between the power booster and the amp with a bit of glue and put your PiGRRL back together.

6. Download the program from [github.com/martinohanlon/grrl-bat-monitor](https://github.com/martinohanlon/grrl-bat-monitor)

```bash
cd ~
git clone https://github.com/martinohanlon/grrl-bat-monitor
```

7. Make the program run at boot by editing /etc/rc.local

```bash
sudo nano /etc/rc.local
```

Scroll down and add the command under '/usr/local/bin/retrogame &' but before 'exit 0':

```text
/home/pi/grrl-bat-monitor/grrl_bat_mon &
```

8. Reboot and test!
