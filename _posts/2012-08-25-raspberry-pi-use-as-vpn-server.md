---
title: 'Raspberry Pi - Use as a VPN Server'
date: 2012-08-25 21:20:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/08/raspberry-pi-use-as-vpn-server.html
---

Anyway, I find myself needing access to my internal network when I'm out and about and decided to look at using my Raspberry Pi as a VPN server.

For the VPN virgin's out there, a VPN allows you to connect to your internal network securely over the internet and gain access to the resources you have at home, perhaps you want to read documents off your NAS drive, open an SSH connect to your Pi, or if your away in a different country you can use your home internet connection to access services which are restricted to your country (i.e. BBC iPlayer in the UK or Hulu in the US).

I choose to use PPTP on the Raspberry Pi, its not as secure as other services such as OpenVPN, but its much easier to setup, maintain and as a typical home user the additional risk was outweighed by the simple maintenance.

I used the instructions on this [blog](http://wellsb.com/post/29412820494/raspberry-pi-vpn-server) as the basis for installing PPTP on the Raspbian distribution.

**Install PPTP**

```bash
sudo apt-get install pptpd
```

**Configure PPTP**
 I needed to specify the IP addresses I wanted my VPN to use in the pptpd configuration file.

```bash
sudo nano /etc/pptpd.conf
```

Adding the following configuration lines to the bottom of the file, you will see some examples commented out:

```text
localip 192.168.1.99
remoteip 192.168.1.100-110
```

localip is the IP address of your Raspberry Pi, my Raspberry Pi has static IP address making this step easier if your network assigns IP addresses dynamically (pretty typical), see this [post](http://stuffaboutcode.blogspot.com/2012/05/raspberry-pi-setting-static-ip-address.html) for details on how to [set a static IP address](http://stuffaboutcode.blogspot.com/2012/05/raspberry-pi-setting-static-ip-address.html).

remoteip is a range of IP addresses which your Raspberry Pi will give out to clients who join the VPN. You need to give sufficient range to cope with the number of clients that may need to connect.

I modified the pptpd options file:

```bash
sudo nano /etc/ppp/pptpd-options
```

Adding the following to the bottom of the file:

```text
ms-dns 192.168.1.1
nobsdcomp
noipx
mtu 1490
mru 1490
```

ms-dns is the ip address of your local dns service, more than often this will be the IP address of your router.

I created a user and password in the chap-secrets config file, this will be the user and password you login as, so its definitely a good idea to make this a strong password.

```bash
sudo nano /etc/ppp/chap-secrets
```

The username and password is put into the chap-secrets file in the format:

```text
username[TAB]*[TAB]password[TAB]*
```

So it looks like this (obviously with your username and password!):

```text
# Secrets for authentication using CHAP
# client        server  secret                  IP addresses
username  *       password        *
```

Restart PPTPD:

```bash
sudo service pptpd restart
```

**Configure Pi to forward traffic**
 In order to access network resources, other than the Pi itself, over the VPN, the Pi needed configuring the forward traffic, modify /etc/sysctl.conf and apply the change:

```bash
sudo nano /etc/sysctl.conf
```

Find the option "net.ipv4.ip_forward", which should be commented out and look like:

```text
#net.ipv4.ip_forward=1
```

Un-comment it and save the changes:

```text
net.ipv4.ip_forward=1
```

Apply the change:

```bash
sudo sysctl -p
```

**Configure router**
 In order to access the VPN from outside your network you need to configure your router to forward TCP port 1723 to the IP address of your Raspberry Pi, see [portforward.com](http://portforward.com/) for more information about port forwarding guides and info; you may find setting up port forwarding simpler if your raspberry Pi has a static IP address, see this [post](http://stuffaboutcode.blogspot.com/2012/05/raspberry-pi-setting-static-ip-address.html) on [how to set a static IP address](http://stuffaboutcode.blogspot.com/2012/05/raspberry-pi-setting-static-ip-address.html).

I had a problem with my router, in that i didn't support "GRE Protocol 47", which meant that when I tried to connect to the VPN from internet it would fail, router support for protocol 47 seems pretty random not necessarily related to a specific brand or price point. So if you have problems connecting to your VPN do a google search for our router and GRE.

**Connect to the VPN**
 Setting up the connection to the VPN will be different depending on the client (e.g. PC, iPad, Phone) but most setups are you are going to need this information:

- Host = this is your external internet address, you might find it useful to use a dynamic IP service such as no-ip so you can use a DNS (e.g. myhost.no-ip.com) see this [post](http://stuffaboutcode.blogspot.com/2012/06/raspberry-pi-access-from-internet-using.html) for more information about [no-ip and how to setup it up](http://stuffaboutcode.blogspot.com/2012/06/raspberry-pi-access-from-internet-using.html).
- Type of VPN = PPTP
- Domain = leave blank
- Username - the username you setup in the chap-secrets file
- Password - the password you setup in the chap-secrets file
