---
title: 'Minecraft: Pi Edition - 2 Games by Nicholas Harris'
date: 2013-05-21 21:52:00 +01:00
tags: [minecraft, python, raspberry-pi]
redirect_from:
  - /2013/05/minecraft-pi-edition-2-games-by.html
---

[Nicholas Harris](https://plus.google.com/109549225711376378768/posts) is a regular commenter and reader of the minecraft posts on [\<Stuff about="code" />](/) and he let me know that he was working on a program for minecraft, he also agreed to let me include a post about what he has done. Check out the [Minecraft - API Basics](/posts/raspberry-pi-minecraft-api-basics/) comments section for a description of Nicholas's development.

![](/assets/img/2013/05/sam_0901.jpg)

Nicholas has pulled together one mother of a minecraft program which encompasses a load of different games, utilities and building tools. Including a script to create a horse, characters from the alphabet, a crazy utility which makes you fall through the earth and die, but perhaps most impressively 2 games of his own invention:

- Arena's starts with you stood in an empty room and the objective is to not fall to your death while the floor beneath you gradually disappears
- Dodge puts you at one end of a line of furnaces which spew there contents towards you and you have to stay out of the way.

They both show a great deal of originality and thought, not to mention coding skill.

{% include youtube.html id="n4mnJZ9xWPA" %}

If you fancy trying out Nicholas's program, follow the instructions below to download, setup and run.

**Create a directory for the program**

```bash
mkdir ~/minecraft-nicholas
cd ~/minecraft-nicholas
```

**Download Nicholas's program**

```bash
wget http://scarabcoder.pancakeapps.com/api.py
```

**Copy the minecraft api python library**

```bash
cp -r ~/mcpi/api/python/mcpi ~/minecraft-nicholas/minecraft
```

**Start up Minecraft and run Nicholas's program**

```bash
python ~/minecraft-nicholas/api.py
```

**Commands**

The program uses a command line interface to start up the games and utilities, so use:

- `/help` to give you a list of the commands
- `/arena` to start the arena game
- `/dodgegame` to start the dodge game.

I think its great when people take the initiative and create something cool off their own back and I couldn't be happier that the drivel I write is actually useful to someone!
