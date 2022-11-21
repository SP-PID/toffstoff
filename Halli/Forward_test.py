
import rotaryio
import time
import board
import displayio
import terminalio
import adafruit_displayio_ssd1306
import adafruit_tcs34725
from adafruit_display_text import label
#from digitalio import DigitalInOut, Direction, Pull
import digitalio
import pwmio
from adafruit_motor import motor as Motor
import countio
import analogio
# import simpleio
import math
import simpleio

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_airlift.esp32 import ESP32

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket


# Class MainMenu contains the possible states of the robot
class MainMenu:
    def __init__(self): # Initialize the class, defines states
        self.STATES = ["START", "INIT", "CONF", "TEST", "RUN", "BT controll", "Exit"] # Possible states
        self.length = len(self.STATES) - 1
        self.CUR_STATE = 0                                              # the current state of the robot
        self.SEL_STATE = 0                                              # the state the robot will be in once select is pressed                                          # defines the screen, calls screen class                                          # Defines I2c
        self.i2c_addresses = ['0x29', '0x3c', '0x60']                   # Array for i2c test
        self.running = True                                             # useful variable for Estop functions
        self.test_ok = True                                             # was test succesful


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
            self.BT_controll()
        if self.CUR_STATE == 6:
            self.estop_state()

    def start_state(self):      # executes actions the robot takes in starting state
        '''Function where the starting state is defined'''
        disp.text_to_display_3("Current State: ", self.STATES[self.CUR_STATE], "Doing start things...")

    def init_state(self):
        '''Function that defines the init state, and runs self testing'''
        disp.text_to_display_3("Running","i2c","check..")
        if bt.ble.connected:    #If bluetooth is connected send message
            bt.uart.write("\nRunning I2C Check.\n")
        i2c_test_ok = self.i2c_test() # Tests the i2c Bus
        time.sleep(2)
        disp.text_to_display_3("i2c","check","DONE")
        if bt.ble.connected:    #If bluetooth is connected send message
            bt.uart.write("I2C check DONE.\n")
        time.sleep(2)
        disp.text_to_display_3("Starting","button","test.")
        if bt.ble.connected:    #If bluetooth is connected send message
            bt.uart.write("Starting button test.\n")
        time.sleep(2)
        button_test_ok = self.button_test() # Tests the buttons
        if i2c_test_ok and button_test_ok:  # if all test are ok then display message
            disp.text_to_display_3("All","Tests","OK")
            if bt.ble.connected:    #If bluetooth is connected send message
                bt.uart.write("All tests OK.\n\n")
            return "All tests ok"
        elif i2c_test_ok and not button_test_ok:    # if button test fail then display message
            disp.text_to_display_3("Button","Test","FAIL")
            if bt.ble.connected:    #If bluetooth is connected send message
                bt.uart.write("Button test failed.\n\n")
            return "Button Test FAIL"
        elif not i2c_test_ok and button_test_ok:    # if i2c test fail then display message
            disp.text_to_display_3("I2c","Test","FAIL")
            if bt.ble.connected:    #If bluetooth is connected send message
                bt.uart.write("I2C test failed.\n\n")
            return "I2C Test FAIL"
        time.sleep(3)
        # reset the menu on oled screen after 3 sec
        disp.text_scroll(self.SEL_STATE, self.STATES, self.length)

    def config_state(self):
        '''Function defines the configuration state'''
        config_submenu.disp_menu()
        disp.text_scroll(self.SEL_STATE, self.STATES)

    def test_state(self):        # Executes the self testing
        '''Function defines the testing state'''
        test_submenu.disp_menu()
        disp.text_scroll(self.SEL_STATE, self.STATES)

    def i2c_test(self): # i2c test function
        '''Function runs the i2c test'''
        is_ok = True
        config.i2c.try_lock() # lock the bus, then look for addresses and save to array
        found_addresses = [hex(device_address) for device_address in config.i2c.scan()]
        config.i2c.unlock() # unlock the i2c bus so that it can be used
        if self.i2c_addresses != found_addresses:
            is_ok = False
        return is_ok

    def button_test(self): # button test function, carries out button test
        '''Function runs the button test'''
        is_ok = True
        modes = ["Estop", "Mode", "Select"]
        button_arr = [ESTOP, MODE, SEL]
        for i in range(0,3):
            test = button_arr[i] # fetch the button to test
            time_start = time.time()
            disp.text_to_display_3("Press",modes[i],"button") # prompts user to press button
            if bt.ble.connected:
                bt.uart.write("Press {} Butoon\n".format(modes[i]))
            while True:
                if test.Read_Lock():
                    break       # if test is succesful then break loop
                if (time_start + 3) < time.time():
                    is_ok = False # test fail if time exceeds 3 seconds
                    break
        return is_ok

    def run_state(self):
        '''Function used to command robot to drive '''
        navi = run_submenu()
        navi.disp_menu()

    def estop_state(self): # emergency stop function stops all processes and ends program
        '''Estop function ends all processes and returns robot to it´s starting state'''
        disp.text_to_display_3("ESTOP", "Mode", "Active!")
        #robot_drive.throttle(0, 0, "FWD")  # stop motors
        self.CUR_STATE = 0          # reset current and select variables
        self.SEL_STATE = 0
        time.sleep(1)
        disp.text_scroll(self.CUR_STATE,self.STATES)

    def mode_increment(self):
        '''increments the select variable, select variable is Int variable'''
        if 0 <= self.SEL_STATE < self.length:
            self.SEL_STATE += 1
        elif self.SEL_STATE >= self.length:
            self.SEL_STATE = 0

    def run_program(self):
        '''Main function of MainMenu class'''
        disp.text_scroll(self.CUR_STATE,self.STATES, self.length)
        while self.running:
            if MODE.Read(): # if mode read is True then...
                self.mode_increment()
                disp.text_scroll(self.SEL_STATE,self.STATES, self.length)
                time.sleep(0.2)
            if ESTOP.Read():   # if estop read is True then...
                self.CUR_STATE = 5
                self.estop_state()
            if SEL.Read_Lock(): # if select read is True then...
                self.CUR_STATE = self.SEL_STATE
                time.sleep(0.1)
                disp.text_to_display_3(self.STATES[self.SEL_STATE], "", "Confirmed!")
                self.change_states()
        self.disp.text_to_display_3("Current State: ", "program", "ended")
        time.sleep(3) # message displayed for 3 sec after loop is broken

    def BT_controll(self):
        '''Bluethooth controll state. In this state varius states of the
        robot can be operated over bluethooth UART terminal'''
        bt.BT_start()   #start the bluethooth operation
        bt.BT_main_menu()   #Go into the Bluethooth menu
        #When The BT menu is exetid the main menu is printed on the oled
        disp.text_scroll(self.CUR_STATE,self.STATES, self.length)

