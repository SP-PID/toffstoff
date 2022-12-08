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

'''create tkinter'''

splash = Tk()
splash.title("Loading screen")
splash.geometry("1024x600")
splash.attributes("-fullscreen", False)
splash.wm_attributes("-topmost", False)
splash.grid()
texti = Text()
rammi = Frame(splash)
rammi.pack()
rammi.place(anchor= 'center', relx= 0.5, rely= 0.5)
img= ImageTk.PhotoImage(Image.open("Loading.png"))
rammi = Label(rammi, image= img)
rammi.pack()

splash.mainloop()