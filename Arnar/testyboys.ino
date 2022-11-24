#include <util/atomic.h> // For the ATOMIC_BLOCK macro
#include <Wire.h>

#define ENCA 2 // YELLOW
#define ENCB 4 // WHITE
#define IN1 5
#define IN2 3
#define END_top 8
#define END_bot 9

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
int Flag = 0;
float kp = 1;
float kd = 0;
float ki = 0;
int distravel = 0;
float distance = 0;
int top = 0;
int bot = 0;

void setup() {
  Serial.begin(115200);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);
  pinMode(END_top,INPUT_PULLUP);
  pinMode(END_bot,INPUT_PULLUP);
  
  //pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  
  Serial.println("target pos");
  calibrate(dir, pwr, IN1, IN2);
}
  
void loop() {
 
  //Les serial
  while (Serial.available()) 
  {
    char c = Serial.read(); //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2); //slow looping to allow buffer to fill with next character
  }
  int end = readString.length();

  if (readString.length() > 0) 
  {
    //Skoða Hvort að það á að breyta p,i eða d
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

    //annars setja nýtt setpoint
    else{
      target = readString.toInt(); //convert readString into a number
      target = target * ratio;
    }
    readString = "";
  }
  

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
 
 
  if(e >= -15 && e <= 15)
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
  //limitSwitches();
  //calibrate(dir,pwr,PWM,IN1,IN2);

  setMotor(dir,pwr,IN1,IN2);

  // store previous error
  eprev = e;

  //Serial.print(target);
  //Serial.print(" ");
  //Serial.print(pos);
  //Serial.println();
}

void setMotor(int dir, int pwmVal,int in1, int in2){
  
  if(dir == 1 && Flag != 1){
    analogWrite(in1,pwmVal);
    digitalWrite(in2,HIGH);
    top =digitalRead(END_top);
    if (top == HIGH){
      digitalWrite(in1,HIGH);
      digitalWrite(in2,HIGH);
      Flag = 1;
    }
    
  }
  else if(dir == -1 && Flag != 2){
    digitalWrite(in1,HIGH);
    analogWrite(in2,pwmVal);
    bot = digitalRead(END_bot);
    if (bot == HIGH){
      digitalWrite(in1,HIGH);
      digitalWrite(in2,HIGH);
      Flag = 2;
    }
    
  }
  else{
    digitalWrite(in1,HIGH);
    digitalWrite(in2,HIGH);
    Flag = 0;
    
  
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


 
void calibrate(int dir, int pwmVal, int in1, int in2){
    delay(3000);
    bot =digitalRead(END_bot);
    while (bot == LOW){
    top =digitalRead(END_top);
    
    if (END_top != HIGH) {
        digitalWrite(in1,HIGH);
        digitalWrite(in2,LOW);
        Serial.println("Ekki a toppnum");
        bot =digitalRead(END_bot);
        while (END_bot == HIGH) {
        delay(0.01);
    }
        posi = 0;
       
    }
    else { 
        posi = 0;
        Serial.println("Toppi nad");
        
    }
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
    posi = 0;
 
    delay(500);
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
    top =digitalRead(END_top);
    bot =digitalRead(END_bot);
    while (END_bot == HIGH){
        delay(0.01);
    }
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
    delay(1000);
    distravel = abs(posi);
    posi = 0;
   
    distance  = distravel/775;}
}