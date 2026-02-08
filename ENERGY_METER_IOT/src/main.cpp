#include <Arduino.h>
#define DT_OUTPUT_PIN 34

#define CURRENT_PER_VOLT 0.55 // Ampere from Clampmeter/Output Votage from CT

void setup()
{
  Serial.begin(115200);

  analogReadResolution(12);       // 0–4095
  analogSetAttenuation(ADC_11db); // 0–3.3 V
}

void loop()
{
  int adcValue = analogRead(DT_OUTPUT_PIN);

  // Voltage calculation
  float voltage = adcValue * (3.3 / 4095.0) + 0.150; // 150 OFFSET

  // Convert voltage to current
  float current = voltage * CURRENT_PER_VOLT;

  Serial.print("Current: ");
  Serial.print(current, 1); // <<< ONLY 1 digit after decimal
  Serial.println(" A");

  delay(1000);
}
