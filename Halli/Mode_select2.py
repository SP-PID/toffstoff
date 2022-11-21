import time
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



# Initialize the Mode button
MODE = digitalio.DigitalInOut(board.D3)
MODE.direction = digitalio.Direction.INPUT
MODE.pull = digitalio.Pull.UP

# Initialize the ESTOP button
ESTOP = digitalio.DigitalInOut(board.D2)
ESTOP.direction = digitalio.Direction.INPUT
ESTOP.pull = digitalio.Pull.UP

# Initialize the Select button
SEL = digitalio.DigitalInOut(board.D4)
SEL.direction = digitalio.Direction.INPUT
SEL.pull = digitalio.Pull.UP

i2c = board.I2C()

displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128  # Define display width
HEIGHT = 64  # Define display hight
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group()  # Variable for what to display
display.show(splash)  # Refreshes the screen
# define screen

# Class screen, contains operations for the oled screen
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
        
    def text_to_display_1(self, text_to_show):
        disp.clear()
        disp.text_to_disp(text_to_show, 0, 6, 2)
        disp.show()

    def text_to_display_3(self, text_1, text_2, text_3):
        disp.clear()
        disp.text_to_disp(text_1, 0, 6, 2)
        disp.text_to_disp(text_2, 0, 26, 2)
        disp.text_to_disp(text_3, 0, 46, 2)
        disp.show()

# Declare useful variables
STATES = ["START", "INIT", "CONF", "TEST", "RUN", "ESTOP"]
CURRENT_STATE = STATES[0]
SELECTED_STATE = STATES[0]


# STATES maybe change to class methods
def start():
    ''' Function that runs code for the START state.'''
    disp.text_to_display_3("START", "mode", "selected!")
    time.sleep(2)

def init():
    ''' Function that runs code for the INIT state.'''
    disp.text_to_display_3("INIT", "mode", "selected!")
    self_check()
    time.sleep(2)

def config():
    ''' Function that runs code for the CONF state.'''
    disp.text_to_display_3("CONF", "mode", "selected!")
    time.sleep(2)

def test():
    ''' Function that runs code for the TEST state.'''
    disp.text_to_display_3("TEST", "mode", "selected!")
    time.sleep(2)

def run():
    ''' Function that runs code for the RUN state.'''
    disp.text_to_display_3("RUN", "mode", "selected!")
    drive()
    time.sleep(2)

def estop():
    ''' Function that runs code for the ESTOP state.'''
    # End the current process and return to start state.
    global CURRENT_STATE                                    # Estop changes global variables to Start state
    global SELECTED_STATE
    global STATES
    print("ESTOP mode selected!")
    CURRENT_STATE = STATES[0]
    SELECTED_STATE = STATES[0]

def self_check():
    ''' Function runs a self check, checks if all components are present and working correctly'''
    print("CHECKING MYSELF!")

def drive():
    ''' Function used for driving the robot '''
    print("driving....")

def select_mode(selected_mode):
    ''' Function that executes the select mode when user presses select '''
    if selected_mode == STATES[0]:
        start()
    if selected_mode == STATES[1]:
        init()
    if selected_mode == STATES[2]:
        config()
    if selected_mode == STATES[3]:
        test()
    if selected_mode == STATES[4]:
        run()
    if selected_mode == STATES[5]:
        estop()

def next_mode(old_state):
    ''' Function that determines what mode is next after a given mode '''
    global STATES
    ind = STATES.index(old_state)
    if ind == 5:
        return STATES[ind]
    return STATES[ind + 1]


def run_program():
    global CURRENT_STATE
    global STATES
    global SELECTED_STATE
    MODE_pressed = False
    Old_state = SELECTED_STATE
    ESTOP_pressed = False
    SEL_pressed = False
    disp.text_to_display_1(SELECTED_STATE)
    while True:
        disp.text_to_display_1(SELECTED_STATE)
        if MODE_pressed:
            Old_state = SELECTED_STATE
            SELECTED_STATE = next_mode(Old_state)
            MODE_pressed = False
            disp.text_to_display_1(SELECTED_STATE)
        if ESTOP_pressed:
            disp.text_to_display_1(STATES[5])           # display ESTOP on the Oled screen
            time.sleep(1)
            estop()
            ESTOP_pressed = False
        if SEL_pressed:
            disp.text_to_display_1(SELECTED_STATE + " selected!")
            time.sleep(1)
            CURRENT_STATE = SELECTED_STATE
            select_mode(SELECTED_STATE)
            SEL_pressed = False
        if MODE.value is False:
            MODE_pressed = True
            time.sleep(0.4)
        if ESTOP.value is False:
            ESTOP_pressed = True
            time.sleep(0.4)
        if SEL.value is False:
            SEL_pressed = True
            time.sleep(0.4)
        


def main():
    global disp
    disp = screen()
    run_program()


if __name__ == "__main__":
    main()

