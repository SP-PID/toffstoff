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
import asyncio

i2c = board.I2C()  # uses board.SCL and board.SDA

WIDTH = 128
HEIGHT = 64

#pin = digitalio.DigitalInOut(board.LED)

encA = digitalio.DigitalInOut(board.D9)
encA.direction = digitalio.Direction.INPUT
#encA.pull = digitalio.Pull.DOWN

encB = digitalio.DigitalInOut(board.D10)
encB.direction = digitalio.Direction.INPUT
#encB.pull = digitalio.Pull.DOWN

class Screen:
    def __init__(self,i2c=i2c): # Init the class
        displayio.release_displays() # Releases displays
        self.display_bus = displayio.I2CDisplay(i2c, device_address=0x3C) # Sets the I2C bus address
        self.disp = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=64) # initiatiates the screen
        self.splash = displayio.Group() # Clears cache

    def text_to_disp(self,text, xpos, ypos, scale):  # Function to set up the print to screen function
        text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale=scale)
        self.splash.append(text_area) # Sends the text to the screen

    def show(self):
        self.disp.show(self.splash)    #Prints what is in splash on the display

    def clear(self):
        self.splash = displayio.Group()  #Clears cache

class Encoder:
    def __init__(self, pinA, pinB):
        self.encoderA = pinA
        self.encoderB = pinB

    def readA(self):
        return self.encoderA.value

    def readB(self):
        return self.encoderB.value

class Enable:
    def __init__(self,value = 0):
        self.value = value

codi = Encoder(encA,encB)
steps = Enable()
skjar = Screen(i2c)

async def encoder():
    prew_state = codi.readA
    while True:

        prev = codi.readA()
        pulses = 0
        start = time.monotonic_ns()
        while pulses < 15:
            curr = codi.readA()
            if curr != prev:
                pulses += 1
                prev = curr

        stop = time.monotonic_ns()

        interval = stop - start
        print(interval)
        if interval != 0:
            rev_time = interval
            rpm_motor = 60000000000 / rev_time
            rpm_shaft = rpm_motor / 100
            steps.value = rpm_motor
        await asyncio.sleep(0.001)
        #print((time.monotonic() - start)/1000000)


async def disp():
    while True:
        skjar.show()
        skjar.clear()
        skjar.text_to_disp("{0:0.0f}".format(steps.value),0,32,2)

        #print(steps.value)
        await asyncio.sleep(0.01)


async def main():

    encoder_task = asyncio.create_task(encoder())
    Display_task = asyncio.create_task(disp())

    await asyncio.gather(encoder_task,Display_task)  # Don't forget "await"!

    print("done")


asyncio.run(main())
