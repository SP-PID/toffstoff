from tkinter import *
import tkinter as tk
from unittest import TextTestRunner
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
import digitalio as dg
import pwmio
from threading import Thread 


class encoders():
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
        
        if not self.button.value and not self.button_held:
            self.encoder.position = 0
            self.pos = 0
            self.last_position = 0
        if self.pos != self.last_position:
            if abs(abs(self.pos)-abs(self.last_position)) < 100:
                self.position = self.pos
                self.last_position = self.position
                return self.position
            else:
                return self.last_position
        else:
            return self.last_position

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
                self.last_position4 = self.position
                return self.position
            else:
                return self.last_position
        else:
            return self.last_position

class PID:
    def __init__(self):
        self.kp = 1
        self.ki = 0
        self.kd = 0
        self.time = 0
        self.old_time = 0
        self.eprew = 0
        self.eintegral = 0

    def regulate(self,target,pos):
        self.time = time.time()
        time_delta = self.time - self.old_time
        self.old_time = self.time
        
        e = pos - target

        dedt = (e - self.eprew)/(time_delta)

        self.eintegral = self.eintegral + (e * time_delta)
        
        u = self.kp*e + self.ki*self.eintegral + self.kd*dedt
        self.eprew = e
        #print((e,self.eintegral,dedt,u,))
        if u > 255:
            u = 255
        if u < -255:
            u = -255
        return u

    def set_p(self,value):
        self.kp = value

    def set_i(self,value):
        self.ki = value

    def set_d(self,value):
        self.kd= value

class DC_encoders():
    def __init__(self) -> None:
        self.encA = dg.DigitalInOut(board.D16)
        self.encA.direction = dg.Direction.INPUT
        self.encA.pull = dg.Pull.DOWN
        self.encB = dg.DigitalInOut(board.D14)
        self.encB.direction = dg.Direction.INPUT
        self.encB.pull = dg.Pull.DOWN
        self.direction = ''
        self.i = 0
        self.iold = 0
        self.last_enc = True


    def read(self):
        if self.encA.value == True and self.last_enc == False:
            print('encA active')
            if self.encB.value == True:
                print('encB active')
                self.direction = 'Forward'
            else:
                self.direction = 'Backwards'
    
            if self.direction == 'Forward':
                self.i += 1
            else:
                self.i -= 1
            self.last_enc = True
            return

        elif self.encA.value == False and self.last_enc == True:
            self.last_enc = False
            return

        if self.i != self.iold:
            self.iold = self.i
        return

    def get_pos(self):
        self.read()
        print(self.i)
        return self.i

class encoder_t():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        dc_enc = DC_encoders()
        while True:
            gv.enc_val = dc_enc.get_pos()

class global_val():
    def __init__(self):
        self.enc_val = 0

print("start")

motor_Ain1 = pwmio.PWMOut(board.D19,frequency = 1000)
print("Ain1 komid")
motor_Ain2 = pwmio.PWMOut(board.D13,frequency = 1000)
print("Ain2 komid")
encoder4 = encoders(0x3a)
print("Encoder komid")
dc_enc = DC_encoders()
print("DC encoder komid")
pid = PID()
print("PID komid")
gv = global_val()

encoder_thread = encoder_t()   #Býr til Class
encoder_thread = Thread(target=encoder_thread.run)    #Býr til þráð  
encoder_thread.start()  #Kveikir á þráð

while True:
    set_point = encoder4.Get_enc_val()
    PWM_val = set_point #pid.regulate(set_point, gv.enc_val)
    #print(set_point, gv.enc_val,PWM_val)

    if PWM_val > 65000:
        PWM_val = 65000

    if PWM_val < -65000:
        PWM_val = -65000

    if PWM_val < 0:
        motor_Ain1.duty_cycle = abs(PWM_val)
        motor_Ain2.duty_cycle = 0
    elif PWM_val > 0:
        motor_Ain1.duty_cycle = 0
        motor_Ain2.duty_cycle = abs(PWM_val)
    else:
        motor_Ain1.duty_cycle = 0
        motor_Ain2.duty_cycle = 0
    #time.sleep(0.01)
