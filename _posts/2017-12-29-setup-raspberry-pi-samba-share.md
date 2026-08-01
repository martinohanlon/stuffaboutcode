---
title: 'Setup Raspberry Pi Samba share'
date: 2017-12-29 22:47:00 +00:00
tags: [raspberry-pi]
redirect_from:
  - /2017/12/setup-raspberry-pi-samba-share.html
---

I almost always setup a samba share on every Raspberry Pi I install, it allows me to easily share files and work on my projects - so I thought I had better write down how I do it.
 Install samba:

```bash
sudo apt-get install samba
```

Modify the Samba config file to add a share called pihome which points to the /home/pi directory:

```bash
sudo nano /etc/samba/smb.conf
```

Scroll to the bottom and add the following:

```text
protocol = SMB2

[pihome]
   comment= Pi Home
   path=/home/pi
   browseable=Yes
   writeable=Yes
   only guest=no
   create mask=0644
   directory mask=0755
   public=no
```

Setup a samba password for the Pi user:

```bash
sudo smbpasswd -a pi
```

Restart the samba service:

```bash
sudo service smbd restart
```

You should now be able to connect to your Pi using the address:

```text
//ip_address_of_pi/pihome
```
