import time
import board
import adafruit_fxos8700
import math

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_fxos8700.FXOS8700(i2c)

def angle():
    # Read acceleration & magnetometer.
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer

    # calculate angular position
    x2 = math.pow(accel_x, 2)
    y2 = math.pow(accel_y, 2)
    z2 = math.pow(accel_z, 2)

    # angular position for x-axis
    result = math.sqrt(y2+z2)
    divx = accel_x/result
    roll = math.atan(divx)*(180/math.pi)
    # angular position for y-axis
    result = math.sqrt(x2+z2)
    divy = accel_y/result
    pitch = math.atan(divy)*(180/math.pi)
    # angular position for z-axis
    result = math.sqrt(x2+y2)
    divz = accel_z/result
    yaw = math.atan(divz)*(180/math.pi)
    return roll, pitch, yaw


while True:
    roll, pitch, yaw, = angle()
    #if -80 < roll > 40:
    if roll < -80:
        print("Right")
    elif roll > 40:
        print("Left")
    else:
        print("OK")
    # Delay for a second.
    time.sleep(1.0)