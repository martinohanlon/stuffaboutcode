---
title: 'Minecraft, a Microbit and an X-Wing'
date: 2015-12-18 13:52:00 +00:00
tags: [adventures-in-minecraft, microbit, minecraft, python]
redirect_from:
  - /2015/12/minecraft-microbit-and-x-wing.html
---

I was having a chat with [David Whale](https://twitter.com/whaleygeek), my co-author of [Adventures in Minecraft](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-111894691X.html) and he remarked that wouldn't it be cool if you could control something in Minecraft using the Microbit. (Btw - you should definitely check out David's virtual [Minecraft Microbit](https://github.com/whaleygeek/mc_microbit).)

I settled on the idea of using the Microbit's accelerometer to control an object flying through Minecraft. What object, well it had to be the X-Wing, from my previous [Minecraft - Star Wars](/posts/minecraft-star-wars/) project.

![](/assets/img/2015/12/minecraft_microbit.jpg)

The A button starts and stops the X-Wing, by tilting the Microbit left and right you can turn and the B button drops blocks of TNT which create craters where they land.

{% include youtube.html id="59KqWVwj_Cc" %}

There are 2 python programs:

1. [microbitreaddata.py](https://github.com/martinohanlon/microbit-micropython/blob/master/examples/mcfly/microbitreaddata.py) - this runs on the Microbit and reads the status of the buttons and accelerometer
2. [mcfly.py](https://github.com/martinohanlon/microbit-micropython/blob/master/examples/mcfly/mcfly.py) - this runs on your computer (I used a Windows PC running Raspberry Juice and full Minecraft, but it would work on a Raspberry Pi as well) which reads the data from the Microbit and makes all the calls to move the X-Wing in Minecraft.

You will find the full code and my other Microbit MicroPython examples at [github.com/martinohanlon/microbit-micropython](https://github.com/martinohanlon/microbit-micropython).
