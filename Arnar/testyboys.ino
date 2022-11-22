#include <util/atomic.h> // For the ATOMIC_BLOCK macro
#include <Wire.h>

#define ENCA 2 // YELLOW
#define ENCB 4 // WHITE
#define PWM 5
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

void setup() {
  Serial.begin(115200);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);
  pinMode(END_top,INPUT);
  pinMode(END_bot,INPUT);
  
  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  
  Serial.println("target pos");
  
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
  limitSwitches();
  calibrate(dir,pwr,PWM,IN1,IN2);

  setMotor(dir,pwr,PWM,IN1,IN2);


  // store previous error
  eprev = e;

  //Serial.print(target);
  //Serial.print(" ");
  //Serial.print(pos);
  //Serial.println();
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2){
  analogWrite(pwm,pwmVal);
  if(dir == 1 && Flag != 1){
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
    Serial.print("1");
    Serial.println();
    Serial.print(Flag);
  }
  else if(dir == -1 && Flag != 2){
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
    Serial.print("2");
    Serial.println();
    Serial.print(Flag);
  }
  else{
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
    Serial.print("3");
    Serial.println();
    Serial.print(Flag);
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
void limitSwitches(){
  if (END_top == LOW){
    Flag = 1;
    } 
  else if (END_bot == LOW){
    Flag = 2;
    }
  else{
    Flag = 0;
    } 
    
  }
  void calibrate(int dir, int pwmVal, int pwm, int in1, int in2){
    delay(3000);
    if (END_top != LOW) {
        digitalWrite(in1,HIGH);
        digitalWrite(in2,LOW);
        while (END_bot == LOW) {
        delay(0.01);
    }
        posi = 0;
       
    }
    else { 
        posi = 0;
        
    }
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
    posi = 0;
 
    delay(500);
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
    while (END_bot == LOW){
        delay(0.01);
    }
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
    delay(1000);
    distravel = abs(posi);
    posi = 0;
   
    distance  = distravel/775;
    

    

  }