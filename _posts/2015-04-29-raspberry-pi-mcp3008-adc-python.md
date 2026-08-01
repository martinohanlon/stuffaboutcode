---
title: 'Raspberry Pi, MCP3008 ADC & Python'
date: 2015-04-29 21:20:00 +01:00
tags: [gpio, python, raspberry-pi]
redirect_from:
  - /2015/04/raspberry-pi-mcp3008-adc-python.html
---

I'm converting a vintage radio into a Raspberry Pi powered music player and I needed an analogue to digital converter (ADC) to allow my raspberry pi to read the old crusty switched and volume controls.

The MCP3008 ADC is pretty cheap and easy to use with the Pi, so I bagged myself one.

![](/assets/img/2015/04/mcp3008.jpg)

Raspberry Pi Spy has got a really good [tutorial on setting up an MCP3008 to read analogue sensors](http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/) which I followed to get everything running, but the code didn't fit my needs so I created a python class for reading data from the MCP3008.

```python
from spidev import SpiDev

class MCP3008:
    def __init__(self, bus = 0, device = 0, channel = 0):
        self.bus, self.device, self.channel = bus, device, channel
        self.spi = SpiDev()

    def __enter__(self):
        self.open()
        return self

    def open(self):
        self.spi.open(self.bus, self.device)

    def read(self):
        adc = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.spi.close()
```

The class is really easy to use, using Python's 'with' statement to control it:

```python
with MCP3008(channel = 0) as ch0:
    print ch0.read()
```

The code is here - [github.com/martinohanlon/mcp3008](https://github.com/martinohanlon/mcp3008)
