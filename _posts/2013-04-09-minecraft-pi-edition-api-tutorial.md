---
title: 'Minecraft: Pi Edition - API Tutorial'
date: 2013-04-09 20:35:00 +01:00
tags: [minecraft, python, raspberry-pi]
redirect_from:
  - /2013/04/minecraft-pi-edition-api-tutorial.html
---

This tutorial started off as an article I wrote on Minecraft: Pi Edition for the [Issue 11 of The Mag Pi](http://www.themagpi.com/en/issue/11), a magazine written by Raspberry Pi enthusiasts, and builds on my first post [Raspberry Pi - Minecraft - API Basics](/posts/raspberry-pi-minecraft-api-basics/), which describes the basics of how to use the API. I highly recommend you give [The Mag Pi](http://www.themagpi.com/) a go, its always full of interesting and relevant articles.

![](/assets/img/2013/04/minecraft-2.jpg)

**Install Minecraft**
 If Minecraft: Pi edition isn't already installed on your Pi, head over to [www.raspberrypi.org/documentation/usage/minecraft](http://www.raspberrypi.org/documentation/usage/minecraft/) and follow the instructions.

**The API**
 The API allows you to write programs which control, alter and interact with the minecraft world, unlocking a whole load of minecraft hacking. How about [creating massive structures at the click of a button](/posts/minecraft-pi-edition-3d-models-version-2/) or a [bridge which automatically appears under your feet](/posts/raspberry-pi-minecraft-auto-bridge/) allowing you to walk across massive chasms or a game of minesweeper, a [huge real time clock](/posts/raspberry-pi-minecraft-analogue-clock/), a [programmable directional cannon](/posts/raspberry-pi-minecraft-cannon/), [turn blocks into bombs](/posts/raspberry-pi-minecraft-block-events/) or the game [snake](/posts/raspberry-pi-minecraft-snake/)?

![](/assets/img/2013/04/minecraft-clock.jpg)

[Massive Analogue Clock](/posts/raspberry-pi-minecraft-analogue-clock/)

![](/assets/img/2013/04/minecraftcannon.jpg)

[Directional Cannon](/posts/raspberry-pi-minecraft-cannon/)

![](/assets/img/2013/04/minecraft-snake.jpg)

[Snake](/posts/raspberry-pi-minecraft-snake/)

Minecraft is a world of cubes or blocks, all with a relative size of 1m x 1m x 1m, and every block has a position in the world of x, y, z; x and z being the horizontal positions and y being the vertical.

![](/assets/img/2013/04/minecraft---xyz.png)

The API works by changing the ‘server’, which runs underneath the game, allowing you to interact with these blocks and the player, such as:

- Get the player’s position
- Change (or set) the player’s position
- Get the type of block
- Change a block
- Change the camera angle
- Post messages to the player

**Libraries**

You can interact with the server directly by sending a message to it, but the nice people at Mojang also provide libraries for python and java which simplify and standardise using the API.

The libraries are installed along with the game in the /opt/minecraft-pi/api/java and api/python directories.

The following example is written in Python and uses Mojang’s python api library.

**API Example**

***Create Directory***

We need to create a directory to put our program into.

```bash
mkdir ~/minecraft-magpi
```

***Create program***

Open the Python 2 editor Idle (or your favourite editor) and create a program file called minecraft-magpi.py in the ~/minecraft-magpi directory

We are going to need 3 modules, the minecraft.py and block.py modules from the minecraft directory containing the library we just copied and the standard time module so we can introduce delays into our program.

```python
import mcpi.minecraft as minecraft
import mcpi.block as block
import time
```

Next, we need to use the Minecraft class in the python library to create a connection to the game’s server, this object will also be how we interact with the game and will provide access to all the functions. When your program runs this statement, Minecraft will have to be running and you will need to be in a game, otherwise you will get errors.

```python
mc = minecraft.Minecraft.create()
```

Using our minecraft object, mc, we can then interact with the game and send the player a message. We will also put a delay in using the time.sleep() function otherwise the whole program will run too fast for us to see what’s going on.

```python
mc.postToChat("Hello Minecraft World")
time.sleep(5)
```

Using the program built so far, you can test to make sure everything is working. Load up minecraft and create a (or enter an existing) world then if you’re using Idle pick 'Run, Run Module' from the menu. If all has been setup correctly you will see the “Hello Minecraft World” message in the game.

![](/assets/img/2013/04/minecraft-helloworld.jpg)

Interacting with the player is done through the player class of the mc object allowing us to find the position and change the position of the player. The next block of code finds the players position using the getPos() command, which returns an object of x,y and z coordinates, the setPos() command is then used to move the player 50 blocks up, by adding 50 to the player’s y coordinate. We then add a delay, so there is enough time for your player to fall down to the ground!

```python
playerPos = mc.player.getPos()
mc.player.setPos(playerPos.x, playerPos.y + 50, playerPos.z)
mc.postToChat("Dont look down")
time.sleep(5)
```

You can use the position of the player as a starting point for interacting blocks, this way you can find out what block the player is standing on or place blocks around the player, there is however a challenge, the x, y and z coordinates returned by the getPos() function are decimals (aka floats), as your player can be in the middle of a block, but to interact with blocks we need to use whole numbers (aka integers), so we need to use the function getTilePos(), which returns the block (or tile) he’s standing on.

The code below gets the players tile position, it then calls the minecraft API’s getBlock() function to find out the type of block the player is standing on (by minusing 1 from the y co-ordinate) before using setBlock() to create blocks of the same type the player is standing on around him. So if your player is standing on DIRT, he will end up with DIRT surrounding him, however if he is standing on STONE, STONE will appear.

```python
playerTilePos = mc.player.getTilePos()
blockBelowPlayerType = mc.getBlock(playerTilePos.x, playerTilePos.y - 1, playerTilePos.z)
mc.setBlock(playerTilePos.x + 1, playerTilePos.y + 1, playerTilePos.z, blockBelowPlayerType)
mc.setBlock(playerTilePos.x, playerTilePos.y + 1, playerTilePos.z + 1, blockBelowPlayerType)
mc.setBlock(playerTilePos.x - 1, playerTilePos.y + 1, playerTilePos.z, blockBelowPlayerType)
mc.setBlock(playerTilePos.x, playerTilePos.y + 1, playerTilePos.z - 1, blockBelowPlayerType)
mc.postToChat("Trapped you")
time.sleep(5)
```

![](/assets/img/2013/04/minecraft-trapped.jpg)

We have now trapped our player within 4 blocks (providing he doesn’t break out!), in order to set him free we need to remove a block. Removing blocks is done using setBlock(), but rather than making the block solid like WOOD or STONE we set it to AIR.

```python
mc.setBlock(playerTilePos.x + 1, playerTilePos.y + 1, playerTilePos.z, block.AIR)
mc.postToChat("Be free")
time.sleep(5)
```

A full list of all the available blocks can be found in either the minecraft api specification or in the block.py module in the python api library ~/mcpi/api/python/mcpi/block.py.

The API also allows you to set many blocks at a time, allowing you to create cuboids very quickly using the setBlocks() command. It works by specifying 2 sets of x,y,z coordinates which it then fills the gap between the 2 coordinates with a certain block you pass as the final parameter. The code below will create a diamond floor underneath our player 50 blocks (across) x 1 block (up) x 50 blocks (along), with our player in the middle (i.e. 25 behind and to the left, 25 in front and to the right).

```python
mc.setBlocks(playerTilePos.x - 25, playerTilePos.y - 1, playerTilePos.z - 25, playerTilePos.x + 25, playerTilePos.y -1, playerTilePos.z + 25, block.DIAMOND_BLOCK)
mc.postToChat("Now thats a big diamond floor!")
```

![](/assets/img/2013/04/minecraft-diamondfloor.jpg)

To recap on the functions covered in this article:

- postToChat(message) - communicate with the player(s) in the game
- getBlock(x, y, z) - get a block type for a specific position
- setBlock(x, y, z, blockType, blockData) - set (change) a block to a specific blockType
- setBlocks(x1, y1, z1, x2, y2, z2, blockType, blockData) - set lots of blocks all at the same time by providing 2 sets of co-ordinates (x, y, z) and fill the gap between with a blockType
- player.getPos() - get the precise position of a player
- player.setPos(x, y, z) - set (change) the players position
- player.getTilePos() - get the position of the block where the player current is

There are a few other functions available in the api which should be explored but using only the small number discussed in this article, its possible, with some imagination and a small amount of programming knowledge to create some quite fantastic constructions, tools and utilities.

I love minecraft, its a tremendously creative game and with the Pi edition’s API it opens up new level of creativity and will hopefully encourage more people to try their hand at programming.

If you want to see more examples of what I have done with Minecraft: Pi edition (e.g. a [massive analogue clock](/posts/raspberry-pi-minecraft-analogue-clock/), the [game of snake](/posts/raspberry-pi-minecraft-snake/), an [auto bridge](/posts/raspberry-pi-minecraft-auto-bridge/) which appears under your feet or the whole of [Manhattan](/posts/minecraft-pi-edition-manhattan-stroll/)) head over to my [Minecraft page](/minecraft/).
