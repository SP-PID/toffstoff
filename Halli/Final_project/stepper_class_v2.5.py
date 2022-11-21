from tkinter import *
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import sys
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
import time
import board
import digitalio as dg

SKREF = 200
pulse = dg.DigitalInOut(board.D17)
pulse.direction = dg.Direction.OUTPUT
direc = dg.DigitalInOut(board.D15)
direc.direction = dg.Direction.OUTPUT
enable = dg.DigitalInOut(board.D18)
enable.direction = dg.Direction.OUTPUT2000
ms1 = dg.DigitalInOut(board.D20)
ms1.direction = dg.Direction.OUTPUT
ms2 = dg.DigitalInOut(board.D21)
ms2.direction = dg.Direction.OUTPUT
ms1.value = False
ms2.value = False
stop = dg.DigitalInOut(board.D9)
stop.direction = dg.Direction.INPUT
stop.pull = dg.Pull.DOWN

class SetPoint():
    def __init__(self) -> None:
        self.pi = 3.14159265359                                                         # Everybody knows pi
        self.degrees_per_step = 1.8                                                     # for some reason this motor will move 0.225 degrees per step
        self.diameter = 19.65                                                           # diameter in millimeters
        self.total_travel = 820                                                         # total travel of the gantry plate is 800 millimeters
        self.circumference = self.diameter * self.pi                                    # circumference in millimeters
        self.steps_per_revolution = 360 / self.degrees_per_step                         # number of steps in a revolution
        self.distance_per_step = self.circumference / self.steps_per_revolution         # distance per step in millimeters
        self.steps_total = self.total_travel / self.distance_per_step                   # total number of steps per length of travel of gantry plate
        self.rotation = False                                                           # variable for which direction the motor will spin
        self.direction = "up"                                                           # variable to tell program to go up or down
        self.current_position = 0                                                       # initializes in lowest position
        self.highest_position = self.steps_total                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position
        self.disable_microstepping()
        self.microstepping = False
        self.reset_actuator()                                                           # actuator finds zero position (bottom)

    def get_total_steps(self):
        ''' Returns total number of steps for end to end travel '''
        return self.steps_total

    def enable_driver(self):        
        ''' Function that enables Easydriver for use '''
        enable.value = False

    def disable_driver(self):        
        ''' Function that disables Easydriver after use '''
        enable.value = True 

    def update_rotation(self,direction):
        ''' Function updates variable for gantry travel direction '''
        self.direction = direction
        if self.direction == "up":
            self.rotation = True            # False means actuator moves down
        if self.direction == "down":
            self.rotation = False
        direc.value = self.rotation

    def pulse(self):
        ''' Function sends out one pulse on pulse pin '''
        pulse.value = True
        time.sleep(0.0007)      # wait
        pulse.value = False
        time.sleep(0.0007)      # wait

    def update_position(self,distance):
        ''' Function keeps track of current position of gantry '''
        if self.direction == "down":
            if self.microstepping:
                self.current_position -= distance/8
            else:
                self.current_position -= distance
        if self.direction == "up":
            if self.microstepping:
                self.current_position += distance/8
            else:
                self.current_position += distance

    def move_to_position(self,position):
        ''' Function moves gantry to a requested position '''
        steps = self.current_position - position
        if self.current_position == position:
            return         
        if self.current_position > position:
            self.update_rotation("down")
        if self.current_position < position:
            self.update_rotation("up")
            steps = -steps
        self.spin_motor(steps)
        #print("Current position " + str(self.current_position))

        

    def spin_motor_helper(self,steps):
        ''' Function that moves the stepper motor '''
        self.enable_driver()
        for _ in range(0, steps):
            self.pulse()                    # one high and one low on pin
            self.update_position(1)
            if self.current_position >= self.highest_position:  # stops before top end of profile
                break
            if self.current_position <= self.lowest_position:   # stops before bottom end of profile
                break                 
        self.disable_driver()

    def spin_motor(self,steps):
        if steps <= 10:
            #print("Microstepping")
            self.enable_microstepping()
            self.spin_motor_helper(steps*8)
            self.disable_microstepping()
        else:
            self.spin_motor_helper(steps)
        self.current_position = int(round(self.current_position,0))

    def enable_microstepping(self):
        #print("Microstepping enabled!")
        self.microstepping = True
        ms1.value = True
        ms2.value = True

    def disable_microstepping(self):
        #print("Microstepping disabled!")
        self.microstepping = False
        ms1.value = False
        ms2.value = False       

    def reset_actuator(self):
        ''' Function that moves the gantry to zero position (bottom) '''
        self.update_rotation("down")    # sets travel direction to down
        self.enable_driver()            # enables the driver to move
        while True:
            self.pulse()                # sends out pulses until the button reads high
            if stop.value == True: #GPIO.input(self.button_pin) == GPIO.HIGH: # read a button
                #print("Bottom reached!")    
                break                        # break loop when bottom reached
        self.disable_driver()           # driver disabled

actuator = SetPoint()

while True:
    position = input("Enter a new position! ")
    try:
        position = int(position)
        actuator.move_to_position(position)
        time.sleep(1)
    except ValueError:
        print('Input not an integer!')
        break