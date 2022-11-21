import board
import adafruit_mpl3115a2
import time
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import neopixel
from rainbowio import colorwheel
i2c = board.I2C()
displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=62)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
sensor.sealevel_pressure = 101000
Min = 24.0
Max = 25.0
neopix = neopixel.NeoPixel(board.NEOPIXEL, 1)
neopix.brightness = 1

while True:
    
    # Make the display context
    splash = displayio.Group()
    
    # altitude
    altitude = sensor.altitude
    text_altitude = "Altitude: {0:0.3f}m".format(altitude)
    text_area_altitude = label.Label(terminalio.FONT, text=text_altitude, color=0xFFFF00, x=20, y=18)
    splash.append(text_area_altitude)
    # Temperature
    # sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
    temperature = sensor.temperature
    text = "Temp: {0:0.3f} °C".format(temperature)
    text_area_temp = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=8)
    splash.append(text_area_temp)
    # sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
    # pressure
    pressure = sensor.pressure
    text_pressure = "Pressure: {0:0.8f}p".format(pressure)
    text_area_pressure = label.Label(terminalio.FONT, text=text_pressure, color=0xFFFF00, x=20, y=28)
    splash.append(text_area_pressure)
    
    display.show(splash)
    # neopix[0] = (0, 255, 0)
    if temperature > Max:
        neopix[0] = (255, 0, 0)
    elif temperature < Min:
        neopix[0] = (0, 0, 255)    
    else:
        neopix[0] = (138, 43, 226)
    



import board
import adafruit_fxos8700
# import adafruit_fxas21002c
# import adafruit_bus_device
import time
import neopixel
# from rainbowio import colorwheel
print("Setup complete!")
x = 0.0
y = 0.0
x_min = 0.0
x_max = 0.0
y_min = 0.0
y_max = 0.0


def get_magneto_val(fxos):
    ''' Function updates global x and y values with values from magnetometer '''
    try:
        global x, y
        magneto = fxos.magnetometer
        x = -magneto[1]
        y = -magneto[2]
        print("x: " + str(x) + " y: " + str(y))
        return
    except AttributeError:
        return

# get_magneto_val needs exception handling to get rid of attribute error, needs global variables for that reason

def calc_maxmin(val):
    ''' Function creates new max and min values adds +- 10 to a given value '''
    max_val = val + 10
    min_val = val - 10
    return min_val, max_val

def set_maxmin(fxos):
    global x_min, y_min, x_max, y_max
    get_magneto_val(fxos)
    x_min, x_max = calc_maxmin(x)
    y_min, y_max = calc_maxmin(y)

# calc_maxmin is needed because of the inaccuracy of the magnetometer the values it returns vary wildly just sitting still on a level surface
def falls_which_way(x, y):
    if x > x_max:# and y < y_min:
        return "forward"
    if x < x_min:
        return "backward"
    return "N/A"




def main():
    global x
    global y
    i2c = board.I2C()
    fxos = adafruit_fxos8700.FXOS8700(i2c)
    # get_magneto_val(fxos)
    set_maxmin(fxos)
    neopix = neopixel.NeoPixel(board.NEOPIXEL, 1)
    neopix.brightness = 1
    isLevel = True
    print("Program running!")
    while True:
        time.sleep(1)
        get_magneto_val(fxos)
        if not (x_min <= x <= x_max):
            isLevel = False
            if x_min > x:
                print(str(x_min) + " " + str(x))
                print("Hitting x_min")
            elif x > x_max:
                print(str(y_min) + " " + str(y))
                print("Hitting x_max")
        elif not (y_min <= y <= y_max):
            isLevel = False
            if y_min > y:
                print(str(y_min) + " " + str(y))
                print("Hitting y_min")
            elif y > y_max:
                print(str(y_min) + " " + str(y))
                print("Hitting y_max")
        else:
            isLevel = True
        if not isLevel:             # if the robot is not level then diode is red
            neopix[0] = (255, 0, 0)
            print(falls_which_way(x, y))
        else:                       # else if robot is level the diode is blue
            neopix[0] = (0, 0, 255)


if __name__ == "__main__":
    main()
