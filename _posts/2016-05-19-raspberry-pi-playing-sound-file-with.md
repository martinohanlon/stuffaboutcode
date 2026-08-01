---
title: 'Raspberry Pi - Playing a Sound File with Python'
date: 2016-05-19 12:40:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2016/05/raspberry-pi-playing-sound-file-with.html
---

A question I get asked a lot in Picademy is how to I play a sound file using Python.

Using just whats on the standard Raspbian image the easiest way, IMO, is to use Pygame.

This small code snippet below shows you how. Just put the wav file in the same place as your program.

```python
import pygame
from time import sleep

#Initialise pygame and the mixer
pygame.init()
pygame.mixer.init()

#load the sound file
mysound = pygame.mixer.Sound("mysound.wav")

#play the sound file for 10 seconds and then stop it
mysound.play()
time.sleep(10)
mysound.stop()
```

You will have to use wav files, as opposed to other sounds files such as mp3, ogg, etc - use [media.io](http://media.io/) to convert them.
