---
title: 'Raspberry Pi CPU Temperature'
date: 2015-06-24 22:49:00 +01:00
tags: [python, raspberry-pi]
redirect_from:
  - /2015/06/raspberry-pi-cpu-temperature.html
---

For a project I am working on I needed a really quick way of reading the Raspberry Pi's CPU temperature, most of the solutions I found ran the command line

```text
vcgencmd measure_temp
```

... via Python's subprocess function and parsed the result.

This just wasn't quick enough for my project as I needed something which would gather lots of data, not just the cpu temperature every second, so I pulled together my own module and class which reads the data directly from /sys/class/thermal/thermal_zone0/temp.

You can find the module at [github.com/martinohanlon/CPUTemp](https://github.com/martinohanlon/CPUTemp), but to use it, just add the following CPUTemp class to your code:

```python
class CPUTemp:
    def __init__(self, tempfilename = "/sys/class/thermal/thermal_zone0/temp"):
        self.tempfilename = tempfilename

    def __enter__(self):
        self.open()
        return self

    def open(self):
        self.tempfile = open(self.tempfilename, "r")

    def read(self):
        self.tempfile.seek(0)
        return self.tempfile.read().rstrip()

    def get_temperature(self):
        return self.get_temperature_in_c()

    def get_temperature_in_c(self):
        tempraw = self.read()
        return float(tempraw[:-3] + "." + tempraw[-3:])

    def get_temperature_in_f(self):
        return self.convert_c_to_f(self.get_temperature_in_c())

    def convert_c_to_f(self, c):
        return c * 9.0 / 5.0 + 32.0

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.tempfile.close()
```

Then to read the temperature use:

```python
with CPUTemp() as cpu_temp:
    print("{} C".format(cpu_temp.get_temperature()))
    print("{} F".format(cpu_temp.get_temperature_in_f()))
```
