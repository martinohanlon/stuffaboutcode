---
title: 'Raspberry Pi - Connect NAS / windows share automatically at start-up'
date: 2012-05-29 14:54:00 +01:00
tags: [raspberry-pi]
redirect_from:
  - /2012/05/raspberry-pi-connect-nas-windows-share.html
---

Anyway, as good (or quite frankly brilliant) as the Pi is, the capacity of an SD card isn't going to go far; so connecting to my trusty NAS drive (e.g. shared folder) was going to be a neccessity and as I was going to be using it a lot, automatically mounting it when the Pi started was also needed.

I was going to be need Samba to connect to my NAS, which can be installed using:

**Install/Update Samba**
**(using Debian Squeeze)**
 Smbfs is required and while smbclient is not, its a useful tool that I thought I might need in the future.

```bash
sudo apt-get install smbfs smbclient
```

**(using Raspian)**
 Samba is already installed and smbfs has been depreciated in wheezy.

**(using Raspbmc)**
 Samba is already installed but I needed to installed cifs-utils in order to mount my NAS drive.

```bash
sudo apt-get install cifs-utils
```

**Make a directory to mount your NAS too**
 I choose to put it in the pi user's home directory using the structure /home/pi/server/share:

```bash
cd /home/pi
mkdir myNAS
cd myNAS
mkdir myShare
```

**Edit fstab file**
 I needed to edit the fstab file to mount the NAS drive at startup:

```bash
sudo nano /etc/fstab
```

I added the following line to the bottom of the file:

```text
//myNAS/myShare /home/pi/myNAS/myShare cifs username=your_username,password=your_password,workgroup=your_workgroup,vers=1.0,users,auto,user_xattr 0 0
```

And saved the changes.

WARNING

- this will mean your username & password is stored in plain text viewable to all on the device, if this is going to be a problem you can use a credentials file, see [http://anothersysadmin.wordpress.com/2007/12/17/howto-mount-samba-shares-in-fstab-using-a-credential-file/](http://anothersysadmin.wordpress.com/2007/12/17/howto-mount-samba-shares-in-fstab-using-a-credential-file/)

**Test**
 I tested the change by mounting the NAS drive using the command:

```bash
sudo mount -a
```

I then navigated to the mount directory and successfully retreived a directory listing from my NAS:

```bash
cd /home/pi/MyNAS/MyShare
ls
```

Success!

**Reboot**
 To be double sure, reboot and make sure your NAS is connected:

```bash
sudo shutdown -r now
```
