# Create a mode called "Switch Test".  Connect two buttons to GPIO 
# pins and debounce the circuit.
# Observe the one of the buttons bouncing with an oscilloscope.  --- sleppt
# Mark one button as 'MODE' and one button as 'ESTOP'.  rauður er ESTOP og grænn er MODE
# Write non-blocking code that allows you to make two LEDs stay lit 
# for 1 second when their associated button is pressed.  
# One way to think about this is that the buttons are keys on a piano 
# and the light is the sound that plays when you push the key. 

import time
import board
import digitalio

class Button:
    def __init__(self, pin):
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

    def Read(self):
        return not self.button.value

MODE_button = Button(board.D3)
ESTOP_button = Button(board.D2)
SEL_button = Button(board.D4)
def get_time():
    return time.time()


def piano():
    ''' Function that runs the main function of the program '''
    test_ok = False
    time_start = get_time()
    while True:
        if MODE_button.Read():
            print("Press MODE")
            test_ok = True
            break
        if (time_start + 3) > get_time():
            break
    time_start = get_time()
    time_end = time_start + 3
    while True:   
        if ESTOP_button.Read():
            print("Press ESTOP")
            test_ok = True
            break
        if (time_start + 3) > get_time():
            break
    time_start = get_time()
    time_end = time_start + 3
    while True:
        if SEL_button.Read():
            print("Press SELECT")
            test_ok = True
            break
        if (time_start + 3) > get_time():
            break


def main():
    piano()


if __name__ == "__main__":
    main()