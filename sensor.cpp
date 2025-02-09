#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Pin Definitions
#define TRIG_PIN 5
#define ECHO_PIN 18
#define MQ137_PIN 34
#define LED_PIN 2

// Network credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server details
const char* serverUrl = "http://your-server.com/api/update-bin-status";
const String binId = "B001";

// Bin dimensions
const float BIN_HEIGHT = 100.0;
const int READING_INTERVAL = 300000;

// Sensor calibration values
const int MQ137_CLEAN_AIR = 100;
const int MQ137_HIGH_THRESHOLD = 300;
const int MQ137_MED_THRESHOLD = 200;

void setup() {
  Serial.begin(115200);
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(MQ137_PIN, INPUT);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

float measureDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;
  
  return distance;
}

String getOdorLevel() {
  int odorValue = analogRead(MQ137_PIN);
  
  if (odorValue > MQ137_HIGH_THRESHOLD) {
    return "High";
  } else if (odorValue > MQ137_MED_THRESHOLD) {
    return "Medium";
  } else {
    return "Low";
  }
}

String getBinStatus(float fillPercentage) {
  if (fillPercentage > 80) {
    return "Critical";
  } else if (fillPercentage > 60) {
    return "Warning";
  } else {
    return "Normal";
  }
}

void updateServer(float fillPercentage, String odorLevel, String status) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    StaticJsonDocument<200> doc;
    doc["binId"] = binId;
    doc["fillLevel"] = fillPercentage;
    doc["odorLevel"] = odorLevel;
    doc["status"] = status;
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      Serial.printf("HTTP Response code: %d\n", httpResponseCode);
    } else {
      Serial.printf("Error code: %d\n", httpResponseCode);
    }
    
    http.end();
  }
}

void loop() {
  float distance = measureDistance();
  float fillPercentage = 100.0 * (1.0 - (distance / BIN_HEIGHT));
  fillPercentage = constrain(fillPercentage, 0, 100);
  
  String odorLevel = getOdorLevel();
  String status = getBinStatus(fillPercentage);
  
  updateServer(fillPercentage, odorLevel, status);
  
  digitalWrite(LED_PIN, status == "Critical");
  
  delay(READING_INTERVAL);
}