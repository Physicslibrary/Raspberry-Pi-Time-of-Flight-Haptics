#!/usr/bin/env python

import pigpio
import VL53L1X
import threading
import time
import sys

# vl53l1x-pi-zero-w-lra.py

# https://github.com/Physicslibrary/Raspberry-Pi-Time-Flight-Haptics

# MIT License

# Copyright (c) 2021 Hartwell Fong

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# June 2021.

# Explores using a Raspberry Pi to oscillate LRA motors with data from a Pimoroni VL53L1X Time of Flight sensor.

pi = pigpio.pi()

pi.set_PWM_frequency(17,200)
pi.set_PWM_frequency(27,200)
pi.set_PWM_frequency(22,200)

pi.set_PWM_frequency(5,200)
pi.set_PWM_frequency(6,200)
pi.set_PWM_frequency(26,200)

pi.set_PWM_frequency(23,200)
pi.set_PWM_frequency(24,200)
pi.set_PWM_frequency(25,200)

# nine zones in VL53L1X ROI (assigned a number for "if(roi > 1000)" to start things)

roi1 = 100000
roi2 = 100000
roi3 = 100000

roi4 = 100000
roi5 = 100000
roi6 = 100000

roi7 = 100000
roi8 = 100000
roi9 = 100000

dutycycle = 0.2

# PWM six more gpio pins at 0.2% duty cycle to see how processor/pigpiod handle loads

pi.set_PWM_dutycycle(5,255*dutycycle)
pi.set_PWM_dutycycle(6,255*dutycycle)
pi.set_PWM_dutycycle(26,255*dutycycle)

pi.set_PWM_dutycycle(23,255*dutycycle)
pi.set_PWM_dutycycle(24,255*dutycycle)
pi.set_PWM_dutycycle(25,255*dutycycle)

tof = VL53L1X.VL53L1X(i2c_bus=1,i2c_address=0x29)
tof.open()
tof.set_timing(66000,70)

# for now, three threads to pulse LRAs based on VL53L1X ranging of three ROI
# testing to 1m

def lra1():

        while True:

                if(roi1 > 1000):
                        pi.set_PWM_dutycycle(17,255*dutycycle)
                        time.sleep(1.0)
                        pi.set_PWM_dutycycle(17,255*0)
                        time.sleep(1.0)

                if(roi1 > 500 and roi1 < 1000):
                        pi.set_PWM_dutycycle(17,255*dutycycle)
                        time.sleep(0.5)
                        pi.set_PWM_dutycycle(17,255*0)
                        time.sleep(0.5)

                if(roi1 < 500):
                        pi.set_PWM_dutycycle(17,255*dutycycle)
                        time.sleep(0.1)
                        pi.set_PWM_dutycycle(17,255*0)
                        time.sleep(0.1)

                if (roi1 < 10):
                        break

def lra2():

        while True:

                if(roi2 > 1000):
                        pi.set_PWM_dutycycle(27,255*dutycycle)
                        time.sleep(1.0)
                        pi.set_PWM_dutycycle(27,255*0)
                        time.sleep(1.0)

                if(roi2 > 500 and roi2 < 1000):
                        pi.set_PWM_dutycycle(27,255*dutycycle)
                        time.sleep(0.5)
                        pi.set_PWM_dutycycle(27,255*0)
                        time.sleep(0.5)

                if(roi2 < 500):
                        pi.set_PWM_dutycycle(27,255*dutycycle)
                        time.sleep(0.1)
                        pi.set_PWM_dutycycle(27,255*0)
                        time.sleep(0.1)

                if (roi1 < 10):
                        break
def lra3():

        while True:

                if(roi3 > 1000):
                        pi.set_PWM_dutycycle(22,255*dutycycle)
                        time.sleep(1.0)
                        pi.set_PWM_dutycycle(22,255*0)
                        time.sleep(1.0)

                if(roi3 > 500 and roi3 < 1000):
                        pi.set_PWM_dutycycle(22,255*dutycycle)
                        time.sleep(0.5)
                        pi.set_PWM_dutycycle(22,255*0)
                        time.sleep(0.5)

                if(roi3 < 500):
                        pi.set_PWM_dutycycle(22,255*dutycycle)
                        time.sleep(0.1)
                        pi.set_PWM_dutycycle(22,255*0)
                        time.sleep(0.1)

                if (roi1 < 10):
                        break

thread1 = threading.Thread(target=lra1)
thread1.start()

thread2 = threading.Thread(target=lra2)
thread2.start()

thread3 = threading.Thread(target=lra3)
thread3.start()

while True:

        tof.set_user_roi(VL53L1X.VL53L1xUserRoi(0,3,3,0))
        tof.start_ranging(0)
        roi1 = tof.get_distance()
        tof.stop_ranging()

        tof.set_user_roi(VL53L1X.VL53L1xUserRoi(0,9,3,6))
        tof.start_ranging(0)
        roi2 = tof.get_distance()
        tof.stop_ranging()

        tof.set_user_roi(VL53L1X.VL53L1xUserRoi(0,15,3,12))

        tof.start_ranging(0)
        roi3 = tof.get_distance()
        tof.stop_ranging()

        if (roi1 < 10): # a way to exit loop by placing something 10mm from sensor
                break

#        print(roi3) # for checking and debugging
#        print(roi2)
#        print(roi1)
#        print("\n")

time.sleep(0.5)

tof.close()

# turn off LRA motors

pi.set_PWM_dutycycle(17,0)
pi.set_PWM_dutycycle(27,0)
pi.set_PWM_dutycycle(22,0)

pi.set_PWM_dutycycle(5,0)
pi.set_PWM_dutycycle(6,0)
pi.set_PWM_dutycycle(26,0)

pi.set_PWM_dutycycle(23,0)
pi.set_PWM_dutycycle(24,0)
pi.set_PWM_dutycycle(25,0)

sys.exit()
