import board
import digitalio
import neopixel
import asyncio
import time

neopix = neopixel.NeoPixel(board.NEOPIXEL, 1)
neopix.brightness = 1

MODEswitch = digitalio.DigitalInOut(board.D2)
MODEswitch.direction = digitalio.Direction.INPUT
MODEswitch.pull = digitalio.Pull.UP

Eswitch = digitalio.DigitalInOut(board.D3)
Eswitch.direction = digitalio.Direction.INPUT
Eswitch.pull = digitalio.Pull.UP
current_mode = "1"
new_mode = False

async def mode_change():
    # print("button read function")
    mode_pressed = False
    e_button_pressed = False
    while True:
        if mode_pressed:
            # print("Mode is pressed!")
            pickMode()
            mode_pressed = False
            return
        elif e_button_pressed:
            # print("E-button is pressed!")
            pickMode(1)
            e_button_pressed = False
            return
        if MODEswitch.value is False:
            mode_pressed = True
            await asyncio.sleep(0.4)
        if Eswitch.value is False:
            e_button_pressed = True
            await asyncio.sleep(0.4)


def pickMode(n=0):
    global current_mode
    global new_mode
    if current_mode == "1":
        current_mode = "2"
        new_mode = True
    elif current_mode == "2":
        current_mode = "3"
        new_mode = True
    elif current_mode == "3":
        current_mode = "4"
        new_mode = True
    elif n == 0 and current_mode == "4":
        return
    if n!=0:
        current_mode = "1"    
        new_mode = True
    return

async def blink_led():
    global current_mode
    global new_mode
    if current_mode == "1":
        neopix[0] = (255, 0, 0)
        neopix.brightness = 1
        await asyncio.sleep(1)
        neopix.brightness = 0
    elif current_mode == "2":
        neopix[0] = (255, 0, 255)
        for _ in range(0, 5, 1):
            neopix.brightness = 1
            await asyncio.sleep(0.5)
            neopix.brightness = 0
            await asyncio.sleep(0.5)
        if new_mode:
            new_mode = False
            return
    else:
        neopix[0] = (0, 255, 0)
        return

async def main():
    while True:
        print("The mode is: " + current_mode)
        task_2 = asyncio.create_task(blink_led())
        task_1 = asyncio.create_task(mode_change())
        await asyncio.gather(task_1, task_2)

if __name__ == "__main__":
    asyncio.run(main())
