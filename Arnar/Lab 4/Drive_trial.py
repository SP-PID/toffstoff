import rotaryio
from time import sleep
import board
from digitalio import DigitalInOut, Direction, Pull
from pwmio import PWMOut
from adafruit_motor import motor as Motor
import countio


class motors:
    def __init__(self,pwm,frequency):
        pwm_high = DigitalInOut(board.pwm)
        self.frequency = frequency
        pwm_high.direction = Direction.OUTPUT
        pwm_high.value = True
    def driver_input(self,A1,A2):
        self.A1 = PWMOut(board.A1,self.frequency)
        self.A2 = PWMOut(board.A2,self.frequency)
        Motor.DCMotor(self.A1,self.A2)


motor_Ain1 = PWMOut(board.D11,frequency = 50)
motor_Ain2 = PWMOut(board.D12,frequency = 50)
motor_Bin1 = PWMOut(board.D2,frequency = 50)
motor_Bin2 = PWMOut(board.D3,frequency = 50)

motor_driver_stb = DigitalInOut(board.D5)
pwm_high = DigitalInOut(board.D13)

motor_a = Motor.DCMotor(motor_Ain1, motor_Ain2)
motor_b = Motor.DCMotor(motor_Bin1, motor_Bin2)
pwm_high.direction = Direction.OUTPUT
pwm_high.value = True

DEBUG = True  # mode of operation; False = normal, True = debug
OP_DURATION = 5  # operation duration in seconds

def ramp_up(motor, direction, duration):
    for speed in [x * 0.01 for x in range(0, 101)]:  # 0.0 to 1.0
        motor.throttle = speed if direction == "forward" else -speed
        sleep(duration / 100)

def ramp_down(motor, direction, duration):
    for speed in [x * 0.01 for x in reversed(range(0, 101))]:  # 1.0 to 0.0
        motor.throttle = speed if direction == "forward" else -speed
        sleep(duration / 100)


def ramping_speed():
    ramp_up(motor_a, "forward", OP_DURATION)
    ramp_down(motor_a, "forward", OP_DURATION)

def print_motor_status(motor):
    if motor == motor_a:
        motor_name = "A"
    elif motor == motor_b:
        motor_name = "B"
    else:
        motor_name = "Unknown"
    print(f"Motor {motor_name} throttle is set to {motor.throttle}.")

def basic_operations():
    # Drive forward at full throttle
    motor_a.throttle = 1.0
    motor_b.throttle = 1.0
    if DEBUG: print_motor_status(motor_a)
    sleep(OP_DURATION)
    # Coast to a stop
    motor_a.throttle = None
    motor_b.throttle = None
    
    if DEBUG: print_motor_status(motor_a)
    sleep(OP_DURATION)
    # Drive backwards at 50% throttle
    motor_a.throttle = -0.5
    motor_b.throttle = -0.5
    if DEBUG: print_motor_status(motor_a)
    sleep(OP_DURATION)
    # Brake to a stop
    motor_a.throttle = 0
    motor_b.throttle = 0
    if DEBUG: print_motor_status(motor_a)
    sleep(OP_DURATION)
motor_driver_stb.direction = Direction.OUTPUT
motor_driver_stb.value = True  # enable (turn on) the motor driver


while True:
    basic_operations()
    # ramping_speed()