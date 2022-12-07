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

class Stepper_control():
    def __init__(self) :
        self.ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)
    def set_SP(self,SP_val):
        SP_val = str(SP_val)
        self.ser.write(str.encode(SP_val))
    def read(self):
        x = self.ser.readline()
        x = x.decode(encoding='utf-8',errors='strict')
        time.sleep(0.01)
        return x
    def calibrate(self):
        self.ser.write(str.encode('cal'))
    def run(self):
        self.ser.write(str.encode('run'))
    def stop(self):
        self.ser.write(str.encode('notrun')) 

stepper = Stepper_control()

while True:
    lesning = input("command: ")
    if lesning == 'calb':
        stepper.calibrate()
    elif lesning == 'notrun':
        stepper.stop()
    elif lesning == 'run':
        stepper.run()
    else:
        stepper.set_SP(lesning)

