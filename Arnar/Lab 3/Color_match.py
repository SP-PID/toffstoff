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


# Use board SCL and SDA
i2c = board.I2C()

# Defines the NeoPixel
Neo = neopixel.NeoPixel(board.NEOPIXEL, 1)
Neo.brightness = 1  # Sets NeoPixel brightness


class RGB: # class to be able to call on the rgb sensor
    def __init__(self,time = 10,gain=16,i2c=i2c):
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.sensor.integration_time = time 
        self.sensor.gain = gain
        self.sensor.led
        
    def raw_data(self):
        return self.sensor.color_raw #returns the raw values, we use clear value

    def rgb_values(self):
        return self.sensor.color_rgb_bytes # Gives us normalised RGB value which takes in the clear value
    def temp(self):
        return self.sensor.color_temperature #returns the the heat of the color in kelvin
    def lux(self):
        return self.sensor.lux # light intensity


while True:
    color_sensor = RGB()  # Initiates the class for the color sensor
    RGB_values = color_sensor.rgb_values()  # Gets the normalized RGB values
    Neo[0] = RGB_values  # Sends the normalized rgb values to the NeoPixel