import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from adafruit_motor import servo
import neopixel
import busio
import audioio
import pulseio
import simpleio
from adafruit_esp32spi import adafruit_esp32spi
import digitalio
from adafruit_debouncer import Debouncer
import random

# keyboard support
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# One pixel connected internally!
dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Initialize WiFi Module
if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])


# MAIN LOOP
# Debounce test



pinup = digitalio.DigitalInOut(board.D1)

pindwn = digitalio.DigitalInOut(board.D5)

pindwn.direction = digitalio.Direction.INPUT

pindwn.pull = digitalio.Pull.UP

switch_dwn = Debouncer(pindwn,interval=0.1)

pinup.direction = digitalio.Direction.INPUT

pinup.pull = digitalio.Pull.UP

switch_up = Debouncer(pinup,interval=0.1)
r= random.randint(0,255)
g = random.randint(0,255)
b = random.randint(0,255)
color = [r,g,b]
ran_rand = random.randint(0,5000)
p=0
ran = 0
while True:

    if ran_rand < 100 and ran_rand > 0:
        ran = random.randint(0,2)
    switch_dwn.update()
    switch_up.update()

    #if switch_dwn.value == False and switch_up.value == False:
    #    if ran < 2:
    #        ran = ran +1
    #    else:
    #        ran = 0


    if switch_dwn.value == False:

        if color[ran] != 0:
            color[ran] = color[ran] -1
        print('down pressed')
        print(color)
        ran_rand = random.randint(0,5000)



    if switch_up.value == False:
        if color[ran] != 255:
            color[ran] = color[ran]+1
        ran_rand = random.randint(0,5000)
        print('up pressed')
        print(color)


    #dot[0] = color

    #dot.show()
    dot[0] = wheel(i & 255)
    for p in range(NUMPIXELS):
        idx = int((p * 256 / NUMPIXELS) + i)
        neopixels[p] = wheel(idx & 255)
    neopixels.show()

i = 0
z=0
while z< 10:
    if i == 0:
        # Lets to a WiFi SSID scan
        for ap in esp.scan_networks():
            print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))
    # spin internal LED around! autoshow is on
    dot[0] = wheel(i & 255)

    # also make the neopixels swirl around
    for p in range(NUMPIXELS):
        idx = int((p * 256 / NUMPIXELS) + i)
        neopixels[p] = wheel(idx & 255)
    neopixels.show()

    # Read analog voltage on A1
    #print("A1: %0.2f" % getVoltage(analog1in), end="\t")

    if not buttons[0].value:
        print("Button D2 pressed!", end="\t")
        # optional! uncomment below & save to have it sent a keypress
        # kbd.press(Keycode.A)
        # kbd.release_all()
    if not buttons[1].value:
        print("Button D3 pressed!", end="\t")
        play_file(audiofiles[0])
    if not buttons[2].value:
        print("Button D4 pressed!", end="\t")
        play_file(audiofiles[1])
    # sweep a servo from 0-180 degrees (map from 0-255)
    servo.angle = simpleio.map_range(i, 0, 255, 0, 180)

    i = (i + 1) % 256  # run from 0 to 255
    time.sleep(0.01) # make bigger to slow down
    z= z +1
    #print("")
