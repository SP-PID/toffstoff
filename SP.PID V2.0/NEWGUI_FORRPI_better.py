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

########################## Estop ##########################

class Estop():
    def __init__(self) -> None:
        self.EHnappur = dg.DigitalInOut(board.D18)
        
    def estop_destroy(self):
        if self.EHnappur.value is True:
            self.E_gluggi.destroy()
        else:
            pass

    def estop(self):
        while True:
            if self.EHnappur.value is False:
                '''stoppa motora'''
                self.E_gluggi = Tk()
                self.E_gluggi.columnconfigure([0,1], minsize=250)
                self.E_gluggi.rowconfigure([0, 2], minsize=100)
                self.E_gluggi.geometry("1024x600")
                self.E_gluggi.attributes("-fullscreen", True)
                self.E_gluggi.attributes("-topmost", True)
                self.E_gluggi.configure(background= 'red')
                self.E_gluggi.eval('tk::PlaceWindow . center')
                label1 = tk.Label(text="EMERGENCY STOP", font=("Helvetica", 20),bg= 'red')
                label1.grid(row=0, column=0, columnspan=2)
                label2 = tk.Label(text="Twist button when safe", font=("Helvetica", 20),bg= 'red')
                label2.grid(row=1, column=0, columnspan=2)
                Etakki1 = tk.Button(master= self.E_gluggi, text= "Reset", command= self.estop_destroy)
                Etakki1.grid(row =2, column =0, columnspan= 2)
                self.E_gluggi.mainloop()

            if self.EHnappur.value is True:
                '''endurraesa motora'''
                break

########################## DC Controller ##########################

