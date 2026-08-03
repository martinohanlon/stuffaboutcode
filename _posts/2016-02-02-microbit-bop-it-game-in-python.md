---
title: 'Microbit - a Bop-it game in Python'
date: 2016-02-02 21:08:00 +00:00
tags: [microbit, python]
redirect_from:
  - /2016/02/microbit-bop-it-game-in-python.html
---

I wanted to create a simple game for the Microbit and after bring brought an [R2D2 Bop-it game](https://www.amazon.co.uk/dp/B013UC5XUG?tag=stuabocod-21) I thought I would make one whereby you have to press the A and B buttons in time.

Lets start by importing the microbit and random libraries:

```python
from microbit import *
import random
```

Create some constants, one for the SPEED which is the amount of time in between each bop for each level, and one for the LEVELUP's which is the amount of points at each level:

```text
SPEED = {0: 1000, 1: 750, 2: 650, 3: 600, 4: 550, 5: 500}
LEVELUP = (5, 10, 15, 20, 25, 30)
```

Create 4 functions which when caused will show A, B, a tick and a cross:

```python
def show_a():
    display.clear()
    display.show("A")

def show_b():
    display.clear()
    display.show("B")

def show_tick():
    display.clear()
    display.set_pixel(0, 3, 9)
    display.set_pixel(1, 4, 9)
    display.set_pixel(2, 3, 9)
    display.set_pixel(3, 2, 9)
    display.set_pixel(4, 1, 9)

def show_cross():
    display.clear()
    display.show("X")
```

Create a function which will wait for the button to be pressed, returning True if it is and False if it isn't:

```python
def wait_for_button(rightbutton, wrongbutton):
    rightpressed = False
    wrongpressed = False

    started = running_time()
    now = running_time()

    while now - started < SPEED[level]:
        if rightbutton.is_pressed():
            rightpressed = True
        if wrongbutton.is_pressed():
            wrongpressed = True
        now = running_time()

    if rightpressed == True and wrongpressed == False:
        return True
    else:
        return False
```

Set 3 variables for the level, the score and one which will be set to True when the game is over:

```python
level = 0
score = 0
gameover = False
```

Scroll "BopBit" on the screen to show its the start of the game:

```python
display.scroll("BopBit")
```

Loop until the game is over:

```python
while gameover == False:
```

Randomly pick an action (either A or B), show it on the screen and wait for a button to be pressed:

```python
    success = False

    #randomly pick an A or B button
    action = random.randint(0, 1)

    #wait for the button to be pressed
    if action == 0:
        show_a()
        success = wait_for_button(button_a, button_b)
    elif action == 1:
        show_b()
        success = wait_for_button(button_b, button_a)
```

If the player pressed the right button in time show a tick and increase the score or show a cross:

```python
    if success:
        show_tick()
        score = score + 1
        #if the score is a levelup score increase the level
        if score in LEVELUP:
            level = level + 1
    else:
        show_cross()
        gameover = True
```

Wait for a small amount of time (half the current speed):

```python
    sleep(int(SPEED[level] / 2))
```

After the game is over, sleep for 1 second, and display the players score on a loop:

```python
sleep(1000)
while True:
    display.scroll("{} points".format(score))
```

You can view the [complete code](https://github.com/martinohanlon/microbit-micropython/blob/master/examples/bopbit.py) in my [Microbit MicroPython examples repository](https://github.com/martinohanlon/microbit-micropython) on github.

How about taking it further by adding new actions such as shaking or a connecting up a speaker and adding a sound track,
