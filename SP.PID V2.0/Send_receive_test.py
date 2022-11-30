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
import serial
ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

ser2 = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)




class write_sp_thread():
    def __init___(self):
        self._running = True
    
    def terminate(self):
        self._running = False
    
    def run(self):
        while True:
            sp = str(gv.sp)
            ser2.write(str.encode(sp))


class global_val():
    def __init__(self):
            self.POS = 0
            self.dc_enc_val = 0
            self.exit = False
            self.sp = 0
            self.kp = 1.0
            self.ki = 0.0
            self.kd = 0.0
            self.sptemp = 0
            self.PWM_val = 0
            self.DC_ratio = 1        

class write_PID_thread():
    def __init___(self):
        self._running = True
    
    def terminate(self):
        self._running = False
    
    def run(self):
        while True:
            kp = "p" +str(gv.kp)
            ki= "i" + str(gv.ki)
            kd = "d" + str(gv.kd)
            sp = str(gv.sp)
            ser.write(str.encode(sp))
            time.sleep(0.00000000001)
            ser.write(str.encode(kp))
            time.sleep(0.00000000001)
            ser.write(str.encode(ki))
            time.sleep(0.00000000001)
            ser.write(str.encode(kd))
            time.sleep(0.00000000001)
class read_PID():
    def __init___(self):
        self._running = True
    
    def terminate(self):
        self._running = False
    
    def run(self):
        while True:
            x = ser.readline();
            x = x.decode(encoding='UTF-8',errors='strict')
            z = ser2.readline();
            z = z.decode(encoding='UTF-8',errors='strict')
            print("Ser1",x)
            print("Ser2",z)
            
            #if e_stop_bot.value == True:
            #    print("zeroed")
            #    ser.write(0)
            time.sleep(0.00000000001)


gv = global_val()
step = write_sp_thread()
step = Thread(target= step.run)
step.start()
re_pid = read_PID()
re_pid = Thread(target= re_pid.run)
re_pid.start()


dc = write_PID_thread()
dc = Thread(target= dc.run)
dc.start()
while True:
    gv.sp = 20
    gv.ki = 3
    gv.kd = 2
    gv.kp = 12
    
    
