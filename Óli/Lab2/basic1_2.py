import time
import board
import displayio
import analogio
import simpleio
import terminalio
import neopixel
from rainbowio import colorwheel
import adafruit_mpl3115a2
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_mpl3115a2

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Initialize the MPL3115A2.
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
# Alternatively you can specify a different I2C address for the device:
# sensor = adafruit_mpl3115a2.MPL3115A2(i2c, address=0x10)

# You can configure the pressure at sealevel to get better altitude estimates.
# This value has to be looked up from your local weather forecast or meteorological
# reports.  It will change day by day and even hour by hour with weather
# changes.  Remember altitude estimation from barometric pressure is not exact!
# Set this to a value in pascals:
sensor.sealevel_pressure = 100600

#Define the neopixel
rgbled = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgbled.brightness = 0.1
#maximum and minimum values of temperature
Min = 20
Max = 25


while True:
    # Make the display context
    sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
    splash = displayio.Group()
    color_bitmap = displayio.Bitmap(128, 64, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a label
    altitude = sensor.altitude
    text = "alt: {0:0.1f}".format(altitude)
    temperature = sensor.temperature
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
    pressure = sensor.pressure
    text1 = "Press: {0:0.1f}".format(temperature)
    text_area1 = label.Label(terminalio.FONT, text=text1, color=0xFFFF00, x=28, y=27)
    splash.append(text_area1)
    splash.append(text_area)
    display.show(splash)


    if temperature < Min:
        rgbled[0] = (0,0,255)
    elif temperature > Max:
        rgbled[0] = (255,0,0)
    else:
        rgbled[0] = (255,0,255)

    time.sleep(1.0)
    pass



