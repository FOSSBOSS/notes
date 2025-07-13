#include <Stepper.h>
/*
quick n dirty music box motor control driver
*/
const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

int currentSpeed = 60;

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for Serial Monitor (optional for native USB boards)
  Serial.println("Send digits 0–9 to set speed (0 = stop, 9 = 90 RPM)");
  myStepper.setSpeed(currentSpeed);
}

void loop() {
  // Check for serial input
  if (Serial.available()) {
    char input = Serial.read();

    if (input >= '0' && input <= '9') {
      currentSpeed = (input - '0') * 10;
      myStepper.setSpeed(currentSpeed);
      Serial.print("Speed set to ");
      Serial.print(currentSpeed);
      Serial.println(" RPM");
    }
  }

  // Step only if speed > 0
  if (currentSpeed > 0) {
    myStepper.step(1);  // small step keeps input responsive
  }
}

