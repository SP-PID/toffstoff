import rotaryio
import time
import board
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import digitalio
from pwmio import PWMOut
from adafruit_motor import motor as Motor
import countio
import analogio
import math
import simpleio

# Class MainMenu contains the possible states of the robot
class MainMenu:
    def __init__(self): # Initialize the class, defines states
        self.STATES = ["START", "INIT", "CONF", "TEST", "RUN", "Exit"] # Possible states
        self.CUR_STATE = 0                                              # the current state of the robot
        self.SEL_STATE = 0                                              # the state the robot will be in once select is pressed
        self.disp = disp                                            # defines the screen, calls screen class
        self.i2c = board.I2C()                                          # Defines I2c
        self.i2c_addresses = ['0x29', '0x3c', '0x60']                   # Array for i2c test
        self.running = True                                             # useful variable for Estop functions
        self.MODE = MODE                                    # Mode button defined
        self.ESTOP = ESTOP                                   # Estop button defined
        self.SEL = SEL                                     # Select button defined
        self.button_arr = [self.ESTOP, self.MODE, self.SEL]             # Array for button test function
        self.test_ok = True                                             # was test succesful

    def share_buttons(self):     
        '''Function makes it so that redefining buttons is not neccesary'''
        return self.button_arr

    def share_screen(self):         
        '''Function makes it so that redefining screen is not neccesary'''
        return self.disp

    def share_i2c(self):            
        '''Function makes it so that redefining i2c is not neccesary'''
        return self.i2c                                                 

    def change_states(self):                             
        '''Function executes selected(now current) state when select is pressed'''
        if self.CUR_STATE == 0:                          
            self.start_state()          # calls appropriate function depending on Current variable
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
        '''Function where the starting state is defined'''
        self.disp.text_to_display_3("Current State: ", self.STATES[self.CUR_STATE], "Doing start things...")

    def init_state(self):
        '''Function that defines the init state, and runs self testing'''
        self.disp.text_to_display_3("Running","i2c","check..")
        i2c_test_ok = self.i2c_test() # Tests the i2c Bus
        time.sleep(2)
        self.disp.text_to_display_3("i2c","check","OK")
        time.sleep(2)
        self.disp.text_to_display_3("Starting","button","test.")
        time.sleep(2)
        button_test_ok = self.button_test() # Tests the buttons
        if i2c_test_ok and button_test_ok:  # if all test are ok then display message
            self.disp.text_to_display_3("All","Tests","OK")
        elif i2c_test_ok and not button_test_ok:    # if button test fail then display message
            self.disp.text_to_display_3("Button","Test","FAIL")
        elif not i2c_test_ok and button_test_ok:    # if i2c test fail then display message
            self.disp.text_to_display_3("I2c","Test","FAIL")
        time.sleep(3)
        self.disp.text_scroll(self.SEL_STATE, self.STATES)       # reset the menu on oled screen after 3 sec

    def config_state(self): 
        '''Function defines the configuration state'''
        config_submenu = Config_submenu()
        config_submenu.disp_menu()
        self.disp.text_scroll(self.SEL_STATE, self.STATES)

    def test_state(self):        # Executes the self testing
        '''Function defines the testing state'''
        test_submenu = Test_submenu()
        test_submenu.disp_menu()
        self.disp.text_scroll(self.SEL_STATE, self.STATES)

    def i2c_test(self): # i2c test function
        '''Function runs the i2c test'''
        is_ok = True
        self.i2c.try_lock() # lock the bus, then look for addresses and save to array
        found_addresses = [hex(device_address) for device_address in self.i2c.scan()]
        self.i2c.unlock() # unlock the i2c bus so that it can be used
        if self.i2c_addresses != found_addresses:
            is_ok = False
        return is_ok

    def button_test(self): # button test function, carries out button test
        '''Function runs the button test'''
        self.button_arr
        is_ok = True
        modes = ["Estop", "Mode", "Select"]
        for i in range(0,3):
            test = self.button_arr[i] # fetch the button to test
            time_start = time.time()
            self.disp.text_to_display_3("Press",modes[i],"button") # prompts user to press button
            while True:
                if test.Read():
                    break       # if test is succesful then break loop
                if (time_start + 3) < time.time():
                    is_ok = False # test fail if time exceeds 3 seconds
                    break
        return is_ok

    def run_state(self):
        '''Function used to command robot to drive '''
        drive.throttle(255, 255, "FWD")       # go forward for two seconds and then stop           
        time.sleep(2)
        drive.throttle(0, 0, "FWD")

    def estop_state(self): # emergency stop function stops all processes and ends program
        '''Estop function ends all processes and returns robot to it´s starting state'''
        self.disp.text_to_display_3("ESTOP", "Mode", "Active!")
        drive.throttle(0, 0, "FWD")  # stop motors
        self.CUR_STATE = 0          # reset current and select variables
        self.SEL_STATE = 0
        time.sleep(1)
        self.disp.text_scroll(self.CUR_STATE,self.STATES)

    def mode_increment(self):
        '''increments the select variable, select variable is Int variable'''
        if 0 <= self.SEL_STATE < 5:
            self.SEL_STATE += 1
        elif self.SEL_STATE >= 5:
            self.SEL_STATE = 0

    def run_program(self):
        '''Main function of MainMenu class'''
        self.disp.text_scroll(self.CUR_STATE,self.STATES)
        while self.running:
            if self.MODE.Read(): # if mode read is True then...
                self.mode_increment()
                self.disp.text_scroll(self.SEL_STATE,self.STATES)
                time.sleep(0.2)
            if self.ESTOP.Read():   # if estop read is True then...
                self.CUR_STATE = 5
                self.estop_state()
            if self.SEL.Read(): # if select read is True then...
                self.CUR_STATE = self.SEL_STATE
                time.sleep(0.5)
                self.disp.text_to_display_3(self.STATES[self.SEL_STATE], "", "Confirmed!")
                self.change_states()
        self.disp.text_to_display_3("Current State: ", "program", "ended")
        time.sleep(3) # message displayed for 3 sec after loop is broken

