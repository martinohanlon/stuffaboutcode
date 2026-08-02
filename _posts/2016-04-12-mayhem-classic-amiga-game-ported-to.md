---
title: 'Mayhem, Amiga game, ported to Raspberry Pi'
date: 2016-04-12 21:53:00 +01:00
tags: [c, games, raspberry-pi]
redirect_from:
  - /2016/04/mayhem-classic-amiga-game-ported-to.html
---

*Update - I've taken Mayhem forward to create [Mayhem 2](/posts/mayhem-2-open-source-cave-shooter/).*

I had a [Commodore Amiga](https://en.wikipedia.org/wiki/Amiga) and a game I played, a lot, was [Mayhem](http://www.lemonamiga.com/games/details.php?id=2972), its a multiplayer (2-4) shooter - imagine multiplayer asteroids, with gravity, fuel and shields!

It was ported to the PC in 2002 by [devpack](https://github.com/devpack) who released the code in 2011 on [github](https://github.com/devpack/mayhem) and [google code](https://code.google.com/archive/p/mayhem/) which is where I picked it up and ported it to the Raspberry Pi.

{% include youtube.html id="Vxozz0Ijdr0" %}

This is the port, but check out the [original Amiga game](https://www.youtube.com/watch?v=fs30DLGxqhs).

I got some help from the [Raspberry Pi forums in getting it to compile](https://www.raspberrypi.org/forums/viewtopic.php?f=33&t=142284&) then it was case of sorting out a few case sensitive filename bugs (it was original written for Windows!) and tracking down a bug in the original code which was causing a memory access error and segmentation fault.

The code is on [github.com/martinohanlon/mayhem-pi](http://github.com/martinohanlon/mayhem-pi).

**Install**

```bash
sudo apt-get install liballegro4.4 liballegro4-dev
git clone https://github.com/martinohanlon/mayhem-pi
```

**Run**

```bash
cd mayhem-pi
./start
```

**Keys**
 Player 1 - z, x, c, v, g
 Player 2 - left, right, pad del, pad 0, pad enter
 Player 3 - b, n, 'comma', m, l
 Player 4 - y, u, o, i, 0
 Change level - 1, 2, 3

**Compile**
 If you want to modify the game, I've got a couple of things on my [list](https://github.com/martinohanlon/mayhem-pi/issues), you can recompile it with.

```bash
cd mayhem-pi
make
```

![](/assets/img/2016/04/mayhem.jpg)
