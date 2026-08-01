---
title: 'Blue Dot - a bluetooth remote for Raspberry Pi'
date: 2017-04-24 22:09:00 +01:00
tags: [gpio, raspberry-pi, robot]
redirect_from:
  - /2017/04/bluedot-bluetooth-remote-for-raspberry.html
---

[Blue Dot](http://bluedot.readthedocs.io/) is a really simple way to add Bluetooth remote control to your Raspberry Pi projects.

![](/assets/img/2017/04/blue_dot_feature.png)

I created Blue Dot after being asked many times at [Picademy](https://www.raspberrypi.org/picademy/) “how can I get rid of all these wires?”.

Blue dot is an [android app](https://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot) (client) and really easy to use [Python library](http://bluedot.readthedocs.io/) which allows you to wirelessly control your Python projects, whether that is a [light switch](http://bluedot.readthedocs.io/en/latest/recipes.html#flash-an-led), [remote camera](http://bluedot.readthedocs.io/en/latest/recipes.html#remote-camera), [robot](http://bluedot.readthedocs.io/en/latest/recipes.html#robot) or anything else you can think of!

{% include youtube.html id="eW9oEPySF58" %}

See the [getting started guide](http://bluedot.readthedocs.io/en/latest/gettingstarted.html) for more info on 'getting started', or follow the tutorial below.

**Installation & Use**
 These instructions assume your Raspberry Pi is running the latest version of [Raspbian with Pixel](https://www.raspberrypi.org/downloads/raspbian/).

You will need a Raspberry Pi with built-in Bluetooth (such as the Pi 3 or Pi Zero W) or a Raspberry Pi and a USB Bluetooth dongle.

**Get the app**
 Download and install the [Blue Dot app](https://play.google.com/store/apps/details?id=com.stuffaboutcode.bluedot) from the google play store.

![](/assets/img/2017/04/bluedotandroid.png)

If you are wondering why there is no iOS app? Its because iOS doesn't support Bluetooth serial comms; you can only really talk to 'standard devices' (cars, speakers, fitness trackers, etc).

**Python library**
 Open a terminal (Menu > Accessories > Terminal) and type:

```bash
sudo apt-get install python3-dbus
sudo pip3 install bluedot
```

Or if you need to use Python 2 (please dont tho!):

```bash
sudo apt-get install python-dbus
sudo pip install bluedot
```

**Pairing**
 In order to communicate over Bluetooth securely you need to pair your phone to your Raspberry Pi.

On your Android phone:

1. Open Settings
2. Select Bluetooth
3. This will make your phone Discoverable

Using your Raspberry Pi

1. Click the bluetooth icon on the taskbar
2. Turn on Bluetooth (if its off)
3. Click Make Discoverable
4. Click Add Device
5. Your phone will appear in the list, select it and click Pair
6. Enter a PIN code

On your Android phone

1. Enter the same PIN code when prompted
2. Click Ok

**Code**
 The simplest way to use the Blue Dot is as a button:

1. Open Python 3 (Menu > Programming > Python 3)
2. Create a new file (File > New File)
3. The following code, will start up the Blue Dot, and wait for it to be pressed:

   ```python
   from bluedot import BlueDot
   bd = BlueDot()
   bd.wait_for_press()
   print("You pressed the blue dot!")
   ```

4. Save your program (File > Save) as mydot.py
5. Run your program (Run > Run Module)
6. Open the Blue Dot app
7. Connect to your Raspberry Pi
8. Press the Blue Dot

As well as waiting for something to happen you can also call functions when the button is pressed, released or the position its pressed moves.

```python
from bluedot import BlueDot
from signal import pause

def say_hello():
    print("Hello World")

def say_goodbye():
    print("goodbye")

bd = BlueDot()
bd.when_pressed = say_hello
bd.when_released = say_goodbye

pause()
```

By using the position of where the button is pressed you can use the Blue Dot like a joystick:

```python
from bluedot import BlueDot
from signal import pause

def dpad(pos):
    if pos.top:
        print("up")
    elif pos.bottom:
        print("down")
    elif pos.left:
        print("left")
    elif pos.right:
        print("right")
    elif pos.middle:
        print("fire")

bd = BlueDot()
bd.when_pressed = dpad

pause()
```

Add to this [gpiozero's Robot](http://gpiozero.readthedocs.io/en/stable/api_boards.html#robot) functions, you can create a Bluetooth controlled robot with very little code.

```python
from bluedot import BlueDot
from gpiozero import Robot
from signal import pause

bd = BlueDot()
robot = Robot(left=(lfpin, lbpin), right=(rfpin, rbpin))

def move(pos):
    if pos.top:
        robot.forward()
    elif pos.bottom:
        robot.backward()
    elif pos.left:
        robot.left()
    elif pos.right:
        robot.right()

def stop():
    robot.stop()

bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop

pause()
```

Check out the [Blue Dot documentation](http://bluedot.readthedocs.io/) for more information and ideas - you really can do a lot with a simple circle :)
