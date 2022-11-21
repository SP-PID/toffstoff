#include <util/atomic.h> // For the ATOMIC_BLOCK macro
#include <Wire.h>


#define ENCA 2 // YELLOW
#define ENCB 4 // WHITE


volatile int posi = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/

int pos = 0;
int old_pos = 0;
String readString = "";

void setup() {
  Serial.begin(115200);
  pinMode(ENCA, INPUT);
  pinMode(ENCB, INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);
  Serial.println("target pos");
  delay(500);
}

void loop() {
  // Read the position in an atomic block to avoid a potential
  // misread if the interrupt coincides with this code running
  // see: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    pos = posi;
  }

  while (Serial.available()) 
  {
    char c = Serial.read(); //gets one byte from serial buffer
    readString += c; //makes the String readString
    //delay(1); //slow looping to allow buffer to fill with next character
  }
  if (readString == "0")
  {
    pos = 0;
    posi = 0;
  }

  readString = "";

  if (pos != old_pos)
  {
   Serial.println(pos);
   old_pos = pos; 
  }
  
  
  
  delay(1);
}


void readEncoder(){
  int b = digitalRead(ENCB);
  if(b > 0){
    posi++;
  }
  else{
    posi--;
  }
}
