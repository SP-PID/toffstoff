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
from time import sleep, perf_counter
from threading import Thread

class DC_encoders():
    def __init__(self) -> None:
        self.encA = dg.DigitalInOut(board.D14)
        self.encA.direction = dg.Direction.INPUT
        self.encA.pull = dg.Pull.DOWN
        self.encB = dg.DigitalInOut(board.D16)
        self.encB.direction = dg.Direction.INPUT
        self.encB.pull = dg.Pull.DOWN
        self.direction = ''
        self.i = 0
        self.iold = 0
        self.last_enc = True

    def read(self):
        if self.encA.value == True and self.last_enc == False:
            if self.encB.value == True:
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
        return self.i

encoder = DC_encoders()
e_stop_top = dg.DigitalInOut(board.D8)
e_stop_top.direction = dg.Direction.INPUT
e_stop_top.pull = dg.Pull.UP
e_stop_bot = dg.DigitalInOut(board.D7)
e_stop_bot.direction = dg.Direction.INPUT
e_stop_bot.pull = dg.Pull.UP


while True:
    value = encoder.get_pos()
    if e_stop_bot.value is True:
        print("bottom")
    if e_stop_top.value is True:
        print("top")
    print(value)