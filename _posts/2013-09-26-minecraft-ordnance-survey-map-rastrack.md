---
title: 'Minecraft Ordnance Survey Map & Rastrack'
date: 2013-09-26 22:39:00 +01:00
tags: [minecraft, python, raspberry-pi]
redirect_from:
  - /2013/09/minecraft-ordnance-survey-map-rastrack.html
---

![](/assets/img/2013/09/2013-09-26_22.08.01.png)

*The Pi's of London*

I noticed an [article](http://www.bbc.co.uk/news/technology-24177844) on BBC News reporting about Ordnance Survey (the key mapping company in the UK) had create a [Minecraft map of the whole of the UK](http://www.ordnancesurvey.co.uk/innovate/developers/minecraft-map-britain.html) based on their data.

I downloaded the map and put in on [raspberry pi powered minecraft server](/posts/raspberry-pi-setup-minecraft-server/) and tweeted a picture of it.

David Whale (@whaleygeek) had an idea, use the data from Ryan Walmsley (@ryanteck)'s [rastrack.co.uk](http://rastrack.co.uk/) to show the Pi's of the UK in minecraft.

{% include youtube.html id="ccdeaeN4cQk" %}

It works like this:

- I took the Minecraft map Ordnance Survey (OS) and put it on a [raspberry pi powered minecraft server](/posts/raspberry-pi-setup-minecraft-server/)
- I got the locations of all the raspberry pi's logged on [http://rastrack.co.uk](http://rastrack.co.uk/) and parsed the data using python
- I converted the latitude and longitude for each pi to OS grid reference, by making a call to a website created by David Whale [http://www.thinkingbinaries.com/test/gpsmap/geodesic.php5](http://www.thinkingbinaries.com/test/gpsmap/geodesic.php5), passing the lat and lon and parsing the returned grid reference
- I converted the OS grid reference to minecraft location by porting the code in the converter page supplied by OS to python [http://oslabs.s3.amazonaws.com/convert.html](http://oslabs.s3.amazonaws.com/convert.html)
- I used the raspberryjuice plugin to use Minecraft:Pi edition API code to create raspberries in the sky at the right co-ordinates

If you want to have a look connect minecraft to **martinohanlon.servebeer.com:25565**.

If you 'hit' (right click with a sword) the middle red wool block in the raspberry, it will tell you who the Pi belongs too.

The code is really hacky, I pulled it together in a few hours, I will look at how I can make this a little more robust and also so it can be re-run to pick up new Pi's added into rastrack.co.uk.

```python
#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
import json
import urllib2
import sys
import math
import random

def getOSGridFromLatLon(lat, lon):
    # this uses david whale's website to get the OS Grid Ref
    gridrefUrl = "http://www.thinkingbinaries.com/test/gpsmap/geodesic.php5?latitude=[lat]&longitude=[lon]&a_latlong=calc&gridreflet=&gridrefEN="
    phraseToFind =  '<input type="text" name="gridreflet" value="'
    dataLenght = 10

    # setup lat, lon in url
    gridrefUrl = gridrefUrl.replace("[lat]", lat)
    gridrefUrl = gridrefUrl.replace("[lon]", lon)
    #print gridrefUrl

    # get webpage
    aResp = urllib2.urlopen(gridrefUrl)
    page = aResp.read()
    #print page

    # strip data from webpage
    phrasePos = page.find(phraseToFind)
    dataStart = phrasePos+len(phraseToFind)
    dataEnd = dataStart + page[dataStart:].find('"')
    gridRef = page[dataStart:dataEnd]
    #print gridRef

    # has a grid ref been returned
    if gridRef == "[range!]":
        gridRef = ""
    else:
        # convert 8 number grid ref to 6 e.g. SO87828991 to SO878899
        gridRef = gridRef[:5] + gridRef[6:9]

    #print gridRef
    return gridRef

# ported from http://oslabs.s3.amazonaws.com/convert.html
def gridToMC(gridRef):

    heightOfGrid = 70

    # get numeric value of letter reference A->0, B->1, C->2, etc
    letter1 = ord(gridRef[0:1])-65
    letter2 = ord(gridRef[1:2])-65

    # shuffle down letters after 'I' [since 'I' is not used in grid]
    if letter1 > 7: letter1 -= 1
    if letter2 > 7: letter2 -= 1

    #print letter1
    #print letter2

    # convert grid letters into 100km-square indexes from false origin (grid square SV)
    ea = ((letter1 - 2) % 5) * 5 + (letter2 % 5)
    no = (19 - math.floor(letter1 / 5) * 5) - math.floor(letter2 / 5)
    tp_ea = ea * 2000
    tp_no = 28000 - (no * 2000)

    # skip grid letters to get numeric part of ref
    gridRefNos = gridRef[2:]
    ea = gridRefNos[:len(gridRefNos)/2]
    no = gridRefNos[len(gridRefNos)/2:]

    #print gridRefNos
    #print ea
    #print no

    # normalise to 1m grid, rounding up to centre of grid square
    #  100m (three-figure)
    if len(gridRefNos) == 6: multiplier = 2
    #  1000m (two figure
    if len(gridRefNos) == 4: multiplier = 20
    # x
    tp_ea = tp_ea + (int(ea) * multiplier)
    # z
    tp_no = tp_no - (int(no) * multiplier)

    #print tp_ea
    #print tp_no

    return tp_ea,heightOfGrid,tp_no

# converts minecraft xyz to be reflective of spawn point
#  as raspberry juice uses spawn point as 0,0,0
def convertXYZToSpawnXYZ(x,y,z):
    spawnX = 9000
    spawnY = 100
    spawnZ = 26000
    # minus a random number from Y so raspberry's arent on top of each other in highly populated areas
    return int(x - spawnX), int(y - spawnY - random.randint(0,9)), int(z - spawnZ)

def buildRaspberry(mc,x,y,z):
    #red wool
    mc.setBlock(x+-1,y+0,z+1, block.WOOL.id, 14)
    mc.setBlock(x+1,y+0,z+1, block.WOOL.id, 14)
    mc.setBlock(x+0,y+0,z+0, block.WOOL.id, 14)
    mc.setBlock(x+-2,y+0,z+0, block.WOOL.id, 14)
    mc.setBlock(x+2,y+0,z+0, block.WOOL.id, 14)
    mc.setBlock(x+-1,y+0,z+-1, block.WOOL.id, 14)
    mc.setBlock(x+1,y+0,z+-1, block.WOOL.id, 14)
    mc.setBlock(x+0,y+0,z+2, block.WOOL.id, 14)
    #black wool
    mc.setBlock(x+0,y+0,z+1, block.WOOL.id, 15)
    mc.setBlock(x+-1,y+0,z+0, block.WOOL.id, 15)
    mc.setBlock(x+1,y+0,z+0, block.WOOL.id, 15)
    mc.setBlock(x+0,y+0,z+-1, block.WOOL.id, 15)
    #green wool
    mc.setBlock(x+0,y+0,z+-2, block.WOOL.id, 13)
    mc.setBlock(x+-1,y+0,z+-3, block.WOOL.id, 13)
    mc.setBlock(x+-2,y+0,z+-3, block.WOOL.id, 13)
    mc.setBlock(x+1,y+0,z+-3, block.WOOL.id, 13)
    mc.setBlock(x+2,y+0,z+-3, block.WOOL.id, 13)

# main
if __name__ == "__main__":

    # open log file
    logfile = open("logfile.txt",'w')
    logfile.write("started\n")

    # load rastrack json data
    #  get the data from rastrack
    aResp = urllib2.urlopen("http://www.rastrack.co.uk/data2.php")
    page = aResp.read()
    #  replace escape chars \ in json cause it screws up
    page = page.replace("\\", " ")
    #  strip the 'var data = ' bit and load into json object
    rastrackData = json.loads(page[11:])
    logfile.write("loaded rastrack json\n")
    # connect to minecraft
    mc = minecraft.Minecraft.create()
    # loop pi's in rastrack data
    for pi in rastrackData["pi"]:
        try:
            #if 1==1:
            # pull out lat and long
            lat = str(pi["latitude"])
            lon = str(pi["longitude"])
            #print lat
            #print lon

            # get the Ordnance Survey grid reference
            gridRef = getOSGridFromLatLon(lat, lon)

            # has a gridRef been returned?
            if gridRef != "":
                logfile.write(str(gridRef) + "\n")

                # convert OS grid to MC xyz
                mcX, mcY, mcZ = gridToMC(gridRef)
                logfile.write("x = " + str(mcX) + " y = " + str(mcY) + " z = " + str(mcZ) + "\n")

                # make xyz reflective of spawn point
                x,y,z = convertXYZToSpawnXYZ(mcX, mcY, mcZ)
                logfile.write("x = " + str(x) + " y = " + str(y) + " z = " + str(z) + "\n")

                # create raspberry in MC
                buildRaspberry(mc,x,y,z)

                # save mc xyz to rastrack json
                pi["x"] = x
                pi["y"] = y
                pi["z"] = z

        except:
            logfile.write("Unexpected error:" + str(sys.exc_info()[0]) + "\n")
            raise

    # save json data to file
    logfile.write("saving rastrack json\n")
    outputFile = open("rastrackData.json", "w")
    json.dump(rastrackData, outputFile)

    logfile.close()
```
