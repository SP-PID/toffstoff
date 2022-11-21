import board
import digitalio
import analogio
import simpleio
import time
import neopixel
from rainbowio import colorwheel
import adafruit_mpl3115a2
i2c = board.I2C()

Min = 20
Max = 25

sensor = adafruit_mpl3115a2.MPL3115A2(i2c)

rgbled = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgbled.brightness = 0.1


while True:
    temp = sensor.temperature

    print((temp,))

    if temp < Min:
        rgbled[0] = (0,0,255)

    elif temp > Max:
        rgbled[0] = (255,0,0)

    else:
        rgbled[0] = (255,0,255)


    time.sleep(0.05)