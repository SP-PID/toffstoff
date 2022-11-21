import board
import adafruit_fxos8700
import adafruit_fxas21002c
import adafruit_bus_device
import time
import neopixel
import terminalio
import displayio
import adafruit_displayio_ssd1306
from adafruit_display_text import label

# Global variable that keeps track of the text to display
disp_text = "Level"

def display_change(text = "Level"):
    ''' Function that handles the display '''
    displayio.release_displays()
    i2c = board.I2C()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
    # Set display parameters
    WIDTH = 128
    HEIGHT = 64 
    BORDER = 0
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
    # Make the display context
    splash = displayio.Group()
    display.show(splash)
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=20, y=HEIGHT//2, scale = 3)
    splash.append(text_area)

def falls_which_way(LR, FB, UD):
    ''' Function determines which way the robot is leaning or if it is upside down, returns string'''
    # LR is for left and right, FB is for front and back and UD is for up and down
    if LR < -4:
        return "Left"
    elif LR > 4:
        return "Right"
    if FB < -4:
        return "Back"
    elif FB > 4:
        return "Fwd"
    elif UD < 0:
        return "Down"
    else:
        return "Level"

def main():
    global disp_text
    # sensor setup
    i2c = board.I2C()
    fxos = adafruit_fxos8700.FXOS8700(i2c)
    # display setup
    display_change()
    # neopixel start
    neopix = neopixel.NeoPixel(board.NEOPIXEL, 1)
    neopix.brightness = 1
    acceleration = fxos.accelerometer
    # useful variables to track status of robot
    isLevel = True
    oldMsg = "Level"
    newMsg = "Level"
    while True:
        acceleration = fxos.accelerometer
        # 10 is straight up, -10 would be stragiht down anything else is not level
        if acceleration[2] < 9: 
            isLevel = False
        else:
            isLevel = True
        if isLevel:
            neopix[0] = (0, 0, 255)
        else:
            neopix[0] = (255, 0, 0)
        # Checks orientation each time loop is repeated, saves a new message in variable
        newMsg = falls_which_way(acceleration[0], acceleration[1], acceleration[2])
        disp_text = newMsg
        # in order to not update the screen each round old and new messages are compared
        if oldMsg != disp_text:
            display_change(disp_text)
            oldMsg = newMsg
        time.sleep(0.2)


if __name__ == "__main__":
    main()
