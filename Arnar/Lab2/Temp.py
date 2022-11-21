import board
import adafruit_mpl3115a2
import digitalio
import time
import neopixel
from rainbowio import colorwheel
neopix = neopixel.NeoPixel(board.NEOPIXEL,1)
neopix.brightness = 1
i2c = board.I2C()
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
sensor.sealevel_pressure = 103040
Min = 20
Max = 26
while True:
    temperature = sensor.temperature
    
    print(temperature)
    if temperature > Max:
        neopix[0] = (255,0,0)
        time.sleep(0.1)
        neopix[0] = (0,0,0)
    elif temperature < Min:
       neopix[0] = (0,0,255)
       time.sleep(0.1)
       neopix[0] = (0,0,0)
    else:
        neopix[0] = (255,0,255)
        
    print('Temperature: {0:0.3f} degrees Celsius'.format(sensor.temperature))