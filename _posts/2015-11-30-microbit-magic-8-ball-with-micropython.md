---
title: 'MicroBit Magic 8 Ball with MicroPython'
date: 2015-11-30 18:41:00 +00:00
tags: [microbit, python]
redirect_from:
  - /2015/11/microbit-magic-8-ball-with-micropython.html
---

I wanted to create something with the MicroBit which used the on-board accelerometer and I settled on a [Magic 8 Ball](https://en.wikipedia.org/wiki/Magic_8-Ball), the fortune-telling pool ball which when shaken and asked a question it provides, a, often cryptic, response.

{% include youtube.html id="b-8cRJiEKbo" %}

The program works out whether the MicroBit has been shaken by:

- Reading the x, y, z values from the accelerometer in a loop and adding them together to get a total force exposed
- Getting the difference between the last reading and the current reading
- If the difference is greater than a threshold, you assume the MicroBit has been shaken

I wrapped this into a function wait_for_shake, which perhaps not unsurprisingly blocks until the MicroBit is shaken!

```python
import microbit

TOLERANCE = 3000

def get_accel_total():
    x = microbit.accelerometer.get_x()
    y = microbit.accelerometer.get_y()
    z = microbit.accelerometer.get_z()
    return x + y + z

def wait_for_shake():
    shaken = False
    last = get_accel_total()
    while not shaken:
        this = get_accel_total()
        diff = last - this
        if diff < 0: diff = diff * -1
        if diff > TOLERANCE:
            shaken = True
        last = this
        microbit.sleep(50)
```

Its not 'very' sophisticated but it works.

Once I had this working it pretty simple to add a loop which waited for the MicroBit to be shaken and scrolled a random message on the LED screen.

```python
MESSAGES = ["It is certain", "Dont count on it", "Ask again"]
while True:
    microbit.display.print("8")
    wait_for_shake()
    microbit.display.clear()
    microbit.sleep(2000)
    message = microbit.random(len(MESSAGES))
    microbit.display.scroll(MESSAGES[message])
```

If you want to add your own messages, just add them to the MESSAGES list.

You can find the code [here](https://github.com/martinohanlon/microbit-micropython/blob/master/examples/8ball.py) and other examples in my [microbit-micropython GitHub repository](https://github.com/martinohanlon/microbit-micropython).

![](/assets/img/2015/11/8ballmicrobit.jpg)
