from tkinter import *
import tkinter as tk
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
import threading


SKREF = 100
pulse = dg.DigitalInOut(board.D23)
pulse.direction = dg.Direction.OUTPUT
direc = dg.DigitalInOut(board.D24)
direc.direction = dg.Direction.OUTPUT
enable = dg.DigitalInOut(board.D18)
enable.direction = dg.Direction.OUTPUT
stop = dg.DigitalInOut(board.D15)
stop.direction = dg.Direction.INPUT
stop.pull = dg.Pull.DOWN

class SetPoint():
    def __init__(self) -> None:
        #self.pulse_pin = pulse                                                          # Pins defined
        #self.dir_pin = direc
        #self.enable_pin = enable
        #self.button_pin = button
        self.pi = 3.14159265359                                                         # Everybody knows pi
        self.degrees_per_step = 1.8                                                     # for some reason this motor will move 0.225 degrees per step
        self.diameter = 19.65                                                           # diameter in millimeters
        self.total_travel = 840                                                         # total travel of the gantry plate is 800 millimeters
        self.circumference = self.diameter * self.pi                                    # circumference in millimeters
        self.steps_per_revolution = 360 / self.degrees_per_step                         # number of steps in a revolution
        self.distance_per_step = self.circumference / self.steps_per_revolution         # distance per step in millimeters
        self.steps_total = self.total_travel / self.distance_per_step                   # total number of steps per length of travel of gantry plate
        self.rotation = False                                                           # variable for which direction the motor will spin
        self.direction = "up"                                                           # variable to tell program to go up or down
        self.current_position = 0                                                       # initializes in lowest position
        self.highest_position = self.steps_total                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position
        self.reset_actuator()                                                           # actuator finds zero position (bottom)

    def get_total_steps(self):
        ''' Returns total number of steps for end to end travel '''
        return self.steps_total

    def enable_driver(self):        
        ''' Function that enables Easydriver for use '''
        enable.value = False
        #GPIO.output(self.enable_pin, False)  

    def disable_driver(self):        
        ''' Function that disables Easydriver after use '''
        enable.value = True
        #GPIO.output(self.enable_pin, True)   

    def update_rotation(self,direction):
        ''' Function updates variable for gantry travel direction '''
        self.direction = direction
        if self.direction == "up":
            self.rotation = True            # False means actuator moves up
        if self.direction == "down":
            self.rotation = False
        #GPIO.output(self.dir_pin, self.rotation)
        direc.value = self.rotation

    def pulse(self):
        ''' Function sends out one pulse on pulse pin '''
        #GPIO.output(self.pulse_pin, True)   # output pin 16 high
        pulse.value = True
        time.sleep(0.0007)      # wait
        #GPIO.output(self.pulse_pin, False)  # output pin 16 low
        pulse.value = False
        time.sleep(0.0007)      # wait

    def update_position(self,distance):
        ''' Function keeps track of current position of gantry '''
        if self.direction == "down":
            self.current_position -= distance
        if self.direction == "up":
            self.current_position += distance

    def move_to_position(self,position):
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
        print("Current position " + str(self.current_position))
        
    def spin_motor(self,steps):
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

    def reset_actuator(self):
        ''' Function that moves the gantry to zero position (bottom) '''
        self.update_rotation("down")    # sets travel direction to down
        self.enable_driver()            # enables the driver to move
        while True:
            self.pulse()                # sends out pulses until the button reads high
            if stop.value == True: #GPIO.input(self.button_pin) == GPIO.HIGH: # read a button
                print("Bottom reached!")    
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

def control_Stepper():
    position = encoder4.get_setpoint()
    actuator.move_to_position(position*20)
    return position

def on_escape(event=None):
    print("escaped")
    win.destroy()
    sys.exit()

def update():
   label1['text'] = "K_p = " + str(encoder1.Get_enc_val())
   label2['text'] = "K_i = " + str(encoder2.Get_enc_val())
   label3['text'] = "K_d = " + str(encoder3.Get_enc_val())
   frame3.after(200, update) # run itself again after 200 ms

