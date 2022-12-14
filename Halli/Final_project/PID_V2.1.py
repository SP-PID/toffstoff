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

SKREF = 20000
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

class Encoders():
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

class encoder_t():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        dc_enc = DC_encoders()
        while True:
            gv.enc_val = dc_enc.get_pos()

class gui_thread():
    def __init__(self):
        self.running =True

    def terminate(self):
        self.running = False

    def run(self):
        def on_escape(event=None):
            gv.exit = True
            win.destroy()
            sys.exit()

        # update PID values from encoders
        def update():
            label1['text'] = "K_p = " + str(gv.encodervalue1)
            label2['text'] = "K_i = " + str(gv.encodervalue2)
            label3['text'] = "K_d = " + str(gv.encodervalue3)
            takki1['text'] = "SP = " + str(gv.sp)
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
            frame3.after(200, update) # run itself again after 200 ms

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

            y = random.randint(0,100)
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
            K_p = round(gv.encodervalue1)     

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
            K_i = round(gv.encodervalue2)     


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
            K_d = round(gv.encodervalue3)     

            # Add y to list
            ys.append(K_d)

            # Limit y list to set number of items
            ys = ys[-x_len:]
            # Update line with new Y values
            line4.set_ydata(ys)
            return line4,

        # Constants to construct plots
        x_len = 300
        y_range = [0,300]
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
        ax1.set_title("this is the shit")
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
        plot2.set_ylim(y_range)
        plot2.set_xlim(x_range)
        plot2.set_title('K_p', rotation='vertical',x=1.1,y=0.3)
        line2, = plot2.plot(xs,ys, color= "green")

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
        plot3.set_title('K_i', rotation='vertical',x=1.1,y=0.3)
        line3, = plot3.plot(xs,ys)

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
        line4, = plot4.plot(xs,ys)

        ani4 = animation.FuncAnimation(figure,
            small_plot3,
            fargs=(ys,),
            interval=INTERVALS,
            blit=True)

        ###############################################################################

        # Add a canvas widget to associate the figure with canvas
        canvas = FigureCanvasTkAgg(figure, win)
        canvas.get_tk_widget().grid(row=0, column=0, rowspan=1, columnspan=5)

        frame = tk.Frame(master= win, bg = "red" ,relief=tk.RAISED,borderwidth=0)
        frame.grid(row =3, column =1, padx=5,pady=5)
        label1 = tk.Label(master=frame, text=f"K_p = 5") 
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

        win.mainloop()

class task1():
    def __init__(self):
        self.running =True
    
    def terminate(self):
        self.running = False
    
    def run(self):
        bla = gv.POS
        interval = 0.1
        old_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - old_time >= interval:
                bla = gv.POS
                old_time = cur_time
            actuator.move(bla) 

class task2():
    def __init__(self):
        self.running =True
    
    def terminate(self):
        self.running = False
    
    def run(self):
        while True:
            gv.POS = int(50)

class get_values():
    def __init__(self):
        self.running =True
    
    def terminate(self):
        self.running = False
    
    def run(self):
        while True:
            gv.sp = encoder4.get_setpoint()
            gv.encodervalue1 = encoder1.Get_enc_val()
            gv.encodervalue2 = encoder2.Get_enc_val()
            gv.encodervalue3 = encoder3.Get_enc_val()

class global_val():
    def __init__(self):
            self.POS = 0
            self.enc_val = 0
            self.exit = False
            self.sp = 0
            self.encodervalue1 = 0
            self.encodervalue2 = 0
            self.encodervalue3 = 0
    

motor_Ain1 = pwmio.PWMOut(board.D19,frequency = 1000)
motor_Ain2 = pwmio.PWMOut(board.D13,frequency = 1000)

dc_enc = DC_encoders()
pid = PID()
live = Live()
encbutton4 = Live()
encoder1 = Encoders(0x38)
encoder2 = Encoders(0x37)
encoder3 = Encoders(0x36)
encoder4 = Encoders(0x3a)
actuator = SetPoint()
gv = global_val()



# t1 = task1()
# t1 = Thread(target= t1.run)
# t1.start()


# t2 = task2()
# t2 = Thread(target= t2.run)
# t2.start()

t4 = get_values()
t4 = Thread(target= t4.run)
t4.start

t3 = gui_thread()
t3 = Thread(target= t3.run)
t3.start()


# encoder_thread = encoder_t()                            #B??r til Class
# encoder_thread = Thread(target=encoder_thread.run)      #B??r til ??r????  
# encoder_thread.start()                                  #Kveikir ?? ??r????

while True:


    PWM_val = pid.regulate(gv.sp, gv.enc_val) * 100
    print(gv.sp, gv.enc_val,PWM_val)

    if PWM_val > 65000:
        PWM_val = 65000

    if PWM_val < -65000:
        PWM_val = -65000

    if PWM_val < 0:
        motor_Ain1.duty_cycle = abs(PWM_val)
        motor_Ain2.duty_cycle = 65535
    elif PWM_val > 0:
        motor_Ain1.duty_cycle = 65535
        motor_Ain2.duty_cycle = abs(PWM_val)
    else:
        motor_Ain1.duty_cycle = 0
        motor_Ain2.duty_cycle = 0
    #time.sleep(0.01)