#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         5          // Configurable, see typical pin layout above
#define SS_PIN          53         // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

const int pir = 4;
const int ledR = 3;
const int ledB = 2;
const int buzzer = 8;
const int button = 7;
int lock = false;
int pirState = LOW;

void setup() {
	Serial.begin(9600);		// Initialize serial communications with the PC
	while (!Serial);		// Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();		// Init MFRC522
	delay(4);				// Optional delay. Some board do need more time after init to be ready, see Readme
	mfrc522.PCD_DumpVersionToSerial();	// Show details of PCD - MFRC522 Card Reader details
	Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));

  pinMode(ledR, OUTPUT);
  pinMode(ledB, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(button, INPUT_PULLUP);
  pinMode(pir, INPUT);  
}

void loop() {
  if(lock){
    detectMotion();
  }
  
  if (digitalRead(button)== LOW) {
    doorStatus();
    tone(buzzer, 1000);
    delay (200);
    noTone (buzzer);
    toggleLed();
    delay(3000);
  }
  
	if ( ! mfrc522.PICC_IsNewCardPresent()) {return;}

	if ( ! mfrc522.PICC_ReadCardSerial()) {return;}

  //Show UID on serial monitor
  String key= "";
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
  key.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
  key.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  
  key.toUpperCase();
  
  Serial.println();
  Serial.print("key tag is :");
  Serial.print(key);

  Serial.println();
  Serial.print("access :");
  
  
  
  if (key == " 96 D6 90 BB")
  {
    doorStatus();
    tone(buzzer, 1000);
    delay (200);
    noTone (buzzer);
    
    Serial.print("access granted");
    
  } else {
    tone(buzzer, 500);
    delay (1000);
    noTone (buzzer);
    
    Serial.print("access denied");
  }

  toggleLed();
  
  delay(3000);
  Serial.println();
}

void doorStatus(){
  if(!lock){
    lock = true;
  } else if(lock){
    lock = false;
  }
}

void toggleLed(){
  if(!lock){
    digitalWrite(ledR, LOW);
    digitalWrite(ledB, HIGH);
  } else if(lock){
    digitalWrite(ledR, HIGH);
    digitalWrite(ledB, LOW);
  }
}

void detectMotion(){
  int val = digitalRead(pir);  // read input value
  if (val == HIGH) {            // check if the input is HIGH
    if (pirState == LOW) {
      // we have just turned on
      Serial.println("Motion detected!");
      tone(buzzer, 10000);
      delay (3000);
      noTone (buzzer);
      pirState = HIGH;
    }
  } else {
    if (pirState == HIGH){
      // we have just turned of
      Serial.println("Motion ended!");
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }
}
