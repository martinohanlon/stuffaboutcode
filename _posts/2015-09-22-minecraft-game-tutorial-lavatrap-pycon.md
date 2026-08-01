---
title: 'Minecraft Game Tutorial - LavaTrap - Pycon 2015'
date: 2015-09-22 20:22:00 +01:00
tags: [games, minecraft, python]
redirect_from:
  - /2015/09/minecraft-game-tutorial-lavatrap-pycon.html
---

At Pycon UK 2015, I did a couple of workshop at its Education Track Kids day.

It was great fun and to make sure there was something fresh for the children to get their teeth into I came up with a new exercise called "LavaTrap" so I thought I would share it!

You can [download the worksheet](https://drive.google.com/open?id=19YVesJJFS6cg4Ndep7F-TS02CpS0qpN1hlSlv6mgISQ) which is great printed as an A5 booklet on a single piece of A4 or you can follow the exercise below.

## The Lava Trap

Using Python and Minecraft: Pi edition we can change the game to do amazing things.

You are going to create mini game - a Lava Pit will instantly appear and Steve will be put at the centre of it, soon through the block he is standing on will disappear so he will have to move, but hang on all the blocks keep disappearing!

![2015-09-13_22.22.00.png](/assets/img/2015/09/p3h-mgzopc2i8nq5lqetbdrehobckykyhznaz9iwswxhs3tyeohz7cdrpkbp6czaapwootsg3m7mwqkqvnpehu9g0yzby5klfyzwodbpstfgtlmrl5kc3vqmhdplpxybrjzh261q.jpg)

## Welcome

The first task is to start your program and get “Welcome to the Lava Trap” to appear on the screen:

1. Press ESC to go back to the Minecraft menu but leave the game playing.
2. Open Python IDLE by clicking Menu > Programming > Python 3.
3. Use File > New Window to create a new program and save it as ‘myprogram.py’.
4. Type the following code into the program to import the modules you will need.

```python
from mcpi.minecraft import Minecraft
from mcpi import block
```

#### `from time import sleep`

1. Create a connection to Minecraft using the code.

#### `mc = Minecraft.create()`

1. Post a message to the chat window.

#### `mc.postToChat("Welcome to the Lava Trap")`

1. Run your program by clicking Run > Run Module.

You should see your message appear in the Minecraft chat window.

### Tips

| An errors will be displayed in the Python Shell in red.   If you get an error check your code carefully.   Capital letters are important `Minecraft` is different to `minecraft`. |
| --- |

## Lava

Next you will use the api to create the pit where the game will be played - when your program runs it will instantly appear under Steve before the game starts.

First update your program so it creates a single block of lava under Steve, by adding the following code:

1. Put a 3 second delay into your program so that you can see what going on.

#### `sleep(3)`

1. Find out where Steve is in the world.

#### `pos = mc.player.getTilePos()`

1. Create a block of lava under Steve.

#### `mc.setBlock(pos.x, pos.y - 1, pos.z, block.LAVA.id)`

1. Run your program by clicking Run > Run Module or by pressing F5.

Your program will wait 3 seconds and then a block of Lava will appear under Steve - he’s going fall in and burn!

### Tips

| Walk somewhere different and run the program again - another Lava block will appear.    Try changing the code to use DIAMOND_BLOCK rather than LAVA and see what happens. |
| --- |

You need to create a lot more lava in order for the game to be a lot more fun - next you will program a large slab of STONE with LAVA on the top:

1. Use setBlocks() to create an area of STONE 2 blocks below Steve for the LAVA to sit on.

#### `mc.setBlocks(pos.x - 5, pos.y - 2, pos.z - 5,`

#### `pos.x + 5, pos.y - 2, pos.z + 5,`

#### `block.STONE.id)`

1. Then create the LAVA under Steve.

#### `mc.setBlocks(pos.x - 5, pos.y - 1, pos.z - 5,`

#### `pos.x + 5, pos.y - 1, pos.z + 5,`

#### `block.LAVA.id)`

1. Run your program to see the Lava ‘pit’.

Make a DIAMOND_BLOCK platform in the middle for Steve to stand on:

1. Create the diamond block.

#### `mc.setBlock(pos.x, pos.y - 1, pos.z, block.DIAMOND_BLOCK.id)`

1. Run your program Steve will be stuck in the middle of the Lava pit.

## Challenge 1 - Can you code yourself out of the Lava Pit?

At the moment unless Steve flies or lays blocks down he can’t get out without getting burned - update your program so he can get out.

### Tips

| Use more setBlocks() commands to make a bridge out of the Lava pit.   You can change Steve’s x,y,z position using mc.player.setTilePos(x, y, z).   If it’s too easy, make the Lava Pit really big - is it still easy? |
| --- |

## Make a game

Update your program to make blocks under Steve disappear:

1. Post messages to the chat screen to warn the player the game is about to start.

#### `mc.postToChat("Get Ready")`

#### `mc.postToChat("Blocks under you will keep disappearing")`

#### `sleep(3)`

#### `mc.postToChat("Go")`

1. Create a variable called gameover and set it to False - it will be set to True at the end of the game.

#### `gameover = False`

1. Create a loop which will continue until the game is over.

#### `while gameover == False:`

1. Get Steve’s position.

#### `playpos = mc.player.getTilePos()`

1. Turn the block under Steve to OBSIDIAN as a warning and wait for 2 seconds.

#### `mc.setBlock(playpos.x, playpos.y - 1, playpos.z,block.OBSIDIAN.id)`

#### `sleep(2)`

1. After the warning turn the block to AIR, if Steve is standing on it, he’s going to be in the Lava pit.

#### `mc.setBlock(playpos.x, playpos.y - 1, playpos.z, block.AIR.id)`

#### `sleep(0.5)`

1. Run the program, the game will start and you will have to put blocks down in the Lava pit to escape because otherwise they are going to disappear and Steve will fall in.

## Game over

The game is over if Steve falls into the Lava, you need to modify your program to check if he has fallen into the Lava and put a message on the screen:

1. Use an if statement to see if Steve’s height (y) is not equal to where he started, if it is set the gameover variable to True.

#### `if playpos.y != pos.y:`

#### `gameover = True`

1. Put a message on the screen to let the player know they have been caught in the lava trap.

#### `mc.postToChat("Game over.")`

1. Run your program and see how long you can stay out of the lava.

## Challenge 2 - Make the game your own.

This game is just the start, can you finish it? Here are some challenges:

1. Make the game harder?
2. Make a better game arena, perhaps build a stadium or walls around it so Steve can get out.
3. Add points to the game, each time Steve doesn’t fall in he gets a point.
4. Change the game so it starts easy but gets harder the longer you play.
5. Add a 2 player (or even multiplayer!) option.

### Tips

| If you make the sleeps shorter it’ll make the game quicker and harder.   Create a variable called points at the start of the game and add 1 to it each time your program goes around the loop.   There are lots of experienced Python developers all around you - perhaps you can teach them! |
| --- |

## Find out more

If you have enjoyed this check out “Adventures in Minecraft” and learn how to program Minecraft using Python on your Raspberry Pi, Windows PC or Apple Mac and the Minecraft resources on the Raspberry Pi website

[www.raspberrypi.org/resources](http://www.raspberrypi.org/resources)

.
