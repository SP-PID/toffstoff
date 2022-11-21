#https://www.geeksforgeeks.org/matplotlib-animate-multiple-lines/ <---MÖGULEGA BETRI LAUSN?
from tkinter import *
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import sys


x_len = 300
y_range = [0,300]
x_range = [0,300]
INTERVALS = 0

def on_escape(event=None):
    print("escaped")
    win.destroy()
    sys.exit()
# Create an instance of tkinter frame
win= Tk()

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# --- fullscreen ---

win.attributes("-fullscreen", True) # run fullscreen
win.wm_attributes("-topmost", True) # keep on top

# --- closing methods ---

# close window with key `ESC`
win.bind("<Escape>", on_escape)

# Set the window size
win.geometry("1024x600")

###############################################################################

# Use TkAgg
matplotlib.use("TkAgg")


# Create a figure of specific size
figure = plt.figure(figsize=(11, 5), dpi=100)
gs = GridSpec(nrows=3, ncols=4)


ax1 = figure.add_subplot(gs[:,0:3],)
xs = list(range(0,300))
ys = [0]* x_len
ax1.set_ylim(y_range)
ax1.set_xlim(x_range)
ax1.set_title('Something Else')
line, = ax1.plot([], [], lw=2)
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

def animate(i, y1, y2):

    y = random.randrange(100,200)
    y1.append(y)
    y1 = y1[-x_len:]

    y = random.randrange(0,100)
    y2.append(y)
    y2 = y2[-x_len:]

    ylist = [y1, y2]

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_ydata(ylist[lnum]) # set data for each line separately. 

    return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(figure, animate, fargs= (y1,y2), init_func=init,
                                interval=INTERVALS, blit=True)


###############################################################################

# Create a figure of specific size
plot2 = figure.add_subplot(gs[0,3])
xs = list(range(0,300))
ys = [0]* x_len
plot2.set_ylim(y_range)
plot2.set_xlim(x_range)
plot2.set_title('Something Else')
line2, = plot2.plot(xs,ys)

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

ani2 = animation.FuncAnimation(figure,
    animate2,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)


###############################################################################

#Create a figure of specific size
plot3 = figure.add_subplot(gs[1,3])
xs = list(range(0,300))
ys = [0]* x_len
plot3.set_ylim(y_range)
plot3.set_title('This Is Different')
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




###############################################################################
#Create a figure of specific size
plot4 = figure.add_subplot(gs[2,3])
xs = list(range(0,300))
ys = [0]* x_len
plot4.set_ylim(y_range)
plot4.set_title('This Is also Different')
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

frame = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=1)
frame.grid(row =3, column =0, padx=5,pady=5)
label = tk.Label(master=frame, text=f"K_p = 5")
label.pack(padx=5, pady=5)

frame2 = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=1)
frame2.grid(row =3, column =1, padx=5,pady=5)
label = tk.Label(master=frame2, text=f"K_i = 5")
label.pack(padx=3, pady=5)

frame2 = tk.Frame(master= win ,relief=tk.RAISED,borderwidth=1)
frame2.grid(row =3, column =2, padx=10,pady=10)
label = tk.Label(master=frame2, text=f"K_i ={random.randrange(0,100)} ")
label.pack(padx=3, pady=5)

button1 = tk.Button(master= win, text= "Exit", command= on_escape)
button1.grid(row =3, column =3)

win.mainloop()
