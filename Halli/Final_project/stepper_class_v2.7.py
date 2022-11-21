
#import board
#import adafruit_seesaw
#from adafruit_seesaw import seesaw, rotaryio, digitalio
import time
import board
import digitalio as dg
import threading
from time import sleep, perf_counter
from threading import Thread

pulse = dg.DigitalInOut(board.D23)
pulse.direction = dg.Direction.OUTPUT
direc = dg.DigitalInOut(board.D24)
direc.direction = dg.Direction.OUTPUT
enable = dg.DigitalInOut(board.D18)
enable.direction = dg.Direction.OUTPUT
ms1 = dg.DigitalInOut(board.D20)
ms1.direction = dg.Direction.OUTPUT
ms2 = dg.DigitalInOut(board.D21)
ms2.direction = dg.Direction.OUTPUT
ms1.value = False
ms2.value = False
stop = dg.DigitalInOut(board.D15)
stop.direction = dg.Direction.INPUT
stop.pull = dg.Pull.DOWN

class SetPoint():
    def __init__(self) -> None:
        self.pi = 3.14159265359                                                         # Everybody knows pi
        self.degrees_per_step = 1.8                                                     # for some reason this motor will move 0.225 degrees per step
        self.diameter = 19.65                                                           # diameter in millimeters
        self.total_travel = 820                                                         # total travel of the gantry plate is 800 millimeters
        self.circumference = self.diameter * self.pi                                    # circumference in millimeters
        self.steps_per_revolution = 360 / self.degrees_per_step                         # number of steps in a revolution
        self.distance_per_step = self.circumference / self.steps_per_revolution         # distance per step in millimeters
        self.steps_total = self.total_travel / self.distance_per_step                   # total number of steps per length of travel of gantry plate
        self.rotation = False                                                           # variable for which direction the motor will spin
        self.direction = "up"                                                           # variable to tell program to go up or down
        self.current_position = 0                                                       # initializes in lowest position
        self.distance = 0
        self.step_size = "FULL"
        self.highest_position = int(round(self.steps_total,0))                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position
        self.multiplier = 1
        self.top_reached = False
        self.idle_time = time.time()
        self.driver_enabled = False
        self.idle = False
        #self.reset_actuator()                                                           # actuator finds zero position (bottom)

    def get_current_position(self):
        return self.current_position

    def enable_driver(self):        
        ''' Function that enables Easydriver for use '''
        #print("Driver enabled")
        self.driver_enabled = True
        enable.value = False

    def disable_driver(self):        
        ''' Function that disables Easydriver after use '''
        #print("Driver disabled")
        self.driver_enabled = False
        enable.value = True 

    def pulse(self):
        ''' Function sends out one pulse on pulse pin '''
        pulse.value = True
        time.sleep(0.0007)      # wait
        pulse.value = False
        time.sleep(0.0007)      # wait

    def update_position(self,distance):
        ''' Function keeps track of current position of gantry '''
        if self.direction == "down":
            self.current_position -= distance
        if self.direction == "up":
            self.current_position += distance

    def update_stepping(self):
        if self.step_size == "FULL":
            ms1.value = False
            ms2.value = False         
            self.multiplier = 1
        if self.step_size == "HALF":
            ms1.value = True
            ms2.value = False
            self.multiplier = 2
        if self.step_size == "QUARTER":
            ms1.value = False
            ms2.value = True
            self.multiplier = 4           
        if self.step_size == "EIGHT":
            ms1.value = True
            ms2.value = True
            self.multiplier = 8              
    
    def determine_direction(self,requested_position):
        self.distance = requested_position - self.current_position# - requested_position # If current position is above requested value then positive else negative
        if self.distance < 0:
            self.direction = "down"
        else:
            self.direction = "up"

    def determine_stepping(self):
        if abs(self.distance) > 10:
            self.step_size = "FULL"
        if abs(self.distance) <= 10:
            self.step_size = "HALF"
        if abs(self.distance) == 2:
            self.step_size = "EIGHT"

    def update_rotation(self):
        ''' Function updates variable for gantry travel direction '''
        if self.direction == "up":
            self.rotation = True            # False means actuator moves down
        if self.direction == "down":
            self.rotation = False
        direc.value = self.rotation

    def move(self,position):
        if position > self.highest_position:
            position = self.highest_position
        self.determine_direction(position)      # determines the direction to travel
        self.update_rotation()                  # updates variable
        self.determine_stepping()               # determines step size
        self.update_stepping()
        if abs(self.distance) < 1:
            self.check_idle()
            if self.idle == True:
                if self.driver_enabled:
                    self.disable_driver()
        else:
            if not self.driver_enabled:
                self.enable_driver()
            if self.current_position <= self.highest_position:
                for i in range(0,self.multiplier):
                    self.pulse()
                self.idle_time = time.time()
                self.update_position(1)
                
    def check_idle(self):
        current_pause = int(round(time.time() - self.idle_time,0))
        if current_pause < 5:
            self.idle = False
        else:
            self.idle = True


    def reset_actuator(self):
        ''' Function that moves the gantry to zero position (bottom) '''
        self.update_rotation("down")    # sets travel direction to down
        self.enable_driver()            # enables the driver to move
        while True:
            self.pulse()                # sends out pulses until the button reads high
            if stop.value == True: #GPIO.input(self.button_pin) == GPIO.HIGH: # read a button   
                break                        # break loop when bottom reached
        self.disable_driver()           # driver disabled

actuator = SetPoint()

POS = 0
def task1():
    global POS
    while True:
        actuator.move(POS)

def task2():
    global POS
    while True:
        POS = int(input("Enter new POS: "))
        time.sleep(0.1)


# create two new threads
t1 = Thread(target=task1)
t2 = Thread(target=task2)

# start the threads
t1.start()
t2.start()

# wait for the threads to complete
t1.join()
t2.join()
