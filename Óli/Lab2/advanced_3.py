import board
import analogio
import simpleio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_mpl3115a2
import time
import math
import adafruit_tcs34725

displayio.release_displays()
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)
signal_in = analogio.AnalogIn(board.A2)
color = sensor.color
color_rgb = sensor.color_rgb_bytes
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

####################################################################
# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
sensor.gain = 4


WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)
# Draw a label

while True:
    splash = displayio.Group()
    if 10 < sensor.color_raw[0] < 20 and 0 < sensor.color_raw[1] < 5 and 0 < sensor.color_raw[2] < 5:
        text = "left"
        time.sleep(0.1)
    elif 0 < sensor.color_raw[0] < 6 and 3 < sensor.color_raw[1] < 10 and 0 < sensor.color_raw[2] < 10 and sensor.color_raw[3] < 15:
        text = "Center"
        time.sleep(0.1)
    elif 0 < sensor.color_raw[0] < 6 and 3 < sensor.color_raw[1] < 10 and 0 < sensor.color_raw[2] < 10 and sensor.color_raw[3] > 15:
        text = "Right"
    else:
        text = "Unknown"

    text_area = label.Label(terminalio.FONT, text=text, x=15, y=15)
    splash.append(text_area)
    distance = simpleio.map_range(signal_in.value, 18000, 46000, 65, 20)
    text = "distance {0:0.2f}".format(distance)
    text_area = label.Label(terminalio.FONT, text=text, x=15, y=25)
    splash.append(text_area)
    if distance < 36:
        text = "OBSTACLE"
        text_area = label.Label(terminalio.FONT, text=text, x=15, y=40, scale = 2)
        splash.append(text_area)
    display.show(splash)
    time.sleep(0.1)
