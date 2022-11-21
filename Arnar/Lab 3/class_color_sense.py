
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
class RGB: # class to be able to call on the rgb sensor
    def __init__(self,time = 10,gain=16,i2c=i2c):
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.sensor.integration_time = time 
        self.sensor.gain = gain
        
    def raw_data(self):
        return self.sensor.color_raw #returns the raw values, we use clear value

    def rgb_values(self):
        return self.sensor.color_rgb_bytes # Gives us normalised RGB value which takes in the clear value
    def temp(self):
        return self.sensor.color_temperature #returns the the heat of the color in kelvin
    def lux(self):
        return self.sensor.lux # light intensity
    
EMG_switch = digitalio.DigitalInOut(board.D2)
EMG_switch.direction = digitalio.Direction.INPUT
EMG_switch.pull = digitalio.Pull.UP

class Enable:
    def __init__(self,value = True):
        self.value = value


def text_to_disp(text, xpos, ypos, scale):
    text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale = scale)
    splash.append(text_area)
    return

async def EMG_stop(pin,enable):
    while True:
        if pin.value == False:
            if enable.value:
                print("Disable")
                #enable.value = False
                mode.value = "Start"
            else:
                print("Enable")
                enable.value = True
            while pin.value == False:
                await asyncio.sleep(0.01)
        await asyncio.sleep(0.1)


async def led(pin):# Creating async function this was to see both of it running at the same time
    with digitalio.DigitalInOut(pin) as led:
        led.switch_to_output()
        while enable.value and mode.value == "led":
            led.value = not led.value
            await asyncio.sleep(0.5)


async def colorsense(): # Creating async function
    while True:
        while mode.value == 1:
            color = RGB(10,16,i2c)
            raw_value = color.raw_data() # Making a variable which has the raw data
            color_rgb = color.rgb_values() # Takes the normilised RGB value
            rgbled[0] = color_rgb # Sends the RGB value to the NeoPixel
            print("Clear value {0}, RGB value {1}".format(raw_value[3],color_rgb))# Prints out the clear and RGB values for visual aid for calibration
            await asyncio.sleep(0.01)# Sleep time so other async functions can work 
    
        



async def main():
    enable =Enable()
    colorsensing = asyncio.create_task(colorsense())# Creating the async task for the colorsensor
    blink = asyncio.create_task(led(board.LED)) # creating the async blink task
    EMG_task = asyncio.create_task(EMG_stop(EMG_switch,enable))
    await asyncio.gather(colorsensing,blink,EMG_task) # Gets information from the tasks
    
asyncio.run(main())# Runs the async main 