import rotaryio
import pwmio
import digitalio
import time
import simpleio
import board
from adafruit_motor import motor as Motor

class PID:
    def __init__(self):
        self.kp = 5
        self.ki = 1
        self.kd = 0.0000001
        self.time = 0
        self.old_time = 0
        self.eprew = 0
        self.eintegral = 0

    def regulate(self,target,pos):
        self.time = time.monotonic()
        time_delta = self.time - self.old_time / 1000000
        self.old_time = self.time
        
        e = pos - target

        dedt = (e - self.eprew)/(time_delta)

        self.eintegral = self.eintegral + (e * time_delta)
        
        u = self.kp*e + self.ki*self.eintegral + self.kd*dedt
        self.eprew = e
        #print((e,self.eintegral,dedt,u,))
        if u > 255:
            return 255
        elif u < -255:
            return -255
        else:
            return u

    def set_p(self,value):
        self.kp = value

    def set_i(self,value):
        self.ki = value

    def set_d(self,value):
        self.kd= value


enc = rotaryio.IncrementalEncoder(board.D3,board.D4)
motor_in1 = pwmio.PWMOut(board.D5,frequency = 500)
motor_in2 = pwmio.PWMOut(board.D6,frequency = 500)
motor = Motor.DCMotor(motor_in1,motor_in2)
pid = PID()
while True:
    pos = enc.position
    test = pid.regulate(1000,pos)
    motor.throttle = test / 255
    #print((pos,test,))
    time.sleep(0.01)