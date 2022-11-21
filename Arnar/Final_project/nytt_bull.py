import matplotlib.pyplot as plt
from matplotlib import animation
import random

x_len = 300
y_range = [0,300]
INTERVALS = 0

xs = list(range(0,x_len))

fig = plt.figure()
ax1 = plt.axes(xlim=(0, 300), ylim=(0,300))
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

# fake data
frame_num = 100


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
anim = animation.FuncAnimation(fig, animate, fargs= (y1,y2), init_func=init,
                                interval=INTERVALS, blit=True)


plt.show()