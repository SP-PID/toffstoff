import board
import digitalio
import time
import neopixel
from rainbowio import colorwheel

i = 0
x = 0.1
delay = 0.1
n = 0.1
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

rgbled = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgbled.brightness = x

Rswitch = digitalio.DigitalInOut(board.D2)
Rswitch.direction = digitalio.Direction.INPUT
Rswitch.pull = digitalio.Pull.UP

Gswitch = digitalio.DigitalInOut(board.D3)
Gswitch.direction = digitalio.Direction.INPUT
Gswitch.pull = digitalio.Pull.UP

FuncIn = digitalio.DigitalInOut(board.D4)
FuncIn.direction = digitalio.Direction.INPUT
FuncIn.pull = digitalio.Pull.DOWN


rgbled.fill(colorwheel(0))

while True:
    if Rswitch.value == False:
        #print("Red is pressed")
        i = (i + 50) % 256  # run from 0 to 255
        print("Color:", i, "Brightness", x)
        while Rswitch.value == False:
            rgbled.brightness = x
        rgbled.fill(colorwheel(i))


    elif Gswitch.value == False:
        #print("Green is pressed")
        x = (x + 0.1) % 0.3
        print("Color:", i, "Brightness", x)
        while Gswitch.value == False:
            rgbled.brightness = x



    if FuncIn.value == True:
        rgbled.brightness = 1
    else:
        rgbled.brightness = 0
