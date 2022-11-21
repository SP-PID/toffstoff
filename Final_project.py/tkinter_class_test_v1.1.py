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
from time import sleep, perf_counter
from threading import Thread

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

live = Live()
encbutton4 = Live()

class Good_GUI():
    def __init__(self):
        #constant that will be used
        self.x_len = 300
        self.y_range = [0,300]
        self.x_range = [0,self.x_len]
        self.INTERVALS = 0
        # Create an instance of tkinter frame
    def run(self):
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
        self.frame.grid(row =3, column =0, padx=5,pady=5)
        self.label1 = tk.Label(master=self.frame, text=f"K_p = 5") 
        self.label1.pack(padx=5, pady=5)

        self.frame2 = tk.Frame(master= self.win ,relief=tk.RAISED,borderwidth=0)
        self.frame2.grid(row =3, column =1, padx=5,pady=5)
        self.label2 = tk.Label(master=self.frame2)
        self.label2.pack(padx=3, pady=5)

        self.frame3 = tk.Frame(master= self.win ,relief=tk.RAISED,borderwidth=0)
        self.frame3.grid(row =3, column =2, padx=10,pady=10)
        self.label3 = tk.Label(master=self.frame3)
        self.label3.pack(padx=3, pady=5)

        self.takki1 = tk.Button(master= self.win, command= live.switch)
        self.takki1.grid(row =3, column =3)

        self.takki2 = tk.Button(master= self.win,activebackground= None, text= "Exit", command= self.on_escape)
        self.takki2.grid(row =3, column =4)

        # run first time
        self.update()

        self.win.mainloop()




    # function to stop the code running
    def on_escape(self,event=None):
        print("escaped")
        self.win.destroy()
        sys.exit()

    # update PID values from encoders
    def update(self):
        self.label1['text'] = "K_p = " + str(50)
        self.label2['text'] = "K_i = " + str(30)
        self.label3['text'] = "K_d = " + str(40)
        self.takki1['text'] = "SP = " + str(20)
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

run = Good_GUI()
run.run()