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

# Initialize clear led
led_1 = digitalio.DigitalInOut(board.D5)
led_1.direction = digitalio.Direction.OUTPUT

# Initialize red led
led_2 = digitalio.DigitalInOut(board.D4)
led_2.direction = digitalio.Direction.OUTPUT

# Initialize the Mode button
MODE = digitalio.DigitalInOut(board.D3)
MODE.direction = digitalio.Direction.INPUT
MODE.pull = digitalio.Pull.UP

# Initialize the ESTOP button
ESTOP = digitalio.DigitalInOut(board.D2)
ESTOP.direction = digitalio.Direction.INPUT
ESTOP.pull = digitalio.Pull.UP

def get_time():
    ''' Function that returns the current time '''
    return time.time()

def piano():
    ''' Function that runs the main function of the program '''
    time_MODE_OFF = 0
    time_ESTOP_OFF = 0
    MODE_pressed = False
    ESTOP_pressed = False
    while True:
        # If MODE or ESTOP is pressed, perform action
        if MODE_pressed:
            led_1.value = True
            time_MODE_OFF = get_time() + 1
            MODE_pressed = False
        elif ESTOP_pressed:
            led_2.value = True
            time_ESTOP_OFF = get_time() + 1
            ESTOP_pressed = False
        # Turn off LEDs if a second has passed since they were turned on
        if get_time() > time_MODE_OFF:
            led_1.value = False
        if get_time() > time_ESTOP_OFF:
            led_2.value = False
        # Actions below allow for user to have time to let go of button before loop continues
        if MODE.value is False:
            MODE_pressed = True
            time.sleep(0.4)
        if ESTOP.value is False:
            ESTOP_pressed = True
            time.sleep(0.4)

def main():
    piano()


if __name__ == "__main__":
    main()