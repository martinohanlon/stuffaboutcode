---
title: 'Raspberry Pi Vintage Radio Build'
date: 2015-05-18 22:26:00 +01:00
tags: [gpio, raspberry-pi]
redirect_from:
  - /2015/05/raspberry-pi-vintage-radio-build.html
---

Mrs O'Hanlon buys tat (aka vintage collectibles) and the one thing she seems to buy more than anything else is old radio's, which never work. One such broken audio player I found in her collection was a circa 1955 [Vidor Lady Anne](http://www.radiomuseum.org/r/vidor_my_lady_anne_cn430.html) and I decided to give it a new lease of life and turn it into a Raspberry Pi powered music player.

My aims were to use the original switches, knobs and dials for the controls and when finished it would look the same as the original.

![](/assets/img/2015/05/img_20150321_142638194.jpg)

![](/assets/img/2015/05/img_20150518_223918678.jpg)

I wanted to use the original on/off switch to start and stop playback, the medium wave / long wave positions to select a playlist (M for Martin's playlist and L for Mrs O'Hanlon's playlist) and the tuning wheel to skip tracks forward and backwards.

{% include youtube.html id="HyYoNMfvp9o" %}

I needed a few things to make this a reality:

- A Raspberry Pi!
- A decent DAC (Digital to Analogue Converter) and AMP to power the speaker
- A music player with a programmable API so I could integrate the original controls
- A way of talking to Lady Anne's ancient hardware.
- A program which would be the bridge between Lady Anne and the music player

**DAC & Amp**

At the [Raspberry Pi 3rd Birthday Party](https://www.raspberrypi.org/happy-birthday-to-us-2/) I met the guys from [IQ Audio](http://iqaudio.com/) and I purchased their DAC+ and Amp+ boards, which appealed to me because of the modular build and because the DAC+ still allowed access to GPIO pins (via an L shaped pin connector you can solder to the bottom). This gave me the guts of the system, now I needed software and hardware.

![](/assets/img/2015/05/img_20150331_223708976.jpg)

**Music Player**

I decided on [Volumio](https://volumio.org/) as the music player, which is a very fancy open source music player which sits over the top of [MPD](http://www.musicpd.org/) (music player daemon). It has a very nice responsive web front which works really well with both desktop and mobile browsers.

![](/assets/img/2015/05/screenshot_2015-05-18-14-50-49.png)

As volumio is built on top of MPD I could use the [python-mpd2](https://github.com/Mic92/python-mpd2) module for interfacing with it - see my blog post [Volumio, MPD & Python](/posts/python-mpd-and-volumio/) for an overview of how this works.

**Lady Anne's Hardware**

I stripped out all the gubbins from the old music player apart from the on/off switch and the volume control.

![](/assets/img/2015/05/img_20150321_142753414.jpg)

![](/assets/img/2015/05/img_20150321_143647162.jpg)

Including 60 years of fluff and dust from the speaker.

![](/assets/img/2015/05/img_20150404_145225.jpg)

This left me with a frame with the switch and the volume control potentiometer, the next step was to work out how the switch worked, its made up of layers, with each layer having a rotating copper disk which when turned connected 2 or more connections.

![](/assets/img/2015/05/img_20150407_224047.jpg)

![](/assets/img/2015/05/img_20150407_223448.jpg)

Much testing was done with a multimeter to work out what each of the terminals on the switch did.

The switch is actually many switches and when I connected a current to it, I was also surprised to see that it also wasn't digital, it simply leaks current, off is anywhere between 0v - 1.5v and this totally messes up the Raspberry Pi's GPIO pins.

As I needed an ADC (Analogue to Digital Converter) to read the value from the potentiometer I came up with the concept of an 'analogue' switch and used an MCP3008 ADC to read the values from the switch and when it was above certain voltage I considered it to be on, below it was off - see my blog post [Raspberry Pi, MCP3008 ADC & Python](/posts/raspberry-pi-mcp3008-adc-python/) for an overview of using the MCP3008 ADC.

![](/assets/img/2015/05/img_20150406_093636146.jpg)

To get the MCP3008 to work with the IQ Audio DAC I had to do a bit of hacking. While the majority of the GPIO pins are exposed by the connector on the DAC, neither of the SPI chip select pins are, which I needed, to talk to the MCP3008.

A few emails to IQAudio suggested that while the pins weren't connected, they could be, so I put a small wire between the raspberry pi header and the GPIO connector on the DAC.

![](/assets/img/2015/05/img_20150412_160030895_hdr.jpg)

The last piece of hardware I needed was a rotary encoder which would fit under the tuning wheel and skip tracks - see my post [Raspberry Pi and KY040 Rotary Encoder](/posts/raspberry-pi-and-ky040-rotary-encoder/) for an overview on how to use one.

![](/assets/img/2015/05/ky040.jpg)

Add all that together and what you end up with is this a breadboard design which looks like this.

![](/assets/img/2015/05/vintage-radio_bb.png)

**Radio control program**

Before I put it all together I needed some software which would connect with the good lady's hardware and talk to MPD to make the controls work.

I sketched out a design (like a proper professional) which would broadly involve creating classes to manage each element of the hardware (on/off, playlist selector, volume control, etc) all of which would place events in a queue.

![](/assets/img/2015/05/img_20150407_093610.jpg)

The events would be actions that would need to be taken by the main radio control program (e.g. on, off, change volume, skip track, etc) by talking to MPD. Event based software is really useful for managing hardware where multiple things can all happen at once, but you only want to do one thing at a time.

The software is online at [github.com/martinohanlon/PiLadyAnneRadio](https://github.com/martinohanlon/PiLadyAnneRadio) and it includes information about the structure of the code and installation - although don't expect it to work without modification as while most of the classes are re-usable its built specifically for this radio.

**Putting it together**

To put it all together I needed to find a way of mounting the Raspberry Pi, DAC & Amp in Lady Anne and turning a mess of components and jumper cables on a breadboard into something which would work reliability.

I moved the breadboard jumble onto stripboard - I made myself a [map](https://github.com/martinohanlon/PiLadyAnneRadio/blob/master/docs/stripboard.xlsx) and soldered the cables and components directly onto the board.

![](/assets/img/2015/05/img_20150502_095145973_hdr.jpg)

I mounted the Pi, DAC & Amp and the stripboard onto perspex which I bolted onto Lady Anne's original frame. Luckily the original lady had a space inside the case for a large battery which was just the right size to fit the Pi in.

![](/assets/img/2015/05/img_20150503_092357429.jpg)

That was it, the lady lived...

There was are a couple of things I want to improve. The original potentiometer is rubbish, its not linear and for the first half a turn nothing happens. It could also do with a better speaker, the quality is not bad, but at higher volumes it cuts out.
