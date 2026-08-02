---
title: 'Talking Minecraft - Rasberry Jamboree 2014'
date: 2014-03-21 21:14:00 +00:00
tags: [minecraft, raspberry-pi]
redirect_from:
  - /2014/03/rasberry-jamboree-2014.html
---

I recently attended the Raspberry Jamboree in Manchester on the 28th February. It was great fun and really good to meet a load of other people from the Raspberry Pi community.

I did a presentation about [Minecraft](/minecraft/) on the Raspberry Pi and why I think its a good thing.

{% include youtube.html id="089CoGZ8UpI" %}

I also ran a Hacking Minecraft workshop, which you can [download here](https://docs.google.com/document/d/17zjTIY6iO8amK21jKYJVOQruycdDRxusavw-RBBW-Is/edit?usp=sharing).

You can find more information and code listings for the demos below:

[A tutorial on using the Minecraft: Pi edition API](/posts/minecraft-pi-edition-api-tutorial/).
[Minecraft Music Visualiser](/posts/minecraft-music-visualiser/).
[Minecraft Auto Bridge](/posts/raspberry-pi-minecraft-auto-bridge/).
[Minecraft Snake Game](/posts/raspberry-pi-minecraft-snake/).
[Minecraft Cannon](/posts/raspberry-pi-minecraft-cannon/).

I also demo'd a program to built a house which then follows you wherever you go.

**Download and Run**
 You can download the code direct from github, [https://github.com/martinohanlon/minecraft-houses](https://github.com/martinohanlon/minecraft-houses), so run minecraft, open/create a world and follow the instructions:

```bash
sudo apt-get install git-core
cd ~
git clone https://github.com/martinohanlon/minecraft-houses.git
cd minecraft-houses
python minecraft-house-follow.py
```

**Code**

```python
#www.stuffaboutcode.com
#Raspberry Pi, Minecraft Snake

#import the minecraft.py module from the minecraft directory
import minecraft
#import minecraft block module
import block
#import time, so delays can be used
import time
#import random module to create random number
import random

HOUSEWIDTH=6
HOUSEHEIGHT=2

def buildHouse(mc, x, y, z):
    #draw floor
    mc.setBlocks(x,y-1,z,x+HOUSEWIDTH,y-1,z+HOUSEWIDTH,block.GRASS.id)

    #draw walls
    mc.setBlocks(x, y, z, x+HOUSEWIDTH, y+HOUSEHEIGHT, z, block.STONE.id)
    mc.setBlocks(x+HOUSEWIDTH, y, z, x+HOUSEWIDTH, y+HOUSEHEIGHT, z+HOUSEWIDTH, block.STONE.id)
    mc.setBlocks(x+HOUSEWIDTH, y, z+HOUSEWIDTH, x, y+HOUSEHEIGHT, z+HOUSEWIDTH, block.STONE.id)
    mc.setBlocks(x, y, z+HOUSEWIDTH, x, y+HOUSEHEIGHT, z, block.STONE.id)

    #draw windows
    mc.setBlocks(x+(HOUSEWIDTH/2)-2,y+1,z,x+(HOUSEWIDTH/2)-2,y+2,z,block.GLASS.id)
    mc.setBlocks(x+(HOUSEWIDTH/2)+2,y+1,z,x+(HOUSEWIDTH/2)+2,y+2,z,block.GLASS.id)

    #draw door
    #cobble arch
    mc.setBlocks(x+(HOUSEWIDTH/2)-1,y,z,x+(HOUSEWIDTH/2)+1,y+2,z,block.COBBLESTONE.id)
    # clear space for door
    mc.setBlocks(x+(HOUSEWIDTH/2),y,z,x+(HOUSEWIDTH/2),y+1,z,block.AIR.id)

    #draw torches
    mc.setBlock(x+(HOUSEWIDTH/2)-1,y+2,z-1,block.TORCH.id,1)
    mc.setBlock(x+(HOUSEWIDTH/2)+1,y+2,z-1,block.TORCH.id,1)

    #draw roof
    mc.setBlocks(x,y+HOUSEHEIGHT+1,z,x+HOUSEWIDTH,y+HOUSEHEIGHT+1,z+HOUSEWIDTH,block.WOOD_PLANKS.id)

def clearHouse(mc, x, y, z):
    mc.setBlocks(x,y-1,z,x+HOUSEWIDTH,y+HOUSEHEIGHT+1,z+HOUSEWIDTH,block.AIR.id)

#main program
if __name__ == "__main__":

    time.sleep(3)

    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()

    playersPath = []
    lastPlayerPos = mc.player.getTilePos()
    playersPath.append(lastPlayerPos)

    lastHousePos = None

    while(True):
        playerPos = mc.player.getTilePos()
        if playerPos != lastPlayerPos:
            playersPath.append(playerPos)
        lastPlayerPos = playerPos

        #when a player has moved 15 blocks, moved their house and reset the path
        if len(playersPath) == 15:

            #clear the old house (if there was one)
            if lastHousePos is not None:
                clearHouse(mc, lastHousePos.x, lastHousePos.y, lastHousePos.z)

            #create house 10 blocks back, we dont want the house on top of us!
            lastHousePos = playersPath[5]
            lastHousePos.y = mc.getHeight(lastHousePos.x,lastHousePos.z)
            buildHouse(mc,lastHousePos.x, lastHousePos.y, lastHousePos.z)

            #clear list
            playersPath[:] = []
```
