---
title: 'Raspberry Pi - Getting an LED to Flash'
date: 2012-11-20 15:00:00 +00:00
tags: [gpio, python, raspberry-pi]
redirect_from:
  - /2012/11/raspberry-pi-getting-led-to-flash.html
---

Anyway I decided to have a go and see what I could do with the Raspberry Pi's GPIO, I like the idea of controlling physical things through software, so with virtually no experience of electronics (Im a software guy) I decided to start small - could I make an LED flash!

{% include youtube.html id="YMxmge8l6jk" %}

Completing this incredibly simple task has meant I have had to learn some new things, gain a load of new skills and buy a load of stuff.

Other than a raspberry Pi, I literally had nothing, so to do this I had to get:

- Soldering iron kit - £9.99 (reduced from £25.99 - bargain!) - Maplin.co.uk
- Raspberry Pi GPIO Breakout Kit - £2.40 - HobbyTronics.co.uk
- Raspberry Pi GPIO 6" cable - £2.40
- 400 point Breadboard - £2.99
- 30 piece Breadboard Jumper Wire Kit - £2.39
- 3mm Red LED / resistor combo (pack 10) - £0.95

I had to solder the breakout board, what a pain that was, before I could build up my simple circuit.

GPIO -> Resistor -> LED -> Ground

Which looked like this.

![](/assets/img/2012/11/sam_0712.jpg)

I then wrote a small python program (using the excellent RPi.GPIO module), which set up the gpio pins and started an loop which set the value of the led to on and off, I used a try/except to capture the keyboard interrupt (ctrl c) so I could clean up before the program exited. I notice from looking online that most people don't perform the clean up at the end, its important you do otherwise you leave the gpio in same state it was when the program finished.

```bash
nano flashled.py
```

```python
import RPi.GPIO as GPIO
import time

# set gpio mode to use BCM pin numbers
GPIO.setmode(GPIO.BCM)
# setup gpio pin 4 as output
GPIO.setup(4, GPIO.OUT)

ledOn = True
# continue until a keyboard interupt is fired
# i.e. user presses CTRL C!
try:
    while True:
        # set gpio output
        GPIO.output(4, ledOn)
        # wait
        time.sleep(1)
        # switch led
        if ledOn == True: ledOn = False
        else: ledOn = True
except KeyboardInterrupt:
    # cleanup GPIO
    GPIO.cleanup()
```

Run the program, which you have to do with sudo otherwise you dont have sufficient permission to access the gpio.

```bash
sudo python flashled.py
```
