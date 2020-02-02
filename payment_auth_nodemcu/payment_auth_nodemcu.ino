#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN 2
#define RST_PIN 0
//#define door 7

//#define outputPin 6    // led indicator connected to digital pin
const int knockSensor = A0; // the piezo is connected to an analog pin
const int thresholdHIGH = 100;  // threshold value to decide when the detected knock is hard (HIGH)
const int thresholdLOW = 50;  // threshold value to decide when the detected knock is gentle (LOW)


const int secretKnockLength = 3; //How many knocks are in your secret knock

/* This is the secret knock sequence
   0 represents a LOW or quiet knock
   1 represents a HIGH or loud knock
   The sequence can be as long as you like, but longer codes increase the difficulty of matching */
const int secretKnock[secretKnockLength] = {1, 1, 1};

int secretCounter = 0; //this tracks the correct knocks and allows you to move through the sequence
int sensorReading = 0; // variable to store the value read from the sensor pin
boolean Switch = 0;
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
const int gate = 7;
void setup()
{
  delay(3000);
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  //pinMode(door, OUTPUT);
  //pinMode(gate, OUTPUT);
  //pinMode(outputPin, OUTPUT);
  sensorReading = analogRead(knockSensor);

  if ( ! mfrc522.PICC_IsNewCardPresent())
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial())
  {
    return;
  }
  String content = "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  if (content.substring(1) == "1A 43 53 A3")
  {
    Serial.println("1");
    Switch = 1;
  }
  else   {
    Serial.println("0");
  }
  int i = 0;
  while (i <= secretCounter) {
    if (Switch) {
      //Serial.println("1");
      if (sensorReading >= thresholdHIGH) {

        //Check to see if a Hard Knock matches the Secret Knock in the correct sequence.
        if (secretKnock[secretCounter] == 1) {

          //The Knock was correct, iterate the counter.
          secretCounter++;
          Serial.println("Correct");

        } else {

          //The Knock was incorrect, reset the counter
          secretCounter = 0;
          Serial.println("Fail - You are a spy!");

        }//close if

        //Allow some time to pass before sampling again to ensure a clear signal.
        delay(100); // 100 miliseconds

        //Gentle knock (LOW) is detected
      } else if (sensorReading >= thresholdLOW) {

        //Check to see if a Gentle Knock matches the Secret Knock in the correct sequence.
        if (secretKnock[secretCounter] == 0) {

          //The Knock was correct, iterate the counter.
          secretCounter++;
          Serial.println("Correct");

        } else {

          //The Knock was incorrect, reset the counter.
          secretCounter = 0;
          Serial.println("Fail - You are a spy!");

        }//close if

        //Allow some time to pass before sampling again to ensure a clear signal.
        delay(100);

      }//close if else

      //Check for successful entry of the code, by seeing if the entire array has been walked through.
      if (secretCounter == (secretKnockLength) ) {

        Serial.println("Welcome in fellow Illuminante!");
        delay(1000);
        secretCounter = 0;
      }//close success check
    }
    i++;
  }
}
void loop() {}
