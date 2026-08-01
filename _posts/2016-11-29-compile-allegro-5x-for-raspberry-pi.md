---
title: 'Compile Allegro 5.x for Raspberry Pi'
date: 2016-11-29 18:12:00 +00:00
tags: [games, raspberry-pi]
redirect_from:
  - /2016/11/compile-allegro-5x-for-raspberry-pi.html
---

I am in the process of porting [Mayhem 2](http://www.stuffaboutcode.com/2016/06/mayhem-2-open-source-cave-shooter.html) to Allegro 5 (with the help of [Jonas Karlsson](https://github.com/karjonas)), and wanted to compile the latest version of Allegro on the Pi, as only an older version is available through apt.
**Install the dependencies**

```bash
sudo apt-get install build-essential git cmake cmake-curses-gui xorg-dev libgl1-mesa-dev libglu-dev libpng-dev libcurl4-nss-dev libfreetype6-dev libjpeg-dev libvorbis-dev libopenal-dev libphysfs-dev libgtk2.0-dev libpulse-dev libflac-dev libdumb1-dev
```

**Get the Code**

```bash
git clone https://github.com/liballeg/allegro5.git
cd allegro5
```

**Check out the version you want** - see [here](https://github.com/liballeg/allegro5/branches/all) for a list of versions

```bash
git checkout 5.2.1
```

**Build it**

```bash
mkdir build
cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../cmake/Toolchain-raspberrypi.cmake
make
```

**Install it**

```bash
sudo make install
export PKG_CONFIG_PATH=/home/pi/allegro5/build/lib/pkgconfig
sudo ldconfig
```
