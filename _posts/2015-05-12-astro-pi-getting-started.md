---
title: 'Astro Pi / Sense HAT - Getting Started Tutorial'
date: 2015-05-12 19:09:00 +01:00
tags: [python, raspberry-pi]
redirect_from:
  - /2015/05/astro-pi-getting-started.html
---

Edit - this post has been updated to reflect the changes made in install and sense-hat module name.

You have managed to get your hands on an [Astro-Pi](http://astro-pi.org/) Sense HAT board... Lucky you. If you need some help getting started - read on.

![](/assets/img/2015/05/astropi.jpg)

**Install Sense HAT / Astro-Pi software**
 If you haven't got a recent version of Raspbian you will need to install the Sense HAT software.

Open up a terminal and run the following commands.

```bash
sudo apt-get update
sudo apt-get install sense-hat
sudo pip-3.2 install pillow
```

You will need to reboot your Raspberry Pi for the changes to take effect.
**Example programs**
 The nice people at [Raspberry Pi](http://www.raspberrypi.org/) have provided some example programs which are a great way to test if everything is working

Open a terminal, create a director, copy the Astro-Pi example's and list the contents:

```bash
mkdir ~/sensehatexamples
cp /usr/src/sense-hat/examples ~/sensehatexamples -a
cd ~/sensehatexamples
ls
```

![](/assets/img/2015/05/astro-pi-examples.jpg)

Each of the files which ends in .py is an example python program and can be run from the terminal using

```bash
sudo python [name_of_example.py]
```

e.g.

```bash
sudo python rainbow.py
```

![](/assets/img/2015/05/astropirainbow.jpg)

Run each of the example program and see what they do:

- colour_cycle.py - loops through all the colours on the led matrix.
- compass.py - shows a dot on the led matrix which points north
- pygame_joysticks - shows how to use the pygame module to read the mini joystick and display the joystick direction on the led matrix
- rainbow.py - shows a rainbow of colours on the led matrix
- rotation.py - shows how to rotate the led matrix and shows a question mark
- space_invader.py - displays the space invader icon in the space_invader.png file on the led matrix
- text_scroll.py - a scrolling text message appears on the led matrix

**Hello Space**
 Writing your first program for the Astro Pi board is really simple, there is a great [Astro Pi python library](https://github.com/astro-pi/astro-pi-hat) that takes away most of the complex code and leaves you to have fun.

Because the Astro Pi board needs access to the GPIO pins you will need to run your programs as a 'super user' using sudo. I think the easiest way of doing this is to start the Python editor IDLE using sudo that way you can run your programs without having to do anything special.

Open IDLE as a super user by starting a terminal and typing:

```bash
sudo idle3 &
```

The python shell will now start, click File -> New Window to create a new program.

Import the AstroPi class and create the object:

```python
from sense_hat import AstroPi

ap = AstroPi()
```

You can use the show_message() function to display a message on the LED matrix:

```python
ap.show_message("Hello Space")
```

To run your program, click Run -> Run Module.

You should see hello space scroll on the LED matrix.

**LED Matrix**

The AstroPi class allow you to interact with the colour LED matrix using the set_pixel(x, y, red, green, blue) function. x and y are the coordinates on the led matrix starting top left 0-7. red, green, blue are the colour values 0-255.

To make the top left pixel red you would use:

```python
ap.set_pixel(0, 0, 255, 0, 0)
```

To make the bottom right pixel white (all colours) you would use:

```python
ap.set_pixel(7, 7, 255, 255, 255)
```

Add the code above to your program and run it.

To turn a pixel off you would set it to black (no colours):

```python
ap.set_pixel(7, 7, 0, 0, 0)
```

You can clear all the pixels using:

```python
ap.clear()
```

The clear() function can also be used to set all the pixels to one colour by passing the r,g,b values in a list i.e. blue:

```python
ap.clear([0,0,255])
```

**Reading Sensors**
 The Astro Pi board comes with the following sensors which you can read:

- Orientation (yaw, pitch & roll) via an accelerometer, 3D gyroscope and magnetometer
- Pressure
- Humidity
- Temperature (via the pressure and humidity sensors)

Create a new program and as before import the AstroPi class and create the object:

```python
from sense-hat import AstroPi

ap = AstroPi()
```

The pressure in millibars can read using the get_pressure() function:

```python
pressure = ap.get_pressure()
print(pressure)
```

The percentage of relative humidity can be read using the get_humidity function:

```python
humidity = ap.get_humidity()
print(humidity)
```

The temperature in degrees Celsius can be read using the get_temperature() function.

```python
temp = ap.get_temperature()
print(temp)
```

The Astro Pi boards humidity and pressure sensors can both read temperature and you can specify which one you want to use with the get_temperature_from_humidity() and get_temperature_from_pressure() functions:

```python
temp = ap.get_temperature_from_pressure()
print(temp)

temp = ap.get_temperature_from_humidity()
print(temp)
```

Orientation of the Astro Pi board can be read in degrees and radians using the functions get_orientation_radians() and get_orientation_degrees(). Both functions return the 3 [flight axes](http://en.wikipedia.org/wiki/Aircraft_principal_axes) of yaw, pitch and roll as a python dictionary:

```python
orientation = ap.get_orientation_degrees()
print(orientation["yaw"])
print(orientation["pitch"])
print(orientation["roll"])

orientation = ap.get_orientation_radians()
print(orientation["yaw"])
print(orientation["pitch"])
print(orientation["roll"])
```

Run the program to see the sensor values displayed.

These are just a sample of the functions available you can view the full documentation here [http://pythonhosted.org/sense-hat/](http://pythonhosted.org/sense-hat/).
