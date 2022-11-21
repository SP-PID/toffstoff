import board
import countio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import time

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.show(splash)

# counts rising edges on the encoder
encA = countio.Counter(board.D10, edge=countio.Edge.RISE)
encB = countio.Counter(board.D9, edge=countio.Edge.RISE)

# function to write text to the LED-screen
def text_to_disp(text, xpos, ypos, scale):
    text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale=scale)
    splash.append(text_area)
    return

while True:
    splash = displayio.Group()      # create the screen environment
    increment = encA.count          # increment reader
    distance = (encA.count*0.2)     # distance traveled (143.3/700 = 0.2)
    text_to_disp("distance: {0:0.1f} mm".format(distance), 15, 15, 1)
    text_to_disp("increment: {0:0.1f}".format(increment), 15, 25, 1)
    display.show(splash)