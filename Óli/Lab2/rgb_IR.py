import board
import analogio
import simpleio
import time
import math
import adafruit_tcs34725

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)
signal_in = analogio.AnalogIn(board.A2)
color = sensor.color
color_rgb = sensor.color_rgb_bytes

while True:
    print((signal_in.value,))
