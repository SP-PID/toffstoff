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

encA = countio.Counter(board.D10, edge=countio.Edge.RISE)

encB = countio.Counter(board.D9, edge=countio.Edge.RISE)


direction = ""


def text_to_disp(text, xpos, ypos, scale):
    text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale=scale)
    splash.append(text_area)
    return

i = 0
iold = 0

while True:
    splash = displayio.Group()
    tach = encA
    distance = (encA.count*0.2)
    text_to_disp("distance: {0:0.1f} mm".format(distance), 15, 15, 1)
    text_to_disp("{0:0.1f}".format(tach), 25, 15, 1)
    display.show(splash)