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
int current_position = 500;
int direction = 0;
int microstepping = 2;
const int max_steps = 2657; 
//int STEPS = 0;
int requested_position = 1000;
int multiplier = 2;
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
int STEPS = abs((current_position - requested_position)); // Number of steps to move
Serial.println(STEPS);
if (STEPS == 0){    
// if the number of steps to go is zero then do nothing
  return 0;
}
if (requested_position > max_steps) {
// if requested position is beyond the actuators top end then go to top
  requested_position = max_steps;
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
}





void loop() {
digitalWrite(ms1,HIGH);
digitalWrite(ms2,LOW);  
int multiplier = update_microstepping(microstepping); 
Serial.println(requested_position);
go_to_position(500);
Serial.println(500);
delay(1000);
go_to_position(1500);
Serial.println(1500);
delay(1000);
go_to_position(3500);
Serial.println(3500);
delay(1000);
go_to_position(0);
Serial.println(0);
delay(1000);

}








