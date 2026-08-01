---
title: 'Raspberry Pi - Initio Robot & Python Motor Control'
date: 2014-08-19 11:51:00 +01:00
tags: [gpio, python, raspberry-pi, robot]
redirect_from:
  - /2014/08/raspberry-pi-initio-robot-python-motor.html
---

When I was at the [2014 Raspberry Jamboree](http://www.raspberrypi.org/using-minecraft-raspberry-pi-edition-to-get-kids-computing/), I was luckily enough to 'acquire' (I won it, I didn't steal it!) a [4tronix initio robot chasis](http://www.4tronix.co.uk/initio/), unfortunately it sat on my shelf for nearly 6 months before I got time to have a go with it.

![](/assets/img/2014/08/initio.jpg)

When I opened up the box I found it also came with a [4tronix PiRoCon](http://4tronix.co.uk/blog/?p=146) robot controller as well - all good!

I wanted to control the robot using Python, so my first stop was the ever useful google, unfortunately other than one simple python example in [4tronix's PiRoCon github repository](https://github.com/4tronix/PiRoCon), the cupboard was bare. I did however know that Cymplecy (SimpleSi)'s [ScratchGPIO](http://cymplecy.wordpress.com/scratchgpio/)code supported the PiRoCon so this code also gave me some inspiration (!). I have since found out that 4tronix have some downloadable examples on their site, check out the very bottom of this [page](http://www.4tronix.co.uk/initio/) - doh!

I wired the motor's up as per the [instructions](http://4tronix.co.uk/blog/?p=41) on 4tronix's website and the speed sensors as per the [instructions](http://cymplecy.wordpress.com/2013/12/29/wheel-encoders-on-a-raspberry-pi-robot/) on Cymplecy's blog and I set about creating a motor control class, which would allow me to control the speed of the motors and also get data from the speed sensors (encoders).

This is my starting point for more advanced features and automation, but as always start small, grow big.

There is a more 'complete' example in the code below, but you use the motor controller class like this:

```python
import time
import motorControl

#setup gpio
GPIO.setmode(GPIO.BOARD)

#create motor control
motors = motorControl.MotorController()

#go forward - both motors at 100%
motors.start(100)
time.sleep(2)

#go forward in a curve
# - motor A at 100%
# - motor B at 50%
motors.start(100,50)
time.sleep(2)

#go backward at 100%
# - using negative power
motors.start(-100)
time.sleep(2)

#stop
motors.stop()

#cleanup gpio
GPIO.cleanup()
```

The full Motor Controller code is below and in my initio repository [github.com/martinohanlon/initio](https://github.com/martinohanlon/initio):

```python
#PiRoCon - 4Tronix Initio - Motor Controller
#Martin O'Hanlon
#www.stuffaboutcode.com

import sys
import time
import RPi.GPIO as GPIO

#motor pins
MOTORAFWRDPIN = 19
MOTORABWRDPIN = 21
MOTORBFWRDPIN = 24
MOTORBBWRDPIN = 26
#encoder pins
MOTORAENCODERPIN = 7
MOTORBENCODERPIN = 11

#motor states
STATEFORWARD = 1
STATESTOPPED = 0
STATEBACKWARD = -1

class MotorController:
    def __init__(self,
                 motorAForwardPin = MOTORAFWRDPIN,
                 motorABackwardPin = MOTORABWRDPIN,
                 motorBForwardPin = MOTORBFWRDPIN,
                 motorBBackwardPin = MOTORBBWRDPIN,
                 motorAEncoderPin = MOTORAENCODERPIN,
                 motorBEncoderPin = MOTORBENCODERPIN,):

        #setup motor classes
        self.motorA = Motor(motorAForwardPin, motorABackwardPin, motorAEncoderPin)
        self.motorB = Motor(motorBForwardPin, motorBBackwardPin, motorBEncoderPin)

    #motor properties
    @property
    def motorA(self):
        return self.motorA

    @property
    def motorB(self):
        return self.motorB

    #start
    def start(self, powerA, powerB = None):
        #if a second power isnt passed in, both motors are set the same
        if powerB == None: powerB = powerA
        self.motorA.start(powerA)
        self.motorB.start(powerB)

    #stop
    def stop(self):
        self.motorA.stop()
        self.motorB.stop()

    #rotate left
    def rotateLeft(self, power):
        self.motorA.start(power * -1)
        self.motorB.start(power)

    #rotate right
    def rotateRight(self, power):
        self.motorA.start(power)
        self.motorB.start(power * -1)

#class for controlling a motor
class Motor:
    def __init__(self, forwardPin, backwardPin, encoderPin):
        #persist values
        self.forwardPin = forwardPin
        self.backwardPin = backwardPin
        self.encoderPin = encoderPin

        #setup GPIO pins
        GPIO.setup(forwardPin, GPIO.OUT)
        GPIO.setup(backwardPin, GPIO.OUT)
        GPIO.setup(encoderPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        #add encoder pin event
        GPIO.add_event_detect(encoderPin, GPIO.RISING, callback=self._encoderCallback,bouncetime=2)

        #setup pwm
        self.forwardPWM = GPIO.PWM(forwardPin,50)
        self.backwardPWM = GPIO.PWM(backwardPin,50)

        #setup encoder/speed ticks
        self.totalTicks = 0
        self.currentTicks = 0

        self.state = STATESTOPPED

    #motor state property
    @property
    def state(self):
        return self.state

    #start
    def start(self, power):
        #forward or backward?
        # backward
        if power < 0:
            if self.state != STATEBACKWARD: self.stop()
            self._backward(power)
            self.state = STATEBACKWARD

        # forward
        if power > 0:
            if self.state != STATEFORWARD: self.stop()
            self._forward(power)
            self.state = STATEFORWARD

        # stop
        if power == 0:
            self.stop()

    #stop
    def stop(self):
        #stop motor
        self.forwardPWM.stop()
        self.backwardPWM.stop()
        self.state = STATESTOPPED
        #reset ticks
        self.currentTicks = 0

    #private function to calculate the freq for the PWM
    def _calcPowerAndFreq(self, power):
        # make power between 0 and 100
        power = max(0,min(100,abs(power)))
        # make half of freq, minimum of 11
        freq = max(11,abs(power/2))
        return power, freq

    #forward
    def _forward(self, power):
        #start forward motor
        power, freq = self._calcPowerAndFreq(power)
        self.forwardPWM.ChangeFrequency(freq)
        self.forwardPWM.start(power)

    #backward
    def _backward(self, power):
        #start backward motor
        power, freq = self._calcPowerAndFreq(power)
        self.backwardPWM.ChangeFrequency(freq)
        self.backwardPWM.start(power)

    #encoder callback
    def _encoderCallback(self, pin):
        self.totalTicks += 1
        self.currentTicks += 1

#tests
if __name__ == '__main__':

    try:
        #setup gpio
        GPIO.setmode(GPIO.BOARD)

        #create motor control
        motors = MotorController()

        #forward
        print("forward")
        motors.start(100)
        time.sleep(2)

        print("encoder ticks")
        print(motors.motorA.totalTicks)
        print(motors.motorB.totalTicks)

        #backward
        print("backward")
        motors.start(-50)
        time.sleep(2)

        #forward curve
        print("forward curve")
        motors.start(100,50)
        time.sleep(2)

        #rotate left
        print("rotate left")
        motors.rotateLeft(50)
        time.sleep(2)

        #rotate right
        print("rotate right")
        motors.rotateRight(50)
        time.sleep(2)

        #stop
        print("stop")
        motors.stop()

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

Its my first time doing any robotics but so far I have been impressed with the [Initio](http://www.4tronix.co.uk/initio), the build quality and support seem really good - let the robot roll!
