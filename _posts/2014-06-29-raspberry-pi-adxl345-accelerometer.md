---
title: 'Raspberry Pi - ADXL345 Accelerometer & Python'
date: 2014-06-29 21:04:00 +01:00
tags: [gpio, python, raspberry-pi]
redirect_from:
  - /2014/06/raspberry-pi-adxl345-accelerometer.html
---

![](/assets/img/2014/06/2013_03_24_img_1453-1024.jpg)
 A little while ago I got my hands on a [Adafuit ADXL345](http://www.adafruit.com/products/1231) (a triple axis accelerometer) from [pimoroni](http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer), you can also get them from Amazon ([US](http://www.amazon.com/gp/product/B00JHJSGF6/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00JHJSGF6&linkCode=as2&tag=stuabocod-20&linkId=DHPXMV6VJVTDJ536), [UK](http://www.amazon.co.uk/gp/product/B00BYGGM92/ref=as_li_ss_tl?ie=UTF8&camp=1634&creative=19450&creativeASIN=B00BYGGM92&linkCode=as2&tag=stuabocod-21)) if that's easier, and I finally got around to setting it up.

Pimoroni also provide a really useful python module to interacting with the ADXL345 which you can get from github - [https://github.com/pimoroni/adxl345-python](https://github.com/pimoroni/adxl345-python).

**Connecting it up**
 Wiring up the accelerometer is pretty easy, there are only 4 connections:

Raspberry Pi -> ADXL345:

- GND - GND
- 3V - 3V3
- SDA - SDA
- SCL - SCL

**Configure your Pi**
 The ADXL345 supports both I2C and SPI connections, I used I2C, which requires some configuration on the Pi:

Add the I2C modules to the Pi's configuration:

```bash
sudo nano /etc/modules
```

add the following lines:

```text
i2c-bcm2708
i2c-dev
```

Remove I2C from the blacklist:

```bash
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```

comment out:

```text
blacklist i2c-bcm2708
```

so its:

```text
#blacklist i2c-bcm2708
```

Reboot to make the changes:

```bash
sudo shutdown -r now
```

**Install Software**
 You will need to install some software:

```bash
sudo apt-get install python-smbus i2c-tools git-core
```

**Test ADXL345**
 You can check that your ADXL345 is found on the I2C bus, by running:

```bash
sudo i2cdetect -y 1
```

You should see a device at address 53

![](/assets/img/2014/06/i2cdetect.png)

Download the ADXL345 pimoroni python library from github:

```bash
git clone https://github.com/pimoroni/adxl345-python
```

Run the example code and test it is working:

```bash
cd adxl345-python
sudo python example.py
```

You should see the G readings from the ADXL345.

![](/assets/img/2014/06/adxl345.png)

If you get 0.000G for all axis then something probably isn't set-up correctly.

**Writing your own python program**
 The adxl345-python project from pimoroni contains a python module for reading data from the ADXL345 perhaps not unsurprisingly called "adxl345.py", inside there is a class called "ADXL345" which is how you to interact with the accelerometer

The program below imports the module, instantiates an ADXL345 object and reads values from the accelerometer as g-forces.

```python
#import the adxl345 module
import adxl345

#create ADXL345 object
accel = adxl345.ADXL345()

#get axes as g
axes = accel.getAxes(True)
# to get axes as ms^2 use
#axes = accel.getAxes(False)

#put the axes into variables
x = axes['x']
y = axes['y']
z = axes['z']

#print axes
print x
print y
print z
```

**Change sensitivity**
 You can change the sensitivity of the ADXL345 by using the .setRange() method of the class.

The default range is 2g which means that the maximum G the ADXL345 can measure is 2.048, but at a high degree of sensitivity, you can change it so the maximum is 2g, 4g, 8g or 16g but with a lower level of sensitivity using:

```text
accel.setRange(adxl345.RANGE_2G)
accel.setRange(adxl345.RANGE_4G)
accel.setRange(adxl345.RANGE_8G)
accel.setRange(adxl345.RANGE_16G)
```

Its a great accelerometer and really easy to use in your python projects.
