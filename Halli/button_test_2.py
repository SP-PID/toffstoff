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

def get_time():
    return time.time()

#MODE_button = Button(board.D3)
#ESTOP_button = Button(board.D2)
#SEL_button = Button(board.D4)

def button_test():
    test_ok = True
    buttons = [board.D2, board.D3, board.D4]
    modes = ["Estop", "Mode", "Select"]
    for i in range(0,3):
        button_test = Button(buttons[i])
        time_start = get_time()
        print("Press " + modes[i] + " button")
        while True:  
            if button_test.Read():
                print(modes[i] +" ok!")
                break
            if (time_start + 3) < get_time():
                test_ok = False
                break

    print("Test ok: " + str(test_ok))

button_test()