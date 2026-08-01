---
title: 'Raspberry Pi 2 or 3 - Minecraft Server'
date: 2015-02-04 22:37:00 +00:00
tags: [minecraft, raspberry-pi]
redirect_from:
  - /2015/02/raspberry-pi-2-minecraft-server.html
---

The new Raspberry Pi 2 has got twice the RAM and a load more processing power, so will it make a better Minecraft server? The old Pi made an adequate Minecraft server providing you only had a few players and you kept the view distance low.

Update - The Pi 3 takes it up a step and provides more stability and connectivity is a lot easier.

![](/assets/img/2015/02/2015-02-03_21.16.37.jpg)

I tried both the vanilla server and a spigot server, both similar results, both performed reasonably well, but Spigot seemed a little more stable (but this is only based on feeling). I was only able to test with up to 3 players but it worked well under those conditions.

{% include youtube.html id="xW4SZZLGjWU" %}

Setting up your own server is pretty simple.

You will need to download either the [vanilla server from Mojang](https://minecraft.net/download) or [build your own spigot server jar file](http://www.spigotmc.org/wiki/buildtools/).

Note - The instructions below, will take you through how to create a vanilla server, if you have built spigot the only difference will be the name of the 'jar file' you put into the start.sh file

**1.** Make a directory for your Minecraft server

```bash
mkdir ~/MinecraftServer
cd ~/MinecraftServer
```

**2.** Download the 1.8.1 vanilla Minecraft server jar file

```bash
wget https://s3.amazonaws.com/Minecraft.Download/versions/1.8.1/minecraft_server.1.8.1.jar
```

**3.** Create a script to run the server jar file

```bash
nano start.sh
```

Enter the following command which will run the server

```bash
java -Xmx1024M -Xms512M -jar minecraft_server.1.8.1.jar nogui
```

Ctrl X to exit & save

**4.** Make the script executable:

```bash
chmod +x start.sh
```

**5.** Run the server

```bash
./start.sh
```

You should receive a message asking you to accept the EULA.

![](/assets/img/2015/02/eula.jpg)

**6.** Accept the EULA (end user license agreement), open eula.txt

```bash
nano eula.txt
```

Change:

```text
eula=false
```

To:

```text
eula=true
```

Ctrl X to save and exit

**7.** Run the server

```bash
./start.sh
```

The first time the server runs it will take a while to start as it creates a new world.

Once you see the word "Done", the server is up and running and you should be able to connect to the server using Minecraft choosing Multiplayer, Direct Connect and entering the IP address of the Pi.

![](/assets/img/2015/02/done.jpg)

You can shutdown the server by typing the command "stop" in the command window .

If you find the server is slow, particularly when generating chunks (i.e. creating new bits of the world when you get to the edge), you could try reducing the view distance. I reduced it from 10 to 7 and this seemed to make the server more responsive.

**8.** Edit view-distance in server.properties

```bash
nano server.properties
```

Change:

```text
view-distance=10
```

To:

```text
view-distance=7
```

Ctrl X to save and exit

Restart the server for the change to take effect.
