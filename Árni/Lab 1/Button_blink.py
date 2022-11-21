import board
import digitalio
import time
import neopixel


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

rgbled = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgbled.brightness = 1

Rswitch = digitalio.DigitalInOut(board.D2)
Rswitch.direction = digitalio.Direction.INPUT
Rswitch.pull = digitalio.Pull.UP

Gswitch = digitalio.DigitalInOut(board.D3)
Gswitch.direction = digitalio.Direction.INPUT
Gswitch.pull = digitalio.Pull.UP

while True:
    if Rswitch.value == False:
        print("Red is pressed")
        rgbled[0] = (255, 0, 0)
    
    if Gswitch.value == False:
        print("Green is pressed")
        rgbled[0] = (0, 255, 0)
    
    else:
        rgbled[0] = (0, 0, 0)
