#!/usr/bin/python

import RPi.GPIO as GPIO
import time

file = open("pan_tilt.txt")
pan, tilt = file.read().strip().split()
pan = int(pan)

if pan >= 30:
    pan = pan - 5

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    pan_pin = 18
    GPIO.setup(pan_pin, GPIO.OUT)
    
    frequency_hertz = 50
    pan_pwm = GPIO.PWM(pan_pin, frequency_hertz)
    
    min_position = 0.40
    max_position = 2.5
    
    ms_per_cycle = 1000 / frequency_hertz
     
    position = (pan * (max_position - min_position) / 100) + min_position
    duty_cycle_percentage = position * 100 / ms_per_cycle
    pan_pwm.start(duty_cycle_percentage)
    time.sleep(.5)
    pan_pwm.stop()
    
    GPIO.cleanup()

    file = open("pan_tilt.txt", "w+")    
    file.write(str(pan) + " " + tilt) 

file.close()
