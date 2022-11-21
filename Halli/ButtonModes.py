import board
import digitalio
# import time
import neopixel
import asyncio

# Create a mode called "Switch Test".  
# Connect two buttons to GPIO pins and debounce the circuit. 
# Observe the one of the buttons bouncing with an oscilloscope.  
# Mark one button as 'MODE' and one button as 'ESTOP'. 
# Write non-blocking code that allows you to make two LEDs stay lit 
# for 1 second when their associated button is pressed.  
# One way to think about this is that the buttons are keys on a piano 
# and the light is the sound that plays when you push the key.



mode = "Start"
mode_change = False

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

neopix = neopixel.NeoPixel(board.NEOPIXEL, 1)
neopix.brightness = 1

MODEswitch = digitalio.DigitalInOut(board.D2)
MODEswitch.direction = digitalio.Direction.INPUT
MODEswitch.pull = digitalio.Pull.UP

Eswitch = digitalio.DigitalInOut(board.D3)
Eswitch.direction = digitalio.Direction.INPUT
Eswitch.pull = digitalio.Pull.UP

modes = ["Start", "Ready", "Drive", "Call mom"]

# changeMode changes global mode variable, modes variable stores mode names so that it is easier to change mode names. global mode_change variable keeps track of if mode has changed since 
# last button press but is not used in this function. series of if statements then execute what ever the selected mode does

def changeMode(n=0):
    ''' Function that changes global mode variable, n variable determines which button was pressed '''
    global modes
    global mode
    global mode_change 
    mode_change = True
    print("change mode function")
    if mode == modes[0]:
        mode = modes[1]
        mode_execute()
    elif mode == modes[1]:
        mode = modes[2]
        mode_execute()
    elif mode == modes[2]:
        mode = modes[3]
        mode_execute()
    if n != 0:
        mode = modes[0]
        mode_execute()

async def button_read():
''' Function reads the buttons, and if a button is pressed the changemode function is called and global variable mode changes '''
    print("button read function")
    mode_pressed = False
    e_button_pressed = False
    while True:
        if mode_pressed:
            print("Mode is pressed!")
            changeMode()
            mode_pressed = False
            return
        elif e_button_pressed:
            print("E-button is pressed!")
            changeMode(1)
            e_button_pressed = False
            return
        if MODEswitch.value is False:
            mode_pressed = True
            await asyncio.sleep(0.4)
        if Eswitch.value is False:
            e_button_pressed = True
            await asyncio.sleep(0.4)

async def print_loop(string_print):
''' Helper function that only prints a given string forever (will not be used)'''
    print("Print loop function")
    while True:
        print(string_print)
        await asyncio.sleep(1)
    
async def mode_execute():
    print("mode execute function")
    global mode
    global modes
    if mode == modes[0]:
        task = asyncio.create_task(print_loop(modes[0]))
    elif mode == modes[1]:
        task = asyncio.create_task(print_loop(modes[1]))
    elif mode == modes[2]:
        task = asyncio.create_task(print_loop(modes[2]))
    elif mode == modes[3]:
        task = asyncio.create_task(print_loop(modes[3]))
    await asyncio.gather(task)


async def main():
    while True:
        print("The mode is: " + mode)
        task_1 = asyncio.create_task(button_read())
        await asyncio.gather(task_1)


if __name__ == "__main__":
    asyncio.run(main())