'''Button clarr to make it possible to call the buttons where
ever in the code'''
class Button:
    def __init__(self, pin):
        '''Define the button as input and pull it up'''
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

    def Read(self):
        '''Returns the state of button, True if button pressed'''
        return not self.button.value


    def Read_Lock(self):
        '''Returns true if the button was pressed and relesed again'''
        if not self.button.value:
            '''Wait and do nothing while the button is pressed'''
            while not self.button.value:
                pass
            return True #Return ture when the button is relesed
        return False

'''Class tha contains all opperations done whilst in BT mode'''
class BT_buttons:
    def __init__(self):
        '''Dictionary for holding the staates of the buttons
        on the controller of the bluefruit app'''
        self.buttons = {}
        '''Create all teh buttons in the dictionary and assign
        them to false'''
        for key in range(9):
            self.buttons[str(key)] = False
        '''Define everything for the buetooth opperation'''
        self.esp32 = ESP32()
        self.adapter = self.esp32.start_bluetooth()
        self.ble = BLERadio(self.adapter)
        self.uart = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart)
        self.last_word = ""
        self.word = ""

    def BT_start(self):
        '''If the bluethooth is not connected print on
        the oled to connect to the robot and tehn wait
        until something is connected'''
        if not self.ble.connected:
            self.ble.start_advertising(self.advertisement)
            disp.clear()
            disp.text_to_disp("Connect to bluetooth!",0,4,1)
            disp.show()
            disp.clear()
            print("waiting to connect")
            '''Do nothing while bluetooth is not connected'''
            while not self.ble.connected:
                pass
            print("connected: trying to read input")
        disp.clear()
        disp.show()
        '''Let know on the oled that BT is connected and
        to go tho the uart terminal and great the robot
        with Hello'''
        disp.text_to_disp("Bluetooth connected!",0,4,1)
        disp.text_to_disp("Go to uart console",0,14,1)
        disp.text_to_disp("Write Hello",0,24,1)
        disp.show()
        disp.clear()

    '''Stop advertisement of BT connection'''
    def BT_stop(self):
        self.ble.stop_advertising(self.advertisement)

    '''Read button pressess from the bluefruit app over
    BT and assign the current state of teh button to the
    buttons dictionary.'''
    def BT_read(self):
        if self.uart.in_waiting:
            print("n")#used for debuggig
            '''Assign packet from BT stream to packet'''
            packet = Packet.from_stream(self.uart)

            '''Check if the packeet is of the right kind'''
            if isinstance(packet, ButtonPacket):
                '''If the button number is not in the
                button dictionary create a new entry and
                assign it a false state, might be
                redundant'''
                if packet.button not in self.buttons:
                    self.buttons[packet.button] = False
                '''Assigns the state of the button pressed
                to the button in the dictionary'''
                self.buttons[packet.button] = packet.pressed
                return

        else:
            return

    '''Returns the current state of the button specified'''
    def BT_Button_read(self, button):
        return self.buttons[button]

    '''Reads and decodes text sent over uart console'''
    def BT_uart(self):
        '''Takes one byte decodes it into text '''
        one_byte = self.uart.read(1).decode("utf-8")
        '''if the byte is not a new line caracter witch denotes
        the end of that message then ad the text in the byte to
        the current word / message'''
        if str(one_byte) != "\n":
            self.word += one_byte
        '''When the new line character appears then the
        current word is assigned to the variable that holds
        teh last complete message'''
        if str(one_byte) == "\n":
            self.last_word = self.word
            self.word = "" #empty the current word

    '''Function that runs the main BT menu'''
    def BT_main_menu(self):
        '''messages to great the person that just connected'''
        title = "I am GOATIFI Racing Champion\nI AM A DRIVING GOD!!!\n\n"
        exit = False

        '''loop that waits for a greating from teh connected
        BT device'''
        while self.ble.connected:
            self.BT_uart() #Reading the BT
            '''If greating is receved write the greating
            and the main menu items then breaks'''
            if self.last_word == "Hello":
                self.uart.write(title)
                self.uart.write(text)
                self.last_word = ""
                break

        '''The main main menu loop'''
        while self.ble.connected:
            '''if the exit variable is true the program
            just returned from a submenu and the main menu
            text has to be printed to the uart console'''
            if exit:
                self.uart.write(text)
                exit = False

            self.BT_uart() #read the uart stream

            '''If user asked for the configuration
            menu go into that menu'''
            if self.last_word == "CONF":
                 exit = self.BT_conf_menu()

            elif self.last_word == "INIT":
                my_bot.init_state()
                exit = True
                self.BT_start() #Used to put the oled to BT mode
                self.last_word = "" #reset the ladt word

            #If user asked for the test
            # menu go into that menu'''
            elif self.last_word == "TEST":
                self.BT_Test()
                exit = True

            #Run the main run code of the robot
            #not implemented yet'''
            elif self.last_word =="RUN":
                my_bot.run_state()
                self.uart.write("\n\nRUN is not implemented yet!\n\n")
                self.last_word = ""
                exit = True

            #Enter the BT drive mode to controll
            #the movements of the robot using the buttons
            #in the bluefruit app'''
            elif self.last_word == "DRIVE":
                self.BT_Drive()

            #'''Exit the BT mode and return to normal
            #button opperation'''
            elif self.last_word == "exit":
                self.uart.write("Exiting Bluetooth mode.")
                self.last_word = ""
                return

            #'''Estop'''
            elif ESTOP.Read():
                self.uart.write("Estop Exit")
                return

            #'''If teh last word is empty do nothing'''
            elif self.last_word == "":
                pass

            #'''If the last word is not eccepted notefy and
            #print the main menu again'''
            else:
                self.uart.write("\nNot an option!\n")
                time.sleep(1)
                self.uart.write(text)
                self.last_word = ""

    '''BT menu used to change the config values of the robot'''
    def BT_conf_menu(self):
        text = "-----------------------------------------------\n"
        text += "Set values - Type in options with value after.\n"
        text += "----------------------------------------------\n"
        text += "Wheel diameter (mm): WD - Current {0:0.1f}\n".format(config.wheel_dia)
        text += "Ramp : R - Current {0:0.1f}\n".format(config.ramp)
        text += "Forward test distance (mm): FTD - Current {0:0.1f}\n".format(config.FW_test_dist)
        text += "Break distance (mm): BD - Current {0:0.1f}\n".format(config.break_dist)
        text += "Follow distance (mm): FD - Current {0:0.1f}\n".format(config.follow)
        text += "Ramp time (s): RT - Current {0:0.1f}\n".format(config.ramp_time)
        text += "Test duration (s): TD - Current {0:0.1f}\n".format(config.test_dur)
        text += "Exit: exit\n"
        self.uart.write(text)
        change = False
        while self.ble.connected:
            text = "-----------------------------------------------\n"
            text += "Set values - Type in options with value after.\n"
            text += "----------------------------------------------\n"
            text += "Wheel diameter (mm): WD - Current {0:0.1f}\n".format(config.wheel_dia)
            text += "Ramp : R - Current {0:0.1f}\n".format(config.ramp)
            text += "Forward test distance (mm): FTD - Current {0:0.1f}\n".format(config.FW_test_dist)
            text += "Break distance (mm): BD - Current {0:0.1f}\n".format(config.break_dist)
            text += "Follow distance (mm): FD - Current {0:0.1f}\n".format(config.follow)
            text += "Ramp time (s): RT - Current {0:0.1f}\n".format(config.ramp_time)
            text += "Test duration (s): TD - Current {0:0.1f}\n".format(config.test_dur)
            text += "Exit: exit\n"
            self.last_word = ""
            self.BT_uart()
            if change:
                self.uart.write(text)
                change = False
            word = self.last_word
            word = word.split()

            if len(word) == 2:
                if word[0] == "WD":
                    config.wheel_dia = float(word[1])
                    print(config.wheel_dia)
                    self.last_word = ""
                    change = True

                elif word[0] == "R":
                    config.ramp = float(word[1])
                    print(config.wheel_dia)
                    self.last_word = ""
                    change = True

                elif word[0] == "FTD":
                    config.FW_test_dist = float(word[1])
                    print(config.wheel_dia)
                    self.last_word = ""
                    change = True

                elif word[0] == "BD":
                    config.break_dist = float(word[1])
                    print(config.wheel_dia)
                    self.last_word = ""
                    change = True

                elif word[0] == "FD":
                    config.follow = float(word[1])
                    print(config.wheel_dia)
                    self.last_word = ""
                    change = True

                elif word[0] == "RT":
                    config.ramp_time = float(word[1])
                    print(config.wheel_dia)
                    self.last_word = ""
                    change = True

                elif word[0] == "TD":
                    config.test_dur = float(word[1])
                    print(config.wheel_dia)
                    self.last_word = ""
                    change = True

                else:
                    self.uart.write("Not an option!")
                    time.sleep(1)
                    self.uart.write(text)

            elif len(word) == 1:
                if word[0] == "exit":
                    self.last_word = ""
                    return True

                else:
                    pass

            elif len(word) == 0:
                pass

            else:
                print(len(word))
                self.uart.write("Not an option!")
                time.sleep(1)
                self.uart.write(text)
                self.last_word = ""

    '''Not used, main menu function calls the init function
    in my_bot'''
    def BT_init(self):
        pass

    '''test menu where user can activate the tests on teh robot
    over BT'''
    def BT_Test(self):
        text = "-----------------------------------------------\n"
        text += "Activate test functions.\n"
        text += "----------------------------------------------\n"
        text += "Button test. [BT]\n"
        text += "Tachometer test. [TT]\n"
        text += "IR test. [IR]\n"
        text += "A2D PWM test. [A2D]\n".format(config.break_dist)
        text += "Ramp up test. [RUT]\n"
        text += "Drive forward test. [DFT]\n"
        text += "Exit: exit\n"
        self.uart.write(text)
        exit = False
        self.last_word = ""
        while self.ble.connected:
            if exit:
                self.uart.write(text)
                exit = False

            self.BT_uart()
            if self.last_word == "BT":
                test_submenu.switch_test()
                self.BT_start()
                self.last_word = ""
                exit = True

            elif self.last_word == "TT":
                test_submenu.tach_test()
                self.BT_start()
                self.last_word = ""
                exit = True

            elif self.last_word == "IR":
                test_submenu.ir_test()
                self.BT_start()
                self.last_word = ""
                exit = True

            elif self.last_word == "A2D":
                self.uart.write("\nA2D PWM test Runing!\n")
                test_submenu.Motor_A2D_PWM()
                self.uart.write("\nA2D PWM test done Runing!\n")
                time.sleep(2)
                self.BT_start()
                self.last_word = ""
                exit = True

            elif self.last_word == "RUT":
                test_submenu.Ramping_up()
                self.BT_start()
                self.last_word = ""
                exit = True

            elif self.last_word == "DFT":
                test_submenu.DRV_OL_FW()
                self.BT_start()
                self.last_word = ""
                exit = True

            elif self.last_word == "exit":
                self.last_word = ""
                return

            elif self.last_word == "":
                pass

            else:
                self.uart.write("\nNot an option!\n")
                time.sleep(1)
                self.uart.write(text)
                self.last_word = ""

    '''Mode to drive the robot over BT using the built in
    controller in teh bluefruit app'''
    def BT_Drive(self):
        text = "Gotta Go FAST!\n"
        self.uart.write(text)
        while self.ble.connected:
            self.BT_read()
            self.uart.write(text)
            if self.buttons["5"]:
                drive.throttle(255,255,"FWD")
            elif self.buttons["6"]:
                drive.throttle(255,255,"REV")
            elif self.buttons["7"]:
                drive.throttle(255,0,"FWD")
            elif self.buttons["8"]:
                drive.throttle(0,255,"FWD")
            else:
                drive.throttle(0,0,"REV")
        drive.throttle(0,0,"FWD")

