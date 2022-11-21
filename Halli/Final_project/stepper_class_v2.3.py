#!usr/bin/python

# This has to be somewhere in the code
import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BOARD)    # Setup of GPIO´s
GPIO.setwarnings(False)     # Don´t need no negativity in my life
pulse = 16
direc = 18
enable = 12
button = 10
GPIO.setup(pulse, GPIO.OUT)    # pins 12, 16 and 18 are used as outputs
GPIO.setup(direc, GPIO.OUT)    # pin 18 is direction
GPIO.setup(enable, GPIO.OUT)
GPIO.output(enable, True)       # pin 12 is high
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# -------------------------------------------------------------------


class SetPoint():
    def __init__(self, pulse, direc, enable, button) -> None:
        self.pulse_pin = pulse                                                          # Pins defined
        self.dir_pin = direc
        self.enable_pin = enable
        self.button_pin = button
        self.pi = 3.14159265359                                                         # Everybody knows pi
        self.degrees_per_step = 1.8                                                     # for some reason this motor will move 0.225 degrees per step
        self.diameter = 19.65                                                           # diameter in millimeters
        self.total_travel = 840                                                         # total travel of the gantry plate is 800 millimeters
        self.circumference = self.diameter * self.pi                                    # circumference in millimeters
        self.steps_per_revolution = 360 / self.degrees_per_step                         # number of steps in a revolution
        self.distance_per_step = self.circumference / self.steps_per_revolution         # distance per step in millimeters
        self.steps_total = self.total_travel / self.distance_per_step                   # total number of steps per length of travel of gantry plate
        self.rotation = False                                                           # variable for which direction the motor will spin
        self.direction = "up"                                                           # variable to tell program to go up or down
        self.current_position = 0                                                       # initializes in lowest position
        self.highest_position = self.steps_total                                        # for readability define top position
        self.lowest_position = 0                                                        # for readability define bottom position
        self.reset_actuator()                                                           # actuator finds zero position (bottom)

    def get_total_steps(self):
        ''' Returns total number of steps for end to end travel '''
        return self.steps_total

    def enable_driver(self):        
        ''' Function that enables Easydriver for use '''
        GPIO.output(self.enable_pin, False)  

    def disable_driver(self):        
        ''' Function that disables Easydriver after use '''
        GPIO.output(self.enable_pin, True)   

    def update_rotation(self,direction):
        ''' Function updates variable for gantry travel direction '''
        self.direction = direction
        if self.direction == "up":
            self.rotation = True            # False means actuator moves up
        if self.direction == "down":
            self.rotation = False
        GPIO.output(self.dir_pin, self.rotation)

    def pulse(self):
        ''' Function sends out one pulse on pulse pin '''
        GPIO.output(self.pulse_pin, True)   # output pin 16 high
        time.sleep(0.0007)      # wait
        GPIO.output(self.pulse_pin, False)  # output pin 16 low
        time.sleep(0.0007)      # wait

    def update_position(self,distance):
        ''' Function keeps track of current position of gantry '''
        if self.direction == "down":
            self.current_position -= distance
        if self.direction == "up":
            self.current_position += distance

    def move_to_position(self,position):
        ''' Function moves gantry to a requested position '''
        steps = self.current_position - position
        if self.current_position == position:
            return         
        if self.current_position > position:
            self.update_rotation("down")
        if self.current_position < position:
            self.update_rotation("up")
            steps = -steps
        self.spin_motor(steps)
        print("Current position " + str(self.current_position))
        
    def spin_motor(self,steps):
        ''' Function that moves the stepper motor '''
        self.enable_driver()
        for _ in range(0, steps):
            self.pulse()                    # one high and one low on pin
            self.update_position(1)
            if self.current_position >= self.highest_position:  # stops before top end of profile
                break
            if self.current_position <= self.lowest_position:   # stops before bottom end of profile
                break                 
        self.disable_driver()

    def reset_actuator(self):
        ''' Function that moves the gantry to zero position (bottom) '''
        self.update_rotation("down")    # sets travel direction to down
        self.enable_driver()            # enables the driver to move
        while True:
            self.pulse()                # sends out pulses until the button reads high
            if GPIO.input(self.button_pin) == GPIO.HIGH: # read a button
                print("Bottom reached!")    
                break                        # break loop when bottom reached
        self.disable_driver()           # driver disabled


actuator = SetPoint(pulse, direc, enable, button)

while True:
    position = input("Enter a new position! ")
    try:
        position = int(position)
        actuator.move_to_position(position)
        time.sleep(1)
    except ValueError:
        print('Input not an integer!')
        break

GPIO.cleanup()