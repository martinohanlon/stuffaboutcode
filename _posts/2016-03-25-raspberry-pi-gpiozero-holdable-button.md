---
title: 'Raspberry Pi gpiozero holdable button'
date: 2016-03-25 08:03:00 +00:00
tags: [gpio, python, raspberry-pi]
redirect_from:
  - /2016/03/raspberry-pi-gpiozero-holdable-button.html
---

The current release of [gpiozero](https://gpiozero.readthedocs.org/) doesn't have the support to hold a button down e.g. when a button is pressed and then held down for 1 second something happens.

This is really useful when building hardware projects and you want 1 button to do 2 things, say turn something on when pressed, and turn off when held down.

I needed this for a project so I thought I would create a new HoldableButton class using gpiozero. Hopefully this will be [incorporated into gpiozero](https://github.com/RPi-Distro/python-gpiozero/issues/115), but until then you can use the class below.

The code is also available [here](https://gist.github.com/martinohanlon/20cee570d6ea4ca0b7ad) as a gist.

You will need to add the HoldableButton class to your Python program:

```python
from gpiozero import Button
from threading import Timer

class HoldableButton(Button):
    def __init__(self, pin=None, pull_up=True, bounce_time=None,
                 hold_time=1, repeat=False):

        super(HoldableButton, self).__init__(pin, pull_up, bounce_time)

        # Set Button when_pressed and when_released to call local functions
        # cant use super() as it doesn't support setters
        Button.when_pressed.fset(self, self._when_button_pressed)
        Button.when_released.fset(self, self._when_button_released)

        self._when_held = None
        self._when_pressed = None
        self._when_released = None
        self._is_held = False

        self.hold_time = hold_time
        self.repeat = repeat
        self._held_timer = None

    #override button when_pressed and when_released
    @property
    def when_pressed(self):
        return self._when_pressed

    @when_pressed.setter
    def when_pressed(self, value):
        self._when_pressed = value

    @property
    def when_released(self):
        return self._when_released

    @when_released.setter
    def when_released(self, value):
        self._when_released = value

    @property
    def when_held(self):
        return self._when_held

    @when_held.setter
    def when_held(self, value):
        self._when_held = value

    @property
    def is_held(self):
        return self._is_held

    def _when_button_pressed(self):
        self._start_hold()
        if self._when_pressed != None:
            self._when_pressed()

    def _when_button_released(self):
        self._is_held = False
        self._stop_hold()
        if self._when_released != None:
            self.when_released()

    def _start_hold(self):
        self._held_timer = Timer(self.hold_time, self._button_held)
        self._held_timer.start()

    def _stop_hold(self):
        if self._held_timer != None:
            self._held_timer.cancel()

    def _button_held(self):
        self._is_held = True
        if self._when_held != None:
            if self.repeat and self.is_pressed:
                self._start_hold()
            self._when_held()
```

Using the HoldableButton class is pretty simple, similar to the gpiozero [Button](https://gpiozero.readthedocs.org/en/v1.1.0/api_input.html#button) class and can be swapped for the Button class with no other changes.

```text
holdbutton = HoldableButton(pin, hold_time = 1, repeat = False)
```

You have to pass a **pin** number and optional hold_time and repeat values:

- hold_time - is the number of seconds after the button is pressed before the button is consider 'held'
- repeat - is a boolean and if set to True will occur 'button held' events to be repeated after each hold_time

You can use all the same methods and properties of the [Button](https://gpiozero.readthedocs.org/en/v1.1.0/api_input.html#button) class, when_pressed, when_released, is_pressed, etc.

There are 2 additional properties **is_held**, which will return a boolean stating whether the button has been held down for the 'hold_time' and **when_held** which when assigned a function will cause the function to be called when the button is held down.

```python
def myheldfunction():
    print("button held")

holdbutton.when_held = myheldfunction
```

Now when a button is held down, the function will be called and "button held" printed.
