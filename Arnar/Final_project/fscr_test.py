#https://www.geeksforgeeks.org/matplotlib-animate-multiple-lines/ <---MÖGULEGA BETRI LAUSN?
import itertools
from tkinter import *
from tkinter import ttk
import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
x_len = 300
y_range = [0,300]
INTERVALS = 0


def on_escape(event=None):
    print("escaped")
    win.destroy()
# Create an instance of tkinter frame
win= Tk()



###############################################################################

# Use TkAgg
matplotlib.use("TkAgg")

# Create a figure of specific size
figure = plt.figure(figsize=(11, 5), dpi=100)
gs = GridSpec(nrows=3, ncols=4)


plot = figure.add_subplot(gs[:,0:3],)
xs = list(range(0,300))
ys = [0]* x_len
plot.set_ylim(y_range)
# plot2 = figure.add_subplot(gs[0,3])
x = [20,50,80,100 ]
y = [ 10, 10, 30,40]

line, = plot.plot(xs,ys)


def animate(i, ys,):
    # Read temperature (Celsius) from TMP102
    Pid = random.randrange(0,100)
    sp = random.randrange(100,200)
    # Add y to list
    ys.append(Pid)
    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)
    return line,

ani = animation.FuncAnimation(figure,
    animate,
    fargs=(ys,),
    interval=INTERVALS,
    blit=True)


###############################################################################

# Create a figure of specific size
plot2 = figure.add_subplot(gs[0,3])
xs = list(range(0,300))
ys = [0]* x_len
plot2.set_ylim(y_range)
plot2.set_title('Something Else')
line2, = plot2.plot(xs,ys)
K_p =random.randrange(0,100)
def animate2(i, ys,K_p,line2):

    # Read temperature (Celsius) from TMP102
    #K_p = round(random.randrange(0,50))     

    # Add y to list
    ys.append(K_p)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line2.set_ydata(ys)

    return line2,

ani2 = animation.FuncAnimation(figure,
    animate2,
    fargs=(ys,K_p,line2),
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
K_i = random.randrange(100,200)

def animate3(i, ys):
    # Read temperature (Celsius) from TMP102
    # Add y to list
    ys.append(K_i)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line3.set_ydata(ys)

    return line3,

ani3 = animation.FuncAnimation(figure,
    animate2,
    fargs=(ys,K_i,line3),
    interval=INTERVALS,
    blit=True)


# plot3 = figure.add_subplot(gs[1,3])
# x = [0.2,0.5,0.8,1.0 ]
# y = [ 1.0, 1.2, 1.3,1.4]
# plot3.plot(x, y, color="red", marker="x", linestyle="-")

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

# plot4 = figure.add_subplot(gs[2,3])
# x = [0.2,0.5,0.8,1.0 ]
# y = [ 1.0, 1.2, 1.3,1.4]
# plot4.plot(x, y, color="red", marker="x", linestyle="-")

###############################################################################

# Add a canvas widget to associate the figure with canvas
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().grid(row=0, column=0, rowspan=3, columnspan=4)


ki = 5

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
label = tk.Label(master=frame2, text=f"K_i ={ki} ")
label.pack(padx=3, pady=5)

button1 = tk.Button(master= win, text= "Exit", command= on_escape)
button1.grid(row =3, column =3)


# frame = tk.Frame(master=win, width=150, height=150)
# frame.pack()



# label2 = tk.Label(master=frame, text="I'm at (75, 75)", bg="yellow")
# label2.place(x=1000, y=1000)



win.mainloop()