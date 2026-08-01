---
title: 'Raspberry Pi - Install Minecraft - leaked pre release'
date: 2013-01-03 06:44:00 +00:00
tags: [games, minecraft, raspberry-pi]
redirect_from:
  - /2013/01/raspberry-pi-install-minecraft-leaked.html
---

Anyway, I've been waiting for minecraft to appear on the Pi since it was announced in Nov 2012, the api into the game really appeals and I'm really keen to play about with it and I cant believe I didn't know that a [pre-release version was leaked](http://www.minecraftforum.net/topic/1587033-minecraft-pi-features-and-news-pre-release-leaked/). I was itching to have a go and this is how I installed it:

**NOTE - The official release of Minecraft is now available, see this [post](http://www.stuffaboutcode.com/2013/02/raspberry-pi-minecraft-install.html) for [how to install Minecraft: Pi Edition](http://www.stuffaboutcode.com/2013/02/raspberry-pi-minecraft-install.html).**

Open LXTerminal from the X desktop

**Download**
 The pre-release was made available for download on dropbox.

```bash
cd ~
wget https://dl.dropbox.com/s/hqk8wsdzlyyujli/minecraft-pi-0.1.tar.gz?dl=1
```

**Extract**

```bash
tar -zxvf minecraft-pi-0.1.tar.gz?dl=1
```

**Execute**

```bash
cd mcpi
./minecraft-pi
```

Note - minecraft has to be run directly on the Pi, it wont work from ssh or via a desktop viewer e.g. TightVNC.

Be warned, this [pre release version has a number of bugs](http://www.minecraftforum.net/topic/1587033-minecraft-pi-features-and-news-pre-release-leaked/).

Update - I've been playing around with the [Minecraft API and have included a video and source code](http://www.stuffaboutcode.com/2013/01/raspberry-pi-minecraft-api-basics.html).
