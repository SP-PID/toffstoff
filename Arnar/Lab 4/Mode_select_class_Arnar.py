import board
import adafruit_tcs34725
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import busio as io
import digitalio
import analogio
import adafruit_ssd1306
import neopixel
from rainbowio import colorwheel
import countio
import time
import sys
import math

# Class MainMenu contains the possible states of the robot
class MainMenu:
    def __init__(self): # Initialize the class, defines states
        self.STATES = ["START", "INIT", "CONF", "TEST", "RUN", "Exit"] # Possible states
        self.CUR_STATE = 0                                              # the current state of the robot
        self.SEL_STATE = 0                                              # the state the robot will be in once select is pressed
        self.disp = screen()                                            # defines the screen, calls screen class
        self.i2c = board.I2C()                                          # Defines I2c
        self.i2c_addresses = ['0x29', '0x3c', '0x60']                   # Array for i2c test
        self.running = True                                             # useful variable for Estop functions
        self.MODE = Button(board.D3)                                    # Mode button defined
        self.ESTOP = Button(board.D2)                                   # Estop button defined
        self.SEL = Button(board.D4)                                     # Select button defined
        self.button_arr = [self.ESTOP, self.MODE, self.SEL]             # Array for button test function
        self.test_ok = True                                             # was test succesful
        
    def drive(self):                                                    # function will be used to command robot to drive
        robot_drive = Drive()
        robot_drive.throttle(255, 255, "FWD")
        time.sleep(2)
        robot_drive.throttle(0, 0, "FWD")
    
    


    def Motor_A2D_PWM():
        pass

    def change_states(self):                                            # once select is pressed this function carries out                 
        if self.CUR_STATE == 0:                                         # the state change and calls appropriate function 
            self.start_state()
        if self.CUR_STATE == 1:
            self.init_state()
        if self.CUR_STATE == 2:
            self.config_state()
        if self.CUR_STATE == 3:
            self.test_state()
        if self.CUR_STATE == 4:
            self.run_state()
        if self.CUR_STATE == 5:
            self.estop_state()

    def start_state(self):      # executes actions the robot takes in starting state
        self.disp.text_to_display_3("Current State: ", self.STATES[self.CUR_STATE], "Doing start things...")
        
    def init_state(self):
        self.disp.text_to_display_3("Running","i2c","check..")
        i2c_test_ok = self.i2c_test() # Tests the i2c Bus
        time.sleep(1)
        self.disp.text_to_display_3("i2c","check","OK")
        time.sleep(1)
        self.disp.text_to_display_3("Starting","button","test.")
        time.sleep(1)
        button_test_ok = self.button_test() # Tests the buttons
        if i2c_test_ok and button_test_ok:  # if all test are ok then display message
            self.disp.text_to_display_3("All","Tests","OK")
        elif i2c_test_ok and not button_test_ok:    # if button test fail then display message
            self.disp.text_to_display_3("Button","Test","FAIL")
        elif not i2c_test_ok and button_test_ok:    # if i2c test fail then display message
            self.disp.text_to_display_3("I2c","Test","FAIL")
        time.sleep(3)
        self.disp.text_scroll(self.SEL_STATE)       # reset the menu on oled screen after 3 sec
        
    def config_state(self):
        pass

    def test_state(self):        # Executes the self testing 
        pass
    
    def i2c_test(self): # i2c test function
        is_ok = True
        self.i2c.try_lock() # lock the bus, then look for addresses and save to array
        found_addresses = [hex(device_address) for device_address in self.i2c.scan()]
        self.i2c.unlock() # unlock the i2c bus so that it can be used
        if self.i2c_addresses != found_addresses: 
            is_ok = False
        return is_ok

    def button_test(self): # button test function, carries out button test
        self.button_arr
        is_ok = True
        modes = ["Estop", "Mode", "Select"]
        for i in range(0,3):
            test = self.button_arr[i]
            time_start = time.time()
            self.disp.text_to_display_3("Press",modes[i],"button")
            while True:  
                if test.Read():
                    break
                if (time_start + 3) < time.time():
                    is_ok = False
                    break
        return is_ok
    
    def run_state(self):
        pass

    def estop_state(self): # emergency stop function stops all processes and ends program
        self.disp.text_to_display_3("ESTOP", "Mode", "Active!")
        self.CUR_STATE = 0
        self.SEL_STATE = 0
        time.sleep(1)
        self.disp.text_scroll(self.CUR_STATE)

    def mode_increment(self): # increments the select variable, select variable is Int variable
        if 0 <= self.SEL_STATE < 5:
            self.SEL_STATE += 1
        elif self.SEL_STATE >= 5:
            self.SEL_STATE = 0

    def run_program(self):
        self.disp.text_scroll(self.CUR_STATE)
        while self.running:
            if self.MODE.Read(): # if mode read is True then...
                self.mode_increment()
                self.disp.text_scroll(self.SEL_STATE)
                time.sleep(0.2)
            if self.ESTOP.Read():   # if estop read is True then...
                self.CUR_STATE = 5
                self.estop_state()
                #self.disp.text_to_display_1(self.STATES[self.CUR_STATE])
            if self.SEL.Read(): # if select read is True then...
                self.CUR_STATE = self.SEL_STATE
                self.disp.text_to_display_3(self.STATES[self.SEL_STATE], "", "Confirmed!")
                self.change_states()
                time.sleep(0.2)
        self.disp.text_to_display_3("Current State: ", "program", "ended") 
        time.sleep(3) # message displayed for 3 sec after loop is broken

