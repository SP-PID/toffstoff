// Define Constants

// Connections to A4988
const int dirPin = 2; // Direction
const int stepPin = 3; // Step
const int ms1 = 6;
const int ms2 = 7;

void setup() {
Serial.begin(9600);
pinMode(stepPin,OUTPUT);
pinMode(dirPin,OUTPUT);
pinMode(ms1,OUTPUT);
pinMode(ms2,OUTPUT);
}

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


int current_position = 500;
int direction = 0;
int microstepping = 2;
const int max_steps = 2657; 
int STEPS = 0;
int requested_position = 1000;
int multiplier = 2;


void loop() {
digitalWrite(ms1,HIGH);
digitalWrite(ms2,LOW);  
//int multiplier = update_microstepping(microstepping);  
//current_position = update_position(current_position,direction);
// If the current position is below the requested position
//Serial.println(current_position);
Serial.println(requested_position);
//if (current_position != requested_position){
STEPS = abs((current_position - requested_position));
Serial.println(STEPS);
if (STEPS == 0){
  return 0;
}

if (current_position > requested_position){
digitalWrite(dirPin,LOW);  // Direction pin low is down
direction = 1;
// set direction of travel to down
}
if (current_position < requested_position){
digitalWrite(dirPin,HIGH);  
direction = 0;
// set direction of travel to down
}
for(int x = 0; x < (STEPS); x++) {
current_position = update_position(current_position,direction);  
for(int y = 0; y < multiplier; y++) {
// one step
  step();
}
// update the current position, should be one step closer to requested

}
//}
//else{
//  return 0;
//  }


Serial.println(current_position);
delay(1000);
}







