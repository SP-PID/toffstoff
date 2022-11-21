#!usr/bin/python

# This has to be somewhere in the code
import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BOARD)    # Setup of GPIO´s
GPIO.setwarnings(False)     # Don´t need no negativity in my life
pulse = 16
direc = 18
enable = 12
GPIO.setup(pulse, GPIO.OUT)    # pins 12, 16 and 18 are used as outputs
GPIO.setup(direc, GPIO.OUT)    # pin 18 is direction
GPIO.setup(enable, GPIO.OUT)
GPIO.output(enable, True)       # pin 12 is high
# -------------------------------------------------------------------


class SetPoint():
    def __init__(self) -> None:
        self.pulse_pin = 16
        self.dir_pin = 18
        self.enable_pin = 12
        self.pi = 3.14159265359                                                         # Everybody knows pi
        self.degrees_per_step = 1.8                                                     # for some reason this motor will move 0.225 degrees per step
        #print("Degrees per step: " + str(self.degrees_per_step))
        self.diameter = 19.65                                                           # diameter in millimeters
        #print("Diameter of pulley: " + str(self.diameter) + " mm")
        self.total_travel = 800                                                         # total travel of the gantry plate is 800 millimeters
        #print("Total travel of gantry: " + str(self.total_travel) + " mm")
        self.circumference = self.diameter * self.pi                                    # circumference in millimeters
        #print("Circumference of pulley: " + str(self.circumference) + " mm")
        self.steps_per_revolution = 360 / self.degrees_per_step                         # number of steps in a revolution
        #print("Number of steps per revolution: " + str(self.steps_per_revolution) + " steps")
        self.distance_per_step = self.circumference / self.steps_per_revolution         # distance per step in millimeters
        #print("Gantry travel per step: " + str(self.distance_per_step) + " mm")
        self.steps_total = self.total_travel / self.distance_per_step                   # total number of steps per length of travel of gantry plate
        #print("Total number of steps: " + str(self.steps_total) + " steps")
        self.rotation = False                                                           # variable for which direction the motor will spin
        self.direction = "up"                                                           # variable to tell program to go up or down
        self.current_position = 0                                                       # initializes in lowest position
        self.highest_position = self.steps_total                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position


    def enable_driver(self):        # Function that enables the driver to run
        ''' Function that enables Easydriver for use '''
        GPIO.output(self.enable_pin, False)  # the motor

    def disable_driver(self):       # Function that prevents the driver from 
        ''' Function that disables Easydriver after use '''
        GPIO.output(self.enable_pin, True)   # moving the motor

    def update_rotation(self,direction):
        self.direction = direction
        if self.direction == "up":
            self.rotation = False            # False means actuator moves up
        if self.direction == "down":
            self.rotation = True
        GPIO.output(self.dir_pin, self.rotation)

    def pulse(self):
        GPIO.output(self.pulse_pin, True)   # output pin 16 high
        time.sleep(0.0005)      # wait
        GPIO.output(self.pulse_pin, False)  # output pin 16 low
        time.sleep(0.0005)      # wait

    def update_position(self,distance):
        if self.direction == "down":
            self.current_position -= distance
        if self.direction == "up":
            self.current_position += distance

    def move_to_position(self,position):
        steps = self.current_position - position
        if self.current_position == position:
            # print("Do nothing")
            return         
        if self.current_position > position:
            self.update_rotation("down")
            # print("down")
        if self.current_position < position:
            self.update_rotation("up")
            # print("up")
            steps = -steps
        # print("Steps to move: " + str(steps))
        self.spin_motor(steps)
        # print("Current position " + str(self.current_position))
        
    def spin_motor(self,steps):
        self.enable_driver()
        for i in range(0, steps):
            self.pulse()
            self.update_position(1)
            if self.current_position >= self.highest_position:  # stops before end of profile
                # print("Top")
                break
            if self.current_position <= self.lowest_position:   # stops before end of profile
                # print("bottom")
                break                 
        self.disable_driver()


actuator = SetPoint()
#actuator.move_to_position(100)        # testcases
#time.sleep(0.5)
#actuator.move_to_position(200)
#time.sleep(0.5)
#actuator.move_to_position(100)
#time.sleep(0.5)
#actuator.move_to_position(200)
#time.sleep(0.5)
#actuator.move_to_position(1000)
#time.sleep(0.5)
#actuator.move_to_position(200)
#time.sleep(0.5)
#actuator.move_to_position(0)

while True:
    position = input("Enter a new position! ")
    try:
        position = int(position)
        actuator.move_to_position(position)
    except ValueError:
        print('Input not an integer!')
        break

GPIO.cleanup()