def animate(i, y1, y2):

    y = control_Stepper()
    y1.append(y)
    y1 = y1[-x_len:]

    y = encoder4.encoder.position
    y2.append(y)
    y2 = y2[-x_len:]

    ylist = [y1, y2]

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_ydata(ylist[lnum]) # set data for each line separately. 

    return lines

def animate2(i, ys):

    # Read temperature (Celsius) from TMP102
    K_p = round(random.randrange(0,50))     

    # Add y to list
    ys.append(K_p)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line2.set_ydata(ys)

    return line2,

actuator = SetPoint()
encoder1 = encoders(0x36)
encoder2 = encoders(0x37)
encoder3 = encoders(0x38)
encoder4 = encoders(0x3a)

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
#win.attributes("-fullscreen", True)
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
figure = plt.figure(figsize=(11, 5), dpi=100)
gs = GridSpec(nrows=3, ncols=4)

################BIG PLOT################

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

def init():
    for line in lines:
        line.set_data(xs,[])
    return lines

y1 = [0] * x_len
y2 = [0] * x_len

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(figure, animate, fargs= (y1,y2), init_func=init,
                                interval=INTERVALS, blit=True)


################ SMALL PLOT 1 ################

# Create a figure of specific size
plot2 = figure.add_subplot(gs[0,3])
xs = list(range(0,x_len))
ys = [0]* x_len
plot2.set_ylim(y_range)
plot2.set_xlim(x_range)
plot2.set_title('K_p', rotation='vertical',x=1.1,y=0.3)
line2, = plot2.plot(xs,ys, color= "green")


ani2 = animation.FuncAnimation(figure,
    animate2,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)


################ SMALL PLOT 2 ################
#Create a figure of specific size
plot3 = figure.add_subplot(gs[1,3])
xs = list(range(0,x_len))
ys = [0]* x_len
plot3.set_ylim(y_range)
plot3.set_title('K_i', rotation='vertical',x=1.1,y=0.3)
line3, = plot3.plot(xs,ys)

def animate3(i, ys):

    # Read temperature (Celsius) from TMP102
    K_i = round(random.randrange(0,50))     


    # Add y to list
    ys.append(K_i)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line3.set_ydata(ys)

    return line3,

ani3 = animation.FuncAnimation(figure,
    animate3,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)

################ SMALL PLOT 1 ################

#Create a figure of specific size
plot4 = figure.add_subplot(gs[2,3])
xs = list(range(0,x_len))
ys = [0]* x_len
plot4.set_ylim(y_range)
plot4.set_title('K_d', rotation='vertical',x=1.1,y=0.3)
line4, = plot4.plot(xs,ys)

def animate4(i, ys):

    # get data for D
    K_d = round(random.randrange(0,50))     

    # Add y to list
    ys.append(K_d)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    # Update line with new Y values
    line4.set_ydata(ys)
    return line4,

ani4 = animation.FuncAnimation(figure,
    animate4,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)

###############################################################################

# Add a canvas widget to associate the figure with canvas
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().grid(row=0, column=0, rowspan=3, columnspan=4)

frame = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=0)
frame.grid(row =3, column =0, padx=5,pady=5)
label1 = tk.Label(master=frame, text=f"K_p = 5")
label1.pack(padx=5, pady=5)

frame2 = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=0)
frame2.grid(row =3, column =1, padx=5,pady=5)
label2 = tk.Label(master=frame2)
label2.pack(padx=3, pady=5)


frame3 = tk.Frame(master= win ,relief=tk.RAISED,fg= "green", bg = "red",borderwidth=0)
frame3.grid(row =3, column =2, padx=10,pady=10)
label3 = tk.Label(master=frame3)
label3.pack(padx=3, pady=5)


takki1 = tk.Button(master= win, text= "Exit", command= on_escape)
takki1.grid(row =3, column =3)


#PID_encoders(self,encoder, button, button_held, last_position):

# run first time
update()

win.mainloop()


