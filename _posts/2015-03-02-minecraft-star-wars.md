---
title: 'Minecraft - Star Wars'
date: 2015-03-02 19:51:00 +00:00
tags: [minecraft, python, raspberry-pi]
redirect_from:
  - /2015/03/minecraft-star-wars.html
---

Myself and David Whale (my co-author on [Adventures in Minecraft](http://www.wiley.com/WileyCDA/WileyTitle/productCd-111894691X.html)) were asked if we would do a talk on "Hacking Minecraft" at the [Raspberry Pi 3rd Birthday Party](http://www.raspberrypi.org/happy-birthday-to-us-2/). I wanted to do something fun to show you how you can do amazing things in Minecraft using the Pi API.

![](/assets/img/2015/03/thatsnomoon.jpg)

After coding the [Solar System in Minecraft](/posts/minecraft-code-solar-system/) I had the idea of creating the Death Star which would be able to 'fire' at the planets and destroy them. I ended up coding an animation of the Death Star destroying Alderaan right up to Luke flying down the trench and successfully bombing the exhaust port with a block of TNT.

{% include youtube.html id="pufDQo9o0gk" %}

If you want to try it out yourself, all the code in at [https://github.com/martinohanlon/minecraft-starwars](https://github.com/martinohanlon/minecraft-starwars). To download the code and run it on your raspberry pi, follow these instructions.

Run Minecraft: Pi Edition and open a world.

Open LX Terminal, and run the following commands to download the program and run the program

```bash
cd ~
git clone https://github.com/martinohanlon/minecraft-starwars
cd minecraft-starwars
python minecraft-starwars.py
```

The code relies heavily on the [minecraftstuff](https://github.com/martinohanlon/minecraftstuff) module which is included in the mcpi directory of the repository, so if you copy the program anywhere else be sure to copy the mcpi directory too.