class Pot:
    def __init__(self, pin):
        self.pot = analogio.AnalogIn(pin)

    def Read(self):
        return self.pot.value

class IR_Sensor:
    def __init__(self, pin):
        self.sensor = analogio.AnalogIn(pin)
        self.voltage = 0

    def Get_dist(self):
        smoothed = smooth.update(self.sensor.value)
        voltage = (smoothed * 3.3) / 65536
        distance = ((26.0865 * voltage ** 4)+ (-175.0947 * voltage ** 3)+ (437.4456 * voltage ** 2)+ (-510.3618 * voltage)+ 279.8494)
        return distance * 10

    def volt(self):
        smoothed = smooth.update(self.sensor.value)
        self.voltage = (smoothed * 3.3) / 65536
        return self.voltage

class Smoothing:
    def __init__(self, coeff=0.2):
        self.coeff = coeff
        self.value = 0

    def update(self, input):
        # compute the error between the input and the accumulator
        difference = input - self.value

        # apply a constant coefficient to move the smoothed value toward the input
        self.value += self.coeff * difference

        return self.value  # Return the smoothed value

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
        self.text_to_disp(text_3, 0, 26, 1)
        self.text_to_disp(text_4, 0, 36, 1)
        self.show()

    def del_last(self):
        del self.splash[-1]

    def text_scroll(self, current, STATES,length = 5): # function to scroll throug the menu on oled screen
        #print(length)
        if current == 0:
            top = STATES[length]
            mid = STATES[0]
            bot = STATES[1]
        elif current == length:
            top = STATES[length - 1]
            mid = STATES[length]
            bot = STATES[0]
        else:
            top = STATES[current-1]
            mid = STATES[current]
            bot = STATES[current+1]

        self.text_to_display_3(top,mid,bot)

