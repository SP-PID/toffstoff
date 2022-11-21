import board
import analogio
import digitalio
import simpleio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_mpl3115a2
import time
import math
import adafruit_tcs34725

displayio.release_displays()    #Releses displays
i2c = board.I2C()  # uses board.SCL and board.SDA
signal_in = analogio.AnalogIn(board.A3) #Define analog pin as signal_in
#define display_bus
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128 #Define display width
HEIGHT = 64 #Define display hight

Rswitch = digitalio.DigitalInOut(board.D2)#Define the red switch.
Rswitch.direction = digitalio.Direction.INPUT#sets the pin to input
Rswitch.pull = digitalio.Pull.UP#Set pull up for input pin

#Defines the display
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()  #Variable for what to display
display.show(splash)    #Prints what is in splash on the display

#Code gotten from https://courses.ideate.cmu.edu/16-223/f2021/text/code/pico-signals.html
#Smootehs out signal data with a coefficiant
class Smoothing:
    
    def __init__(self, coeff=0.1):
        self.coeff = coeff
        self.value = 0

    def update(self, input):
        # compute the error between the input and the accumulator
        difference = input - self.value

        # apply a constant coefficient to move the smoothed value toward the input
        self.value += self.coeff * difference

        return self.value #Return the smoothed value

#A function that takes a thousand readings, runs them though smoothing code
#and returns the last value
def sense():
    smooth = Smoothing(0.2) #Define class

    #take 1000 measurements and run through the smoothing code
    for i in range(1000):
        signal = signal_in.value

        smoothed = smooth.update(signal)
        voltage = (smoothed * 3.3) / 65536
        distance = (23.0203 * voltage**4) + (-166.053 * voltage**3) + (444.6225 * voltage**2) + (-548.2265 * voltage) + 307.0276

    return distance

#main loop to run for ever
while True:

    #if the red switch is pressed the sense function is called
    #and the result from it displayed on the oled screen
    if Rswitch.value == False:
        splash = displayio.Group()#Clear screen
        distance = sense()#Call sense function

        #prepare data to be printed to screen
        text = "Distance {0:0.4f}".format(distance)
        text_area = label.Label(terminalio.FONT, text=text, x=15, y=35)
        splash.append(text_area)

        #Wrhile the switch is still pressed the program waits til it is released
        while Rswitch.value == False:
            time.sleep(0.001)

    display.show(splash) #Show data to display