class Button:
    def __init__(self, pin):
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

    def Read(self):
        '''Returns state of button, True if button pressed'''
        return not self.button.value
        
    def Read_Lock(self):
        if not self.button.value:
            while not self.button.value:
                p = 1
            return True
        return False

class Pot:
    def __init__(self, pin):
        self.pot = analogio.AnalogIn(pin)

    def Read(self):
        return self.pot.value

class screen:
    def __init__(self,i2c = board.I2C()): # Init the class
        displayio.release_displays() # Releases displays
        self.display_bus = displayio.I2CDisplay(i2c, device_address=0x3C) # Sets the I2C bus address
        self.disp = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=64) # initiatiates the screen
        self.splash = displayio.Group() # Clears cache

    def text_to_disp(self,text, xpos, ypos, scale):  # Function to set up the print to screen function
        text_area = label.Label(terminalio.FONT, text=text, x=xpos, y=ypos, scale=scale, save_text = False)
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

    def text_to_display_3(self, text_1="", text_2="", text_3=""):
        '''function displays three lines on oled'''
        self.clear()
        self.text_to_disp(text_1, 0, 6, 1)
        self.text_to_disp(text_2, 0, 26, 2)
        self.text_to_disp(text_3, 0, 46, 1)
        self.show()

    def del_last(self):
        del self.splash[-1]

    def text_scroll(self, current, STATES): # function to scroll throug the menu on oled screen
        menu_length = len(STATES)
        if current == 0:
            top = STATES[menu_length-1]
            mid = STATES[0]
            bot = STATES[1]
        elif current == menu_length-1:
            top = STATES[menu_length-2]
            mid = STATES[menu_length-1]
            bot = STATES[0]
        else:
            top = STATES[current-1]
            mid = STATES[current]
            bot = STATES[current+1]
        self.text_to_display_3(top,mid,bot)

