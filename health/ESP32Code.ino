#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>

// WiFi and Server Configuration
const char* ssid = "POSTGRAD";
const char* password = "PG@unzaC$";
const char* serverName = "http://172.16.60.32:8013/api/vitals/create/";

// Sensor Configuration
#define HEART_SENSOR_PIN 34  // Heart rate sensor pin
#define SAMPLE_SIZE 4        // Number of samples for heart rate averaging
#define RISE_THRESHOLD 5     // Threshold for detecting rising signal

// Create MLX90614 instance
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

// Heart Rate Variables
float reads[SAMPLE_SIZE];
float sum = 0;
int ptr = 0;
float last = 0;
float before = 0;
bool rising = false;
int rise_count = 0;
float first = 0;
float second = 0;
float third = 0;
long last_beat = 0;
float current_heart_rate = 0;
bool new_heart_rate = false;

void setup() {
  Serial.begin(115200);
  
  // Initialize I2C for temperature sensor
  Wire.begin(21, 22);
  
  // Initialize temperature sensor
  if (!mlx.begin()) {
    Serial.println("Error initializing MLX90614 sensor!");
    while (1);
  }
  
  // Configure ADC for heart rate sensor
  analogSetWidth(12);
  analogSetAttenuation(ADC_11db);
  
  // Initialize heart rate array
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    reads[i] = 0;
  }
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.println("IP address: " + WiFi.localIP().toString());
}

void updateHeartRate() {
  float reader = 0;
  int n = 0;
  long start = millis();
  
  // Average readings over 20ms
  do {
    reader += analogRead(HEART_SENSOR_PIN);
    n++;
  } while (millis() < start + 20);
  
  reader /= n;
  
  // Update moving average
  sum -= reads[ptr];
  sum += reader;
  reads[ptr] = reader;
  last = sum / SAMPLE_SIZE;
  
  // Detect heartbeat
  if (last > before) {
    rise_count++;
    
    if (!rising && rise_count > RISE_THRESHOLD) {
      rising = true;
      first = millis() - last_beat;
      last_beat = millis();
      
      // Calculate heart rate
      float heart_rate = 60000.0 / (0.4 * first + 0.3 * second + 0.3 * third);
      
      if (heart_rate >= 40 && heart_rate <= 200) {
        current_heart_rate = heart_rate;
        new_heart_rate = true;
        Serial.print("Heart Rate: ");
        Serial.print(current_heart_rate, 1);
        Serial.println(" BPM");
      }
      
      third = second;
      second = first;
    }
  } else {
    rising = false;
    rise_count = 0;
  }
  
  before = last;
  ptr = (ptr + 1) % SAMPLE_SIZE;
}

void sendDataToServer(float temperature, float heart_rate) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    
    // Create JSON with both temperature and heart rate
    String jsonPayload = "{\"temperature\":\"" + String(temperature) + 
                        "\",\"heart_rate\":\"" + String(heart_rate) + "\"}";
    
    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response code: " + String(httpResponseCode));
      Serial.println("Response: " + response);
    } else {
      Serial.println("Error on sending POST: " + String(httpResponseCode));
    }
    
    http.end();
  } else {
    Serial.println("WiFi not connected");
  }
}

void loop() {
  static unsigned long lastSendTime = 0;
  const unsigned long SEND_INTERVAL = 5000; // Send data every 5 seconds
  
  // Update heart rate continuously
  updateHeartRate();
  
  // Send data to server every SEND_INTERVAL milliseconds
  if (millis() - lastSendTime >= SEND_INTERVAL) {
    // Read temperature
    float temperature = mlx.readObjectTempC();
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");
    
    // Send both temperature and heart rate
    sendDataToServer(temperature, current_heart_rate);
    
    lastSendTime = millis();
  }
  
  // Small delay to prevent overwhelming the sensors
  delay(10);
}