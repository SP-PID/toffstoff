import board
import adafruit_fxos8700
import adafruit_fxas21002c
import adafruit_bus_device
import time
import neopixel
import terminalio
import displayio
import adafruit_displayio_ssd1306
from adafruit_display_text import label

i2c = board.I2C()
fxos = adafruit_fxos8700.FXOS8700(i2c)
neopix = neopixel.NeoPixel(board.NEOPIXEL, 1)
neopix.brightness = 1

class Upright:
    def __init__(self) -> None:
        self.falls_to = "Upright"

    def falls_which_way(self,LR, FB, UD):
        ''' Function determines which way the robot is leaning or if it is upside down, changes variable falls_to '''
        # LR is for left and right, FB is for front and back and UD is for up and down
        if UD < 9.5:
            if LR < -1.25:
                self.falls_to = "Left"
                neopix.neopix[0] = (255, 0, 0)
                return
            elif LR > 1.25:
                self.falls_to = "Right"
                neopix.neopix[0] = (255, 0, 0)
                return
            if FB < -1.5:
                self.falls_to = "Backwards"
                neopix.neopix[0] = (255, 0, 0)
                return
            elif FB > 1:
                self.falls_to = "Forward"
                neopix.neopix[0] = (255, 0, 0)
                return
            if UD < 0:
                self.falls_to = "UpsideDown"
                neopix.neopix[0] = (255, 0, 0)
                return
        else:
            self.falls_to = "Upright"
            neopix.neopix[0] = (0, 0, 255)

    def read_accelerometer(self):
        ''' Reads the accelerometer and returns string value '''
        acceleration = fxos.accelerometer
        self.falls_which_way(acceleration[0], acceleration[1], acceleration[2])
        return self.falls_to

is_upright = Upright()
print(is_upright.read_accelerometer())



