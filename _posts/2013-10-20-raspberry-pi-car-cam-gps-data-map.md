---
title: 'Raspberry Pi Car Cam - GPS Data & Map'
date: 2013-10-20 07:34:00 +01:00
tags: [camera, car, gps, python, raspberry-pi]
redirect_from:
  - /2013/10/raspberry-pi-car-cam-gps-data-map.html
---

Ever since I made my [car cam which recorded video and overlaid OBD data](/posts/raspberry-pi-car-cam-overlaid-with-obd/), I've continued to work on the project and in particular on overlaying GPS data. I wanted to create something which was similar to the mini map you get on car racing games which shows you where the car is on the track as its going round.

{% include youtube.html id="Wv_zeE10arg" %}

Im not at a race track often, so I took Mrs O'Hanlon's fiesta for a spin around [Stourbridge ring road](https://maps.google.co.uk/?ll=52.45648,-2.145896&spn=0.015377,0.03047&t=m&z=15), its got speed restrictions and its very busy but it does at least go round and round!

This has been a pretty intense project, probably the most complex I've done with the raspberry pi and has involved several steps:

1. I needed a better way of syncing data gathered by the Pi with video taken on the camera, with my first OBD overlay it was 'VERY' difficult to get it lined up. To acheive this I made a custom version of [Raspivid to allow me to read, in real time, what frame it was on](/posts/raspberry-pi-syncing-data-with-raspivid/)
2. I had to create a [python class to control raspivid](/posts/raspberry-pi-run-raspivid-with-python/)
3. I had to set up a [GPS receiver and create a python class to control it](/posts/raspberry-pi-gps-setup-and-python/)

I then wrote a program which would start up my custom raspivid program, read the frame number alongside the GPS data and create a separate movie which would be the map and the data. I could then overlay the data video on top of the camera video and bingo, mini map on the side of my car video.

The data movie is created by producing an animation of single images. While raspivid is running my program continually reads the current frame count, the GPS data and then using PIL (python imaging library) creates and image of the map and some GPS data (lat, long, speed) for that frame.

The map is made by converting GPS co-ordinates to XY positions using a [Mercator projection](http://en.wikipedia.org/wiki/Mercator_projection) and then each frame is drawn by creating lines between all the sets of XY positions captured since the video started.

Where there are gaps between the frames, I use symbolic links to reference the last frame that was created, so I end up with a data frame (image) for every frame in the car video, this is frame 4993:

![](/assets/img/2013/10/004993.jpg)

I then used mencoder to join all the frames together, in exactly the same way you would for a time lapse video.

My rig was pretty basic, I ran a simple program at boot which started the GPS service, lit an led and waited for a button to be pressed, when the button was pressed it started my program, which ran until it timed out and then the program shut the pi down. Plenty of gaffer tape was also used to stick it to the dashboard!

![](/assets/img/2013/10/carcamgps.jpg)

Finally once I had 2 videos, one from the camera and one from the data, I used [Microsoft Expression](http://www.microsoft.com/en-gb/download/details.aspx?id=18974) (its a free and pretty effective encoder for Windows) to overlay the data onto of the video.

You will find all my code at [https://github.com/martinohanlon/vidGPSOverlay](https://github.com/martinohanlon/vidGPSOverlay), although please don't expect it to just run, there are dependencies for my custom raspivid program as well as the GPS service, so you may need to give it a bit of love to get it going!

The code:

```python
from PIL import Image, ImageFont, ImageDraw
from RaspividController import *
from GPSController import *
import time
import datetime

DATAFRAME_WIDTH = 500
DATAFRAME_HEIGHT = 300
MAP_WIDTH = 300
MAP_HEIGHT = 300
MAX_SCALE = 1
FONT_PATH = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
VIDEOTIME = 600000

def drawPoint(imagedraw,x,y,width,colour):
    imagedraw.ellipse((x-(width/2),y-(width/2),x+(width/2),y+(width/2)), colour)

class DataDrawer():
    def __init__(self, imagesFolder):
        #setup variables
        self.imagesFolder = imagesFolder
        self.imageSize = (300,300)
        self.minX = 99999999999
        self.maxX = -99999999999
        self.minY = 99999999999
        self.maxY = -99999999999
        self.lastFrameNo = 0
        self.lastLat = 0
        self.lastLon = 0
        self.xyPositions = []
        self.mapScale = 1
        self.padX = 0
        self.padY = 0
        #load font
        self.font = ImageFont.truetype(FONT_PATH, 14)
        #create first frame
        self.newDataFrame(1, 0, 0 ,0)

    def newDataFrame(self, frameNo, speed, lat, lon):
        #check to make sure the frame has moved on since last time
        if frameNo > self.lastFrameNo:

            #create sumbolic links between last frame and this frame
            for missingFrameNo in range(self.lastFrameNo+1, frameNo):
                os.symlink(self.imagesFolder + "/" + "{0:06d}".format(self.lastFrameNo) + ".jpg",
                           self.imagesFolder + "/" + "{0:06d}".format(missingFrameNo) + ".jpg")

            #create new image
            frame = Image.new("RGBA", (DATAFRAME_WIDTH, DATAFRAME_HEIGHT))
            frameDraw = ImageDraw.Draw(frame)

            #data
            frameDraw.text((315,10),"    Speed " + str(round(speed,2)),font=self.font)
            frameDraw.text((315,50)," Latitude " + str(lat),font=self.font)
            frameDraw.text((315,90),"Longitude " + str(lon),font=self.font)

            #map
            #only create map if we have a GPS fix
            if lat != 0 and lon != 0:
                #only add a new set of coords if the lat and lon have changed
                if self.lastLat != lat or self.lastLon != lon:
                    #get x & y coords
                    x,y = GpsUtils.latLongToXY(lat, lon)
                    #print "x " + str(x)
                    #print "y " + str(y)

                    #add x,y to list
                    self.xyPositions.append([x,y])

                    #update mins and maxs
                    if x < self.minX: self.minX = x
                    if x > self.maxX: self.maxX = x
                    if y < self.minY: self.minY = y
                    if y > self.maxY: self.maxY = y

                    #persist lat and lon
                    self.lastLat = lat
                    self.lastLon = lon

                    #calculate scale
                    diffX = self.maxX - self.minX
                    #print "diffX " + str(diffX)
                    diffY = self.maxY - self.minY
                    #print "diffY " + str(diffY)
                    if diffX > diffY:
                        if diffX != 0: self.mapScale = MAP_WIDTH / float(diffX)
                        else: self.mapScale = 1
                    else:
                        if diffY != 0: self.mapScale = MAP_HEIGHT / float(diffY)
                        else: self.mapScale = 1
                    #print "mapScale " + str(self.mapScale)

                    #set max scale
                    if self.mapScale > MAX_SCALE: self.mapScale = MAX_SCALE

                    #re-calculate padding
                    self.padX = int((MAP_WIDTH - (diffX * self.mapScale)) / 2)
                    self.padY = int((MAP_HEIGHT - (diffY * self.mapScale)) / 2)

                #draw lines
                for position in range(1, len(self.xyPositions)):
                    #draw line between previous position and this one
                    x1 = self.padX + abs((self.xyPositions[position-1][0] * self.mapScale) - (self.minX * self.mapScale))
                    y1 = self.padY + abs((self.xyPositions[position-1][1] * self.mapScale) - (self.maxY * self.mapScale))
                    x2 = self.padX + abs((self.xyPositions[position][0] * self.mapScale) - (self.minX * self.mapScale))
                    y2 = self.padY + abs((self.xyPositions[position][1] * self.mapScale) - (self.maxY * self.mapScale))
                    #print "coords - " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2)
                    frameDraw.line((x1, y1, x2, y2), fill="white", width=3)

                #draw start and end point
                if len(self.xyPositions) > 1:
                    # start
                    drawPoint(frameDraw, self.padX + abs((self.xyPositions[0][0] * self.mapScale) - (self.minX * self.mapScale)),self.padY + abs((self.xyPositions[0][1] * self.mapScale) - (self.maxY * self.mapScale)), 10, "red")
                    # end
                    drawPoint(frameDraw, self.padX + abs((self.xyPositions[len(self.xyPositions)-1][0] * self.mapScale) - (self.minX * self.mapScale)), self.padY + abs((self.xyPositions[len(self.xyPositions)-1][1] * self.mapScale) - (self.maxY * self.mapScale)), 10, "green")

            #save image
            frame.save(self.imagesFolder + "/" + "{0:06d}".format(frameNo) + ".jpg", "JPEG")
            #update last frame
            self.lastFrameNo = frameNo
```

```python
# main program
if __name__ == "__main__":
    try:
        #create data folder
        localtime = datetime.datetime.now()
        foldername = "/home/pi/dev/cbb/vidGPSOverlay/data/" + str(localtime.year) + str(localtime.month) + str(localtime.day) + str(localtime.hour) + str(localtime.minute) + str(localtime.second)
        if not os.path.exists(foldername): os.makedirs(foldername)

        #start raspivid
        print "starting raspivid controller"
        vidcontrol = RaspiVidController(foldername+"/vid.h264", VIDEOTIME, False, ["-fps", "25", "-vf", "-hf"])
        vidcontrol.start()

        #start gps controller
        print "starting gps contoller"
        gpscontrol = GpsController()
        gpscontrol.start()

        #wait for controllers to startup and gps fix
        time.sleep(3)

        #create data file
        datafile = open(foldername+"/data.csv", "w")

        #create datadrawer object
        datadrawer = DataDrawer(foldername)

        #loop
        while(vidcontrol.isAlive()):
            #get framecount
            framecount = vidcontrol.getFrameCount()

            #wait for a bit as the gps data is a little behind + it allows the processor to have a rest!
            time.sleep(0.1)

            #get gps data
            lat = gpscontrol.fix.latitude
            lon = gpscontrol.fix.longitude
            utc = gpscontrol.utc
            speed = gpscontrol.fix.speed
            speedMPH = speed * GpsUtils.MPS_TO_MPH

            #write data
            dataString = str(framecount) + "," + str(speedMPH) + "," + str(lat) + "," + str(lon) + "," + "\n"
            datafile.write(dataString)
            datadrawer.newDataFrame(int(framecount), speedMPH, lat, lon)

    except KeyboardInterrupt:
        print "Cancelled"

    except:
        print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
        raise

    finally:

        #shutdown raspivid
        vidcontrol.stopController()
        vidcontrol.join()
        print "stopped raspivid controllder"

        #shutdown gps controller
        gpscontrol.stopController()
        gpscontrol.join()
        print "stopped gps controllder"

        #close data file
        print "closing data file"
        datafile.close()
```
