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
e_stop_top = dg.DigitalInOut(board.D7)
e_stop_top.direction = dg.Direction.INPUT
e_stop_top.pull = dg.Pull.UP
e_stop_bot = dg.DigitalInOut(board.D8)
e_stop_bot.direction = dg.Direction.INPUT
e_stop_bot.pull = dg.Pull.UP
motor_Ain1 = pwmio.PWMOut(board.D13,frequency = 1000)
motor_Ain2 = pwmio.PWMOut(board.D19,frequency = 1000)


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
class Live():
    def __init__(self):
        self.good = True

    def switch(self):
        if self.good:
            self.good = False
            #print(self.good)
        else:
            self.good = True
            #print(self.good)
 
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
        self.highest_position = self.steps_total                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position
        self.disable_microstepping()
        self.microstepping = False
        self.reset_actuator()                                                           # actuator finds zero position (bottom)

    def get_total_steps(self):
        ''' Returns total number of steps for end to end travel '''
        return self.steps_total

    def enable_driver(self):        
        ''' Function that enables Easydriver for use '''
        enable.value = False

    def disable_driver(self):        
        ''' Function that disables Easydriver after use '''
        enable.value = True 

    def update_rotation(self,direction):
        ''' Function updates variable for gantry travel direction '''
        self.direction = direction
        if self.direction == "up":
            self.rotation = True            # False means actuator moves down
        if self.direction == "down":
            self.rotation = False
        direc.value = self.rotation

    def pulse(self):
        ''' Function sends out one pulse on pulse pin '''
        pulse.value = True
        time.sleep(0.0007)      # wait
        pulse.value = False
        time.sleep(0.0007)      # wait

    def update_position(self,distance):
        ''' Function keeps track of current position of gantry '''
        if self.direction == "down":
            if self.microstepping:
                self.current_position -= distance/8
            else:
                self.current_position -= distance
        if self.direction == "up":
            if self.microstepping:
                self.current_position += distance/8
            else:
                self.current_position += distance

    def move(self,position):
        ''' Function moves gantry to a requested position '''
        steps = self.current_position - position
        if self.current_position == position:
            return         
        if self.current_position > position:
            self.update_rotation("down")
        if self.current_position < position:
            self.update_rotation("up")
            steps = -steps
        self.spin_motor(steps)
        #print("Current position " + str(self.current_position))

        

    def spin_motor_helper(self,steps):
        ''' Function that moves the stepper motor '''
        self.enable_driver()
        for _ in range(0, steps):
            self.pulse()                    # one high and one low on pin
            self.update_position(1)
            if self.current_position >= self.highest_position:  # stops before top end of profile
                break
            if self.current_position <= self.lowest_position:   # stops before bottom end of profile
                break                 
        self.disable_driver()

    def spin_motor(self,steps):
        if steps <= 10:
            #print("Microstepping")
            self.enable_microstepping()
            self.spin_motor_helper(steps*8)
            self.disable_microstepping()
        else:
            self.spin_motor_helper(steps)
        self.current_position = int(round(self.current_position,0))

    def enable_microstepping(self):
        #print("Microstepping enabled!")
        self.microstepping = True
        ms1.value = True
        ms2.value = True

    def disable_microstepping(self):
        #print("Microstepping disabled!")
        self.microstepping = False
        ms1.value = False
        ms2.value = False       

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

class stepper_thread():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        ratio = 2660 / 775
        sp = gv.sp
        interval = 0.1
        old_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - old_time >= interval:
                sp = gv.sp
                old_time = cur_time
            if sp != actuator.current_position:
                actuator.move(int(round(sp * ratio)))
            time.sleep(0.00001)

class PID:
    def __init__(self):
        self.kp = 1.0
        self.ki = 0.0
        self.kd = 0.0
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
        
        if self.kp > 0:
            kp_val = self.kp*e
        
        else:
            kp_val = 0

        if self.ki > 0:
            ki_val = self.ki*self.eintegral

        else:
            ki_val = 0
        
        if self.kd > 0:
            kd_val = self.kd*dedt
        
        else:
            kd_val = 0
        
        u = kp_val + ki_val + kd_val
        self.eprew = e
        #print((e,self.eintegral,dedt,u,))
        #if u > 255:
        #    u = 255
        #if u < -255:
        #    u = -255
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

