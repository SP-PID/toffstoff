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


class Drive:
    def __init__(self) -> None:
        self.motor_Ain1 = PWMOut(board.D11,frequency = 50)
        self.motor_Ain2 = PWMOut(board.D12,frequency = 50)
        self.motor_Bin1 = PWMOut(board.D8,frequency = 50)
        self.motor_Bin2 = PWMOut(board.D9,frequency = 50)
        self.motor_a = Motor.DCMotor(self.motor_Ain1,self.motor_Ain2)
        self.motor_b = Motor.DCMotor(self.motor_Bin1,self.motor_Bin2)
        self.potknob1 = analogio.AnalogIn(board.A1)
        self.potknob2 = analogio.AnalogIn(board.A2)
        self.encA = rotaryio.IncrementalEncoder(board.D6,board.D7)
        self.encB = rotaryio.IncrementalEncoder(board.D4,board.D5)
        self.robot_drive = Drive()

    def pwm_sense(self):
        pot1 = self.potknob1.value // 256
        pot2 = self.potknob2.value // 256
        return pot1, pot2

    def throttle(self, PwmA, PwmB, direction):
        if direction == "FWD":
            self.motor_a.throttle = PwmA/255
            self.motor_b.throttle = PwmB/255
        elif direction == "REV":
            self.motor_a.throttle = -(PwmA/255)
            self.motor_b.throttle = -(PwmB/255)
        else:
            self.motor_a.throttle = 0
            self.motor_b.throttle = 0


def drive(self):                                                    # function will be used to command robot to drive
        robot_drive.throttle(255, 255, "FWD")
        time.sleep(2)
        self.robot_drive.throttle(0, 0, "FWD")


while True:
    Drive()
    

