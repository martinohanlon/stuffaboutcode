---
title: 'Minecraft: Pi Edition - 3d Models - Version 2'
date: 2013-04-13 08:15:00 +01:00
tags: [games, minecraft, python]
redirect_from:
  - /2013/04/minecraft-pi-edition-3d-models-version-2.html
---

I created a program, which using the Minecraft: Pi Edition API, takes [3d models and creates them in Minecraft](http://www.stuffaboutcode.com/2013/03/minecraft-pi-edition-create-massive-3d.html), but version 1 only created the models as wire-frames and only in one block.

Version 2 is now out which uses the same concept of taking a 3d model as an [obj file](http://en.wikipedia.org/wiki/Wavefront_.obj_file) and using the api to render it in Minecraft but it now draw's complete polygons rather than wire-frames and gives the ability to specify a minecraft block for each material, allowing models to be created completely and in 'colour'.

The first model to try, well that of a Raspberry Pi of course! Thanks to mnt and his [Sketchup model of a Raspberry Pi](http://sketchup.google.com/3dwarehouse/details?mid=38a07906d6aebaa8a58e28eb06d46abc&prevstart=0) which I exported as an obj file and my program made in Minecraft.

| ![](/assets/img/2013/04/raspberrypi.png) | ![](/assets/img/2013/04/sam_0872.jpg) |
| --- | --- |

{% include youtube.html id="NIFRxcdN9nI" %}

[http://youtu.be/NIFRxcdN9nI](http://youtu.be/NIFRxcdN9nI)

Adding the use of materials to the program was relatively easy, the obj file specifies which material should be used for a face (or faces), my program just uses a python dictionary object to specify the mapping between material and block type/data in python e.g. MATERIALS= {"Material1": \[block.STONE, None\], "Material2": \[block.WOOL.id, 0\]}, using polygons rather wire-frames was much more difficult.

To support drawing polygons, which when put together would create [3d polyhedrons](http://en.wikipedia.org/wiki/Polyhedron) I wrote a MinecraftDrawing class to implement the following algorithm:

- Find all the points on all the edges of the polygon (red lines)
- Draw lines between the edges of the polygon

This was complicated due to the Minecraft 'screen' being 3d, not 2d and google totally failing me in finding some example code! So I had to write it myself, ridiculous!

I ended up creating several versions of this function, trying to create a more performant version, but as the faces became more complicated (i.e. bigger with more than 3 points) my performant versions ended up missing blocks, so I settled on a simple implementation that was slow but always filled the gap!

I'll get the code onto github shortly and update the post.

I then went on to re-draw the space shuttle and manhattan of previous posts.

![](/assets/img/2013/04/sam_0873.jpg)

*Space Shuttle*

![](/assets/img/2013/04/sam_0874.jpg)

*Manhattan*
