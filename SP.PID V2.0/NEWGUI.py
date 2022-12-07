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

global xstemp
xstemp = 0

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
            self.SetPoint = []
            self.DC_Motor = []
            self.Timi = []
            self.animate = False
            self.xstemp = 0
            self.xstemp1 = 0
            self.xstemp2 = 0
            self.xstemp3 = 0


########################## Write Data ##########################

class SaveData():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def StoreData(self):
        filename = 'SP-' +str(datetime.now().strftime("%Y-%m-%d %H.%M"))+'.csv'
        listi1 = [gv.SetPoint, gv.DC_Motor, gv.Timi]
        export_data = zip_longest(*listi1, fillvalue='')
        with open("temp.csv", mode= 'w',encoding="ISO-8859-1", newline= '') as csvfile:
            #fieldnames = ['SP', 'DC', 'Time']
            writer = csv.writer(csvfile)
            writer.writerow(("SP","DC","TIME"))
            writer.writerows(export_data)
        csvfile.close()
        gv.SetPoint = []
        gv.DC_Motor = []
        gv.Timi = []
        ## geyma undir öðru nafni rename-a og síðan move. 
        old_path = r'C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\temp.csv'
        new_path = r'C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\New path\temp.csv'
        shutil.move(old_path, new_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H.%M")
        old_name = r"C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\New path\temp.csv"
        new_name = r"C:\Users\olisb\Documents\Programing\SP.PID\toffstoff\SP.PID V2.0\New path\SP.PID " + timestamp + ".csv"
        os.rename(old_name,new_name)
 

live = Live()
gv = global_val()
savedata = SaveData()

class WriteDataThread():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while True:
            while live.good is True:
                self.sp = random.randint(0,100)
                self.dc = random.randint(100,200)
                self.timi = random.randint(200,300)
                gv.SetPoint.append(self.sp)
                gv.DC_Motor.append(self.dc)
                gv.Timi.append(self.timi)
                time.sleep(0.001)
            time.sleep(0.001)




writedata_thread =  WriteDataThread()
writedata_thread = Thread(target= writedata_thread.run)
writedata_thread.start()


########################## Button functions ##########################

def on_escape(event=None):
    exit = True
    win.destroy()
    sys.exit()
    #bæta hér við að slökkva á mótorum

def store():
    original = r'C:\Users\Ron\Deskto p\Test_1\products.csv'
    target = r'C:\Users\Roon\Desktop\Test_2\products.csv'
    
    shutil.copyfile(original, target)

def reset():
        while True:
            '''stoppa motora'''
            E_gluggi = Tk()
            E_gluggi.columnconfigure([0,1], minsize=250)
            E_gluggi.rowconfigure([0, 1], minsize=100)
            E_gluggi.attributes("-fullscreen", False)
            E_gluggi.attributes("-topmost", True)
            E_gluggi.configure(background= 'red')
            E_gluggi.eval('tk::PlaceWindow . center')
            label1 = tk.Label(text="E stop on", font=("Helvetica", 20),bg= 'red')
            label1.grid(row=0, column=0, columnspan=2)
            E_gluggi.mainloop()
            E_gluggi.after(4000, E_gluggi.destroy())

########################## GUI STARTS ##########################

# update PID values from encoders
def update():
    label1['text'] = "K_p = " + str(1)
    label2['text'] = "K_i = " + str(2)
    label3['text'] = "K_d = " + str(3)
    label4['text'] = "SP = " + str(4)
    takki1['text'] = "Record"
    if live.good is True:
        takki1['bg'] = "green"
        takki1['activebackground'] = "green"
        takki1['fg'] = "white"
        takki1['activeforeground'] = "white"
        gv.animate = False
    else:
        takki1['bg'] = "red"
        takki1['activebackground'] = "red"
        takki1['fg'] = "black"
        takki1['activeforeground'] = "black"
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
        y = random.randint(0,100)
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

# Constants to construct plots
x_len = 500
y_range = [0,800]
x_range = [0,x_len]
INTERVALS = 0

# Create an instance of tkinter frame
splash = Tk()
splash.title("Loading screen")
splash.geometry("1024x600")
#splash.attributes("-fullscreen", True)
splash.wm_attributes("-topmost", True)
rammi = Frame(splash, width=1024, height= 600)
rammi.pack()
rammi.place(anchor= 'center', relx= 0.5, rely= 0.5)
#splash_label = Label(splash, text= "LOADING", font= ("helvetica", 20),bg= '#ab23ff')
#splash_label.pack(anchor= 'w',pady=290, padx = 250)
splash.wm_attributes('-transparentcolor','#ab23ff')

img= ImageTk.PhotoImage(Image.open("Loading.png"))
rammi = Label(rammi, image= img)
rammi.pack()


win= Tk()

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# --- fullscreen & configurations ---

# run fullscreen
#win.attributes("-fullscreen", True)
# keep on top
win.wm_attributes("-topmost", False)
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
anim = animation.FuncAnimation(figure, Big_Plot, fargs= (y1,y2,xs), init_func=init,
                                interval=INTERVALS, blit=True)


################ SMALL PLOT 1 ################

plot2 = figure.add_subplot(gs[1:10,31:40])
#xs = list(range(0,x_len))
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
takki3.grid(row =3, column =7)

takki4 = tk.Button(master= win,activebackground= None, text= "Reset", command= reset)
takki4.grid(row =3, column =6)

# run first time
update()
def winmain():
    splash.destroy()
    #gv.animate= True
    #print(gv.animate)
#    win.mainloop()

splash.after(4000, winmain)

splash.mainloop()