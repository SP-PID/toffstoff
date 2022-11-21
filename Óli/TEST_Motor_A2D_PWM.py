import rotaryio
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from pwmio import PWMOut
from adafruit_motor import motor as Motor
import analogio
import math
import ulab.numpy as np
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306


displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.show(splash)

# function to write text to the LED-screen
def text_to_disp(text, xpos, ypos, scale):
    text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale=scale)
    splash.append(text_area)
    return

# define the motors and frequency they run on
motor_Ain1 = PWMOut(board.D10, frequency=50)
motor_Ain2 = PWMOut(board.D11, frequency=50)
motor_a = Motor.DCMotor(motor_Ain1, motor_Ain2)
motor_Bin1 = PWMOut(board.D8, frequency=50)
motor_Bin2 = PWMOut(board.D9, frequency=50)
motor_b = Motor.DCMotor(motor_Bin1, motor_Bin2)


DEBUG = True  # mode of operation; False = normal, True = debug
OP_DURATION = 5  # operation duration in seconds

def encoder(enc, A_or_B):
    motor_rad = 0.02244085
    delta_time = 0
    angular_velocity = 0
    delta_angle = 0

    while True:
        pos1 = potknob1.value // 256  # make 0-255 range
        motor_a.throttle = pos1 / 255

        pos2 = potknob2.value // 256  # make 0-255 range
        motor_b.throttle = pos2 / 255
        # print(pos1,pos2)
        # print(enc)
        now = time.monotonic()
        ticks = get_enc_value(A_or_B)
        angle = ticks * (2 * np.pi / 700)
        # print(angle)
        time.sleep(0.5)
        
        now = time.monotonic()              # Get first time value
        ticks = get_enc_value(A_or_B)       # get first encoder value
        angle = ticks * (2 * np.pi / 700)   # calculate the angle 
        time.sleep(0.5)                     # delay to get next value 
        delta_time = now - time.monotonic() # get time duration 
        ticks = get_enc_value(A_or_B)       # get second encoder value 
        delta_angle = angle - (ticks * (2 * math.pi / 700)) 
        angular_velocity = delta_angle / delta_time
        linear_velocity = motor_rad * angular_velocity
        # print('Angular velocity: {}'.format(angular_velocity))
        # print('Linear velocity: {}'.format(linear_velocity))
        return angular_velocity, linear_velocity



# function that calls for the value of the encoder, A_or_B selects which encoder to read of 
def get_enc_value(A_or_B):
    if A_or_B == "A":
        enc = encA.position
    elif A_or_B == "B":
        enc = encB.position
    return enc
    
encA = rotaryio.IncrementalEncoder(board.D6, board.D7)
encB = rotaryio.IncrementalEncoder(board.D4, board.D5)

potknob1 = analogio.AnalogIn(board.A1)
potknob2 = analogio.AnalogIn(board.A2)

while True:
    # sleep(100)
    splash = displayio.Group()
    A = "A"
    B = "B"
    angular_velocityA, linear_velocityA = encoder(encA.position, A)     # get angular and linear velocity on encoder A
    angular_velocityB, linear_velocityB = encoder(encB.position, B)     # get angular and linear velocity on encoder B

    text_to_disp("ang vel a: {0:0.4f}".format(angular_velocityA), 0, 15, 1)
    text_to_disp("lin vel a: {0:0.4f}".format(linear_velocityA), 0, 25, 1)
    text_to_disp("ang vel b: {0:0.4f}".format(angular_velocityB), 0, 35, 1)
    text_to_disp("lin vel b: {0:0.4f}".format(linear_velocityB), 0, 45, 1)
    display.show(splash)
    # basic_operations()
    # ramping_speed()
