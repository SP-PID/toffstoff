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
import time
from threading import Thread
from PIL import ImageTk, Image
import csv
import shutil 
from datetime import datetime
from itertools import zip_longest
import os
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
import digitalio as dg
import pwmio
import serial

class DC_control():
    def __init__(self) :
        self.ser = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)
    def set_SP(self,SP_val):
        SP_val = str(SP_val)
        self.ser.write(str.encode(SP_val))
    def set_P(self,P_val):
        P_val = "p" + str(P_val)
        self.ser.write(str.encode(P_val))
    def set_I(self,I_val):
        I_val = "i" + str(I_val)
        self.ser.write(str.encode(I_val))
    def set_D(self,D_val):
        D_val = "d" + str(D_val)
        self.ser.write(str.encode(D_val))
    def run(self):
        self.ser.write(str.encode('run'))
    def stop(self):
        self.ser.write(str.encode('stop'))
    def calibrate(self):
        self.ser.write(str.encode('calibrate'))
    def reset(self):
        self.ser.write(str.encode('reset'))
    def id(self):
        self.ser.write(str.encode('identify'))
    def read(self):
        x = self.ser.readline()
        x = x.decode(encoding='UTF-8',errors='strict')
        return x
    def dc_data(self):
        try:
            x = self.read()
            x = x.split(" ")
            Dc = x[1]
            timi = x[0]
            print(x)
            return timi, Dc
        except:
            pass

dc = DC_control()

while True:
    lesning = input("command: ")
    if lesning == 'run':
        dc.run()
    elif lesning == 'stop':
        dc.stop()
    elif lesning == 'calibrate':
        dc.calibrate()
    elif lesning == 'reset':
        dc.reset()
    elif lesning == 'id':
        dc.id()
    else:
        dc.set_SP(lesning)
    print(dc.read())