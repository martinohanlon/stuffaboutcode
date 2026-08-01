---
title: 'Raspberry Pi Syncing data with RaspiVid'
date: 2013-09-03 19:46:00 +01:00
tags: [c, camera, raspberry-pi]
redirect_from:
  - /2013/09/raspberry-pi-syncing-data-with-raspivid.html
---

Since I used a [Raspberry Pi to capture video and data from my car and then overlay the data](http://www.stuffaboutcode.com/2013/07/raspberry-pi-car-cam-overlaid-with-obd.html) onto the video, I've been looking for an easier way of synchronising data with video, simply put "Its was a right pain in the bum".

It was difficult because while you can note the time the data was captured, you don't know what the 'time' will be in the video because you get drift (e.g. if you specify 30 frames a second, it isn't always 'exactly' 30 frames a second, sometimes its more, sometimes its less, sometimes frames are dropped) and the longer the video the more 'drift'.

After investigating several ways of doing this I decided what I need was a way of 'asking' raspivid while it was running "where it was", that way I could tag that information alongside the data and use it to sync it to video later.

To do this I had to answer a number of questions:

- What data in the video encoding process could I use? *I settled on current frame number*
- How could I find the frame number? *By modifying raspivid to 'count frames'*
- How could I count frames? *By examining the contents of a 'buffer' before it was written to disk to see if it contained an end frame and if it did increment a count*
- How could I get the frame count out while it was running? *By using a shared memory segment and semaphore*

I have forked the raspberrypi/userland repository (which contains raspivid), [https://github.com/martinohanlon/userland](https://github.com/martinohanlon/userland), the raspivid code is in /host_applications/linux/apps/raspicam/RaspiVid.c and all my changes are commented with the heading MaOH. View my custom raspivid code [here](https://github.com/martinohanlon/userland/blob/master/host_applications/linux/apps/raspicam/RaspiVid.c).

I created a really simple demo, which recorded the screen and noted the frame number and key pressed before formatting it as a subtitle file which I then encoded to the movie file, to test the synchronisation. The quality is terrible but it does work.

{% include youtube.html id="BswR2eNEwQA" %}

**Compile userland fork**
 Clone my userland fork

```bash
mkdir ~/code
cd ~/code
git clone git://github.com/martinohanlon/userland.git
```

See this [post](http://www.stuffaboutcode.com/2013/08/compile-raspberry-pi-userland-raspivid.html) to on [how to compile userland](http://www.stuffaboutcode.com/2013/08/compile-raspberry-pi-userland-raspivid.html), if you want to keep the original raspivid software (probably a good idea!), dont run the command sudo make install.

My custom raspivid program will be compiled in the

```text
~/code/userland/build/bin
```

directory.

**Using my custom raspivid**

The custom version of raspivid I created works exactly the same as the original, but if the program is outputting the video to a file, it also outputs the frame count at run time to shared memory.

```text
~/code/userland/build/bin/raspivid -o test.h264
```

**Reading the frame count**

To get the frame count while raspivid is running, you need to read the value from system V shared memory and to protect the value from corruption while reading it, you need to use a semaphore.

The process works like this:

1. Acquire the semaphore, which will stop raspivid updating it
2. Read the frame count from shared memory
3. Release the semaphore

In order to use the shared memory and semaphore you need the keys:

- shared memory - 20130821
- semaphore - 20130822

Any programming language which can read from shared memory and use semaphores should be able to do this. The frame count is written to the shared memory as a string to make it easier to consume, messing about with integer types can be bit painful.

**Example Python code**
 The following code reads the frame count from shared memory 100 times, pausing for 0.5 seconds between each read. It used a great python module, [sysv_ipc](http://semanchuk.com/philip/sysv_ipc/), which greatly simplifies the interaction with shared memory, see [http://semanchuk.com/philip/sysv_ipc/](http://semanchuk.com/philip/sysv_ipc/) for more information, download and install instructions.

To install sysv_ipc:

```bash
sudo apt-get install python-dev
wget http://semanchuk.com/philip/sysv_ipc/sysv_ipc-0.6.5.tar.gz
tar -xf sysv_ipc-0.6.5.tar.gz
cd sysv_ipc-0.6.5
sudo python setup.py install
```

Python code:

```python
import sysv_ipc
import time

# Open shared memory object
memory = sysv_ipc.SharedMemory(20130821)

# Open semaphore
semaphore = sysv_ipc.Semaphore(20130822)

for count in range(0,100):
    print "acquiring semaphore"
    # Acquire the semaphore using a 2 second timeout
    semaphore.acquire(2)

    # Read value from shared memory
    frameCount = memory.read()

    # Release the semaphore
    semaphore.release()

    print "released semaphore"

    # Find the 'end' of the string and strip
    i = frameCount.find('\0')
    if i != -1:
        frameCount = frameCount[:i]

    print "value is " + frameCount

    # wait
    time.sleep(0.5)
```

Remember to run raspivid before running this code, otherwise you will be presented with an error saying the shared memory / semaphore doesn't exist.

I would welcome any improvements to this and would actively encourage you to download my code and "have a go".
