---
title: 'Nintendo DS - Homebrew Paint Program'
date: 2013-01-31 21:42:00 +00:00
tags: [games]
redirect_from:
  - /2013/01/nintendo-ds-homebrew-paint-program.html
---

I was off snowboarding last week and found this great little program on my Nintendo DS which according to the date modified on the source file I wrote back in February 2008, which allows you to create your own little pictures using the touch screen.

![](/assets/img/2013/01/2013-01-31-21.22.50.jpg)

You draw on the screen using the touch pen and change the color by holding down Y, X, A and using Up and Down to add or remove Red, Green and Blue to change the colour of the pen.

It uses a library called "[PA_Lib](http://gamebrew.org/wiki/PA_lib)" which as I remember back in 2008 was pretty good, but it seems like things have moved on in the 5 years since I created this program and other libraries and frameworks are more mature and well established.

Regardless the code is really simple, there are only 2 functions:

- main - which controls the program and is the starting point
- ColorUpDownControl - which controls setting the color

The main function is below, but if you want to [download](https://docs.google.com/a/ohanlonweb.com/folder/d/0BwqjqhNUlUf1MnZwWmxNN2RYQ3c/edit) it and have a go, I've uploaded all the [source, libraries, build utilities and executable](https://docs.google.com/a/ohanlonweb.com/folder/d/0BwqjqhNUlUf1MnZwWmxNN2RYQ3c/edit).

```c
// Includes
#include <PA9.h>       // Include for PA_Lib

int ColorUpDownControl(int intColor, int intTicks) {

 if (Pad.Newpress.Up) {
      if (intColor == 31) {
         intColor = 0;
      } else {
    intColor++;
    }
   } else {
    if (Pad.Held.Up) {
       if ((intTicks % 10) == 0) {
        if (intColor == 31) {
           intColor = 0;
        } else {
      intColor++;
      }
   }
    }
   }

   if (Pad.Newpress.Down) {
      if (intColor == 0) {
         intColor = 31;
      } else {
    intColor--;
    }
   } else {
    if (Pad.Held.Down) {
       if ((intTicks % 10) == 0) {
        if (intColor == 0) {
           intColor = 31;
        } else {
      intColor--;
      }
    }
    }
 }
 return intColor;
}

// Function: main()
int main(int argc, char ** argv)
{

   int intRed = 31;
   int intGreen = 31;
   int intBlue = 31;
   int intTicks = 0;

 PA_Init();    // Initializes PA_Lib
 PA_InitVBL(); // Initializes a standard VBL

 PA_SetBgPalCol(0, 0, PA_RGB(0, 0, 0)); // set the bottom screen color to black

 // This will initialise a 16 bit background on each screen. This must be loaded before any other background.
 // If you need to load this after a backgrounds, you'll have to use PA_ResetBgSys, PA_Init8bit, then reload
 // your backgrounds...
 PA_Init16bitBg(0, 3);
 PA_Init16bitBg(1, 3);

 PA_InitText(1, 0); // Text system for top screen
 PA_SetTextCol(1, 31, 31, 31); // Set text color to white

 PA_OutputText(1, 1, 1, "Mart Drawing - 16bit");

 // Infinite loop to keep the program running
 while (1)
 {
  // Simple draw function, draws on the screen...
  PA_16bitDraw(0, PA_RGB(intRed, intGreen, intBlue));  // Color : full red...

  // Button control
  if ((Pad.Newpress.Y) || (Pad.Held.Y)) {
     intRed = ColorUpDownControl(intRed, intTicks);
  }
  if ((Pad.Newpress.X) || (Pad.Held.X)) {
     intGreen = ColorUpDownControl(intGreen, intTicks);
  }
  if ((Pad.Newpress.A) || (Pad.Held.A)) {
     intBlue = ColorUpDownControl(intBlue, intTicks);
  }
  if (Pad.Newpress.Start) {
     PA_Clear16bitBg(0);
  }

  // Set the current color on the top screen
  PA_Draw16bitRect(1, 10, 20, 40, 50, PA_RGB(intRed, intGreen, intBlue));

  //Increment & reset ticks
  intTicks++;
  if (intTicks > 1000) intTicks = 0;

  // Debug Info
  PA_OutputText(1, 1, 18, "Stylus X = %d  ", Stylus.X);
  PA_OutputText(1, 1, 19, "Stylus Y = %d  ", Stylus.Y);
  PA_OutputText(1, 1, 20, "R = %d  G = %d  B = %d   ", intRed, intGreen, intBlue);
  //PA_OutputText(1, 1, 21, "Ticks = %d   ", intTicks);

  PA_WaitForVBL();
 }

 return 0;
} // End of main()
```
