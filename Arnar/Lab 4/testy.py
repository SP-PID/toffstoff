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
motor_Ain1 = PWMOut(board.D10,frequency = 50)
motor_Ain2 = PWMOut(board.D11,frequency = 50)
motor_Bin1 = PWMOut(board.D8,frequency = 50)
motor_Bin2 = PWMOut(board.D9,frequency = 50)
motor_a = Motor.DCMotor(motor_Ain1,motor_Ain2)
motor_b = Motor.DCMotor(motor_Bin1,motor_Bin2)
potknob1 = analogio.AnalogIn(board.A1)
potknob2 = analogio.AnalogIn(board.A2)
encA = rotaryio.IncrementalEncoder(board.D6,board.D7)
encB = rotaryio.IncrementalEncoder(board.D4,board.D5)

class screen:
    def __init__(self,i2c=i2c): # Init the class
        displayio.release_displays() # Releases displays
        self.display_bus = displayio.I2CDisplay(i2c, device_address=0x3C) # Sets the I2C bus address 
        self.disp = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=64) # initiatiates the screen
        self.splash = displayio.Group() # Clears cache

    def text_to_disp(self,text, xpos, ypos, scale):  # Function to set up the print to screen function
        text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale=scale)
        self.splash.append(text_area) # Sends the text to the screen
        
    def show(self):
        
        display.show(self.splash)    #Prints what is in splash on the display
    def clear(self):
        self.splash = displayio.Group()  #Clears cache

class Smoothing:
    def __init__(self, coeff=0.1):
        self.coeff = coeff
        self.value = 0

    def update(self, input):
        # compute the error between the input and the accumulator
        difference = input - self.value

        # apply a constant coefficient to move the smoothed value toward the input
        self.value += self.coeff * difference

        return self.value  # Return the smoothed value


def IR_test():
    global modes
    smooth = Smoothing(0.2)  # Define class
    disp.clear()
    Text = "IR test"  # Text to display
    timestamp = time.monotonic()
    while time.monotonic()- timestamp  < 5:
        signal = signal_in.value  # Read the signal value from teh IR sensor

        smoothed = smooth.update(signal)  # Run teh signal vlaue trough the smoothing class

        voltage = (smoothed * 3.3) / 65536  # Calculate the voltage from the value read
        

        # Calculate the distance in Cm using the polynomial from Matlab
        distance = ((26.0865 * voltage ** 4)+ (-175.0947 * voltage ** 3)+ (437.4456 * voltage ** 2)+ (-510.3618 * voltage)+ 279.8494)
        disp.text_to_disp(Text, 0, 8, 2)  # Function to print
        # Print the raw value that the m4 read to the screen
        text1 = "Raw: {0:0.4f}".format(smoothed)# Text to display
        disp.text_to_disp(text1, 0, 28, 1)  # Function to print
        # Print the calculated voltage
        text2 = "Voltage: {0:0.4f} V".format(voltage) # Text to display
        disp.text_to_disp(text2, 0, 38, 1)  # Function to print
        
        # print the calculated distance
        text3 = "Distance: {0:0.4f} Cm".format(distance)# Text to display
        disp.text_to_disp(text3, 0, 48, 1)  # Function to print
        
        disp.show() # Displaying on the display
        disp.clear() # Clearing the screen cache
        if E_stop.value == False: # Emg stop to send to Start mode
            modes = 0
            return True
    disp.show()
    return False






def ramp_up(motor, direction, duration,pwm):
    timestamp = time.monotonic()
    while time.monotonic() - timestamp < duration:
        motor.throttle = simpleio.map_range(time.monotonic()-timestamp, 0, duration, 0, pwm)
        print("Ramp up",motor.throttle)
    

def ramp_down(motor, direction, duration,pwm):
    timestamp = time.monotonic()
    while time.monotonic() - timestamp < duration:
        motor.throttle = simpleio.map_range(time.monotonic()-timestamp, 0, duration, pwm, 0)
        print("Ramp down",motor.throttle)


def ramping_speed(motor,direction,duration,pwm):
    ramp_up(motor, direction, duration,pwm)
    ramp_down(motor, direction, duration,pwm)


def potentiometer():
    motor_radius = 22.44085
    motor_rad = 0.02244085
    delta_time = 0
    angular_velocity = 0
    delta_angle = 0

    while True:
        now = time.monotonic()
        ticks = encA.position
        angle = ticks * (2*math.pi/700)
        time.sleep(0.5)
        delta_time = now - time.monotonic()
        delta_angle = angle - (encA.position * (2*math.pi/700))
        angular_velocity = delta_angle/delta_time
        linear_velocity = motor_rad * angular_velocity
        #print('Angular velocity: {}'.format(angular_velocity))
        #print('Linear velocity: {}'.format(linear_velocity))
    
    
def pwm_sense():
    pot1= potknob1.value // 256
    pot2 = potknob2.value // 256
    return pot1, pot2
    
def throttle(PwmA,PwmB,direction):
    
    if direction == "FWD":
        motor_a.throttle = PwmA/255
        motor_b.throttle = PwmB/255
    elif direction == "REV":
        motor_a.throttle = -(PwmA/255)
        print(motor_a.throttle)
        motor_b.throttle = -(PwmB/255)
    else:
        motor_a.throttle = 0
        motor_b.throttle = 0
    
def brake(motor):
    pass    

while True:
    a,b =pwm_sense()
    ramping_speed(motor_a,"FWD",5,a/255)
    ramping_speed(motor_b,"FWD",5,b/255)
    #a,b =pwm_sense()
    #c =input("FWD or REV: ")
    #throttle(a,b,c)
    
