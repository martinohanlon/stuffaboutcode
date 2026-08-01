---
title: 'Raspberry Pi - Minecraft - Install'
date: 2013-02-11 17:29:00 +00:00
tags: [games, minecraft, raspberry-pi]
redirect_from:
  - /2013/02/raspberry-pi-minecraft-install.html
---

Im so excited... The [first release of Minecraft](http://pi.minecraft.net/?page_id=10) has been made available.

![](/assets/img/2013/02/minecraft-bridge.png)

**Download**

```bash
cd ~
wget https://s3.amazonaws.com/assets.minecraft.net/pi/minecraft-pi-0.1.1.tar.gz
```

**Extract**

```bash
tar -zxvf minecraft-pi-0.1.1.tar.gz
```

**Execute**

```bash
cd mcpi
./minecraft-pi
```

Note - minecraft has to be run directly on the Pi, it wont work from ssh or via a desktop viewer e.g. TightVNC.

**API**
 By far the best thing about the Minecraft: Pi edition (other than it being free) is the api which allows you to interact with the world in real time. Ive created a few posts / tutorials / interesting things about the Minecraft API:

- [Minecraft - API - The basics](http://www.stuffaboutcode.com/2013/01/raspberry-pi-minecraft-api-basics.html) - an basic introduction into the Minecraft API, its functions and how to use it.
- [Minecraft - API - Tutorial](http://www.stuffaboutcode.com/2013/04/minecraft-pi-edition-api-tutorial.html) - an in-depth look at the API, the concepts and how to use it.
- [Minecraft Projects](http://www.stuffaboutcode.com/p/minecraft.html) - projects I have built using the API, such as:
