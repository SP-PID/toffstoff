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
pulse = dg.DigitalInOut(board.D23)
pulse.direction = dg.Direction.OUTPUT
direc = dg.DigitalInOut(board.D24)
direc.direction = dg.Direction.OUTPUT
enable = dg.DigitalInOut(board.D18)
enable.direction = dg.Direction.OUTPUT
ms1 = dg.DigitalInOut(board.D20)
ms1.direction = dg.Direction.OUTPUT
ms2 = dg.DigitalInOut(board.D21)
ms2.direction = dg.Direction.OUTPUT
ms1.value = False
ms2.value = False
stop = dg.DigitalInOut(board.D15)
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
        self.distance = 0
        self.stepp_size = "FULL"
        self.highest_position = self.steps_total                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position
        self.multiplier = 1
        self.reset_actuator()                                                           # actuator finds zero position (bottom)

    def get_current_position(self):
        return self.current_position

    def enable_driver(self):        
        ''' Function that enables Easydriver for use '''
        enable.value = False

    def disable_driver(self):        
        ''' Function that disables Easydriver after use '''
        enable.value = True 

    def pulse(self):
        ''' Function sends out one pulse on pulse pin '''
        pulse.value = True
        time.sleep(0.0007)      # wait
        pulse.value = False
        time.sleep(0.0007)      # wait

    def update_position(self,distance):
        ''' Function keeps track of current position of gantry '''
        if self.direction == "down":
            self.current_position -= distance*self.multiplier
        if self.direction == "up":
            self.current_position += distance*self.multiplier

    def update_stepping(self):
        if self.step_size == "FULL":
            ms1.value = False
            ms2.value = False         
            self.multiplier = 1
        if self.step_size == "HALF":   
            ms1.value = True
            ms2.value = False
            self.multiplier = 0.5
        if self.step_size == "QUARTER":
            ms1.value = False
            ms2.value = True
            self.multiplier = 0.25           
        if self.step_size == "EIGHT":
            ms1.value = True
            ms2.value = True
            self.multiplier = 0.125              
    
    def determine_direction(self,requested_position):
        self.distance = self.current_position - requested_position # If current position is above requested value then positive else negative
        if self.distance < 0:
            self.direction = "down"
        else:
            self.direction = "up"

    def determine_stepping(self,distance):
        if distance > 10:
            self.stepp_size = "FULL"
        else:
            self.stepp_size = "EIGHT"

    def update_rotation(self):
        ''' Function updates variable for gantry travel direction '''
        if self.direction == "up":
            self.rotation = True            # False means actuator moves down
        if self.direction == "down":
            self.rotation = False
        direc.value = self.rotation

    def move(self,position):
        self.determine_direction(position)      # determines the direction to travel
        self.update_rotation()                  # updates variable
        self.determine_stepping()               # determines step size
        self.update_stepping
        self.pulse()

    # if current position is the same as requested position then do nothing
    # if current position is less than requested value then up one slow
        # if current position is alot less then requested value then up one
    # if current position is more than requested value then down one slow
        # if current position is alot more than requested value then down one

    def update_rotation(self,direction):
        ''' Function updates variable for gantry travel direction '''
        self.direction = direction
        if self.direction == "up":
            self.rotation = True            # False means actuator moves down
        if self.direction == "down":
            self.rotation = False
        direc.value = self.rotation

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

my_Arr = list(range(1, 250))
#my_Arr = list(range(250, 1))

for i in range(0,len(my_Arr)):
    actuator.move(my_Arr[i])

#for j in range(0,len(my_Arr)):
#    actuator.move(my_Arr[j])
      

