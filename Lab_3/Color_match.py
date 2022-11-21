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


    raw_data = sensor.color_raw
    splash = displayio.Group()
    color = sensor.color
    color_rgb = sensor.color_rgb_bytes

    temp = sensor.color_temperature
    lux = sensor.lux

    rgbled[0] = color_rgb
    text =("Red: {0}".format(color_rgb[0]))
    text1 = ("Green: {0}".format(color_rgb[1]))
    text2 = ("Blue: {0}".format(color_rgb[2]))
    text3 = ("Clear: {0}".format(raw_data[3]))
    text_to_disp(text,0,4,1)
    text_to_disp(text1,0,14,1)
    text_to_disp(text2,0,24,1)
    text_to_disp(text3,0,34,1)




    display.show(splash)
