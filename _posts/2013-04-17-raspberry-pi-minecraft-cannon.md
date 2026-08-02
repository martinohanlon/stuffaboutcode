---
title: 'Raspberry Pi - Minecraft Cannon'
date: 2013-04-17 07:01:00 +01:00
tags: [minecraft, python, raspberry-pi]
redirect_from:
  - /2013/04/raspberry-pi-minecraft-cannon.html
---

![](/assets/img/2013/04/minecraftcannon-2.jpg)I had this idea about using [Minecraft: Pi Edition and its API](/posts/minecraft-pi-edition-api-tutorial/) to show how trigonometry, [mechanics](http://en.wikipedia.org/wiki/Mechanics) and mathematics can actually be useful and given that everyone likes to blow stuff up.... I thought I would make a cannon.

A cannon which could point in any direction (0-360 degrees), angle upwards (0-90 degrees) and when fired would send a cannon ball upwards, falling in-line with the laws of gravity and then explode when it hit the ground.

{% include youtube.html id="6NHorP5VuYQ" %}

**http://youtu.be/6NHorP5VuYQ**

I liked the idea of a command line interface, its a cannon after all they are not meant to be hi-tech devices, to control the cannon you use the following commands:

- start - create \[start-up\] the cannon
- rotate \[0-360 degress\] - rotate the cannon
- tilt \[0-90 degress\] - tilt the cannon upwards
- fire - FIRE!
- exit - exit and clear the cannon

The code contains 4 classes written in Python:

1. CannonCommands - used to control the command line interface, based on python's cmd module
2. MinecraftDrawing - a generic class I'm building up which supports many generic drawing functions (drawLine, drawFace, drawSphere, etc)
3. MinecraftCannon - a class which controls the building and changing of the cannon base and its gun, this contains all the code required to 'point' the gun to a specific point on the a sphere based on the direction and tilt angles
4. MinecraftBullet - a class which controls the flight of the bullet through the air and its eventual explosion, including the maths to manage general mechanics of velocity and gravity

**Download and run**

You can download the code direct from [github](https://github.com/martinohanlon/minecraft-cannon)

, [https://github.com/martinohanlon/minecraft-cannon](https://github.com/martinohanlon/minecraft-cannon), so run minecraft, open/create a world and follow the instructions:

```bash
sudo apt-get install git-core
cd ~
git clone https://github.com/martinohanlon/minecraft-cannon.git
cd minecraft-cannon
python minecraft-cannon.py
```
