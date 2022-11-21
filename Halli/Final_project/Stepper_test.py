#!usr/bin/python
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)    # Setup of GPIO´s
GPIO.setwarnings(False)     # Don´t need no negativity in my life
GPIO.setup(16, GPIO.OUT)    # pins 12, 16 and 18 are used as outputs
GPIO.setup(18, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, True)       # pin 12 is high

def enable_driver():        # Function that enables the driver to run
    GPIO.output(12, False)  # the motor

def disable_driver():       # Function that prevents the driver from 
    GPIO.output(12, True)   # moving the motor

def rotation(rotate):             # will be used to change rotation of motor
    if rotate == "clockwise":
        return False            # False is counter clockwise rotation
    if rotate == "counter-clockwise":
        return True
    else: 
        return False

def degrees(deg):
    # 1599 steps are 360 degrees
    # 4.441 steps in one degree
    steps = 1600
    deg_in_circle = 360
    one_degree = steps/deg_in_circle
    return deg * one_degree

def spin_motor(steps_run):
    enable_driver()
    steps = 0
    while steps < steps_run: # one rotation of the motor is 1599 steps
        GPIO.output(16, True)   # output pin 16 high
        time.sleep(0.00005)      # 0.1 millisecond wait
        GPIO.output(16, False)  # output pin 16 low
        time.sleep(0.00005)      # 0.1 millisecond wait
        # This should result in frequency of 5000 Hz
        steps += 1
    disable_driver()

rotate = "clockwise"
GPIO.output(18, rotation(rotate))
for _ in range(0,3):
    spin_motor(degrees(45))
    time.sleep(1)

GPIO.cleanup()