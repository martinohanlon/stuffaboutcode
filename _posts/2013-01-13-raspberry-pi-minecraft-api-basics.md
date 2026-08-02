---
title: 'Raspberry Pi - Minecraft API - the basics'
date: 2013-01-13 20:28:00 +00:00
tags: [games, minecraft, python, raspberry-pi]
redirect_from:
  - /2013/01/raspberry-pi-minecraft-api-basics.html
---

Anyway, I've been exploring the API which comes with the new Pi edition of Minecraft. See [Raspberry Pi - Minecraft - Install](/posts/raspberry-pi-minecraft-install/) for details on how to install Minecraft: Pi Edition. If you want a more in-depth tutorial rather than just the basics, see my [Minecraft: Pi Edition - API Tutorial](/posts/minecraft-pi-edition-api-tutorial/) post.

{% include youtube.html id="icrbqilD4Ng" %}

[http://youtu.be/icrbqilD4Ng](http://youtu.be/icrbqilD4Ng)

The API works by connecting to the 'server' which maintains the Minecraft world and issuing commands to change the world in real-time. The api specification is included with the the game, ~/mcpi/api/mcpi_protocol_spec.txt.

The nice people at [Mojang](http://www.mojang.com/), who write Minecraft, also provide class libraries in Java and Python to simplify interactions with the game, which are in the ~/mcpi/api/\[java/python\] directories.

**Create a directory for the program**

```bash
mkdir ~/minecraft-api
```

**Copy the python class library from minecraft to the programs directory**

```bash
cp -r ~/mcpi/api/python/mcpi ~/minecraft-api/minecraft
```

**Create minecraft-api.py python program**

```bash
nano ~/minecraft-api/minecraft-api.py
```

or open Idle and save minecraft-api.py to the minecraft-api directory

**Code**

```python
#www.stuffaboutcode.com
#Raspberry Pi, Minecraft API - the basics

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time

if __name__ == "__main__":

    time.sleep(2)

    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()
    #Post a message to the minecraft chat window
    mc.postToChat("Hi, Minecraft API, the basics, what can you do? ")

    time.sleep(5)
    #Find out your players position
    playerPos = mc.player.getPos()
    mc.postToChat("Find your position - its x=" + str(playerPos.x) + ", y=" + str(playerPos.y) + ", z=" + str(playerPos.z))

    time.sleep(5)

    #Using your players position
    # - the players position is an x,y,z coordinate of floats (e.g. 23.59,12.00,-45.32)
    # - in order to use the players position in other commands we need integers (e.g. 23,12,-45)
    # - so round the players position
    # - the Vec3 object is part of the minecraft class library
    playerPos = minecraft.Vec3(int(playerPos.x), int(playerPos.y), int(playerPos.z))

    #Changing your players position
    mc.postToChat("Move your player - 30 blocks UP!")
    time.sleep(2)
    mc.player.setPos(playerPos.x,playerPos.y + 30,playerPos.z)
    # - wait for you to fall!
    time.sleep(5)

    #Interacting with a block
    # - get the type block directly below you
    blockType =  mc.getBlock(playerPos.x,playerPos.y - 1,playerPos.z)
    mc.postToChat("Interact with blocks - the block below you is of type - " + str(blockType))

    time.sleep(5)

    # - change the block below you to wood planks
    mc.setBlock(playerPos.x,playerPos.y-1,playerPos.z,block.WOOD_PLANKS)
    mc.postToChat("Change blocks - the block below you is now wood planks")

    time.sleep(5)

    #Creating many blocks
    mc.postToChat("Create blocks - making a diamond tower")

    # - loop 20 times
    for up in range(0, 20):
        mc.setBlock(playerPos.x + 1, playerPos.y + up, playerPos.z, block.DIAMOND_BLOCK)

    time.sleep(2)

    # - put you on top of the tower
    mc.postToChat("Dont look down, because Im putting you on top of it!")
    time.sleep(1)
    mc.player.setPos(playerPos.x + 1, playerPos.y + 20, playerPos.z)

    time.sleep(5)

    mc.postToChat("www.stuffaboutcode.com")
```

The complete code repository is also on [github](http://github.com/), [https://github.com/martinohanlon/minecraft-api.git](https://github.com/martinohanlon/minecraft-api.git).

**Run**

Note - minecraft must be running and you must be in a game

```bash
python ~/minecraft-api/minecraft-api.py
```

or if using Idle, click Run Module

**Performance (on pre-release 0.1)**

If you are using the pre-release (version 0.1) of Minecraft you will probably notice that the performance of the API is pretty slow, one of the key reasons for this is that the connection module supplied by mojang, prints the commands sent to the server, which is really useful for debugging but VERY slow - you can turn this off by modifying the connection.py module.

```bash
nano ~/minecraft-api/minecraft/connection.py
```

Change the send function and comment out the 2 print statements, so it looks like this:

```python
    def send(self, f, *data):
        """Sends data. Note that a trailing newline '\n' is added here"""
        s = "%s(%s)\n"%(f, flatten_parameters(data))
        #print "f,data:",f,data
        #print "s",s
        self.drain()
        self.lastSent = s
        self.socket.sendall(s)
```

Check out my [minecraft posts](/minecraft/), such as a game of [Hide and Seek in Minecraft](/posts/raspberry-pi-minecraft-hide-and-seek/), an [Auto Bridge](/posts/raspberry-pi-minecraft-auto-bridge/), no matter where you walk a bridge will always be under your feet or a [Massive Analogue Clock](/posts/raspberry-pi-minecraft-analogue-clock/), big enough so you can walk on the arms.
