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

def ewin_retry():
    pass

def ewin_destroy():
    pass

ewin = tk.Tk()
ewin.columnconfigure([0,1], minsize=250)
ewin.rowconfigure([0, 1], minsize=100)
ewin.eval('tk::PlaceWindow . center')
label1 = tk.Label(text="USB not found", font=("Helvetica", 20))
label1.grid(row=0, column=0, columnspan=2)

label2 = tk.Button(text="retry", command=ewin_retry)
label2.grid(row=1, column=0)
label3 = tk.Button(text="Cancel", command= ewin_destroy)
label3.grid(row=1, column=1)

ewin.mainloop()
