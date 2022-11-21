from tkinter import *
import tkinter as tk
from unittest import TextTestRunner
import random
import sys
import board
import adafruit_seesaw
from adafruit_seesaw import seesaw, rotaryio, digitalio
import time
import digitalio as dg
import pwmio
from time import sleep, perf_counter
from threading import Thread

pulse = dg.DigitalInOut(board.D17)
pulse.direction = dg.Direction.OUTPUT
direc = dg.DigitalInOut(board.D15)
direc.direction = dg.Direction.OUTPUT
enable = dg.DigitalInOut(board.D18)
enable.direction = dg.Direction.OUTPUT
ms1 = dg.DigitalInOut(board.D20)
ms1.direction = dg.Direction.OUTPUT
ms2 = dg.DigitalInOut(board.D21)
ms2.direction = dg.Direction.OUTPUT
ms1.value = False
ms2.value = False
stop = dg.DigitalInOut(board.D9)
stop.direction = dg.Direction.INPUT
stop.pull = dg.Pull.UP

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
        #self.reset_actuator()                                                           # actuator finds zero position (bottom)

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

    def reset_actuator(self):
        ''' Function that moves the gantry to zero position (bottom) '''
        self.rotation = False    
        while True:
            self.pulse()                
            if stop.value == True:   
                break                        

class Encoder():
    def __init__(self,address):
            self.qt_enc = seesaw.Seesaw(board.I2C(), addr=address)
            self.qt_enc.pin_mode(24, self.qt_enc.INPUT_PULLUP)
            self.button = digitalio.DigitalIO(self.qt_enc, 24)
            self.button_held = False
            self.encoder = rotaryio.IncrementalEncoder(self.qt_enc)
            self.last_position = 0
            self.pos = 0

    def Get_enc_val(self):
        self.pos = -self.encoder.position
        if self.pos < 0 :
            self.encoder.position = 0
            self.pos = 0
        if not self.button.value and not self.button_held:
            self.encoder.position = 0
            self.pos = 0
            self.last_position = 0
        if self.pos != self.last_position:
            if abs(abs(self.pos)-abs(self.last_position)) < 100:
                self.position = self.pos
                self.last_position = self.position
                return self.position/10
            else:
                return self.last_position/10
        else:
            return self.last_position/10

    def get_setpoint(self):
        self.pos = -self.encoder.position
        if self.pos > SKREF and self.pos < (SKREF + 10):
            self.encoder.position = -(SKREF)
            self.pos = SKREF
            self.last_position = SKREF
        if self.pos < 0:
            self.encoder.position = 0
            self.pos =0
        if self.pos != self.last_position:
            if abs(abs(self.pos)-abs(self.last_position)) < 100:
                self.position = self.pos
                self.last_position = self.position
                return self.position
            else:
                return self.last_position
        else:
            return self.last_position



encoder = Encoder(0x36)
actuator = SetPoint()

POS = 0
def task1():
    global POS
    while True:
        actuator.move(POS)

def task2():
    global POS
    while True:
        POS = int(encoder.Get_enc_val()*100)
        print(POS)
        time.sleep(0.2)


# create two new threads
t1 = Thread(target=task1)
t2 = Thread(target=task2)

# start the threads
t1.start()
t2.start()

# wait for the threads to complete
t1.join()
t2.join()

