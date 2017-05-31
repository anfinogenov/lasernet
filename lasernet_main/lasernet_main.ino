const int DETECTOR = 0;
const int LASER = 13;
const int GREEN = 11;
const int RED = 9;
const int latency = 20;
const int laser_on = 1000;
const bool RECEIVER = true;

void enable_pin (int pin) {
  digitalWrite(pin, HIGH);
}

void disable_pin (int pin) {
  digitalWrite(pin, LOW);
}

int update_status (int reading) {
  if (reading > laser_on) {
    enable_pin(GREEN);
    disable_pin(RED);
  }
  else {
    enable_pin(RED);
    disable_pin(GREEN);
  }
  return reading;
}

void send_byte (char symbol) {
  digitalWrite(LASER, HIGH);
  delay(latency);
  for (int i = 128; i >= 1; i/= 2) {
    if (symbol & i) digitalWrite(LASER, HIGH);
    else digitalWrite(LASER, LOW);
    delay(latency);
  }
  digitalWrite(LASER, LOW);
  delay(latency);
}

char receive_byte (void) {
  unsigned char byte_read = 0;
  delay(3*latency/2);
  for (int i = 128; i >= 1; i /= 2) {  
    if (update_status(analogRead(DETECTOR)) > laser_on)
      byte_read |= i;
    if (i >= 1) delay(latency);
    else delay(latency/2);
  }
  return byte_read;
}

void setup() {
  pinMode(LASER, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(RED, OUTPUT);
  Serial.begin(115200);
  digitalWrite(LASER, HIGH);
  update_status(analogRead(DETECTOR));
}
 
void loop() {
  if (RECEIVER) {
    if (analogRead(DETECTOR) > laser_on)
      Serial.write(receive_byte());
    else return; 
  } else {
    char value = 0;
    if (Serial.available() > 0) {
      value = Serial.read();
      send_byte(value);
    } 
  }
}
  
