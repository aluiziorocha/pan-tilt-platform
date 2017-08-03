#!/usr/bin/python

import RPi.GPIO as GPIO
import time

file = open("pan_tilt.txt")
pan, tilt = file.read().strip().split()
tilt = int(tilt)

if tilt <= 70:
    tilt = tilt + 5

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    tilt_pin = 27
    GPIO.setup(tilt_pin, GPIO.OUT)
    
    frequency_hertz = 50
    tilt_pwm = GPIO.PWM(tilt_pin, frequency_hertz)
    
    min_position = 0.40
    max_position = 2.5
    
    ms_per_cycle = 1000 / frequency_hertz
     
    position = (tilt * (max_position - min_position) / 100) + min_position
    duty_cycle_percentage = position * 100 / ms_per_cycle
    tilt_pwm.start(duty_cycle_percentage)
    time.sleep(.5)
    tilt_pwm.stop()
    
    GPIO.cleanup()

    file = open("pan_tilt.txt", "w+")    
    file.write(pan + " " + str(tilt)) 

file.close()
