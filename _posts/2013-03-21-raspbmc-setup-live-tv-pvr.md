---
title: 'Raspbmc - Setup Live TV & PVR'
date: 2013-03-21 21:09:00 +00:00
tags: [raspbmc-xbmc]
redirect_from:
  - /2013/03/raspbmc-setup-live-tv-pvr.html
---

I recently updated my 'media player' Pi, which spends most of its time showing [peppa pig](http://www.peppapig.com/), to the latest version of Raspbmc; before this it was running a very old version with a cobbled together and home compiled version of tvheaded so I could also view Live TV.

I thought I would put some instructions together about how to setup Live TV on RaspBMC.

![](/assets/img/2013/03/20130623_220542.jpg)

Note - Until the[June 2013 release of Raspbmc](http://www.raspbmc.com/2013/06/raspbmcs-jam-packed-june-jollifications/), Live TV didn't work, although you could listen to live music, record live tv and radio and playback recordings, but if you tried to view Live TV you would just get a blank screen. So if your version of raspbmc is older than June 2013 your first job is to update!

![](/assets/img/2013/03/wintv-usb-stick.jpg)

*Hauppauge WinTV Nova-T USB*

I got a lot of this information from this [post](http://forum.stmlabs.com/showthread.php?tid=2648)by Quonith on the raspbmc forum, which describes in great detail how to setup Live TV on Raspbmc, its very out of date now as the majority of the components you need are already installed with Raspbmc.

**Setup your USB TV Tuner hardware**
 The first thing you need to do is setup your USB TV tuner, I found a [Hauppauge WinTV Nova-T USB Stick](http://www.linuxtv.org/wiki/index.php/Hauppauge_WinTV-NOVA-T-Stick) lying around, if your fortunate to have the same one, continue on, if not head over to [http://www.linuxtv.org/wiki/index.php/DVB-T_USB_Devices](http://www.linuxtv.org/wiki/index.php/DVB-T_USB_Devices) and see if you can find the firmware for your particular tuner.

***Download the firmware***
 You need to download the firmware to the /lib/firmware directory on your raspberry pi, if you have the same TV tuner as me, use these commands.

```bash
cd /lib/firmware

sudo wget http://linuxtv.org/downloads/firmware/dvb-usb-dib0700-1.20.fw
```

**Get a MPEG 2 License**
 In order to play / stream MPEG2 content you will need an MPEG2 license, you can get one of these from the raspberry pi foundation.

[http://www.raspberrypi.com/mpeg-2-license-key/](http://www.raspberrypi.com/mpeg-2-license-key/)

Once you receive your licence code, go to Programs, Raspbmc settings, scroll down to MPEG2 license key and put it in.

![](/assets/img/2013/03/sam_0842.jpg)

Don't bother trying to use mine, they are tied to a specific Pi and it will only work on my Pi.

Reboot!

**Enable TvHeadend**
 TvHeadend is already installed with Raspbmc, you just need to enable it, goto Programs, Raspbmc Setting, Scroll down to Enable TvHeadend and select it.

![](/assets/img/2013/03/sam_0843.jpg)

**Setup TvHeadend**

You need to open up a web browser and goto the ip address of you Pi using port 9981, this will open up the TvHeadend user interface.

```text
http://<ip of Pi>:9981
```

Goto Configuration, DVB Inputs, TV Adapters

If you setup your TV tuner correctly, you should be able to "Select TV adapter" from the drop down list. If the list is empty your TV adapter isn't configured properly.

Enable the adapter by ticking the "Enabled" box and clicking Save.

![](/assets/img/2013/03/tvheadendenableadapter.png)

You need to configure TvHeadend with the correct multiplexes for your TV transmitter, if your lucky you may be able to pick your transmitter from the list by using "Add DVB Network by Location", then waiting for "Muxes awaiting initial scan" to reach zero, if however after this the number of services you have got is 0, you are going to have to [setup the muxes manually](http://www.stuffaboutcode.com/2012/12/tvheadend-no-services-found-setting-up.html) see this [post](http://www.stuffaboutcode.com/2012/12/tvheadend-no-services-found-setting-up.html) for a how-to. This is because the config files distributed with TvHeadend are out of date.

Once you have a number of services found, click "Map DVB Services to Channels".

Then wait! It'll take a while to map the services, you can watch the progress by opening up the TvHeadend System Log by clicking the small double chevron up arrow in the bottom right hand corner.

**Setup Timeshift**
 In order to get LiveTV working on raspbmc you will need to enable timeshift, this gets round some long standing issues where LiveTV wouldn't play due to a problem somwhere in the raspbmc, xbmc, tvheadend, omxplayer stack, this [post](http://forum.stmlabs.com/showthread.php?tid=4478) on the [Raspbmc forum](http://forum.stmlabs.com/) for more info.

Configuration, Recording, Timeshift, Click Enabled and Save configuration.

![](/assets/img/2013/03/tvheadendtimeshift.png)

**Setup Live TV in Raspbmc**

Settings, Live TV, General - Enable Live TV

![](/assets/img/2013/03/sam_0845.jpg)

XBMC will prompt you to pick a live TV add-on, pick Tvheadend HTSP Client Add-on and enable it.

Be prepared to be patient, because the first time you run it, its going to be slow and sluggish while it setups all the channels, my advice, goto Live TV, All Channels and leave it for a while! Then leave it for a bit longer. During this time it will be downloading the EPG (electronic programme guide), setting up the channels in XBMC and a load of other config.

Then have a go!
