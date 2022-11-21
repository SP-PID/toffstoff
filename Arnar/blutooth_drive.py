
from turtle import distance
import rotaryio
import time
import board
import displayio
import terminalio
import adafruit_displayio_ssd1306
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
import adafruit_tcs34725
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_airlift.esp32 import ESP32

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
Neo = neopixel.NeoPixel(board.NEOPIXEL, 1)
Neo.brightness = 1  # Sets NeoPixel brightness


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
        i2c_test_ok = self.i2c_test() # Tests the i2c Bus
        time.sleep(2)
        disp.text_to_display_3("i2c","check","OK")
        time.sleep(2)
        disp.text_to_display_3("Starting","button","test.")
        time.sleep(2)
        button_test_ok = self.button_test() # Tests the buttons
        if i2c_test_ok and button_test_ok:  # if all test are ok then display message
            disp.text_to_display_3("All","Tests","OK")
        elif i2c_test_ok and not button_test_ok:    # if button test fail then display message
            disp.text_to_display_3("Button","Test","FAIL")
        elif not i2c_test_ok and button_test_ok:    # if i2c test fail then display message
            disp.text_to_display_3("I2c","Test","FAIL")
        time.sleep(3)
        disp.text_scroll(self.SEL_STATE, self.STATES)       # reset the menu on oled screen after 3 sec

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
            while True:
                if test.Read():
                    break       # if test is succesful then break loop
                if (time_start + 3) < time.time():
                    is_ok = False # test fail if time exceeds 3 seconds
                    break
        return is_ok

    def run_state(self):
        '''Function used to command robot to drive '''
        robot_drive.throttle(255, 255, "FWD")       # go forward for two seconds and then stop           
        time.sleep(2)
        robot_drive.throttle(0, 0, "FWD")

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
        bt = BT_buttons()
        bt.BT_start()

        disp.show()
        disp.clear()
        while bt.ble.connected:
            bt.BT_read()

            if bt.BT_Button_read("5") and bt.BT_Button_read("8"):
                drive.throttle(50,255,"FWD")
            
            elif bt.BT_Button_read("5") and bt.BT_Button_read("7"):
                drive.throttle(255,50,"FWD")

            elif bt.BT_Button_read("5"):
                drive.throttle(255,255,"FWD")
            
            else:
                drive.throttle(0,0,"FWD")
            
            if ESTOP.Read_Lock():
               bt.BT_stop()
               return

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
                pass
            return True
        return False

class BT_buttons():
    def __init__(self):
        self.buttons = {}
        for key in range(9):
            self.buttons[str(key)] = False

        self.esp32 = ESP32()
        self.adapter = self.esp32.start_bluetooth()
        self.ble = BLERadio(self.adapter)
        self.uart = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart)

    def BT_start(self):
        self.ble.start_advertising(self.advertisement)
        print("waiting to connect")
        while not self.ble.connected:
            pass
        print("connected: trying to read input")

    def BT_stop(self):
        self.ble.stop_advertising(self.advertisement)

    
    def BT_read(self):
        if self.uart.in_waiting:
            print("n")
            packet = Packet.from_stream(self.uart)

            if isinstance(packet, ButtonPacket):
                if packet.button not in self.buttons:
                    self.buttons[packet.button] = False

                self.buttons[packet.button] = packet.pressed
                return

        else:
            return

    def BT_Button_read(self, button):
        return self.buttons[button]
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

class Pot:
    def __init__(self, pin):
        self.pot = analogio.AnalogIn(pin)

    def Read(self):
        return self.pot.value

class IR_Sensor:
    def __init__(self, pin):
        self.sensor = analogio.AnalogIn(pin)

    def Get_dist(self):
        smoothed = smooth.update(self.sensor.value)
        voltage = (smoothed * 3.3) / 65536
        distance = ((26.0865 * voltage ** 4)+ (-175.0947 * voltage ** 3)+ (437.4456 * voltage ** 2)+ (-510.3618 * voltage)+ 279.8494)
        return distance * 10

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
        self.text_to_disp(text_to_show, 0, 6, 1)
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
        print(length)
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
        if self.Current == 1:
            self.tach_test()
        if self.Current == 2:
            self.ir_test()
        if self.Current == 3:
            self.Color_test()
        if self.Current == 4:
            self.Motor_A2D_PWM()
        if self.Current == 5:
            drive.Ramping_up()
        if self.Current == 6:
            drive.DRV_OL_FW()
        if self.Current == 7:
            self.current = 0
            self.running = False

    def switch_test(self):
        pass

    def tach_test(self):
        timestamp = time.monotonic()
        while time.monotonic() - timestamp < config.test_dur:
            dist1 = self.encA.position * (config.wheel_dia/100)
            dist2 = self.encB.position * (config.wheel_dia/100)
            disp.text_to_display_1("Dist RW:{0} Dist LW {1}".format(dist1,dist2))

    def ir_test(self):
        timestamp = time.monotonic()
        while time.monotonic() - timestamp < config.test_dur:
            distance = ir.Get_dist()
            disp.text_to_display_1("Distance:{0}mm^2".format(distance))
            if ESTOP.Read_Lock() == True:
                break
        self.disp.show()
        self.disp.clear()

    def Color_test(self):
        timestamp = time.monotonic()
        while time.monotonic() - timestamp < config.test_dur: 
            RGB_values = color_sense.rgb_values()  # Gets the normalized RGB values
            disp.text_to_display_1("R: {0} G:{1} B: {2}".format(RGB_values[0],RGB_values[1],RGB_values[2]))
            if ESTOP.Read_Lock() == True:
                break
        self.disp.show()
        self.disp.clear()
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
        
