---
title: 'Minecraft Sat Nav'
date: 2014-11-24 21:54:00 +00:00
tags: [adventures-in-minecraft, gps, minecraft, python]
redirect_from:
  - /2014/11/minecraft-sat-nav.html
---

![](/assets/img/2014/11/2014-11-24_21.14.04.jpg)A couple of months back the ordnance survey created version 2 of their [Minecraft map of Great Britain](http://www.ordnancesurvey.co.uk/innovate/developers/minecraft-map-britain.html), its got loads more detail than the original, and is even more brilliant than there first one.

It is however a pain to get around... Welcome "Minecraft Sat Nav", utterly ridiculous, totally pointless but at the same time brilliant.

Imagine you are exploring Minecraft Great Britain and you suddenly realise you need to get to [Macclesfield](http://en.wikipedia.org/wiki/Macclesfield) but dont know the way, simple fire up Minecraft Sat Nav (patent pending!) and type

```text
navigate Macclesfield
```

and it will give you a street by street navigation between your location and a town which was previously one of the world's biggest producers of silk!

{% include youtube.html id="XPZBeaVDn8A" %}

**How does it work? Here are some facts:**

1. Its a python program
2. It uses a [Canarymod](http://canarymod.net/) minecraft server to host the map
3. The [RaspberryJuice plugin](https://github.com/martinohanlon/canaryraspberryjuice) is used to talk to Minecraft
4. It uses the [MapQuest open API's](http://developer.mapquest.com/en_GB/web/products/open) to get the locations and directions
5. I reverse engineered Ordance Survey's '[conversion tool](http://oslabs.s3.amazonaws.com/convert.html)' to work out how to turn eastings and northings into Minecraft co-ordinates
6. I used [Hannah Fry's](http://hannahfry.co.uk/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii/) awesome python code to turn latitude and longitude into eastings and northings
7. Its got a low tech 'retro styled' command line interface

**You want to have a go yourself? Here's a guide:**

1. Buy yourself a copy of [Adventures in Minecraft](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-111894691X.html) ;) - honestly you really cant go wrong and it'll teach you what you need to know to make your own Minecraft Sat Nav!
2. Setup a [Canarymod server with RaspberryJuice](http://www.stuffaboutcode.com/2014/10/minecraft-raspberryjuice-and-canarymod.html)
3. Download the [Ordnance Survey Minecraft GB map](http://www.ordnancesurvey.co.uk/innovate/developers/minecraft-map-britain.html)
4. Replace the default world in canarymod with the Minecraft GB map
5. Download the[Minecraft Sat Nav](https://github.com/martinohanlon/minecraft-osmapnav) program
6. Run the MinecraftSatNav.py python program

**The commands are really simple:**

- `teleport <location>` e.g. `teleport london`
- `navigate <destination>` e.g. `navigate fort william`
- `navigateFrom <start>,<dest>` e.g. `navigate sheffield, grindleford`
- `exit`

Enuf said..
