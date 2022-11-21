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
from time import sleep, perf_counter
from threading import Thread

SKREF = 100
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
        self.distance = 0
        self.step_size = "FULL"
        self.highest_position = int(round(self.steps_total,0))                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position
        self.multiplier = 1
        self.top_reached = False
        self.idle_time = time.time()
        self.driver_enabled = False
        self.idle = False
        self.reset_actuator()                                                           # actuator finds zero position (bottom)

    def get_current_position(self):
        return self.current_position

    def enable_driver(self):        
        ''' Function that enables Easydriver for use '''
        #print("Driver enabled")
        self.driver_enabled = True
        enable.value = False

    def disable_driver(self):        
        ''' Function that disables Easydriver after use '''
        #print("Driver disabled")
        self.driver_enabled = False
        enable.value = True 

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
        if self.step_size == "FULL":
            ms1.value = False
            ms2.value = False         
            self.multiplier = 1
        if self.step_size == "HALF":
            ms1.value = True
            ms2.value = False
            self.multiplier = 2
        if self.step_size == "QUARTER":
            ms1.value = False
            ms2.value = True
            self.multiplier = 4           
        if self.step_size == "EIGHT":
            ms1.value = True
            ms2.value = True
            self.multiplier = 8              
    
    def determine_direction(self,requested_position):
        self.distance = requested_position - self.current_position# - requested_position # If current position is above requested value then positive else negative
        if self.distance < 0:
            self.direction = "down"
        else:
            self.direction = "up"

    def determine_stepping(self):
        if abs(self.distance) > 10:
            self.step_size = "FULL"
        if abs(self.distance) <= 10:
            self.step_size = "HALF"
        if abs(self.distance) == 2:
            self.step_size = "EIGHT"

    def update_rotation(self):
        ''' Function updates variable for gantry travel direction '''
        if self.direction == "up":
            self.rotation = True            # False means actuator moves down
        if self.direction == "down":
            self.rotation = False
        direc.value = self.rotation

    def move(self,position):
        if position > self.highest_position:
            position = self.highest_position
        self.determine_direction(position)      # determines the direction to travel
        self.update_rotation()                  # updates variable
        self.determine_stepping()               # determines step size
        self.update_stepping()
        if abs(self.distance) < 1:
            self.check_idle()
            if self.idle == True:
                if self.driver_enabled:
                    self.disable_driver()
        else:
            if not self.driver_enabled:
                self.enable_driver()
            if self.current_position <= self.highest_position:
                for i in range(0,self.multiplier):
                    self.pulse()
                self.idle_time = time.time()
                self.update_position(1)
                
    def check_idle(self):
        current_pause = int(round(time.time() - self.idle_time,0))
        if current_pause < 5:
            self.idle = False
        else:
            self.idle = True


    def reset_actuator(self):
        ''' Function that moves the gantry to zero position (bottom) '''
        self.rotation = False   # sets travel direction to down
        self.enable_driver()            # enables the driver to move
        while True:
            self.pulse()                # sends out pulses until the button reads high
            if stop.value == True: #GPIO.input(self.button_pin) == GPIO.HIGH: # read a button   
                break                        # break loop when bottom reached
        self.disable_driver()           # driver disabled

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

class Live():
    def __init__(self):
        self.good = True

    def switch(self):
        if self.good:
            self.good = False
            print(self.good)
        else:
            self.good = True
            print(self.good)

