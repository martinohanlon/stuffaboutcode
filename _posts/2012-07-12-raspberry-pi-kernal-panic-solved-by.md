---
title: 'Raspberry Pi - Kernal Panic solved by using rpi-update'
date: 2012-07-12 13:16:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/07/raspberry-pi-kernal-panic-solved-by.html
---

## Updating Raspberry Pi Firmware and Kernel

Anyway... I was having some stability issues with the raspberry pi when running my iPlayer personal podcast and was being presented with a **"Kernel panic - not syncing : Fatal exception in interrupt"** error every couple of days. My issues seem to be consistent with those experienced by other people when the raspberry pi is under heavy load.

Some advice suggested updating the pi's firmware and kernel, which initially sounded a bit scary, but there is a great tool called [rpi-update](https://github.com/Hexxeh/rpi-update/) which automates the process. Once I did this my raspberry pi became much more stable and I havent experienced a Kernel panic since.

These instructions were taken from [https://github.com/Hexxeh/rpi-update/](https://github.com/Hexxeh/rpi-update/) head here for more information and options, but if you want to follow the 'default' update you can use the information below.

**Download rpi-update**

```bash
sudo wget http://goo.gl/1BOfJ -O /usr/bin/rpi-update && chmod +x /usr/bin/rpi-update
```

**Install ca-certificates**

```bash
sudo apt-get install ca-certificates
```

**Run rpi-update**
*Note - rpi-update must be run as root*

```bash
sudo rpi-update
```

The first time you run rpi-update you will likely be presented with an error:

```text
/opt/vc/sbin/vcfiled: error while loading shared libraries: libvchiq_arm.so: cannot open shared object file: No such file or directory
```

This is, apparently, nothing to worry about and the update will have completed successfully, see [forum](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=50&t=9704) for more details.
