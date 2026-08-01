---
title: 'Microbit - get data from USB'
date: 2016-03-25 18:15:00 +00:00
tags: [microbit, python]
redirect_from:
  - /2016/03/microbit-get-data-from-usb.html
---

As part of my [Minecraft, a Microbit and an X-Wing](http://www.stuffaboutcode.com/2015/12/minecraft-microbit-and-x-wing.html) project, I used the USB to read data from the Microbit's accelerometer and buttons to make the X-Wing move.

[@NCSComputing](https://www.blogger.com/) on twitter has started re-using the code to make other things happen, so thought it would be a good idea to write up how it works, so others can do the same.

![](/assets/img/2016/03/celdeexwoaakuwq.jpg)

To make this work you need one program which runs on the Microbit and prints data and a second runs on your computer (a Raspberry Pi, PC, Mac, anything with a USB port) which reads the data via a serial connection.

![](/assets/img/2016/03/img_20160325_175730786_hdr.jpg)

See [github.com/martinohanlon/microbit-serial](https://github.com/martinohanlon/microbit-serial) for the code for both of these programs.

**The Microbit**
 The [microbitreaddata.py](https://github.com/martinohanlon/microbit-serial/blob/master/microbitreaddata.py) python program runs on the Microbit, gets the data and prints it to the output, which in this case is the USB serial connection, and should be flashed to your computer using the [Python editor](https://www.microbit.co.uk/create-code):

```python
from microbit import *

REFRESH = 500

def get_data():
    x, y, z = accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()
    a, b = button_a.was_pressed(), button_b.was_pressed()
    print(x, y, z, a, b)

def run():
    while True:
        sleep(REFRESH)
        get_data()

display.show('M')
run()
```

**Your Computer**
 The [clientreaddata.py](https://github.com/martinohanlon/microbit-serial/blob/master/clientreaddata.py) python program runs on the computer and reads the data using [pyserial](http://pyserial.readthedocs.org/en/latest/pyserial.html#installation):

```python
import serial

#the port will depend on your computer
#for a raspberry pi it will probably be /dev/ttyACM0
#PORT = "/dev/ttyACM0"
#for windows it will be COM(something)
PORT = "COM3"

BAUD = 115200

s = serial.Serial(PORT)
s.baudrate = BAUD
s.parity   = serial.PARITY_NONE
s.databits = serial.EIGHTBITS
s.stopbits = serial.STOPBITS_ONE

try:
    while True:
        #read a line from the microbit, decode it and
        # strip the whitespace at the end
        data = s.readline().rstrip()

        #split the accelerometer data into x, y, z
        data_s = data.split(" ")
        x, y, z = data_s[0], data_s[1], data_s[2]
        a, b = data_s[3], data_s[4]
        print(x,y,z)
        print(a,b)

finally:
    s.close()
```

The values of the accelerometer will be put into the variables x, y, z and the buttons in a & b.

**Setting the PORT**
 You will have to change the [PORT variable in the clientreaddata.py program](https://github.com/martinohanlon/microbit-serial/blob/master/clientreaddata.py#L5) to the comm port that the Microbit is connected to on your computer.

For a Raspberry Pi it is probably "/dev/ttyACM0", in the event it isn't, unplug the Microbit and run:

```bash
ls /dev/tty*
```

![](/assets/img/2016/03/microbitpiport.jpg)

Then plug the Microbit and run the command again, the new device which appears will be the port of your Microbit.

For Windows it will be "COM#", the # being a number, the easiest way is to look in [Device Manager](http://lmgtfy.com/?q=open+windows+device+manager) for the "mBed Serial Port (COM#)"

![](/assets/img/2016/03/microbit-windowscommport.jpg)
