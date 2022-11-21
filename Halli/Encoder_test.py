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
motor_Bin1 = PWMOut(board.D10,frequency = 50)
motor_Bin2 = PWMOut(board.D11,frequency = 50)
motor_b = Motor.DCMotor(motor_Bin1,motor_Bin2)
encA = rotaryio.IncrementalEncoder(board.D8,board.D9)
encB = rotaryio.IncrementalEncoder(board.D7,board.D6)
diameter = 4.5 # cm
circumference = diameter * 3.14159265359

def get_enc_value():
    global circumference
    motor_a.throttle = 1
    motor_b.throttle = 1
    start_time = 0
    start_time = time.time()
    actual_end_time = 0
    end_time = start_time + 10
    count = 0
    while True:
        #time.sleep(0.01)
        time_now = time.time()
        if  time_now > end_time:
            actual_end_time = time_now
            break
        if encA.position > 730:
            count = count + 1
            encA.position = 0
            encB.position = 0
    motor_a.throttle = 0
    motor_b.throttle = 0     
    print()
    #print("Start time: " + str(start_time) + " End time: " + str(end_time))
    #print("Actual end time: " + str(actual_end_time))
    difference = actual_end_time-start_time
    print("Ran for: " + str(difference) + " Seconds")
    print("Tyre spins: " + str(count))
    distance = (count * circumference) * 0.01
    print("Distance: " + str(distance) + " m")
    speed = distance / difference # 
    print("Speed: " + str(speed) + " m/s")
    #time.sleep(0.1)
    print()

motor_a.throttle = 0
motor_b.throttle = 0
time.sleep(2)
encA.position = 0
encB.position = 0
#while True:
#get_enc_value()
