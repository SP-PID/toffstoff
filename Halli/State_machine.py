

STATES = ["START", "INIT", "CONF", "TEST", "RUN", "ESTOP"]
CURRENT_STATE = STATES[0]
SELECTED_STATE = STATES[0]

# STATES:
def start():
    print("START mode selected!")

def init():
    print("INIT mode selected!")
    self_check()

def config():
    print("CONF mode selected!")

def test():
    print("TEST mode selected!")

def run():
    print("RUN mode selected!")

def estop():
    global CURRENT_STATE
    global SELECTED_STATE
    global STATES
    print("ESTOP mode selected!")
    CURRENT_STATE = STATES[0]
    SELECTED_STATE = STATES[0]

def self_check():
    print("CHECKING MYSELF!")

def drive():
    print("")
# executes selected mode
def select_mode(selected_mode):
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
    global STATES
    ind = STATES.index(old_state)
    if ind == 5:
        return STATES[ind]
    return STATES[ind + 1]

def piano():
    global CURRENT_STATE
    global STATES
    global SELECTED_STATE
    MODE_pressed = False
    Old_state = SELECTED_STATE
    ESTOP_pressed = False
    SEL_pressed = False
    while True:
        print("The current state is: " + CURRENT_STATE)
        print("Selected mode is: " + SELECTED_STATE)
        button = int(input("press button: "))
        if button == 1:
            print("MODE was pressed!")
            MODE_pressed = True
        if button == 2:
            print("ESTOP was pressed!")
            ESTOP_pressed = True
        if button == 3:
            print("SELECT was pressed!")
            SEL_pressed = True
        if MODE_pressed:
            Old_state = SELECTED_STATE
            SELECTED_STATE = next_mode(Old_state)
            MODE_pressed = False
        elif ESTOP_pressed:
            estop()
            ESTOP_pressed = False
        elif SEL_pressed:
            CURRENT_STATE = SELECTED_STATE
            select_mode(SELECTED_STATE)
            ESTOP_pressed = False

def main():
    piano()


if __name__ == "__main__":
    main()