class Button:
    def __init__(self, pin):
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

    def Read(self):
        return not self.button.value

class screen:
    def __init__(self,i2c = board.I2C()): # Init the class
        displayio.release_displays() # Releases displays
        self.display_bus = displayio.I2CDisplay(i2c, device_address=0x3C) # Sets the I2C bus address
        self.disp = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=64) # initiatiates the screen
        self.splash = displayio.Group() # Clears cache

    def text_to_disp(self,text, xpos, ypos, scale):  # Function to set up the print to screen function
        '''Adds text to oled screen splash'''
        text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale=scale)
        self.splash.append(text_area) # Sends the text to the screen

    def show(self):
        '''Function prints what is in splash on the display'''
        self.disp.show(self.splash)

    def clear(self):
        '''Function clears screen cache'''
        self.splash = displayio.Group()

    def text_to_display_1(self, text_to_show):
        '''Function displays one line on oled'''
        self.clear()
        self.text_to_disp(text_to_show, 0, 6, 2)
        self.show()
    
    def text_to_display_2(self, text_1="", text_2=""):
        '''function displays three lines on oled'''
        self.clear()
        self.text_to_disp(text_1, 0, 6, 1)
        self.text_to_disp(text_2, 0, 16, 1)
        self.show()
    
    def text_to_display_3(self, text_1="", text_2="", text_3=""):
        '''function displays three lines on oled'''
        self.clear()
        self.text_to_disp(text_1, 0, 6, 1)
        self.text_to_disp(text_2, 0, 26, 2)
        self.text_to_disp(text_3, 0, 46, 1)
        self.show()
    def text_to_display_4(self, text_1="", text_2="", text_3="", text_4=""):
        '''function displays three lines on oled'''
        self.clear()
        self.text_to_disp(text_1, 0, 6, 1)
        self.text_to_disp(text_2, 0, 16, 1)
        self.text_to_disp(text_3, 0, 36, 1)
        self.text_to_disp(text_4, 0, 46, 1)
        self.show()

    def text_scroll(self, current, STATES):
        '''Function allows user to scroll through menu on oled screen'''
        if current == 0:
            top = STATES[5]
            mid = STATES[0]
            bot = STATES[1]
        elif current == 5:
            top = STATES[4]
            mid = STATES[5]
            bot = STATES[0]
        else:
            top = STATES[current-1]
            mid = STATES[current]
            bot = STATES[current+1]
        self.text_to_display_3(top,mid,bot)


        
    def text_scroll(self, current): # function to scroll throug the menu on oled screen
        STATES = ["START", "INIT", "CONF", "TEST", "RUN", "ESTOP"]
        if current == 0:
            top = STATES[5]
            mid = STATES[0]
            bot = STATES[1]
        elif current == 5:
            top = STATES[4]
            mid = STATES[5]
            bot = STATES[0]        
        else:
            top = STATES[current-1]
            mid = STATES[current]
            bot = STATES[current+1]              
        self.text_to_display_3(top,mid,bot)