class DC_control():
    def __init__(self, port) :
        self.port = port
        self.ser = serial.Serial(
        port=self.port,
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
    
    def read(self):
        x = self.ser.readline()
        x = x.decode(encoding='UTF-8',errors='strict')
        return x

    def write(self, value):
        self.ser.write(str.encode(value))
    
    def dc_data(self):
        try:
            x = self.read()
            x = x.split(" ")
            Dc = int(x[1])
            timi = int(x[0])
            print(x)
            return timi, Dc
        except:
            pass

########################## Stepper Controller ##########################

class Stepper_control():
    def __init__(self,port) :
        self.port = port
        self.ser = serial.Serial(
        port=port,
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
        x = x.decode(encoding='UTF-8',errors='strict')
        print("stepper" + x)
        time.sleep(0.01)

    def write(self, value):
        self.ser.write(str.encode(value))
    
    def calibrate(self):
        self.ser.write(str.encode('identify'))
    
    def run(self):
        self.ser.write(str.encode('run'))
    
    def stop(self):
        self.ser.write(str.encode('notrun'))    

########################## Read/Write encoders ##########################

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
            #print(self.encoder.position)


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

########################## Bool Switch ##########################

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

########################## Global Variables ##########################

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
            self.SetPoint = []
            self.DC_Motor = []
            self.Timi = []
            self.animate = False
            self.xstemp = 0
            self.xstemp1 = 0
            self.xstemp2 = 0
            self.xstemp3 = 0
            self.Estop = False

########################## Write Data ##########################

class SaveData():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def StoreData(self):
        listi1 = [gv.SetPoint, gv.DC_Motor, gv.Timi]
        export_data = zip_longest(*listi1, fillvalue='')
        with open("temp.csv", mode= 'w',encoding="ISO-8859-1", newline= '') as csvfile:
            #fieldnames = ['SP', 'DC', 'Time']
            writer = csv.writer(csvfile)
            writer.writerow(("SP","DC","TIME"))
            writer.writerows(export_data)
        csvfile.close()
        ## geyma undir öðru nafni rename-a og síðan move
        dir_path = r'/media/pipipi/' 
        res = []
        try:
            for (dir_path, dir_names, file_names) in os.walk(dir_path):
                res.extend(dir_names)
                break
            print(res)
            old_path = r'/home/pipipi/Documents/PID_REGL/temp.csv'
            new_path = r"/media/pipipi/" + res[0] + "/temp.csv"
            shutil.move(old_path, new_path)
            timestamp = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
            old_name = r"/media/pipipi/" + res[0]+ "/temp.csv"
            new_name = r"/media/pipipi/" + res[0]+ "/SP.PID " + timestamp + ".csv"
            os.rename(old_name,new_name)
            gv.SetPoint = []
            gv.DC_Motor = []
            gv.Timi = []
        except IndexError:
            print("Enginn USB Lykill")
            self.ErrorWindow()
            pass

    def ErrorWindow(self):
        self.ewin = tk.Tk()
        self.ewin.columnconfigure([0,1], minsize=250)
        self.ewin.rowconfigure([0, 1], minsize=100)
        #self.ewin.geometry("1024x600")
        self.ewin.attributes("-fullscreen", False)
        self.ewin.attributes("-topmost", True)
        self.ewin.eval('tk::PlaceWindow . center')
        label12 = tk.Label(text="USB not found", font=("Helvetica", 20))
        label12.grid(row=0, column=0, columnspan=2)
        label22 = tk.Button(text="retry", command=self.ewin_retry)
        label22.grid(row=1, column=0)
        label32 = tk.Button(text="Cancel", command= self.ewin_destroy)
        label32.grid(row=1, column=1)
        self.ewin.mainloop()

    def ewin_destroy(self):
        self.ewin.destroy()
        gv.SetPoint = []
        gv.DC_Motor = []
        gv.Timi = []
        pass
    
    def ewin_retry(self):
        self.ewin.destroy()
        self.StoreData()

########################## Get serial devices ##########################

#def set_up_serial():
s = serial.Serial(baudrate = 115200,timeout=1)
avableports = []
portNames = [
"/dev/ttyUSB0",
"/dev/ttyUSB1",
"/dev/ttyUSB2",
"/dev/ttyUSB3",
]   

for pname in portNames:
    try:
        s.port = pname
        s.open()
        if s.isOpen():
            print("Found {}.".format(pname))
            avableports.append(pname)
        
    except:
        pass

    s.close()
print(avableports)

for port in avableports:
    print("Checking port {}".format(port))
    s.port = port
    s.open()
    time.sleep(1.5)
    s.write(str.encode('identify'))
    time.sleep(0.5)
    x = s.readline()
    x = x.decode(encoding='UTF-8',errors='strict')
    x = x.strip()
    print(x)
    s.close()
    
    if x == "DC":
        dc_control = DC_control(port)
        time.sleep(1.5)
        dc_control.write("identify")
        time.sleep(0.25)
        if dc_control.read == "DC":
            print("DC control active!")
        else:
            print("DC controll Error!")

    elif x == "Stepper":
        stepper_control = Stepper_control(port)
        time.sleep(1.5)
        stepper_control.write("identify")
        time.sleep(0.25)
        if stepper_control.read == "Stepper":
            print("Stepper control active!")
        else:
            print("Stepper controll Error!")

    else:
        
        print("{} not known!".format(port))

    time.sleep(2)

########################## Define Classes ##########################
print("fyrir")
#stepper_control.run()

time.sleep(0.1)
stepper_control.calibrate()
print("eftir")
#dc_control = DC_control()
#stepper_control = Stepper_control()
#set_up_serial()
live = Live()
gv = global_val()
savedata = SaveData()
kp = Encoders(0x38)
ki = Encoders(0x37)
kd = Encoders(0x36)
sp = Encoders(0x3a)
E_stop = Estop()


########################## Threads ##########################

class get_values_thread():
    def __init__(self):
        self.running =True
    
    def terminate(self):
        self.running = False
    
    def run(self):
        kpold = kp.Get_enc_val()
        kiold = ki.Get_enc_val()
        kdold = kd.Get_enc_val() 
        while True:
            gv.sptemp = sp.get_setpoint() * 10
            #print(gv.sptemp)
            kptemp = kp.Get_enc_val()
            kitemp = ki.Get_enc_val()
            kdtemp = kd.Get_enc_val()
            if E_stop.EHnappur.value is False:
                E_stop.estop()
            #print(gv.sptemp)
            if not sp.button.value and not  sp.button_held:
                gv.sp = gv.sptemp
                dc_control.set_SP(gv.sptemp)
                stepper_control.set_SP(gv.sptemp)
            if kpold != kptemp:
                gv.kp = kptemp
                kpold = kptemp
                dc_control.set_P(kptemp)
            if kiold != kitemp:
                gv.ki = kitemp
                kiold = kitemp
                dc_control.set_I(kitemp)
            if kdold != kdtemp:
                gv.kd = kdtemp
                kdold = kdtemp
                dc_control.set_D(kdtemp)

class WriteDataThread():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while True:
            while live.good is False:
                self.sp = gv.sptemp
                #self.timi, self.dc = dc_control.dc_data()
                gv.SetPoint.append(self.sp)
                #gv.DC_Motor.append(self.dc)
                #gv.Timi.append(self.timi)
                time.sleep(0.001)
            time.sleep(0.001)

class Drive_stepper_motor_thread():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):

        stepper_control.run()
        oldsp = 0
        while True:
            if oldsp != gv.sp:           
                stepper_control.set_SP(gv.sp)
                oldsp = gv.sp
                print(gv.sp)
            time.sleep(0.000001)

class Drive_DC_motor_thread():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while True:
            pass

get_values = get_values_thread()
get_values = Thread(target= get_values.run)
get_values.start()

writedata_thread =  WriteDataThread()
writedata_thread = Thread(target= writedata_thread.run)
writedata_thread.start()

stepper_thread = Drive_stepper_motor_thread()
stepper_thread = Thread(target= stepper_thread.run)
stepper_thread.start()

########################## GUI Functions ##########################

def on_escape(event=None):
    exit = True
    win.destroy()
    sys.exit()
    #bæta hér við að slökkva á mótorum

# update PID values from encoders
def update():
    label1['text'] = "K_p = " + str(gv.kp)
    label2['text'] = "K_i = " + str(gv.ki)
    label3['text'] = "K_d = " + str(gv.kd)
    label4['text'] = "SP = " + str(gv.sptemp)
    takki1['text'] = "Record"
    if live.good is True:
        takki1['bg'] = "green"
        takki1['activebackground'] = "green"
        takki1['fg'] = "white"
        takki1['activeforeground'] = "white"
        gv.animate = False
        takki1['text'] = "Record"        
    else:
        takki1['bg'] = "red"
        takki1['activebackground'] = "red"
        takki1['fg'] = "black"
        takki1['activeforeground'] = "black"
        takki1['text'] = "Recording"   
        gv.animate = True
    frame3.after(50, update) # run itself again after 200 ms

# creates lists of lists for the big plot
def init():
    for line in lines:
        line.set_data(xs,[])
    return lines

# function for live animation on the BIG graph
def Big_Plot(i, y1, y2,xs):
    if gv.animate:
        y = gv.sp
        y1.append(y)
        
        y = random.randint(100,200)
        y2.append(y)
        if gv.xstemp < x_len - 1:
            gv.xstemp += 1
        else:    
            xs = xs[-x_len:]
        xs.append(gv.xstemp)
    y2 = y2[-x_len:]
    y1 = y1[-x_len:]

    ylist = [y1, y2]

#for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_data(xs, ylist[lnum]) # set data for each line separately. 
    return lines

# function for live animation on small graph no 1
def small_plot1(i, ys, xs):
    if gv.animate:
        # Read temperature (Celsius) from TMP102
        K_p = random.randint(0,50)     

        # Add y to list
        ys.append(K_p)
        
        if gv.xstemp1 < x_len - 1:
            gv.xstemp1 += 1
        else:    
            xs = xs[-x_len:]
        #xs.insert(0,time)
        xs.append(gv.xstemp1)
        # Limit y list to set number of items
        #ys = ys[-x_len:]
        ys = ys[-x_len:]

        # Update line with new Y values
        line2.set_data(xs,ys)
        #line2.set_xdata(xs)

    return line2,

# function for live animation on small graph no 2
def small_plot2(i, ys, xs):
    if gv.animate:
        # Read temperature (Celsius) from TMP102
        K_i = random.randint(0,50)    

        ys.append(K_i)
        if gv.xstemp2 < x_len - 1:
            gv.xstemp2 += 1
        else:    
            xs = xs[-x_len:]
        # Add y to list
        xs.append(gv.xstemp2)

        # Limit y list to set number of items
        ys = ys[-x_len:]

        # Update line with new Y values
        line3.set_data(xs, ys)

    return line3,

# function for live animation on small graph no 3
def small_plot3(i, ys, xs):
    if gv.animate:
        # Read temperature (Celsius) from TMP102
        K_d = random.randint(0,50)    

        ys.append(K_d)
        if gv.xstemp3 < x_len - 1:
            gv.xstemp3 += 1
        else:    
            xs = xs[-x_len:]
        # Add y to list
        xs.append(gv.xstemp3)

        # Limit y list to set number of items
        ys = ys[-x_len:]

        # Update line with new Y values
        line4.set_data(xs, ys)

    return line4,

########################## LOADING SCREEN ##########################

splash = Tk()
splash.title("Loading screen")
splash.geometry("1024x600")
splash.attributes("-fullscreen", True)
splash.wm_attributes("-topmost", True)
rammi = Frame(splash, width=1024, height= 600)
rammi.pack()
rammi.place(anchor= 'center', relx= 0.5, rely= 0.5)
img= ImageTk.PhotoImage(Image.open("Loading.png"))
rammi = Label(rammi, image= img)
rammi.pack()




########################## GUI STARTS ##########################
# Constants to construct plots
x_len = 500
y_range = [0,800]
x_range = [0,x_len]
INTERVALS = 0
win= Tk()

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# --- fullscreen & configurations ---

# run fullscreen
win.attributes("-fullscreen", True)
# keep on top
win.attributes("-topmost", True)
# close window with key `ESC`
win.bind("<Escape>", on_escape)
# hide cursor
'''uncomment win.config to hide cursor'''
win.config(cursor = "none")
# Set the window size
win.geometry("1024x600")
# Use TkAgg
matplotlib.use("TkAgg")

######################################

# Create a figure of specific size
figure = plt.figure(figsize=(11, 6), dpi=93)
gs = GridSpec(nrows=36, ncols=40)
plt.subplots_adjust(left= 0.05,right= 0.96,bottom= 0.05, top= 0.96)

################ BIG PLOT ################

ax1 = figure.add_subplot(gs[:,0:29],)
ax1.grid(linestyle= '--')
xs = []
ys = []
ax1.set_ylim(y_range)
ax1.set_xlim(x_range)
ax1.set_title("SP.PID")
line, = ax1.plot([], [])
plotlays, plotcols = [2], ["black","red"]
lines = []

for index in range(2):
    lobj = ax1.plot([],[],lw=2,color=plotcols[index])[0]
    lines.append(lobj)

y1 = []
y2 = []

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(figure,
        Big_Plot, 
        fargs= (y1,y2,xs), 
        init_func=init,
        interval=INTERVALS, 
        blit=True)

################ SMALL PLOT 1 ################

plot2 = figure.add_subplot(gs[1:10,31:40])

xs = []
ys = []
plot2.set_ylim(y_range)
plot2.set_xlim(x_range)
plot2.set_title('PWM', rotation='vertical',x=1.1,y=0.3)
line2, = plot2.plot(xs,ys, color= "red")

ani2 = animation.FuncAnimation(figure,
    small_plot1,
    fargs=(ys,xs,),
    interval=INTERVALS,
    blit=True)

################ SMALL PLOT 2 ################

plot3 = figure.add_subplot(gs[13:22,31:40])
xa = []
ya = []
plot3.set_ylim(y_range)
plot3.set_xlim(x_range)
plot3.set_title('PWM', rotation='vertical',x=1.1,y=0.3)
line3, = plot3.plot(xa,ya, color= "red")

ani3 = animation.FuncAnimation(figure,
        small_plot2,
        fargs=(ya,xa,),
        interval=INTERVALS,
        blit=True)

################ SMALL PLOT 3 ################

plot4 = figure.add_subplot(gs[25:34,31:40])
xb = []
yb = []
plot4.set_ylim(y_range)
plot4.set_xlim(x_range)
plot4.set_title('K_d', rotation='vertical',x=1.1,y=0.3)
line4, = plot4.plot(xb,yb, color= "red")

ani4 = animation.FuncAnimation(figure,
        small_plot3,
        fargs=(yb,xb,),
        interval=INTERVALS,
        blit=True)

###############################################################################

# Add a canvas widget to associate the figure with canvas
canvas = FigureCanvasTkAgg(figure, master= win)
canvas.get_tk_widget().grid(row=0, column=0, rowspan=1, columnspan=7,)

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

frame4 = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=0)
frame4.grid(row =3, column =0, padx=10,pady=10)
label4 = tk.Label(master=frame4)
label4.pack(padx=3, pady=5)


takki1 = tk.Button(master= win, command= live.switch)
takki1.grid(row =3, column =4)

takki2 = tk.Button(master= win,activebackground= None, text= "Exit", command= on_escape)
takki2.grid(row =3, column =5)

takki3 = tk.Button(master= win,activebackground= None, text= "Save", command= savedata.StoreData)
takki3.grid(row =3, column =6)

takki4 = tk.Button(master= win,activebackground= None, text= "Reset", command= on_escape)
takki4.grid(row =3, column =7)
update()
def winmain():
    splash.destroy()
#    win.mainloop()

splash.after(4000, winmain)

splash.mainloop()