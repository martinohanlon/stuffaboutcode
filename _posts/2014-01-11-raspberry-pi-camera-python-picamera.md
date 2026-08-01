---
title: 'Raspberry Pi - Camera, Python & PiCamera'
date: 2014-01-11 08:32:00 +00:00
tags: [camera, python, raspberry-pi]
redirect_from:
  - /2014/01/raspberry-pi-camera-python-picamera.html
---

![](https://www.modmypi.com/image/cache/data/raspberry-pi-expansion-boards/raspberry-pi/raspberry-pi-camera-board-close-800x800.JPG)For my [raspberry pi car cam project](http://www.stuffaboutcode.com/2013/07/raspberry-pi-car-cam-overlaid-with-obd.html) I needed to find a better way of [syncing data with video](http://www.stuffaboutcode.com/2013/09/raspberry-pi-syncing-data-with-raspivid.html) so I modified [raspivid](http://www.stuffaboutcode.com/2013/09/raspberry-pi-syncing-data-with-raspivid.html) and created [python class to run raspivid](http://www.stuffaboutcode.com/2013/09/raspberry-pi-run-raspivid-with-python.html). I did this hack mainly because I couldn't be bothered and didn't really have the skill to write an interface to the camera in python, luckily someone else has!

[Picamera](https://pypi.python.org/pypi/picamera) is a python interface for the raspberry pi camera board, created by Dave Jones (aka [waveform80](https://github.com/waveform80)), think of it as the python equivalent of raspivid and raspistill. Using picamera you can 'programmatically' take videos and images and is much easier way of capturing video/images in your python projects.

There is some great documentation for Picamera at [picamera.readthedocs.org](http://picamera.readthedocs.org/), which includes detailed instructions about how to install picamera, getting started and a complete reference for the module. You can also find the code at [github.com/waveform80/picamera](https://github.com/waveform80/picamera).

**Install picamera**

```bash
sudo apt-get install python-picamera
```

**Take a video**

The following code will record a video and save it to 'foo.h264'.

```python
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_preview()
    camera.start_recording('foo.h264')
    camera.wait_recording(60)
    camera.stop_recording()
    camera.stop_preview()
```

**Take a picture**

The following code will take a single picture and save it to 'foo.jpg'.

```python
import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera.capture('foo.jpg')
```

There is much more information on [http://picamera.readthedocs.org](http://picamera.readthedocs.org/) and its well worth a read.

There are also some great functions such as split recording, capturing images while recording and pulling out data from the encoder while the video is recording (such as frame number).
