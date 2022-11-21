import board
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_airlift.esp32 import ESP32
# Takes input from a smartphone app, using bluetooth ESP32 module. translates to commands in code
esp32 = ESP32() # DEFAULT
adapter = esp32.start_bluetooth()
ble = BLERadio(adapter)
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    print("waiting to connect")
    while not ble.connected:
        pass
    print("connected: trying to read input")
    while ble.connected:
        # Returns b'' if nothing was read.
        one_byte = uart.read()
        if one_byte:
            # Selects the correct string to show what button was pressed
            if one_byte == b'!B516!B507':
                print("UP")
            if one_byte == b'!B615!B606':
                print("DOWN")                
            if one_byte == b'!B813!B804':
                print("RIGHT")
            if one_byte == b'!B714!B705':
                print("LEFT")
            if one_byte == b'!B11:!B10;':
                print("1")
            if one_byte == b'!B219!B20:':
                print("2")
            if one_byte == b'!B318!B309':
                print("3")
            if one_byte == b'!B417!B408':
                print("4")