class DC_thread():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        time.sleep(3)
        if e_stop_top.value == False:
            motor_Ain1.duty_cycle = 15000
            motor_Ain2.duty_cycle = 0
            while not e_stop_top.value:
                time.sleep(0.00001)
            ser.write(b'0')
        else:
            ser.write(b'0')
        motor_Ain1.duty_cycle = 0
        motor_Ain2.duty_cycle = 0
        ser.write(b'0')
        time.sleep(1)
        ser.write(b'0')
        motor_Ain1.duty_cycle = 0
        motor_Ain2.duty_cycle = 15000
        while e_stop_bot.value == False:
            time.sleep(0.0001)
         
        motor_Ain1.duty_cycle = 0
        motor_Ain2.duty_cycle = 0            
        time.sleep(1)
        disttravel = abs(gv.dc_enc_val)
        ser.write(b'0') 
        gv.DC_ratio = disttravel / 775
        print(gv.dc_enc_val)
        ser.write(b'0')
        gv.dc_enc_val = 0
        time.sleep(1)
        print("Distravel:", disttravel)
        print("Encoder val:", gv.dc_enc_val)
        print("Distravel:", gv.DC_ratio)
        #print("Distravel:" + gv.disttravel)
        ser.write(b'0')
        while True:
            PWM_val = pid_regulator.regulate(gv.sp * gv.DC_ratio , gv.dc_enc_val) * 100
            gv.PWM_val = PWM_val 
            
            #print(gv.sp, gv.dc_enc_val,PWM_val)
            
            if PWM_val > 65000:
                PWM_val = 65000

            if PWM_val < -65000:
                PWM_val = -65000
            print(PWM_val)
            if PWM_val > 0 and e_stop_bot.value == False:
                motor_Ain1.duty_cycle = 0
                motor_Ain2.duty_cycle = abs(PWM_val)
                print('1')
            elif PWM_val < 0 and e_stop_top.value == False:
                print('2')
                motor_Ain1.duty_cycle = abs(PWM_val)
                motor_Ain2.duty_cycle = 0
            else:
                motor_Ain1.duty_cycle = 0
                motor_Ain2.duty_cycle = 0
            time.sleep(0.000000001)
            
class DC_encoder_thread():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        
        ser.write(b'0')
        
        while True:
            x = ser.readline();
            x = x.decode(encoding='UTF-8',errors='strict')
            try:
                gv.dc_enc_val = int(x)
            except ValueError:
                pass
            
            #if e_stop_bot.value == True:
            #    print("zeroed")
            #    ser.write(0)
            time.sleep(0.00000000001)


#dc_encoders = DC_encoders()
pid_regulator = PID()
live = Live()
actuator = SetPoint()
kp = Encoders(0x38,10)
ki = Encoders(0x37)
kd = Encoders(0x36)
sp = Encoders(0x3a)
gv = global_val()

get_values = get_values_thread()
get_values = Thread(target= get_values.run)
get_values.start()

stepper = stepper_thread()
stepper = Thread(target= stepper.run)
stepper.start()

DC_motor = DC_thread()
DC_motor = Thread(target= DC_motor.run)
DC_motor.start()

DC_encoder_read = DC_encoder_thread()
DC_encoder_read = Thread(target= DC_encoder_read.run)
DC_encoder_read.start()

def on_escape(event=None):
    gv.exit = True
    win.destroy()
    sys.exit()

# update PID values from encoders
def update():
    label1['text'] = "K_p = " + str(gv.kp)
    label2['text'] = "K_i = " + str(gv.ki)
    label3['text'] = "K_d = " + str(gv.kd)
    takki1['text'] = "SP = " + str(gv.sptemp)
    if live.good is True:
        takki1['bg'] = "green"
        takki1['activebackground'] = "green"
        takki1['fg'] = "white"
        takki1['activeforeground'] = "white"
    else:
        takki1['bg'] = "red"
        takki1['activebackground'] = "red"
        takki1['fg'] = "black"
        takki1['activeforeground'] = "black"
    frame3.after(50, update) # run itself again after 200 ms

# creates lists of lists for the big plot
def init():
    for line in lines:
        line.set_data(xs,[])
    return lines

# function for live animation on the BIG graph
def Big_Plot(i, y1, y2):

    y = gv.sp
    y1.append(y)
    y1 = y1[-x_len:]

    y = gv.dc_enc_val / gv.DC_ratio
    y2.append(y)
    y2 = y2[-x_len:]

    ylist = [y1, y2]

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_ydata(ylist[lnum]) # set data for each line separately. 
    return lines

