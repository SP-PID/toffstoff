# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
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
display.show(splash) 
# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4
class RGB:
    def __init__(self,time = 10,gain=16,i2c):
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.integration_time = time 
        self.gain = gain
        
    def raw_data(self):
        return self.sensor.color_raw

    def rgb_values(self):
        return self.sensor.color_rgb_bytes

sensor.integration_time = 10
sensor.gain = 16
def text_to_disp(text, xpos, ypos, scale):
    text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale = scale)
    splash.append(text_area)
    return
# Main loop reading color and printing it every second.
red = 0
green = 0
blue = 0
while True:
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    #print(sensor.color_raw)
    test = round(sensor.color_raw[0]/255)
    test1 = round(sensor.color_raw[1]/255)
    test2 = round(sensor.color_raw[2]/255)
    #print("Test {0} {1} {2}".format(test,test1,test2))
    raw_data = sensor.color_raw
    splash = displayio.Group()
    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    #print(
    #    "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
    #        color, color_rgb
    #    )
    #)

    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    if raw_data[3] > 450:
        green = 0
        blue = 0
        red = 0
        text =("Crash")
        text_to_disp(text,0,8,2)
    
    elif color_rgb[0] > color_rgb[1] and color_rgb[0] > color_rgb[2]:
        red = color_rgb[0]
        print(red)
        green = 0
        blue = 0
        red += 60
        

        text =("Vinstri")
        text_to_disp(text,0,8,2)
    elif color_rgb[1] > color_rgb[0] and color_rgb[1] > color_rgb[2]:
        green = color_rgb[1]
        green += 60
        red = 0
        blue = 0
        #color_rgb[1] = green
        text =("Beint")
        text_to_disp(text,0,8,2)
    elif color_rgb[2] > color_rgb[1] and color_rgb[2] > color_rgb[0]:
        blue = color_rgb[2]
        blue += 60
        green = 0
        red = 0
        
        #color_rgb[2] = blue
        text =("Hægri")
        text_to_disp(text,0,8,2)
        
    rgbled[0] = (red,green,blue)
    
    #rgbled[1] = color_rgb[1]
    #rgbled[2] = color_rgb[2]
    #print(rgbled)
    text =("Red: {0}".format(color_rgb[0]))
    #text1 = ("Green: {0}".format(color_rgb[1]))
    #text2 = ("Blue: {0}".format(color_rgb[2]))
    #text3 = ("Clear: {0}".format(raw_data[3]))
    text_to_disp(text,0,8,2)
    #text_to_disp(text1,0,14,1)
    #text_to_disp(text2,0,24,1)
    #text_to_disp(text3,0,34,1)
    
    
    
    #print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
    # Delay for a second and repeat.
    display.show(splash)
    
    