class Test_submenu:
    def __init__(self) -> None:
        self.states = ["Switch", "Tach", "IR", "Drive", "Exit"]
        self.length_states = len(self.states)
        self.disp= my_bot.share_screen()
        self.buttons = my_bot.share_buttons()
        self.i2c = my_bot.share_i2c()
        self.Selected = 0
        self.Current = 0
        self.running = True

    def disp_menu(self):
        '''Main function of Test_submenu class'''
        self.disp.text_scroll(self.Current, self.states)
        while self.running:
            if self.buttons[1].Read(): # if mode read is True then...
                self.mode_increment()
                self.disp.text_scroll(self.Selected, self.states)
                time.sleep(0.2)
            if self.buttons[0].Read():   # if estop read is True then...
                self.Current = self.length_states-1
                self.running = False
                my_bot.estop_state()
            if self.buttons[2].Read(): # if select read is True then...
                self.Current = self.Selected
                self.run_tests()
                time.sleep(0.5)

    def mode_increment(self):
        '''Function increments Selected variable and resets it if value is larger than or equal to 5'''
        if 0 <= self.Selected < self.length_states-1:
            self.Selected += 1
        elif self.Selected >= self.length_states-1:
            self.Selected = 0

    def run_tests(self): 
        '''A function that runs the selected tests'''                                           
        if self.Current == 0:                                         
            self.switch_test()
        if self.Current == 1:
            self.tach_test()
        if self.Current == 2:
            self.ir_test()
        if self.Current == 3:
            drive.DRV_OL_FW()
        if self.Current == 4:           # Exit function, returns to main
            self.running = False
            
class Config_submenu:
    def __init__(self) -> None:
        self.states = ["Wheel_Dia", "Ramp", "Test dist", "Break Dist", "Follow","Exit"]
        self.length_states = len(self.states)
        self.disp= my_bot.share_screen()
        self.buttons = my_bot.share_buttons()
        self.Selected = 0
        self.Current = 0
        self.running = True

    def run_config(self):      
        '''Runs appropriate config functions'''                                      
        if self.Current == 0:                                         
            self.wheel()
        if self.Current == 1:
            self.ramp()
        if self.Current == 2:
            self.test_dist()
        if self.Current == 3:
            self.break_dist()
        if self.Current == 4:
            self.follow()
        if self.Current == 5:       # Exit function, returns to main
            self.running = False            
        if self.Current == 6:
            self.ramp_time()
        if self.Current == 7:
            self.test_dur()


    def disp_menu(self):
        '''Main function of Config submenu class'''
        self.disp.text_scroll(self.Current, self.states)
        print(self.length_states)
        while self.running:
            if self.buttons[1].Read(): # if mode read is True then...
                print(self.Selected)
                self.mode_increment()
                self.disp.text_scroll(self.Selected, self.states)
                time.sleep(0.2)
            if self.buttons[0].Read():   # if estop read is True then...
                self.Current = 5
                self.running = False
                my_bot.estop_state()
            if self.buttons[2].Read(): # if select read is True then...
                self.Current = self.Selected
                self.run_config()
                time.sleep(0.5)

    def mode_increment(self):
        '''Function increments Selected variable and resets it if value is larger than or equal to 5'''
        if 0 <= self.Selected < self.length_states-1:
            self.Selected += 1
        elif self.Selected >= self.length_states-1:
            self.Selected = 0

    def wheel(self):
        config.wheel_dia = self.set_val(100,10,"Wheel diameter",config.wheel_dia,"mm")
            
    def ramp(self):
        config.ramp = int(self.set_val(0, 255, "Ramp value", config.ramp,""))

    def test_dist(self):
        config.FW_test_dist = self.set_val(100, 3000, "Test distance", config.FW_test_dist,"mm")

    def break_dist(self):
        config.break_dist = self.set_val(200, 1000, "Break distance", config.break_dist,"mm")

    def follow(self):
        config.follow = self.set_val(300, 1500, "Follow distance", config.follow,"mm")

    def ramp_tiem(self):
        config.ramp_time = self.set_val(0.1, 5, "Ramp time", config.ramp_time,"sec")

    def test_dur(self):
        config.test_dur = self.set_val(0.1, 5, "Test run time", config.ramp_time,"sec")

    def set_val(self,max_val,min_val,conf_text,value,unit):
        prev_value = value
        disp.clear()
        disp.text_to_disp("Set "+conf_text,0,4,1)
        disp.text_to_disp("Current: {0:0.1f}".format(prev_value)+unit,0,13,1)
        disp.text_to_disp("ESTOP or MODE: Cancel",0,49,1)
        disp.text_to_disp("Set: Select",0,58,1)
        disp.text_to_disp("Set: Select",0,58,1)
        SEL.Read_Lock()
        
        while True:
            set_val = round(simpleio.map_range(pot1.Read(),0,65535,min_val,max_val),1)
            disp.del_last()
            disp.text_to_disp("New value: {0:0.1f}".format(set_val)+unit,0,30,1)
            disp.show()
            if SEL.Read_Lock():
                new_value = set_val
                disp.clear()
                disp.text_to_disp("New value\nset",0,12,2)
                disp.show()
                time.sleep(2)
                self.disp_menu()
                return new_value
            if ESTOP.Read_Lock() or MODE.Read_Lock():
                disp.clear()
                disp.text_to_disp("New value\nnot set",0,12,2)
                disp.show()
                time.sleep(2)
                self.disp_menu()
                return prev_value
            time.sleep(0.05)
        
