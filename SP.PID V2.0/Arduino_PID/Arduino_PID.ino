#include <util/atomic.h> // For the ATOMIC_BLOCK macro
#include <Wire.h>


#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define OLED_DC     8
#define OLED_CS     10
#define OLED_RESET  9



#define ENCA 2 // YELLOW
#define ENCB 4 // WHITE
#define PWM 5
#define IN2 5
#define IN1 3

volatile int posi = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
long prevT = 0;
float eprev = 0;
float eintegral = 0;
int target;
String readString = "";
float pwr;
int dir;
long time = micros();
int set = 1;
float ratio = 1440 / 360 ;

float kp = 1;
float kd = 0;
float ki = 0;

void setup() {
  Serial.begin(115200);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);

  
  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  
  Serial.println("target pos");}

void loop() {
  

  // set target position
  //int target = 1200;
  while (Serial.available()) 
  {
    char c = Serial.read(); //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2); //slow looping to allow buffer to fill with next character
  }
  int end = readString.length();

  if (readString.length() >0) 
  {
    //Serial.println(readString); //so you can see the captured String
    

    if (readString.substring(0,1) == "p")
    {
      kp = readString.substring(1,end).toFloat();
    }

    else if (readString.substring(0,1) == "i")
    {
      ki = readString.substring(1,end).toFloat();
    }

    else if (readString.substring(0,1) == "d")
    {
      kd = readString.substring(1,end).toFloat();
    }

    else{
      target = readString.toInt(); //convert readString into a number
      target = target * ratio;
    }
    readString = "";
  }

  // // PID constants
  
  // if (set == 1 && micros() - time > 3000000)
  // {
  //   Serial.println("up");
  //   target = 1440;
  //   set = 0;
  //   time = micros();
  // }

  // if (set == 0 && micros() - time > 3000000)
  // {
  //   Serial.println("Down");
  //   target = 0;
  //   set = 1;
  //   time = micros();
  // }
  

  // time difference
  long currT = micros();
  float deltaT = ((float) (currT - prevT))/( 1.0e6 );
  prevT = currT;

  // Read the position in an atomic block to avoid a potential
  // misread if the interrupt coincides with this code running
  // see: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
  int pos = 0; 
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    pos = posi;
  }
  
  // error
  int e = pos - target;

  // derivative
  float dedt = (e-eprev)/(deltaT);

  // integral
  eintegral = eintegral + e*deltaT;

  // control signal
  float u = kp*e + kd*dedt + ki*eintegral;

  // motor power
  
  if(e >= -1 && e <= 1)
  {
    pwr = 0;
    dir = 0;
  }
  else{
    
    float pwr = fabs(u);
    if( pwr > 255 ){
        pwr = 255;
        }
    
    
    if(u<0){
    dir = -1;
    }
    else{dir = 1;}
  }

  // signal the motor
//  setMotor(dir,pwr,PWM,IN1,IN2);


  // store previous error
  eprev = e;

  Serial.print(target);
  Serial.print(" ");
  Serial.print(pos);
  Serial.println();
  delay(1);
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2){
  analogWrite(pwm,pwmVal);
  if(dir == 1){
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
  }
  else if(dir == -1){
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
  }
  else{
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
  }  
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
