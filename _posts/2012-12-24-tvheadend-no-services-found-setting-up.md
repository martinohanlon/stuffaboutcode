---
title: 'Tvheadend - no services found, setting up muxes'
date: 2012-12-24 11:56:00 +00:00
tags: [raspbmc-xbmc]
redirect_from:
  - /2012/12/tvheadend-no-services-found-setting-up.html
---

Anyway, I found an old usb tv tuner and I decided to see if I could get my raspberry pi running [raspbmc](http://www.raspbmc.com/) to show live TV, it turned out that configuring Tvheadend was a lot more complicated than I expected. Follow this [tutorial](http://www.stuffaboutcode.com/2013/03/raspbmc-setup-live-tv-pvr.html) to setting up live tv on raspbmc.

Once the tv tuner is setup and appears in the devices list in TV adapters in the Configuration menu on tvheadend you should be able to use the "Add DVB services by location", but I found that when I picked my transmitter it would scan the muxes but would not find any services.

**"No services found"**

It turned out that the config files distributed with tvheadend install where out of date, this is very likely in the UK as transmitter setups have changed a great deal over the past few months and years, leaving me with to manually update add the muxes.

**Press the 'Add mux(es) manually' button on the Multiplexes tab**

![](/assets/img/2012/12/tvheadendscreen_addmuex.png)

This shows a dialogue which allows you configure the muxes which are specific to your transmitter, all these values are available on the internet, in the UK, you can use [http://www.ukfree.tv/txlist.php](http://www.ukfree.tv/txlist.php) to find your local transmitter.

When you find your local transmitter, see this [link](http://www.ukfree.tv/txdetail.php?a=SK113003) for an example, there will be a number of multiplexes or mux(s), displayed as:

![](/assets/img/2012/12/transmitterdetail.png)

Using the information on ukfree.tv add a mux on Tvheadend for each mux on your transmitter:

- Frequency - is displayed in MHz and tvheadend requires it in KHz, so times the value by 1000
- Bandwidth - in the UK use 8 MHz
- Constellation - is displayed at the top in the format 64QAM, Tvheadend expresses it the other way round QAM-64
- Transmission mode - is displayed next to the constellation - 8K
- Guard interval - in the UK use 1/32
- Hierarchy - in the UK use None
- FEC Hi - is displayed next to Transmission Mode - 2/3
- FEC Lo - in the UK use None

![](/assets/img/2012/12/addmuxdialogue_complete.png)

Click Add and repeat for all the mux(s) on your transmitter.

If all the values are right, Tvheadend should pick up a MuxID once it has scanned the mux.

Then wait for "

Muxes awaiting initial scan

" to become 0, if everything is setup ok you should also see the number of **"Services"** climbing, before clicking "

Map DVB Services to channels

" on the general tab.
