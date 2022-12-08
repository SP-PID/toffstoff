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
boolean running = false;
int end = 0;

void setup() {
Serial.begin(115200);
pinMode(stepPin,OUTPUT);
pinMode(dirPin,OUTPUT);
pinMode(ms1,OUTPUT);
pinMode(ms2,OUTPUT);
pinMode(endPin,INPUT_PULLUP);

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
            Serial.println("Stepper");
            readString = "";
            break;
        }
    }
  
  }

reset_actuator();
//Serial.println("Setup complete!");
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
if (requested_position < 0){
  return 0;
}
if (requested_position > max_steps) { // if requested position is beyond the actuators top end then go to top   
requested_position = max_steps;
  }
int STEPS = abs((current_position - requested_position)); // Number of steps to move
if (STEPS == 0){ // if the number of steps to go is zero then do nothing   
  return 0;
  }
if (current_position > requested_position){ // set direction of travel to down 
digitalWrite(dirPin,LOW);  
direction = 1;
  }
if (current_position < requested_position){ // set direction of travel to up
digitalWrite(dirPin,HIGH);  
direction = 0;
  }
for(int x = 0; x < STEPS; x++) { // move to requested position
current_position = update_position(current_position,direction);  // update current position for each step
for(int y = 0; y < multiplier; y++) {
step(); // one step
    }
  }
Serial.println("SP");
}

// Reset the actuator before operations start
void reset_actuator() {
    digitalWrite(dirPin,LOW);  // set direction of travel to down
    direction = 1;  
    current_position = 0;
    buttonState = digitalRead(endPin); 
    while (!buttonState){
        buttonState = digitalRead(endPin); 
        step(); // one step per repetition of loop untill actuator is at zero
    }
    Serial.println("ZE");
}

void(* resetFunc) (void) = 0;//declare reset function at address 0

void loop() {
//Serial.println("Loop begins");
int multiplier = update_microstepping(microstepping); 
while (Serial.available()) 
  {
    char c = Serial.read(); //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2); //slow looping to allow buffer to fill with next character
  }
int end = readString.length();
if (end > 0) {
    if (readString == "run"){
        //Serial.println("Run command");
        running = true;
    }
    if (readString == "notrun"){
        //Serial.println("Stop running command");
        running = false;
    }
    if (readString == "cal"){
        //Serial.println("Resetting Setpoint actuator");
        reset_actuator();
    }
    if (readString == "rst"){
      //Serial.println("Reset command");
      delay(1000);
      resetFunc();
    }
if (running == true) {
  new_position = readString.toInt();
  Serial.println(new_position);
  if (new_position != current_position) {
      go_to_position(new_position);
      delay(1000);
    }
  Serial.println(current_position);
}
readString = "";
}
}

