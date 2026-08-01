---
title: 'Microbit making Minecraft Earthquakes'
date: 2016-09-20 20:03:00 +01:00
tags: [microbit, minecraft]
redirect_from:
  - /2016/09/microbit-making-minecraft-earthquakes.html
---

In this tutorial you are going to connect your Microbit up to your Raspberry Pi and program them so that when your Microbit is shaken it creates an earthquake in Minecraft.

![](/assets/img/2016/09/ezgif.com-optimize.gif)

This is part of a workshop I delivered at [PyConUK 2016](http://2016.pyconuk.org/) - [download the complete worksheet](https://drive.google.com/open?id=1VElMfrxKNG5qnwfQ0mx5o8-IeuYRfRatxlRqzInn6GE).

You are going to connect your micro:bit’s pins to the Raspberry Pi gpio pins using some cables and crocodile clips; programs on the micro@bit and Raspberry Pi will make Steve shake in Minecraft.

**Install mu**
 To put you python program on your Micro:bit you will need the editor [mu](https://github.com/mu-editor/mu).

Open a Terminal (Menu > Accessories > Terminal) and type:

```bash
sudo apt-get update
sudo apt-get install mu
```

**Angry micro:bit**
 The first task is to program your micro:bit so it gets angry when it's shaken.

- Connect your micro:bit to the Raspberry Pi using the USB cable.
- Open mu to create a new Python program for your micro:bit by clicking on Menu > Programming > mu.
- Click New and type the following code into the editor.

```python
from microbit import *
while True:
    if accelerometer.current_gesture() == "shake":
        display.show(Image.ANGRY)
    else:
        display.show(Image.HAPPY)
```

- Click Flash to put your program on your micro:bit.

When the yellow light on the back of your micro:bit stops flashing your program will run.
 You should see a happy face on your micro:bit - until it’s shaken!

![](/assets/img/2016/09/mbhappy.png)

Any errors will be scrolled on your micro:bit’s leds; if you get an error check your code carefully.

**Pins**

Now you need to finish your micro:bit program so that it turns pin 0 on and off when it's shaken

- Go back to Mu and modify your program so that it turns pins 0 on (1) and off (0) when shaken.

```python
from microbit import *
while True:
    if accelerometer.current_gesture() == "shake":
        display.show(Image.ANGRY)
        pin0.write_digital(1)
    else:
        display.show(Image.HAPPY)
        pin0.write_digital(0)
```

- Click Flash to put your program on your micro:bit.

**Connect it up**
 Next you will use a jumper cable and a crocodile clip to connect your micro:bit to the Raspberry Pi.

- Connect the jumper cable to GPIO17 on the Raspberry Pi
- Clip the crocodile clip to the end of the jumper cable
- Clip the other end of the crocodile clip to pin0 on the micro:bit

![](/assets/img/2016/09/imgp6235_crop.jpg)![](/assets/img/2016/09/raspberry-pi-gpio-layout-model-b-plus-rotated-2700x900.png)

**Shake Steve**
 You now need to create your Minecraft program to shake Steve when the micro:bit is shaken and pin0 is set to 1.

- Click Menu > Games > Minecraft: Pi Edition to run the game.
- Click Start Game, then click Create New (or choose an existing one) to enter a world:
- Press ESC to go back to the Minecraft menu but leave the game playing.
- Open Python IDLE by clicking Menu > Programming > Python 3.
- Use File > New Window to create a new program and save it as ‘mc_micro.py’.
- Type the following code into the program to import the modules you will need

```python
from mcpi.minecraft import Minecraft
from gpiozero import DigitalInputDevice
from time import sleep
```

- Create a connection to Minecraft using the code.

```text
mc = Minecraft.create()
```

- Post a message to the chat window.

```text
mc.postToChat("Micromine bitcraft earthquake")
```

- Run your program by clicking Run > Run Module.

You should see your message appear in the Minecraft chat window.

Any errors will be displayed in the Python Shell in red.

Update your program to shake Steve, by adding the following code at the bottom of your program.

- Create a pin which is connected to Pi GPIO 17 and micro:bit pin 0.

```text
pin0 = DigitalInputDevice(17)
```

- Create a loop which constants gets Steve’s position.

```python
while True:
    sleep(0.1)
    pos = mc.player.getPos()
```

- If pin0 is on (1) it adds 0.5 to Steve’s height (y).

```python
    if pin0.value == 1:
        pos.y = pos.y + 0.5
        mc.player.setPos(pos)
```

- Run your program by clicking Run > Run Module.

Shake your micro:bit and Steve will be shaken in Minecraft.

**Challenges**

Can you change the program so that it creates a more realistic earthquake by adding random values to the x, y, z values.

Complete the [worksheet](https://drive.google.com/open?id=1VElMfrxKNG5qnwfQ0mx5o8-IeuYRfRatxlRqzInn6GE) from [PyConUK 2016](http://2016.pyconuk.org/) which includes using the micro:bit buttons to makes blocks disappear and appear.
