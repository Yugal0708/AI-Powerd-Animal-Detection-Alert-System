#include <TinyGPS++.h>
#include <SoftwareSerial.h>

// ============ PIN DEFINITIONS ============
#define RED_LED 13        // Red LED for HIGH danger
#define GREEN_LED 12      // Green LED 
#define BUZZER 11         // Buzzer for alerts

// GPS Module (NEO-6M) - Software Serial

#define GPS_RX 4          // Arduino pin 4 connects to GPS TX
#define GPS_TX 3          // Arduino pin 3 connects to GPS RX

// ============ GPS SETUP ============
TinyGPSPlus gps;
SoftwareSerial gpsSerial(GPS_RX, GPS_TX);

// ============ VARIABLES ============
char incomingSignal = 'L';  // Default LOW danger
bool alertActive = false;
unsigned long lastGPSRead = 0;
unsigned long lastGPSSend = 0;
const unsigned long GPS_READ_INTERVAL = 100;   // Read GPS every 100ms (fast)
const unsigned long GPS_SEND_INTERVAL = 2000;  // Send to Python every 2 seconds

void setup() {
  // Initialize serial communication with Python
  Serial.begin(9600);
  
  // Initialize GPS serial
  gpsSerial.begin(9600);
  
  // Setup pins
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  
  // Initial state - Green LED ON, everything else OFF
  digitalWrite(GREEN_LED, HIGH);
  digitalWrite(RED_LED, LOW);
  digitalWrite(BUZZER, LOW);
  
  Serial.println("Arduino Alert System Ready!");
  Serial.println("GPS: Acquiring satellites...");
  Serial.println("IMPORTANT: Place GPS module near window with clear sky view");
}

void loop() {
  // ===== READ SIGNAL FROM PYTHON =====
  if (Serial.available() > 0) {
    incomingSignal = Serial.read();
    handleSignal(incomingSignal);
  }
  
  // ===== ALWAYS READ GPS DATA (continuously) =====
  // This is critical - GPS needs constant reading to acquire and maintain lock
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastGPSRead >= GPS_READ_INTERVAL) {
    lastGPSRead = currentMillis;
    
    // Read all available GPS data
    while (gpsSerial.available() > 0) {
      char c = gpsSerial.read();
      gps.encode(c);
      
      // Debug: uncomment to see raw GPS data
      // Serial.write(c);
    }
  }
  
  // ===== SEND GPS LOCATION PERIODICALLY =====
  // Send GPS status every 2 seconds (or immediately when alert triggered)
  if (currentMillis - lastGPSSend >= GPS_SEND_INTERVAL) {
    lastGPSSend = currentMillis;
    sendGPSLocation();
  }
}

void handleSignal(char signal) {
  switch (signal) {
    case 'H': // HIGH DANGER
      Serial.println("HIGH DANGER DETECTED!");
      digitalWrite(RED_LED, HIGH);
      digitalWrite(GREEN_LED, LOW);
      
      // Loud buzzer - continuous beep pattern
      for (int i = 0; i < 5; i++) {
        digitalWrite(BUZZER, HIGH);
        delay(200);
        digitalWrite(BUZZER, LOW);
        delay(100);
      }
      
      alertActive = true;
      sendGPSLocation(); // Send location immediately
      break;
      
    case 'M': // MEDIUM DANGER
      Serial.println("MEDIUM DANGER DETECTED!");
      digitalWrite(RED_LED, HIGH);
      digitalWrite(GREEN_LED, LOW);
      
      // Medium buzzer - slower beep pattern
      for (int i = 0; i < 3; i++) {
        digitalWrite(BUZZER, HIGH);
        delay(150);
        digitalWrite(BUZZER, LOW);
        delay(150);
      }
      
      alertActive = true;
      sendGPSLocation();
      break;
      
    case 'L': // LOW DANGER or SAFE
      digitalWrite(RED_LED, LOW);
      digitalWrite(GREEN_LED, HIGH);
      digitalWrite(BUZZER, LOW);
      alertActive = false;
      break;
      
    default:
      // Unknown signal - stay in safe mode
      digitalWrite(RED_LED, LOW);
      digitalWrite(GREEN_LED, HIGH);
      digitalWrite(BUZZER, LOW);
      alertActive = false;
      break;
  }
}

void sendGPSLocation() {
  if (gps.location.isValid()) {
    // GPS has a fix!
    Serial.print("GPS:");
    Serial.print(gps.location.lat(), 6);
    Serial.print(",");
    Serial.println(gps.location.lng(), 6);
    
    // Debug info
    Serial.print("Satellites: ");
    Serial.print(gps.satellites.value());
    Serial.print(" | HDOP: ");
    Serial.print(gps.hdop.value());
    Serial.print(" | Age: ");
    Serial.print(gps.location.age());
    Serial.println("ms");
  } else {
    // GPS not ready yet - still searching
    Serial.println("GPS:WAITING");
    Serial.print("Satellites: ");
    Serial.print(gps.satellites.value());
    Serial.print(" | Chars processed: ");
    Serial.print(gps.charsProcessed());
    Serial.print(" | Sentences with fix: ");
    Serial.println(gps.sentencesWithFix());
    
    // Check if GPS is receiving data at all
    if (gps.charsProcessed() < 10) {
      Serial.println("WARNING: No GPS data received! Check wiring:");
      Serial.println("  - GPS TX → Arduino Pin 4");
      Serial.println("  - GPS RX → Arduino Pin 3");
      Serial.println("  - GPS VCC → 5V");
      Serial.println("  - GPS GND → GND");
    }
  }
}