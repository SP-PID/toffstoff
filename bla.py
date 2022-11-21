# SSD1306, Pot and Switch, ItsyBitsy M4 Express V4
#     *** Tony Goodhew 11 June 2018 ***
# Lines, boxes, blocks and circles
# Bar graph + Defined characters
# 10 K Ohm Pot on A5 and Switch on D2
# SSD1306 on SDA and SCL - I2C

import gc  # Import libraries
import board
import math
from time import sleep
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import adafruit_framebuf
gc.collect()  # Make room

#Set up ssd1306
import busio as io
import adafruit_ssd1306
i2c = io.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Set up Potentiometer and button switch
pot_in = AnalogIn(board.A5)    # Potentiometer
sw = DigitalInOut(board.D2)    # Switch
sw.direction = Direction.INPUT
sw.pull = Pull.UP              # Internal pull-up

# Define special characters - 8 bytes each - 0...7
# Bytes top to bottom, 5 least significant bits only
smiley = [0x00,0x0A,0x00,0x04,0x11,0x0E,0x00,0x00]
sad = [0x00,0x0A,0x00,0x04,0x00,0x0E,0x11,0x00]
heart = [0,0,0,10,31,14,4,0]
b_heart = [0,10,31,0,0,14,4,0]
up_arrow =[0,4,14,21,4,4,0,0]
down_arrow = [0,4,4,21,14,4,0,0]
bits = [128,64,32,16,8,4,2,1]  # Powers of 2

def char(xpos, ypos, pattern):  # Print defined character
    for line in range(8):       # 5x8 characters
        for ii in range(5):     # Low value bits only
            i = ii + 3
            dot = pattern[line] & bits[i]  # Extract bit
            if dot:  # Only print WHITE dots
                oled.pixel(xpos+i*2, ypos+line*2, dot)
                oled.pixel(xpos+i*2+1, ypos+line*2, dot)
                oled.pixel(xpos+i*2, ypos+line*2+1, dot)
                oled.pixel(xpos+i*2+1, ypos+line*2+1, dot)

def horiz(l,r,t,c):  # left, right ,top, colour
    n = r-l+1        # Horizontal line
    for i in range(n):
        oled.pixel(l + i, t , c)

def vert(l,t,b,c):   # left, top, bottom, colour
    n = b-t+1        # Vertical line
    for i in range(n):
        oled.pixel(l, t+i, c)

def box(l,r,t,b,c):  # left, right, top, bottom, colour
    horiz(l,r,t,c)   # Hollow rectangle
    horiz(l,r,b,c)
    vert(l,t,b,c)
    vert(r,t,b,c)

def block(l,r,t,b,c):  # left, right, top, bottom, colour
    n = b-t+1          # Solid rectangle
    for i in range(n):
        horiz(l,r,t+i,c)  # One line at a time

def line(x,y,xx,yy,c): # (x,y) to (xx,yy)
    if x > xx:
        t = x  # Swap co-ordinates if necessary
        x = xx
        xx = t
        t = y
        y = yy
        yy = t
    if xx-x == 0:  # Avoid div by zero if vertical
        vert(x,min(y,yy),max(y,yy),c)
    else:          # Draw line one dot at a time L to R
        n=xx-x+1
        grad = float((yy-y)/(xx-x))  # Calculate gradient
        for i in range(n):
            y3 = y + int(grad * i)
            oled.pixel(x+i,y3,c)  # One dot at a time

def display(t):  # Time in seconds
    oled.show()  # Show new screen and wait
    sleep(t)

def deg(xx,yy):  # Draw Degree symbol
    oled.pixel(xx,yy+1,1)
    oled.pixel(xx,yy,1)
    oled.pixel(xx+1,yy,1)
    oled.pixel(xx+1,yy+1,1)

def align(n, max_chars):
    # Aligns string of n in max_chars
    msg1 = str(n)
    space = max_chars - len(msg1)
    msg2 = ""
    for m in range(space):
        msg2 = msg2 +" "
    msg2 = msg2 + msg1
    return msg2  # String - ready for display

def showgraph(v):   # Bar graph on SSD 1306
    oled.text("P", 0, 50, 1)
    block(10, v+10, 50, 60, 1)
    vert(10, 45, 63, 1)
    if val == 100:
        oled.text("T",115, 50, 1)
    else:
        oled.text(str(v),111, 50, 1)

def circle(cx,cy,r,c):   # Centre (x,y), radius, colour
    for angle in range(0, 90, 2):  # 0 to 90 degrees in 2s
        y3=int(r*math.sin(math.radians(angle)))
        x3=int(r*math.cos(math.radians(angle)))
        oled.pixel(cx-x3,cy+y3,c)  # 4 quadrants
        oled.pixel(cx-x3,cy-y3,c)
        oled.pixel(cx+x3,cy+y3,c)
        oled.pixel(cx+x3,cy-y3,c)

oled.fill(1)  # Clear screen WHITE
oled.text("Free space:",30,15,0)  # BLACK text
oled.text(str(gc.mem_free()),44,30,0)
oled.show()   # Update screen
sleep(3)
oled.fill(0)  # Clear screen BLACK
oled.show()
for r in range(5,30,5):  # Draw concentric circles
    circle(64,32,r,1)
display(3)
oled.fill(0)  # Clear screen BLACK
oled.show()
for r in range(5,30,5):  # Moving centre
    circle(64,10+r,r,1)
display(3)

oled.fill(1)
oled.text("LINES",47,20,0)  # Black on white
display(2)

oled.fill(0)                  # Lines demo
for step in range(8, 1, -1):
    oled.fill(0)
    msg = "Step: " + str(step)
    oled.text(msg, 44, 20, 1)
    display(1)
    oled.fill(0)
    x = 0  # Block 1
    y = 0
    x2 = 127
    for y2 in range(0,64, step):
        line(x, y, x2, y2, 1)
        oled.show()
    x = 0  # Block 2
    y = 63
    x2 = 127
    for y2 in range(63,-1,-step):
        line(x, y, x2, y2, 1)
        oled.show()
    x = 127  # Block 3
    y = 0
    x2 = 0
    for y2 in range(0,64, step):
        line(x, y, x2, y2, 1)
        oled.show()
    x = 127  # Block 4
    y = 63
    x2 = 0
    for y2 in range(63,-1,-step):
        line(x, y, x2, y2, 1)
        oled.show()
    sleep(1)
oled.fill(0)  # Clear up
oled.show()

while True: # Turn the pot, press button down, hold and release
    pot = pot_in.value
    oled.fill(0)
    button = sw.value  # Read button switch
    msg = "Pot RAW: " + align(str(pot), 5) +"   "
    oled.text(msg, 0, 10, 1)
    power = int(255 * pot / 65300)  # Range 0 to 255
    msg = "Power: " + align(str(power), 3) +"   "
    oled.text(msg,0, 20,1)
    oled.text("  ? C", 90,20,1)   # No temperature sensor fitted
    deg(110,20)                   # Degree character
    val = int(power * 100 / 255)  # Range 0 to 100 ('T')
    showgraph(val)
    if button == 1:  # This is the slow part of the loop
        oled.text("1",6,34,1)
        char(16, 30, up_arrow)    # Defined characters
        char(34, 30, smiley)      # when button UP
        char(54, 30, heart)
        oled.text("True", 80,36,1)
    else:
        oled.text("0",6,34,1)
        char(16, 30, down_arrow)  # Defined characters
        char(34, 30, sad)         # when button pressed
        char(54, 30, b_heart)
        oled.text("False",80,36,1)
    oled.show()