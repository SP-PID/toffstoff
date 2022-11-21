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

    y = gv.enc_val
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
plot3.set_title('K_i', rotation='vertical',x=1.1,y=0.3)
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

takki1 = tk.Button(master= win)
takki1.grid(row =3, column =0)

takki2 = tk.Button(master= win,activebackground= None, text= "Exit", command= on_escape)
takki2.grid(row =3, column =4)

# run first time
update()

win.mainloop()
