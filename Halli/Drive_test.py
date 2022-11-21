import rotaryio
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from pwmio import PWMOut
from adafruit_motor import motor as Motor
import countio
import analogio
import math
import ulab.numpy as np

motor_Ain1 = PWMOut(board.D12,frequency = 50)
motor_Ain2 = PWMOut(board.D13,frequency = 50)
motor_a = Motor.DCMotor(motor_Ain1,motor_Ain2)
# motor_c = Motor.
motor_Bin1 = PWMOut(board.D10,frequency = 50)
motor_Bin2 = PWMOut(board.D11,frequency = 50)
motor_b = Motor.DCMotor(motor_Bin1,motor_Bin2)
encA = rotaryio.IncrementalEncoder(board.D8,board.D9)
encB = rotaryio.IncrementalEncoder(board.D7,board.D6) 
DEBUG = True
OP_DURATION = 0.5  # operation duration in seconds

class Conf():
    def __init__(self):
        self.wheel_dia = 22
        self.ramp = 125
        self.FW_test_dist = 1000
        self.break_dist = 300
        self.follow = 500
        self.ramp_time = 1
        self.test_dur = 5
        self.i2c = board.I2C()


def ramp_up(motor, direction):
    for speed in [x * 0.01 for x in range(0, 101)]:  # 0.0 to 1.0
        motor.throttle = speed if direction == "forward" else -speed

def ramp_down(motor, direction):
    for speed in [x * 0.01 for x in reversed(range(0, 101))]:  # 1.0 to 0.0
        motor.throttle = speed if direction == "forward" else -speed


def ramp_up_2(direction, increments = 0.08):
    duration = int(1/increments) 
    for speed in [x * increments for x in range(1, duration)]:
        motor_a.throttle = speed if direction == "forward" else -speed
        motor_b.throttle = speed if direction == "forward" else -speed

def ramp_down_2(direction, increments = 0.08):
    duration = int(1/increments) 
    #print(increments)
    for speed in [x * increments for x in reversed(range(1, duration))]:
        motor_a.throttle = speed if direction == "forward" else -speed
        motor_b.throttle = speed if direction == "forward" else -speed

def turn_around(direction, increments = 0.08):
    duration = int(1/increments) 
    print(increments)
    for speed in [x * increments for x in range(1, duration)]:
        motor_a.throttle = -speed if direction == "right" else speed
        motor_b.throttle = speed if direction == "right" else -speed    
    
    for speed in [x * increments for x in reversed(range(1, duration))]:
        motor_a.throttle = -speed if direction == "right" else speed
        motor_b.throttle = speed if direction == "right" else -speed

def how_fast(speed):
    if speed == "Fast":
        return 0.5
    elif speed == "Medium":
        return 0.07
    elif speed == "Slow":
        return 0.02
    else:
        return 0.01

def velocity():
    motor_radius = config.wheel_dia
    motor_rad = motor_radius/1000
    delta_time = 0
    angular_velocity1 = 0
    angular_velocity2 = 0
    delta_angle = 0
    now = time.monotonic()
    ticks1 = encA.position
    ticks2 = encB.position
    angle1 = ticks1 * (2 * math.pi / 700)
    angle2 = ticks2 * (2 * math.pi / 700)
    time.sleep(0.1)
    ticks1 = encA.position
    ticks2 = encB.position
    delta_time = now - time.monotonic()
    delta_angle1 = angle1 - (ticks1 * (2 * math.pi / 700))
    delta_angle2 = angle2 - (ticks2 * (2 * math.pi / 700))
    if delta_time > 0:
        angular_velocity1 = delta_angle1 / delta_time
        angular_velocity2 = delta_angle2 / delta_time
    linear_velocity1 = motor_rad * angular_velocity1
    linear_velocity2 = motor_rad * angular_velocity2
    return angular_velocity1, linear_velocity1,angular_velocity2, linear_velocity2

def basic_operations():
    increments = how_fast("Fast")
    ramp_up_2("forward",increments)
    print("Full speed")
    time.sleep(1)
    print("Ramping down")
    ramp_down_2("forward",increments)
    print("Turning around")
    turn_around("right",increments)  

def forward(robot_speed="Fast"):
    increments = how_fast(robot_speed)
    ramp_up_2("forward",increments)
    print("Full speed")

def stop(robot_speed="Fast"):
    increments = how_fast(robot_speed)
    ramp_down_2("forward",increments)
    motor_a.throttle = 0
    motor_b.throttle = 0    

def get_enc_value():
    for i in range(0,10):
        print("Velocity: " + str(velocity()))
        time.sleep(1)
        
config = Conf()        
while True:
    question = input("Try again?(y/n) ")
    if question == "y":
        forward()
        get_enc_value()
        stop()
    else:
        pass





