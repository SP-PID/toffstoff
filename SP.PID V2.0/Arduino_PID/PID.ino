#include <util/atomic.h> // For the ATOMIC_BLOCK macro
#include <Wire.h>

#define ENCA 3 // YELLOW
#define ENCB 2 // WHITE
#define IN1 5
#define IN2 6
#define END_top 9
#define END_bot 8
#define Estop 12

volatile int posi = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
long prevT = 0;
float eprev = 0;
float eintegral = 0;
int target = 0;
String readString = "";
float pwr;
int dir;
long time = micros();
int set = 1;
int Flag = 0;
float kp = 1;
float kd = 0;
float ki = 0;
int distravel = 0;
float steps = 0;
int top = 0;
int bot = 0;
int pos_old = 0;
int end = 0;
int max_pwr = 255;
float dedt = 0;



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

  while (true)
  {
    while (Serial.available()) 
    {
        char c = Serial.read(); //gets one byte from serial buffer
        readString += c; //makes the String readString
        delay(2); //slow looping to allow buffer to fill with next character
    }

    end = readString.length();
    if (readString.length() > 0) 
    {
        if (readString == "identify")
        {
            Serial.println("DC");
            readString = "";
            break;
        }
    }
  
  }
  Serial.println("Ready!");
}

void loop() {
 while (Serial.available()) 
  {
    char c = Serial.read(); //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2); //slow looping to allow buffer to fill with next character
  }
  end = readString.length();
  if (readString.length() > 0) 
  {
    Serial.println(readString);
    if (readString == "calibrate")
    {
      Serial.println("Calibrating");
      calibrate(IN1, IN2);
      Serial.println("Calibration done!"); 
    } 
    
    if (readString == "run")
    {
      readString = "";
      run();
    }
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

    else if (readString.substring(0,1) == "m")
    {
      int temp = readString.substring(1,end).toInt();
      if (temp < 255)
      {
        max_pwr = temp;
      }

      else
      {
        max_pwr = 255;
      }
    }
    //annars setja nýtt setpoint
    else{
      target = readString.toInt(); //convert readString into a number
    }
    readString = "";
  }

}

void run(){

  long currT = micros();
  float deltaT = ((float) (currT - prevT))/( 1.0e6 );
  prevT = currT;

  while (true) 
  {
  while (Serial.available()) 
  {
    char c = Serial.read(); //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2); //slow looping to allow buffer to fill with next character
    //Serial.println("Núna hér");
  }

  if (readString == "Estop" || digitalRead(Estop) == HIGH)
  {
    digitalWrite(IN1,HIGH);
    digitalWrite(IN2,HIGH);
    target = 0;
    Serial.println("Estop activated");
    break;
  }
  end = readString.length();
  if (readString.length() > 0) 
  {
    if (readString == "stop"){
      digitalWrite(IN1,HIGH);
      digitalWrite(IN2,HIGH);
      break;
    }
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
  if (kd != 0)
  {
    dedt = (e - eprev) / (deltaT);
  }

  else
  {
    dedt = 0;
  }

  // integral
  if (ki != 0)
  {
    eintegral = eintegral + (e * deltaT);
  }

  else
  {
    eintegral = 0;
  }

  // control signal
  float u = (kp*e) + (kd*dedt) + (ki*eintegral);
  // motor power
  
 
  //if(e >= -2 && e <= 2)
  //{
  //  pwr = 0;
  //  dir = 0;
  //}
  //else{
   float pwr = fabs(u);
   
    if( pwr > 255 )
    {
        pwr = 255;
    }
    
    pwr = 255 - pwr;
  
    
    //Serial.println(pwr);

    if(u < 0)
    {
      dir = -1;
    }
    
    else
    {
      dir = 1;
    }
  //}

   if (pos_old != pos){
    Serial.print(millis());
    Serial.print(',');
    Serial.println(pos);
    //Serial.print(u);
    //Serial.print(',');
    //Serial.println(pwr);
    pos_old = pos;
  }

  // signal the motor
  setMotor(dir,pwr,IN1,IN2);

  // store previous error
  eprev = e;
  
 
  //Serial.print(target);
  //Serial.print(" ");
  //Serial.println(pos);
  //Serial.println();
}}

void setMotor(int dir, int pwmVal, int in1, int in2){
  
  // Drive down
  if(dir == 1 && Flag != 2)
  {
    Flag = 0;
    analogWrite(in1, pwmVal);
    digitalWrite(in2, HIGH);
  
    if (digitalRead(END_bot) == HIGH)
    {
      digitalWrite(in1,HIGH);
      digitalWrite(in2,HIGH);
      Flag = 2;
    }
  }

  // Drive up
  else if(dir == -1 && Flag != 1)
  {
    Flag = 0;
    digitalWrite(in1, HIGH);
    analogWrite(in2, pwmVal);
    
    if (digitalRead(END_top) == HIGH)
    {
      digitalWrite(in1,HIGH);
      digitalWrite(in2,HIGH);
      
      Flag = 1;
    }
  }
  
  else
  {
    
    digitalWrite(in1,HIGH);
    digitalWrite(in2,HIGH);
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


 
void calibrate(int in1, int in2){
    delay(1000);
    Serial.println("Driving up");
    while (digitalRead(END_top) != HIGH) 
    {
        digitalWrite(in1,HIGH);
        analogWrite(in2,170);
        bot = digitalRead(END_bot);
    }
    
    digitalWrite(in1,HIGH);
    digitalWrite(in2,HIGH);
    posi = 0;
    
    Serial.println("Top reached");
    delay(1000);
    
    Serial.println("Driving down");
    while (digitalRead(END_bot) != HIGH)
    {
    analogWrite(in1,170);
    digitalWrite(in2,HIGH);
    }
    
    digitalWrite(in1,HIGH);
    digitalWrite(in2,HIGH);
    
    distravel = abs(posi);
    posi = 0;
    
    delay(1000);
   
    steps = 775/distravel;
    Serial.println(distravel);
    //Serial.println(steps);
    }