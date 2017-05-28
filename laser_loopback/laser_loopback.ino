const int sleepmks = 250; //250 is ok
const int sleepms = 200;
const int laserPin = 13;
const int photoresistorPin = 0;
const int error = 5;
int laser_on = 1000;

void setup() {
  pinMode(laserPin, OUTPUT);
  digitalWrite(laserPin, HIGH);
  Serial.begin(115200);
  delay(100);
  laser_on = analogRead(photoresistorPin);
}

char send_receive_byte (char symbol) {
  unsigned char byte_read = 0;
  for (int i = 128; i >= 1; i /= 2) {
    if (symbol & i) digitalWrite(laserPin, HIGH);
    else  digitalWrite(laserPin, LOW);
    
    delayMicroseconds(sleepmks);
    //delay(sleepms);

    if ((analogRead(photoresistorPin)) > (laser_on - error))\
      byte_read |= i;
  }
  digitalWrite(laserPin, LOW);
  return byte_read;
}

void loop() {
  char value = 0;
  if (Serial.available() > 0) {
    value = Serial.read();
    char byte_read = send_receive_byte(value);
    Serial.write(byte_read);
  }
}

