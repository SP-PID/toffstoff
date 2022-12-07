#include <util/atomic.h> // For the ATOMIC_BLOCK macro
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>



#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define OLED_DC     8
#define OLED_CS     10
#define OLED_RESET  9
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT,
  &SPI, OLED_DC, OLED_RESET, OLED_CS);

float voltage;
float current;
float power;
String readString;
String oldstring;
int end;



void setup() {
  Serial.begin(115200);

  if(!display.begin(SSD1306_SWITCHCAPVCC)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

display.display();
delay(500);

display.clearDisplay();

display.setTextColor(SSD1306_WHITE);
printdisplay();
}

void loop() {
  while (Serial.available()) 
  {
    char c = Serial.read(); //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2); //slow looping to allow buffer to fill with next character
  }
  end = readString.length();
  
  if ( readString != oldstring && end > 0)
  {
  Serial.println(readString);
  printdisplay();
  }
  oldstring = readString;
  readString = "";
  delay(5);
}



void printdisplay()
{
  display.setTextSize(1);      
  display.clearDisplay();
  
  display.setCursor(0,0);
  String p = "Voltage: ";
  display.print(readString);
  display.display();
}
