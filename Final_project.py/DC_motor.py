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
import threading

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
                self.last_position4 = self.position
                return self.position
            else:
                return self.last_position
        else:
            return self.last_position

motor_Ain1 = pwmio.PWMOut(board.D19,frequency = 50)
motor_Ain2 = pwmio.PWMOut(board.D13,frequency = 50)

encoder4 = encoders(0x3a)

while True:
    PWM_val = encoder4.Get_enc_val()
    print(PWM_val*100)
    if PWM_val < 0:
        motor_Ain1.duty_cycle = abs(PWM_val) *100
        motor_Ain2.duty_cycle = 0
    elif PWM_val > 0:
        motor_Ain1.duty_cycle = 0
        motor_Ain2.duty_cycle = abs(PWM_val) *100
    else:
        motor_Ain1.duty_cycle = 0
        motor_Ain2.duty_cycle = 0