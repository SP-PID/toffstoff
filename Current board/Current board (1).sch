EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCU_Module2:Metro_M4_Airlift A1
U 1 1 63077A48
P 5250 3900
F 0 "A1" V 5250 3900 50  0000 C CNN
F 1 "Metro_M4_Airlift" V 5100 3900 50  0000 C CNN
F 2 "Module:Arduino_UNO_R3" H 5250 3900 50  0001 C CIN
F 3 "https://www.arduino.cc/en/Main/arduinoBoardUno" H 5250 3900 50  0001 C CNN
	1    5250 3900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 6307B262
P 5250 5200
F 0 "#PWR?" H 5250 4950 50  0001 C CNN
F 1 "GND" H 5255 5027 50  0000 C CNN
F 2 "" H 5250 5200 50  0001 C CNN
F 3 "" H 5250 5200 50  0001 C CNN
	1    5250 5200
	1    0    0    -1  
$EndComp
Wire Wire Line
	5250 5200 5250 5100
Wire Wire Line
	5250 5100 5350 5100
Wire Wire Line
	5350 5100 5350 5000
Wire Wire Line
	5250 5000 5250 5100
Connection ~ 5250 5100
Wire Wire Line
	5150 5000 5150 5100
Wire Wire Line
	5150 5100 5250 5100
$Comp
L power:+3.3V #PWR?
U 1 1 6307C5E8
P 5350 2800
F 0 "#PWR?" H 5350 2650 50  0001 C CNN
F 1 "+3.3V" H 5365 2973 50  0000 C CNN
F 2 "" H 5350 2800 50  0001 C CNN
F 3 "" H 5350 2800 50  0001 C CNN
	1    5350 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 2900 5350 2800
$Comp
L Switch:SW_MEC_5G SW1
U 1 1 63081B58
P 4200 3500
F 0 "SW1" H 4200 3693 50  0000 C CNN
F 1 "SW_MEC_5G" H 4200 3694 50  0001 C CNN
F 2 "" H 4200 3700 50  0001 C CNN
F 3 "http://www.apem.com/int/index.php?controller=attachment&id_attachment=488" H 4200 3700 50  0001 C CNN
	1    4200 3500
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_MEC_5G SW2
U 1 1 63083049
P 4200 3900
F 0 "SW2" H 4200 4093 50  0000 C CNN
F 1 "SW_MEC_5G" H 4200 4094 50  0001 C CNN
F 2 "" H 4200 4100 50  0001 C CNN
F 3 "http://www.apem.com/int/index.php?controller=attachment&id_attachment=488" H 4200 4100 50  0001 C CNN
	1    4200 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 3500 4750 3500
Wire Wire Line
	4400 3900 4550 3900
Wire Wire Line
	4550 3900 4550 3600
Wire Wire Line
	4550 3600 4750 3600
$Comp
L power:GND #PWR?
U 1 1 630842D8
P 3850 4050
F 0 "#PWR?" H 3850 3800 50  0001 C CNN
F 1 "GND" H 3855 3877 50  0000 C CNN
F 2 "" H 3850 4050 50  0001 C CNN
F 3 "" H 3850 4050 50  0001 C CNN
	1    3850 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 4050 3850 3900
Wire Wire Line
	3850 3900 4000 3900
Wire Wire Line
	3850 3900 3850 3500
Wire Wire Line
	3850 3500 4000 3500
Connection ~ 3850 3900
Wire Notes Line
	4000 4000 4400 4000
Wire Notes Line
	4400 4000 4400 3250
Wire Notes Line
	4400 3250 4000 3250
Wire Notes Line
	4000 3250 4000 4000
Text Notes 3000 3150 0    50   ~ 0
Pull Up resistor internally on microcontroller
$Comp
L Sensor_Pressure2:MPL3115A2_modoule U1
U 1 1 63089222
P 7050 3200
F 0 "U1" H 7428 3051 50  0000 L CNN
F 1 "MPL3115A2_modoule" H 7428 2960 50  0000 L CNN
F 2 "" H 7150 3500 50  0001 C CNN
F 3 "" H 7150 3500 50  0001 C CNN
	1    7050 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 3600 6150 3600
Wire Wire Line
	6150 3600 6150 4250
Wire Wire Line
	6150 4700 5750 4700
$Comp
L power:+3.3V #PWR?
U 1 1 6308B5C2
P 6850 3050
F 0 "#PWR?" H 6850 2900 50  0001 C CNN
F 1 "+3.3V" H 6865 3223 50  0000 C CNN
F 2 "" H 6850 3050 50  0001 C CNN
F 3 "" H 6850 3050 50  0001 C CNN
	1    6850 3050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 6308C0A3
P 6750 3350
F 0 "#PWR?" H 6750 3100 50  0001 C CNN
F 1 "GND" H 6755 3177 50  0000 C CNN
F 2 "" H 6750 3350 50  0001 C CNN
F 3 "" H 6750 3350 50  0001 C CNN
	1    6750 3350
	1    0    0    -1  
$EndComp
Wire Wire Line
	6750 3200 6900 3200
Wire Wire Line
	6750 3200 6750 3350
