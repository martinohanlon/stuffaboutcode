---
title: 'Raspberry Pi - first time setup'
date: 2012-05-28 22:40:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/05/raspberry-pi-first-time-setup.html
---

Anyway, I've got my Raspberry Pi up and running but a lot of it has been done through trial, error and a few SD re-imaging's (down to me screwing it up!)

Each time I setup an SD card for the raspberry pi, these are the tasks I ran first to get it 'up and running'.

**Enable ssh**

Note - this only applies to the debian squeeze (19-04-2012) distro!

If you using the debian squeeze distro access to the Pi via SSH isnt enabled by default, you have to change the name of a file on the SD card to enable it at startup. After you have written your new SD card, browse the contents of the card and you will see a file called "boot_enable_ssh.rc" rename this to "boot.rc".

When the Pi boots, it should now enable the SSH daemon (SSHD) at startup and you will be able to connect to it using a terminal application (e.g. [Putty](http://www.putty.org/)).
 To connect to the Pi you will need to know the IP address, you can find this by using the command

```bash
ifconfig
```

.

**Resize SD card (Debian Squeeze)**
 If you are using Debian Squeeze and yourv'e got an SD card greater than 2GB you will need to resize it in order to use the full capacity of the card; this is due to the debian image being a fixed 2GB and unlike other OS (e.g. Fedora), Debian doesnt automatically resize the image to fill the whole capacity.

The instructions for doing this are well documented on the Pi Wiki, goto [http://elinux.org/RPi_Easy_SD_Card_Setup](http://elinux.org/RPi_Easy_SD_Card_Setup) and follow the section on "Manually resizing the SD card on Raspberry Pi".

WARNING - when creating the new partition DONT use the default for the start block. Use the p command and make note of the start of the main (number 2) partition, it should be 157696. Do it wrong and your going to have to re-image your SD card (I speak from experience!)

**Resize SD Card (Raspbian)**
 If your using Raspbian, you can use the raspi-config utility to resize the SD card, run:

```bash
sudo raspi-config
```

and choose the resize sd card option, which will resize the card next time the Pi is rebooted.

**Change pi user password**
 The Pi comes with a default username and password, as a minimum, its a good idea to change the password of the "pi" user from "raspberry" to something specific, use the command:

```text
passwd
```

**Set root password**
 Debian doesnt set a root password by default, if you want the ability to login as root (although as p4bl0 says its a good idea to use sudo instead), use the command to set a password:

```bash
sudo passwd root
```

**Update apt-get**
 Apt-get is going to become your new best friend using the Pi, its a super easy, very powerful tool for installing software. To make sure you have the latest lists, run apt-get using the command update:

```bash
sudo apt-get update
```

This should start you on your way using Debian on the Raspberry Pi.

If you want to connect your Raspberry Pi to a [NAS drive at startup](http://stuffaboutcode.blogspot.co.uk/2012/05/raspberry-pi-connect-nas-windows-share.html) or give it a [static IP address](http://stuffaboutcode.blogspot.co.uk/2012/05/raspberry-pi-setting-static-ip-address.html), check out my other blog updates