class Test_submenu:
    def __init__(self) -> None:
        self.STATES = ["Switch", "Tach", "IR", "n/a", "n/a","n/a"]
        self.display = MainMenu.disp
        self.i2c = MainMenu.i2c

class Drive:
    def __init__(self) -> None:
        self.disp = screen()
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
        #self.config = Conf()  

    def pwm_sense(self,A_or_B):
        self.pot1 = self.potknob1.value // 256
        self.pot2 = self.potknob2.value // 256
        if A_or_B =="A":
            return self.pot1
        if A_or_B =="B":
            return self.pot2
    
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
    
    def velocity(self):
        motor_radius = config.wheel_dia
        motor_rad = motor_radius/1000
        delta_time = 0
        angular_velocity = 0
        delta_angle = 0
        now = time.monotonic()
        ticks1 = self.get_enc_value("A")
        ticks2 = self.get_enc_value("B")
        angle1 = ticks1 * (2 * math.pi / 700)
        angle2 = ticks2 * (2 * math.pi / 700)
        time.sleep(0.1)
        ticks1 = self.get_enc_value("A")
        ticks2 = self.get_enc_value("B")
        delta_time = now - time.monotonic()
        delta_angle1 = angle1 - (ticks1 * (2 * math.pi / 700))
        delta_angle2 = angle2 - (ticks2 * (2 * math.pi / 700))
        angular_velocity1 = delta_angle1 / delta_time
        angular_velocity2 = delta_angle2 / delta_time
        linear_velocity1 = motor_rad * angular_velocity1
        linear_velocity2 = motor_rad * angular_velocity2
        return angular_velocity1, linear_velocity1,angular_velocity2, linear_velocity2

    def get_enc_value(self,A_or_B):
        if A_or_B == "A":
            enc = self.encA.position
        elif A_or_B == "B":
            enc = self.encB.position
        return enc
    
    def DRV_OL_FW(self):
        dist1 = 0
        dist2 = 0
        self.encA.position = 0
        self.encB.position = 0
        
        while dist1 < config.FW_test_dist and dist2 < config.FW_test_dist:
            dist1 = self.encA.position * (config.wheel_dia/100)
            dist2 = self.encB.position * (config.wheel_dia/100)
            self.throttle(255,255,"FWD")
            self.disp.text_to_disp("Distance: {0}mm".format(dist1), 0, 6, 1)
            self.disp.show()
            self.disp.clear()

        self.throttle(0,0,0)
    
    def Ramping_up(self,direction,duration,pwm):
    
        def ramp_up(direction,duration,pwm):
                timestamp = time.monotonic()
                while time.monotonic() - timestamp < duration:
                    throttle = simpleio.map_range(time.monotonic()-timestamp, 0, duration, 0, pwm)
                    self.throttle(throttle,throttle,direction)
                    a1,l1,a2,l2 =self.velocity()
                    self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
                self.disp.clear()
                self.disp.show()
                
        def ramp_down(direction, duration,pwm):
            timestamp = time.monotonic()
            while time.monotonic() - timestamp < duration:
                throttle = simpleio.map_range(time.monotonic()-timestamp, 0, duration, pwm, 0)
                self.throttle(throttle,throttle,direction)
                a1,l1,a2,l2 =self.velocity()
                self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
            self.disp.clear()
            self.disp.show()
        ramp_up(direction,duration,pwm)
        ramp_down(direction,duration,pwm)

    def encoder(self,duration):
                timestamp = time.monotonic()
                while time.monotonic() - timestamp < duration:
                    self.motor_a.throttle = self.pwm_sense("A") / 255
                    self.motor_b.throttle = self.pwm_sense("B") / 255
                    a1,l1,a2,l2 =self.velocity()
                    self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
                self.disp.clear()
                self.disp.show()








        
my_bot = MainMenu()
my_bot.run_program()
