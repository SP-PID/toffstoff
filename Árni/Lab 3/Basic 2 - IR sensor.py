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

smooth = Smoothing(0.2) #Define class

while True:
    splash = displayio.Group()#Blank splash
    signal = signal_in.value #Read the signal value from teh IR sensor

    smoothed = smooth.update(signal) #Run teh signal vlaue trough the smoothing class

    voltage = (smoothed * 3.3) / 65536 # Calvulate the voltage from the value read

    #Calculate the distance in Cm using the polynomial from Matlab
    distance = (26.0865 * voltage**4) + (-175.0947 * voltage**3) + (437.4456 * voltage**2) + (-510.3618 * voltage) + 279.8494

    #Print the raw value that the m4 read to the screen 
    print((voltage,))
    text = "Raw {0:0.4f}".format(smoothed)
    text_area = label.Label(terminalio.FONT, text=text, x=15, y=15)
    splash.append(text_area)

    #Print the calculated voltage
    text = "Voltage {0:0.4f}".format(voltage)
    text_area = label.Label(terminalio.FONT, text=text, x=15, y=25)
    splash.append(text_area)

    #print the calculated distance
    text = "Distance {0:0.4f}".format(distance)
    text_area = label.Label(terminalio.FONT, text=text, x=15, y=35)
    splash.append(text_area)





    display.show(splash)