class run_submenu:
    def __init__(self) -> None:
        self.states = ["Clockwise", "AntiClockwise", "Exit"]
        self.length = len(self.states) - 1
        self.Selected = 0
        self.Current = 0
        self.running = True

    def disp_menu(self):
        '''Main function of Test_submenu class'''
        disp.text_scroll(self.Current, self.states, self.length)
        while self.running:
            if MODE.Read(): # if mode read is True then...
                self.mode_increment()
                disp.text_scroll(self.Selected, self.states, self.length)
                time.sleep(0.2)
            if ESTOP.Read():   # if estop read is True then...
                self.Current = 5
                self.running = False
                my_bot.estop_state()
            if SEL.Read_Lock(): # if select read is True then...
                self.Current = self.Selected
                self.run_tests()
                time.sleep(0.1)

    def mode_increment(self):
        if 0 <= self.Selected < self.length:
            self.Selected += 1
        elif self.Selected >= self.length:
            self.Selected = 0

    def run_tests(self):
        '''A function that runs the selected tests'''
        if self.Current == 0:
            navi = Navigate("C")
            navi.navi()
        if self.Current == 1:
            navi = Navigate("A")
            navi.navi()
        if self.Current == 2:
            self.current = 0
            self.running = False


class Test_submenu:
    def __init__(self) -> None:
        self.states = ["Switch", "Tach", "IR","Color_test", "A2D PWM", "RampUp", "DRV OL FW", "Exit"]
        self.length = len(self.states) - 1
        self.Selected = 0
        self.Current = 0
        self.running = True

    def disp_menu(self):
        '''Main function of Test_submenu class'''
        disp.text_scroll(self.Current, self.states, self.length)
        while self.running:
            if MODE.Read(): # if mode read is True then...
                self.mode_increment()
                disp.text_scroll(self.Selected, self.states, self.length)
                time.sleep(0.2)
            if ESTOP.Read():   # if estop read is True then...
                self.Current = 5
                self.running = False
                my_bot.estop_state()
            if SEL.Read_Lock(): # if select read is True then...
                self.Current = self.Selected
                self.run_tests()
                time.sleep(0.1)

    def mode_increment(self):
        if 0 <= self.Selected < self.length:
            self.Selected += 1
        elif self.Selected >= self.length:
            self.Selected = 0

    def run_tests(self):
        '''A function that runs the selected tests'''
        if self.Current == 0:
            self.switch_test()
            self.disp_menu()
        if self.Current == 1:
            self.tach_test()
            self.disp_menu()
        if self.Current == 2:
            self.ir_test()
            self.disp_menu()
        if self.Current == 3:
            self.Color_test()
            self.disp_menu()
        if self.Current == 4:
            self.Motor_A2D_PWM()
            self.disp_menu()
        if self.Current == 5:
            drive.Ramping_up()
            self.disp_menu()
        if self.Current == 6:
            drive.DRV_OL_FW()
            self.disp_menu()
        if self.Current == 7:
            self.current = 0
            self.running = False

    def switch_test(self):
        if bt.ble.connected:
            bt.uart.write("\nButton test not implemented!\n")
        pass


    def tach_test(self):
        drive.encA.position = 0
        drive.encB.position = 0
        timestamp = time.monotonic()
        if bt.ble.connected:
            bt.uart.write("\nTach test not implemented!\n")
        pass
        while time.monotonic() - timestamp < config.test_dur:
            if ESTOP.Read_Lock() == True:
                break
            dist1 = drive.encA.position * (config.wheel_dia/100)
            dist2 = drive.encB.position * (config.wheel_dia/100)
            drive.throttle(100,100,"FWD")
            disp.text_to_display_2("Dist RW:{0}".format(dist1),"Dist LW:{0}".format(dist2))
        drive.throttle(0,0,0)
        disp.clear()
        disp.show()

    def ir_test(self):
        if bt.ble.connected:
            bt.uart.write("\nIR test not implemented!\n")
        pass
        timestamp = time.monotonic()
        while time.monotonic() - timestamp < config.test_dur:
            distance = ir.Get_dist()
            disp.text_to_display_1("Distance:{0}mm".format(distance))
            if ESTOP.Read_Lock() == True:
                break
        disp.clear()
        disp.show()

    def Color_test(self):
        if bt.ble.connected:
            bt.uart.write("\nColor test not implemented!\n")
        pass
        timestamp = time.monotonic()
        while time.monotonic() - timestamp < config.test_dur:
            RGB_values = color_sense.rgb_values()  # Gets the normalized RGB values
            disp.text_to_display_1("R:{0} G:{1} B:{2}".format(RGB_values[0],RGB_values[1],RGB_values[2]))
            if ESTOP.Read_Lock() == True:
                break
        disp.clear()
        disp.show()

    def Motor_A2D_PWM(self):
        drive.Motor_A2D_PWM()

    def Ramping_up(self):
        drive.Ramping_up()

    def DRV_OL_FW(self):
        drive.DRV_OL_FW()

