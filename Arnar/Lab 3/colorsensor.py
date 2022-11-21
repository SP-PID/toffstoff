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

#Defines the NeoPixel
rgbled = neopixel.NeoPixel(board.NEOPIXEL, 1)   
rgbled.brightness = 1 #Sets NeoPixel brightness

displayio.release_displays()  
# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
WIDTH = 128 #Define display width
HEIGHT = 64 #Define display hight
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group()  #Variable for what to display
display.show(splash) # Refreshes the screen

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
sensor.integration_time = 10 # This is refresh times in milliseconds
# Change sensor gain to 1, 4, 16, or 60
sensor.gain = 16 # Gain of the signal
def text_to_disp(text, xpos, ypos, scale): # function to set up the print to screen function
    text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale = scale)
    splash.append(text_area)
    return
# Main loop reading color and printing it every second.
while True:
    raw_data = sensor.color_raw # Getting the raw data for the clear data 
    splash = displayio.Group() #
    color = sensor.color # giving the color sensor a name as color
    color_rgb = sensor.color_rgb_bytes # This returns the values for RGB from (0-255)        
    rgbled[0] = color_rgb # Here we send the value from the color sensor to the Neopixel
    text =("Red: {0}".format(color_rgb[0])) # Setting the up printout to display value from the red filter
    text1 = ("Green: {0}".format(color_rgb[1])) # Setting the up printout to display value from the green filter
    text2 = ("Blue: {0}".format(color_rgb[2])) # Setting the up printout to display value from the blue filter
    text3 = ("Clear: {0}".format(raw_data[3])) # Setting the up printout to display value from the clear filter
    text_to_disp(text,0,4,1) # This is a call to the function above
    text_to_disp(text1,0,14,1)
    text_to_disp(text2,0,24,1)
    text_to_disp(text3,0,34,1)
    display.show(splash) # Refreshes the screen
    
    
