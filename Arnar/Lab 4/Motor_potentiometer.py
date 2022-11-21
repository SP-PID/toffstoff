import rotaryio
from time import sleep
import board
from digitalio import DigitalInOut, Direction, Pull
from pwmio import PWMOut
from adafruit_motor import motor as Motor
import countio
import analogio
# class motors:
#     def __init__(self):
#         pwm_high = DigitalInOut(board.D13)
#         pwm_high.direction = Direction.OUTPUT
#         pwm_high.value = True
#     def driver_input(self,A1,A2,freq):
#         self.A1 = PWMOut(A1,frequency = freq)
#         self.A2 = PWMOut(A2,frequency = freq)
#         return self.A1,self.A2


#motor_a=motors()
#motor_a.driver_input(board.D11,board.D12,50)
#motor_b=motors()
#motor_b.driver_input(board.D2,board.D3,50)

motor_Ain1 = PWMOut(board.D10,frequency = 50)
motor_Ain2 = PWMOut(board.D11,frequency = 50)
motor_a = Motor.DCMotor(motor_Ain1,motor_Ain2)
motor_Bin1 = PWMOut(board.D8,frequency = 50)
motor_Bin2 = PWMOut(board.D9,frequency = 50)
motor_b = Motor.DCMotor(motor_Bin1,motor_Bin2)





DEBUG = True  # mode of operation; False = normal, True = debug
OP_DURATION = 5  # operation duration in seconds

def ramp_up(motor, direction, duration):
    for speed in [x * 0.01 for x in range(0, 101)]:  # 0.0 to 1.0
        motor.throttle = speed if direction == "forward" else -speed


def ramp_down(motor, direction, duration):
    for speed in [x * 0.01 for x in reversed(range(0, 101))]:  # 1.0 to 0.0
        motor.throttle = speed if direction == "forward" else -speed



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
    #motor_b.throttle = 1.0
    if DEBUG: print_motor_status(motor_a)
    sleep(OP_DURATION)
    # Coast to a stop
    motor_a.throttle = None
    #motor_b.throttle = None

    if DEBUG: print_motor_status(motor_a)
    sleep(OP_DURATION)
    # Drive backwards at 50% throttle
    motor_a.throttle = -0.5
    #motor_b.throttle = -0.5
    if DEBUG: print_motor_status(motor_a)
    sleep(OP_DURATION)
    # Brake to a stop
    motor_a.throttle = 0
    #motor_b.throttle = 0
    if DEBUG: print_motor_status(motor_a)
    sleep(OP_DURATION)

def potentiometer():
    position1 = potknob1.value  # ranges from 0-65535
    pos1 = potknob1.value // 256  # make 0-255 range
    motor_a.throttle= pos1/255
   
    position2 = potknob2.value  # ranges from 0-65535
    pos2 = potknob2.value // 256  # make 0-255 range
    motor_b.throttle= pos2/255
    print(pos1,pos2)
    position5 = encoder()


def encoder():
    position4 = enc.position
    return position4
enc = rotaryio.IncrementalEncoder(board.D6,board.D7)
potknob1 = analogio.AnalogIn(board.A1)

potknob2 = analogio.AnalogIn(board.A2)

while True:
    #sleep(100)
    potentiometer()
    
    #basic_operations()
    #ramping_speed()
