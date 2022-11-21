from operator import index
import time
import board
import digitalio

STATES = ["START", "INIT", "CONF", "TEST", "RUN", "ESTOP"]
CURRENT_STATE = "OFF"

# Initialize the Mode button
MODE = digitalio.DigitalInOut(board.D4)
MODE.direction = digitalio.Direction.INPUT
MODE.pull = digitalio.Pull.UP

# Initialize the ESTOP button
ESTOP = digitalio.DigitalInOut(board.D3)
ESTOP.direction = digitalio.Direction.INPUT
ESTOP.pull = digitalio.Pull.UP

# Initialize the SEL button
SEL = digitalio.DigitalInOut(board.D2)
SEL.direction = digitalio.Direction.INPUT
SEL.pull = digitalio.Pull.UP

def get_time():
    ''' Function that returns the current time '''
    return time.time()

def next_mode(old_state):
    global STATES
    ind = STATES.index(old_state)
    return STATES[ind + 1]



def piano():
    ''' The main function of the program '''
    global CURRENT_STATE
    global STATES
    MODE_pressed = False
    New_mode = ""
    ESTOP_pressed = False
    SEL_pressed = False
    CURRENT_STATE = STATES[0]
    Old_mode = CURRENT_STATE
    while True:
        # If MODE is pressed, Variable New_mode will be updated with the next mode to be selected
        if MODE_pressed:
            Old_mode = New_mode
            New_mode = next_mode(Old_mode)
            MODE_pressed = False
        elif ESTOP_pressed:
        # If ESTOP is pressed, CURRENT_STATE variable will immediately be changed to ESTOP
            CURRENT_STATE = STATES[5]
            ESTOP_pressed = False
        # if SEL is pressed, the New_mode variable will be selected and CURRENT_STATE variable is updated
        elif SEL_pressed:
            # Do something
            ESTOP_pressed = False
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
    piano()


if __name__ == "__main__":
    main()



# def main(): # Here is our main function
#     global modes # define modes as global
#     global disp # defines disp as global variable
#    modes = 0 # sets  starting value as 0
#    disp = screen() # initiates 

#    while True:
#        if modes == 0 :
#            start() # Starts the program goes into Start mode
#        if modes == 1:
#            if IR_test(): # If IR is done running continue to wait
#                continue
#            Wait() # Test to see if pressed to go to the next mode
#        elif modes == 2:
#            if Color_match(): # If Color match is True 
#                continue
#            Wait() # waiting for input
#        elif modes == 3:
#            if Tachometer(): # Call on the encoder function
#                continue
#            modes = 0  # Sends it to Start mode

main() # Our main function