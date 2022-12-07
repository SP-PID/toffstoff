// Define Constants

const int dirPin = 7; // Direction
const int stepPin = 6; // Step
const int ms1 = 3;
const int ms2 = 4;
const int endPin = 2;
char input;
int current_position = 0;
int direction = 0;
int microstepping = 2;
const int max_steps = 2657; 
int requested_position = 1000;
int multiplier = 2;
String readString = "";
int new_position;
boolean buttonState;


void setup() {
Serial.begin(9600);
pinMode(stepPin,OUTPUT);
pinMode(dirPin,OUTPUT);
pinMode(ms1,OUTPUT);
pinMode(ms2,OUTPUT);
pinMode(endPin,INPUT_PULLUP);
reset_actuator();
}


// controls the microstepping function of the TMC2208 driver
int update_microstepping(int microstepping) {
  if (microstepping == 2)
    {digitalWrite(ms1,HIGH);
    digitalWrite(ms2,LOW);
    return 2; }
  if (microstepping == 4)
    {digitalWrite(ms1,LOW);
    digitalWrite(ms2,HIGH);
    return 4;}
  if (microstepping == 8)
    {digitalWrite(ms1,LOW);
    digitalWrite(ms2,LOW);
    return 8;}
  if (microstepping == 16)
    {digitalWrite(ms1,HIGH);
    digitalWrite(ms2,HIGH);
    return 16;}
  }

// update position keeps track of current gantry position
int update_position(int current_position,char direction[]) {
  //Serial.println(current_position);
  if (direction == 1){
    return current_position - 1;
  }
  if (direction == 0){            // zero is up
    return current_position + 1;
  }
}

// step function moves the stepper one step in some direction
void step() {
  digitalWrite(stepPin,HIGH);
  delayMicroseconds(300);
  digitalWrite(stepPin,LOW);
  delayMicroseconds(300);
}

void go_to_position(int requested_position) {
// if requested position is beyond the actuators top end then go to top    
if (requested_position > max_steps) {
Serial.println("Top Reached");
requested_position = max_steps;
  }
int STEPS = abs((current_position - requested_position)); // Number of steps to move
Serial.println(STEPS);
if (STEPS == 0){    
// if the number of steps to go is zero then do nothing
  return 0;
  }
if (current_position > requested_position){
// set direction of travel to down   
digitalWrite(dirPin,LOW);  
direction = 1;
  }
if (current_position < requested_position){
// set direction of travel to up
digitalWrite(dirPin,HIGH);  
direction = 0;
  }
// move to requested position
for(int x = 0; x < STEPS; x++) {
// update current position for each step
current_position = update_position(current_position,direction);  
for(int y = 0; y < multiplier; y++) {
// one step
step();
    }
  }
  Serial.println(current_position);
}

void reset_actuator() {
    digitalWrite(dirPin,LOW);  
    direction = 1;  
    buttonState = digitalRead(endPin);
   // Serial.println(buttonState);    
    while (!buttonState){
        buttonState = digitalRead(endPin);
       // Serial.println(buttonState); 
        step();
    }
}




void loop() {

int multiplier = update_microstepping(microstepping); 
while (Serial.available()) 
  {
    char c = Serial.read(); //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2); //slow looping to allow buffer to fill with next character
  }
int end = readString.length();
if (end > 0) {
Serial.println(readString);
new_position = readString.toInt();
if (new_position != current_position) {
  go_to_position(new_position);
  delay(1000);
}
}
readString = "";
}





