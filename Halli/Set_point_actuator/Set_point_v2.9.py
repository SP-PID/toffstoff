
#import board
#import adafruit_seesaw
#from adafruit_seesaw import seesaw, rotaryio, digitalio
import time
import board
import digitalio as dg
import threading
from time import sleep, perf_counter
from threading import Thread

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
        self.rotation = False                                                           # variable for which direction the motor will spin
        self.direction = "up"                                                           # variable to tell program to go up or down
        self.current_position = 0                                                       # initializes in lowest position
        self.distance = 0
        self.step_size = "FULL"
        self.highest_position = 2657                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position
        self.multiplier = 1
        self.enable_driver()
        self.top_reached = False
        self.reset_actuator()                                                           # actuator finds zero position (bottom)

    def get_current_position(self):
        return self.current_position

    def enable_driver(self):        
        ''' Function that enables Easydriver for use '''
        enable.value = False

    def pulse(self):
        ''' Function sends out one pulse on pulse pin '''
        pulse.value = True
        time.sleep(0.0007)      # wait
        pulse.value = False
        time.sleep(0.0007)      # wait

    def update_position(self,distance):
        ''' Function keeps track of current position of gantry '''
        if self.direction == "down":
            self.current_position -= distance
        if self.direction == "up":
            self.current_position += distance             
    
    def update_stepping(self):
        if abs(self.distance) >= 30:
            ms1.value = False
            ms2.value = False         
            self.multiplier = 1
        if 30 > abs(self.distance) >= 20:
            ms1.value = True
            ms2.value = False         
            self.multiplier = 2
        if 20 > abs(self.distance) > 10:
            ms1.value = False
            ms2.value = True         
            self.multiplier = 4
        if abs(self.distance) <= 10:
            ms1.value = True
            ms2.value = True
            self.multiplier = 8 

    def update_direction(self,requested_position):
        self.distance = requested_position - self.current_position
        if self.distance < 0:
            self.direction = "down"
            self.rotation = False
        else:
            self.direction = "up"
            self.rotation = True
        direc.value = self.rotation

    def move(self,position):
        if position > self.highest_position:
            position = self.highest_position
        self.update_direction(position)                  
        self.update_stepping()
        if abs(self.distance) < 1:
            pass
        else:
            if self.current_position <= self.highest_position:
                for i in range(0,self.multiplier):
                    self.pulse()
                self.update_position(1)
        if position == self.current_position:
            return True
        return False

    def reset_actuator(self):
        ''' Function that moves the gantry to zero position (bottom) '''
        self.rotation = False    
        while True:
            self.pulse()                
            if stop.value == True:   
                break                        

    def go_to(self,POS):
        while True:
            in_position = actuator.move(POS)
            if in_position:
                break



actuator = SetPoint()



