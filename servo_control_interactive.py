#!/usr/bin/python

# This gives us control of the Raspberry Pi's pins.
import RPi.GPIO as GPIO

# This is only used for time delays... standard Python stuff.
import time

# Tell i which pin number we'll  be using to refer to the GPIO pains.
# We will use the BCM pin ordering.
GPIO.setmode(GPIO.BCM)

# We will tell the Broadcom CPU which pins do what.
# There are many pins and most have up to 5 different functions,
# each with a default.  Check the pinout to find non-specialized
# "GPIO" pins.  We'll use P!-Pin_11 (using BOARD reference),
# which is the same as GPIO17 (Broadcom / BCM reference).
# We need our pin to use the GPIO digital output function, so we just
# tell it to designate this pin for OUTPUT.
pan_pin = 18
tilt_pin = 27
GPIO.setup(pan_pin, GPIO.OUT)
GPIO.setup(tilt_pin, GPIO.OUT)

# Now we can use PWM on pins.  It's software PWM, so don't expect perfect
# results.  Linux is a multitasking OS so other processes could interrupt
# the process which generate the PWM signal at any time.
# Raspberry Pi has a hardware PWm channel, but this Pythong library
# does not yet support it.  
frequency_hertz = 50
pan_pwm = GPIO.PWM(pan_pin, frequency_hertz)
tilt_pwm = GPIO.PWM(tilt_pin, frequency_hertz)

# How to position a servo?  All servos are pretty much the same.
# Send repeated purses of an absolute duration (not a relative duty cycle)
# between 0.40 ms and 2.5 ms in duration.  A single pulse will only move it
# a short distance in the desired direction.  Repeated pulses will continue
# its movement and then once it arrives at the specified position it will
# insruct the motor to forcefully hold its position.
min_position = 0.40
max_position = 2.5

# total number of milliseconds in a a cycle.  Given this, we will then 
# know both how long we want to pulse in this cycle and how long tghe 
# cycle itself is.  That is all we need to calculate a duty cycle as 
# a percentage.
ms_per_cycle = 1000 / frequency_hertz
 
# These loops will ask to adjust the pan and tilt position.
x = '50'
while (x != 'end'):
	x = raw_input('Pan position [0 - 100 or \'end\' to finish]: ')
	if (x != 'end') and (unicode.isnumeric(unicode(x))):
		position = (int(x) * (max_position - min_position) / 100) + min_position
		duty_cycle_percentage = position * 100 / ms_per_cycle
		print("Pan position: " + str(position))
		print("Duty Cycle: " + str(duty_cycle_percentage))
		print("")
		pan_pwm.start(duty_cycle_percentage)
		time.sleep(.5)

pan_pwm.stop()
x = '50'
while (x != 'end'):
	x = raw_input('Tilt position [0 - 100 or \'end\' to finish]: ')
	if (x != 'end') and (unicode.isnumeric(unicode(x))):
		position = (int(x) * (max_position - min_position) / 100) + min_position
		duty_cycle_percentage = position * 100 / ms_per_cycle
		print("Tilt position: " + str(position))
		print("Duty Cycle: " + str(duty_cycle_percentage))
		print("")
		tilt_pwm.start(duty_cycle_percentage)
		time.sleep(.5)

tilt_pwm.stop()
# We have shut all our stuff down but we should do a complete
# close on all GPIO stuff.  There's only one copy of real hardware.
# We need to be polite and put it back the way we found it.
GPIO.cleanup()

