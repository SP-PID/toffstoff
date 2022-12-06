#include <util/atomic.h> // For the ATOMIC_BLOCK macro
#include <SPI.h>
#include <Wire.h>
//#include <Adafruit_GFX.h>
//#include <Adafruit_SSD1306.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;

//#define SCREEN_WIDTH 128 // OLED display width, in pixels
//#define SCREEN_HEIGHT 64 // OLED display height, in pixels

//#define OLED_DC     8
//#define OLED_CS     10
//#define OLED_RESET  9
//Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT,
//  &SPI, OLED_DC, OLED_RESET, OLED_CS);
float voltage;
float current;
float power;



void setup() {
  Serial.begin(115200);

  //if(!display.begin(SSD1306_SWITCHCAPVCC)) {
  //  Serial.println(F("SSD1306 allocation failed"));
  //  for(;;); // Don't proceed, loop forever
  //}

  if (! ina219.begin()) {
    Serial.println("Failed to find INA219 chip");
    while (1) { delay(10); }
  }

  Serial.println("Measuring voltage and current with INA219 ...");

//display.display();
//  delay(500);

//display.clearDisplay();

//display.setTextColor(SSD1306_WHITE);
//printdisplay();
}

void loop() {
  voltage = ina219.getBusVoltage_V();
  current = ina219.getCurrent_mA();
  power = ina219.getPower_mW();
  Serial.print(voltage);
  Serial.print(" ");
  Serial.print(current/1000);
  //Serial.print(" ");
  //Serial.print(power/1000);
  Serial.println();
  //printdisplay();
  delay(5);
}



//void printdisplay()
//{
//  display.setTextSize(1);      
//  display.clearDisplay();
  
//  display.setCursor(0,0);
//  String p = "Voltage: ";
//  display.print(p + voltage);
  
//  display.setCursor(0,10);
//  String i = "Curretnt: ";
//  display.print(i + current / 1000);
//  display.display();
//}
