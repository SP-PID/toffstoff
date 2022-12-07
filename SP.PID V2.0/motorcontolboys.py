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
        baudrate = 1000000,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

ser2 = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate = 1000000,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

class DC_control():
    def __init__(self) :
        self.ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)
    
    def set_SP(self,SP_val):
        SP_val = "p" + str(SP_val)
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
    
    def read(self):
        x = self.ser.readline()
        x = x.decode(encoding='UTF-8',errors='strict')

class Stepper_control():
    def __init__(self) :
        self.ser = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)
    def set_SP(self,SP_val):
        SP_val = "p" + str(SP_val)
        self.ser.write(str.encode(SP_val))
    def read(self):
        x = self.ser.readline()
        x = x.decode(encoding='UTF-8',errors='strict')
    def calibrate(self):
        self.ser.write(str.encode('calibrate'))




class Encoders():
    def __init__(self,address,zerostate=0):
            self.SKREF = 2500000
            self.qt_enc = seesaw.Seesaw(board.I2C(), addr=address)
            self.qt_enc.pin_mode(24, self.qt_enc.INPUT_PULLUP)
            self.button = digitalio.DigitalIO(self.qt_enc, 24)
            self.button_held = False
            self.encoder = rotaryio.IncrementalEncoder(self.qt_enc)
            self.last_position = 0
            self.pos = zerostate
            self.zerostate = zerostate
            self.encoder.position = self.zerostate
            print(self.encoder.position)


    def Get_enc_val(self):
        self.pos = -self.encoder.position
        
        if self.pos < 0 :
            self.encoder.position = 0
            self.pos = 0
        
        if not self.button.value and not self.button_held:
            self.encoder.position = -self.zerostate
            self.pos = self.zerostate
            self.last_position = self.zerostate
        
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
        if self.pos > self.SKREF and self.pos < (self.SKREF + 10):
            self.encoder.position = -(self.SKREF)
            self.pos = self.SKREF
            self.last_position = self.SKREF
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

# class DC_encoder_thread():

#     def __init__(self):
#         self._running = True

#     def terminate(self):
#         self._running = False

#     def run(self):
        
#         ser.write(b'0')
        
#         while True:
#             x = ser.readline();
#             x = x.decode(encoding='UTF-8',errors='strict')
#             try:
#                 gv.dc_enc_val = int(x)
#             except ValueError:
#                 pass
            
#             if e_stop_bot.value == True:
#                print("zeroed")
#                ser.write(0)
#             time.sleep(0.00000000001)






# class write_sp_thread():
#     def __init___(self):
#         self._running = True
    
#     def terminate(self):
#         self._running = False
    
#     def run(self):
#         sp = "sp" + str(gv.sp)
#         ser2.write(str.encode(sp))



# class write_PID_thread():
#     def __init___(self):
#         self._running = True
    
#     def terminate(self):
#         self._running = False
    
#     def run(self):
#         kp = "p" +str(gv.kp)
#         ki= "i" + str(gv.ki)
#         kd = "d" + str(gv.kd)
#         sp = str(gv.sp)
#         ser.write(str.encode(sp))
#         time.sleep(0.00001)
#         ser.write(str.encode(kp))
#         time.sleep(0.00001)
#         ser.write(str.encode(ki))
#         time.sleep(0.00001)
#         ser.write(str.encode(kd))
#         time.sleep(0.00001)
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

class get_values_thread():
    def __init__(self):
        self.running =True
    
    def terminate(self):
        self.running = False
    
    def run(self):
        kpold = kp.Get_enc_val()
        spold = sp.get_setpoint()
        kiold = ki.Get_enc_val()
        kdold = kd.Get_enc_val() 
        while True:
            gv.sptemp = sp.get_setpoint() * 10
            #print(gv.sptemp)
            kptemp = kp.Get_enc_val()
            kitemp = ki.Get_enc_val()
            kdtemp = kd.Get_enc_val()
            #print(gv.sptemp)
            if not sp.button.value and not sp.button_held:
                gv.sp = gv.sptemp
            if kpold != kptemp:
                gv.kp = kptemp
                kpold = kptemp
                pid_regulator.set_p(kptemp)
            if kiold != kitemp:
                gv.ki = kitemp
                kiold = kitemp
                pid_regulator.set_i(kitemp)
            if kdold != kdtemp:
                gv.kd = kdtemp
                kdold = kdtemp
                pid_regulator.set_d(kdtemp)

                
kp = Encoders(0x38,10)
ki = Encoders(0x37)
kd = Encoders(0x36)
sp = Encoders(0x3a)
gv = global_val()

encoders = Encoders()
get_values = get_values_thread()
get_values = Thread(target= get_values.run)
get_values.start()
