---
title: 'Minecraft Fractal Trees'
date: 2014-07-19 09:22:00 +01:00
tags: [games, minecraft, python, raspberry-pi]
redirect_from:
  - /2014/07/minecraft-fractal-trees.html
---

I have been experimenting with the [Minecraft Graphics Turtle](http://www.stuffaboutcode.com/2014/05/minecraft-graphics-turtle.html) I created, its a typical graphics turtle in that you issue it commands such as forward, backward, left, right but you can also tell it to go up and down and go 3d!

I wanted to create something that took advantage of the 3d world available in Minecraft and decided to see if I could make some 3d fractals. Fractals are repeating patterns which when observed at different scales appear the same - I know that sounds like rubbish, but that's what they are!

These are the 3d fractal tree's I created in Minecraft:

![](/assets/img/2014/07/2014-07-07_21.38.43.jpg)

![](/assets/img/2014/07/2014-07-07_22.12.56.jpg)

This is what a 2d fractal tree looks like:

[Fractal tree — Rosetta Code](https://rosettacode.org/wiki/Fractal_tree)

I found some python turtle code to create the 2d tree at [interactivepython.org/runestone/static/pythonds/Recursion/graphical.html](http://interactivepython.org/runestone/static/pythonds/Recursion/graphical.html):

```python
import turtle

def tree(branchLen,t):
    if branchLen > 5:
        t.forward(branchLen)
        t.right(20)
        tree(branchLen-15,t)
        t.left(40)
        tree(branchLen-15,t)
        t.right(20)
        t.backward(branchLen)

def main():
    t = turtle.Turtle()
    myWin = turtle.Screen()
    t.left(90)
    t.up()
    t.backward(100)
    t.down()
    t.color("green")
    tree(75,t)
    myWin.exitonclick()

main()
```

Its recursive, which means that a function calls itself, so in the example above the tree() function calls itself passing a smaller and smaller branch until the branch gets smaller than 5 and the function doesn't call itself any more and exits. Recursion is the basis of all fractals, its how you get the repeating patterns.

I modded this code to use my Minecraft Graphics Turtle and rather than create 2 branches each time the function is called it creates 4 branches - 2 facing north to south and 2 facing east to west.

```python
#Minecraft Turtle Example
import minecraftturtle
import minecraft
import block

def tree(branchLen,t):
    if branchLen > 6:
        if branchLen > 10:
            t.penblock(block.WOOD)
        else:
            t.penblock(block.LEAVES)

        #for performance
        x,y,z = t.position.x, t.position.y, t.position.z
        #draw branch
        t.forward(branchLen)

        t.up(20)
        tree(branchLen-2, t)

        t.right(90)
        tree(branchLen-2, t)

        t.left(180)
        tree(branchLen-2, t)

        t.down(40)
        t.right(90)
        tree(branchLen-2, t)

        t.up(20)

        #go back
        #t.backward(branchLen)
        #for performance - rather than going back over every line
        t.setposition(x, y, z)

#create connection to minecraft
mc = minecraft.Minecraft.create()

#get players position
pos = mc.player.getPos()

#create minecraft turtle
steve = minecraftturtle.MinecraftTurtle(mc, pos)

#point up
steve.setverticalheading(90)

#set speed
steve.speed(0)

#call the tree fractal
tree(20, steve)
```

The other change I made was to change the block type so that the shorter branches (the ones at the top) are made of leaves and the ones at the bottom are made of wood.

I created these on the full version of [Minecraft using Bukkit and Raspberry Juice](http://www.stuffaboutcode.com/2013/06/programming-minecraft-with-bukkit.html), so I could take hi-def pictures but the same code works on the raspberry pi.

If you want to have a go, download the minecraft turtle code from [github.com/martinohanlon/minecraft-turtle](https://github.com/martinohanlon/minecraft-turtle) and run the [example_3dfractaltree.py](https://github.com/martinohanlon/minecraft-turtle/blob/master/example_3dfractaltree.py) program:

```bash
sudo apt-get install git-core
cd ~
git clone https://github.com/martinohanlon/minecraft-turtle.git
cd ~/minecraft-turtle
python example_3dfractaltree.py
```

I also made a fractal tree made out of random colours, check out [example_3dfractaltree_colors.py](https://github.com/martinohanlon/minecraft-turtle/blob/master/example_3dfractaltree_colors.py).

![](/assets/img/2014/07/2014-07-07_22.20.43.jpg)
