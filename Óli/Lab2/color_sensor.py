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
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
# Initialize the MPL3115A2.



while True:
        # Make the display context
    if signal_in.value >35000:
        print("obstacle")
        time.sleep(0.1)
    else:
        print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
        time.sleep(0.1)
