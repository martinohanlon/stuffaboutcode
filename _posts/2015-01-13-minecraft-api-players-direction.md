---
title: 'Minecraft API - Player''s Direction'
date: 2015-01-13 21:26:00 +00:00
tags: [adventures-in-minecraft, minecraft, python]
redirect_from:
  - /2015/01/minecraft-api-players-direction.html
---

![](/assets/img/2015/01/2014-06-03_22.16.15.png)One of the questions I get asked a lot about the Minecraft: Pi edition APi is "how can I get the direction the player is facing?" and I have always had to say "sorry you can't do that".

While I can't change the API for Minecraft: Pi edition I can change [RaspberryJuice](http://www.stuffaboutcode.com/2014/10/minecraft-raspberryjuice-and-canarymod.html) - so I decided to add functions to allow you to find out where the player is looking. You can download the RaspberryJuice plugin [Canarymod](http://canarymod.net/plugins/raspberry-juice) and [Bukkit](http://dev.bukkit.org/bukkit-plugins/raspberryjuice/).

I have also created a new [Adventures in Minecraft starterkit](http://www.stuffaboutcode.com/p/adventures-in-minecraft-forum.html?place=msg%2Fadventures-in-minecraft-forum%2FG3MuBXDwoqw%2Fp3KE-yc3OkgJ) which includes the new version of RapsberryJuice and everything you need to use the new api functions.

{% include youtube.html id="b6Y9pIGC4c8" %}

The 3 new functions in the api are:

- player.getRotation() - return the angle of rotation between 0 and 360
- player.getPitch() - returns the angle of pitch between -90 and 90
- player.getDirection() - returns a unit-vector of x,y,z pointing in the direction the player is facing

The functions also work with the entities as well so you can use entity.getRotation(), entity.getPitch() and entity.getDirection()

Here are the couple of code examples I demo in the video.

Get the players rotation and pitch angles:

```python
#import the minecraft module
import mcpi.minecraft as minecraft

#create a connection to minecraft
mc = minecraft.Minecraft.create()

while True:
    #get the players rotational angle
    angle = mc.player.getRotation()
    #get the player up and down angle
    pitch = mc.player.getPitch()
    mc.postToChat(str(angle) + " : " + str(pitch))
```

Create a block in front of the player using getDirection():

```python
import mcpi.minecraft as minecraft
import mcpi.block as block
import time

#how far in front of the player the block will be
BLOCKDISTANCE = 5

mc = minecraft.Minecraft.create()

while True:
    #get the position
    pos = mc.player.getPos()
    #get the direction
    direction = mc.player.getDirection()
    #calc the position of the block in front of the player
    x = round(pos.x + (direction.x * BLOCKDISTANCE))
    y = round(pos.y + (direction.y * BLOCKDISTANCE) + 1)
    z = round(pos.z + (direction.z * BLOCKDISTANCE))
    mc.setBlock(x,y,z,block.DIAMOND_BLOCK)
    time.sleep(0.1)
    mc.setBlock(x,y,z,block.AIR)
```

I hope you find the new api functions useful.