class Config_submenu:
    def __init__(self) -> None:
        self.states = ["Wheel_Dia", "Ramp", "Test dist", "Break Dist", "Follow", "Ramp time", "Test_duration","Exit"]
        self.length = len(self.states) - 1
        self.Selected = 0
        self.Current = 0
        self.running = True

    def disp_menu(self):
        '''Main function of Config submenu class'''
        disp.text_scroll(self.Current, self.states, self.length)
        while self.running:
            if MODE.Read(): # if mode read is True then...
                self.mode_increment()
                disp.text_scroll(self.Selected, self.states,self.length)
                time.sleep(0.2)

            if ESTOP.Read():   # if estop read is True then...
                self.Current = 5
                self.running = False
                my_bot.estop_state()
            if SEL.Read_Lock(): # if select read is True then...
                self.Current = self.Selected
                time.sleep(0.1)
                self.run_config()

    def mode_increment(self):
        '''A function that increments the Selected variable'''
        if 0 <= self.Selected < self.length:
            self.Selected += 1
        elif self.Selected >= self.length:
            self.Selected = 0

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

        if self.Current == 5:
            self.ramp_time()

        if self.Current == 6:
            self.test_dur()

        if self.Current == 7:
            self.current = 0
            self.running = False

    def wheel(self):
        config.wheel_dia = self.set_val(100,10,"Wheel diameter",config.wheel_dia,"mm")

    def ramp(self):
        config.ramp = int(self.set_val(0, 255, "Ramp value", config.ramp,""))

    def test_dist():
        config.FW_test_dist = self.set_val(100, 3000, "Test distance", config.FW_test_dist,"mm")

    def break_dist():
        config.break_dist = self.set_val(200, 1000, "Break distance", config.break_dist,"mm")

    def follow():
        config.follow = self.set_val(300, 1500, "Follow distance", config.follow,"mm")

    def ramp_time():
        config.ramp_time = self.set_val(0.1, 5, "Ramp time", config.ramp_time,"sec")

    def test_dur():
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

