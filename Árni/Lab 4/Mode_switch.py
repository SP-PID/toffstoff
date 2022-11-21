import time
import board
import adafruit_tcs34725
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import busio as io
import digitalio
import analogio
import simpleio
import adafruit_ssd1306
import neopixel
from rainbowio import colorwheel
import countio
import asyncio

# Use board SCL and SDA
i2c = board.I2C()

# Defines the NeoPixel
Neo = neopixel.NeoPixel(board.NEOPIXEL, 1)
Neo.brightness = 1  # Sets NeoPixel brightness

# Define screen
displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128  # Define display width
HEIGHT = 64  # Define display hight
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group()  # Variable for what to display
display.show(splash)  # Refreshes the screen

# defines the IR sensor
signal_in = analogio.AnalogIn(board.A3)

# Buttons
# Emgstop
E_stop = digitalio.DigitalInOut(board.D2)
E_stop.direction = digitalio.Direction.INPUT
E_stop.pull = digitalio.Pull.UP
# Mode buttton
Mode_switch = digitalio.DigitalInOut(board.D3)  # Define the mode switch.
Mode_switch.direction = digitalio.Direction.INPUT  # sets the pin to input
Mode_switch.pull = digitalio.Pull.UP  # Set pull up for input pin

Select_sw = digitalio.DigitalInOut(board.D4)  # Define the mode switch.
Select_sw.direction = digitalio.Direction.INPUT  # sets the pin to input
Select_sw.pull = digitalio.Pull.UP  # Set pull up for input pin

# Defining Encoders pin 
encA = countio.Counter(board.D10, edge=countio.Edge.RISE)
encB = countio.Counter(board.D9, edge=countio.Edge.RISE)




# Class to smooth the input from the IR sensor
class Smoothing:
    def __init__(self, coeff=0.1):
        self.coeff = coeff
        self.value = 0

    def update(self, input):
        # compute the error between the input and the accumulator
        difference = input - self.value

        # apply a constant coefficient to move the smoothed value toward the input
        self.value += self.coeff * difference

        return self.value  # Return the smoothed value


# Define colorsensor

class RGB:
    def __init__(self, time=10, gain=16, i2c=i2c):
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.integration_time = time # This sets the time of refreshing
        self.gain = gain # Sets the gain, The gain can be 1,4,16,60. With increasing gain more disturbance

    def raw_data(self):
        return self.sensor.color_raw  # Gives raw values including Clear light value

    def rgb_values(self):
        return self.sensor.color_rgb_bytes  # Gives back normalized RGB values

    def temp(self):
        return (
            self.sensor.color_temperature
        )  # returns the the heat of the color in kelvin

    def lux(self):
        return self.sensor.lux  # light intensity

# define screen
class screen:
    def __init__(self,i2c=i2c): # Init the class
        displayio.release_displays() # Releases displays
        self.display_bus = displayio.I2CDisplay(i2c, device_address=0x3C) # Sets the I2C bus address 
        self.disp = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=64) # initiatiates the screen
        self.splash = displayio.Group() # Clears cache

    def text_to_disp(self,text, xpos, ypos, scale):  # Function to set up the print to screen function
        text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale=scale)
        self.splash.append(text_area) # Sends the text to the screen
        
    def show(self):
        
        display.show(self.splash)    #Prints what is in splash on the display
    def clear(self):
        self.splash = displayio.Group()  #Clears cache



def IR_test():
    global modes
    smooth = Smoothing(0.2)  # Define class
    disp.clear()
    Text = "IR test"  # Text to display
    timestamp = time.monotonic()
    while True:
        signal = signal_in.value  # Read the signal value from teh IR sensor

        smoothed = smooth.update(signal)  # Run teh signal vlaue trough the smoothing class

        voltage = (smoothed * 3.3) / 65536  # Calculate the voltage from the value read
        

        # Calculate the distance in Cm using the polynomial from Matlab
        distance = ((26.0865 * voltage ** 4)+ (-175.0947 * voltage ** 3)+ (437.4456 * voltage ** 2)+ (-510.3618 * voltage)+ 279.8494)
        disp.text_to_disp(Text, 0, 8, 2)  # Function to print
        # Print the raw value that the m4 read to the screen
        text1 = "Raw: {0:0.4f}".format(smoothed)# Text to display
        disp.text_to_disp(text1, 0, 28, 1)  # Function to print
        # Print the calculated voltage
        text2 = "Voltage: {0:0.4f} V".format(voltage) # Text to display
        disp.text_to_disp(text2, 0, 38, 1)  # Function to print
        
        # print the calculated distance
        text3 = "Distance: {0:0.4f} Cm".format(distance)# Text to display
        disp.text_to_disp(text3, 0, 48, 1)  # Function to print
        
        disp.show() # Displaying on the display
        disp.clear() # Clearing the screen cache
        if E_stop.value == False: # Emg stop to send to Start mode
            modes = 0
            return True
        if Mode_switch.value == False:
            return False
    disp.show()
    return False