Wire Wire Line
	6900 3100 6850 3100
Wire Wire Line
	6850 3100 6850 3050
$Comp
L Sensor_Pressure2:SSD1306_Display U2
U 1 1 6308E1FE
P 7000 3850
F 0 "U2" H 7928 3546 50  0000 L CNN
F 1 "SSD1306_Display" H 7928 3455 50  0000 L CNN
F 2 "" H 7500 3500 50  0001 C CNN
F 3 "" H 7500 3500 50  0001 C CNN
	1    7000 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 3700 6250 3700
Wire Wire Line
	6250 3700 6250 4350
Wire Wire Line
	6250 4600 5750 4600
Wire Wire Line
	6900 4250 6150 4250
Connection ~ 6150 4250
Wire Wire Line
	6150 4250 6150 4700
Wire Wire Line
	6900 4350 6250 4350
Connection ~ 6250 4350
Wire Wire Line
	6250 4350 6250 4600
$Comp
L power:+3.3V #PWR?
U 1 1 63092C40
P 6750 3950
F 0 "#PWR?" H 6750 3800 50  0001 C CNN
F 1 "+3.3V" H 6765 4123 50  0000 C CNN
F 2 "" H 6750 3950 50  0001 C CNN
F 3 "" H 6750 3950 50  0001 C CNN
	1    6750 3950
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR?
U 1 1 6309379C
P 6700 4150
F 0 "#PWR?" H 6700 3900 50  0001 C CNN
F 1 "GND" H 6705 3977 50  0000 C CNN
F 2 "" H 6700 4150 50  0001 C CNN
F 3 "" H 6700 4150 50  0001 C CNN
	1    6700 4150
	0    1    1    0   
$EndComp
Wire Wire Line
	6700 4150 6900 4150
Wire Wire Line
	6750 3950 6850 3950
Wire Wire Line
	6850 3950 6850 4050
Wire Wire Line
	6850 4050 6900 4050
$Comp
L Sensor_Pressure2:TCS34725_RGBsensor U3
U 1 1 6309E298
P 7000 4500
F 0 "U3" H 7578 4051 50  0000 L CNN
F 1 "TCS34725_RGBsensor" H 7578 3960 50  0000 L CNN
F 2 "" H 7300 4050 50  0001 C CNN
F 3 "" H 7300 4050 50  0001 C CNN
	1    7000 4500
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 630A02D1
P 6750 4600
F 0 "#PWR?" H 6750 4450 50  0001 C CNN
F 1 "+3.3V" H 6765 4773 50  0000 C CNN
F 2 "" H 6750 4600 50  0001 C CNN
F 3 "" H 6750 4600 50  0001 C CNN
	1    6750 4600
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR?
U 1 1 630A02D7
P 6700 4800
F 0 "#PWR?" H 6700 4550 50  0001 C CNN
F 1 "GND" H 6705 4627 50  0000 C CNN
F 2 "" H 6700 4800 50  0001 C CNN
F 3 "" H 6700 4800 50  0001 C CNN
	1    6700 4800
	0    1    1    0   
$EndComp
Wire Wire Line
	6700 4800 6900 4800
Wire Wire Line
	6750 4600 6850 4600
Wire Wire Line
	6850 4600 6850 4700
Wire Wire Line
	6850 4700 6900 4700
Wire Wire Line
	6900 5000 6150 5000
Wire Wire Line
	6150 5000 6150 4700
Connection ~ 6150 4700
Wire Wire Line
	6900 5100 6250 5100
Wire Wire Line
	6250 5100 6250 4600
Connection ~ 6250 4600
$Comp
L Sensor_Pressure2:2Y0A02_F22 U4
U 1 1 630A2C78
P 7000 2250
F 0 "U4" H 7678 2001 50  0000 L CNN
F 1 "2Y0A02_F22-IR distance_sensor" H 6900 2200 50  0000 L CNN
F 2 "" H 7400 1950 50  0001 C CNN
F 3 "" H 7400 1950 50  0001 C CNN
	1    7000 2250
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 630A4E45
P 6750 2350
F 0 "#PWR?" H 6750 2200 50  0001 C CNN
F 1 "+3.3V" H 6765 2523 50  0000 C CNN
F 2 "" H 6750 2350 50  0001 C CNN
F 3 "" H 6750 2350 50  0001 C CNN
	1    6750 2350
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR?
U 1 1 630A4E4B
P 6700 2550
F 0 "#PWR?" H 6700 2300 50  0001 C CNN
F 1 "GND" H 6705 2377 50  0000 C CNN
F 2 "" H 6700 2550 50  0001 C CNN
F 3 "" H 6700 2550 50  0001 C CNN
	1    6700 2550
	0    1    1    0   
$EndComp
Wire Wire Line
	6700 2550 6900 2550
Wire Wire Line
	6750 2350 6850 2350
Wire Wire Line
	6850 2350 6850 2450
Wire Wire Line
	6850 2450 6900 2450
Wire Wire Line
	6900 2650 6050 2650
Wire Wire Line
	6050 2650 6050 4100
Wire Wire Line
	6050 4100 5750 4100
$EndSCHEMATC
