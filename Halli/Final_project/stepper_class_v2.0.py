#!usr/bin/python

# This has to be somewhere in the code
import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BOARD)    # Setup of GPIO´s
GPIO.setwarnings(False)     # Don´t need no negativity in my life
GPIO.setup(16, GPIO.OUT)    # pins 12, 16 and 18 are used as outputs
GPIO.setup(18, GPIO.OUT)    # pin 18 is direction
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, True)       # pin 12 is high
# -------------------------------------------------------------------


class SetPoint():
    def __init__(self) -> None:
        self.pi = 3.14159265359                                                         # Everybody knows pi
        self.degrees_per_step = 0.225                                                   # for some reason this motor will move 0.225 degrees per step
        self.diameter = 50                                                              # diameter in millimeters
        self.total_travel = 800                                                         # total travel of the gantry plate is 800 millimeters             
        self.circumference = self.diameter * self.pi                                    # circumference in millimeters
        self.rotations = self.total_travel / self.circumference                         # total number of rotations (DELETE)
        self.steps_per_revolution = 360 / self.degrees_per_step                         # number of steps in a revolution
        self.distance_per_step = self.circumference / self.steps_per_revolution         # distance per step in millimeters
        self.steps_total = self.total_travel / self.distance_per_step                   # total number of steps per length of travel of gantry plate
        self.rotation = False                                                           # variable for which direction the motor will spin
        self.direction = "up"                                                           # variable to tell program to go up or down
        self.current_position = 0                                                       # initializes in lowest position
        self.highest_position = self.steps_total                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position


    def enable_driver(self):        # Function that enables the driver to run
        ''' Function that enables Easydriver for use '''
        GPIO.output(12, False)  # the motor

    def disable_driver(self):       # Function that prevents the driver from 
        ''' Function that disables Easydriver after use '''
        GPIO.output(12, True)   # moving the motor

    def steps(self,distance):
        ''' Function calculates steps to move '''
        return int(round(distance/self.distance_per_step,0))

    def update_rotation(self,direction):
        self.direction = direction
        if self.direction == "up":
            self.rotation = False            # False means actuator moves up
        if self.direction == "down":
            self.rotation = True
        GPIO.output(18, self.rotation)

    def return_position(self):
        return int(round(self.current_position*self.distance_per_step,0))

    def update_position(self,distance):
        if self.direction == "down":
            self.current_position -= distance
        if self.direction == "up":
            self.current_position += distance

    def move_to_position(self,position):
        dist = self.current_position - position # checks if the new position is above or below current position
        if dist < 0:
            self.update_rotation("down")
            dist = -dist
        if dist > 0:
            self.update_rotation("up")
        else:
            return                              # do nothing
        steps = self.steps(dist)                # check how many steps to new position
        self.spin_motor(steps)
        
    # ATH MEÐ MS1 og MS2 er örugglega að nota microstepping!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def spin_motor(self,steps):
        self.enable_driver()
        for i in range(0, steps):
            GPIO.output(16, True)   # output pin 16 high
            time.sleep(0.00005)      # wait
            GPIO.output(16, False)  # output pin 16 low
            time.sleep(0.00005)      # wait
            self.update_position(1)
            if self.current_position >= self.highest_position:  # stops before end of profile
                print("Top")
                break
            if self.current_position <= self.lowest_position:   # stops before end of profile
                print("bottom")
                break                 
        self.disable_driver()


actuator = SetPoint()
actuator.spin_motor(10,"up")        # testcases
time.sleep(0.5)
actuator.spin_motor(10,"up")
time.sleep(0.5)
actuator.spin_motor(500,"up")
time.sleep(0.5)
actuator.spin_motor(300,"down")
time.sleep(0.5)
actuator.spin_motor(300,"down")
time.sleep(0.5)
actuator.spin_motor(500,"up") 
GPIO.cleanup()