def Color_match():
    disp.clear()
    global modes
    Text = "ColorMatch"  # Printing out the mode
    disp.text_to_disp(Text, 0, 8, 2)  # Function to print the text
    disp.show() # Call to class to display text
    timestamp = time.monotonic()  # Takes the timestamp
    while True:
        color_sensor = RGB()  # Initiates the class for the color sensor
        RGB_values = color_sensor.rgb_values()  # Gets the normalized RGB values
        Neo[0] = RGB_values  # Sends the normalized rgb values to the NeoPixel
        if E_stop.value == False: # Emergency stop, to stop whatever is happening and send to Start
            modes = 0 # sets variable to 0 for Start mode
            return True # Returns true to continue
        if Mode_switch.value == False:
            Neo[0] = (0,0,0) #Shuts off the NeoPixel
            return False
            
    return False


def start():
    global modes # Calling the global modes variable
    Text = "Start"  # Printing out the mode
    disp.clear() # Call to the class to clear cache

    disp.text_to_disp(Text,0,8,2) # Call to class to set what to print
    disp.text_to_disp("Press mode switch to\ncontinue",0,28,1) # Call to class to set what to print
    disp.show() # Call to the class to display
    
    
    while True:
        if Mode_switch.value == False: # way to increment the modes value
            modes += 1 # Makes the mode value increas by one
            while Mode_switch.value == False: # This is an easy way to make it increment once
                p = 1 # Useless but necessary variable
            return


def Wait():
    global modes # Calling on the global modes variable
    Text = "Next mode"  # Printing out the mode
    disp.clear() # Calling the class to clear the cache

    disp.text_to_disp(Text,0,8,2) # Calling the class and setting what the text to display is
    disp.text_to_disp("Press mode switch",0,28,1) # Call to class to set what to print
    disp.text_to_disp("to continue",0,38,1) # Call to class to set what to print
    disp.text_to_disp("Press E-stop to",0,48,1) # Call to class to set what to print
    disp.text_to_disp("return to start",0,58,1) # Call to class to set what to print
    disp.show() # Call to the class to display the text
    
    while Mode_switch.value == False:
        p = 1
    
    while True:
        if Mode_switch.value == False: # incrementing the modes value
            modes += 1
            return False
        if E_stop.value == False: # Emg stop to go to Start mode
            modes = 0
            return True

def Tachometer():
    global modes # Calling the global "modes" variable
    disp.clear() # clearing the cache on the screen
    timestamp = time.monotonic() # Getting the time
    while True: # Runs for 5 secons
        disp.clear() # Clear the cache on the screen
        disp.text_to_disp("Tachometer test",0,8,2) # Sending text to display
        increment = encA.count          # increment reader
        distance = (encA.count*0.2)     # distance traveled (143.3/700 = 0.2)
        disp.text_to_disp("distance: {0:0.1f} mm".format(distance), 0, 28, 1) # sending text to display the distance
        disp.text_to_disp("increment: {0:0.1f}".format(increment), 0, 38, 1) # sending text to display the increment
        disp.show() # Making the display display
        if E_stop.value == False: # EMG stop to send to Start
            modes = 0
            return True
        if Mode_switch == False:
            return False
    return False


def main(): # Here is our main function
    global modes # define modes as global
    global disp # defines disp as global variable
    modes = 0 # sets  starting value as 0
    disp = screen() # initiates 

    while True:
        if modes == 0 :
            start() # Starts the program goes into Start mode
        if modes == 1:
            if IR_test(): # If IR is done running continue to wait
                continue
            Wait() # Test to see if pressed to go to the next mode
        elif modes == 2:
            if Color_match(): # If Color match is True 
                continue
            Wait() # waiting for input
        elif modes == 3:
            if Tachometer(): # Call on the encoder function
                continue
            modes = 0  # Sends it to Start mode

main() # Our main function