# function for live animation on small graph no 1
def small_plot1(i, ys):

    # Read temperature (Celsius) from TMP102
    K_p = gv.PWM_val     

    # Add y to list
    ys.append(K_p)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line2.set_ydata(ys)

    return line2,

# function for live animation on small graph no 2
def small_plot2(i, ys):

    # Read temperature (Celsius) from TMP102
    K_i = round(gv.ki)     


    # Add y to list
    ys.append(K_i)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line3.set_ydata(ys)

    return line3,

# function for live animation on small graph no 3
def small_plot3(i, ys):

    # get data for D
    K_d = round(gv.ki)     

    # Add y to list
    ys.append(K_d)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    # Update line with new Y values
    line4.set_ydata(ys)
    return line4,

# Constants to construct plots
x_len = 500
y_range = [0,1000]
x_range = [0,x_len]
INTERVALS = 0

# Create an instance of tkinter frame

win= Tk()

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# --- fullscreen & configurations ---

# run fullscreen
win.attributes("-fullscreen", True)
# keep on top
win.wm_attributes("-topmost", True)
# close window with key `ESC`
win.bind("<Escape>", on_escape)
# hide cursor
win.config(cursor = "none")
# Set the window size
win.geometry("1024x600")
# Use TkAgg
matplotlib.use("TkAgg")

######################################

# Create a figure of specific size
figure = plt.figure(figsize=(11, 6), dpi=93)
gs = GridSpec(nrows=3, ncols=4)

################ BIG PLOT ################

ax1 = figure.add_subplot(gs[:,0:3],)
xs = list(range(0,x_len))
ys = [0]* x_len
ax1.set_ylim(y_range)
ax1.set_xlim(x_range)
ax1.set_title("SP.PID")
line, = ax1.plot([], [])
plotlays, plotcols = [2], ["black","red"]
lines = []

for index in range(2):
    lobj = ax1.plot([],[],lw=2,color=plotcols[index])[0]
    lines.append(lobj)

y1 = [0] * x_len
y2 = [0] * x_len

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(figure, Big_Plot, fargs= (y1,y2), init_func=init,
                                interval=INTERVALS, blit=True)


################ SMALL PLOT 1 ################

plot2 = figure.add_subplot(gs[0,3])
xs = list(range(0,x_len))
ys = [0]* x_len
plot2.set_ylim([-65535,65535])
plot2.set_xlim([0,x_len])
plot2.set_title('PWM', rotation='vertical',x=1.1,y=0.3)
line2, = plot2.plot(xs,ys, color= "red")

ani2 = animation.FuncAnimation(figure,
    small_plot1,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)

################ SMALL PLOT 2 ################

plot3 = figure.add_subplot(gs[1,3])
xs = list(range(0,x_len))
ys = [0]* x_len
plot3.set_ylim(y_range)
plot3.set_xlim(x_range)
plot3.set_title('PWM', rotation='vertical',x=1.1,y=0.3)
line3, = plot3.plot(xs,ys, color= "red")

ani3 = animation.FuncAnimation(figure,
    small_plot2,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)

################ SMALL PLOT 3 ################

plot4 = figure.add_subplot(gs[2,3])
xs = list(range(0,x_len))
ys = [0]* x_len
plot4.set_ylim(y_range)
plot4.set_xlim(x_range)
plot4.set_title('K_d', rotation='vertical',x=1.1,y=0.3)
line4, = plot4.plot(xs,ys, color= "red")

ani4 = animation.FuncAnimation(figure,
    small_plot3,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)

###############################################################################

# Add a canvas widget to associate the figure with canvas
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().grid(row=0, column=0, rowspan=1, columnspan=5)

frame = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=0)
frame.grid(row =3, column =1, padx=5,pady=5)
label1 = tk.Label(master=frame) 
label1.pack(padx=5, pady=5)

frame2 = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=0)
frame2.grid(row =3, column =2, padx=5,pady=5)
label2 = tk.Label(master=frame2)
label2.pack(padx=3, pady=5)

frame3 = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=0)
frame3.grid(row =3, column =3, padx=10,pady=10)
label3 = tk.Label(master=frame3)
label3.pack(padx=3, pady=5)

takki1 = tk.Button(master= win, command= live.switch)
takki1.grid(row =3, column =0)

takki2 = tk.Button(master= win,activebackground= None, text= "Exit", command= on_escape)
takki2.grid(row =3, column =4)

# run first time
update()

#
win.mainloop()