class Navigate:
    def __init__(self,direction="C") -> None:
        self.last_color = "green"
        self.current_color = "green"
        self.moving = "straight"
        self.speed = 60
        self.direction = direction

    def navi(self):
        while True:
            distance = 0
            for _ in range(0,10):
                distance += ir.Get_dist()
            distance = distance/10
            print(distance)
            if distance < 250:
                drive.stop()
                time.sleep(2)
            if ESTOP.Read():
                drive.stop()
                my_bot.estop_state()
                break
            self.make_turns()
            RGB = color_sense.rgb_values()
            #print(RGB)
            if 115 < RGB[0] < 130 and 0 < RGB[1] < 10 and 0 < RGB[2] < 10:
                self.current_color = "red" # (125, 3, 2) ## REDGREEN = (28,26,7)
            elif 0 < RGB[0] < 10 and 15 < RGB[1] < 30 and 15 < RGB[2] < 30:
                self.current_color = "blue" # (6, 27, 27) ## BLUEGREEN = (8,31,21)
            elif 0 < RGB[0] < 15 and 40 < RGB[1] < 50 and 5 < RGB[2] < 15:
                self.current_color = "green" # (8, 45, 11)
            elif 20 < RGB[0] < 35 and 15 < RGB[1] < 25 and 0 < RGB[2] < 10:
                self.current_color = "white" # (29,21,7)
            if self.direction == "C":
                self.is_moving_to()
            else:
                self.is_moving_to2()
            #print(self.moving)
            if self.current_color != self.last_color:
                self.last_color = self.current_color

    def is_moving_to(self):
        if self.current_color == "red":
            if self.last_color == "green":      # green to red is moving left
                self.moving = "left"
            if self.last_color == "white":      # white to red is moving right
                self.moving = "right"
        elif self.current_color == "green":
            if self.last_color == "red":        # red to green is moving right
                self.moving = "right"
            if self.last_color == "blue":       # blue to green is moving left
                self.moving = "left"
            if self.last_color == "green":
                self.moving = "straight"
        elif self.current_color == "blue":
            if self.last_color == "white":      # white to blue is moving left
                self.moving = "left"
            if self.last_color == "green":      # green to blue is moving right
                self.moving = "right"
        elif self.current_color == "white":
            if self.last_color == "blue":
                self.moving = "offright"
            if self.last_color == "red":
                self.moving = "offleft"
            #if self.last_color == "white":
            #    self.stopwatch = time.time()

    def is_moving_to2(self):
        if self.current_color == "red":
            if self.last_color == "green":      # green to red is moving left
                self.moving = "right"
            if self.last_color == "white":      # white to red is moving right
                self.moving = "left"
        elif self.current_color == "green":
            if self.last_color == "red":        # red to green is moving right
                self.moving = "left"
            if self.last_color == "blue":       # blue to green is moving left
                self.moving = "right"
            if self.last_color == "green":
                self.moving = "straight"
        elif self.current_color == "blue":
            if self.last_color == "white":      # white to blue is moving left
                self.moving = "right"
            if self.last_color == "green":      # green to blue is moving right
                self.moving = "left"
        elif self.current_color == "white":
            if self.last_color == "blue":
                self.moving = "offleft"
            if self.last_color == "red":
                self.moving = "offright"
            #if self.last_color == "white":
            #    self.stopwatch = time.time()

    def make_turns(self):
        if self.moving == "straight":
            drive.forward(self.speed)
        if self.moving == "left":
            drive.correct_right(self.speed)
        if self.moving == "right":
            drive.correct_left(self.speed)
        if self.moving == "offleft":
            drive.turn_right(self.speed)
        if self.moving == "offright":
            drive.turn_left(self.speed)

    def make_turns_2(self):
        if self.current_color == "green":
            drive.forward(self.speed)
        if self.current_color == "red":
            drive.correct_right(self.speed)
        elif self.current_color == "blue":
            drive.correct_left(self.speed)
        elif self.current_color == "white":
            if self.moving == "straight":
                drive.spin(self.speed)
        elif self.moving == "left":
            if self.current_color == "white":
                drive.turn_right(0.025,self.speed)
            else:
                drive.forward(self.speed)
        elif self.moving == "right":
            if self.current_color == "white":
                drive.turn_left(0.025,self.speed)
            else:
                drive.forward(self.speed)


