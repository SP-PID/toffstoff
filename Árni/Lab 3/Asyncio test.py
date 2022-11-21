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

displayio.release_displays()
i2c = board.I2C()  # uses board.SCL and board.SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 64

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

splash = displayio.Group()
display.show(splash)

#pin = digitalio.DigitalInOut(board.LED)

Rswitch = digitalio.DigitalInOut(board.D2)
Rswitch.direction = digitalio.Direction.INPUT
Rswitch.pull = digitalio.Pull.UP

class Enable:
    def __init__(self,value = True):
        self.value = value


async def button(pin,enable):
    while True:
        if pin.value == False:
            if enable.value:
                print("Disable")
                enable.value = False
            else:
                print("Enable")
                enable.value = True
            while pin.value == False:
                await asyncio.sleep(0.01)
        await asyncio.sleep(0.1)



async def led(pin,enable):
    with digitalio.DigitalInOut(pin) as led:
        led.switch_to_output()
        while True:
            if enable.value == True:
                led.value = not led.value
                await asyncio.sleep(0.1)
            else:
                led.value = False
                await asyncio.sleep(0.01)


async def main():
    enable = Enable()
    button_task = asyncio.create_task(button(Rswitch,enable))
    led_task = asyncio.create_task(led(board.LED,enable))

    await asyncio.gather(button_task,led_task)  # Don't forget "await"!

    print("done")


asyncio.run(main())