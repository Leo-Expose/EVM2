#include <EEPROM.h>

// Define the number of candidates
#define NUM_CANDIDATES 6

// Define pin numbers for each button
int buttonPins[NUM_CANDIDATES] = {2, 3, 4, 5, 6, 7};

// Array to hold vote counts
int votes[NUM_CANDIDATES] = {0, 0, 0, 0, 0, 0};

void setup() {
  Serial.begin(9600);
  
  // Initialize button pins as inputs
  for (int i = 0; i < NUM_CANDIDATES; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
  
  // Load vote counts from EEPROM
  for (int i = 0; i < NUM_CANDIDATES; i++) {
    votes[i] = EEPROM.read(i);
  }
}

void loop() {
  for (int i = 0; i < NUM_CANDIDATES; i++) {
    if (digitalRead(buttonPins[i]) == LOW) {
      delay(50); // Debounce delay
      if (digitalRead(buttonPins[i]) == LOW) {
        votes[i]++;
        EEPROM.write(i, votes[i]);
        Serial.print("Vote: ");
        Serial.println(i);
        delay(5000); // Prevent multiple counts from a single press
      }
    }
  }
}
