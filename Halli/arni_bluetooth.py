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
import board
import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_airlift.esp32 import ESP32

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket

esp32 = ESP32() # DEFAULT
adapter = esp32.start_bluetooth()
ble = BLERadio(adapter)
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

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
        #STATES = ["START", "INIT", "CONF", "TEST", "RUN", "ESTOP"]
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

def BT_read(buttons):
    if uart.in_waiting:
            packet = Packet.from_stream(uart)

            if isinstance(packet, ButtonPacket):
                if packet.button not in buttons:
                    buttons[packet.button] = False

                buttons[packet.button] = packet.pressed
    return buttons
buttons = {}
for key in range(9):
    buttons[str(key)] = False

class BT_buttons():
    def __init__(self):
        self.buttons = {}
        for key in range(9):
            self.buttons[str(key)] = False

    def BT_start(self):
        ble.start_advertising(advertisement)
        print("waiting to connect")
        while not ble.connected:
            pass
        print("connected: trying to read input")

    def BT_read(self):

        if uart.in_waiting:
                packet = Packet.from_stream(uart)

                if isinstance(packet, ButtonPacket):
                    if packet.button not in buttons:
                        self.buttons[packet.button] = False

                    self.buttons[packet.button] = packet.pressed

    def BT_Button_read(self, button):
        return self.buttons[button]




disp = screen()

while True:

    ble.start_advertising(advertisement)
    print("waiting to connect")
    while not ble.connected:
        pass
    print("connected: trying to read input")

    while ble.connected:
        buttons = BT_read(buttons)

        if buttons["1"]:
            disp.text_to_disp("1",90,8,2)
        else:
            disp.text_to_disp("1",90,8,1)

        if buttons["2"]:
            disp.text_to_disp("2",110,8,2)
        else:
            disp.text_to_disp("2",110,8,1)

        if buttons["3"]:
            disp.text_to_disp("3",90,32,2)
        else:
            disp.text_to_disp("3",90,32,1)

        if buttons["4"]:
            disp.text_to_disp("4",110,32,2)
        else:
            disp.text_to_disp("4",110,32,1)

        if buttons["5"]:
            disp.text_to_disp("^",27,16,3)
        else:
            disp.text_to_disp("^",32,8,1)

        if buttons["6"]:
            disp.text_to_disp("v",27,48,3)
        else:
            disp.text_to_disp("v",32,48,1)

        if buttons["7"]:
            disp.text_to_disp("<",0,26,3)
        else:
            disp.text_to_disp("<",5,28,1)

        if buttons["8"]:
            disp.text_to_disp(">",50,26,3)
        else:
            disp.text_to_disp(">",55,28,1)

        disp.show()
        disp.clear()