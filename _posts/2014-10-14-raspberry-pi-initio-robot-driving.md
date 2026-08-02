---
title: 'Raspberry Pi Initio Robot - Driving Straight'
date: 2014-10-14 05:54:00 +01:00
tags: [python, raspberry-pi, robot]
redirect_from:
  - /2014/10/raspberry-pi-initio-robot-driving.html
---

I've been continuing my Raspberry Pi Robot project (see previous [post](/posts/raspberry-pi-initio-robot-python-motor/)) and the next challenge was to create some functions to allow my robot to be autonomous.

First challenge... Drive in a straight line! Not as easy as it seems. You put both motors onto 100% power forward and it veers slightly to the right (or in my case it does!). The reason is simple the motors which drive the left and right wheels don't turn at exactly the same rate.

What to do. Well the [Initio](http://www.4tronix.co.uk/initio/) robot chasis I have is fitted with wheel encoders which 'tick' when the wheels go round to show how far they have moved, so if I wanted to make the robot go straight I needed to make left and right wheels moved the same distance.

So, I turn both motors on and count the encoder ticks, if the left one is getting ahead I slow it down a bit, unless the right catches up and vice versa!

I created a new python class called NavigationController which is where I will put all of my robots autonomous functions and created a straight function which when passed a power and a distance would drive straight until that distance was reached. It constantly checks the encoder values for both wheels and adjusts the power of the 2 motors to make sure it goes straight.

**Code**
 You can see all my robot code here [https://github.com/martinohanlon/initio](https://github.com/martinohanlon/initio)

```python
#Navigation class to accurately move initio robot
#Martin O'Hanlon
#www.stuffaboutcode.com

#import modules
import sys
import motorControl
import time
import RPi.GPIO as GPIO
import math
import thread

#states
STATEMOVING = 1
STATESTOPPED = 0

#Constant of Proportionality
# multipler used to convert difference in motor position to power change
KP = 2

#Wheel circumference
#(in mm)
WHEELCIRCUMFERENCEMM = 174.0
#(in encoder ticks)
WHEELCIRCUMFERENCE = 36.0

#Encoder to mm ratio (wheel circumference in mm / wheel circumference to encoder ticks)
ENCODERTOMM = WHEELCIRCUMFERENCEMM / WHEELCIRCUMFERENCE

class NavigationController:
    #initialise - motors is the MotorControl object
    def __init__(self, motors, distanceInMM = False):
        self.motors = motors
        self.state = STATESTOPPED

        #if distanceinMM is set to True all distance are consider to be in millimeters
        # if False all distances are in encoder ticks
        self.distanceInMM = distanceInMM

    #navigation state property
    @property
    def state(self):
        return self.state

    #motors property
    @property
    def motors(self):
        return self.state

    #move the robot in a straight line
    def straight(self, power, distance = None, ownThread = False):
        # if distance is not passed, continues forever and launches a seperate thread
        # if distance is passed, loops until distance is reached
        if distance == None:
            #set a really long distance - this is a 'bit' dirty...  But simple!
            distance = 99999999999
            #call it in its own thread
            ownThread = True

        if ownThread:
            #call it in its own thread
            thread.start_new_thread(self._straight,(power, distance))
        else:
            self._straight(power, distance)

    #move the robot in a staight line
    def _straight(self, power, distance):

        #convert distance
        if self.distanceInMM: distance = self._convertMillimetersToTicks(distance)

        #if the state is moving, set it to STOP
        if(self.state != STATESTOPPED): self.stop()

        #turn on both motors
        self.motors.start(power, power)

        #change state to moving
        self.state = STATEMOVING

        #keep track of the last motor error, so we only change if we need too
        lastMotorError = 0

        #loop until the distance is reached or it has been STOPPED, correcting the power so the robot goes straight
        while(self.motors.motorA.currentTicks < distance and self.state == STATEMOVING):

            #get the number of ticks of each motor
            #get the error by minusing one from the other
            motorError = self.motors.motorA.currentTicks - self.motors.motorB.currentTicks
            #print("motorError = " + str(motorError))

            #only change if the motorError has changed
            if(motorError != lastMotorError):

                #work out the value to slow the motor down by using the KP
                powerChange = (motorError * KP)
                #print("powerChange = " + str(powerChange))

                #in the unlikely event they are equal!
                if(powerChange == 0):
                    self.motors.start(power, power)
                else:
                    #if its going backward, turn the power change into a negative
                    if power < 0: powerChange * -1

                    #if its a positive number
                    if(motorError > 0):
                        #set motor A to power - 'slow down value'
                        #set motor B to power
                        self.motors.start(power - powerChange, power)
                    #if its a negative number
                    if(motorError < 0):
                        #set motor A to power
                        #set motor B to power - 'slow down value'
                        self.motors.start(power, power - powerChange)

            #update last motor error
            lastMotorError = motorError

        # if they havent already been stopped - stop the motors
        self.stop()

    #stops the robot
    def stop(self):
        self.motors.stop()
        self.state = STATESTOPPED

    def _convertMillimetersToTicks(self, millimeters):
        print ENCODERTOMM
        return int(round(millimeters / ENCODERTOMM,0))

#tests
if __name__ == '__main__':

    try:
        #setup gpio
        GPIO.setmode(GPIO.BOARD)

        #create motor control
        motors = motorControl.MotorController()

        #create navigation control, use True for distances in millimeters
        nav = NavigationController(motors, True)

        #run a straight line just through motor control
        print("straight line, no correction")
        motors.start(100,100)
        time.sleep(10)
        #stop
        print("stop")
        motors.stop()
        #get length
        print("encoder ticks")
        print(motors.motorA.totalTicks)
        print(motors.motorB.totalTicks)

        #time.sleep(10)

        #reset encoder ticks
        motors.motorA.resetTotalTicks()
        motors.motorB.resetTotalTicks()

        #run a straight line through nav control
        print("straight line, with correction")
        nav.straight(100, 500)
        #get length
        print("encoder ticks")
        print(motors.motorA.totalTicks)
        print(motors.motorB.totalTicks)

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        print ("cleanup")
        #cleanup gpio
        GPIO.cleanup()
```

Next job - turning in an arc!
