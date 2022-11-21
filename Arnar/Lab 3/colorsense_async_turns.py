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
import asyncio





#Defines the NeoPixel
rgbled = neopixel.NeoPixel(board.NEOPIXEL, 1)   
rgbled.brightness = 1 #Sets NeoPixel brightness

displayio.release_displays()  
# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
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
    def __init__(self,time = 10,gain=16,i2c=i2c):
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.sensor.integration_time = time 
        self.sensor.gain = gain
        
    def raw_data(self):
        return self.sensor.color_raw

    def rgb_values(self):
        return self.sensor.color_rgb_bytes
    def temp(self):
        return self.sensor.color_temperature
    def lux(self):
        return self.sensor.lux
    


def text_to_disp(text, xpos, ypos, scale):
    text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale = scale)
    splash.append(text_area)
    return
# Main loop reading color and printing it every second.
red = 0
green = 0
blue = 0

async def led(pin):
    with digitalio.DigitalInOut(pin) as led:
        led.switch_to_output()
        while True:
            led.value = not led.value
            await asyncio.sleep(0.5)
async def colorsense():
    while True:
        color = RGB(2.4,16,i2c)
        clear_value = color.raw_data()
        color_rgb = color.rgb_values()
        
        if clear_value[3] > 250:
            green = 0
            blue = 0
            red = 0
    
        elif color_rgb[0] > color_rgb[1] and color_rgb[0] > color_rgb[2]:
            red = color_rgb[0]
            green = 0
            blue = 0
            red += 60
        elif color_rgb[1] > color_rgb[0] and color_rgb[1] > color_rgb[2]:
            green = color_rgb[1]
            green += 60
            red = 0
            blue = 0
        elif color_rgb[2] > color_rgb[1] and color_rgb[2] > color_rgb[0]:
            blue = color_rgb[2]
            blue += 60
            green = 0
            red = 0
        rgbled[0] = (red,green,blue)
        print("Clear value {0}, RGB value {1}".format(clear_value[3],color_rgb))
        
        await asyncio.sleep(0.01)
    
        



async def main():
    colorsensing = asyncio.create_task(colorsense())
    blink = asyncio.create_task(led(board.LED))
    await asyncio.gather(colorsensing,blink)
    
asyncio.run(main())