class Drive:
    def __init__(self) -> None:
        self.disp = screen()
        self.motor_Ain1 = pwmio.PWMOut(board.D12,frequency = 50)
        self.motor_Ain2 = pwmio.PWMOut(board.D13,frequency = 50)
        self.motor_Bin1 = pwmio.PWMOut(board.D5,frequency = 50)
        self.motor_Bin2 = pwmio.PWMOut(board.D11,frequency = 50)
        self.motor_a = Motor.DCMotor(self.motor_Ain1,self.motor_Ain2)
        self.motor_b = Motor.DCMotor(self.motor_Bin1,self.motor_Bin2)
        self.encA = rotaryio.IncrementalEncoder(board.D6,board.D7)
        self.encB = rotaryio.IncrementalEncoder(board.D8,board.D9) 
        #self.config = Conf()  

    def pwm_sense(self,A_or_B):
        self.pot1 = pot1.Read() // 256
        self.pot2 = pot2.Read() // 256
        if A_or_B =="A":
            return self.pot1
        if A_or_B =="B":
            return self.pot2
    
    def throttle(self, PwmA, PwmB, direction): 
        if direction == "REV":
            self.motor_a.throttle = PwmA/255
            self.motor_b.throttle = PwmB/255
        elif direction == "FWD":
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
    
    def Ramping_up(self,pwm):
        direction = "FWD"
        duration = self.config.test_dur
        def ramp_up(direction,duration):
                timestamp = time.monotonic()
                while time.monotonic() - timestamp < duration:
                    if ESTOP.Read_Lock() == True:
                        break
                    pwm1=self.pwm_sense("A") / 255
                    pwm2 =self.pwm_sense("B") / 255
                    throttle1 = simpleio.map_range(time.monotonic()-timestamp, 0, duration, pwm1, 0)
                    throttle2 = simpleio.map_range(time.monotonic()-timestamp, 0, duration, pwm2, 0)
                    self.motor_a.throttle = throttle1
                    self.motor_b.throttle =throttle2
                    a1,l1,a2,l2 =self.velocity()
                    self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
                self.disp.clear()
                self.disp.show()
                
        def ramp_down(direction, duration):
            timestamp = time.monotonic()
            while time.monotonic() - timestamp < duration:
                if ESTOP.Read_Lock() == True:
                    break
                pwm1=self.pwm_sense("A") / 255
                pwm2 =self.pwm_sense("B") / 255
                throttle1 = simpleio.map_range(time.monotonic()-timestamp, 0, duration, pwm1, 0)
                throttle2 = simpleio.map_range(time.monotonic()-timestamp, 0, duration, pwm2, 0)
                self.motor_a.throttle = throttle1
                self.motor_b.throttle =throttle2
                a1,l1,a2,l2 =self.velocity()
                self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
            self.disp.clear()
            self.disp.show()
        ramp_up(direction,duration,pwm)
        ramp_down(direction,duration,pwm)
        self.throttle(0,0,0)

    def Motor_A2D_PWM(self):
                duration = config.test_dur
                timestamp = time.monotonic()
                while time.monotonic() - timestamp < duration:
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




MODE = Button(board.D3)                                    # Mode button defined
ESTOP = Button(board.D2)                                   # Estop button defined
SEL = Button(board.D4)

pot1 = Pot(board.A1)
pot2 = Pot(board.A2)
color_sense = RGB()  # Initiates the class for the color sensor
smooth = Smoothing()
ir = IR_Sensor(board.A0)
disp = screen()

drive = Drive()

config = Conf()
config_submenu = Config_submenu()
test_submenu = Test_submenu()
my_bot = MainMenu()
my_bot.run_program()
