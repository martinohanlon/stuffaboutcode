---
title: 'Raspberry Pi Touchscreen Portrait'
date: 2017-05-05 18:07:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2017/05/raspberry-pi-touchscreen-portrait.html
---

I recently wanted to turn my Raspberry Pi Official Touchscreen portrait (i.e. sideways!), which turns out is a bit of pain.

![](/assets/img/2017/05/img_20170501_174954646_hdr.jpg)

Turning the display is relatively easy but making the touch work is more difficult - there was a [set of instructions on the Raspberry Pi forum](https://www.raspberrypi.org/forums/viewtopic.php?p=1084567#p1084567), but a [recent update to Jessie meant they no longer worked](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=172025), so I pulled this set of instructions together:

**Install xinput:**

```bash
sudo apt-get install xinput
```

**Rotate the display by editing config.txt:**

```bash
sudo nano /boot/config.txt
```

.. add this to the buttom of the file:

```text
display_rotate=1
```

Use Ctrl X, Yes to Save
**Create a script to rotate the touchscreen:**

```bash
nano /home/pi/touch_rotate.sh
```

.. add the following command

```text
xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix'  0 1 0 -1 0 1 0 0 1
```

**Make the script executable:**

```bash
chmod +x touch_rotate.sh
```

**Make the script run when the GUI starts by editing autostart:**

```bash
sudo nano ~/.config/lxsession/LXDE-pi/autostart
```

.. add this to the bottom to run your script

```text
@/home/pi/touch_rotate.sh
```

**Reboot:**

```bash
sudo reboot
```
