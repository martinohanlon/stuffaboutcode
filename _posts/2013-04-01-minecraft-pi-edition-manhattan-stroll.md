---
title: 'Minecraft: Pi Edition - Manhattan Island'
date: 2013-04-01 19:56:00 +01:00
tags: [games, minecraft, python]
redirect_from:
  - /2013/04/minecraft-pi-edition-manhattan-stroll.html
---

How about a stroll around Manhattan? Well a stroll around Manhattan in Minecraft, perhaps admire the Empire State Building or the pay $25 to take in the view from the "top of the rock"?

![](/assets/img/2013/04/empirestate.jpg)

*Empire State Building*

![](/assets/img/2013/04/topoftherock.jpg)

*View from "Top of the Rock"*

I decided to see how much I could push the program I wrote which uses the API in the Pi edition of Minecraft to [render 3d models in the Minecraft World](http://www.stuffaboutcode.com/2013/03/minecraft-pi-edition-create-massive-3d.html). It turns out I could push it a LOT, I fancied creating a city scene, and is any more dramatic than New York, Manhattan Island.

{% include youtube.html id="yZFKd5QkcPo" %}

I found a [Google sketchup model of Manhattan](http://sketchup.google.com/3dwarehouse/details?mid=26f13875a2461471eeddf776b5d39ee1) and using [OBJexporter](http://sketchucation.com/forums/viewtopic.php?p=294844#p294844), exported the model to an OBJ file.

![](/assets/img/2013/04/ny_lil.png)

*Sketchup 3d model of Manhattan*

To give a scale of how massive this model is, previously the most complicated model I had produced in Minecraft was of a girls head, that took about 3 minutes to render, this took 1 hour 25 minutes, and that was after I had already cleared a suitably large area! The Pi took it all in its stride though and while it took a long time, there were no errors or glitches.

The model is pre 9/11, so the iconic Twin Towers still dominate the skyline.

![](/assets/img/2013/04/twintowers.jpg)

*Iconic buildings*

**Download and run**
 I have updated my [program](http://www.stuffaboutcode.com/2013/03/minecraft-pi-edition-create-massive-3d.html)to include the new york model, which you can download direct from [git-hub](https://github.com/martinohanlon/minecraft-renderObj.git), so run minecraft, open/create a world and follow the instructions:

```bash
sudo apt-get install git-core
cd ~
git clone https://github.com/martinohanlon/minecraft-renderObj.git
cd minecraft-renderObj
python minecraft-renderObj.py
```

If you want to know more about how this works and have a go yourself, head to this post, [http://www.stuffaboutcode.com/2013/03/minecraft-pi-edition-create-massive-3d.html](http://www.stuffaboutcode.com/2013/03/minecraft-pi-edition-create-massive-3d.html).
