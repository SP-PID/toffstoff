import board
import digitalio
import analogio
import simpleio
import time
import neopixel
from rainbowio import colorwheel
import adafruit_mpl3115a2
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import adafruit_framebuf
import busio as io
import adafruit_ssd1306
import ulab

displayio.release_displays()    #Releses displays
i2c = board.I2C()   #Define i2c variable

#define display_bus
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
WIDTH = 128 #Define display width
HEIGHT = 64 #Define display hight

#Defines the display
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

splash = displayio.Group()  #Variable for what to display
display.show(splash)    #Prints what is in splash on the display

# Greating
text = "Hello"  #Define the text greating
#Creaates a text area at a certain place with a sertain scale
text_area = label.Label(terminalio.FONT, text=text, x=20, y=HEIGHT//2, scale = 3)
splash.append(text_area) #Text area addet to splash

Rswitch = digitalio.DigitalInOut(board.D2)#Define the red switch.
Rswitch.direction = digitalio.Direction.INPUT#sets the pin to input
Rswitch.pull = digitalio.Pull.UP#Set pull up for input pin

sensor = adafruit_mpl3115a2.MPL3115A2(i2c)  #Defines barrometric sensor
rgbled = neopixel.NeoPixel(board.NEOPIXEL, 1)   #Define NeoPixel LED

zero = 101325   #Zero value for pressure att sea level in Pa

lis1 = []#empty list

#function to add things to splash.append
#takes in the text, x and y positions and the scale
#and adds it to splash
def text_to_disp(text, xpos, ypos, scale):
    text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale = scale)
    splash.append(text_area)
    return


#Main run loop
while True:
    splash = displayio.Group()#Blank splash

    #Redefine sensor for each loop to avoid
    #pressure and altitude data problems.
    #If not done pressure and altitude data won't
    #be correct.
    sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
    text = "Hold red to zero"
    text_to_disp(text, 0, 54, 1)#Adds text to splash

    #check if the red switch has been pressed.
    #If so take the last measured pressure value
    #and asign it to the zero to get a new zero point.
    #Once the press has been registered a "Zeroed!!!"
    #message will be shown.
    if Rswitch.value == False:
        zero = int(pressure*100)# set new zero
        sensor.sealevel_pressure = zero #Assign the new zero to sensor
        text = "Zeroed!!!" #Define message
        splash.pop()    #Remove the last text item added to splash
        text_to_disp(text, 0, 54, 1)# add zeroed message to splash


    #Adds the zero line to splash to be displayed
    text = "zero:{0:0.1f}Hpa".format(zero / 100)
    text_to_disp(text, 0, 44, 1)
    sensor.sealevel_pressure = zero #assign zero to sensor



    pressure = sensor.pressure #Read sensor pressure

    #Adds the pressure line to splash to be displayed
    text = "Pre:{0:0.1f} Hpa".format(pressure)
    text_to_disp(text, 0, 14, 1)

    #Insert the current measured pressure and adds it
    #to the start of the list
    lis1.insert(0,pressure)

    #If the list has more than 10 elemnets
    #remove the oldest element
    if len(lis1) > 10:
        lis1.pop()

    nparr = ulab.numpy.zeros(10)#Define a numpy array
    #Copy al form lis1 to the numpy array
    for i in range(0,len(lis1)):
        nparr[i] = lis1[i]

    #Calculate the difference of each elemnt to the next
    #and puts the result into a new array called diffs
    diffs = ulab.numpy.diff(nparr)

    #If the sum of the difference's is positive the pressure
    #is increasing over time so a up arrow is printed.
    #if the sum is negative a down arrow is printed
    #if the sum is zero the pressure is holding steady.
    if ulab.numpy.sum(diffs) > 0:
        text = "^"
    elif ulab.numpy.sum(diffs) < 0:
        text = "v"
    else:
        text = "-"

    text_to_disp(text, 100, 25, 2)

    #Print a line that shows altitude from sensor
    altitude = sensor.altitude
    text = "Alt:{0:0.1f} M".format(altitude)
    text_to_disp(text, 0, 24, 1)

    #print a line that shows temperature from sensor
    temp = sensor.temperature
    text = "Temp:{0:0.1f} °C".format(temp)
    text_to_disp(text, 0, 34, 1)

    display.show(splash)#Show elements in splash on screen
    time.sleep(1)#Wait for one second





