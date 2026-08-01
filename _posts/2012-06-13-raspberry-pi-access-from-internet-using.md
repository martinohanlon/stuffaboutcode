---
title: 'Raspberry Pi - access from the internet using no-ip'
date: 2012-06-13 21:51:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/06/raspberry-pi-access-from-internet-using.html
---

Anyway... As part of my [iPlayer custom podcast](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-bbc-iplayer-personal.html) solution I needed to be able to connect to my Pi externally over the internet.

**Sign up for a host with no-ip.com**

My ISP assigns IP addresses dynamically (pretty typical but not very useful for accessing from the internet), so I setup a free account with [www.no-ip.com](http://www.no-ip.com/) who offer a free dynamic dns service whereby they provide you with a URL (e.g. myhost.no-ip.org) and they redirect internet traffic from that URL to your IP address.

You can either login to no-ip.com and update your ip address manually, as and when it changes (not practical!), or no-ip provide client software which will run in the background on your Pi and periodically update your no-ip host with your IP address.

Note - Its important you create yourself an account and add a host on no-ip before installing the client as you will need your account details as part of the install.

**Install no-ip client**
 (most of this detail is taken from [http://www.no-ip.com/support/guides/update_clients/setting_up_linux_update_client.html](http://www.no-ip.com/support/guides/update_clients/setting_up_linux_update_client.html) but there are a few discrepancies)

***Create a directory for the client software***

```bash
mkdir /home/pi/noip
cd /home/pi/noip
```

***Download the client software***

```bash
wget http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz
```

***Extract the archive***

```bash
tar vzxf noip-duc-linux.tar.gz
```

***Navigate to the archive directory***
 Note - use 'ls' to check the directory name create when the archive was extracted, it was noip-2.1.9-1 when I installed the client.

```bash
cd noip-2.1.9-1
```

***Compile and install***
 The client was compiled and installed on the Raspberry Pi, using the following commands:

```bash
sudo make
sudo make install
```

During the install I was asked to proide my login, password and a refresh interval.

***Run the client***
 The client is run using the following command:

```bash
sudo /usr/local/bin/noip2
```

The client runs continuously until shutdown or the Raspberry Pi is shutdown, if you want to set up your Pi so the no-ip client is started at boot, check out this [blog](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-run-program-at-start-up.html) which describes how to [configure the application to start at boot](http://stuffaboutcode.blogspot.co.uk/2012/06/raspberry-pi-run-program-at-start-up.html).

I then had to configure my broadband router to forward the specific port I wanted my Pi to service (e.g. port 80 for www) to the internal IP address of my Raspberry Pi, see [portforward.com](http://portforward.com/) for more information about port forwarding guides and info; you may find setting up port forwarding simpler if your raspberry Pi has a static IP address, see this [post](http://stuffaboutcode.blogspot.co.uk/2012/05/raspberry-pi-setting-static-ip-address.html) on how to [set a static IP address](http://stuffaboutcode.blogspot.co.uk/2012/05/raspberry-pi-setting-static-ip-address.html).
