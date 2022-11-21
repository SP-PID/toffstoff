# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, and some white text.
"""

import time
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_mpl3115a2
import neopixel
from rainbowio import colorwheel

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=62)

# Initialize the MPL3115A2.
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
# Alternatively you can specify a different I2C address for the device:
# sensor = adafruit_mpl3115a2.MPL3115A2(i2c, address=0x10)

# You can configure the pressure at sealevel to get better altitude estimates.
# This value has to be looked up from your local weather forecast or meteorological
# reports.  It will change day by day and even hour by hour with weather
# changes.  Remember altitude estimation from barometric pressure is not exact!
# Set this to a value in pascals:
sensor.sealevel_pressure = 101011


Min = 20
Max = 26
neopix = neopixel.NeoPixel(board.NEOPIXEL,1)
neopix.brightness = 1

while True:
    # Make the display context
    splash = displayio.Group()
    
    #altitude
    altitude = sensor.altitude
    text_altitude = "Altitude: {0:0.3f}m".format(altitude)
    text_area_altitude = label.Label(terminalio.FONT, text=text_altitude, color=0xFFFF00, x=20, y=18)
    splash.append(text_area_altitude)
    # Temperature
    #temperature = sensor.temperature
    #text = "Temp: {0:0.3f} °C".format(temperature)
    #text_area_temp = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=8)
    #splash.append(text_area_temp)
    
    #pressure
    pressure = sensor.pressure
    text_pressure = "Pressure: {0:0.8f}p".format(pressure)
    text_area_pressure = label.Label(terminalio.FONT, text=text_pressure, color=0xFFFF00, x=20, y=28)
    splash.append(text_area_pressure)
    
    display.show(splash)
    
    
    #if temperature > Max:
    #    neopix[0] = (255,0,0)
    #elif temperature < Min:
    #   neopix[0] = (0,0,255)
    #else:
    #    neopix[0] = (255,0,255)
    #pass
