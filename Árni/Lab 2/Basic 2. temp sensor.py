import board
import digitalio #Not used in code
import analogio #Not used in code
import simpleio #Not used in code
import time
import neopixel
from rainbowio import colorwheel    #Not used in code
import adafruit_mpl3115a2

i2c = board.I2C()   #Definest the I2C bus pins

Min_temp = 20    #Defines the Min value for temperature
Max_temp = 25    #Defines the Max value for temperature

#Defines the sensor
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)  

#Defines the NeoPixel
rgbled = neopixel.NeoPixel(board.NEOPIXEL, 1)   
rgbled.brightness = 0.1 #Sets NeoPixel brightness

#Loop that runs indefinitly
while True:
    temp = sensor.temperature   #Read the temperature from the sensor

    print((temp,))  #Print the temperature to serial to plot

    #Check if measured temperature is les than Min_temp
    if temp < Min_temp: 
        rgbled[0] = (0,0,255)   #Set NeoPixel to show blue light

    #Check if measured temperature is higher than Max_temp
    elif temp > Max_temp:   
        rgbled[0] = (255,0,0)   #Set neopixel to show red light

    else:   # if nither previus statment applies
        rgbled[0] = (255,0,255) #Sets NeoPixel to purple

    #Wait for one second before running the loop again.
    time.sleep(1)   

