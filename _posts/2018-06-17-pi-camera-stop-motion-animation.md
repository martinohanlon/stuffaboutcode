---
title: 'Pi Camera stop motion animation'
date: 2018-06-17 21:23:00 +01:00
tags: [python, raspberry-pi]
redirect_from:
  - /2018/06/pi-camera-stop-motion-animation.html
---

In preparation for a Raspberry Pi event I decided to create a simple GUI for creating stop motion animations using the Pi camera module to use for a demo.

![](/assets/img/2018/06/picamera_setup.jpg)

Its a really simple application, you start it up, you click "take image", you re-position the scene, you click "take image" and so on until you are happy with your animation and you click "save" to store it as an animated gif.

![](/assets/img/2018/06/df5pzagxuaa3im7.jpg)

![](/assets/img/2018/06/animation1529238449.919678.gif)

You can find the source code at [gist.github.com/martinohanlon](https://gist.github.com/martinohanlon/52a7557a91d9e5b353a278447fbacc34).

**Install**
 1. Connect a camera module
 2. Enable the camera (Menu > Preferences > Raspberry Pi Configuration, Interfaces, Camera)
 3. Open a terminal (Menu > Accessories > Terminal), install the modules and download the code:

```bash
sudo pip3 install guizero
sudo pip3 install imageio
wget -O guizero_stopmotion.py https://gist.githubusercontent.com/martinohanlon/52a7557a91d9e5b353a278447fbacc34/raw/guizero_stopmotion.py
```

4. Run the program:

```bash
python3 guizero_stopmotion.py
```

**A couple of "interesting" things about this project**
 The gui was created using [guizero](https://lawsie.github.io/guizero/) which is a super simple to use library for creating GUI's, definitely have a look.

Most of the work was finding a way to create animated gifs in Python and working with images in memory rather than stored on disk

When the image is captured from the camera it isn't stored to a file, it is stored in a numpy array, this means each frame is only stored in memory making it faster:

```text
# create the camera
camera = PiCamera(resolution="640x480")
camera_output = PiRGBArray(camera)
...
# capture the image
camera.capture(camera_output, "rgb")
# append the camera image to the list as a numpy array
animation.images.append(camera_output.array)
```

The python module imageio is used to create the gif by passing the frames as a list, but again rather than being written to disk each time it is created as an in memory BytesIO stream:

```text
gif_output = BytesIO()
imageio.mimsave(gif_output, animation.images, format="gif")
```

When the animated gif is displayed in guizero the BytesIO stream has to be open into a PIL Image.

```text
animation.image = Image.open(gif_output)
```