class Drive:
    def __init__(self) -> None:
        self.motor_Ain1 = PWMOut(board.D11,frequency = 50)
        self.motor_Ain2 = PWMOut(board.D12,frequency = 50)
        self.motor_Bin1 = PWMOut(board.D9,frequency = 50)
        self.motor_Bin2 = PWMOut(board.D10,frequency = 50)
        self.motor_a = Motor.DCMotor(self.motor_Ain1,self.motor_Ain2)
        self.motor_b = Motor.DCMotor(self.motor_Bin1,self.motor_Bin2)
        self.potknob1 = pot1
        self.potknob2 = pot2
        self.encA = rotaryio.IncrementalEncoder(board.D7,board.D8)
        self.encB = rotaryio.IncrementalEncoder(board.D5,board.D6) 
        # self.config = Conf()  

    def pwm_sense(self):
        '''Function reads potentiometers'''
        pot1 = self.potknob1.value // 256
        pot2 = self.potknob2.value // 256
        return pot1, pot2
    
    def throttle(self, PwmA, PwmB, direction): 
        '''Function that determines speed of each motor'''
        if direction == "FWD":
            self.motor_a.throttle = PwmA/255
            self.motor_b.throttle = PwmB/255
        elif direction == "REV":
            self.motor_a.throttle = -(PwmA/255)
            self.motor_b.throttle = -(PwmB/255)
        else:
            self.motor_a.throttle = 0
            self.motor_b.throttle = 0


    def get_enc_value(self,A_or_B):
        '''Function reads and returns value of drive motor encoders'''
        if A_or_B == "A":
            enc = self.encA.position
        elif A_or_B == "B":
            enc = self.encB.position
        return enc
    
    def DRV_OL_FW(self):
        '''A function for testing drive motors'''
        dist1 = 0
        dist2 = 0
        while dist1 < 1000 and dist2 < 1000:
            dist1 = self.get_enc_value("A") * 0.22
            dist2 = self.get_enc_value("A") * 0.22
            self.throttle(255,255,"FWD")
        self.throttle(0,0,0)

class Conf():
    def __init__(self):
        self.wheel_dia = 22
        self.ramp = 125
        self.FW_test_dist = 1000
        self.break_dist = 300
        self.follow = 500
        self.ramp_time = 1
        self.test_dur = 5


MODE = Button(board.D3)                                    # Mode button defined
ESTOP = Button(board.D2)                                   # Estop button defined
SEL = Button(board.D4)

pot1 = Pot(board.A1)
pot2 = Pot(board.A2)

disp = screen()

drive = Drive()

config = Conf()
my_bot = MainMenu()
my_bot.run_program()
