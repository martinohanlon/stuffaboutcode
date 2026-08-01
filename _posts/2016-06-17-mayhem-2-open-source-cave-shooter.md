---
title: 'Mayhem 2 - an open source cave shooter'
date: 2016-06-17 20:00:00 +01:00
tags: [games]
redirect_from:
  - /2016/06/mayhem-2-open-source-cave-shooter.html
---

I recently [ported an abandoned version the classic amiga game, Mayhem, to the Raspberry Pi](http://www.stuffaboutcode.com/2016/04/mayhem-classic-amiga-game-ported-to.html) - I did this exclusively so I could play the game with my friend, Lee, using [RetroPie](http://retropie.org/).

Since then myself and Lee, an artist for sumo digital, have been modding the game, adding new levels, features and controls - it now really is Mayhem **2**.

![](/assets/img/2016/06/mayhem2pg.jpg)

Mayhem 2 is available for [Windows](https://github.com/martinohanlon/mayhem) and [Raspberry Pi](https://github.com/martinohanlon/mayhem-pi).

I'm hoping there will be lots more features and changes to the game over the coming months, if anyone has any idea's or would like to contribute it would be great to hear from you.

**Gameplay**

Mayhem 2 is a multiplayer (2 - 4) flight shooter with a really simple objective - destroy your opponents before they destroy you.

Your ship has limited fuel which will run down when you boost, if you run out you will be unable to control your ship, to refuel, land on any flat surface.

You can protect yourself from attack using your shields which will stop all bullets, be careful though your shields run down quickly and you wont be able to boost while your shields are on.

Power -ups are dropped (sometimes) when a player is destroyed (by either crashing or being shot) and when collected will give you a temporary boost such as a triple-shot weapon, better shields or more thrust.

{% include youtube.html id="oxAzUuwuleM" %}

New levels have been added including new ones with no edges, where you can seamlessly fly across the edge of the map.

{% include youtube.html id="E3mho6J6OG8" %}

**Options**

Levels 1-3 are the original game levels, all other levels are new to Mayhem 2.

DCA are anti spaceship guns which will fire at the player if they get too close.

Wall collision can be turned off for new players to get used to the controls and playing the game.

**Controls**

Mayhem 2 supports joystick and keyboard control, joystick controls can be configured via the main menu.

Default joystick controls, assume an "xbox / ps like" joystick:

| Control | Action |
| --- | --- |
| Stick 1 | Left / Right |
| Button 1 (A) | Thrust |
| Button 2 (B) | Shield |
| Button 6 (RB) | Fire |

If joysticks are connected, they are used as the players controls, if there are less than 4 joysticks connected, keys are used for the rest of the players in order:

| Key | Left | Right | Shield | Thrust | Fire |
| --- | --- | --- | --- | --- | --- |
| 1 | z | x | c | v | g |
| 2 | left | right | pad del | pad 0 | pad enter |
| 3 | b | n | , | m | l |
| 4 | y | u | o | i | 0 |

**Install**

***For windows:***

Download the zip file from [https://github.com/martinohanlon/mayhem/archive/master.zip](https://github.com/martinohanlon/mayhem/archive/master.zip), open and copy mayhem-master to a folder.

Double click Mayhem2.exe in the mayhem-master folder.

Note - You maybe presented with message saying that the application was stopped from starting as it is unrecognised, click 'more info' and and choose 'run anyway'.

***For Raspberry Pi:***

Open a terminal and type:

```bash
sudo apt-get install liballegro4.4 liballegro4-dev
git clone https://github.com/martinohanlon/mayhem-pi
```

Run using:

```bash
cd mayhem-pi
./start
```

**Code**

The full source code is available on GitHub for [Windows](https://github.com/martinohanlon/mayhem) and [Raspberry Pi](https://github.com/martinohanlon/mayhem-pi).
