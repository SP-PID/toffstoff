import rotaryio
import time
import board
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
from pwmio import PWMOut
from adafruit_motor import motor as Motor
import countio
import analogio
import simpleio
import math


i2c = board.I2C()
motor_Ain1 = PWMOut(board.D12,frequency = 50)
motor_Ain2 = PWMOut(board.D11,frequency = 50)
motor_Bin1 = PWMOut(board.D8,frequency = 50)
motor_Bin2 = PWMOut(board.D9,frequency = 50)
motor_a = Motor.DCMotor(motor_Ain1,motor_Ain2)
motor_b = Motor.DCMotor(motor_Bin1,motor_Bin2)
potknob1 = analogio.AnalogIn(board.A1)
potknob2 = analogio.AnalogIn(board.A2)
encA = rotaryio.IncrementalEncoder(board.D6,board.D7)
encB = rotaryio.IncrementalEncoder(board.D4,board.D5)



def get_enc_value(A_or_B):
    if A_or_B == "A":
        enc = encA.position
    elif A_or_B == "B":
        enc = encB.position
    return enc


def pwm_sense():
    pot1= potknob1.value // 256
    pot2 = potknob2.value // 256
    return pot1, pot2
    
def throttle(PwmA,PwmB,direction): 
    if direction == "FWD":
        motor_a.throttle = PwmA/255
        motor_b.throttle = PwmB/255
        print(motor_a.throttle, motor_b.throttle)
    elif direction == "REV":
        motor_a.throttle = -(PwmA/255)
        print(motor_a.throttle)
        motor_b.throttle = -(PwmB/255)
    else:
        motor_a.throttle = 0
        motor_b.throttle = 0

def DRV_OL_FW():
    dist1 = 0
    dist2 = 0
    while dist1 < 1000 and dist2 < 1000:
        dist1 = encA.position * 0.22
        dist2 = encB.position * 0.22
        print(dist1)
        throttle(255,255,"FWD")
    throttle(0,0,0)

DRV_OL_FW()