class Good_GUI():
    def __init__(self):
        #constant that will be used
        self.x_len = 300
        self.y_range = [0,300]
        self.x_range = [0,self.x_len]
        self.INTERVALS = 0
        self.label1 = 0
        self.label2 = 0
        self.label3 = 0
        self.K_p = None
        self.K_i = None
        self.K_d = None
        self.SetPoint = None
        # Create an instance of tkinter frame
    #def run(self):
        self.win = Tk()
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
        # --- fullscreen & configurations ---
        # run fullscreen
        self.win.attributes("-fullscreen", True)
        # keep on top
        self.win.wm_attributes("-topmost", True)
        # close window with key `ESC`
        self.win.bind("<Escape>", self.on_escape)
        # hide cursor
        #win.config(cursor = "none")
        # Set the window size
        self.win.geometry("1024x600")
        # Use TkAgg
        matplotlib.use("TkAgg")
        ######################################

        # Create a figure of specific size
        self.figure = plt.figure(figsize=(11, 6), dpi=93)
        self.gs = GridSpec(nrows=3, ncols=4)
        ################ BIG PLOT ################
        self.ax1 = self.figure.add_subplot(self.gs[:,0:3],)
        self.xs = list(range(0,self.x_len))
        self.ys = [0]* self.x_len
        self.ax1.set_ylim(self.y_range)
        self.ax1.set_xlim(self.x_range)
        self.ax1.set_title("PID")
        self.line, = self.ax1.plot([], [])
        self.plotlays, self.plotcols = [2], ["black","red"]
        self.lines = []
        for index in range(2):
            lobj = self.ax1.plot([],[],lw=2,color=self.plotcols[index])[0]
            self.lines.append(lobj)

        self. y1 = [0] * self.x_len
        self.y2 = [0] * self.x_len

        # call the animator.  blit=True means only re-draw the parts that have changed.
        self.anim = animation.FuncAnimation(self.figure, self.Big_Plot, fargs= (self.y1,self.y2), init_func=self.init,
                                        interval=self.INTERVALS, blit=True)

        ################ SMALL PLOT 1 ################

        self.plot2 = self.figure.add_subplot(self.gs[0,3])
        self.xs = list(range(0,self.x_len))
        self.ys = [0]* self.x_len
        self.plot2.set_ylim(self.y_range)
        self.plot2.set_xlim(self.x_range)
        self.plot2.set_title('K_p', rotation='vertical',x=1.1,y=0.3)
        self.line2, = self.plot2.plot(self.xs,self.ys, color= "green")

        self.ani2 = animation.FuncAnimation(self.figure,
            self.small_plot1,
            fargs=(self.ys,),
            interval=self.INTERVALS,
            blit=True)
        ################ SMALL PLOT 2 ################

        self.plot3 = self.figure.add_subplot(self.gs[1,3])
        self.xs = list(range(0,self.x_len))
        self.ys = [0]* self.x_len
        self.plot3.set_ylim(self.y_range)
        self.plot3.set_title('K_i', rotation='vertical',x=1.1,y=0.3)
        self.line3, = self.plot3.plot(self.xs,self.ys)

        self.ani3 = animation.FuncAnimation(self.figure,
            self.small_plot2,
            fargs=(self.ys,),
            interval=self.INTERVALS,
            blit=True)

        ################ SMALL PLOT 3 ################

        self.plot4 = self.figure.add_subplot(self.gs[2,3])
        self.xs = list(range(0,self.x_len))
        self.ys = [0]* self.x_len
        self.plot4.set_ylim(self.y_range)
        self.plot4.set_title('K_d', rotation='vertical',x=1.1,y=0.3)
        self.line4, = self.plot4.plot(self.xs,self.ys)

        self.ani4 = animation.FuncAnimation(self.figure,
            self.small_plot3,
            fargs=(self.ys,),
            interval=self.INTERVALS,
            blit=True)

        ###############################################################################

        # Add a canvas widget to associate the figure with canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self.win)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=1, columnspan=5)

        self.frame = tk.Frame(master= self.win, bg = "red" ,relief=tk.RAISED,borderwidth=0)
        self.frame.grid(row =3, column =1, padx=5,pady=5)
        self.label1 = tk.Label(master=self.frame) 
        self.label1.pack(padx=5, pady=5)

        self.frame2 = tk.Frame(master= self.win ,relief=tk.RAISED,borderwidth=0)
        self.frame2.grid(row =3, column =2, padx=5,pady=5)
        self.label2 = tk.Label(master=self.frame2)
        self.label2.pack(padx=3, pady=5)

        self.frame3 = tk.Frame(master= self.win ,relief=tk.RAISED,borderwidth=0)
        self.frame3.grid(row =3, column =3, padx=10,pady=10)
        self.label3 = tk.Label(master=self.frame3)
        self.label3.pack(padx=3, pady=5)

        self.takki1 = tk.Button(master= self.win, command= live.switch)
        self.takki1.grid(row =3, column =0)

        self.takki2 = tk.Button(master= self.win,activebackground= None, text= "Exit", command= self.on_escape)
        self.takki2.grid(row =3, column =4)

        # run first time
        self.update(self.K_p,self.K_i,self.K_d,self.SetPoint)
    def run(self):
        self.win.mainloop()

    # function to stop the code running
    def on_escape(self,event=None):
        print("escaped")
        self.win.destroy()
        sys.exit()

    # update PID values from encoders
    def update(self,K_p = 0, K_i = 0, K_d = 0, SetPoint = 0):
        self.label1['text'] = "K_p = " + str(K_p)
        self.label2['text'] = "K_i = " + str(K_i)
        self.label3['text'] = "K_d = " + str(K_d)
        self.takki1['text'] = "SP = " + str(SetPoint)
        if live.good is True:
            self.takki1['bg'] = "green"
            self.takki1['activebackground'] = "green"
            self.takki1['fg'] = "white"
            self.takki1['activeforeground'] = "white"
        else:
            self.takki1['bg'] = "red"
            self.takki1['activebackground'] = "red"
            self.takki1['fg'] = "black"
            self.takki1['activeforeground'] = "black"
        self.frame3.after(200, self.update) # run itself again after 200 ms

    # creates lists of lists for the big plot
    def init(self):
        for line in self.lines:
            line.set_data(self.xs,[])
        return self.lines

    #Create the big graph
    def Big_Plot(self,i, y1, y2):

        self.y = random.randint(0,100)
        self.y1.append(self.y)
        self.y1 = self.y1[-self.x_len:]

        self.y = random.randint(0,100)
        self.y2.append(self.y)
        self.y2 = self.y2[-self.x_len:]

        self.ylist = [self.y1, self.y2]

        #for index in range(0,1):
        for lnum,line in enumerate(self.lines):
            line.set_ydata(self.ylist[lnum]) # set data for each line separately. 
        return self.lines

    # function for live animation on small graph no 1
    def small_plot1(self,i, ys):

        # Read temperature (Celsius) from TMP102
        self.K_p = round(random.randrange(0,50))     

        # Add y to list
        self.ys.append(self.K_p)

        # Limit y list to set number of items
        self.ys = self.ys[-self.x_len:]

        # Update line with new Y values
        self.line2.set_ydata(self.ys)

        return self.line2,

    # function for live animation on small graph no 2
    def small_plot2(self,i, ys):

        # Read temperature (Celsius) from TMP102
        self.K_i = round(random.randrange(0,50))     

        # Add y to list
        self.ys.append(self.K_i)

        # Limit y list to set number of items
        self.ys = self.ys[-self.x_len:]

        # Update line with new Y values
        self.line3.set_ydata(ys)

        return self.line3,

    # function for live animation on small graph no 3
    def small_plot3(self,i, ys):
            # get data for D
        self.K_d = round(random.randrange(0,50))     

        # Add y to list
        ys.append(self.K_d)

        # Limit y list to set number of items
        ys = ys[-self.x_len:]
        # Update line with new Y values
        self.line4.set_ydata(ys)
        return self.line4,
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
        self.encB = dg.DigitalInOut(board.D12)
        self.encB.direction = dg.Direction.INPUT
        self.encB.pull = dg.Pull.DOWN
        self.direction = ''
        self.i = 0
        self.iold = 0
        self.last_enc = True
        self.enc2 = rotaryio.IncrementalEncoder(board.D12,board.D16)

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

run = Good_GUI()
#actuator = SetPoint()

live = Live()
encbutton4 = Live()




# class task1():
#     def __init__(self):
#         self._running =True
    
#     def terminate(self):
#         self.running = False
    
#     def run():
#         actuator.move(gv.POS)

# class task2():
#     def __init__(self):
#         self._running =True
    
#     def terminate(self):
#         self.running = False
    
#     def run():
#         gv.POS = int(encoder4.get_setpoint())

class global_val():
    def __init__(self) -> None:
            self.POS = 0
            self.enc_val = 0
    
class gui_thread():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        run.run()
        

gv = global_val()
Gui_thread = gui_thread()   #Býr til Class
Gui_thread = Thread(target=Gui_thread.run())    #Býr til þráð 


# t1 = task1()
# t1 = Thread(target = t1.run())

# t2 = task2()
# t2 = Thread(target=t2.run())

Gui_thread.start()  #Kveikir á þráð
# t1.start()
# t2.start()


