#include <Arduino.h>
#include <HardwareSerial.h>

#define RXD2 16
#define TXD2 17

HardwareSerial mySerial(2);

void setup() {
  Serial.begin(9600);     // USB debug
  mySerial.begin(9600, SERIAL_8N1, RXD2, TXD2);

  Serial.println("ESP32 sender ready");
}

void loop() {
  float current = 0.5;   // Example current in Amps

  String msg = "CURRENT:" + String(current, 2) + "A";
  mySerial.println(msg);

  Serial.print("Sent → Pi: ");
  Serial.println(msg);

  delay(2000);
}
