---
title: 'Raspberry Pi - Minecraft Piano'
date: 2013-06-16 09:09:00 +01:00
tags: [minecraft, python, raspberry-pi]
redirect_from:
  - /2013/06/raspberry-pi-minecraft-piano.html
---

Every wanted to learn the Piano? How about the Minecraft Piano?

{% include youtube.html id="J1IZIhGrfwE" %}

I had this idea of using events in Minecraft, so that every time you hit a block it made a noise, which led to me creating the Minecraft Piano. Its really simple when you hit a certain type of block it plays a different piano chord, in my program F to B through middle C.

![](/assets/img/2013/06/minecraft-piano-keys.jpg)

The notes are played by the program constantly checking if a block has been hit, if it has finding out what type of block it is and then playing a WAV file of that note. e.g. if a SAND block been hit play Middle C.

**Create notes**
 The most difficult bit of this project was to get wav files of piano chords, there are several sources online of real piano recordings but they are massive files sizes and totally over the top for what I needed.

I found a really nice python utility called [PySynth](http://home.arcor.de/mdoege/pysynth/) which is a virtual synthesiser and has a useful function to save a note to a wav file.

I wrote a really simple program which used PySynth to create wav files of notes I wanted for the Piano.

```python
import pysynth_b

#notes to create
notes = ('f3', 'g3', 'a3', 'b3', 'c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4')
#use pysynth to make notes
for note in notes:
    # play note and a very short rest
    synth = ((note, 3), ('r', 50))
    pysynth_b.make_wav(synth, fn='notes/' + note + '.wav')
```

My program then uses the mc.events.pollBlockHits() api function to find out what blocks have been hit, then it finds out the type of block and depending on what block it is, then uses pygame to play the wav file.

**Blocks to Notes**
 STONE - F, GRASS - G, WOOD - A, DIRT - B, SAND - C, GRAVEL - D, LEAVES - E, COBBLESTONE - F, BRICK_BLOCK - G, WOOD_PLANKS - A, WOOL - B

**Download and run**
 You can download the code direct from [github](https://github.com/martinohanlon/minecraft-cannon), [https://github.com/martinohanlon/minecraft-piano](https://github.com/martinohanlon/minecraft-piano), so run minecraft, open/create a world and follow the instructions:

```bash
sudo apt-get install git-core
cd ~
git clone https://github.com/martinohanlon/minecraft-piano.git
cd minecraft-piano
python minecraft-piano.py
```

All the piano note wav files and the code to create them is included in the github repository.

**Code**
 I've included the code for reference but if you want to have a go or modify it I would recommend you download the repository from github as you will need other files (e.g. wav's) to get it working.

```python
#www.stuffaboutcode.com
#Raspberry Pi, Minecraft Piano - Different blocks back different tones when hit!

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time
#import pygame to use the mixer to play wav file
import pygame

if __name__ == "__main__":

    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()

    #Initialise pygame and the mixer
    pygame.init()
    pygame.mixer.init()
    #load WAVS files
    noteF3= pygame.mixer.Sound("notes/f3.wav")
    noteG3= pygame.mixer.Sound("notes/g3.wav")
    noteA3= pygame.mixer.Sound("notes/a3.wav")
    noteB3= pygame.mixer.Sound("notes/b3.wav")
    noteC4= pygame.mixer.Sound("notes/c4.wav")
    noteD4= pygame.mixer.Sound("notes/d4.wav")
    noteE4= pygame.mixer.Sound("notes/e4.wav")
    noteF4= pygame.mixer.Sound("notes/f4.wav")
    noteG4= pygame.mixer.Sound("notes/g4.wav")
    noteA4= pygame.mixer.Sound("notes/a4.wav")
    noteB4= pygame.mixer.Sound("notes/b4.wav")

    #block type to sound obj
    blocksToWavs = {block.STONE.id: noteF3,
                    block.GRASS.id: noteG3,
                    block.WOOD.id: noteA3,
                    block.DIRT.id: noteB3,
                    block.SAND.id: noteC4,
                    block.GRAVEL.id: noteD4,
                    block.LEAVES.id: noteE4,
                    block.COBBLESTONE.id: noteF4,
                    block.BRICK_BLOCK.id: noteG4,
                    block.WOOD_PLANKS.id: noteA4,
                    block.WOOL.id: noteB4}

    #Post a message to the minecraft chat window
    mc.postToChat("Minecraft Piano, www.stuffaboutcode.com")

    #loop until Ctrl C
    try:
        while True:
            #Get the block hit events
            blockHits = mc.events.pollBlockHits()
            # if a block has been hit
            if blockHits:
                # for each block that has been hit
                for blockHit in blockHits:
                    #If the block hit type (DIRT, WOOD, etc) is in the
                    # blocksToWavc dictionary - play the WAV
                    blockType = mc.getBlock(blockHit.pos.x, blockHit.pos.y, blockHit.pos.z)
                    if (blockType in blocksToWavs.keys()):
                        noteToPlay = blocksToWavs[blockType]
                        noteToPlay.play()
            #sleep for a short time
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("stopped")
```
