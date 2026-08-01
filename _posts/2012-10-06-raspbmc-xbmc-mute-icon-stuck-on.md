---
title: 'Raspbmc / xbmc - mute icon stuck on'
date: 2012-10-06 07:58:00 +01:00
tags: [raspberry-pi, raspbmc-xbmc]
redirect_from:
  - /2012/10/raspbmc-xbmc-mute-icon-stuck-on.html
---

![](/assets/img/2012/10/2012-10-06-07.06.46-1.jpg)

Anyway, I use raspbmc and xbmc on my raspberry pi as a media server and every now and again the mute symbol gets stuck on even though the volume isn't muted and no matter what I do I can't turn mute off.

Some google searches suggest this is a bug in xbmc when xbmc get confused when using one of the remote apps to control it; other users suggest you can reset this by using the remote app, but I can never get this to work.

The only solution I have found is to modify xbmc guisettings.xml file:

So if you are using raspbmc you will find this in the /home/pi/.xbmc/userdata folder, but other implementations of xbmc will have a similar structure.

```bash
nano /home/pi/.xbmc/userdata/guisettings.xml
```

The file is an xml file and the /audio/mute element that needs to be changed is:

```xml
    <audio>
        <mute>true</mute>
        <fvolumelevel>0.622222</fvolumelevel>
    </audio>
```

Modify the setting to false:

```xml
    <audio>
        <mute>false</mute>
        <fvolumelevel>0.622222</fvolumelevel>
    </audio>
```

Save the file (CTRL X)

Reboot and hey pesto the poxy thing has gone!
