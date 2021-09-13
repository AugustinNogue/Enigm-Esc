/*
  This code update two values, the fssPressed and enoughWeight.
  The code also handle request made in functions found in the raspberry.py 
  file.
  The code can request a setup and a cleanup wich means a reset of fssPressed and enoughWeight.
  The setup also activate the solenoide and the cleanup deactivate it
  It can also request the status of those two variables and deactivation of the solenoide.
   
  Based on Serial Event example

  When new serial data arrives, this sketch adds it to a String.
  When a newline is received, the loop prints the string and clears it.
  
  created 9 May 2011
  by Tom Igoe

  You can find the base exemple which belong to the public domain at this adress

  http://www.arduino.cc/en/Tutorial/SerialEvent
  

  Based on Example using the SparkFun HX711 breakout board with a scale
  
  By: Nathan Seidle
  SparkFun Electronics
  Date: November 19th, 2014
  License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).
  
  This example demonstrates basic scale output. See the calibration sketch to get the calibration_factor for your
  specific load cell setup.
  
  This example code uses bogde's excellent library: https://github.com/bogde/HX711
  bogde's library is released under a GNU GENERAL PUBLIC LICENSE

  Arduino pin 2 -> HX711 CLK
  3 -> DAT
  5V -> VCC
  GND -> GND
  
  The HX711 board can be powered from 2.7V to 5V so the Arduino 5V power should be fine.
  
*/

#include "HX711.h" //This library can be obtained here http://librarymanager/All#Avia_HX711
#include <assert.h>

#define calibration_factor -7050.0 //This value is obtained using the SparkFun_HX711_Calibration sketc
//Load cell pins :
#define LOADCELL_DOUT_PIN  3 
#define LOADCELL_SCK_PIN  2  

HX711 scale;

int fsrAnalogPin = 0; // FSR is connected to analog 0
int fsrReading;      // the analog reading from the FSR resistor divider
int loadCellReading;

int solenoidPin = 9;// Solenoid Pin

int inputValue = 0;
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complet
String fsrPressed = "false";
String enoughLCWeight = "false";

/*
  Program setup.
*/
void setup() {
  // initialize serial:
  Serial.begin(9600);
  // Scale configuration
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare();  //Assuming there is no weight on the scale at start up, reset the scale to 0
  
  pinMode(solenoidPin, OUTPUT); //Sets solenoid pin as an output
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

/*
  Program loop.
*/
void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    // Status request:
    if (inputString.startsWith("status update")){
      // FSR status request:
      if (inputString.indexOf("fsr") > -1){
        // Send reply regarding the FSR:
        Serial.println("fsr activated: " + fsrPressed);
        }
      // Load cell status request:
      else if (inputString.indexOf("load cell") > -1){
        // Send reply regarding the load cell:
        Serial.println("load cell activated: " + enoughLCWeight);
        }
      else{
        // In case of an invalid request:
        Serial.println("invalid set Command");
        }
      }
    // Setup request:
    else if (inputString.startsWith("setup")){
      fsrPressed = "false"; // Reset fsrPressed
      enoughLCWeight = "false"; // Reset enoughLCWeight
      digitalWrite(solenoidPin, LOW); // Switch Solenoid ON
      }
    // Cleanup request:
    else if (inputString.startsWith("cleanup")){
      fsrPressed = "false"; // Reset fsrPressed
      enoughLCWeight = "false"; // Reset enoughLCWeight
      digitalWrite(solenoidPin, HIGH); // Switch Solenoid OFF
      }
    // Deactivate the solenoide:
    else if (inputString.startsWith("deactivate solenoide")){
      digitalWrite(solenoidPin, HIGH); // Switch Solenoid OFF
      }
    // In case of an invalid request
    else{
      Serial.println("invalid Command");
      }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
  // Check FSR status:
  updateFsr();
  // Check load cell status:
  updateLoadCell();
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
/*
  updateFsr update the fsrPressed variable when the weight pressed on the FSR is
  sufficient.
  The update consist of assigning the string "true" to it when conditions are met.
*/
void updateFsr(){
  assert(fsrPressed == "false" or fsrPressed == "true");
  // Analog read of the FSR:
  fsrReading = analogRead(fsrAnalogPin);
  // If the strenght apply is over 800 units.
  if (fsrReading > 800){
    fsrPressed = "true";
    } 
  }

/*
  updateLoadCell update the enoughLCWeight variable when the weight on the load cell is
  sufficient.
  The update consist of assigning the string "true" to it when conditions are met.
*/
void updateLoadCell(){
  assert(enoughLCWeight == "false" or enoughLCWeight == "true");
  loadCellReading = scale.get_units(); //scale.get_units() returns a float;
  // If the load cell reading value is over 3 kgs:
  if (abs(loadCellReading) > 3){
    enoughLCWeight = "true";
    } 
  }