class Drive:
    def __init__(self) -> None:
        self.disp = screen()
        self.motor_Ain1 = pwmio.PWMOut(board.D12,frequency = 50)
        self.motor_Ain2 = pwmio.PWMOut(board.D13,frequency = 50)
        self.motor_Bin1 = pwmio.PWMOut(board.D10,frequency = 50)
        self.motor_Bin2 = pwmio.PWMOut(board.D11,frequency = 50)
        self.motor_a = Motor.DCMotor(self.motor_Ain1,self.motor_Ain2)
        self.motor_b = Motor.DCMotor(self.motor_Bin1,self.motor_Bin2)
        self.encA = rotaryio.IncrementalEncoder(board.D8,board.D9)
        self.encB = rotaryio.IncrementalEncoder(board.D7,board.D6)
        #self.config = Conf()

    def pwm_sense(self,A_or_B):
        self.pot1 = pot1.Read() // 256
        self.pot2 = pot2.Read() // 256
        if A_or_B =="A":
            return self.pot1
        if A_or_B =="B":
            return self.pot2

    def drive_left(self,speed):
        self.throttle(speed,0,"FWD")

    def drive_right(self,speed):
        self.throttle(0,speed,"FWD")

    def correct_left(self,speed):
        self.throttle(speed,speed/2,"FWD")

    def reverse(self,speed):
        self.throttle(speed,speed,"REV")

    def spin(self,speed):
        self.stop()
        self.throttle(speed,-speed,"FWD")

    def correct_right(self,speed):
        self.throttle(speed/2,speed,"FWD")

    def turn_left(self,speed):
        #print("Turning Left")
        self.throttle(speed,-speed,"FWD")
        #time.sleep(time_run)

    def turn_right(self,speed):
        #print("Turning Right")
        self.throttle(-speed,speed,"FWD")
        #time.sleep(time_run)

    def forward(self,speed):
        self.throttle(speed,speed,"FWD")

    def stop(self):
        print("Stop!")
        self.throttle(0,0,"")

    def throttle(self, PwmA, PwmB, direction):
        if direction == "REV":
            self.motor_a.throttle = -PwmA/255
            self.motor_b.throttle = -PwmB/255
        elif direction == "FWD":
            self.motor_a.throttle = PwmA/255
            self.motor_b.throttle = PwmB/255
        else:
            self.motor_a.throttle = 0
            self.motor_b.throttle = 0

    def velocity(self):
        motor_radius = config.wheel_dia
        motor_rad = motor_radius/1000
        delta_time = 0
        angular_velocity1 = 0
        angular_velocity2 = 0
        delta_angle = 0
        now = time.monotonic()
        ticks1 = self.encA.position
        ticks2 = self.encB.position
        angle1 = ticks1 * (2 * math.pi / 700)
        angle2 = ticks2 * (2 * math.pi / 700)
        time.sleep(0.1)
        ticks1 = self.encA.position
        ticks2 = self.encB.position
        delta_time = now - time.monotonic()
        delta_angle1 = angle1 - (ticks1 * (2 * math.pi / 700))
        delta_angle2 = angle2 - (ticks2 * (2 * math.pi / 700))
        if delta_time > 0:
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
            if ESTOP.Read_Lock() == True:
                break
            if ir.Get_dist() > config.follow:
                dist1 = self.encA.position * (config.wheel_dia/100)
                dist2 = self.encB.position * (config.wheel_dia/100)
                self.throttle(255,255,"FWD")

            if ir.Get_dist() < config.break_dist:
                self.throttle(0,0,0)

            self.disp.text_to_disp("Distance: {0}mm".format(dist1), 0, 6, 1)
            self.disp.show()
            self.disp.clear()

        self.throttle(0,0,0)

    def Ramping_up(self):
        direction = "FWD"
        duration = config.test_dur
        self.ramp_up()
        self.ramp_down()

    def ramp_up(self):
            timestamp = time.monotonic()
            while time.monotonic() - timestamp < config.test_dur:
                if ESTOP.Read_Lock() == True:
                    break
                pwm1 = self.pwm_sense("A") / 255
                pwm2 = self.pwm_sense("B") / 255
                throttle1 = simpleio.map_range(time.monotonic()-timestamp, 0, config.test_dur, 0, pwm1)
                throttle2 = simpleio.map_range(time.monotonic()-timestamp, 0, config.test_dur, 0, pwm2)
                self.motor_a.throttle = throttle1
                self.motor_b.throttle =throttle2
                a1,l1,a2,l2 =self.velocity()
                self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
            self.disp.clear()
            self.disp.show()

    def ramp_down(self):
        timestamp = time.monotonic()
        while time.monotonic() - timestamp < config.test_dur:
            if ESTOP.Read_Lock() == True:
                break
            pwm1 = self.pwm_sense("A") / 255
            pwm2 = self.pwm_sense("B") / 255
            throttle1 = simpleio.map_range(time.monotonic() - timestamp, 0, config.test_dur, pwm1, 0)
            throttle2 = simpleio.map_range(time.monotonic() - timestamp, 0, config.test_dur, pwm2, 0)
            self.motor_a.throttle = throttle1
            self.motor_b.throttle =throttle2
            a1,l1,a2,l2 =self.velocity()
            self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
        self.disp.clear()
        self.disp.show()
        self.throttle(0,0,0)


    def Motor_A2D_PWM(self):
                duration = config.test_dur
                timestamp = time.monotonic()
                while time.monotonic() - timestamp < duration:
                    if ESTOP.Read_Lock() == True:
                        break
                    self.motor_a.throttle = self.pwm_sense("A") / 255
                    self.motor_b.throttle = self.pwm_sense("B") / 255
                    a1,l1,a2,l2 =self.velocity()
                    self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
                self.disp.clear()
                self.disp.show()
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
        self.i2c = board.I2C()

class RGB: # class to be able to call on the rgb sensor
    def __init__(self):
        self.sensor = adafruit_tcs34725.TCS34725(board.I2C())
        self.sensor.integration_time = 10
        self.sensor.gain = 16

    def raw_data(self):
        return self.sensor.color_raw #returns the raw values, we use clear value

    def rgb_values(self):
        return self.sensor.color_rgb_bytes # Gives us normalised RGB value which takes in the clear value
    def temp(self):
        return self.sensor.color_temperature #returns the the heat of the color in kelvin
    def lux(self):
        return self.sensor.lux # light intensity


MODE = Button(board.D3)                                    # Mode button defined
ESTOP = Button(board.D2)                                   # Estop button defined
SEL = Button(board.D4)

pot1 = Pot(board.A1)
pot2 = Pot(board.A2)

smooth = Smoothing()
ir = IR_Sensor(board.A0)
disp = screen()
color_sense = RGB()
drive = Drive()

bt = BT_buttons()

config = Conf()
config_submenu = Config_submenu()
test_submenu = Test_submenu()
my_bot = MainMenu()
my_bot.run_program()
