import tkinter as tk

window = tk.Tk()

frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
frame1.pack(fill=tk.Y, side=tk.LEFT)

frame2 = tk.Frame(master=window, width=100,height=100, bg="yellow")
frame2.pack(fill=tk.Y, side=tk.LEFT)

frame3 = tk.Frame(master=window, width=50,height= 100, bg="blue")
frame3.pack(fill=tk.Y, side=tk.RIGHT)

frame4 = tk.Frame(master=window, width=50,height= 100, bg="green")
frame4.pack(fill=tk.Y, side=tk.TOP)

frame5 = tk.Frame(master=window, width=50,height= 100, bg="purple")
frame5.pack(fill=tk.Y, side=tk.TOP)

frame6 = tk.Frame(master=window, width=100,height= 100, bg="black")
frame6.pack(fill=tk.Y, side=tk.BOTTOM)


window.mainloop()