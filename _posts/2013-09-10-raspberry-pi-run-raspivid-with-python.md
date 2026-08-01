---
title: 'Raspberry Pi - Run Raspivid with Python'
date: 2013-09-10 21:29:00 +01:00
tags: [camera, python, raspberry-pi]
redirect_from:
  - /2013/09/raspberry-pi-run-raspivid-with-python.html
---

I've been looking for a way to control raspivid with Python and it seems that a few people have also struggled particularly with starting and stopping raspivid, so I thought I would put together a Python class to control raspivid.

Its a simple class called RaspiVidController which uses threading to not block the calling program but stay alive while the raspivid is running and shut down if you choose to stop it or it times out.

**Usage**
 The class is created by passing 3 parameters:

- filePath - the path of the file where the video is to be saved
- timeout - the time in milliseconds raspivid should run for
- preview - whether raspivid should preview output to the screen

There is also an optional parameter, otherOptions, which can be used to pass any other options to raspivid as a list e.g. \["-fps", "25", "-vf"\].

The 3 key methods in the class are:

- start - start raspivid, this immediately returns to the calling program, but raspivid is running in the background
- stopController - stops the controller and raspivid if its running
- isAlive - returns True if raspivid is still running

There is a more complex example in the code below, but a simple example would be:

```python
#create the controller class
vidcontrol = RaspiVidController("/home/pi/test.h264", 10000, False)

#start raspivid
vidcontrol.start()

#DO SOME STUFF

#stop raspivid
vidcontrol.stopController()
```

**Code**

```python
import os
import subprocess
import threading
import time

RASPIVIDCMD = ["raspivid"]
TIMETOWAITFORABORT = 0.5

#class for controlling the running and shutting down of raspivid
class RaspiVidController(threading.Thread):
    def __init__(self, filePath, timeout, preview, otherOptions=None):
        threading.Thread.__init__(self)

        #setup the raspivid cmd
        self.raspividcmd = RASPIVIDCMD

        #add file path, timeout and preview to options
        self.raspividcmd.append("-o")
        self.raspividcmd.append(filePath)
        self.raspividcmd.append("-t")
        self.raspividcmd.append(str(timeout))
        if preview == False: self.raspividcmd.append("-n")

        #if there are other options, add them
        if otherOptions != None:
            self.raspividcmd = self.raspividcmd + otherOptions

        #set state to not running
        self.running = False

    def run(self):
        #run raspivid
        raspivid = subprocess.Popen(self.raspividcmd)

        #loop until its set to stopped or it stops
        self.running = True
        while(self.running and raspivid.poll() is None):
            time.sleep(TIMETOWAITFORABORT)
        self.running = False

        #kill raspivid if still running
        if raspivid.poll() == True: raspivid.kill()

    def stopController(self):
        self.running = False

#test program
if __name__ == '__main__':

    #create raspivid controller
    vidcontrol = RaspiVidController("/home/pi/test.h264", 10000, False, ["-fps", "25"])

    try:
        print("Starting raspivid controller")
        #start up raspivid controller
        vidcontrol.start()
        #wait for it to finish
        while(vidcontrol.isAlive()):
            time.sleep(0.5)

    #Ctrl C
    except KeyboardInterrupt:
        print "Cancelled"
    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]

        raise

    #if it finishes or Ctrl C, shut it down
    finally:
        print "Stopping raspivid controller"
        #stop the controller
        vidcontrol.stopController()
        #wait for the tread to finish if it hasn't already
        vidcontrol.join()

    print "Done"
```
