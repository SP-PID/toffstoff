import board
import adafruit_mpl3115a2
import time
i2c = board.I2C()

while True:
    sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
    print('Pressure: {0:0.3f} pascals'.format(sensor.pressure))
    time.sleep(1)
    print('Altitude: {0:0.3f} meters'.format(sensor.altitude))
    time.sleep(1)
    print('Temperature: {0:0.3f} degrees Celsius'.format(sensor.temperature))
    time.sleep(1)
    