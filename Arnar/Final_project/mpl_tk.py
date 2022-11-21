# import tkinter as tk
# import matplotlib

# matplotlib.use('TkAgg')

# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg,
#     NavigationToolbar2Tk
# )


# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title('Tkinter Matplotlib Demo')

#         # prepare data
#         data = {
#             'Python': 11.27,
#             'C': 11.16,
#             'Java': 10.46,
#             'C++': 7.5,
#             'C#': 5.26
#         }
#         languages = data.keys()
#         popularity = data.values()

#         # create a figure
#         figure = Figure(figsize=(6, 4), dpi=100)

#         # create FigureCanvasTkAgg object
#         figure_canvas = FigureCanvasTkAgg(figure, self)

#         # create the toolbar
#         NavigationToolbar2Tk(figure_canvas, self)

#         # create axes
#         axes = figure.add_subplot()

#         # create the barchart
#         axes.bar(languages, popularity)
#         axes.set_title('Top 5 Programming Languages')
#         axes.set_ylabel('Popularity')

#         figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# if __name__ == '__main__':
#     app = App()
#     app.mainloop()




    # Import required libraries
from tkinter import *
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create an instance of tkinter frame
win= Tk()

# Set the window size
win.geometry("1024x600")

# Use TkAgg
matplotlib.use("TkAgg")

# Create a figure of specific size
figure = Figure(figsize=(5, 5), dpi=100)
#figure1 = Figure(figsize=(3, 3), dpi=100)
# Define the points for plotting the figure
plot = figure.add_subplot(1, 1, 1)
plot.plot(0.6, 0.1, color="blue", marker="o", linestyle="")
#plot1 = figure1.add_subplot(1,1,1)
#plot1,plot(0.5,0.3,color="green", marker="o", linestyle="")
# Define Data points for x and y axis
x = [0.2,0.5,0.8,1.0 ]
y = [ 1.0, 1.2, 1.3,1.4]
plot.plot(x, y, color="red", marker="x", linestyle="-")
#x1 = [0.2,0.5,0.8,1.0 ]
#y1 = [1,2,3,4]
#plot1.plot(x1, y1, color="red", marker="x", linestyle="")
# Add a canvas widget to associate the figure with canvas
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().grid(row=0, column=0)

# Create a figure of specific size
figure1 = Figure(figsize=(3, 3), dpi=70)
#figure1 = Figure(figsize=(3, 3), dpi=100)
# Define the points for plotting the figure
plot1 = figure1.add_subplot(1, 1, 1)
plot1.plot(0.6, 0.1, color="blue", marker="o", linestyle="")
#plot1 = figure1.add_subplot(1,1,1)
#plot1,plot(0.5,0.3,color="green", marker="o", linestyle="")
# Define Data points for x and y axis
x = [0.2,0.5,0.8,1.0 ]
y = [ 1.0, 1.2, 1.3,1.4]
plot1.plot(x, y, color="red", marker="x", linestyle="")
#x1 = [0.2,0.5,0.8,1.0 ]
#y1 = [1,2,3,4]
#plot1.plot(x1, y1, color="red", marker="x", linestyle="")
# Add a canvas widget to associate the figure with canvas
canvas = FigureCanvasTkAgg(figure1, win)
canvas.get_tk_widget().grid(row=0, column=101)
win.mainloop()

# import pandas as pd
# import numpy as np
# import tkinter as tk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
    
# class Graph(tk.Frame):
#     def __init__(self, master=None, title="", *args, **kwargs):
#         super().__init__(master, *args, **kwargs)
#         self.fig = Figure(figsize=(4, 3))
#         ax = self.fig.add_subplot(111)
#         df = pd.DataFrame({"values": np.random.randint(0, 50, 10)}) #dummy data
#         df.plot(ax=ax)
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self)
#         self.canvas.draw()
#         tk.Label(self, text=f"Graph {title}").grid(row=0)
#         self.canvas.get_tk_widget().grid(row=1, sticky="nesw")
#         toolbar_frame = tk.Frame(self)
#         toolbar_frame.grid(row=2, sticky="ew")
#         NavigationToolbar2Tk(self.canvas, toolbar_frame)
    
# root = tk.Tk()
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# # --- fullscreen ---

# #root.overrideredirect(True)  # sometimes it is needed to toggle fullscreen
#                               # but then window doesn't get events from system
# #root.overrideredirect(False) # so you have to set it back

# root.attributes("-fullscreen", True) # run fullscreen
# root.wm_attributes("-topmost", True) # keep on top
# #root.focus_set() # set focus on window

# # --- closing methods ---

# def on_escape(event=None):
#     print("escaped")
#     root.destroy()
# # close window with key `ESC`
# root.bind("<Escape>", on_escape)

# for num, i in enumerate(list("ABC")):
#     Graph(root, title=i, width=200).grid(row=num//2, column=num%2)

# text_box = tk.Text(root, width=50, height=10, wrap=tk.WORD)
# text_box.grid(row=1, column=1, sticky="nesw")
# text_box.delete(0.0, "end")
# text_box.insert(0.0, 'My message will be here.')

# root.mainloop()