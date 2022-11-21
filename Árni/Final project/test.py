
from tkinter import *
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec

# Create an instance of tkinter frame
win= Tk()

# Set the window size
win.geometry("1024x600")

# Use TkAgg
matplotlib.use("TkAgg")

# Create a figure of specific size
figure = Figure(figsize=(5, 5), dpi=100)
gs = GridSpec(nrows=3, ncols=4)
plot = figure.add_subplot(gs[:,1:3])

# Define Data points for x and y axis
x = [0.2,0.5,0.8,1.0 ]
y = [ 1.0, 1.2, 1.3,1.4]
plot.plot(x, y, color="red", marker="x", linestyle="-")

plot2 = figure.add_subplot(gs[1,4])
x = [0.2,0.5,0.8,1.0 ]
y = [ 1.0, 1.2, 1.3,1.4]
plot2.plot(x, y, color="red", marker="x", linestyle="-")

# Add a canvas widget to associate the figure with canvas
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().grid(row=0, column=0)

# Create a figure of specific size
# figure1 = Figure(figsize=(3, 3), dpi=70)
# figure1 = Figure(figsize=(3, 3), dpi=100)
# Define the points for plotting the figure
# plot1 = figure1.add_subplot(1, 1, 1)
# plot1.plot(0.6, 0.1, color="blue", marker="o", linestyle="")
# plot1 = figure1.add_subplot(1,1,1)
# plot1,plot(0.5,0.3,color="green", marker="o", linestyle="")
# Define Data points for x and y axis
# x = [0.2,0.5,0.8,1.0 ]
# y = [ 1.0, 1.2, 1.3,1.4]
# plot1.plot(x, y, color="red", marker="x", linestyle="")
# x1 = [0.2,0.5,0.8,1.0 ]
# y1 = [1,2,3,4]
# plot1.plot(x1, y1, color="red", marker="x", linestyle="")
# Add a canvas widget to associate the figure with canvas
# canvas = FigureCanvasTkAgg(figure1, win)
# canvas.get_tk_widget().grid(row=0, column=101)
win.mainloop()

