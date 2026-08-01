---
title: 'GPIO Xmas Tree Reaction Game'
date: 2014-12-18 12:05:00 +00:00
tags: [games, raspberry-pi]
redirect_from:
  - /2014/12/gpio-xmas-tree-reaction-game.html
---

In order to bring a bit of Christmas based fun to the office (I am normally a bit of a '[bah humbug](http://en.wikipedia.org/wiki/Humbug)') I have created a reaction game using a [Raspberry Pi](http://www.raspberrypi.org/) and a [GPIO Xmas Tree](http://www.pocketmoneytronics.co.uk/?page_id=239) from [pocketmoneytronics](http://www.pocketmoneytronics.co.uk/).

![](/assets/img/2014/12/20141218_103130.jpg)

The game is pretty simple, random leds are lit up on the xmas tree, the player has to press the button when the green led on the top of the tree is lit up. The quicker you are, the higher you score.

A random animation is played when the tree is waiting for the next player, you press the button to start, all the leds are lit up and then its time to play. At the end the players position is displayed on the tree, with 1st place lighting up the top of the tree.

**Have a go**
 You will need a Raspberry Pi, a GPIO Xmas Tree and a button:

1. Plug the GPIO Xmas tree into the far left set of pins on the GPIO header
2. Connect the button up between 3.3V and GPIO 4.

![](/assets/img/2014/12/20141218_110520.jpg)

**Update - 23/12/2014 - 2 player**
 The GPIO Xmas Tree Reaction game has gone 2 player... You go head to head versus a friend, the quickest to the green led wins and an led on either the left or right of the tree is lit up to show you who won.

![](/assets/img/2014/12/20141223_195203.jpg)

If you want to play head to head:

1. Connect the button up between 3.3V and GPIO22
2. Press the 2nd button to start the 2 player game, pressing the 1st button, still starts the 1 player game

**Get the code**

Download the code from [github.com/martinohanlon/GPIOXmasTreeGame](https://github.com/martinohanlon/GPIOXmasTreeGame) and run the game - open a terminal and run:

```bash
git clone https://github.com/martinohanlon/GPIOXmasTreeGame
cd GPIOXmasTreeGame/xmastreegame
python xmastreegame.py
```

**How does it work**
 There was only 1 particular challenge to creating the game (other than my dodgy soldering which meant I ruined the first tree I brought) - doing more than one thing at a time!

The libraries supplied by pocketmoneytronics are really good and there are some great examples, the problem I had is that when you tell the tree to "light up leds 1 & 4", that is all your program can do, it blocks because the tree uses [Charlieplexing](http://www.pocketmoneytronics.co.uk/?page_id=251) and the libraries don't support threading.

Charliewhat? In summary, each gpio pin is actually controlling 2 leds and when you light up 2 leds on the tree the program is actually turning the leds on and off independently really quickly, so quickly that its tricking your eyes into thinking that both leds are actually turned on.

This is why you cant just "turn on led 1 and led 4", the tree doesn't work that way.

To get around this, I made a threaded version of the pocketmoneytronics tree.py module.

Using the original libraries, you would have used the following code to light up all the leds for 1 second:

```text
tree.setup()
#turn all the leds on for 1 second
#the program stops here and nothing can happen until the leds turns off
tree.leds_on_and_wait(ALL, 1)
tree.cleanup()
```

Using my threaded class you would use:

```text
#create the XmasTree object
tree = XmasTree()
#start the tree object
tree.start()
#turn all leds on
tree.leds_on(ALL)
#the program can now do what it wants and the leds will stay on
sleep(1)
tree.stop()
```

The rest of the program was pretty easy to create, wait for a button to be pressed, light up led's randomly with a random delay in between, get the difference in time between turning on the yellow led and the button being pressed and hey presto, a Christmas themed game.

**The code**
 All the code is here [github.com/martinohanlon/GPIOXmasTreeGame](https://github.com/martinohanlon/GPIOXmasTreeGame).

```python
import threading
import RPi.GPIO as GPIO
from time import sleep, time
from ThreadedTree import XmasTree
from random import getrandbits, randint
from os.path import isfile

#CONSTANTS
#leds
L0 = 1
L1 = 2
L2 = 4
L3 = 8
L4 = 16
L5 = 32
L6 = 64
ALL = 1+2+4+8+16+32+64
#leds as a list
LEDS = [L0,L1,L2,L3,L4,L5,L6]
#leds as a list descending down the tree
LEDSDESC = [L0,L6,L5,L4,L2,L1,L3]
#gpio pin the game button is connected too
NEWGAMEBUTTONPIN = 4
#gpio pin which will cause the game to stop if trigger
STOPGAMEBUTTONPIN = 17

class TreeRandom(threading.Thread):
    def __init__(self, xmasTree):
        #setup threading
        threading.Thread.__init__(self)
        #setup properties
        self.stopped = False
        self.running = False
        self.xmasTree = xmasTree

    def run(self):
        self.running = True
        while not self.stopped:
            ledsToLight = 0
            #loop through all the lights, randomly pick which ones to light
            for led in LEDS:
                if getrandbits(1) == 1:
                    ledsToLight = ledsToLight + led
            #turn the leds on
            self.xmasTree.leds_on(ledsToLight)
            #delay
            sleep(1)
        #when its stopped turn the leds off
        self.xmasTree.leds_on(0)
        self.running = False

    def stop(self):
        #stop the animation
        self.stopped = True
        #wait for it to stop running
        while self.running:
            sleep(0.01)

class TreeGame():
    def __init__(self, xmasTree, scoresFile):
        self.scoresFile = scoresFile
        self.scores = self._loadScores()
    #print self.scores

    def play(self):
        #turn on all leds
        xmasTree.leds_on(ALL)
        #wait a bit
        sleep(2)
        #get a random number, which will be how many leds will be lit before the green one
        steps = randint(7,14)
        for step in range(0,steps):
            #light a random red led
            ledToLight = LEDS[randint(1,6)]
            xmasTree.leds_on(ledToLight)
            #wait for a random time between 0.5 and 1 second
            timeToSleep = randint(5,10) / 10.0
            sleep(timeToSleep)
        #light the green led
        xmasTree.leds_on(L0)
        #get the time
        startTime = time()
        #wait for button to be released (if its pressed)
        while(GPIO.input(NEWGAMEBUTTONPIN) == 1):
            sleep(0.001)
        #wait for the button to be pressed
        while(GPIO.input(NEWGAMEBUTTONPIN) == 0):
            sleep(0.001)
        #get the time
        endTime = time()
        timeDiff = endTime - startTime
        #put the score in the score list and find the position
        # loop through all the scores
        for score in range(0,len(self.scores)):
            # is this time less than the current score?
            if timeDiff < self.scores[score]:
                #record the players position
                position = score
                self.scores.insert(score,timeDiff)
                break
        #save to the score file
        self._saveScores()
        #flash the position
        self._displayPosition(position)

    def _displayPosition(self,position):
        #if there position was less than 6, flash it on the tree
        # else flash all the lights
        if position <= 6:
            ledToLight = LEDSDESC[position]
        else:
            ledToLight = ALL
        #flash the position
        for count in range(15):
            xmasTree.leds_on(ledToLight)
            sleep(0.2)
            xmasTree.leds_on(0)
            sleep(0.2)

    # load the scores files
    def _loadScores(self):
        scores = []
        #does the file exist?  If so open it
        if isfile(self.scoresFile):
            with open(self.scoresFile, "r") as file:
                for score in file:
                    scores.append(float(score))
        else:
            #no file so put an initial score which is massive
            scores.append(999)

        return scores

    # save the scores file
    def _saveScores(self):
        with open(self.scoresFile, "w") as file:
            for score in self.scores:
                file.write(str(score)+"\n")

#main program
if __name__ == "__main__":

    #setup GPIO
    GPIO.setmode(GPIO.BCM)

    #setup the new game button
    GPIO.setup(NEWGAMEBUTTONPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #setup the stop game button
    GPIO.setup(STOPGAMEBUTTONPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    #create threaded tree object
    xmasTree = XmasTree()
    #start the xmas tree
    xmasTree.start()
    #create tree game oject
    treeGame = TreeGame(xmasTree, "scores.txt")

    try:
        stopGame = False
        #loop until the stop game pin is set
        while(not stopGame):
            #run the xmas tree random animation
            treeRandom = TreeRandom(xmasTree)
            treeRandom.start()

            #wait until a button is pressed to either start a new game or stop the game
            while(GPIO.input(NEWGAMEBUTTONPIN) == 0 and GPIO.input(STOPGAMEBUTTONPIN) == 0):
                sleep(0.01)

            #new game
            if GPIO.input(NEWGAMEBUTTONPIN) == 1:
                #stop the animation
                treeRandom.stop()
                #run the game
                treeGame.play()
                #game over, start the animation again
                sleep(1)

            #stop game
            elif GPIO.input(STOPGAMEBUTTONPIN) == 1:
                stopGame = True

    finally:
        #stop tree random animation
        treeRandom.stop()
        #stop xmas tree
        xmasTree.stop()
        #cleanup gpio
        GPIO.cleanup()
```
