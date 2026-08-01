---
title: 'XBMC / Raspbmc kept buffering'
date: 2012-08-07 14:31:00 +01:00
tags: [raspberry-pi, raspbmc-xbmc]
redirect_from:
  - /2012/08/xbmc-raspbmc-kept-buffering.html
---

Anyway, I kept having a problems streaming videos from my NAS drive with xbmc and raspbmc on my raspberry Pi with it constantly stopping and re buffering... Very annoying.

My usual suspect would have been the NAS drive or network not having the capacity but I already used Boxee (which is based on xbmc) on a pc connected to the same switch using the same NAS so I was pretty confident I should start looking at either the Pi or xbmc.

Some google searches led me to look at increasing the cache memory size xbmc uses when streaming over a network.

This value is stored in an xml element the ~/.xbmc/userdata/advancedsettings.xml file, which can be modified by using ssh to connect to the Pi while xbmc is running (go to System, Information to find out the IP address).

See if the file exists, some later releases of raspbmc dont have any advanced settings and therefore no advancedsettings.xml file:

```bash
cat ~/.xbmc/userdata/advancedsettings.xml
```

**If the file exists**, you should see an output similar to this.

```xml
<advancedsettings>
   <splash>false</splash>
   <network>
        <cachemembuffersize>5282880</cachemembuffersize>
   </network>
   <fanartheight>540</fanartheight>
   <thumbsize>256</thumbsize>
   <gui>
       <algorithmdirtyregions>3</algorithmdirtyregions>
       <nofliptimeout>0</nofliptimeout>
   </gui>
   <lookandfeel>
       <enablerssfeeds>false</enablerssfeeds>
        <webserver>true</webserver>
   </lookandfeel>
   <bginfoloadermaxthreads>2</bginfoloadermaxthreads>
</advancedsettings>
```

The value we are interested in is:

```xml
<cachemembuffersize>5282880</cachemembuffersize>
```

which is "the number of bytes used for buffering streams ahead in memory XBMC will not buffer ahead more than this. WARNING: for the bytes set here, XBMC will consume 3x the amount of RAM"

I'm not sure why the value of 5282880 has been picked, I can only assume whoever set it was trying to set the it to 5mb, being 5x1024x1024 = 52**4**2880 but got a digit wrong.

I went for double at 10mb or 10\*1024\*1024 = 10485760 which seemed to resolve my buffering issues, although different values may work better for others.

Edit or create a advancedsettings.xml file

```bash
nano ~/.xbmc/userdata/advancedsettings.xml
```

If the **file exists**change:

```xml
<cachemembuffersize>5282880</cachemembuffersize>
```

to:

```xml
<cachemembuffersize>10485760</cachemembuffersize>
```

If the **file doesn't exist**insert the following:

```xml
<advancedsettings>
   <network>
       <cachemembuffersize>10485760</cachemembuffersize>
   </network>
</advancedsettings>
```

Ctrl X to save and reboot

```bash
sudo shutdown -r now
```

I haven't noticed any adverse effects of giving XBMC a greater memory cache on the Raspberry Pi, but anyone knows issues of doing this, let me know.
