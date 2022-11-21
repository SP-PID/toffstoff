import board
import analogio
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
text = "Temp:"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
splash.append(text_area)
splash.append(text_area)
################################################################################################

while True:
        # Make the display context
    if signal_in.value >35000:
        text = "obstacle"
        time.sleep(0.1)
    else:
        text = 'Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes)
        time.sleep(0.1)

