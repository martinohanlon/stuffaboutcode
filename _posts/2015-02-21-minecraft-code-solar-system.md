---
title: 'Minecraft - Code a Solar System'
date: 2015-02-21 00:00:00 +00:00
tags: [adventures-in-minecraft, minecraft, python]
redirect_from:
  - /2015/02/minecraft-code-solar-system.html
---

*Update - I took this further and created a DeathStar to blow up planets too, in a [Minecraft Star Wars](http://www.stuffaboutcode.com/2015/03/minecraft-star-wars.html) animation.*

Every wondered how big the Sun is? Well check out the picture below.

![](/assets/img/2015/02/2015-02-20_22.00.31.png)

If the Earth was the size of 1 block in Minecraft the Sun would have a diameter of 109 blocks and if the distance was to scale 11728 blocks away!

{% include youtube.html id="kI2piJOi3nU" %}

What about the size and distance of the other planets in blocks?

| Planet | Diameter | Distance |
| --- | --- | --- |
| Mercury | 0.38 | 4539.04 |
| Venus | 0.95 | 8482.28 |
| Earth | 1.0 | 11727.81 |
| Mars | 0.53 | 17866.1 |
| Jupiter | 11.21 | 61037.94 |
| Saturn | 9.45 | 112378.49 |
| Uranus | 4.01 | 225188.15 |
| Neptune | 3.88 | 352391.03 |
| Pluto | 0.19 | 460175.6 |

I didn't build this Solar System I coded it. I took information about the diameter and distance of the planets from [Nasa's Planetary Fact Sheet](http://nssdc.gsfc.nasa.gov/planetary/factsheet/) and created a fairly simple program which created spheres of the right size based on a factor of Kilometers to Blocks.

The code is on github at [github.com/martinohanlon/minecraft-solarsystem](https://github.com/martinohanlon/minecraft-solarsystem) or you can download the [Minecraft world](https://drive.google.com/file/d/0BwqjqhNUlUf1MzlFS3ZKRHo5Z3c/view?usp=sharing).

You can change the ratio of the sun and planets by changing the constant KMTOBLOCK, which is the number of kilometers per block - be careful though, the sun will be VERY big if the value is too low. You might have to increase the height of your Minecraft world too.

```python
#Minecraft - Code a solar system
#Martin O'Hanlon
#www.stuffaboutcode.com

#import minecraft api library
import mcpi.minecraft as minecraft
import mcpi.block as block

# draw hollow sphere
def drawHollowSphere(mc, x1, y1, z1, radius, blockType, blockData=0):
    # create sphere
    for x in range(radius*-1,radius):
        for y in range(radius*-1, radius):
            for z in range(radius*-1,radius):
                if (x**2 + y**2 + z**2 < radius**2) and (x**2 + y**2 + z**2 > (radius**2 - (radius * 2))):
                    mc.setBlock(x1 + x, y1 + y, z1 +z, blockType, blockData)

# draw sphere
def drawSphere(mc, x1, y1, z1, radius, blockType, blockData=0):
    # create sphere
    for x in range(radius*-1,radius):
        for y in range(radius*-1, radius):
            for z in range(radius*-1,radius):
                if (x**2 + y**2 + z**2 < radius**2):
                    mc.setBlock(x1 + x, y1 + y, z1 +z, blockType, blockData)

#setup constants (all values in kilometers)
SUN = 1391684
#name, diameter, distance, blockId, blockData
PLANETS = (("mercury", 4879, 57900000, block.WOOL.id, 7),
           ("venus", 12104, 108200000, block.WOOL.id, 0),
           ("earth", 12756, 149600000, block.WOOL.id, 11),
           ("mars", 6792, 227900000, block.WOOL.id, 14),
           ("jupiter", 142984, 778600000, block.WOOL.id, 4),
           ("saturn", 120536, 1433500000, block.WOOL.id, 8),
           ("uranus", 51118, 2872500000, block.WOOL.id, 3),
           ("neptune", 49528, 4495100000, block.WOOL.id, 10),
           ("pluto", 2390, 5870000000, block.WOOL.id, 6))

#how many km's to a block
# change this value to have different sizes in the solar system
KMTOBLOCK = 12756.0

#middle of the minecraft sky, where the centre of the planets will be
MCMIDDLE = 75

#program
print("Minecraft Planets")
print("1 block = {} kilometers".format(KMTOBLOCK))

#connect to minecraft
mc = minecraft.Minecraft.create()

#set the middle of the solar system
pos = minecraft.Vec3(0,MCMIDDLE,0)

#create the sun
sunDiameter = round(SUN / KMTOBLOCK, 2)
sunRadius = int(round(sunDiameter / 2))
print("Sun - Diameter = {} blocks".format(sunDiameter))
drawHollowSphere(mc, pos.x, pos.y, pos.z, sunRadius, block.WOOL.id, 1)
gapToLeave = (sunDiameter / 2) + 20
pos.z = pos.z + gapToLeave

#loop through the planets
for planet in PLANETS:
    name = planet[0]
    diameter = round(planet[1] / KMTOBLOCK, 2)
    radius = int(round(diameter / 2))
    distance = round(planet[2] / KMTOBLOCK, 2)
    print("{} - Diameter = {} blocks - Distance = {} blocks".format(name, diameter, distance))
    #if the diameter is less than 1.5 draw a single block
    if diameter < 1.5:
        mc.setBlock(pos.x, pos.y, pos.z, planet[3], planet[4])
        pass
    else:
        drawSphere(mc, pos.x, pos.y, pos.z, radius, planet[3], planet[4])
        pass

    gapToLeave = (diameter / 2) + 20
    pos.z = pos.z + gapToLeave

#move the player to the sun
mc.player.setPos(0,0,0)
```

Have fun.
