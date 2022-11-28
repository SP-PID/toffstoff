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
from time import sleep, perf_counter
from threading import Thread
from PIL import ImageTk, Image
import csv
import shutil 


class WriteData():
    def __init__(self):
        pass

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


live = Live()
gv = global_val()
########################## Button functions ##########################

def on_escape(event=None):
    exit = True
    win.destroy()
    sys.exit()
    #bæta hér við að slökkva á mótorum

def store():
    original = r'C:\Users\Ron\Deskto p\Test_1\products.csv'
    target = r'C:\Users\Ron\Desktop\Test_2\products.csv'
    
    shutil.copyfile(original, target)

def reset():
    pass

########################## GUI STARTS ##########################

# update PID values from encoders
def update():
    label1['text'] = "K_p = " + str(1)
    label2['text'] = "K_i = " + str(2)
    label3['text'] = "K_d = " + str(3)
    takki1['text'] = "SP = " + str(4)
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

    y = random.randint(0,100)
    y1.append(y)
    y1 = y1[-x_len:]

    y = random.randint(100,200)
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
    K_p = random.randint(0,50)     

    # Add y to list
    ys.insert(0,K_p)

    # Limit y list to set number of items
    #ys = ys[-x_len:]
    ys = ys[:x_len]
    # Update line with new Y values
    line2.set_ydata(ys)

    return line2,

# function for live animation on small graph no 2
def small_plot2(i, ys):

    # Read temperature (Celsius) from TMP102
    K_i = random.randint(0,50)    


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
    K_d = random.randint(0,50)    

    # Add y to list
    ys.append(K_d)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    # Update line with new Y values
    line4.set_ydata(ys)
    return line4,

# Constants to construct plots
x_len = 500
y_range = [0,800]
x_range = [0,x_len]
INTERVALS = 0

# Create an instance of tkinter frame
splash = Tk()
splash.title("Test Loading screen")
splash.geometry("1024x600")
splash.attributes("-fullscreen", True)
splash.wm_attributes("-topmost", True)
rammi = Frame(splash, width=1024, height= 600)
rammi.pack()
rammi.place(anchor= 'center', relx= 0.5, rely= 0.5)
#splash_label = Label(splash, text= "LOADING", font= ("helvetica", 20),bg= '#ab23ff')
#splash_label.pack(anchor= 'w',pady=290, padx = 250)
splash.wm_attributes('-transparentcolor','#ab23ff')

img= ImageTk.PhotoImage(Image.open("SP.PID V2.0\Loading.png"))
rammi = Label(rammi, image= img)
rammi.pack()

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
'''uncomment win.config to hide cursor'''
#win.config(cursor = "none")
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

plot2 = figure.add_subplot(gs[1:10,31:40])
xs = list(range(0,x_len))
ys = [0]* x_len
plot2.set_ylim([-255,255])
plot2.set_xlim([0,x_len])
plot2.set_title('PWM', rotation='vertical',x=1.1,y=0.3)
line2, = plot2.plot(xs,ys, color= "red")

ani2 = animation.FuncAnimation(figure,
    small_plot1,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)

################ SMALL PLOT 2 ################

plot3 = figure.add_subplot(gs[13:22,31:40])
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

plot4 = figure.add_subplot(gs[25:34,31:40])
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

takki1 = tk.Button(master= win, command= live.switch)
takki1.grid(row =3, column =0)

takki2 = tk.Button(master= win,activebackground= None, text= "Exit", command= on_escape)
takki2.grid(row =3, column =4)

takki3 = tk.Button(master= win,activebackground= None, text= "Save", command= store)
takki3.grid(row =3, column =5)

takki4 = tk.Button(master= win,activebackground= None, text= "Reset", command= on_escape)
takki4.grid(row =3, column =6)

# run first time
update()
def winmain():
    splash.destroy()
#    win.mainloop()

splash.after(400, winmain)

splash.mainloop()