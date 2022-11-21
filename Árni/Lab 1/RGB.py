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

R_in = analogio.AnalogIn(board.A1)
G_in = analogio.AnalogIn(board.A2)
B_in = analogio.AnalogIn(board.A3)

rgbled.brightness = 0.4

while True:
    time.sleep(0.05)
    Red = simpleio.map_range(R_in.value,0,65520,0,255)
    Blue = simpleio.map_range(G_in.value,0,65520,0,255)
    Green = simpleio.map_range(B_in.value,0,65520,0,255)
    print((Red,Blue,Green))

    rgbled[0] = (Red, Blue, Green)

