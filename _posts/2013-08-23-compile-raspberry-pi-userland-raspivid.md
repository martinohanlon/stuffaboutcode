---
title: 'Compile Raspberry Pi Userland / RaspiVid / RaspiStill'
date: 2013-08-23 21:43:00 +01:00
tags: [c, raspberry-pi]
redirect_from:
  - /2013/08/compile-raspberry-pi-userland-raspivid.html
---

I've been working on a few changes to the RaspiVid program which controls the raspberry pi camera board.

The first step was to get the code from github, [https://github.com/raspberrypi/userland](https://github.com/raspberrypi/userland) and compile it. The raspberry pi camera programs (RaspiVid and RaspiCam) are part of the 'userland' repository and as such I needed to compile the whole repository.

I got most of this information from [http://www.darkoperator.com/blog/2013/5/23/fixin-raspistill-and-raspivid-for-headless-streaming-on-the.html](http://www.darkoperator.com/blog/2013/5/23/fixin-raspistill-and-raspivid-for-headless-streaming-on-the.html).

**Install dependencies**

```bash
sudo apt-get install git-core gcc build-essential cmake vlc
```

**Download code**

```bash
mkdir ~/code

cd ~/code

git clone git://github.com/raspberrypi/userland.git
```

**Create make files**

```bash
cd ~/code/userland

sed -i 's/if (DEFINED CMAKE_TOOLCHAIN_FILE)/if (NOT DEFINED CMAKE_TOOLCHAIN_FILE)/g' makefiles/cmake/arm-linux.cmake
```

**Compile**

```bash
mkdir ~/code/userland/build

cd ~/code/userland/build

sudo cmake -DCMAKE_BUILD_TYPE=Release ..

sudo make
```

Wait - it will take about 15 minutes to compile the whole of the userland repository.

The executables will be created in the bin directory:

```bash
cd ~/code/userland/build/bin
```

**Re-compile**
 If you change any of the applications, you can re-compile using:

```bash
sudo make
```

It will only compile the changes you have made and will taken significantly less time than the first build.

**Install**
 If you want to install the newly built applications, use:

```bash
sudo make install
```
