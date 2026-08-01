---
title: 'Raspberry Pi - Setting a Static IP Address'
date: 2012-05-30 09:09:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/05/raspberry-pi-setting-static-ip-address.html
---

Anyway, I needed to change my Raspberry Pi so it had a static IP address. I've got a typical network at home, wireless router in the cupboard under the stairs, a couple of powerline ethernet plugs and broadband provided by someone who offers little support for anything out of the ordinary and using dhcp to dynamically allocate the IP address to the Pi was causing a few headaches - just because it kept changing!

Setting the Pi to use a static IP address was the way forward.

**Modify /etc/network/interfaces**
 The Raspberry Pi's network configuration is stored in the file /etc/network/interfaces, so this needs to be modified in order to change it from using dhcp to get an IP address to assigning a static one.

```bash
sudo nano /etc/network/interfaces
```

First step is to comment out the line:

```text
iface eth0 inet [dhcp]/[manual]
```

by placing a # at the start:

```text
# iface eth0 inet [dhcp]/[manual]
```

Next step is to add the static IP configuration to the end of the file, this will be specific to your network setup, but for most 'home' users it will be pretty similar.

You will need to know the IP address of your router, it is probably 192.168.1.1 or 192.168.2.1, but you can check by logging into your router and checking the configuration.

You will also need to decide on an IP address for your Pi that is within the range of your routers IP address e.g. 192.168.1.99.

So in my setup, where I wanted to give the Raspberry Pi an address of 192.168.1.99 and my router has the address 192.168.1.1; I added the following to the bottom of the /etc/network/interfaces file.

```text
iface eth0 inet static
     address 192.168.1.99
     netmask 255.255.255.0
     network 192.168.1.0
     broadcast 192.168.1.255
     gateway 192.168.1.1
```

Ctrl X to save the changes

**Restart**
 I found that using the raspbian distro I had to reboot the Pi for the network changes to take effect:

```bash
sudo shutdown -r now
```

**Test**
 I tested the change by making sure I could still ping my router

```text
ping 192.168.1.1
```
