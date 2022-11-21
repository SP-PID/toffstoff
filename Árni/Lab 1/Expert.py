import board
import digitalio
import analogio
import simpleio
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

signal_in = analogio.AnalogIn(board.A1)
pot_in = analogio.AnalogIn(board.A2)

rgbled.fill(colorwheel(0))

while True:
    time.sleep(0.1)
    color = signal_in.value/255
    bright = simpleio.map_range(pot_in.value,0,65520,0.007,1)
    print((bright,color,))
    rgbled.brightness = bright
    rgbled.fill(colorwheel(color))

