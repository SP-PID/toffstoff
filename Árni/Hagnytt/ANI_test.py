import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import time


fig, ax = plt.subplots()
global i
i = 0
xdata, ydata = [0]*100, [0] * 10 #[*range(0,100,1)]

ln, = ax.plot([], [])

def init():
    ax.set_xlim(data[1][0], data[1][-1])
    ax.set_ylim(-1, 10)
    return ln,

def update(frames,data,):
    global i

    t = time.time()-First
    data[1].append(t)
    data[2].append(np.sin(t*10)) #(random.uniform(0,9))

    print(data[1])

    #print(data)
    if data[1][-1] < 10:
        ax.set_xlim(0,10)
    else:    
        ax.set_xlim(data[1][-1] - 10, data[1][-1])
    
    #xdata.append(data[1][0])
    #ydata.append(data[2][0])
    
    ln.set_data(data[1], data[2])
    if i < 10:
        i += 1
    return ln,

data = {1:[0] * 10,2:[0] * 10}


data[1].insert(0,time.time())
First = data[1][0]
data[1][0] = data[1][0] - First
data[2].insert(0,random.randint(0,5)) 


#print(data)

ani = FuncAnimation(fig, update, fargs = (data,),
                    init_func=init, blit=False, interval = 1)
plt.show()